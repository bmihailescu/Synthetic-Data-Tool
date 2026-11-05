import json
import io
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

from django.test import TestCase


class V6BikeGenerationTests(TestCase):
	@staticmethod
	def _json_paths(value, prefix=""):
		paths = set()
		if isinstance(value, dict):
			for key, child in value.items():
				child_path = f"{prefix}.{key}" if prefix else key
				paths.add(child_path)
				paths.update(V6BikeGenerationTests._json_paths(child, child_path))
		elif isinstance(value, list):
			for child in value:
				paths.update(V6BikeGenerationTests._json_paths(child, prefix + "[]"))
		return paths

	@staticmethod
	def _xml_paths(element, prefix=""):
		tag = element.tag.rsplit("}", 1)[-1]
		path = f"{prefix}/{tag}"
		paths = {path, *(f"{path}/@{name}" for name in element.attrib)}
		for child in element:
			paths.update(V6BikeGenerationTests._xml_paths(child, path))
		return paths

	def test_home_page_exposes_schema_mode_selector(self):
		response = self.client.get("/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'id="schema_mode"')
		self.assertContains(response, 'name="schema_category"')
		self.assertContains(response, 'value="data_analytics"')
		self.assertContains(response, 'value="api_tests"')
		self.assertContains(response, "Data and Analytics")
		self.assertContains(response, "API Tests")
		self.assertContains(response, 'id="v6_schema_mode"')
		self.assertContains(response, 'id="aviva_schema_mode"')
		self.assertContains(response, 'value="v6_bike"')
		self.assertContains(response, 'value="aviva_integration"')
		self.assertContains(response, 'id="manual-schema-fields"')
		self.assertContains(response, 'id="saved-schema-select"')
		self.assertContains(response, 'id="saved-schema-preview"')
		self.assertContains(response, 'id="json_multiple_entries"')
		self.assertContains(response, 'value="yes"')
		self.assertContains(response, 'value="no"')

	def test_v6_mode_returns_requested_json_records(self):
		response = self.client.post(
			"/",
			{"schema_mode": "v6_bike", "num_of_entries": "2"},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/json")
		self.assertIn("SyntheticV6Bike.json", response["Content-Disposition"])

		records = json.loads(response.content)
		self.assertEqual(len(records), 2)
		self.assertTrue(all(record["$type"].startswith("TransactorProxy.Domain.TransactorOptions") for record in records))
		templates = json.loads(
			Path(__file__).with_name("v6_bike_templates.json").read_text()
		)
		expected_risk_paths = self._json_paths(
			json.loads(templates[0]["record"]["RiskData"])
		)
		expected_xml_paths = [
			self._xml_paths(ET.fromstring(template["record"]["ClientXml"]))
			for template in templates
		]
		for record in records:
			risk_data = json.loads(record["RiskData"])
			self.assertTrue(risk_data["Vehicles"])
			self.assertEqual(self._json_paths(risk_data), expected_risk_paths)
			self.assertIn("MyLicence", risk_data["Riders"][0])
			self.assertTrue(risk_data["Proposer"]["EntityId"])
			self.assertTrue(risk_data["AgentId"])
			self.assertTrue(record["Credentials"]["$value"])
			self.assertTrue(record["ProductAccessTokens"]["$values"][0])
			self.assertIn('<client xmlns="http://www.wisl.co.uk/schemas"', record["ClientXml"])
			self.assertNotIn("ns0:", record["ClientXml"])
			xml = ET.fromstring(record["ClientXml"])
			self.assertEqual(
				xml.tag,
				"{http://www.wisl.co.uk/schemas}client",
			)
			self.assertIn(self._xml_paths(xml), expected_xml_paths)

	def test_v6_mode_without_multiple_entries_returns_one_json_file_per_client(self):
		response = self.client.post(
			"/",
			{
				"schema_mode": "v6_bike",
				"num_of_entries": "5",
				"json_multiple_entries": "no",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/zip")
		self.assertIn("SyntheticV6Bike.zip", response["Content-Disposition"])
		with ZipFile(io.BytesIO(response.content)) as archive:
			filenames = archive.namelist()
			self.assertEqual(len(filenames), 5)
			self.assertEqual(len(set(filenames)), 5)
			self.assertTrue(all(name.endswith(".json") for name in filenames))
			for filename in filenames:
				self.assertIsInstance(json.loads(archive.read(filename)), dict)

	def test_aviva_mode_returns_count_files_for_each_template(self):
		response = self.client.post(
			"/",
			{"schema_mode": "aviva_integration", "num_of_entries": "2"},
		)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response["Content-Type"], "application/zip")
		self.assertIn("Aviva.IntegrationTests.zip", response["Content-Disposition"])
		templates = json.loads(
			(Path(__file__).with_name("aviva_integration_templates.json")).read_text()
		)
		template_paths = {
			item["name"]: self._json_paths(item["record"])
			for item in templates
		}
		with ZipFile(io.BytesIO(response.content)) as archive:
			filenames = archive.namelist()
			self.assertEqual(len(filenames), 44)
			self.assertEqual(len(set(filenames)), 44)
			counts = Counter(filename.rsplit("_", 1)[0] for filename in filenames)
			self.assertEqual(set(counts), set(template_paths))
			self.assertTrue(all(count == 2 for count in counts.values()))
			for filename in filenames:
				name = filename.rsplit("_", 1)[0]
				record = json.loads(archive.read(filename))
				self.assertEqual(self._json_paths(record), template_paths[name])

	def test_v6_mode_rejects_non_positive_record_count(self):
		response = self.client.post(
			"/",
			{"schema_mode": "v6_bike", "num_of_entries": "0"},
		)

		self.assertEqual(response.status_code, 400)

# Create your tests here.
