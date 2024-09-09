from locators.finance_report.finance_report_locators import FinanceReportLocators
from pages.finance_report.finance_report_page import DashboardFinanceReport
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_smoke_finance_report(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    finance_report_page = DashboardFinanceReport(driver)

    side_bar_page.navigate_to_page(PageNames.FINANCE_REPORT)
    finance_report_page.wait_for_spinner_load()
    assert True is finance_report_page.is_element_present(FinanceReportLocators.client_account_filter_data_qa)
