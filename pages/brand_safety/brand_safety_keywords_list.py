from pages.base_page import BasePage
from locators.brand_safety.brand_safety_keywords_locators import \
    BrandSafetyKeywordsLocators
import time

brand_safety_information = {}


class DashboardBrandSafetyKeywordsList(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def get_keywords_list(self):
        keyword_list = []
        elements = self.wait_for_presence_of_all_elements_located(
            BrandSafetyKeywordsLocators.keywords_list_locator)
        for index in range(len(elements)):
            keyword_list.append(str(elements[index].text).strip())
        return keyword_list

    def get_success_message(self):
        return self.get_element_text(
            BrandSafetyKeywordsLocators.success_message_locator)

    def add_keyword(self, keyword_name):
        self.click_on_element(
            BrandSafetyKeywordsLocators.add_keywords_locator)
        self.set_value_into_element(
            BrandSafetyKeywordsLocators.keyword_provide_field_locator,
            keyword_name)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(
            BrandSafetyKeywordsLocators.confirm_button_alert_locator)
        self.wait_for_visibility_of_element(
            BrandSafetyKeywordsLocators.loader_locator)
        self.wait_for_element_to_be_invisible(
            BrandSafetyKeywordsLocators.loader_locator)

    def delete_keyword(self, keyword_name):
        self.click_on_element(
            BrandSafetyKeywordsLocators.delete_icon_locator_xpath.format(
                keyword_name),
            locator_initialization=True)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(
            BrandSafetyKeywordsLocators.confirm_button_alert_locator)
        if self.wait_for_visibility_of_element(
            BrandSafetyKeywordsLocators.loader_locator):
            self.wait_for_element_to_be_invisible(
                BrandSafetyKeywordsLocators.loader_locator)

    def navigate_back_to_brand_safety_list(self):
        self.click_on_element(
            BrandSafetyKeywordsLocators.brand_safety_link_locator)
