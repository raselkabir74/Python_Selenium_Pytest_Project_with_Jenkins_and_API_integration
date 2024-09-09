from pages.sidebar.sidebar import DashboardSidebarPage
from pages.traffic_discovery.traffic_discovery_list import \
    DashboardTrafficDiscoveryPage
from locators.traffic_discovery.traffic_discovery_list_locators import \
    TrafficDiscoveryLocators
from configurations import generic_modules
from utils.page_names_enum import PageNames


def test_regression_traffic_discovery(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    SidebarPage = DashboardSidebarPage(driver)
    TrafficDiscoveryPage = DashboardTrafficDiscoveryPage(driver)
    SidebarPage.navigate_to_page(PageNames.TRAFFIC_DISCOVERY)
    assert TrafficDiscoveryPage.is_traffic_discovery_table_existed()


def test_regression_traffic_discovery_verify_group_by_and_filtering_for_apps(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    SidebarPage = DashboardSidebarPage(driver)
    TrafficDiscoveryPage = DashboardTrafficDiscoveryPage(driver)

    generic_modules.step_info("[START - RTB-8838] Verify grouping by app/sites works correctly")

    SidebarPage.navigate_to_page(PageNames.TRAFFIC_DISCOVERY)
    TrafficDiscoveryPage.search_by_country_and_group_by_app_sites(country=TrafficDiscoveryLocators.country)
    TrafficDiscoveryPage.select_list_table_length(length='100')
    assert 3 == TrafficDiscoveryPage.grouped_by_column_count(), "3 columns should exist in the table"
    assert TrafficDiscoveryPage.verify_app_id_exist_in_table(TrafficDiscoveryLocators.app_id), \
        "App ID 632064380 (Vinted app) does not exist in the table"


def test_regression_traffic_discovery_verify_multiple_grouping(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    SidebarPage = DashboardSidebarPage(driver)
    TrafficDiscoveryPage = DashboardTrafficDiscoveryPage(driver)
    TrafficDiscoveryPageLocators = TrafficDiscoveryLocators()

    SidebarPage.navigate_to_page(PageNames.TRAFFIC_DISCOVERY)
    TrafficDiscoveryPage.search_and_group_by_country_package_app_sites(
        country=TrafficDiscoveryLocators.country, package=TrafficDiscoveryLocators.package_option,
        app_sites=TrafficDiscoveryLocators.site_name)
    TrafficDiscoveryPage.select_list_table_length(length='100')
    country_column_list = TrafficDiscoveryPage.get_text_or_value_from_list(
        TrafficDiscoveryPageLocators.traffic_discovery_table_country_locator, split_text=False)
    package_column_list = TrafficDiscoveryPage.get_text_or_value_from_list(
        TrafficDiscoveryPageLocators.traffic_discovery_table_packages_names_locator, split_text=False)
    app_sites_column_list = TrafficDiscoveryPage.get_text_or_value_from_list(
        TrafficDiscoveryPageLocators.traffic_discovery_table_app_sites_names_locator, split_text=False)
    assert TrafficDiscoveryLocators.country == TrafficDiscoveryPage.get_selected_options_using_js_code(
        TrafficDiscoveryPageLocators.select_and_group_by_country_label_locator)
    assert "True" is TrafficDiscoveryPage.get_checkbox_status(
        TrafficDiscoveryLocators.select_and_group_by_country_label_locator)
    assert TrafficDiscoveryLocators.package_option == \
        TrafficDiscoveryPage.get_selected_options_using_js_code(
            TrafficDiscoveryPageLocators.select_and_group_by_package_label_locator)
    assert "True" is TrafficDiscoveryPage.get_checkbox_status(
        TrafficDiscoveryLocators.select_and_group_by_package_label_locator)
    assert TrafficDiscoveryLocators.site_name == TrafficDiscoveryPage.get_selected_options_using_js_code(
        TrafficDiscoveryPageLocators.select_and_group_by_app_sites_label_locator)
    assert "True" is TrafficDiscoveryPage.get_checkbox_status(
        TrafficDiscoveryLocators.select_and_group_by_app_sites_label_locator)
    assert 5 == TrafficDiscoveryPage.grouped_by_column_count(), "5 columns should exist in the table"
    for country in country_column_list:
        assert TrafficDiscoveryLocators.country == country, "Country column should contain only Lithuania"
    for package in package_column_list:
        assert TrafficDiscoveryLocators.package_category == package, \
            "Package column should contain only Kids and Family-Oriented Games"
    app_sites_set = set(app_sites_column_list)
    assert len(app_sites_column_list) == len(app_sites_set), "App/Site Name column should not contain duplicates"

    generic_modules.step_info("[END - RTB-8838] Verify grouping by app/sites works correctly")
