import time
from pathlib import Path

from selenium import webdriver

from Pages.AutoBasePageObject import AutoBasePageObject
from Pages.MainHomePage import MainHomePage


SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "screenshots"
DOWNLOAD_DIR = Path(__file__).resolve().parent.parent / "downloads"


def _create_driver():
    DOWNLOAD_DIR.mkdir(exist_ok=True)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.page_load_strategy = "eager"
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": str(DOWNLOAD_DIR),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True,
        },
    )
    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_cdp_cmd(
        "Page.setDownloadBehavior",
        {"behavior": "allow", "downloadPath": str(DOWNLOAD_DIR)},
    )
    return driver


def _save_screenshot(driver, data_type, stage):
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    filename = f"{data_type.lower().replace(' ', '-')}-test-{stage}.png"
    screenshot_path = SCREENSHOT_DIR / filename
    driver.save_screenshot(str(screenshot_path))
    print("Screenshot saved:", screenshot_path)


def _run_data_type(column_name, data_type, configure=None, record_count=10):
    driver = _create_driver()
    try:
        main_home_page = MainHomePage(driver)
        main_home_page.open()
        _save_screenshot(driver, data_type, "before-typing")
        main_home_page.enter_column_name(column_name)
        _save_screenshot(driver, data_type, "after-typing")
        main_home_page.select_data_type(data_type)
        if configure:
            configure(main_home_page)
        main_home_page.enter_record_count(record_count).submit()
        time.sleep(5)
    finally:
        driver.quit()

    rows = AutoBasePageObject(DOWNLOAD_DIR).read_latest_csv()
    print("Test Completed")
    return rows


def test_web_app_for_id(record_count=10):
    SCREENSHOT_DIR.mkdir(exist_ok=True)
    driver = _create_driver()
    try:
        print("Starting test for web app ID column")
        main_home_page = MainHomePage(driver)
        main_home_page.open()
        print("Navigated to web app URL")

        column_input = main_home_page.get_column_name_input()
        _save_screenshot(driver, "id", "before-typing")

        main_home_page.enter_column_name("Test ID Column")
        print("Column input value after typing:", repr(column_input.get_attribute("value")))
        _save_screenshot(driver, "id", "after-typing")

        main_home_page.select_data_type("Id").enter_record_count(record_count).submit()
        time.sleep(5)
    finally:
        driver.quit()

    rows = AutoBasePageObject(DOWNLOAD_DIR).read_latest_csv()
    print("Test Completed")
    return rows


def test_web_app_for_address(record_count=10):
    return _run_data_type("Test Address Column", "Address", record_count=record_count)


def test_web_app_for_date(record_count=10):
    def configure(main_home_page):
        main_home_page.enter_date_range(
            "%y/%m/%d,01/12/2025",
            "%y/%m/%d,12/05/2026",
        )

    return _run_data_type("Test Date Column", "Date", configure, record_count)


def test_web_app_for_email(record_count=10):
    return _run_data_type("Test Email Column", "Email", record_count=record_count)


def test_web_app_for_job(record_count=10):
    return _run_data_type("Test Job Column", "Job", record_count=record_count)


def test_web_app_for_multiple_choice(record_count=10):
    def configure(main_home_page):
        main_home_page.enter_multiple_choice_format("red, green, blue")

    return _run_data_type("Test Multiple Choice Column", "Multiple Choice", configure, record_count)


def test_web_app_for_name(record_count=10):
    return _run_data_type("Test Name Column", "Name", record_count=record_count)


def test_web_app_for_number(record_count=10):
    def configure(main_home_page):
        main_home_page.enter_number_range(10, 100)

    return _run_data_type("Test Number Column", "Number", configure, record_count)


def test_web_app_for_string(record_count=10):
    def configure(main_home_page):
        main_home_page.enter_string_length(5)

    return _run_data_type("Test String Column", "String", configure, record_count)


def test_web_app_for_text(record_count=10):
    return _run_data_type("Test Text Column", "Text", record_count=record_count)
