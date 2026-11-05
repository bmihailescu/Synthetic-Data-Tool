import copy
import datetime
import json
import random
import re
import secrets
import uuid
from functools import lru_cache
from pathlib import Path

from faker import Faker


_TEMPLATE_PATH = Path(__file__).with_name("aviva_integration_templates.json")
_HEX_VALUE = re.compile(r"^[0-9a-f]{32,64}$", re.I)
_MAKES = ["FORD", "VAUXHALL", "VOLKSWAGEN", "BMW", "AUDI", "TOYOTA", "PEUGEOT", "HONDA"]
_MODELS = ["Focus", "Astra", "Golf", "116", "A4", "Corolla", "Bipper", "CB125F"]
_UUID_FIELDS = {
    "addressid", "agentid", "callerid", "entityid", "historyid", "objectid",
    "policydetailsid", "policyid", "softwarehouseid", "telephoneid", "vehicleid",
}
_DATE_FIELDS = {
    "date", "dateofbirth", "datepassedtest", "registereddate", "purchasedate",
    "claimdate", "startdate", "enddate", "inceptiondate", "quoteDate".lower(),
}


@lru_cache(maxsize=1)
def _templates():
    return json.loads(_TEMPLATE_PATH.read_text(encoding="utf-8"))


def _normalise(key):
    return re.sub(r"[^a-z0-9]", "", key.lower())


def _new_id():
    return str(uuid.uuid4()).upper()


def _random_date(value, fake):
    if value.startswith(("0001-01-01", "1899-12-30")):
        return value
    new_date = fake.date_between(start_date="-75y", end_date="+1y")
    if "T" not in value:
        return new_date.isoformat()
    if "+" in value:
        suffix = "+00:00"
    elif value.endswith("Z"):
        suffix = "Z"
    else:
        suffix = ""
    return new_date.isoformat() + "T00:00:00" + suffix


def _person_context(value, fake, parent=None):
    context = dict(parent or {})
    normalized_keys = {_normalise(key): key for key in value}
    if "forename" in normalized_keys or "firstname" in normalized_keys:
        title_key = normalized_keys.get("titleid")
        title = value.get(title_key) if title_key else None
        gender_key = normalized_keys.get("genderid")
        gender = value.get(gender_key) if gender_key else None
        female = gender in ("F", "Female") or title in ("004", "005", "069")
        context["person"] = {
            "first": fake.first_name_female() if female else fake.first_name_male(),
            "last": fake.last_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "postcode": fake.postcode(),
        }
    if "address" in normalized_keys:
        address_key = normalized_keys["address"]
        address = value.get(address_key)
        if isinstance(address, dict):
            context["address"] = {
                "houseno": str(random.randint(1, 150)),
                "housename": fake.street_name(),
                "street": fake.street_name(),
                "locality": fake.city_suffix(),
                "city": fake.city(),
                "county": fake.county(),
                "postcode": fake.postcode(),
                "eircode": fake.postcode(),
            }
    return context


def _random_string(value, key, fake, context):
    norm = _normalise(key)
    person = context.get("person", {})
    address = context.get("address", {})

    if norm in ("forename", "firstname"):
        return person.get("first", fake.first_name())
    if norm in ("surname", "lastname"):
        return person.get("last", fake.last_name())
    if "email" in norm:
        return person.get("email", fake.email())
    if any(term in norm for term in ("telephone", "phonenumber")) or norm in ("phone", "telephoneno"):
        return person.get("phone", fake.phone_number())
    if "postcode" in norm or norm == "eircode":
        return person.get("postcode", fake.postcode())
    if norm in address:
        return address[norm]
    if norm in ("make", "vehiclemake"):
        return random.choice(_MAKES)
    if norm in ("model", "vehiclemodel"):
        return random.choice(_MODELS)
    if norm in ("series", "type") and "vehicle" in norm:
        return str(random.randint(1, 9))
    if "registrationnumber" in norm:
        return fake.license_plate()
    if "licencenumber" in norm or "drivinglicencenumber" in norm:
        return "TEST" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=8))
    if "policynumber" in norm:
        return "AV" + "".join(random.choices("0123456789", k=10))
    if "clientreference" in norm or norm in ("quotereference", "pipereference"):
        return fake.bothify(text="??????????").upper()
    if "token" in norm or norm in ("callerid", "softwarehouseid"):
        return secrets.token_hex(12)
    if norm in _UUID_FIELDS or _HEX_VALUE.fullmatch(value):
        return _new_id()
    if "date" in norm or norm.endswith("since"):
        return _random_date(value, fake)
    if "createdby" in norm:
        return "SYNTHETIC"
    if norm in ("occupationid", "employersbusinessid") and value == "":
        return fake.random_int(min=1, max=999).__str__().zfill(3)
    if not value:
        return value
    return value


def _randomise(value, key, fake, context=None):
    if isinstance(value, dict):
        local_context = _person_context(value, fake, context)
        return {
            child_key: _randomise(child, child_key, fake, local_context)
            for child_key, child in value.items()
        }
    if isinstance(value, list):
        return [_randomise(child, key, fake, context) for child in value]
    if value is None:
        return None
    if isinstance(value, bool):
        return random.choice((True, False))
    if isinstance(value, int):
        norm = _normalise(key)
        if "yearofmanufacture" in norm:
            return random.randint(1990, datetime.date.today().year)
        if "mileage" in norm:
            return random.randrange(500, 30001, 500)
        if "age" in norm or norm.endswith("years"):
            return random.randint(0, 75)
        if "cubiccapacity" in norm or norm in ("cc", "abicc"):
            return random.choice((50, 125, 150, 250, 500, 650, 900, 1200, 1600, 2000))
        if "premium" in norm or "cost" in norm or "amount" in norm:
            return random.randint(0, 5000)
        return value
    if isinstance(value, float):
        norm = _normalise(key)
        if any(term in norm for term in ("premium", "cost", "amount", "value", "excess")):
            return round(random.uniform(0, 25000), 2)
        return value
    if isinstance(value, str):
        norm = _normalise(key)
        if norm.endswith("riskdata") and value.lstrip().startswith(("{", "[")):
            try:
                nested = json.loads(value)
            except json.JSONDecodeError:
                return value
            return json.dumps(_randomise(nested, key, fake, context), ensure_ascii=False, separators=(",", ":"))
        if norm in ("riskdata", "originalriskdata") and value:
            return value
        return _random_string(value, key, fake, context or {})
    return value


def generate_aviva_files(files_per_type):
    if files_per_type < 1:
        raise ValueError("Files per type must be at least 1.")
    templates = _templates()
    if len(templates) != 22:
        raise ValueError(f"Expected 22 Aviva templates, found {len(templates)}.")

    fake = Faker("en_GB")
    files = []
    for template in templates:
        for index in range(1, files_per_type + 1):
            record = _randomise(copy.deepcopy(template["record"]), "", fake)
            filename = f"{template['name']}_{index:04d}.json"
            files.append((filename, json.dumps(record, ensure_ascii=False, indent=2)))
    return files