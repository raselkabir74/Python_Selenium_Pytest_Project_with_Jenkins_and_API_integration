from selenium.webdriver.common.keys import Keys
from locators.audience.audience_list_locator import AudienceListLocators
from pages.base_page import BasePage
from configurations import generic_modules

audience_url = '{}/admin/audiences/create'.format(
    generic_modules.BASE_URL)
global_audience_url = '{}/admin/audiencesShared/create'.format(
    generic_modules.BASE_URL)


class DspDashboardAudienceList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_add_audience(self, load_page=False):
        if load_page:
            self.driver.get(audience_url)
        self.click_on_element(
            AudienceListLocators.add_audience_button_locator)

    def get_success_message(self):
        self.wait_for_presence_of_element(
            AudienceListLocators.success_message_locator)
        self.wait_for_visibility_of_element(
            AudienceListLocators.success_message_locator)
        return self.get_element_text(
            AudienceListLocators.success_message_locator)

    def search_and_action(self, audience_name, action="None",
                          force_reload=False):
        if force_reload:
            self.driver.get(audience_url)
            self.set_value_into_element(
                AudienceListLocators.audience_search_field_locator,
                audience_name)
        else:
            self.set_value_into_element(
                AudienceListLocators.audience_search_field_locator,
                audience_name)
        self.wait_for_presence_of_element(
            AudienceListLocators.audience_search_field_locator).send_keys(
            Keys.ENTER)
        self.wait_for_visibility_of_element(
            AudienceListLocators.three_dot_of_audience_xpath.format(
                audience_name),
            locator_initialization=True)
        if action != 'None':
            self.click_on_element(
                AudienceListLocators.three_dot_of_audience_xpath.format(
                    audience_name),
                locator_initialization=True)
        if action.lower() == 'edit':
            self.click_on_three_dot_option(
                AudienceListLocators.edit_data_qa)
        elif action.lower() == 'delete':
            self.click_on_three_dot_option(
                AudienceListLocators.delete_data_qa)
            self.click_on_element(
                AudienceListLocators.confirm_button_alert_locator)

    def search_and_action_global_audience(self, audience_name,
                                          action="None",
                                          force_reload=False, tab_id='1'):
        if force_reload:
            self.driver.get(global_audience_url)
            self.set_value_into_element(
                AudienceListLocators.audience_search_field_locator,
                audience_name)
        else:
            self.set_value_into_element(
                AudienceListLocators.audience_search_field_locator,
                audience_name)
        self.wait_for_presence_of_element(
            AudienceListLocators.audience_search_field_locator).send_keys(
            Keys.ENTER)
        if action != 'None':
            self.click_on_element(
                AudienceListLocators.checkbox_audience_xpath.format(
                    audience_name),
                locator_initialization=True)
        if action.lower() == 'edit':
            self.click_on_element(
                AudienceListLocators.edit_link_xpath.format(
                    tab_id),
                locator_initialization=True)
        elif action.lower() == 'delete':
            self.click_on_element(
                AudienceListLocators.delete_link_xpath.format(
                    tab_id),
                locator_initialization=True)
            self.click_on_element(
                AudienceListLocators.confirm_button_alert_locator)
