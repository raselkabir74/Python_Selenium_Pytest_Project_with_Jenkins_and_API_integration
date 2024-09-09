import time
import json

from pages.report.report_page import DashboardReportPage
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.report import ReportUtils as ReportUtil
from configurations import generic_modules
from utils.page_names_enum import PageNames
from locators.report.report_page_locator import ReportPageLocators
from utils.compare import CompareUtils as CompareUtil


def test_regression_report(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    report_page = DashboardReportPage(driver)
    navbar_page = DashboardNavbar(driver)
    sidebar_page = DashboardSidebarPage(driver)
    expected_widget_id_list = (
        '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 15, 16, 31, 32, 33, 34, 35, 40, 41, 42, 43, 44, 45, 46, 47, '
        '48, 49, 50, 51, 52, 53, 54, 56, 57, 62, 68, 71, 75]')
    pulled_widget_ids_from_db = ReportUtil.pull_widget_id_from_db(db_connection)
    navbar_page.impersonate_user("Eskimi - Arunas B.")
    sidebar_page.navigate_to_page(PageNames.REPORTS)
    report_page.generate_report()
    print("expected widget id :",
          generic_modules.ordered(expected_widget_id_list))
    print("pulled widget id db:",
          generic_modules.ordered(pulled_widget_ids_from_db))
    assert expected_widget_id_list == pulled_widget_ids_from_db
    # These assertions failed on stage and other named env
    # registered a bug https://eskimidev.atlassian.net/browse/RTB-8201
    if "qa-testing" in config['credential']['url']:
        assert "The report in Excel will be downloaded soon. You will receive the report in an email if you leave the page." \
            "" \
            "" in report_page.download_report(
            report_type='Excel')
        time.sleep(report_page.TWO_SEC_DELAY)
        assert "The report in PDF will be downloaded soon. You will receive the report in an email if you leave the page." \
                in report_page.download_report(
                report_type='PDF')
        time.sleep(report_page.TWO_SEC_DELAY)
        assert "The report in PDF with charts will be downloaded soon. You will receive the report in an email if you " \
                "leave the page." in report_page.download_report(
                report_type='PDF with chart')

def test_regression_report_filtering_and_data_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    report_page = DashboardReportPage(driver)
    navbar_page = DashboardNavbar(driver)
    sidebar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-9463] Verify campaign report filtering and data")

    with open('assets/report/campaign_report_data.json') as json_file:
        campaign_data = json.load(json_file)

    navbar_page.impersonate_user(campaign_data['campaign_info']['client_name'])
    sidebar_page.navigate_to_page(PageNames.REPORTS)
    # CLIENT VIEW AND SPENT BASED ON COST
    report_page.generate_specific_report(campaign_data['campaign_info']['campaign_name'],
                                         campaign_data['campaign_info']['campaign_id'],
                                         ReportPageLocators.client_view, ReportPageLocators.spent_based_on_cost)
    #FILTER VERIFICATION
    assert campaign_data['campaign_info']['campaign_name'] in report_page.get_selected_options_using_js_code(
          ReportPageLocators.campaign_select_data_qa)
    assert ReportPageLocators.client_view == report_page.get_selected_options_using_js_code(
          ReportPageLocators.report_view_select_data_qa)
    assert ReportPageLocators.spent_based_on_cost == report_page.get_selected_options_using_js_code(
          ReportPageLocators.spent_select_data_qa)
    #DATA VERIFICATION
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.client_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
        campaign_data["client_view"]["spent_based_on_cost"])
    # CLIENT VIEW AND SPENT BASED ON REVENUE
    report_page.update_spent_option(ReportPageLocators.spent_based_on_revenue)
    assert ReportPageLocators.spent_based_on_revenue == report_page.get_selected_options_using_js_code(
          ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.client_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
		campaign_data["client_view"]["spent_based_on_revenue"])
    # CLIENT VIEW AND SPENT BASED ON REVENUE WITH MARGIN
    report_page.update_spent_option(ReportPageLocators.spent_based_on_revenue_with_margin)
    assert ReportPageLocators.spent_based_on_revenue_with_margin == report_page.get_selected_options_using_js_code(
		  ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.client_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
		pulled_campaign_report_data_gui,
        campaign_data["client_view"]["spent_based_on_revenue_with_margin"])
    # CLIENT VIEW AND SPENT BASED ON REVENUE WITH AGENCY SHARE
    report_page.update_spent_option(ReportPageLocators.spent_based_on_revenue_with_agency_share)
    assert ReportPageLocators.spent_based_on_revenue_with_agency_share == \
        report_page.get_selected_options_using_js_code(ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.client_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
        campaign_data["client_view"]["spent_based_on_revenue_with_agency_share"])
    # ADMIN VIEW AND SPENT BASED ON COST
    report_page.update_view_mode(ReportPageLocators.admin_view)
    report_page.update_spent_option(ReportPageLocators.spent_based_on_cost)
    assert ReportPageLocators.admin_view == report_page.get_selected_options_using_js_code(
        ReportPageLocators.report_view_select_data_qa)
    assert ReportPageLocators.spent_based_on_cost == report_page.get_selected_options_using_js_code(
        ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.admin_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
        campaign_data["admin_view"]["spent_based_on_cost"])
    # ADMIN VIEW AND SPENT BASED ON REVENUE
    report_page.update_spent_option(ReportPageLocators.spent_based_on_revenue)
    assert ReportPageLocators.spent_based_on_revenue == report_page.get_selected_options_using_js_code(
        ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.admin_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
        campaign_data["admin_view"]["spent_based_on_revenue"])
    # ADMIN VIEW AND SPENT BASED ON REVENUE WITH MARGIN
    report_page.update_spent_option(ReportPageLocators.spent_based_on_revenue_with_margin)
    assert ReportPageLocators.spent_based_on_revenue_with_margin == report_page.get_selected_options_using_js_code(
        ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.admin_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
        campaign_data["admin_view"]["spent_based_on_revenue_with_margin"])
    # ADMIN VIEW AND SPENT BASED ON REVENUE WITH AGENCY SHARE
    report_page.update_spent_option(ReportPageLocators.spent_based_on_revenue_with_agency_share)
    assert ReportPageLocators.spent_based_on_revenue_with_agency_share == \
        report_page.get_selected_options_using_js_code(ReportPageLocators.spent_select_data_qa)
    pulled_campaign_report_data_gui = report_page.get_report_budget_related_metrics_data(
        view_mode=ReportPageLocators.admin_view)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_report_data_gui,
        campaign_data["admin_view"]["spent_based_on_revenue_with_agency_share"])

    