from locators.platform_stats.platform_stats_locator import PlatformStatsLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.platform_stats.platform_stats_page import DashboardPlatformStats
from utils.page_names_enum import PageNames


def test_smoke_dashboard_platform_stats(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    platform_stats_page = DashboardPlatformStats(driver)

    side_bar_page.navigate_to_page(PageNames.PLATFORMS_STATS)
    assert 'Platform' in platform_stats_page.get_element_text(PlatformStatsLocators.platform_label_data_qa)

