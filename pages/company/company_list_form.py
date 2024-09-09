from pages.base_page import BasePage
from locators.company.company_list_locators import CompanyListLocators
from selenium.webdriver.common.keys import Keys
import time


class DashboardCompanyListForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_add_company_page(self):
        self.click_on_element(
            CompanyListLocators.add_company_button_locator_data_qa)

    def get_success_message(self):
        return self.get_element_text(
            CompanyListLocators.success_message_locator_data_qa)

    def get_no_record_found_message(self):
        time.sleep(self.ONE_SEC_DELAY)
        return self.get_element_text(
            CompanyListLocators.no_record_message_locator)

    def search_user_and_action(self, search_text, action='None'):
        time.sleep(self.ONE_SEC_DELAY)
        self.set_value_into_element(
            CompanyListLocators.search_box_locator_data_qa,
            search_text)
        self.wait_for_presence_of_element(
            CompanyListLocators.search_box_locator_data_qa).send_keys(
            Keys.ENTER)
        time.sleep(self.ONE_SEC_DELAY)
        if action != 'None':
            self.click_on_element(
                CompanyListLocators.three_dot_locator_xpath.format(
                    search_text),
                locator_initialization=True)
        if action.lower() == 'delete':
            self.click_on_element(
                CompanyListLocators.delete_option_locator)
            self.click_on_element(
                CompanyListLocators.alert_confirm_button_locator)
        elif action.lower() == 'edit':
            self.click_on_element(
                CompanyListLocators.edit_option_locator)
