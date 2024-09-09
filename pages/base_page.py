import base64
import datetime as dt
import fnmatch
import json
import os
import re
import time
import uuid
import calendar
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP

from PIL import Image
from selenium.common import NoSuchElementException, ElementNotVisibleException, \
    WebDriverException
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait

from configurations import generic_modules

""" This class is the parent of all pages """
""" It contains all the generic methods and functionalities available to all the pages """


class BasePage:
    ONE_MINUTE = generic_modules.ONE_MINUTE_DELAY
    HALF_MINUTE = generic_modules.HALF_MINUTE_DELAY
    TWO_SEC_DELAY = generic_modules.SHORT_DELAY
    FIVE_SEC_DELAY = generic_modules.FIVE_SEC_DELAY
    ONE_SEC_DELAY = generic_modules.ONE_SEC_DELAY

    # [Start] Tag Names
    input_tag = "input"
    a_tag = "a"
    div_tag = "div"
    span_tag = "span"
    textarea_tag = "textarea"
    li_tag = "li"
    td_tag = "td"
    data_count_tag = "data-count"
    placeholder_tag = "placeholder"
    href_tag = "href"
    # [End] Tag Names

    # [Start] Attribute Names
    class_attribute = "class"
    id_attribute = "id"
    title_attribute = "title"
    name_attribute = "name"
    data_qa_attribute = "data-qa"

    # [End] Attribute Names

    def __init__(self, driver):
        self.driver = driver

    def click_on_sidebar_menu(self, menu_name):
        locator = By.XPATH, "//dfn[@data-qa='" + menu_name + "']"
        if 'http://rtb.local/admin' in self.driver.current_url:
            time.sleep(2)
            self.scroll_into_view(locator)
            time.sleep(2)
        self.wait_for_element_to_be_clickable(locator).click()

    def click_on_element_using_tag_attribute(self, tag_name="",
                                             attribute="",
                                             attribute_value=""):
        if attribute == self.id_attribute:
            locator = (By.ID, attribute_value)
        else:
            locator = (By.XPATH,
                       "//" + tag_name + "[@" + attribute + "='" + attribute_value + "']")
        self.click_on_element(locator)

    class MaxRetriesExceededException(Exception):
        pass

    def click_on_element(self, locator, locator_initialization=False,
                         click_on_presence_of_element=False,
                         time_out=30,
                         max_retries=3,
                         locator_to_be_appeared=None):
        retries = 0
        wait_time = 20

        if locator_initialization:
            if "//" in locator:
                formed_locator = (By.XPATH, locator)
            else:
                formed_locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                formed_locator = locator
            else:
                formed_locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        while retries < max_retries:
            try:
                if 'http://rtb.local/admin' in self.driver.current_url:
                    time.sleep(1)
                    self.scroll_into_view(formed_locator)
                    time.sleep(1)
                if retries > 0:
                    element = self.wait_for_presence_of_element(formed_locator, time_out=wait_time)
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    if click_on_presence_of_element:
                        self.wait_for_presence_of_element(formed_locator, time_out=wait_time).click()
                    else:
                        self.wait_for_presence_of_element(formed_locator, time_out=wait_time)
                        self.wait_for_element_to_be_clickable(formed_locator).click()
                if locator_to_be_appeared is not None:
                    if '//' in locator_to_be_appeared[1] or By.ID == locator_to_be_appeared[0]:
                        formed_locator_to_be_appeared = locator_to_be_appeared
                    else:
                        formed_locator_to_be_appeared = (By.XPATH, "//*[@data-qa='" + locator_to_be_appeared + "']")
                    WebDriverWait(self.driver, timeout=time_out, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            formed_locator_to_be_appeared))
                return
            except Exception as e:
                print(e)
                retries += 1
        raise self.MaxRetriesExceededException(f"Max retries ({max_retries}) exceeded.")

    def click_on_three_dot_option(self, option_name_or_data_qa,
                                  parent_attribute_value=""):
        if parent_attribute_value == "":
            locator = (
                By.XPATH,
                "//a[@title='" + option_name_or_data_qa + "'] | //a[contains(@data-qa, '" + option_name_or_data_qa + "')]")
        else:
            locator = (
                By.XPATH,
                "//*[contains(@class, '" + parent_attribute_value + "')]//a[@title='" + option_name_or_data_qa + "'] "
                                                                                                                 "| //*[contains(@class, '" + parent_attribute_value + "')]//a[contains(@data-qa, "
                                                                                                                                                                       "'" + option_name_or_data_qa + "')]")
        self.click_on_element(locator)

    def set_value_into_element(self, locator, text,
                               locator_initialization=False):
        if locator_initialization:
            if "//" in locator:
                locator = (By.XPATH, locator)
            else:
                locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                locator = locator
            else:
                locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        self.wait_for_presence_of_element(locator)
        self.clear_field(locator)
        self.wait_for_presence_of_element(locator).send_keys(text)

    def clear_field(self, locator):
        if '//' in locator[1] or By.ID == locator[0]:
            locator = locator
        else:
            locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        self.wait_for_presence_of_element(locator).clear()

    def select_dropdown_value(self, dropdown_label_data_qa, dropdown_item="",
                              select_by_value=False, value="1", index=1):
        locator = "(//label[contains(text(), '" + dropdown_label_data_qa + "')]/..//select | //select[" \
                                                                           "contains(@data-qa, '" + \
                  dropdown_label_data_qa + "')])[" + str(index) + "]"
        self.dropdown_selection(locator, dropdown_item,
                                select_by_value, value)

    def select_dropdown_value_from_div(self, attribute_type,
                                       attribute_value,
                                       dropdown_item="",
                                       select_by_value=False,
                                       value="1",
                                       tag_name="div"):
        locator = "//" + tag_name + "[@" + attribute_type + "='" + attribute_value + "']/..//select"
        self.dropdown_selection(locator, dropdown_item,
                                select_by_value, value)

    def dropdown_selection(self, locator, dropdown_item="",
                           select_by_value=False, value="1"):
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        if select_by_value:
            Select(
                self.driver.find_element(By.XPATH,
                                         locator)).select_by_value(
                value)
        else:
            Select(self.driver.find_element(By.XPATH,
                                            locator)).select_by_visible_text(
                dropdown_item)

    def deselect_all_dropdown_value(self, dropdown_label):
        locator = "//label[contains(text(), '" + dropdown_label + "')]/..//select"
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        Select(self.driver.find_element(By.XPATH,
                                        locator)).deselect_all()

    def deselect_dropdown_value(self, dropdown_label, dropdown_item="",
                                select_by_value=False, value="1"):
        locator = "//label[contains(text(), '" + dropdown_label + "')]/..//select"
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        if select_by_value:
            Select(
                self.driver.find_element(By.XPATH,
                                         locator)).deselect_by_value(
                value)
        else:
            Select(self.driver.find_element(By.XPATH,
                                            locator)).deselect_by_visible_text(
                dropdown_item)

    def get_element_count(self, locator, time_out=HALF_MINUTE):
        element = self.wait_for_presence_of_all_elements_located(
            locator,
            time_out)
        return len(element)

    def get_element_text(self, locator, time_out=ONE_MINUTE,
                         locator_initialization=False, input_tag=False,
                         max_retries=3):
        retries = 0
        if locator_initialization:
            if "//" in locator:
                locator = (By.XPATH, locator)
            else:
                locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                locator = locator
            else:
                locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        while retries < max_retries:
            try:
                if input_tag:
                    element_text = self.wait_for_visibility_of_element(
                        locator,
                        time_out).get_attribute(
                        "value")
                else:
                    WebDriverWait(self.driver, time_out).until(
                        EC.presence_of_element_located(locator),
                        "Web element was not available within the specific time out. "
                        "Locator: '" + str(locator) + "'")
                    element_text = self.wait_for_presence_of_element(
                        locator,
                        time_out).text
                return element_text
            except StaleElementReferenceException:
                retries += 1

    def get_checked_element_value_attribute(self, label):
        locator = (By.XPATH,
                   "//label[normalize-space(text())='" + label + "']/..//input[@checked='checked']")
        return self.get_element_text(locator, input_tag=True)

    def is_visible(self, locator, time_out=ONE_MINUTE,
                   locator_initialization=False):
        is_visible = None
        try:
            self.wait_for_visibility_of_element(locator,
                                                time_out=time_out,
                                                locator_initialization=locator_initialization)
            is_visible = True
        except TimeoutException:
            is_visible = False
        finally:
            return is_visible

    def is_element_present(self, locator, time_out=HALF_MINUTE,
                           locator_initialization=False):
        is_present = None
        if locator_initialization:
            if "//" in locator:
                locator = (By.XPATH, locator)
            else:
                locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                locator = locator
            else:
                locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        try:
            WebDriverWait(self.driver, time_out).until(
                EC.presence_of_element_located(locator),
                "Web element was not available within the specific time out. "
                "Locator: '" + str(locator) + "'")
            is_present = True
        except TimeoutException:
            is_present = False
        finally:
            return is_present

    def is_element_displayed(self, locator, locator_initialization=False,
                             time_out=HALF_MINUTE):
        if locator_initialization:
            if "//" in locator:
                element = self.driver.find_element(By.XPATH,
                                                   locator)
            else:
                element = self.driver.find_element(By.ID,
                                                   locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                locator = locator
            else:
                locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
            element = WebDriverWait(self.driver, time_out).until(
                EC.presence_of_element_located(locator),
                "Web element was not available within the specific "
                "time out. "
                "Locator: '" + str(locator) + "'")
        return element.is_displayed()

    def get_url(self, url, time_out=HALF_MINUTE):
        self.wait_url_contains(time_out, url)
        return self.driver.current_url

    def go_to_url(self, url):
        try:
            self.driver.get(url)
            WebDriverWait(self.driver, 5).until(
                EC.alert_is_present(),
                'Timed out waiting for alert to appear')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("Alert not present")
        time.sleep(self.ONE_SEC_DELAY)

    def go_to_prev_page(self):
        return self.driver.back()

    def hover_on_element(self, locator, time_out=ONE_MINUTE):
        hover = ActionChains(self.driver).move_to_element(
            self.wait_for_presence_of_element(time_out, locator))
        hover.perform()

    def scroll_into_view(self, locator):
        if '//' in locator[1] or By.ID == locator[0]:
            formed_locator = locator
        else:
            formed_locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        element = self.driver.find_element(*formed_locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(2)

    def do_page_up(self, time_out=ONE_MINUTE):
        self.wait_for_presence_of_element((By.TAG_NAME, 'body'),
                                          time_out).send_keys(
            Keys.PAGE_UP)

    def do_page_down(self, time_out=ONE_MINUTE):
        self.wait_for_presence_of_element((By.TAG_NAME, 'body'),
                                          time_out).send_keys(
            Keys.PAGE_DOWN)

    def wait_for_presence_of_element(self, locator, time_out=HALF_MINUTE,
                                     locator_initialization=False,
                                     max_retries=3):
        retries = 0
        if locator_initialization:
            if "//" in locator:
                formed_locator = (By.XPATH, locator)
            else:
                formed_locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                formed_locator = locator
            else:
                formed_locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        while retries < max_retries:
            try:
                return WebDriverWait(self.driver, time_out,
                                     poll_frequency=0.5).until(
                    EC.presence_of_element_located(
                        formed_locator),
                    "Web element was not present within the specific time out. Locator: '" + str(
                        formed_locator) + "'")
            except StaleElementReferenceException:
                retries += 1

    def wait_for_element_to_be_clickable(self, locator,
                                         time_out=HALF_MINUTE,
                                         locator_initialization=False,
                                         max_retries=3):
        retries = 0
        if locator_initialization and retries == 0:
            if "//" in locator:
                formed_locator = (By.XPATH, locator)
            else:
                formed_locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                formed_locator = locator
            else:
                formed_locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        while retries < max_retries:
            try:
                return WebDriverWait(self.driver, time_out,
                                     poll_frequency=0.5).until(
                    EC.element_to_be_clickable(formed_locator),
                    "Web element was not clickable within the specific time out. Locator: '" + str(
                        formed_locator) + "'")
            except StaleElementReferenceException:
                retries += 1

    def wait_for_visibility_of_element(self, locator, time_out=HALF_MINUTE,
                                       locator_initialization=False,
                                       max_retries=3):
        retries = 0
        if locator_initialization and retries == 0:
            if "//" in locator:
                formed_locator = (By.XPATH, locator)
            else:
                formed_locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                formed_locator = locator
            else:
                formed_locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        while retries < max_retries:
            try:
                return WebDriverWait(self.driver, time_out,
                                     poll_frequency=0.5).until(
                    EC.visibility_of_element_located(
                        formed_locator),
                    "Web element was not visible within the specific time out. Locator: '" + str(
                        formed_locator) + "'")
            except StaleElementReferenceException:
                retries += 1

    def wait_for_visibility_of_all_elements_located(self, locator,
                                                    time_out=HALF_MINUTE):
        return WebDriverWait(self.driver, time_out,
                             poll_frequency=0.5).until(
            EC.visibility_of_all_elements_located(locator),
            "Web elements were not visible within the specific time out. Locator: '" + str(
                locator) + "'")

    def wait_for_presence_of_all_elements_located(self, locator,
                                                  time_out=HALF_MINUTE):
        return WebDriverWait(self.driver, time_out).until(
            EC.presence_of_all_elements_located(locator),
            "Web elements were not present within the specific time "
            "out. Locator: '" + str(locator) + "'")

    def wait_url_contains(self, time_out, url):
        return WebDriverWait(self.driver, time_out).until(
            EC.url_contains(url))

    def wait_alert_is_present(self, time_out=HALF_MINUTE):
        time.sleep(self.TWO_SEC_DELAY)
        return WebDriverWait(self.driver, time_out).until(
            EC.alert_is_present(),
            "Alert was not present within the specific time out")

    def accept_alert(self):
        Alert(self.driver).accept()

    def get_alert_text(self):
        alert = Alert(self.driver)
        return alert.text

    @staticmethod
    def get_current_timestamp():
        return datetime.now()

    def is_alert_popup_available(self, time_out=HALF_MINUTE):
        try:
            time.sleep(self.ONE_SEC_DELAY)
            WebDriverWait(self.driver, time_out).until(
                EC.alert_is_present())
            return True
        except TimeoutException:
            return False

    @staticmethod
    def get_current_date_with_specific_format(date_format):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        today = date.today()
        date1 = today.strftime(date_format)
        return str(date1)

    @staticmethod
    def get_specific_date_with_specific_format(date_format, days_to_add=0,
                                               days_to_subtract=0):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        expected_date = None
        if days_to_add != 0:
            expected_date = dt.datetime.today() + dt.timedelta(
                days=days_to_add)
        elif days_to_subtract != 0:
            expected_date = dt.datetime.today() - dt.timedelta(
                days=days_to_subtract)
        date1 = expected_date.strftime(date_format)
        return str(date1)

    @staticmethod
    def get_first_day_of_previous_month(date_format='%Y-%m-%d'):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        today = dt.datetime.today()
        first_day_this_month = today.replace(day=1)
        last_month = first_day_this_month - dt.timedelta(days=1)
        first_day_last_month = last_month.replace(day=1)
        return first_day_last_month.strftime(date_format)

    @staticmethod
    def get_last_day_of_previous_month(date_format='%Y-%m-%d'):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        today = dt.datetime.today()
        first_day_of_this_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_this_month - dt.timedelta(days=1)
        last_day_formatted = last_day_of_previous_month.strftime(date_format)
        return last_day_formatted

    @staticmethod
    def get_last_day_of_current_month(date_format='%Y-%m-%d'):
        """
        Get the last day of the current month in the specified format.

        Args:
            date_format (str): The format in which to return the date.

        Returns:
            str: The last day of the current month formatted as specified.
        """
        today = dt.datetime.today()
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]
        last_date = today.replace(day=last_day_of_month)
        last_day_formatted = last_date.strftime(date_format)
        return last_day_formatted

    @staticmethod
    def get_first_day_of_current_month(date_format='%Y-%m-%d'):
        """
        Get the first day of the current month in the specified format.

        Args:
            date_format (str): The format in which to return the date.

        Returns:
            str: The first day of the current month formatted as specified.
        """
        today = dt.datetime.today()
        first_day_of_month = today.replace(day=1)
        first_day_formatted = first_day_of_month.strftime(date_format)
        return first_day_formatted

    def is_first_date_or_last_date_of_the_month(self, date_format='%Y-%m-%d'):
        """
        Check if today is the first or the last date of the current month.

        Returns:
            bool: True if today is the first or last date of the current month, otherwise False.
        """
        current_date = self.get_current_date_with_specific_format(date_format)
        return (self.get_first_day_of_current_month() == current_date or
                self.get_last_day_of_current_month() == current_date)

    def select_specific_date_range(self, field_name_or_data_qa, date_range_to_select):
        field_locator = (By.XPATH,
                         "(//label[contains(text(), '" + field_name_or_data_qa + "')]/..//input)[1] | (//input["
                                                                                 "@data-qa='" + field_name_or_data_qa + "'])["
                                                                                                                        "1]")
        date_range_locator = (
            By.XPATH,
            "//a[contains(text(), '" + date_range_to_select + "')]")
        self.click_on_element(field_locator)
        self.click_on_element(date_range_locator)

    def set_value_into_specific_input_field(self, field_name_or_data_qa, text,
                                            is_textarea=False,
                                            tab_out=False,
                                            attribute="",
                                            attribute_value=""):
        if is_textarea:
            if attribute == self.id_attribute:
                field_locator = (By.ID, attribute_value)
            else:
                field_locator = (By.XPATH,
                                 "//label[normalize-space(text())='" + field_name_or_data_qa + "']/..//textarea | //*["
                                                                                               "@data-qa='" + field_name_or_data_qa + "']")
        else:
            if attribute == self.id_attribute:
                field_locator = (By.ID, attribute_value)
            else:
                field_locator = (By.XPATH,
                                 "//label[normalize-space(text())='" + field_name_or_data_qa + "']/..//input | //*["
                                                                                               "@data-qa='" + field_name_or_data_qa + "']")
        self.set_value_into_element(field_locator, text)
        if tab_out:
            self.wait_for_presence_of_element(
                field_locator).send_keys(
                Keys.TAB)

    def select_from_modal(self, search_text, field_label_or_data_qa="", selection_locator='', is_delay='',
                          click_uncheck_all=True, search_data_qa=""):
        time.sleep(self.TWO_SEC_DELAY)
        field_locator = (
            By.XPATH,
            "//label[contains(text(), '" + field_label_or_data_qa + "')]/..//span[@class='mselect-selection'] | "
                                                                    "//select[@data-qa='" + field_label_or_data_qa + "']/..//span[@class='mselect-selection']")
        uncheck_all_button_locator = (
            By.XPATH,
            "//*[@class='additional-btns']//button[contains(@class, 'uncheck-all')]")
        search_field_locator = (
            By.XPATH,
            "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        if search_data_qa != '':
            checkbox_locator = (By.XPATH, "//input[@data-qa='" + search_data_qa + "']")
        else:
            checkbox_locator = (By.XPATH,
                            "//label[contains(text(), '" + search_text + "')]/../input | //label[contains(text(), '"
                            + search_text + "')]")
        select_button_locator = (
            By.XPATH, "//button[@data-bb-handler='confirm']")
        if field_label_or_data_qa != "":
            self.wait_for_element_to_be_clickable(field_locator)
            self.click_on_element(field_locator)
            try:
                self.wait_for_presence_of_element(
                    uncheck_all_button_locator)
                self.wait_for_element_to_be_clickable(
                    uncheck_all_button_locator,
                    self.ONE_MINUTE)
            except TimeoutException:
                self.click_on_element(select_button_locator)
                self.wait_for_element_to_be_clickable(
                    field_locator)
                self.click_on_element(field_locator)
                self.wait_for_presence_of_element(
                    uncheck_all_button_locator)
                self.wait_for_visibility_of_element(
                    uncheck_all_button_locator)
        if click_uncheck_all:
            try:
                self.wait_for_visibility_of_element(
                    uncheck_all_button_locator)
                self.wait_for_element_to_be_clickable(
                    uncheck_all_button_locator,
                    self.ONE_MINUTE)
                self.click_on_element(uncheck_all_button_locator)
            except TimeoutException:
                self.click_on_element(select_button_locator)
                self.click_on_element(selection_locator)
                time.sleep(self.TWO_SEC_DELAY)
                self.wait_for_visibility_of_element(
                    uncheck_all_button_locator)
                self.wait_for_element_to_be_clickable(
                    uncheck_all_button_locator,
                    self.ONE_MINUTE)
                self.click_on_element(uncheck_all_button_locator)
        self.wait_for_presence_of_element(search_field_locator)
        self.wait_for_element_to_be_clickable(search_field_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.set_value_into_element(search_field_locator, search_text)
        self.wait_for_presence_of_element(checkbox_locator,
                                          self.HALF_MINUTE)
        self.wait_for_visibility_of_element(checkbox_locator,
                                            self.HALF_MINUTE)
        self.wait_for_element_to_be_clickable(checkbox_locator,
                                              self.HALF_MINUTE)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(checkbox_locator)
        self.wait_for_visibility_of_element(select_button_locator)
        self.wait_for_element_to_be_clickable(select_button_locator)
        if is_delay == 'yes':
            time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(select_button_locator)

    def select_from_modal_form_using_js_code_without_retry(self, field_label_or_xpath_or_data_qa,
                                                           option_to_select="",
                                                           option_list_to_select=None, index="1"):
        """
        Select from modal form using js code
        :param index:
        :param field_label_or_xpath_or_data_qa:
        :param option_to_select:
        :param option_list_to_select:
        :return:
        """
        if "//" in field_label_or_xpath_or_data_qa:
            xpath_expression = field_label_or_xpath_or_data_qa
        else:
            xpath_expression = "(//label[contains(text(), '" + field_label_or_xpath_or_data_qa + "')]/..//select | //select[@data-qa='" + field_label_or_xpath_or_data_qa + "'])[" + index + "]"
        javascript_selector = f'document.evaluate("{xpath_expression}", document, null, ' \
                              f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'
        self.deselect_all_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa, index=index)

        if option_list_to_select is None:
            javascript_code = f"""
                var select = {javascript_selector};
                var optionToSelect = "{option_to_select}";

                for (var i = 0; i < select.options.length; i++) {{
                    if (select.options[i].text === optionToSelect) {{
                        select.options[i].selected = true;
                        var event = new Event('change', {{ bubbles: true, cancelable: true }});
                        select.dispatchEvent(event);
                    }}
                }}
            """
        else:
            javascript_code = f"""
                var select = {javascript_selector};
                var optionsToSelect = {json.dumps(option_list_to_select)};
                var selectedOptions = [];

                for (var i = 0; i < select.options.length; i++) {{
                    if (optionsToSelect.includes(select.options[i].text)) {{
                        select.options[i].selected = true;
                        selectedOptions.push(select.options[i].text);
                    }}
                }}
                var event = new Event('change', {{ bubbles: true, cancelable: true }});
                select.dispatchEvent(event);
            """
        self.driver.execute_script(javascript_code)

        if option_list_to_select is None:
            result = 'Success' if self.verify_selected_options_using_js_code(
                field_label_or_xpath_or_data_qa,
                [option_to_select], index=index) else 'Failure'
        else:
            result = 'Success' if self.verify_selected_options_using_js_code(
                field_label_or_xpath_or_data_qa,
                option_list_to_select, index=index) else 'Failure'
        if result != 'Success':
            select_item = option_to_select if option_list_to_select is None else option_list_to_select
            raise AssertionError(
                f"Finally failed to select '{select_item}' for field '{field_label_or_xpath_or_data_qa}' in UI")

    def select_from_modal_form_using_js_code(self, field_label_or_xpath_or_data_qa, option_to_select="",
                                             option_list_to_select=None,
                                             max_retries=5, index="1"):
        for retry_count in range(max_retries):
            try:
                self.select_from_modal_form_using_js_code_without_retry(field_label_or_xpath_or_data_qa,
                                                                        option_to_select,
                                                                        option_list_to_select, index=index)
                break
            except Exception as e:
                print(f"Attempt {retry_count + 1} failed: {e}")
                time.sleep(1)
                if retry_count == max_retries - 1:
                    raise

    def verify_selected_options_using_js_code(self, field_label_or_xpath,
                                              expected_selected_options, index="1"):
        """
        Verify selected options using js code
        :param index:
        :param field_label_or_xpath:
        :param expected_selected_options:
        :return:
        """
        if "//" in field_label_or_xpath:
            xpath_expression = field_label_or_xpath
        else:
            xpath_expression = "(//label[contains(text(), '" + field_label_or_xpath + "')]/..//select | //select[" \
                                                                                      "@data-qa='" + \
                               field_label_or_xpath + "'])[" + index + "]"
        javascript_selector = f'document.evaluate("{xpath_expression}", document, null, ' \
                              f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'

        javascript_code = f"""
            var select = {javascript_selector};
            var selectedOptions = [];

            for (var i = 0; i < select.options.length; i++) {{
                if (select.options[i].selected) {{
                    selectedOptions.push(select.options[i].text);
                }}
            }}
            return selectedOptions;
        """

        selected_options = self.driver.execute_script(javascript_code)
        return generic_modules.ordered(selected_options) == generic_modules.ordered(expected_selected_options)

    def get_selected_options_using_js_code(self, field_label_or_xpath_data_qa, select_any_value=False):
        """
        Get selected options using js code
        :param select_any_value:
        :param field_label_or_xpath_data_qa:
        :return:
        """
        if "//" in field_label_or_xpath_data_qa:
            xpath_expression = field_label_or_xpath_data_qa
        else:
            xpath_expression = "//label[contains(text(), '" + field_label_or_xpath_data_qa + "')]/..//select | //select[" \
                                                                                             "@data-qa='" + field_label_or_xpath_data_qa + "']"
        javascript_selector = f'document.evaluate("{xpath_expression}", document, null, ' \
                              f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'

        javascript_code = f"""
            var select = {javascript_selector};
            var selectedOptions = [];

            for (var i = 0; i < select.options.length; i++) {{
                if (select.options[i].selected) {{
                    selectedOptions.push(select.options[i].text);
                }}
            }}
            return selectedOptions;
        """
        if select_any_value:
            locator = (By.XPATH,
                       "//select[@data-qa='" + field_label_or_xpath_data_qa + "']/..//span["
                                                                              "@class='mselect"
                                                                              "-selection__rendered']")
            return self.wait_for_presence_of_element(locator).text
        selected_options = self.driver.execute_script(javascript_code)
        if len(selected_options) == 1:
            selected_options = ', '.join(selected_options)
        return selected_options

    def deselect_all_from_modal_form_using_js_code(self, field_label_or_xpath_data_qa, index="1"):
        """
        Deselect all from modal form using js code
        :param index:
        :param field_label_or_xpath_data_qa:
        :return:
        """
        if "//" in field_label_or_xpath_data_qa:
            xpath_expression = field_label_or_xpath_data_qa
        else:
            xpath_expression = "(//label[contains(text(), '" + field_label_or_xpath_data_qa + "')]/..//select | " \
                                                                                              "//select[@data-qa='" + \
                               field_label_or_xpath_data_qa + "'])[" + index + "]"
        javascript_selector = f'document.evaluate("{xpath_expression}", document, null, ' \
                              f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'
        javascript_code = f"""
                var select = {javascript_selector};
                for (var i = 0; i < select.options.length; i++) {{
                  select.options[i].selected = false;
                }}
                var event = new Event('change', {{ bubbles: true, cancelable: true }});
                select.dispatchEvent(event);
                """
        self.driver.execute_script(javascript_code)

    def select_all_from_modal_form_using_js_code(self,
                                                 field_label_or_xpath_data_qa):
        """
        Select all from modal form using js code
        :param field_label_or_xpath_data_qa:
        :return:
        """
        if "//" in field_label_or_xpath_data_qa:
            xpath_expression = field_label_or_xpath_data_qa
        else:
            xpath_expression = "//label[contains(text(), '" + field_label_or_xpath_data_qa + "')]/..//select | //select[" \
                                                                                             "@data-qa='" + field_label_or_xpath_data_qa + "']"
        javascript_selector = f'document.evaluate("{xpath_expression}", document, null, ' \
                              f'XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue'
        javascript_code = f"""
                var select = {javascript_selector};
                for (var i = 0; i < select.options.length; i++) {{
                  select.options[i].selected = true;
                }}
                var event = new Event('change', {{ bubbles: true, cancelable: true }});
                select.dispatchEvent(event);
                """
        self.driver.execute_script(javascript_code)

    def check_uncheck_all_from_from_modal(self, field_label_or_data_qa,
                                          check_all=True):
        field_locator = (
            By.XPATH,
            "//label[contains(text(), '" + field_label_or_data_qa + "')]/..//span[@class='mselect-selection'] | "
                                                                    "//select[@data-qa='" + field_label_or_data_qa + "']/..//span[@class='mselect-selection']")
        uncheck_all_button_locator = (
            By.XPATH,
            "//*[@class='additional-btns']//button[contains(@class, 'uncheck-all') and text()='Uncheck All']")
        check_all_button_locator = (
            By.XPATH,
            "//*[@class='additional-btns']//button[contains(@class, 'check-all') and text()='Check All']")
        select_button_locator = (
            By.XPATH, "//button[@data-bb-handler='confirm']")
        search_field_locator = (
            By.XPATH,
            "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        self.wait_for_element_to_be_clickable(field_locator)
        self.click_on_element(field_locator)
        self.clear_field(search_field_locator)
        time.sleep(self.TWO_SEC_DELAY)
        if check_all:
            self.wait_for_element_to_be_clickable(
                check_all_button_locator)
            self.click_on_element(check_all_button_locator)
        else:
            self.wait_for_element_to_be_clickable(
                uncheck_all_button_locator)
            self.click_on_element(uncheck_all_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(select_button_locator)

    def select_from_modal_for_multiple_country(self, search_text,
                                               field_label=""):
        field_locator = (
            By.XPATH,
            "//label[contains(text(), '" + field_label + "')]/..//span[@class='mselect-selection']")
        search_field_locator = (
            By.XPATH,
            "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        checkbox_locator = (By.XPATH,
                            "//label[normalize-space(text())='" + search_text + "']/../input")
        select_button_locator = (
            By.XPATH, "//button[@data-bb-handler='confirm']")

        if field_label != "":
            self.wait_for_element_to_be_clickable(field_locator)
            self.click_on_element(field_locator)
        self.set_value_into_element(search_field_locator, search_text)
        time.sleep(self.ONE_SEC_DELAY)
        self.wait_for_element_to_be_clickable(checkbox_locator,
                                              self.HALF_MINUTE)
        self.click_on_element(checkbox_locator)
        self.wait_for_element_to_be_clickable(select_button_locator)
        self.click_on_element(select_button_locator)

    def select_multiple_item_from_modal(self, search_text_list,
                                        field_label_data_qa=""):
        field_locator = (
            By.XPATH,
            "//label[contains(text(), '" + field_label_data_qa + "')]/..//span[@class='mselect-selection'] | "
                                                                 "//select[@data-qa='" + field_label_data_qa + "']/..//span[@class='mselect-selection']")
        uncheck_all_button_locator = (
            By.XPATH,
            "//*[@class='additional-btns']//button[contains(@class, 'uncheck-all')]")
        search_field_locator = (
            By.XPATH,
            "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        select_button_locator = (
            By.XPATH, "//button[@data-bb-handler='confirm']")

        if field_label_data_qa != "":
            self.wait_for_element_to_be_clickable(field_locator)
            self.click_on_element(field_locator)
        self.wait_for_element_to_be_clickable(
            uncheck_all_button_locator,
            self.HALF_MINUTE)
        self.click_on_element(uncheck_all_button_locator)
        for search_text in search_text_list:
            checkbox_locator = (
                By.XPATH, "//label[normalize-space(text())='"
                + search_text + "']/../input | //label[contains(text(), '" + search_text +
                "')]/../input")
            self.set_value_into_element(search_field_locator,
                                        search_text)
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_element_to_be_clickable(checkbox_locator,
                                                  self.HALF_MINUTE)
            self.click_on_element(checkbox_locator)
        self.click_on_element(select_button_locator)

    def get_selected_multiple_items_from_modal(self, field_label):
        selected_checkboxes = []
        field_locator = (
            By.XPATH,
            "//label[contains(text(), '" + field_label + "')]/..//span[@class='mselect-selection']")
        show_all_button_locator = (
            By.XPATH,
            "//*[@class='additional-btns']//button[contains(@class, 'get-selected')]")
        cancel_button_locator = (
            By.XPATH, "//button[text()='CANCEL']")
        checked_checkbox_locators = (
            By.XPATH,
            "//div[@class='bootbox-body']//ul[contains(@class, 'select-items')]//li[@class='select-item']//input")
        self.wait_for_element_to_be_clickable(field_locator)
        self.click_on_element(field_locator)
        self.click_on_element(show_all_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        checked_checkbox_elements = self.wait_for_presence_of_all_elements_located(
            checked_checkbox_locators)
        for checked_checkbox_element in checked_checkbox_elements:
            if checked_checkbox_element.is_selected():
                index = checked_checkbox_elements.index(
                    checked_checkbox_element) + 1
                checked_checkbox_locator = (
                    By.XPATH,
                    "(//div[@class='bootbox-body']//ul[contains(@class, 'select-items')]//li["
                    "@class='select-item']//input/following-sibling::label)[" + str(
                        index) + "]")
                checked_checkbox_element = self.wait_for_presence_of_element(
                    checked_checkbox_locator)
                selected_checkboxes.append(
                    checked_checkbox_element.text)
        self.click_on_element(cancel_button_locator)
        return selected_checkboxes

    def check_uncheck_specific_checkbox(self, checkbox_name_or_data_qa, do_check,
                                        value="", index="1",
                                        without_text=False):
        if without_text:
            if value != "":
                checkbox_locator = "//label[normalize-space()='" + checkbox_name_or_data_qa + "']/..//input[@value='" + value + \
                                   "'] | //label[text()='" + checkbox_name_or_data_qa + "']/..//input[@value='" + value + "'] | " \
                                                                                                                          "//input[@data-qa='" + checkbox_name_or_data_qa + "' and @value='" + value + "']"
            else:
                checkbox_locator = "(//*[normalize-space()='" + checkbox_name_or_data_qa + "']/..//input | //*[text(" \
                                                                                           ")='" + checkbox_name_or_data_qa + \
                                   "']/..//input | //input[@data-qa='" + checkbox_name_or_data_qa + "'])[" + str(
                    index) + "]"
        else:
            if value != "":
                checkbox_locator = "//label[normalize-space(text())='" + checkbox_name_or_data_qa + "']/..//input[@value='" + \
                                   value + "'] | //label[text()='" + checkbox_name_or_data_qa + "']/..//input[@value='" + value + \
                                   "'] | //input[@data-qa='" + checkbox_name_or_data_qa + "' and @value='" + value + "']"
            else:
                checkbox_locator = "(//*[normalize-space(text())='" + checkbox_name_or_data_qa + "']/..//input | //*[text(" \
                                                                                                 ")='" + checkbox_name_or_data_qa + \
                                   "']/..//input | //input[@data-qa='" + checkbox_name_or_data_qa + "'])[" + str(
                    index) + "]"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != do_check:
            self.click_on_element(checkbox_locator)

    def get_text_using_tag_attribute(self, tag_name="", attribute_name="",
                                     attribute_value="",
                                     time_out=HALF_MINUTE):
        if attribute_name == self.id_attribute:
            locator = (By.ID, attribute_value)
        else:
            locator = (By.XPATH,
                       "//" + tag_name + "[@" + attribute_name + "='" + attribute_value + "']")
        if tag_name == "input":
            text = self.wait_for_presence_of_element(
                locator).get_attribute(
                'value')
        else:
            WebDriverWait(self.driver, time_out).until(
                EC.presence_of_element_located(locator),
                "Web element was not available within the specific time out. "
                "Locator: '" + str(locator) + "'")
            text = self.wait_for_presence_of_element(locator).text
        return text

    def set_text_using_tag_attribute(self, tag_name="", attribute_name="",
                                     attribute_value="", input_value="",
                                     index=1):
        if attribute_name == self.id_attribute:
            locator = (By.ID, attribute_value)
        else:
            locator_string = "(//" + tag_name + "[@" + attribute_name + "='" + attribute_value + "'])[" + str(
                index) + \
                             "]"
            locator = (By.XPATH, locator_string)
        self.set_value_into_element(locator, input_value)

    def get_text_or_value_from_selected_option(self, dropdown_label_data_qa,
                                               value=False):

        if "//" in dropdown_label_data_qa:
            locators = (By.XPATH, dropdown_label_data_qa + "//option")
        else:

            locators = (By.XPATH,
                        "(//label[contains(text(), '" + dropdown_label_data_qa + "')]/..//select//option | //select[@data-qa='" + \
                        dropdown_label_data_qa + "']//option)")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        option = ""
        for element in elements:
            if element.is_selected():
                if value:
                    option = str(
                        element.get_attribute(
                            'value')).strip()
                    break
                else:
                    option = str(
                        element.text).strip()
                    break
        return option

    def get_text_or_value_from_single_selected_option(self, locator_data_qa,
                                                      value=False):

        if "//" in locator_data_qa:
            locators = (By.XPATH, locator_data_qa + "//option")
        else:
            locators = (By.XPATH,
                        "//select[@data-qa='" + locator_data_qa + "']//option")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        option = ""
        for element in elements:
            if element.is_selected():
                if value:
                    option = str(
                        element.get_attribute(
                            'value')).strip()
                    break
                else:
                    option = str(
                        element.text).strip()
                    break
        return option

    def get_selected_value_of_modal_from_field(self,
                                               select_tag_id_or_class="",
                                               field_label_or_data_qa="",
                                               select_any_value=False):
        if field_label_or_data_qa == "":
            locator = (By.XPATH,
                       "//select[@id='" + select_tag_id_or_class + "']/following-sibling::span//span["
                                                                   "@class='mselect-selection__rendered selected'] | "
                                                                   "//select[@class='" + select_tag_id_or_class +
                       "']/following-sibling::span//span[@class='mselect-selection__rendered selected']")
        else:
            if select_any_value:
                locator = (By.XPATH,
                           "//label[contains(text(), '" + field_label_or_data_qa + "')]/..//span["
                                                                                   "@class='mselect-selection__rendered'] | //select[@data-qa='" + field_label_or_data_qa + "']/..//span[@title]")
            else:
                locator = (By.XPATH,
                           "//label[contains(text(), '" + field_label_or_data_qa + "')]/..//span["
                                                                                   "@class='mselect-selection__rendered "
                                                                                   "selected'] | //select[@data-qa='" + field_label_or_data_qa + "']/..//span[@title]")

        return self.wait_for_presence_of_element(locator).text

    def get_selected_checkbox_name_from_a_section(self, section_div_id,
                                                  label_is_parent=False,
                                                  span_is_present=False,
                                                  multiple=False):
        locators = (By.XPATH,
                    "//div[@id='" + section_div_id + "']//input[@type='checkbox']")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        if multiple:
            checkbox_names = []
            for index in range(len(elements)):
                if elements[index].is_selected():
                    locator = "(//div[@id='" + section_div_id + "']//input[@type='checkbox'])[" + str(
                        index + 1) + "]/.."
                    if label_is_parent:
                        checkbox_names.append(
                            str(self.wait_for_presence_of_element(
                                (By.XPATH,
                                 locator)).text).strip())
                    elif span_is_present:
                        checkbox_names.append(
                            str(self.wait_for_presence_of_element(
                                (By.XPATH,
                                 locator + "//span")).text).strip())
                    else:
                        checkbox_names.append(
                            str(self.wait_for_presence_of_element(
                                (By.XPATH,
                                 locator + "//label")).text).strip())
            return checkbox_names
        else:
            checkbox_name = ""
            for index in range(len(elements)):
                if elements[index].is_selected():
                    locator = "(//div[@id='" + section_div_id + "']//input[@type='checkbox'])[" + str(
                        index + 1) + "]/.."
                    if label_is_parent:
                        checkbox_name = str(
                            self.wait_for_presence_of_element(
                                (By.XPATH,
                                 locator)).text).strip()
                    elif span_is_present:
                        checkbox_name = str(
                            self.wait_for_presence_of_element(
                                (By.XPATH,
                                 locator + "//span")).text).strip()
                    else:
                        checkbox_name = str(
                            self.wait_for_presence_of_element(
                                (By.XPATH,
                                 locator + "//label")).text).strip()
            return checkbox_name

    def get_checkbox_status(self, checkbox_name_or_data_qa, value="",
                            without_text=False):
        if without_text:
            if value != "":
                checkbox_locator = "//label[normalize-space()='" + checkbox_name_or_data_qa + "']/..//input[@value='" + value + \
                                   "'] | //label[text()='" + checkbox_name_or_data_qa + "']/..//input[@value='" + value + "'] | " \
                                                                                                                          "//input[@data-qa='" + checkbox_name_or_data_qa + "' and @value='" + value + "']"
            else:
                checkbox_locator = "//label[normalize-space()='" + checkbox_name_or_data_qa + "']/..//input | //label[text()='" + \
                                   checkbox_name_or_data_qa + "']/..//input | //input[@data-qa='" + checkbox_name_or_data_qa + "']"
        else:
            if value != "":
                checkbox_locator = "//label[normalize-space(text())='" + checkbox_name_or_data_qa + "']/..//input[@value='" + \
                                   value + "'] | //label[text()='" + checkbox_name_or_data_qa + "']/..//input[@value='" + value + \
                                   "'] | //input[@data-qa='" + checkbox_name_or_data_qa + "' and @value='" + value + "']"
            else:
                checkbox_locator = "//label[normalize-space(text())='" + checkbox_name_or_data_qa + "']/..//input | //label[" \
                                                                                                    "text()='" + checkbox_name_or_data_qa + \
                                   "']/..//input | //input[@data-qa='" + checkbox_name_or_data_qa + "']"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected():
            return 'True'
        else:
            return ''

    def get_checkbox_status_for_specific_checkbox(self, checkbox_locator):
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected():
            return 'True'
        else:
            return ''

    def check_uncheck_specific_grid_row_checkbox(self, parent_div_id,
                                                 check_the_checkbox,
                                                 check_all_checkbox=False,
                                                 column_value_to_identify_column="",
                                                 data_qa_attribute_id=None):
        if check_all_checkbox:
            checkbox_locator = "(//div[@id='" + parent_div_id + "']//tr[1]//input[@type='checkbox'])[1]"
        else:
            if data_qa_attribute_id is not None:
                checkbox_locator = "//tr[@data-qa=" + data_qa_attribute_id + "]//input[@type='checkbox']"
            else:
                checkbox_locator = "//div[@id='" + parent_div_id + "']//a[normalize-space()='" + \
                                   column_value_to_identify_column + "']/..//..//..//input[@type='checkbox']"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != check_the_checkbox:
            self.click_on_element(checkbox_locator)

    def select_item_from_multi_action_menu(self, action_button_id,
                                           item_name_to_select):
        actions_locator = (
            By.XPATH, "//*[@id='" + action_button_id + "']")
        self.click_on_element(actions_locator)
        actions_item_locator = (
            By.XPATH, "//a[@title='" + item_name_to_select + "']")
        self.click_on_element(actions_item_locator)

    def switch_to_new_window(self):
        time.sleep(self.TWO_SEC_DELAY)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_the_current_window_and_back_to_previous_window(self):
        self.driver.close()
        time.sleep(self.TWO_SEC_DELAY)
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_specific_form_grid_column_index(self, form_tag_id,
                                            column_name):
        index = 0
        locators = (
            By.XPATH,
            "//form[@id='" + form_tag_id + "']//tr[1]//td")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        for index in range(len(elements)):
            column_locator = (By.XPATH,
                              "//form[@id='" + form_tag_id + "']//tr[1]//th[" + str(
                                  index + 1) + "]")
            if self.get_element_text(
                    column_locator) == column_name:
                index = index + 1
                break
        return index

    def set_value_into_specific_form_grid_input_field(self, form_tag_id,
                                                      column_name,
                                                      column_value_to_set,
                                                      row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         column_name)
        locator = (By.XPATH,
                   "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                       index) + "]//textarea | //form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                       index) + "]//input")
        self.set_value_into_element(locator, column_value_to_set)

    def select_dropdown_value_from_specific_form_grid(self, form_tag_id,
                                                      column_name,
                                                      column_value_to_select,
                                                      row_number="1",
                                                      search_option_available=True):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         column_name)
        dropdown_icon_locator = (By.XPATH,
                                 "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                                     index) + "]//span[@role='presentation']")
        self.click_on_element(dropdown_icon_locator)
        if search_option_available:
            input_field_locator = (
                By.XPATH,
                "//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']")
            self.set_value_into_element(input_field_locator,
                                        column_value_to_select)
            self.wait_for_presence_of_element(
                input_field_locator).send_keys(
                Keys.ENTER)
        else:
            self.wait_for_presence_of_element(
                (By.XPATH,
                 "//li[normalize-space()='" + column_value_to_select + "']")).click()

    def select_value_from_specific_form_grid_modal(self, form_tag_id,
                                                   column_name,
                                                   column_value_to_select,
                                                   row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         column_name)
        dropdown_icon_locator = (By.XPATH,
                                 "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                                     index) + "]//span[@role='presentation']")
        self.click_on_element(dropdown_icon_locator)
        self.select_from_modal(column_value_to_select)

    def check_uncheck_specific_form_grid_row_checkbox(self, form_tag_id,
                                                      column_name,
                                                      check_the_checkbox,
                                                      row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         column_name)
        checkbox_locator = (By.XPATH,
                            "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                                index) + "]//input[@type='checkbox']")
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != check_the_checkbox:
            self.click_on_element(checkbox_locator)

    def deselect_all_options_from_grid_modal(self, locator):
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        Select(self.driver.find_element(By.XPATH,
                                        locator)).deselect_all()

    def check_uncheck_specific_form_grid_row_checkbox_modal(self,
                                                            checkbox_name,
                                                            do_check,
                                                            value="",
                                                            row_number="1"):
        if value != "":
            checkbox_locator = "(// label[normalize-space(text())='" + checkbox_name + "'] /..// input[ @value = '" \
                               + value + "'])[" + row_number + "] | (// label[text() = '" + checkbox_name + "'] /..// " \
                                                                                                            "input[ " \
                                                                                                            "@value = " \
                                                                                                            "'" + \
                               value + "'])[" + row_number + "] "
        else:
            checkbox_locator = "(//input[@data-name='" + checkbox_name + "'])[" + row_number + "]"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != do_check:
            self.click_on_element(checkbox_locator)

    def click_link_of_specific_column_of_specific_row_from_grid(self,
                                                                form_tag_id,
                                                                column_name,
                                                                row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         column_name)
        locator = (By.XPATH,
                   "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                       index) + "]//div")
        self.click_on_element(locator)

    def click_ok_button_of_specific_column_modal_from_grid(self,
                                                           form_tag_id,
                                                           column_name,
                                                           row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         column_name)
        locator = (By.XPATH,
                   "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                       index) + "]//button[@class='btn btn-primary js-modal-data-save']")
        self.scroll_to_specific_element(locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(locator)

    def wait_for_element_to_be_invisible(self, locator,
                                         time_out=ONE_MINUTE,
                                         max_retries=1):
        retries = 0
        while retries < max_retries:
            try:
                return WebDriverWait(self.driver,
                                     time_out).until(
                    EC.invisibility_of_element_located(
                        locator))
            except TimeoutException:
                retries += 1
                if retries == max_retries:
                    print(
                        f"Web element remain visible after specific time out. Locator: '{locator}'")
            except StaleElementReferenceException:
                retries += 1

    def click_element_execute_script(self, locator,
                                     locator_initialize=False):
        if locator_initialize:
            (method, locator) = locator
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].click();",
                                       element)
        else:
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].click();",
                                       element)

    def click_on_specific_tab(self, tab_name_or_data_qa):
        tab_locator = (By.XPATH,
                       "//a[normalize-space()='" + tab_name_or_data_qa + "' and @data-toggle='tab'] | //a["
                                                                         "@data-qa='" + tab_name_or_data_qa + "']")
        self.click_on_element(tab_locator)

    def switch_to_iframe(self, locator, is_element=False):
        if is_element:
            iframe = locator
        else:
            iframe = self.wait_for_presence_of_element(locator)
        self.driver.switch_to.frame(iframe)
        time.sleep(self.TWO_SEC_DELAY)

    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    def get_attribute_value(self, locator, attribute_name,
                            locator_initialization=False):
        if locator_initialization:
            if "//" in locator:
                locator = (By.XPATH, locator)
            else:
                locator = (By.ID, locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                locator = locator
            else:
                locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
        return self.wait_for_presence_of_element(
            locator).get_attribute(
            attribute_name)

    def click_on_specific_button(self, button_name_or_data_qa,
                                 script_executor_click=False, locator_to_be_appeared=None):
        button_locator = "//button[normalize-space(text())='" + button_name_or_data_qa + "'] | //a[normalize-space()='" + \
                         button_name_or_data_qa + "'] | //*[@data-qa='" + button_name_or_data_qa + "']"
        if script_executor_click:
            self.click_element_execute_script(button_locator)
        else:
            self.click_on_element(button_locator,
                                  locator_initialization=True,
                                  locator_to_be_appeared=locator_to_be_appeared)

    def get_specific_grid_column_index(self, div_id, column_name):
        index = 0
        locators = (By.XPATH, "//div[@id='" + div_id + "']//tr[1]//th")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        for index in range(len(elements)):
            column_locator = (By.XPATH,
                              "//div[@id='" + div_id + "']//tr[1]//th[" + str(
                                  index + 1) + "]")
            actual_column_value = self.get_element_text(
                column_locator)
            if actual_column_value == '':
                actual_column_value = self.wait_for_presence_of_element(
                    column_locator).get_attribute(
                    "innerHTML")
            if actual_column_value == column_name:
                index = index + 1
                break
        return index

    def get_value_from_specific_grid_column(self, div_id, column_name,
                                            a_tag=False, row_number="1"):
        index = self.get_specific_grid_column_index(div_id,
                                                    column_name)
        if a_tag:
            locator = (
                By.XPATH,
                "//div[@id='" + div_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                    index) + "]//a")
        else:
            locator = (By.XPATH,
                       "//div[@id='" + div_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                           index) + "]")
        value = self.get_element_text(locator)
        return str(value)

    def is_image_present(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            status = self.driver.execute_script(
                "return arguments[0].complete " + "&& typeof arguments[0].naturalWidth != \"undefined\" " + "&& "
                                                                                                            "arguments["
                                                                                                            "0].naturalWidth > 0",
                element)
        except Exception as e:
            print(e)
            status = False
        return status

    def get_value_from_specific_input_field(self, field_name_or_data_qa,
                                            is_textarea=False,
                                            inner_html=False):
        if is_textarea:
            field_locator = (By.XPATH,
                             "//label[normalize-space(text())='" + field_name_or_data_qa + "']/..//textarea | //*["
                                                                                           "@data-qa='" + field_name_or_data_qa + "']")
        else:
            field_locator = (By.XPATH,
                             "//label[normalize-space(text())='" + field_name_or_data_qa + "']/..//input | //*[@data-qa='" +
                             field_name_or_data_qa + "']")
        if is_textarea is False:
            text = self.wait_for_presence_of_element(
                field_locator).get_attribute('value')
        elif inner_html:
            text = self.wait_for_presence_of_element(
                field_locator).get_attribute("innerHTML")
        else:
            text = self.wait_for_presence_of_element(
                field_locator).text
        return text

    def select_specific_radio_button(self, radio_button_name):
        locator = (By.XPATH,
                   "//label[normalize-space()='" + radio_button_name + "']//input")
        self.click_on_element(locator)

    def is_specific_field_enabled(self, field_name_or_data_qa, is_input_field=False):
        if is_input_field:
            locator = "//label[normalize-space()='" + field_name_or_data_qa + "']/..//input | //input[@data-qa='" + field_name_or_data_qa + "']"
            element = self.driver.find_element(By.XPATH, locator)
            status = element.get_attribute('readonly')
            return not status
        else:
            locator = "//label[normalize-space()='" + field_name_or_data_qa + "']/..//select | //select[" \
                                                                              "@data-qa='" + field_name_or_data_qa + "']"
            element = self.driver.find_element(By.XPATH, locator)
            return element.is_enabled()

    def scroll_to_specific_element(self, locator,
                                   locator_initialization=False):
        if locator_initialization:
            if "//" in locator:
                locator = (By.XPATH, locator)
            else:
                locator = (By.ID, locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(
            self.wait_for_presence_of_element(locator)).perform()

    def wait_for_spinner_load(self, timeout=60, spinner_locator=None, wait_for_loading_spinner_to_start=2):
        """
        Implementing wait for spinner load functionality
        Wait until Spinner exists on UI. Once it is disappeared, exit from loop
        Default time out value up to 60 secs
        :param wait_for_loading_spinner_to_start:
        :param timeout:
        :param spinner_locator:
        :return:
        """
        try:
            if spinner_locator is not None:
                spinner_load_locator = spinner_locator
            else:
                spinner_load_locator = (
                    By.XPATH,
                    "//div[@class='dataTables_processing card']")
            spinner_control = WebDriverWait(self.driver, wait_for_loading_spinner_to_start).until(
                EC.visibility_of_all_elements_located(
                    spinner_load_locator),
                'spinner load locator not found before specified time out')
            end_time = time.time() + timeout
            flag = False
            while len(spinner_control) > 0:
                spinner_control = WebDriverWait(self.driver,
                                                wait_for_loading_spinner_to_start).until(
                    EC.visibility_of_all_elements_located(
                        spinner_load_locator),
                    'spinner load locator not found before specified time out')
                for element in spinner_control:
                    if "display: none;" in element.get_attribute(
                            "style"):
                        flag = True
                        break
                if flag:
                    break
                if time.time() > end_time:
                    break

        except TimeoutException:
            pass
        except NoSuchElementException:
            pass
        except ElementNotVisibleException:
            pass
        except WebDriverException:
            pass

    @staticmethod
    def is_a_specific_file_available_into_a_folder(folder_path, file_name):
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            return True
        else:
            return False

    def go_back(self):
        self.driver.back()

    def take_screenshot(self, screenshot_filename,
                        screenshot_folder='tests_screenshots'):
        screenshot_dir = os.path.join(os.getcwd(), screenshot_folder)
        screenshot_path = os.path.join(screenshot_dir,
                                       screenshot_filename)
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)
        self.driver.save_screenshot(screenshot_path)

    @staticmethod
    def change_resolution(image_filename, new_width=1920, new_height=1080,
                          output_filename=None):
        """
        Resize provided image while maintaining resolution compatibility
        across different environments, such as headful, headless, and jenkins.
        """
        image_path = os.path.join(os.getcwd(), 'tests_screenshots',
                                  image_filename)
        image = Image.open(image_path)
        new_image = image.resize((new_width, new_height))
        if output_filename is None:
            output_filename = image_filename
        output_path = os.path.join(os.getcwd(), 'tests_screenshots',
                                   output_filename)
        new_image.save(output_path)

    @staticmethod
    def get_file_size(file_directory, file_name):
        files = os.listdir(file_directory)
        for file in files:
            if fnmatch.fnmatch(file, file_name):
                full_file_path = os.path.join(file_directory, file)
                file_size = os.path.getsize(full_file_path)
                return file_size
        raise FileNotFoundError(
            f"No files matching the file name '{file_name}' found in the specified directory.")

    @staticmethod
    def is_a_file_with_specific_file_name_part_available_into_a_folder(file_directory, file_name_part):
        files = [file for file in os.listdir(file_directory) if re.match(file_name_part, file)]
        return len(files) > 0

    @staticmethod
    def delete_file(file_directory, file_name):
        files = os.listdir(file_directory)
        deleted_count = 0
        for file in files:
            if fnmatch.fnmatch(file, file_name):
                full_file_directory = os.path.join(file_directory, file)
                os.remove(full_file_directory)
                deleted_count += 1
        if deleted_count == 0:
            raise FileNotFoundError(
                f"No files matching the file name '{file_name}' found in the specified directory.")
        return deleted_count

    def get_text_or_value_from_list(self, locator, selected_option="", attribute_name=None,
                                    locator_initialization=False, split_text=True):
        """
        Implementing get text or value from list
        :param locator:
        :param selected_option:
        :param attribute_name:
        :param locator_initialization:
        :return:
        """
        if locator_initialization:
            locator = (By.XPATH, locator)
        self.wait_for_visibility_of_all_elements_located(locator)
        elements = self.driver.find_elements(*locator)
        if attribute_name is None:
            if split_text:
                elements_list = [element.text.split('(')[0].strip() for element in elements]
            else:
                elements_list = [element.text for element in elements]
        else:
            elements_list = [element.get_attribute(attribute_name) for element in elements]
        if selected_option is not "":
            if all(element == selected_option for element in elements_list):
                return selected_option
            else:
                return None
        else:
            return elements_list

    def drag_and_drop_for_dashboard(self, source_locator, target_locator, retries=10):
        action_chains = ActionChains(self.driver)
        while retries > 0:
            try:
                source_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, source_locator)))
                action_chains.click_and_hold(source_element).perform()
                target_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                                      target_locator)))
                action_chains.move_to_element(target_element).perform()
                action_chains.release(target_element).perform()
                break
            except Exception as e:
                retries -= 1
                time.sleep(0.5)
                if retries == 0:
                    raise e

    @staticmethod
    def is_list_sorted(data_list, numbers=False, dates=False, order='ascending'):
        if not data_list:
            raise ValueError("The list is empty")
        if numbers:
            data_list = [Decimal(element.replace(',', '')) for element in data_list]
            if order == 'ascending':
                if data_list == sorted(data_list):
                    return True
            elif order == 'descending':
                if data_list == sorted(data_list, reverse=True):
                    return True
        if dates:
            data_list = [datetime.strptime(date_1, "%d %b, %Y").strftime("%Y-%m-%d") for date_1 in data_list]
        if order == 'ascending':
            if data_list == sorted(data_list, key=str.lower):
                return True
        elif order == 'descending':
            if data_list == sorted(data_list, key=str.lower, reverse=True):
                return True
        else:
            raise ValueError

    @staticmethod
    def round_up_half_float(number_to_round):
        return str(Decimal(str(number_to_round)).quantize(Decimal('0.01'), ROUND_HALF_UP))

    @staticmethod
    def get_random_string(length=10):
        return uuid.uuid4().hex[:length]

    @staticmethod
    def base64_encoder(path_to_file):
        with open(path_to_file, 'rb') as zip_file:
            zip_data = zip_file.read()
        base64_encoded_data = base64.b64encode(zip_data).decode('utf-8')
        return base64_encoded_data

    @staticmethod
    def ordered(data_list):
        return sorted(data_list, key=lambda x: x["id"])

    @staticmethod
    def get_specific_date_with_specific_format_for_api(date_format, days_to_add=0, days_to_subtract=0):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        expected_date = None
        if days_to_add != 0:
            expected_date = dt.datetime.today() + dt.timedelta(days=days_to_add)
        elif days_to_subtract != 0:
            expected_date = dt.datetime.today() - dt.timedelta(days=days_to_subtract)
        elif days_to_add == 0 and days_to_subtract == 0:
            expected_date = dt.datetime.today()
        date1 = expected_date.strftime(date_format)
        return str(date1)
