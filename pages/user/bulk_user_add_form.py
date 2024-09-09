from pages.base_page import BasePage
from locators.user.bulk_user_add_form_locators import BulkUserAddFormLocators
from selenium.webdriver.common.keys import Keys


class DashboardBulkUserAddFormPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_bulk_user_information(self, data):
        self.select_dropdown_value(BulkUserAddFormLocators.agency_client_account_label, data['user_to_copy'])
        self.set_value_into_element(
            BulkUserAddFormLocators.email_input_locator,
            data['email'])
        self.wait_for_presence_of_element(
            BulkUserAddFormLocators.email_input_locator).send_keys(
            Keys.SPACE)
        self.click_on_element(
            BulkUserAddFormLocators.send_invitation_button_data_qa)
