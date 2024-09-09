from selenium.webdriver.common.by import By

from locators.package.package_list_locator import PackageListLocators
from pages.base_page import BasePage


class DashboardPackagesList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_add_package(self):
        self.click_on_element(
            PackageListLocators.add_package_button_locator_data_qa)

    def get_success_message(self):
        self.wait_for_visibility_of_element(
            PackageListLocators.success_message_locator)
        return self.get_element_text(
            PackageListLocators.success_message_locator)

    def edit_package(self, package_name):
        self.set_value_into_element(
            PackageListLocators.search_box_locator,
            package_name)
        self.click_on_element(
            PackageListLocators.package_checkbox_xpath.format(
                package_name),
            locator_initialization=True)
        self.click_on_element(PackageListLocators.edit_link_locator)

    def delete_package(self, package_name):
        self.set_value_into_element(
            PackageListLocators.search_box_locator,
            package_name)
        self.click_on_element(
            PackageListLocators.package_checkbox_xpath.format(
                package_name),
            locator_initialization=True)
        self.click_on_element(PackageListLocators.delete_link_locator)
        self.click_on_element(
            PackageListLocators.alert_confirm_button_locator)

    def click_on_checkboxes(self, locator):
        checkboxes = self.driver.find_elements(By.XPATH, locator)

        if len(checkboxes) >= 3:
            checkboxes[1].click()
            checkboxes[2].click()
