import base64
import datetime
import json
import random
import secrets
import uuid
import xml.etree.ElementTree as ET

from faker import Faker


_NAMESPACE = "http://www.wisl.co.uk/schemas"
ET.register_namespace("", _NAMESPACE)

_BIKES = [
    ("YAMAHA", "DT50X", "TRAIL", 50),
    ("DUCATI", "998", "SUPER SPORTS", 998),
    ("AEON", "ECHO 150", "SCOOTER", 149),
    ("ADLY", "ACTIVATOR", "SCOOTER", 125),
    ("HONDA", "CB125F", "ROADSTER", 125),
    ("SUZUKI", "GSX-R600", "SPORTS", 599),
    ("KAWASAKI", "NINJA 650", "SPORTS", 649),
    ("BMW", "R 1250 GS", "ADVENTURE", 1254),
    ("TRIUMPH", "BONNEVILLE T100", "CLASSIC", 900),
    ("ROYAL ENFIELD", "CLASSIC 350", "CLASSIC", 349),
    ("KTM", "390 DUKE", "NAKED", 373),
    ("VESPA", "PRIMAVERA 125", "SCOOTER", 124),
]

_TITLES = [("003", "Male"), ("005", "Female"), ("009", "Male"), ("069", "Female")]
_MARITAL_STATUSES = ["S", "M", "D", "P", "B"]
_RELATIONSHIPS = [("P", True), ("W", False), ("A", False), ("L", False)]
_OCCUPATIONS = [("A42", "139"), ("B76", "189"), ("M01", "036"), ("001", "188")]


def _id():
    return uuid.uuid4().hex.upper()


def _iso_date(value):
    return value.isoformat()


def _person(fake, relationship, permanent_reference):
    title_id, gender = random.choice(_TITLES)
    first_name = fake.first_name_male() if gender == "Male" else fake.first_name_female()
    surname = fake.last_name()
    date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=75)
    occupation_id, employer_id = random.choice(_OCCUPATIONS)
    address = _address(fake)
    entity_id = _id()

    return {
        "Address": address,
        "ProposerType": "P" if relationship == "P" else "R",
        "CreditChecksConsent": random.choice([True, False]),
        "UKResidenceMonths": random.randrange(12),
        "OtherInsurances": [],
        "TitleId": title_id,
        "Forename": first_name,
        "Surname": surname,
        "DateOfBirth": _iso_date(date_of_birth),
        "GenderId": "M" if gender == "Male" else "F",
        "EmailAddress": fake.email(),
        "MotherMaidenName": fake.last_name(),
        "MaritalStatusId": random.choice(_MARITAL_STATUSES),
        "CriminalConvictions": False,
        "CountyCourtJudgements": False,
        "UKResidenceDate": _iso_date(date_of_birth),
        "UKResidenceYears": random.randint(1, max(1, datetime.date.today().year - date_of_birth.year)),
        "YearsAtMainAddress": random.randint(0, 20),
        "HomeOwner": random.choice([True, False]),
        "DwellingTypeId": random.choice(["01", "02", "03"]),
        "Smoker": random.choice([True, False]),
        "Teetotal": random.choice([True, False]),
        "CreditCardHolder": random.choice([True, False]),
        "ChildrenUnder18": random.choice([True, False]),
        "RegisteredDisabled": False,
        "Occupations": [{
            "OccupationId": occupation_id,
            "EmployersBusinessId": employer_id,
            "EmploymentStatusId": random.choice(["E", "S", "R"]),
            "PartTime": random.choice([True, False]),
        }],
        "HomeOwnershipType": random.choice(["3HOAGEK9", "2HOAGEK9", None]),
        "ConcurrentClientSince": "1899-12-30T00:00:00",
        "ResidentSinceBirth": random.choice([True, False]),
        "MonthsAtMainAddress": random.randrange(12),
        "PermanentReferenceNumber": permanent_reference,
        "Telephone": fake.phone_number(),
        "BusinessTelephone": None,
        "ObjectId": None,
        "EntityId": entity_id,
        "_relationship": relationship,
        "_title_id": title_id,
        "_gender": gender,
    }


def _address(fake):
    address_lines = fake.address().splitlines()
    return {
        "HouseName": None,
        "HouseNo": str(random.randint(1, 150)) + " " + fake.street_name(),
        "Postcode": fake.postcode(),
        "Eircode": None,
        "Street": fake.street_name(),
        "Locality": fake.city_suffix(),
        "City": fake.city(),
        "County": fake.county(),
        "CountryId": "GB",
    }


def _rider(fake, relationship, permanent_reference):
    person = _person(fake, relationship, permanent_reference)
    rider = {key: value for key, value in person.items() if not key.startswith("_")}
    rider.update({
        "ObjectId": str(permanent_reference),
        "RelationshipId": relationship,
        "DatePassedTest": _iso_date(fake.date_between(start_date="-45y", end_date="-1y")),
        "LicenceTypeId": random.choice(["F", "P"]),
        "LicenceRestrictionsId": random.choice(["0", "8"]),
        "LicenceCountryOfIssue": "023",
        "LicenceNumber": "TEST" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8)),
        "MainUser": relationship == "P",
        "DrivingFrequency": [],
        "AccessToOtherVehicles": random.choice([True, False]),
        "VehiclesOwned": random.randint(0, 3),
        "VehiclesDriven": random.randint(0, 3),
        "VehiclesAvailableToFamily": random.randint(0, 3),
        "ClubMember": random.choice([True, False]),
        "VehicleUseId": random.choice(["01", "04", "0"]),
        "InsurancePreviouslyRefused": False,
        "InsuranceTermsApplied": False,
        "InsuranceCancelled": False,
        "ProsecutionPending": False,
        "MotoringOrganisationId": random.choice(["0", "99"]),
        "DisabledBadgeHolder": False,
        "CompanyCar": {
            "CompanyCarNcd": 0,
            "CompanyCarUsageId": "0",
            "CompanyCarExpiryDate": "1899-12-30T00:00:00",
        },
        "DeclaredBankrupt": False,
        "Claims": [],
        "Convictions": [],
        "Qualifications": [],
        "MedicalConditions": [],
        "PassCBT": random.choice([True, False]),
        "PassCBTDate": _iso_date(fake.date_between(start_date="-20y", end_date="today")),
        "A2LicensePassed": random.choice([True, False]),
        "DateA2Passed": "1899-12-30T00:00:00",
        "PreviousExperience": {
            "havePreviousExperiance": random.choice([True, False]),
            "Years": random.randint(0, 30),
            "DateFrom": "1899-12-30T00:00:00",
            "DateTo": "1899-12-30T00:00:00",
            "CC": "0",
            "AbiCode": "0",
            "Make": "",
            "Model": "",
        },
        "OtherVehicleNcdYears": random.randint(0, 15),
        "OtherVehicleVehicleType": None,
    })
    return rider


def _vehicle(fake, vehicle_index):
    make, model, series, cc = random.choice(_BIKES)
    year = random.randint(1990, datetime.date.today().year)
    postcode = fake.postcode()
    price = random.randrange(500, 30001, 100)
    vehicle_id = _id()
    return {
        "SideCar": random.choice([True, False]),
        "KeptAtHome": random.choice([True, False]),
        "Group": str(random.randint(1, 20)),
        "AbiCode": "".join(random.choices("0123456789", k=8)),
        "Make": make,
        "Model": model,
        "Series": series,
        "NoOfSeats": random.choice([1, 2]),
        "CubicCapacity": cc,
        "YearOfManufacture": year,
        "BodyTypeId": random.choice(["M1", "M2"]),
        "FuelTypeId": random.choice(["002", "003"]),
        "GearboxId": random.choice(["001", "002"]),
        "ColourId": random.choice(["0", "1", "2", "3"]),
        "QPlated": False,
        "QPlatedReasonId": "0",
        "RegistrationNumber": "" if random.choice([True, False]) else fake.license_plate(),
        "PersonalisedPlate": False,
        "OwnerId": str(vehicle_index),
        "KeeperId": str(vehicle_index),
        "EstimatedValue": float(price),
        "ValueCodeId": "M",
        "PricePaid": float(price),
        "PurchaseDate": _iso_date(fake.date_between(start_date="-15y", end_date="today")),
        "RegisteredDate": _iso_date(fake.date_between(start_date=f"-{datetime.date.today().year - year}y", end_date="today")),
        "Imported": random.choice([True, False]),
        "CountryOfRegistrationId": "023",
        "AnnualMileage": random.randrange(500, 15001, 500),
        "BusinessMileage": random.randrange(0, 5001, 500),
        "CurrentMileage": random.randrange(0, 100001, 1000),
        "OvernightParkingId": random.choice(["0", "1", "2"]),
        "LastMotDate": "0001-01-01T00:00:00",
        "CoverTypeId": random.choice(["01", "02"]),
        "VoluntaryExcess": float(random.choice([0, 100, 150, 300, 500])),
        "RightHandDrive": True,
        "VehicleUses": [{"UseCode": "04", "Drivers": [str(vehicle_index)]}],
        "NcdDetails": {
            "Years": float(random.randint(0, 15)),
            "NcdReasonId": "0",
            "EntitlementReasonId": "8",
            "TypeId": "0",
            "CountryEarnedId": "GB",
            "Protected": random.choice([True, False]),
            "DateExpiry": _iso_date(fake.date_between(start_date="today", end_date="+1y")),
            "ClaimedPercent": 0.0,
        },
        "OtherNcdDetails": {
            "Years": 0,
            "TypeId": "MC",
            "YearsClaimFree": 0,
            "InsurerId": "998",
            "OtherVehicleDrivingRestrictions": "0",
            "IsPolicyStillCurrent": False,
        },
        "GarageAddress": {
            "HouseName": None,
            "HouseNo": str(random.randint(1, 150)),
            "Postcode": postcode,
            "Eircode": None,
            "Street": fake.street_name(),
            "Locality": fake.city_suffix(),
            "City": fake.city(),
            "County": fake.county(),
            "CountryId": "GB",
        },
        "Accessories": [],
        "Modifications": [],
        "SecurityDevices": [{
            "TypeId": random.choice(["001", "039", "496"]),
            "FittedbyId": random.choice(["1", "2", "4"]),
            "DateFitted": "1899-12-30T00:00:00",
            "CertificateSeen": False,
        }],
        "WrittenOffCategory": "0",
        "Pillion": random.choice([True, False]),
        "PillionFrequencyId": random.choice(["0", "3CBM9T15"]),
        "StorageStructureId": "STRSTC01",
        "GaragingStructure": None,
        "KeptResidential": random.choice([True, False]),
        "DistanceMeasurementId": "0",
        "DistanceMeasurementUnitsId": "0",
        "VehicleCheckId": "0",
        "KeptCommutingId": random.choice(["0", "1"]),
        "CommutingGarageAlarmed": random.choice([True, False]),
        "CommuntingGarage": {"HouseName": None, "HouseNo": "", "Postcode": postcode,
                             "Eircode": None, "Street": "", "Locality": "", "City": "",
                             "County": "", "CountryId": "GB"},
        "HasCameraMounted": False,
        "UseId": "01",
        "PermanentReferenceNumber": vehicle_index,
        "ValueReasonId": "0",
        "ObjectId": None,
        "EntityId": vehicle_id,
    }


def _build_risk_data(fake):
    proposer = _person(fake, "P", 1)
    riders = [_rider(fake, relationship, index) for index, (relationship, _) in enumerate(
        random.sample(_RELATIONSHIPS[1:], random.randint(0, len(_RELATIONSHIPS) - 1)), start=2
    )]
    proposer_fields = {key: value for key, value in proposer.items() if not key.startswith("_")}
    riders.insert(0, _rider_from_proposer(proposer))
    vehicles = [_vehicle(fake, index) for index in range(1, random.randint(2, 3))]
    start_date = fake.date_between(start_date="today", end_date="+180d")
    end_date = start_date + datetime.timedelta(days=365)

    return {
        "Proposer": proposer_fields,
        "Riders": riders,
        "Vehicles": vehicles,
        "Cover": {
            "CoverPeriodUnits": "2",
            "CoverPeriod": 12,
            "DrivingRestrictionId": random.choice(["0", "9"]),
            "CoverStartDate": _iso_date(start_date),
            "PreviousInsurance": {
                "PreviousExpiryDate": _iso_date(start_date),
                "PreviousPolicyNumber": "TBA",
                "PreviousInsurerId": str(random.randint(1, 999)),
                "PreviousPaymentRegularity": "06",
                "YearsWithCurrentInsurer": random.randint(0, 15),
            },
        },
        "PreviousPolicyPremium": round(random.uniform(100, 2500), 2),
        "InsurerRatingFactor": [],
        "MarketingReference": "",
        "PrefferedContactMethod": random.choice(["3EHPHID7", "EMAIL"]),
        "InceptionDate": _iso_date(start_date),
        "StartDate": _iso_date(start_date),
        "EndDate": _iso_date(end_date),
        "CreatedDate": datetime.datetime.now().replace(microsecond=0).isoformat(),
        "IntermediaryId": "A03575",
        "IntermediaryReference": "1001",
        "SupplierId": "40",
        "CreditScore": "QUER0999;",
        "SourceOfBusinessId": "YahCAL01",
        "BusinessSourceCode": None,
        "DataSourceId": "002",
        "CampaignId": "3RFUV034",
        "ActivityId": "3LIS9C48",
        "AgentDescription": "1001",
        "SubAgentId": "",
        "IntroducerId": [],
        "AgentId": _id(),
        "BrokerSourceOfBusinessId": "002",
        "TargetPremium": round(random.uniform(100, 2500), 2),
        "GdprConsents": [],
        "HistoryId": None,
        "PolicyDetailsId": _id(),
        "SourceOriginator": "0",
        "DocumentsRequired": False,
        "CompanySchemeCode": None,
        "PolicyLengthId": "SLPL001Y",
        "YearsWithIntermediary": random.randint(0, 20),
        "BusinessPostcode": None,
    }


def _rider_from_proposer(person):
    relationship = person["_relationship"]
    rider = {key: value for key, value in person.items() if not key.startswith("_")}
    rider.update({
        "ObjectId": "1",
        "RelationshipId": relationship,
        "DatePassedTest": "2016-01-01",
        "LicenceTypeId": "F",
        "LicenceRestrictionsId": "8",
        "LicenceCountryOfIssue": "023",
        "LicenceNumber": "TEST" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8)),
        "MainUser": True,
        "DrivingFrequency": [],
        "AccessToOtherVehicles": True,
        "VehiclesOwned": 1,
        "VehiclesDriven": 1,
        "VehiclesAvailableToFamily": 1,
        "ClubMember": False,
        "VehicleUseId": "04",
        "InsurancePreviouslyRefused": False,
        "InsuranceTermsApplied": False,
        "InsuranceCancelled": False,
        "ProsecutionPending": False,
        "MotoringOrganisationId": "99",
        "DisabledBadgeHolder": False,
        "CompanyCar": {"CompanyCarNcd": 0, "CompanyCarUsageId": "0", "CompanyCarExpiryDate": "1899-12-30T00:00:00"},
        "DeclaredBankrupt": False,
        "Claims": [],
        "Convictions": [],
        "Qualifications": [],
        "MedicalConditions": [],
        "PassCBT": True,
        "PassCBTDate": "2015-01-01",
        "A2LicensePassed": False,
        "DateA2Passed": "1899-12-30T00:00:00",
        "PreviousExperience": {"havePreviousExperiance": False, "Years": 0, "DateFrom": "1899-12-30T00:00:00",
                               "DateTo": "1899-12-30T00:00:00", "CC": "0", "AbiCode": "0", "Make": "", "Model": ""},
        "OtherVehicleNcdYears": 0,
        "OtherVehicleVehicleType": None,
    })
    return rider


def _add(parent, name, value=None, attributes=None):
    element = ET.SubElement(parent, "{%s}%s" % (_NAMESPACE, name), attributes or {})
    if value is not None:
        element.text = str(value)
    return element


def _build_client_xml(risk_data, record_id, policy_id, policy_number, start_date):
    proposer = risk_data["Proposer"]
    address = proposer["Address"]
    vehicle = risk_data["Vehicles"][0]
    root = ET.Element("{%s}client" % _NAMESPACE, {"iD": record_id, "hID": "1"})
    for name, value in (
        ("businessTypeID", "0"), ("clientHistory", "false"), ("clientReference", ""),
        ("company", "false"), ("dateEstablished", "1899-12-30T00:00:00.00000"),
        ("dateOfBirth", proposer["DateOfBirth"]), ("deceased", "false"),
        ("dwellingID", "01"), ("dwellingStatusID", proposer["HomeOwnershipType"] or "3HOAGEK9"),
        ("eMail", proposer["EmailAddress"]), ("forename", proposer["Forename"]),
        ("portfoliokey", "124"), ("sex", "Male" if proposer["GenderId"] == "M" else "Female"),
        ("surname", proposer["Surname"]), ("titleID", proposer["TitleId"]),
        ("creditCheckConsent", "CRCK0003"),
    ):
        _add(root, name, value)

    xml_address = _add(root, "address", attributes={"iD": _id(), "hID": "1", "fID": record_id})
    for name, key in (("house", "HouseNo"), ("street", "Street"), ("locality", "Locality"),
                      ("city", "City"), ("county", "County"), ("country", "CountryId"),
                      ("postcode", "Postcode")):
        _add(xml_address, name, address.get(key, ""))
    _add(xml_address, "countryID", "0")

    business = _add(root, "business", attributes={"iD": _id(), "hID": "1", "fID": record_id})
    _add(business, "businessDescID", "0")
    _add(business, "businessDesc", "")
    _add(business, "companyRegistrationNo", "")
    _add(business, "vatRegistered", "false")
    _add(business, "webSite", "")

    policies = _add(root, "policies")
    policy = _add(policies, "policy", attributes={"iD": policy_id, "hID": "1"})
    for name, value in (
        ("accepted", "false"), ("activityID", "3LIS9C48"), ("adminFee", "25"),
        ("agentReference", "1001"), ("authorisationDate", start_date + "T00:00:00.00000"),
        ("businessSourceCodeID", "002"), ("campaignID", "3RFUV034"),
        ("createdBy", "SYNTHETIC"), ("createdDate", datetime.datetime.now().replace(microsecond=0).isoformat()),
        ("currencyID", "1"), ("insurerID", "52"), ("live", "false"),
        ("policyEndDate", (datetime.date.fromisoformat(start_date) + datetime.timedelta(days=365)).isoformat()),
        ("policyInceptionDate", start_date), ("policyNumber", policy_number),
        ("policyStartDate", start_date), ("policyStatusID", "3AJPUL75"), ("policyType", "25"),
        ("portfoliokey", "124"), ("premium", "0"), ("productType", "25"),
        ("sourceBusinessID", "YahCAL01"),
    ):
        _add(policy, name, value)

    insured_parties = _add(policy, "insuredParties")
    for rider_data in risk_data["Riders"]:
        insured = _add(insured_parties, "insuredParty", attributes={
            "iD": rider_data["EntityId"], "hID": "1", "fID": policy_id,
        })
        for name, value in (
            ("client", "true" if rider_data["RelationshipId"] == "P" else "false"),
            ("dateOfBirth", rider_data["DateOfBirth"]), ("forename", rider_data["Forename"]),
            ("surname", rider_data["Surname"]), ("sex", "Male" if rider_data["GenderId"] == "M" else "Female"),
            ("titleID", rider_data["TitleId"]), ("relationshipID", rider_data["RelationshipId"]),
            ("permanentReferenceNumber", rider_data["PermanentReferenceNumber"]),
            ("homeOwner", str(rider_data["HomeOwner"]).lower()),
        ):
            _add(insured, name, value)

    motor = _add(policy, "motor")
    _add(motor, "coverID", "01")
    _add(motor, "noClaimsBonus", vehicle["NcdDetails"]["Years"])
    vehicles = _add(motor, "vehicles")
    xml_vehicle = _add(vehicles, "vehicle", attributes={
        "iD": vehicle["EntityId"], "hID": "1", "fID": policy_id,
    })
    for name, value in (
        ("annualMileage", vehicle["AnnualMileage"]), ("bodyTypeID", vehicle["BodyTypeId"]),
        ("derivedClassOfUseID", "001"), ("keeperID", vehicle["KeeperId"]),
        ("keptAtHome", str(vehicle["KeptAtHome"]).lower()), ("ownershipID", "1"),
        ("pricePaid", vehicle["PricePaid"]), ("purchaseDate", vehicle["PurchaseDate"]),
        ("registeredDate", vehicle["RegisteredDate"]), ("value", vehicle["EstimatedValue"]),
        ("vehicleCoverID", vehicle["CoverTypeId"]), ("vehicleFuelID", vehicle["FuelTypeId"]),
        ("vehicleGearboxID", vehicle["GearboxId"]), ("yearOfMake", str(vehicle["YearOfManufacture"])),
    ):
        _add(xml_vehicle, name, value)
    motorcycle = _add(xml_vehicle, "motorcycle", attributes={"iD": vehicle["EntityId"], "hID": "1", "fID": vehicle["EntityId"]})
    for name, key in (("aBICC", "CubicCapacity"), ("aBICode", "AbiCode"), ("aBIFuel", "FuelTypeId"),
                      ("aBIMake", "Make"), ("aBIModel", "Model"), ("aBIType", "Series"),
                      ("pillion", "Pillion")):
        value = vehicle[key]
        _add(motorcycle, name, str(value).lower() if isinstance(value, bool) else value)

    return '<?xml version="1.0" encoding="utf-8"?>' + ET.tostring(root, encoding="unicode")


def _build_record(fake):
    risk_data = _build_risk_data(fake)
    record_id = _id()
    policy_id = _id()
    policy_number = "124/001/" + secrets.token_hex(3).upper()
    target_premium = round(random.uniform(100, 2500), 2)
    start_date = risk_data["Cover"]["CoverStartDate"]
    return {
        "$type": "TransactorProxy.Domain.TransactorOptions, TransactorProxy.Domain",
        "ClientXml": _build_client_xml(risk_data, record_id, policy_id, policy_number, start_date),
        "SchemeIntermediary": "A03575",
        "ProductType": 25,
        "EnrichmentsXml": "<response><insurer><capstone><enrichmentData>QUER0999</enrichmentData></capstone><scheme>ALL</scheme></insurer></response>",
        "Credentials": {"$type": "System.Byte[], System.Private.CoreLib", "$value": base64.b64encode(secrets.token_bytes(12)).decode("ascii")},
        "ProductAccessTokens": {
            "$type": "System.Collections.Generic.List`1[[System.String, System.Private.CoreLib]], System.Private.CoreLib",
            "$values": [secrets.token_hex(12)],
        },
        "RiskData": json.dumps(risk_data, separators=(",", ":")),
        "ClientReference": fake.bothify(text="##########"),
        "CallerId": secrets.token_hex(12),
        "QuoteDate": datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z"),
        "QuoteType": "New Business",
        "SoftwareHouseId": _id().lower(),
        "PreQuoteDataEnrichment": {
            "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.Object, System.Private.CoreLib]], System.Private.CoreLib",
        },
        "OtherInputs": {
            "$type": "System.Collections.Generic.Dictionary`2[[System.String, System.Private.CoreLib],[System.String, System.Private.CoreLib]], System.Private.CoreLib",
            "capstone_ALL": "QUER0999",
            "POLICY_NUMBER": policy_number,
            "POLICY_STATUS_ID": "3AJPUL75",
            "QUOTE_CREATED_BY": "SYNTHETIC",
            "CLIENT_XML_PREMIUMS": json.dumps({
                "PREMIUM": str(target_premium),
                "PREMIUM_BEFORE_IPT": str(round(target_premium / 1.12, 2)),
                "PREMIUM_INCLUDING_APR": str(target_premium),
            }),
            "PAYMENT_PLAN_ID": _id(),
            "MTA_START_DATE": start_date + "T00:00:00.00000",
            "OriginalInceptionDate": "1899-12-30T00:00:00",
            "AggregatorURN": "",
            "TargetPremium_insurerID": "BEMOT",
            "TargetPremium_premium": str(target_premium),
            "TargetPremium_currentRenewalDate": start_date + "T00:00:00.00000",
            "TargetPremium_onlineYN": "true",
            "TargetPremium_telephone": "true",
            "TargetPremium_renewal": "false",
            "TargetPremium_newinsurer": "false",
            "TargetPremium_lastyear": str(target_premium),
            "TargetPremium_bestquote": str(target_premium),
            "TargetPremium_coverID": "0",
            "TargetPremium_totalExcess": str(risk_data["Vehicles"][0]["VoluntaryExcess"]),
        },
        "IsTestSchemeQuote": False,
        "Enrichments": None,
        "QuoteReference": None,
    }


def generate_v6_bike_records(record_count):
    if record_count < 1:
        raise ValueError("Record count must be at least 1.")
    fake = Faker("en_GB")
    return [_build_record(fake) for _ in range(record_count)]