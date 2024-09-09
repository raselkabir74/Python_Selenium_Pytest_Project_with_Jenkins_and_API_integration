from locators.rebate_overview.rebate_overview_locators import RebateOverviewLocators
from pages.rebate_overview.rebate_overview_page import DashboardRebateOverview
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_smoke_finance_rebate_overview(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    rebate_overview_page = DashboardRebateOverview(driver)

    side_bar_page.navigate_to_page(PageNames.REBATE_OVERVIEW)
    assert True is rebate_overview_page.is_element_present(RebateOverviewLocators.company_group_filter_locator)
