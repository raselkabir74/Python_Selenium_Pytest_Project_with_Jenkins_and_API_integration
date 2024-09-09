from pages.base_page import BasePage
from locators.user.userlist_locators import UserListLocators
from selenium.webdriver.common.keys import Keys


class DashboardUserListForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_add_user_page(self):
        self.wait_for_element_to_be_invisible(
            UserListLocators.processing_loader_locator,
            max_retries=2)
        self.click_on_element(UserListLocators.add_user_button_data_qa)

    def navigate_to_bulk_user_page(self):
        self.wait_for_element_to_be_invisible(
            UserListLocators.processing_loader_locator,
            max_retries=2)
        self.click_on_element(
            UserListLocators.bulk_user_button_data_qa)

    def get_success_message(self):
        return self.get_element_text(
            UserListLocators.success_message_data_qa)

    def wait_for_loader_to_be_invisible(self):
        self.wait_for_element_to_be_invisible(
            UserListLocators.processing_loader_locator,
            max_retries=2)

    def search_user_and_action(self, search_text, action='None'):
        self.wait_for_element_to_be_invisible(
            UserListLocators.processing_loader_locator,
            max_retries=2)
        self.set_value_into_element(
            UserListLocators.search_box_data_qa,
            search_text)
        self.wait_for_presence_of_element(
            UserListLocators.search_box_data_qa).send_keys(
            Keys.ENTER)
        self.wait_for_element_to_be_invisible(
            UserListLocators.processing_loader_locator,
            max_retries=2)
        if action != 'None':
            self.click_on_element(
                UserListLocators.three_dot_locator)
        if action.lower() == 'delete':
            self.click_on_element(
                UserListLocators.delete_option_locator)
            self.click_on_element(
                UserListLocators.alert_confirm_button_locator)
            self.wait_for_element_to_be_invisible(
                UserListLocators.processing_loader_locator,
                max_retries=2)
        elif action.lower() == 'edit':
            self.click_on_element(
                UserListLocators.edit_option_locator)
