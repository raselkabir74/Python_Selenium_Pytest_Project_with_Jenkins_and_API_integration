from locators.changelog.changelog_locators import ChangelogLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.changelog.changelog_page import DashboardChangelog
from utils.page_names_enum import PageNames


def test_smoke_dashboard_changelog(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    changelog_page = DashboardChangelog(driver)

    side_bar_page.navigate_to_page(PageNames.CHANGELOG)
    assert 'Account' in changelog_page.get_element_text(ChangelogLocators.account_filter_data_qa)
    assert 'Item ID' in changelog_page.get_element_text(ChangelogLocators.item_id_data_qa)

