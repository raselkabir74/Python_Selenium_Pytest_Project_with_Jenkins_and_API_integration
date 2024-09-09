from locators.partner_report.partner_report_locators import PartnerReportLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.partner_report.partner_report_page import DashboardPartnerReport
from utils.page_names_enum import PageNames


def test_smoke_dashboard_partner_report(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    partner_report_page = DashboardPartnerReport(driver)

    side_bar_page.navigate_to_page(PageNames.PARTNER_REPORT)
    assert 'Account' in partner_report_page.get_element_text(PartnerReportLocators.account_filter_data_qa)

