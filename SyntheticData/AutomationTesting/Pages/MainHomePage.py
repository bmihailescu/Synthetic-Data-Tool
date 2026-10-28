from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select


class MainHomePage:
    URL = "http://localhost:8000/"

    COLUMN_NAME_INPUT = (By.CSS_SELECTOR, "#row1 > input")
    DATA_TYPE_DISPLAY = (By.ID, "dataTypeDisplayValue")
    ADD_ROW_BUTTON = (By.CSS_SELECTOR, "#add button")
    FORMAT_START_DATE_INPUT = (By.XPATH, '(//input[@type="date"])[1]')
    FORMAT_END_DATE_INPUT = (By.XPATH, '(//input[@type="date"])[2]')
    MULTIPLE_CHOICE_FORMAT_INPUT = (
        By.CSS_SELECTOR,
        'input[placeholder="Eg. red,blue,green"]',
    )
    NUMBER_MIN_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Min"]')
    NUMBER_MAX_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Max"]')
    STRING_LENGTH_INPUT = (By.CSS_SELECTOR, 'input[placeholder="Length"]')
    TEXT_WORD_COUNT_INPUT = (
        By.CSS_SELECTOR,
        'input[placeholder="No. of Words (optional)"]',
    )
    FILE_TYPE_SELECT = (By.NAME, "file_type")
    BLANK_PERCENTAGE_INPUT = (By.NAME, "blankPercent")
    BAD_DATA_INPUT = (By.NAME, "badData")
    RECORD_COUNT_INPUT = (By.ID, "num_of_entries")
    SUBMIT_BUTTON = (By.ID, "submit")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.element_to_be_clickable(self.COLUMN_NAME_INPUT))
        return self

    def enter_column_name(self, column_name):
        self._fill(self.COLUMN_NAME_INPUT, column_name)
        return self

    def get_column_name_input(self):
        return self.wait.until(EC.element_to_be_clickable(self.COLUMN_NAME_INPUT))

    def select_data_type(self, data_type):
        data_type_display = self.wait.until(
            EC.element_to_be_clickable(self.DATA_TYPE_DISPLAY)
        )
        data_type_display.click()

        data_type_option = (
            By.XPATH,
            f'//a[@class="dropdown-item"][normalize-space()="{data_type}"]',
        )
        self.wait.until(EC.element_to_be_clickable(data_type_option)).click()
        return self

    def enter_record_count(self, record_count):
        self._fill(self.RECORD_COUNT_INPUT, record_count)
        return self

    def add_row(self):
        self.wait.until(EC.element_to_be_clickable(self.ADD_ROW_BUTTON)).click()
        return self

    def enter_date_range(self, start_date, end_date):
        self._fill(self.FORMAT_START_DATE_INPUT, start_date)
        self._fill(self.FORMAT_END_DATE_INPUT, end_date)
        return self

    def enter_multiple_choice_format(self, choices):
        self._fill(self.MULTIPLE_CHOICE_FORMAT_INPUT, choices)
        return self

    def enter_number_range(self, minimum, maximum):
        self._fill(self.NUMBER_MIN_INPUT, minimum)
        self._fill(self.NUMBER_MAX_INPUT, maximum)
        return self

    def enter_string_length(self, length):
        self._fill(self.STRING_LENGTH_INPUT, length)
        return self

    def enter_text_word_count(self, word_count):
        self._fill(self.TEXT_WORD_COUNT_INPUT, word_count)
        return self

    def select_file_type(self, file_type):
        file_type_select = self.wait.until(
            EC.element_to_be_clickable(self.FILE_TYPE_SELECT)
        )
        Select(file_type_select).select_by_value(file_type)
        return self

    def set_blank_percentage(self, percentage):
        self._fill(self.BLANK_PERCENTAGE_INPUT, percentage)
        return self

    def set_bad_data_level(self, level):
        self._fill(self.BAD_DATA_INPUT, level)
        return self

    def _fill(self, locator, value):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.clear()
        element.send_keys(str(value))
        return self

    def submit(self):
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()
