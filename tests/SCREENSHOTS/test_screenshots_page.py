from locators.screenshots.screenshots_locators import ScreenshotsLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.screenshots.screenshots_page import DashboardScreenshots
from utils.page_names_enum import PageNames


def test_smoke_dashboard_screenshots(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    screenshots_page = DashboardScreenshots(driver)

    side_bar_page.navigate_to_page(PageNames.SCREENSHOTS)
    assert 'Filter' in screenshots_page.get_element_text(ScreenshotsLocators.filter_data_qa)

