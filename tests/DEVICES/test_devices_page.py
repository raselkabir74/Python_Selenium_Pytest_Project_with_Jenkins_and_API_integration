from locators.devices.devices_locators import DevicesLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.devieces.devices_page import DashboardDevices
from utils.page_names_enum import PageNames


def test_smoke_dashboard_devices(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    devices_page = DashboardDevices(driver)

    side_bar_page.navigate_to_page(PageNames.DEVICES)
    assert 'Brands' in devices_page.get_element_text(DevicesLocators.brand_label_data_qa)
