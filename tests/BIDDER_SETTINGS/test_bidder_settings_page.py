from locators.bidder_settings.bidder_settings_locator import BidderSettings
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.bidder_settings.bidder_settings_page import DashboardBidderSettings
from utils.page_names_enum import PageNames


def test_smoke_dashboard_bidder_settings(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    bidder_settings_page = DashboardBidderSettings(driver)

    side_bar_page.navigate_to_page(PageNames.BIDDER_SETTINGS)
    assert 'Country' in bidder_settings_page.get_element_text(BidderSettings.country_th_locator)
