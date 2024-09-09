import time

from selenium.webdriver.common.by import By

from locators.user.userform_locators import UserFormLocators
from pages.base_page import BasePage

user_information = {}


class DashboardUserFormPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_main_and_billing_info(self, data, generated_password):
        self.set_value_into_element(UserFormLocators.username_data_qa,
                                    data['username'])
        self.set_value_into_element(UserFormLocators.password_data_qa,
                                    generated_password)
        self.set_value_into_element(
            UserFormLocators.repeat_password_data_qa,
            generated_password)
        self.set_value_into_element(
            UserFormLocators.account_name_data_qa,
            data['account_name'])
        self.set_value_into_element(UserFormLocators.email_data_qa,
                                    data['email'])
        self.set_value_into_element(
            UserFormLocators.contact_person_full_name_data_qa,
            data['contact_person_full_name'])
        self.set_value_into_element(
            UserFormLocators.contact_person_email_data_qa,
            data['contact_person_email'])
        self.set_value_into_element(
            UserFormLocators.contact_person_phone_data_qa,
            data['contact_person_phone'])
        self.select_dropdown_value(UserFormLocators.country_label, data['country'])
        self.select_dropdown_value(UserFormLocators.company_label, data['company_name'])

    def provide_branding_info(self, data):
        self.select_dropdown_value(UserFormLocators.sales_manager_label, data['sales_manager'])
        self.select_dropdown_value(UserFormLocators.responsible_adops_label, data['responsible_adops'])
        self.select_dropdown_value(UserFormLocators.account_manager_label, data['account_manager'])

    def provide_currency_margin(self, data):
        self.select_dropdown_value(UserFormLocators.currency_label, data['currency'])
        self.set_value_into_element(UserFormLocators.min_bid_data_qa,
                                    data['min_bid'])
        self.set_value_into_element(UserFormLocators.max_bid_data_qa,
                                    data['max_bid'])
        self.set_value_into_element(UserFormLocators.tech_fee_data_qa,
                                    data['tech_fee'])

    def click_save_user_btn(self):
        self.click_on_element(UserFormLocators.save_button_locator)

    @staticmethod
    def reset_user_information():
        global user_information
        user_information = {'main_and_billing_info': {},
                            'branding_info': {},
                            'currency_margin': {}}

    def get_user_information(self):
        self.reset_user_information()
        user_information['main_and_billing_info'][
            'username'] = self.get_element_text(
            UserFormLocators.username_data_qa,
            input_tag=True)
        user_information['main_and_billing_info'][
            'account_name'] = self.get_element_text(
            UserFormLocators.account_name_data_qa, input_tag=True)
        user_information['main_and_billing_info'][
            'email'] = self.get_element_text(
            UserFormLocators.email_data_qa,
            input_tag=True)
        user_information['main_and_billing_info'][
            'contact_person_full_name'] = self.get_element_text(
            UserFormLocators.contact_person_full_name_data_qa,
            input_tag=True)
        user_information['main_and_billing_info'][
            'contact_person_email'] = self.get_element_text(
            UserFormLocators.contact_person_email_data_qa,
            input_tag=True)
        user_information['main_and_billing_info'][
            'contact_person_phone'] = self.get_element_text(
            UserFormLocators.contact_person_phone_data_qa,
            input_tag=True)
        user_information['main_and_billing_info'][
            'country'] = self.get_element_text(
            UserFormLocators.country_dropdown_locator)
        user_information['main_and_billing_info'][
            'company_name'] = self.get_element_text(
            UserFormLocators.company_dropdown_locator)
        user_information['branding_info'][
            'sales_manager'] = self.get_text_or_value_from_selected_option(
            UserFormLocators.sales_manager_label)
        user_information['branding_info'][
            'responsible_adops'] = self.get_text_or_value_from_selected_option(
            UserFormLocators.responsible_adops_label)
        user_information['branding_info'][
            'account_manager'] = self.get_text_or_value_from_selected_option(
            UserFormLocators.account_manager_label)
        user_information['currency_margin'][
            'currency'] = self.get_element_text(
            UserFormLocators.currency_dropdown_locator)
        user_information['currency_margin'][
            'currency_rate'] = self.get_element_text(
            UserFormLocators.currency_rate_data_qa, input_tag=True)
        user_information['currency_margin'][
            'min_bid'] = self.get_element_text(
            UserFormLocators.min_bid_data_qa,
            input_tag=True)
        user_information['currency_margin'][
            'max_bid'] = self.get_element_text(
            UserFormLocators.max_bid_data_qa,
            input_tag=True)
        user_information['currency_margin'][
            'tech_fee'] = self.get_element_text(
            UserFormLocators.tech_fee_data_qa,
            input_tag=True)
        self.click_on_element(UserFormLocators.cancel_button_locator)
        return user_information

    def provide_and_save_user_information(self, user_data,
                                          generated_password):
        self.provide_main_and_billing_info(
            user_data['main_and_billing_info'],
            generated_password)
        self.provide_branding_info(user_data['branding_info'])
        self.provide_currency_margin(user_data['currency_margin'])
        self.click_save_user_btn()

    def check_uncheck_checkbox(self, checkbox_name, do_check):
        checkbox_locator = (By.XPATH,
                            "//label[contains(text(),  '" + checkbox_name + "')]/..//input | //input[@data-qa='"
                            + checkbox_name + "']")
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != do_check:
            self.click_on_element(checkbox_locator)

    def provide_user_mandatory_information(self, data, generated_password):
        self.set_value_into_element(UserFormLocators.username_data_qa,
                                    data['main_and_billing_info']['username'])
        self.set_value_into_element(UserFormLocators.password_data_qa,
                                    generated_password)
        self.set_value_into_element(
            UserFormLocators.repeat_password_data_qa,
            generated_password)
        self.set_value_into_element(
            UserFormLocators.account_name_data_qa,
            data['main_and_billing_info']['account_name'])
        self.set_value_into_element(UserFormLocators.email_data_qa,
                                    data['main_and_billing_info']['email'])
        self.select_dropdown_value(UserFormLocators.country_label, data['main_and_billing_info']['country'])
        self.provide_branding_info(data['branding_info'])

    def select_child_acc(self, user_name, user_id):
        self.wait_for_element_to_be_clickable(UserFormLocators.select_user_locator)
        self.click_on_element(UserFormLocators.select_user_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.wait_for_presence_of_element(UserFormLocators.select_child_acc_user_search_locator). \
            send_keys(user_name)
        self.click_on_element(UserFormLocators.child_acc_checkbox_xpath.format(user_id), locator_initialization=True)
        self.click_on_element(UserFormLocators.select_btn_locator)
