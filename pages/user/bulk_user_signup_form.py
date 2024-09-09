from pages.base_page import BasePage
from locators.user.bulk_user_signup_form_locators import \
    BulkUserSignUpFormLocators
import time


class DashboardBulkUserSignUpFormPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_bulk_user_signup_information(self, data,
                                             generated_password):
        self.set_value_into_element(
            BulkUserSignUpFormLocators.password_locator,
            generated_password)
        self.set_value_into_element(
            BulkUserSignUpFormLocators.repeat_password_locator,
            generated_password)
        self.set_value_into_element(
            BulkUserSignUpFormLocators.account_name_locator,
            data['account_name'])
        self.set_value_into_element(
            BulkUserSignUpFormLocators.contact_person_full_name_locator,
            data['contact_person_full_name'])
        self.set_value_into_element(
            BulkUserSignUpFormLocators.contact_person_phone_locator,
            data['contact_person_phone'])
        time.sleep(2)
        self.click_on_element(
            BulkUserSignUpFormLocators.submit_button_locator)

    def click_login_button_after_signup(self):
        self.click_on_element(
            BulkUserSignUpFormLocators.login_button_locator)
