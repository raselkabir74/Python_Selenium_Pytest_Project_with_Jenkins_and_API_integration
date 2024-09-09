import time

from locators.traffic_discovery.traffic_discovery_list_locators import \
    TrafficDiscoveryLocators
from pages.base_page import BasePage


class DashboardTrafficDiscoveryPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def is_traffic_discovery_table_existed(self):
        return self.is_visible(
            TrafficDiscoveryLocators.traffic_discovery_table_locator)

    def is_chart_graph_existed(self):
        return self.is_visible(
            TrafficDiscoveryLocators.chart_line_graph_locator)

    def search_by_country_and_group_by_app_sites(self, country):
        self.select_from_modal_form_using_js_code_without_retry(
            TrafficDiscoveryLocators.select_and_group_by_country_label_locator, option_to_select=country)
        self.check_uncheck_specific_checkbox(TrafficDiscoveryLocators.select_and_group_by_app_sites_label_locator,
                                             do_check=True)
        self.click_on_element(TrafficDiscoveryLocators.traffic_discovery_search_button_locator)
        # Necessary evil to wait for the table to be loaded
        time.sleep(self.ONE_SEC_DELAY)

    def select_list_table_length(self, length='100'):
        self.select_dropdown_value(TrafficDiscoveryLocators.rows_per_page_label, length)

    def grouped_by_column_count(self):
        elements = self.driver.find_elements(*TrafficDiscoveryLocators.traffic_discovery_table_columns_locator)
        return len(elements)

    def verify_app_id_exist_in_table(self, app_id):
        elements = self.get_text_or_value_from_list(
            TrafficDiscoveryLocators.traffic_discovery_table_app_sites_names_locator, split_text=False)
        results = False
        for element in elements:
            if app_id in element:
                results = True
        return results

    def search_and_group_by_country_package_app_sites(self, country, package, app_sites):
        self.select_from_modal_form_using_js_code_without_retry(
            TrafficDiscoveryLocators.select_and_group_by_country_label_locator, option_to_select=country)
        self.check_uncheck_specific_checkbox(
            TrafficDiscoveryLocators.select_and_group_by_country_label_locator, do_check=True)
        self.select_from_modal_form_using_js_code_without_retry(
            TrafficDiscoveryLocators.select_and_group_by_package_label_locator, option_to_select=package)
        self.check_uncheck_specific_checkbox(
            TrafficDiscoveryLocators.select_and_group_by_package_label_locator, do_check=True)
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal_form_using_js_code_without_retry(
            TrafficDiscoveryLocators.select_and_group_by_app_sites_label_locator, option_to_select=app_sites)
        self.check_uncheck_specific_checkbox(
            TrafficDiscoveryLocators.select_and_group_by_app_sites_label_locator, do_check=True)
        self.click_on_element(TrafficDiscoveryLocators.traffic_discovery_search_button_locator)
        # Necessary evil to wait for the table to be loaded
        time.sleep(self.ONE_SEC_DELAY)
