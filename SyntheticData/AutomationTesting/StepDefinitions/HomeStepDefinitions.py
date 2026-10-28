from StepLibraries.HomeStepLibrary import (
    test_web_app_for_address,
    test_web_app_for_date,
    test_web_app_for_email,
    test_web_app_for_id,
    test_web_app_for_job,
    test_web_app_for_multiple_choice,
    test_web_app_for_name,
    test_web_app_for_number,
    test_web_app_for_string,
    test_web_app_for_text,
)
from behave import given


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} ID's")
def run_id_data_type_step(context, record_count=10):
    return test_web_app_for_id(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Address values")
def run_address_data_type_step(context, record_count=10):
    return test_web_app_for_address(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Date values")
def run_date_data_type_step(context, record_count=10):
    return test_web_app_for_date(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Email values")
def run_email_data_type_step(context, record_count=10):
    return test_web_app_for_email(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Job values")
def run_job_data_type_step(context, record_count=10):
    return test_web_app_for_job(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Multiple Choice values")
def run_multiple_choice_data_type_step(context, record_count=10):
    return test_web_app_for_multiple_choice(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Name values")
def run_name_data_type_step(context, record_count=10):
    return test_web_app_for_name(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Number values")
def run_number_data_type_step(context, record_count=10):
    return test_web_app_for_number(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} String values")
def run_string_data_type_step(context, record_count=10):
    return test_web_app_for_string(record_count)


@given("I can navigate to the Syn Data Home Page and create a CSV file with {record_count:d} Text values")
def run_text_data_type_step(context, record_count=10):
    return test_web_app_for_text(record_count)


if __name__ == "__main__":
    run_id_data_type_step(None, 10)
