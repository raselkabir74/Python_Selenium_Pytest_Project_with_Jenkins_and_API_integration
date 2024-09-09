import os
import time

from locators.sites_categoires.site_cetagories_locators import SiteCategoriesLocators
from pages.base_page import BasePage


class DashboardSiteCategories(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def search_and_action(self, category, category_id, action="None"):
        self.set_value_into_element(SiteCategoriesLocators.category_search_field_locator, category)
        self.wait_for_visibility_of_element(SiteCategoriesLocators.three_dot_of_category_locator.format(
            category_id), locator_initialization=True)
        if action != 'None':
            self.click_on_element(SiteCategoriesLocators.three_dot_of_category_locator.format(category_id),
                                  locator_initialization=True)
        if action.lower() == 'edit':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_element_execute_script(SiteCategoriesLocators.category_edit_locator)
        elif action.lower() == 'delete':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_element_execute_script(SiteCategoriesLocators.category_delete_locator)
            self.click_on_element(SiteCategoriesLocators.confirm_delete_btn_locator)

    def create_new_app_site_category(self, sites_categories_data):
        self.click_on_element(SiteCategoriesLocators.new_app_sites_btn)
        self.set_value_into_element(SiteCategoriesLocators.title_input_locator,
                                    sites_categories_data['sites_categories_data']['category_name'])
        self.set_value_into_specific_input_field(
            SiteCategoriesLocators.csv_upload_label, os.path.join(
                os.getcwd(), sites_categories_data['sites_categories_data']['csv_upload']))
        self.click_on_element(SiteCategoriesLocators.save_btn_locator)
