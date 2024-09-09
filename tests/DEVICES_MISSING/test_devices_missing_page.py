from locators.devices_missing.devices_missing_locators import DevicesMissingLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.devices_missing.devices_missing_page import DashboardDevicesMissing
from utils.page_names_enum import PageNames


def test_smoke_dashboard_devices_missing(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    devices_missing_page = DashboardDevicesMissing(driver)

    side_bar_page.navigate_to_page(PageNames.DEVICES_MISSING)
    assert 'Filter' in devices_missing_page.get_element_text(DevicesMissingLocators.filter_label_data_qa)
