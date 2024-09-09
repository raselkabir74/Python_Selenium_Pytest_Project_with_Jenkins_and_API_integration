import time

from selenium.webdriver.common.keys import Keys

from configurations import generic_modules
from locators.creative.creative_list_locator import CreativeListLocators
from locators.creative.creative_form_locator import CreativeFormLocators
from pages.base_page import BasePage

creative_url = '{}/admin/create/creatives-sets'.format(
    generic_modules.BASE_URL)
creative_url_to_search = '{}/admin/creatives-sets'.format(
    generic_modules.BASE_URL)
creative_information_from_grid = {'general_information': {}}


class DspDashboardCreativeList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_add_creative(self, load_page=False):
        if load_page:
            self.driver.get(creative_url)
        self.click_on_element(CreativeListLocators.btn_create_data_qa)

    def get_success_message(self):
        return self.get_element_text(
            CreativeListLocators.success_message_locator)

    def search_and_action(self, creative_name, action="None",
                          force_reload=False):
        if force_reload:
            self.driver.get(creative_url_to_search)
            self.set_value_into_element(
                CreativeListLocators.creative_search_field_locator,
                creative_name)
        else:
            time.sleep(self.TWO_SEC_DELAY)
            self.set_value_into_element(
                CreativeListLocators.creative_search_field_locator,
                creative_name)
        self.wait_for_presence_of_element(
            CreativeListLocators.creative_search_field_locator).send_keys(
            Keys.ENTER)
        self.wait_for_visibility_of_element(
            CreativeListLocators.three_dot_of_creative_xpath.format(
                creative_name),
            locator_initialization=True)
        if action != 'None':
            self.click_on_element(
                CreativeListLocators.three_dot_of_creative_xpath.format(
                    creative_name),
                locator_initialization=True)
        if action.lower() == 'edit':
            self.click_on_three_dot_option(
                CreativeListLocators.edit_label)
        elif action.lower() == 'navigate':
            self.click_on_element(
                CreativeListLocators.specific_creative_id_locator.format(creative_name), locator_initialization=True)
        elif action.lower() == 'delete':
            self.click_on_three_dot_option(
                CreativeListLocators.delete_label)
            self.click_on_element(
                CreativeListLocators.confirm_button_alert_locator)

    def get_creative_information_from_grid(self, row_number="1",
                                           no_preview=False):
        self.reset_creative_information()
        creative_information_from_grid['general_information'][
            'title'] = self.get_value_from_specific_grid_column(
            CreativeListLocators.creatives_table_wrapper_div_id,
            CreativeListLocators.title_column, a_tag=True,
            row_number=row_number)
        if not no_preview:
            self.wait_for_preview_to_be_updated(
                CreativeListLocators.first_row_image_preview_locator)
            creative_information_from_grid['general_information'][
                'preview'] = str(self.is_image_present(
                CreativeListLocators.first_row_image_preview_locator))
        creative_information_from_grid['general_information'][
            'format'] = self.get_value_from_specific_grid_column(
            CreativeListLocators.creatives_table_wrapper_div_id,
            CreativeListLocators.format_column,
            row_number=row_number)
        creative_information_from_grid['general_information'][
            'dimensions'] = self.get_value_from_specific_grid_column(
            CreativeListLocators.creatives_table_wrapper_div_id,
            CreativeListLocators.dimensions_column,
            row_number=row_number)
        creative_information_from_grid['general_information'][
            'status'] = self.get_value_from_specific_grid_column(
            CreativeListLocators.creatives_table_wrapper_div_id,
            CreativeListLocators.status_column,
            row_number=row_number)
        return creative_information_from_grid

    def wait_for_status_to_be_updated(self, creative_title='',
                                      status='Active',
                                      timeout=15, row_number='1'):
        if creative_title != '':
            self.search_and_action(creative_title)
        end_time = time.time() + timeout
        while self.get_value_from_specific_grid_column(
                CreativeListLocators.creatives_table_wrapper_div_id,
                CreativeListLocators.status_column,
                row_number=row_number) != status:
            self.driver.refresh()
            if creative_title != '':
                self.search_and_action(creative_title)
            if time.time() > end_time:
                break

    def wait_for_creative_count_to_be_updated(self, creative_title='',
                                              count='1',
                                              timeout=15, row_number='1'):
        if creative_title != '':
            self.search_and_action(creative_title)
        end_time = time.time() + timeout
        while self.get_value_from_specific_grid_column(
                CreativeListLocators.creatives_set_table_wrapper_div_id,
                CreativeListLocators.creative_count,
                row_number=row_number) != count:
            self.driver.refresh()
            if creative_title != '':
                self.search_and_action(creative_title)
            if time.time() > end_time:
                break

    def wait_for_preview_to_be_updated(self, preview_img_locator,
                                       creative_title='', timeout=15):
        if creative_title != '':
            self.search_and_action(creative_title)
        end_time = time.time() + timeout
        while self.is_image_present(preview_img_locator) is False:
            self.driver.refresh()
            if creative_title != '':
                self.search_and_action(creative_title)
            if time.time() > end_time:
                break

    @staticmethod
    def reset_creative_information():
        # RESET CAMPAIGN_APPROVE INFORMATION BEFORE GETTING DATA
        global creative_information_from_grid
        creative_information_from_grid = {'general_information': {}}

    def add_creative_into_creative_set(self, creative_data):
        self.search_and_action(creative_data['general_information']['title'], action='navigate')
        self.click_on_element(CreativeListLocators.add_creative_btn_data_qa)
        self.select_dropdown_value(CreativeFormLocators.format_select_data_qa, creative_data[
            'general_information']['format'])
        self.click_on_specific_button(CreativeFormLocators.continue_button_data_qa)
