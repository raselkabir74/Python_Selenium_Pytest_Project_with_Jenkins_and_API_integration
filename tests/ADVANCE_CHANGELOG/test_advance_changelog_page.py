from locators.advance_changelog.advance_changelog_locators import AdvanceChangelogLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.advance_changelog.advance_changelog_page import DashboardAdvanceChangelog
from utils.page_names_enum import PageNames


def test_smoke_dashboard_advance_changelog(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    advance_changelog_page = DashboardAdvanceChangelog(driver)

    side_bar_page.navigate_to_page(PageNames.ADVANCED_CHANGELOG)
    assert 'Change By' in advance_changelog_page.get_element_text(AdvanceChangelogLocators.change_by_filter_data_qa)
