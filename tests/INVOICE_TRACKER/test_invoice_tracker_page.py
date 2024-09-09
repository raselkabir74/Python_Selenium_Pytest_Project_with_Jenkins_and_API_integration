from locators.invoice_tracker.invoice_tracker_locators import InvoiceTrackerLocators
from pages.invoice_tracker.invoice_tracker_page import DashboardInvoiceTracker
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_smoke_finance_invoice_tracker(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    invoice_tracker_page = DashboardInvoiceTracker(driver)

    side_bar_page.navigate_to_page(PageNames.INVOICE_TRACKER)
    invoice_tracker_page.wait_for_spinner_load(spinner_locator=InvoiceTrackerLocators.overlay_loading_locator)
    country = invoice_tracker_page.get_element_text(InvoiceTrackerLocators.country_row_data_qa)
    assert country, "Country cell is empty"
    invoice_tracker_page.click_on_element(InvoiceTrackerLocators.three_dots_action_data_qa,
                                          locator_to_be_appeared=InvoiceTrackerLocators.add_payment_option_data_qa)
    invoice_tracker_page.click_on_element(InvoiceTrackerLocators.add_payment_option_data_qa,
                                          locator_to_be_appeared=InvoiceTrackerLocators.payment_modal_locator)
    assert True is invoice_tracker_page.is_element_present(InvoiceTrackerLocators.amount_paid_input_locator)


def test_smoke_finance_invoice_tracker_payments_log(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    invoice_tracker_page = DashboardInvoiceTracker(driver)

    side_bar_page.navigate_to_page(PageNames.INVOICE_TRACKER)
    invoice_tracker_page.wait_for_spinner_load(spinner_locator=InvoiceTrackerLocators.overlay_loading_locator)
    invoice_tracker_page.click_on_element(InvoiceTrackerLocators.invoice_tracker_logs_data_qa,
                                          locator_to_be_appeared=InvoiceTrackerLocators.payment_action_data_qa)
    invoice_tracker_page.click_on_element(InvoiceTrackerLocators.payment_action_data_qa,
                                          locator_to_be_appeared=InvoiceTrackerLocators.invoice_tracker_filter_data_qa)
    assert True is invoice_tracker_page.is_element_present(InvoiceTrackerLocators.invoice_tracker_filter_data_qa)
    assert True is invoice_tracker_page.is_element_present(InvoiceTrackerLocators.first_payments_log_table_row_locator)
    assert True is invoice_tracker_page.is_element_displayed(
        InvoiceTrackerLocators.first_payments_log_table_row_locator)
