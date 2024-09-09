from locators.telcodash.telcodash_locators import TelcodashLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.telcodash.telcodash_page import DashboardTelcodas
from utils.page_names_enum import PageNames


def test_smoke_dashboard_telcodash(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    telcodash_page = DashboardTelcodas(driver)

    side_bar_page.navigate_to_page(PageNames.TELCODASH)
    assert 'Country' in telcodash_page.get_element_text(TelcodashLocators.country_filter_data_qa)
