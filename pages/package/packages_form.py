import time

from selenium.webdriver.common.by import By

from configurations.generic_modules import step_printer
from locators.package.package_form_locator import PackageFormLocators
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
import os

package_information = {'package_mandatory_data': {}, 'package_remaining_data': {}}


class DashboardPackagesForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_package_data_and_save(self, package_data, filters_selected=False):
        step_printer("PACKAGE_MANDATORY_DATA")
        self.provide_package_mandatory_data(package_data)

        step_printer("PACKAGE_REMAINING_DATA")
        self.provide_package_remaining_data(package_data)

        if filters_selected:
            self.select_package_filters(package_data)

        self.click_on_element(PackageFormLocators.save_button_locator_data_qa)

    def provide_package_mandatory_data(self, package_data):
        self.set_value_into_specific_input_field(PackageFormLocators.package_field_data_qa,
                                                 package_data['package_mandatory_data']['name'])
        self.select_dropdown_value(PackageFormLocators.auction_type_data_qa,
                                   package_data['package_mandatory_data']['auction_type'])
        self.set_value_into_specific_input_field(
            PackageFormLocators.csv_upload_label, os.path.join(os.getcwd(), package_data['package_mandatory_data'][
                                                                                                        'csv_upload']))

    def provide_package_remaining_data(self, package_data):
        self.select_from_modal(package_data['package_remaining_data']['user'], PackageFormLocators.user_data_qa,
                               is_delay='yes')
        self.select_from_modal(package_data['package_remaining_data']['tags'], PackageFormLocators.tags_data_qa)

    def select_package_filters(self, package_data):
        self.select_from_modal(package_data['package_remaining_data']['country'], PackageFormLocators.country_data_qa,
                               is_delay='yes')
        self.select_from_modal(package_data['package_remaining_data']['exchange'], PackageFormLocators.exchange_data_qa,
                               is_delay='yes')
        self.select_from_modal("", PackageFormLocators.environment_data_qa, is_delay='yes',
                               search_data_qa=package_data['package_remaining_data']['environment'])

    def get_package_data(self, operation='add', filters_selected=False):
        self.reset_package_information()
        self.get_package_mandatory_data(operation)
        self.get_package_remaining_data()
        if filters_selected:
            self.get_package_filters_data()
        self.click_on_element(
            PackageFormLocators.cancel_button_locator_data_qa)
        return package_information

    def get_package_mandatory_data(self, operation='add'):
        self.reset_package_information()
        package_information['package_mandatory_data'][
            'name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            PackageFormLocators.package_field_data_qa)
        package_information['package_mandatory_data'][
            'auction_type'] = self.get_text_or_value_from_selected_option(
            PackageFormLocators.auction_type_label)
        if operation == 'edit':
            package_information['package_mandatory_data'][
                'csv_upload'] = 'assets/packages/edit_package_sites.csv'
        else:
            package_information['package_mandatory_data'][
                'csv_upload'] = 'assets/packages/package_sites.csv'

        package_information['sites'] = self.get_packages_sites()
        return package_information

    def get_package_remaining_data(self):
        package_information['package_remaining_data']['user'] = self.get_text_using_tag_attribute(
            self.span_tag, self.data_qa_attribute, PackageFormLocators.user_data_qa)
        package_information['package_remaining_data']['tags'] = self.get_text_using_tag_attribute(
            self.span_tag, self.data_qa_attribute, PackageFormLocators.tags_data_qa)
        return package_information

    def get_package_filters_data(self):
        time.sleep(self.TWO_SEC_DELAY)
        package_information['package_remaining_data']['country'] = self.get_text_using_tag_attribute(
            self.span_tag, self.data_qa_attribute, PackageFormLocators.country_data_qa)
        package_information['package_remaining_data']['exchange'] = self.get_text_using_tag_attribute(
            self.span_tag, self.data_qa_attribute, PackageFormLocators.exchange_data_qa)
        package_information['package_remaining_data']['environment'] = self.get_text_using_tag_attribute(
            self.span_tag, self.data_qa_attribute, PackageFormLocators.environment_data_qa)
        return package_information

    def get_packages_sites(self):
        sites = []
        for option in Select(self.driver.find_element(By.ID,
                                                      PackageFormLocators.selected_site_list_id)).options:
            sites.append(option.get_attribute('value'))
        sites.sort()
        return sites

    @staticmethod
    def reset_package_information():
        global package_information
        package_information = {'package_mandatory_data': {}, 'package_remaining_data': {}}
