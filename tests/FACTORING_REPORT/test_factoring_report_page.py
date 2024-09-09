from locators.factoring_report.factoring_report_locators import FactoringReportLocators
from pages.factoring_report.factoring_report_page import DashboardFactoringReport
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_smoke_factoring_report(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    factoring_report_page = DashboardFactoringReport(driver)

    side_bar_page.navigate_to_page(PageNames.FACTORING_REPORT)
    assert True is factoring_report_page.is_element_present(FactoringReportLocators.company_filter_locator)
    assert True is factoring_report_page.is_element_present(
        FactoringReportLocators.first_factoring_report_table_row_locator)
    assert True is factoring_report_page.is_element_displayed(
        FactoringReportLocators.first_factoring_report_table_row_locator)
