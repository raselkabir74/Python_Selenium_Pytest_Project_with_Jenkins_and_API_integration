from pages.base_page import BasePage
from locators.country_settings.country_settings_form_locators import \
    CountrySettingsLocators
import time

country_settings_information = {}


class DashboardCountrySettingsList(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def add_country_settings(self, data):
        self.click_on_element(
            CountrySettingsLocators.add_new_country_button_locator)
        self.select_dropdown_value(CountrySettingsLocators.select_country_label, data['country'])
        self.click_on_element(
            CountrySettingsLocators.ok_button_modal_locator)
        self.click_on_element(
            CountrySettingsLocators.cpc_checkbox_xpath.format(
                data['country']),
            locator_initialization=True)
        self.set_value_into_element(
            CountrySettingsLocators.cpc_maximum_cpc_input_xpath.format(
                data['country']), data['cpc']['maximum_cpc'],
            locator_initialization=True)
        self.set_value_into_element(
            CountrySettingsLocators.cpc_minimum_impression_learn_xpath.format(
                data['country']),
            data['cpc']['minimum_impression'],
            locator_initialization=True)
        self.set_value_into_element(
            CountrySettingsLocators.cpc_minimum_spend_learn_xpath.format(
                data['country']),
            data['cpc']['maximum_spend'],
            locator_initialization=True)
        self.click_on_element(
            CountrySettingsLocators.save_all_button_locator)
        time.sleep(self.TWO_SEC_DELAY)

    def get_success_message(self):
        return self.get_element_text(
            CountrySettingsLocators.success_message_locator)

    def delete_country_settings(self, data):
        self.click_on_element(
            CountrySettingsLocators.cross_icon_xpath.format(
                data['country']),
            locator_initialization=True)
        self.click_on_element(
            CountrySettingsLocators.ok_button_modal_locator)
        self.click_on_element(
            CountrySettingsLocators.save_all_button_locator)
        time.sleep(self.TWO_SEC_DELAY)

    def get_country_settings_data(self, data):
        self.reset_country_settings_information()
        country_settings_information['country'] = data['country']
        country_settings_information['cpc'][
            'maximum_cpc'] = self.get_element_text(
            CountrySettingsLocators.cpc_maximum_cpc_input_xpath.format(
                data['country']), locator_initialization=True,
            input_tag=True)
        country_settings_information['cpc'][
            'minimum_impression'] = self.get_element_text(
            CountrySettingsLocators.cpc_minimum_impression_learn_xpath.format(
                data['country']),
            locator_initialization=True, input_tag=True)
        country_settings_information['cpc'][
            'maximum_spend'] = self.get_element_text(
            CountrySettingsLocators.cpc_minimum_spend_learn_xpath.format(
                data['country']), locator_initialization=True,
            input_tag=True)
        return country_settings_information

    def reset_country_settings_information(self):
        global country_settings_information
        country_settings_information = {"cpc": {}}
