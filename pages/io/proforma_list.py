from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from locators.io.proforma_list_locator import ProformaListLocators
from locators.io.proforma_form_locator import ProformaFormLocators
from pages.base_page import BasePage


class DspDashboardProformaList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def search_and_action(self, io_title, io_id, action="None"):
        self.set_value_into_element(
            ProformaListLocators.search_field_locator, io_title)
        self.wait_for_presence_of_element(
            ProformaListLocators.search_field_locator).send_keys(
            Keys.ENTER)
        self.wait_for_visibility_of_element(
            ProformaListLocators.three_dot_of_io_xpath.format(io_id),
            locator_initialization=True)
        if action != 'None':
            self.click_on_element(
                ProformaListLocators.three_dot_of_io_xpath.format(io_id), locator_initialization=True)
        elif action.lower() == 'edit io':
            self.click_on_three_dot_option(
                ProformaListLocators.edit_io_label_data_qa,
                ProformaListLocators.dropdown_menu_mx_auto_dropdown_menu_left_class)

    def click_on_specific_proforma(self, io_title):
        locator = (By.XPATH,
                   "(//div[text()='" + io_title + "']/..//following-sibling::td[4])[1]")
        self.click_on_element(locator,
                              locator_to_be_appeared=ProformaFormLocators.save_and_generate_proforma_button_data_qa)
