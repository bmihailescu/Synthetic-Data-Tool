import base64
import copy
import datetime
import json
import random
import re
import secrets
import uuid
import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path

from faker import Faker


_TEMPLATE_PATH = Path(__file__).with_name("v6_bike_templates.json")
_XML_NAMESPACE = "http://www.wisl.co.uk/schemas"
ET.register_namespace("", _XML_NAMESPACE)
_UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-?(?:[0-9a-f]{4}-?){3}[0-9a-f]{12}$", re.I)
_GUID_KEYS = {
    "addressid", "agentid", "breakdownid", "businessid", "clientid", "entityid",
    "paymentplanid", "policydetailsid", "policyid", "productid", "schemeid",
    "telephoneid", "vehicleid",
}
_BIKES = [
    ("YAMAHA", "DT50X", "TRAIL", 50),
    ("DUCATI", "998", "SUPER SPORTS", 998),
    ("AEON", "ECHO 150", "SCOOTER", 149),
    ("ADLY", "ACTIVATOR", "SCOOTER", 125),
    ("YINHUA", "125", "SCOOTER", 125),
    ("HONDA", "CB125F", "ROADSTER", 125),
    ("SUZUKI", "GSX-R600", "SPORTS", 599),
    ("KAWASAKI", "NINJA 650", "SPORTS", 649),
    ("BMW", "R 1250 GS", "ADVENTURE", 1254),
    ("TRIUMPH", "BONNEVILLE T100", "CLASSIC", 900),
    ("ROYAL ENFIELD", "CLASSIC 350", "CLASSIC", 349),
    ("KTM", "390 DUKE", "NAKED", 373),
    ("VESPA", "PRIMAVERA 125", "SCOOTER", 124),
]
_TITLES = [("003", "M"), ("005", "F"), ("009", "M"), ("069", "F")]


@lru_cache(maxsize=1)
def _templates():
    return json.loads(_TEMPLATE_PATH.read_text(encoding="utf-8"))


def _new_id():
    return str(uuid.uuid4()).upper()


def _new_bike():
    make, model, series, cc = random.choice(_BIKES)
    return {
        "Make": make,
        "Model": model,
        "Series": series,
        "CubicCapacity": cc,
        "YearOfManufacture": random.randint(1990, datetime.date.today().year),
        "AbiCode": "".join(random.choices("0123456789", k=8)),
    }


def _new_person(fake):
    title_id, gender_id = random.choice(_TITLES)
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=75)
    return {
        "Forename": fake.first_name_male() if gender_id == "M" else fake.first_name_female(),
        "Surname": fake.last_name(),
        "DateOfBirth": date_of_birth.isoformat() + "T00:00:00",
        "GenderId": gender_id,
        "TitleId": title_id,
        "EmailAddress": fake.email(),
        "Telephone": fake.phone_number(),
        "Address": {
            "HouseName": None,
            "HouseNo": str(random.randint(1, 150)),
            "Postcode": fake.postcode(),
            "Eircode": None,
            "Street": fake.street_name(),
            "Locality": fake.city_suffix(),
            "City": fake.city(),
            "County": fake.county(),
            "CountryId": "GB",
        },
    }


def _random_date(fake, original):
    if original.startswith(("0001-01-01", "1899-12-30")):
        return original
    new_date = fake.date_between(start_date="-75y", end_date="+1y")
    if "T" in original:
        return new_date.isoformat() + "T00:00:00"
    return new_date.isoformat()


def _random_text(value, key, fake, person, bike, policy_number):
    normalized = re.sub(r"[^a-z0-9]", "", key.lower())
    if normalized in ("forename", "firstname", "firstnamevalue"):
        return person["Forename"]
    if normalized in ("surname", "lastname"):
        return person["Surname"]
    if normalized in ("email", "emailaddress") or "email" in normalized:
        return person["EmailAddress"]
    if "telephone" in normalized or normalized in ("phone", "phonenumber"):
        return person["Telephone"]
    if "postcode" in normalized or normalized == "postcode":
        return person["Address"]["Postcode"]
    if normalized in ("street", "house", "houseno", "housename"):
        return person["Address"]["Street"] if normalized == "street" else person["Address"]["HouseNo"]
    if normalized in ("locality", "city", "county"):
        return person["Address"][normalized.title()]
    if normalized in ("make", "abimake"):
        return bike["Make"]
    if normalized in ("model", "abimodel"):
        return bike["Model"]
    if normalized in ("series", "abitype"):
        return bike["Series"]
    if normalized in ("cc", "abicc", "cubiccapacity"):
        return str(bike["CubicCapacity"])
    if normalized in ("yearofmake", "yearofmanufacture"):
        return str(bike["YearOfManufacture"])
    if normalized in ("abicode",):
        return bike["AbiCode"]
    if "policynumber" in normalized:
        return policy_number
    if normalized in ("createdby", "quotecreatedby"):
        return "SYNTHETIC"
    if "licencenumber" in normalized or "drivinglicencenumber" in normalized:
        return "TEST" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    if "registrationnumber" in normalized:
        return fake.license_plate()
    if "date" in normalized or normalized.endswith("since"):
        return _random_date(fake, value)
    if normalized in ("id", "fid") or normalized in _GUID_KEYS or _UUID_PATTERN.match(value):
        return _new_id()
    if normalized == "password":
        return secrets.token_urlsafe(12)
    if normalized == "number":
        return fake.credit_card_number()
    if normalized in ("description", "details", "breakdowndetails", "generalquestiondetails"):
        return fake.sentence()
    if not value:
        return value
    return value


def _randomize_json(value, key, fake, person, bike, policy_number):
    if isinstance(value, dict):
        return {
            child_key: _randomize_json(child, child_key, fake, person, bike, policy_number)
            for child_key, child in value.items()
        }
    if isinstance(value, list):
        return [_randomize_json(child, key, fake, person, bike, policy_number) for child in value]
    if isinstance(value, bool):
        return random.choice([True, False])
    if isinstance(value, int) and not isinstance(value, bool):
        normalized = re.sub(r"[^a-z0-9]", "", key.lower())
        if normalized in ("cubiccapacity", "abicc"):
            return bike["CubicCapacity"]
        if normalized in ("yearofmanufacture", "yearofmake"):
            return bike["YearOfManufacture"]
        if normalized in ("permanentreferencenumber", "objectid"):
            return random.randint(1, 4)
        if normalized in ("annualmileage",):
            return random.randrange(500, 15001, 500)
        if normalized in ("businessmileage",):
            return random.randrange(0, 5001, 500)
        if normalized in ("currentmileage",):
            return random.randrange(0, 100001, 1000)
        if normalized in ("premium", "targetpremium"):
            return random.randint(100, 2500)
        return value
    if isinstance(value, float):
        normalized = re.sub(r"[^a-z0-9]", "", key.lower())
        if any(term in normalized for term in ("premium", "value", "amount", "excess")):
            return round(random.uniform(0, 30000), 2)
        return value
    if isinstance(value, str):
        return _random_text(value, key, fake, person, bike, policy_number)
    return value


def _randomize_person(person_data, fake, person=None, bike=None, policy_number=""):
    person = person or _new_person(fake)
    result = _randomize_json(person_data, "", fake, person, bike, policy_number)
    for key, value in person.items():
        if key in result:
            result[key] = value
    if isinstance(result.get("Address"), dict):
        for key, value in person["Address"].items():
            if key in result["Address"]:
                result["Address"][key] = value
    return result


def _randomize_risk_data(risk_data, fake, bike, policy_number):
    result = _randomize_json(risk_data, "", fake, _new_person(fake), bike, policy_number)
    proposer = _randomize_person(risk_data["Proposer"], fake, bike=bike, policy_number=policy_number)
    result["Proposer"] = proposer
    result["Riders"] = [
        _randomize_person(rider, fake, bike=bike, policy_number=policy_number)
        for rider in risk_data.get("Riders", [])
    ]
    if result["Riders"]:
        for key in ("Forename", "Surname", "DateOfBirth", "GenderId", "TitleId", "EmailAddress", "Address"):
            if key in result["Riders"][0] and key in proposer:
                result["Riders"][0][key] = copy.deepcopy(proposer[key])

    vehicles = result.get("Vehicles", [])
    for vehicle in vehicles:
        for key in ("Make", "Model", "Series", "CubicCapacity", "YearOfManufacture", "AbiCode"):
            if key in vehicle:
                vehicle[key] = bike[key]
    return result


def _randomize_xml(xml_text, fake, person, bike, policy_number):
    root = ET.fromstring(xml_text)
    for element in root.iter():
        tag = element.tag.rsplit("}", 1)[-1]
        element.text = _random_text(element.text or "", tag, fake, person, bike, policy_number)
        for name, value in list(element.attrib.items()):
            if name in ("iD", "fID") or _UUID_PATTERN.match(value):
                element.set(name, _new_id())
    return '<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(root, encoding="unicode")


def _build_record(template, fake):
    record = copy.deepcopy(template["record"])
    bike = _new_bike()
    policy_number = "124/001/" + secrets.token_hex(3).upper() + "/AFG"
    person = _new_person(fake)
    risk_data = _randomize_risk_data(
        json.loads(record["RiskData"]), fake, bike, policy_number
    )
    record["RiskData"] = json.dumps(risk_data, separators=(",", ":"), ensure_ascii=False)
    record["ClientXml"] = _randomize_xml(
        record["ClientXml"], fake, risk_data["Proposer"], bike, policy_number
    )
    record["Credentials"]["$value"] = base64.b64encode(secrets.token_bytes(12)).decode("ascii")
    record["ProductAccessTokens"]["$values"] = [secrets.token_hex(12)]
    record["ClientReference"] = fake.bothify(text="##########")
    record["CallerId"] = _new_id().replace("-", "").lower()
    record["SoftwareHouseId"] = _new_id().replace("-", "").lower()
    record["QuoteDate"] = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")

    other_inputs = record.get("OtherInputs", {})
    for key in ("POLICY_NUMBER", "POLICYNUMBER"):
        if key in other_inputs:
            other_inputs[key] = policy_number
    if "CLIENT_XML_PREMIUMS" in other_inputs:
        premium = round(random.uniform(100, 2500), 2)
        other_inputs["CLIENT_XML_PREMIUMS"] = json.dumps({
            "PREMIUM": str(premium),
            "PREMIUM_BEFORE_IPT": str(round(premium / 1.12, 2)),
            "PREMIUM_INCLUDING_APR": str(premium),
        })
    return record


def generate_v6_bike_records(record_count):
    if record_count < 1:
        raise ValueError("Record count must be at least 1.")
    templates = _templates()
    if not templates:
        raise ValueError("No V6 bike schema templates are available.")
    fake = Faker("en_GB")
    return [_build_record(random.choice(templates), fake) for _ in range(record_count)]