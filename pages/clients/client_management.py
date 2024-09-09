import time

from pages.base_page import BasePage
from locators.clients.client_management_locator import ClientManagementLocator


class DashboardClientManagement(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_client_info_and_save(self, client_name, campaign_name, value):
        self.select_dropdown_value(ClientManagementLocator.select_client_label, dropdown_item=client_name)
        self.select_dropdown_value(ClientManagementLocator.select_campaign_label, dropdown_item=campaign_name)
        time.sleep(1)
        self.set_value_into_element(ClientManagementLocator.margin_input_locator, value)
        self.wait_for_element_to_be_clickable(ClientManagementLocator.save_btn_locator)
        self.click_on_element(ClientManagementLocator.save_btn_locator)
