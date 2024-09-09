from locators.income_report.income_report_locators import IncomeReportLocators
from pages.income_report.income_report_page import DashboardIncomeReport
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_smoke_income_report_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    income_report_page = DashboardIncomeReport(driver)

    side_bar_page.navigate_to_page(PageNames.INCOME_REPORT)
    assert True is income_report_page.is_element_present(IncomeReportLocators.billing_entity_filter_data_qa)
    assert True is income_report_page.is_element_present(IncomeReportLocators.first_income_report_table_row_locator)
    assert True is income_report_page.is_element_displayed(IncomeReportLocators.first_income_report_table_row_locator)
    income_report_page.click_on_element(IncomeReportLocators.three_dots_action_data_qa,
                                        locator_to_be_appeared=IncomeReportLocators.add_transaction_option_data_qa)
    income_report_page.click_on_element(IncomeReportLocators.add_transaction_option_data_qa,
                                        locator_to_be_appeared=IncomeReportLocators.bank_receive_statement_country_th_data_qa)
    assert True is income_report_page.is_element_displayed(
        IncomeReportLocators.bank_receive_statement_country_th_data_qa)
    income_report_page.click_on_element(IncomeReportLocators.bank_receive_statement_history_data_qa)
    assert True is income_report_page.is_element_displayed(IncomeReportLocators.history_transaction_date_th_data_qa)
