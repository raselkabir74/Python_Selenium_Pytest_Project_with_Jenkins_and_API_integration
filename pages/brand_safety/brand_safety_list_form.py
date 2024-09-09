from pages.base_page import BasePage
from locators.brand_safety.brand_safety_list_locators import \
    BrandSafetyListLocators
import time
from selenium.webdriver.common.keys import Keys


class DashboardKeywordListForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_add_keywords_page(self):
        self.click_on_element(
            BrandSafetyListLocators.add_button_locator)

    def navigate_to_keyword_count_page(self, brand_safety_name):
        self.click_on_element(
            BrandSafetyListLocators.keyword_count_xpath.format(
                brand_safety_name),
            locator_initialization=True)

    def delete_keywords(self, brand_safety_name):
        self.click_on_element(
            BrandSafetyListLocators.three_dot_of_campaign_xpath.format(
                brand_safety_name),
            locator_initialization=True)
        self.click_on_three_dot_option(
            BrandSafetyListLocators.delete_data_qa)
        self.click_on_element(
            BrandSafetyListLocators.confirm_button_alert_locator)

    def navigate_to_edit_keywords(self, brand_safety_name):
        self.click_on_element(
            BrandSafetyListLocators.brand_safety_option_edit_link_xpath.format(
                brand_safety_name),
            locator_initialization=True)

    def get_success_message(self):
        return self.get_element_text(
            BrandSafetyListLocators.success_message_locator)

    def search(self, brand_safety_name):
        time.sleep(1)
        self.set_value_into_element(
            BrandSafetyListLocators.search_field_locator,
            brand_safety_name)
        self.wait_for_presence_of_element(
            BrandSafetyListLocators.search_field_locator).send_keys(
            Keys.ENTER)
        time.sleep(1)
