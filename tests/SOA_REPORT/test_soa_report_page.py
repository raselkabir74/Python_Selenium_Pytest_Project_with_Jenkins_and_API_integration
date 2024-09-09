import json
import os

from configurations import generic_modules
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.io_form_locator import IoFormLocators
from locators.soa_report.soa_report_locators import SoaReportLocators
from pages.io.invoice_form import DspDashboardInvoiceForm
from pages.io.io_form import DspDashboardIoForm
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.soa_report.soa_report import DspDashboardSoaReport
from utils.page_names_enum import PageNames


def test_finance_soa_report_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    soa_report_page = DspDashboardSoaReport(driver)
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    generic_modules.step_info("[START - RTB-7924] Validate filter options are available in the SOA Report page")
    sidebar_navigation.navigate_to_page(PageNames.SOA_REPORT)
    soa_report_page_filter_field_data_qa = (
        SoaReportLocators.client_account_data_qa,
        SoaReportLocators.client_company_data_qa,
        SoaReportLocators.io_data_qa,
        SoaReportLocators.eskimi_billing_entity_data_qa,
        SoaReportLocators.sent_data_qa,
        SoaReportLocators.paid_data_qa,
        SoaReportLocators.io_period_data_qa,
        SoaReportLocators.invoice_period_data_qa,
        SoaReportLocators.credit_invoice_data_qa,
        SoaReportLocators.io_signed_data_qa,
        SoaReportLocators.currency_data_qa)

    for field_data_qa in soa_report_page_filter_field_data_qa:
        assert soa_report_page.is_specific_filter_field_available(
            field_data_qa)
    assert True is soa_report_page.is_element_present(SoaReportLocators.period_data_qa)
    generic_modules.step_info("[END - RTB-7924] Validate filter options are available in the SOA Report page")

    generic_modules.step_info(
        "[START - RTB-7925] Validate that all filter options are working properly to generate report")

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # IO AND INVOICE CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_data_and_save(io_data)
    io_number = "IO " + io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                                  IoFormLocators.insertion_order_info_data_qa)
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    invoice_number = "ELT " + io_form_page.get_text_using_tag_attribute(invoice_form_page.div_tag,
                                                                        invoice_form_page.class_attribute,
                                                                        InvoiceFormLocators.first_invoice_number_class)
    sidebar_navigation.navigate_to_page(PageNames.SOA_REPORT)

    generic_modules.step_info("[START - RTB-7927] Validate that additional columns are displayed correctly when added")
    soa_report_page.click_on_element(SoaReportLocators.account_name_checkbox_data_qa)
    soa_report_page.click_on_element(SoaReportLocators.client_company_name_checkbox_data_qa)
    soa_report_page.click_on_element(SoaReportLocators.tax_split_deduction_checkbox_data_qa)
    assert True is soa_report_page.is_element_present(SoaReportLocators.account_name_column_locator)
    assert True is soa_report_page.is_element_present(SoaReportLocators.client_company_name_column_locator)
    assert True is soa_report_page.is_element_present(SoaReportLocators.deduction_column_locator)
    generic_modules.step_info("[END - RTB-7927] Validate that additional columns are displayed correctly when added")

    # VALIDATE CLIENT ACCOUNT FILTER
    soa_report_page.select_dropdown_value(SoaReportLocators.client_account_data_qa, io_data['client_profile']['client'])
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)

    # VALIDATE CLIENT COMPANY FILTER
    soa_report_page.select_dropdown_value(SoaReportLocators.client_company_data_qa, io_data['client_profile'][
        'client_company'])
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)

    generic_modules.step_info("[START - RTB-7943] Validate that additional columns "
                              "(Account name, Client company name, Tax split (deduction)) are showing proper data")
    assert io_data['client_profile']['client'] == soa_report_page.get_text_or_value_from_list(
        SoaReportLocators.account_name_rows_data_qa, io_data['client_profile']['client'])
    assert io_data['client_profile']['client_company'] == soa_report_page.get_text_or_value_from_list(
        SoaReportLocators.client_company_name_rows_locator, io_data['client_profile']['client_company'])
    generic_modules.step_info("[END - RTB-7943] Validate that additional columns "
                              "(Account name, Client company name, Tax split (deduction)) are showing proper data")

    # VALIDATE IO FILTER
    # It's commented out, because for the new io filter, our method to select value not working.
    # soa_report_page.clear_specific_filter_option_from_soa_report_page(SoaReportLocators.client_company_data_qa)
    # soa_report_page.select_dropdown_value(SoaReportLocators.io_data_qa, io_number)
    # soa_report_page.wait_for_spinner_load()
    # assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
    #     SoaReportLocators.invoice_number_column_locator, invoice_number)
    # soa_report_page.clear_specific_filter_option_from_soa_report_page(SoaReportLocators.io_data_qa)

    # VALIDATE BILLING ENTITY FILTER
    soa_report_page.select_from_modal(io_data['billing_entity']['company_profile'],
                                      SoaReportLocators.eskimi_billing_entity_data_qa)
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.check_uncheck_all_from_from_modal(SoaReportLocators.eskimi_billing_entity_data_qa, check_all=False)

    # VALIDATE SENT FILTER
    soa_report_page.select_from_modal("No", SoaReportLocators.sent_data_qa)
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.check_uncheck_all_from_from_modal(SoaReportLocators.sent_data_qa, check_all=False)

    # VALIDATE PAID FILTER
    soa_report_page.select_from_modal("No", SoaReportLocators.paid_data_qa)
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.check_uncheck_all_from_from_modal(SoaReportLocators.paid_data_qa, check_all=False)

    # VALIDATE IO PERIOD FILTER
    current_month_year = soa_report_page.get_current_date_with_specific_format(
        "%Y-%m")
    soa_report_page.select_from_modal(current_month_year, SoaReportLocators.io_period_data_qa)
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.check_uncheck_all_from_from_modal(SoaReportLocators.io_period_data_qa, check_all=False)

    # VALIDATE INVOICE PERIOD FILTER
    invoice_period = soa_report_page.get_invoice_period()
    soa_report_page.select_from_modal(invoice_period, SoaReportLocators.invoice_period_data_qa)
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.check_uncheck_all_from_from_modal(SoaReportLocators.invoice_period_data_qa, check_all=False)

    # VALIDATE CREDIT INVOICE FILTER
    soa_report_page.select_dropdown_value(SoaReportLocators.credit_invoice_data_qa, "No")
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.clear_specific_filter_option_from_soa_report_page(SoaReportLocators.credit_invoice_data_qa)

    # VALIDATE IO SIGNED FILTER
    soa_report_page.select_dropdown_value(SoaReportLocators.io_signed_data_qa, "No")
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)
    soa_report_page.clear_specific_filter_option_from_soa_report_page(SoaReportLocators.io_signed_data_qa)

    # VALIDATE CURRENCY FILTER
    soa_report_page.select_dropdown_value(SoaReportLocators.currency_data_qa, "USD")
    soa_report_page.wait_for_spinner_load()
    assert invoice_number == soa_report_page.check_if_the_invoice_is_in_the_list(
        SoaReportLocators.invoice_number_column_locator, invoice_number)

    generic_modules.step_info(
        "[END - RTB-7925] Validate that all filter options are working properly to generate report")

    generic_modules.step_info("[START - RTB-7926] Validate Clear all button")
    soa_report_page.click_on_element(SoaReportLocators.clear_all_button_data_qa)
    soa_report_page.wait_for_spinner_load()
    assert soa_report_page.is_visible(SoaReportLocators.no_data_for_defined_criteria_locator)
    assert "0" == soa_report_page.get_attribute_value(SoaReportLocators.filter_count_data_qa,
                                                      attribute_name="data-count")
    generic_modules.step_info("[END - RTB-7926] Validate Clear all button")

    generic_modules.step_info("[START - RTB-7944] Verify that Total row is showing proper amount and currency")
    soa_report_page.click_on_element(SoaReportLocators.account_name_checkbox_data_qa)
    soa_report_page.click_on_element(SoaReportLocators.client_company_name_checkbox_data_qa)
    soa_report_page.click_on_element(SoaReportLocators.tax_split_deduction_checkbox_data_qa)
    soa_report_page.select_dropdown_value(SoaReportLocators.client_account_data_qa, io_data['client_profile']['client'])
    soa_report_page.select_dropdown_value(SoaReportLocators.rows_per_page_label, SoaReportLocators.all_option)
    soa_report_page.wait_for_spinner_load()

    # TOTAL AMOUNT VALIDATION FOR INVOICE AMOUNT COLUMN
    invoice_amount_and_currency_list = soa_report_page.get_amount_and_currency_list_from_specific_columns(
        SoaReportLocators.invoice_amount_rows_locator, SoaReportLocators.currency_rows_locator)
    total_invoice_amount = soa_report_page.get_calculated_total_amount_by_currency(invoice_amount_and_currency_list)
    invoice_amount_from_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.total_row_for_invoice_amount_data_qa)
    invoice_amount_from_second_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.second_total_row_for_invoice_amount_data_qa)

    for currency, amount_str in invoice_amount_from_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_invoice_amount[currency] == amount
        assert set(total_invoice_amount.keys()) == set(invoice_amount_from_total_row.keys())
    for currency, amount_str in invoice_amount_from_second_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_invoice_amount[currency] == amount
        assert set(total_invoice_amount.keys()) == set(invoice_amount_from_total_row.keys())

    # TOTAL AMOUNT VALIDATION FOR PAID AMOUNT COLUMN
    paid_amount_and_currency_list = soa_report_page.get_amount_and_currency_list_from_specific_columns(
        SoaReportLocators.paid_amount_rows_locator, SoaReportLocators.currency_rows_locator)
    total_paid_amount = soa_report_page.get_calculated_total_amount_by_currency(paid_amount_and_currency_list)
    paid_amount_from_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.total_row_for_paid_amount_data_qa)
    paid_amount_from_second_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.second_total_row_for_paid_amount_data_qa)

    for currency, amount_str in paid_amount_from_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_paid_amount[currency] == amount
        assert set(total_paid_amount.keys()) == set(paid_amount_from_total_row.keys())
    for currency, amount_str in paid_amount_from_second_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_paid_amount[currency] == amount
        assert set(total_paid_amount.keys()) == set(paid_amount_from_total_row.keys())

    # TOTAL AMOUNT VALIDATION FOR CREDIT AMOUNT COLUMN
    credit_amount_and_currency_list = soa_report_page.get_amount_and_currency_list_from_specific_columns(
        SoaReportLocators.credit_amount_rows_locator, SoaReportLocators.currency_rows_locator)
    total_credit_amount = soa_report_page.get_calculated_total_amount_by_currency(credit_amount_and_currency_list)
    credit_amount_from_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.total_row_for_credit_amount_data_qa)
    credit_amount_from_second_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.second_total_row_for_credit_amount_data_qa)
    for currency, amount_str in credit_amount_from_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_credit_amount[currency] == amount
        assert set(total_credit_amount.keys()) == set(credit_amount_from_total_row.keys())
    for currency, amount_str in credit_amount_from_second_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_credit_amount[currency] == amount
        assert set(total_credit_amount.keys()) == set(credit_amount_from_total_row.keys())

    # TOTAL AMOUNT VALIDATION FOR DEDUCTION COLUMN
    deduction_amount_and_currency_list = soa_report_page.get_amount_and_currency_list_from_specific_columns(
        SoaReportLocators.deduction_rows_locator, SoaReportLocators.currency_rows_locator)
    total_deduction_amount = soa_report_page.get_calculated_total_amount_by_currency(deduction_amount_and_currency_list)
    deduction_from_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.total_row_for_deduction_data_qa)
    deduction_from_second_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.second_total_row_for_deduction_data_qa)
    for currency, amount_str in deduction_from_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_deduction_amount[currency] == amount
        assert set(total_deduction_amount.keys()) == set(deduction_from_total_row.keys())
    for currency, amount_str in deduction_from_second_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_deduction_amount[currency] == amount
        assert set(total_deduction_amount.keys()) == set(deduction_from_total_row.keys())

    # TOTAL AMOUNT VALIDATION FOR BALANCE COLUMN
    balance_amount_and_currency_list = soa_report_page.get_amount_and_currency_list_from_specific_columns(
        SoaReportLocators.balance_rows_locator, SoaReportLocators.currency_rows_locator)
    total_balance_amount = soa_report_page.get_calculated_total_amount_by_currency(
        balance_amount_and_currency_list)
    balance_from_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.total_row_for_balance_data_qa)
    balance_from_second_total_row = soa_report_page.get_total_row_amount(
        SoaReportLocators.second_total_row_for_balance_data_qa)
    for currency, amount_str in balance_from_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_balance_amount[currency] == amount
        assert set(total_balance_amount.keys()) == set(balance_from_total_row.keys())
    for currency, amount_str in balance_from_second_total_row.items():
        amount = amount_str.strip().replace(',', '')
        assert total_balance_amount[currency] == amount
        assert set(total_balance_amount.keys()) == set(balance_from_total_row.keys())

    generic_modules.step_info("[END - RTB-7944] Verify that Total row is showing proper amount and currency")


def test_finance_soa_report_page_export_excel_pdf(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    soa_report_page = DspDashboardSoaReport(driver)

    download_dir = os.path.join(os.getcwd(), "downloads")

    generic_modules.step_info("[START - RTB-7928] Validate Export excel functionality")

    # EXPORT EXCEL
    sidebar_navigation.navigate_to_page(PageNames.SOA_REPORT)
    soa_report_page.select_dropdown_value(SoaReportLocators.client_company_data_qa, "Webcoupers")
    soa_report_page.select_from_modal("Eskimi NG-NG", SoaReportLocators.eskimi_billing_entity_data_qa)
    soa_report_page.click_on_element(SoaReportLocators.export_excel_button_data_qa)
    soa_report_page.wait_for_spinner_load()
    file_name = "SOA Report.xlsx"
    assert soa_report_page.is_a_specific_file_available_into_a_folder(
        download_dir, file_name)
    actual_size_in_bytes = soa_report_page.get_file_size(download_dir, file_name)
    assert "90000" > str(actual_size_in_bytes) > "69000"
    soa_report_page.delete_file(download_dir, file_name)
    generic_modules.step_info("[END - RTB-7928] Validate Export excel functionality")

    generic_modules.step_info("[START - RTB-7929] Validate Export PDF functionality")

    # EXPORT PDF
    soa_report_page.click_on_element(SoaReportLocators.export_pdf_button_data_qa)
    soa_report_page.wait_for_spinner_load()
    current_date = soa_report_page.get_current_date_with_specific_format(
        "%Y_%m_%d")
    file_name_part = "SOA_Report_Webcoupers_" + current_date
    assert soa_report_page.is_a_file_with_specific_file_name_part_available_into_a_folder(
        download_dir, file_name_part)
    actual_size_in_bytes = soa_report_page.get_file_size(download_dir, file_name_part + "*")
    assert "500000" > str(actual_size_in_bytes) > "440000"
    soa_report_page.delete_file(download_dir, file_name_part + "*")
    generic_modules.step_info("[END - RTB-7929] Validate Export PDF functionality")


def test_finance_soa_report_page_sending_report_emails(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    soa_report_page = DspDashboardSoaReport(driver)

    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)

    generic_modules.step_info(
        "[START - RTB-7930] Validate Initiate sending report functionality and redirection to SOA report emails work")

    # INITIATE SENDING REPORT
    sidebar_navigation.navigate_to_page(PageNames.SOA_REPORT)
    soa_report_page.select_dropdown_value(SoaReportLocators.client_company_data_qa,
                                          io_data['client_profile']['client_company'])
    soa_report_page.select_from_modal(io_data['billing_entity']['company_profile'],
                                      SoaReportLocators.eskimi_billing_entity_data_qa)
    soa_report_page.wait_for_spinner_load()
    soa_report_page.click_on_element(SoaReportLocators.initiate_sending_report_button_data_qa)
    soa_report_page.click_on_element(SoaReportLocators.save_sending_report_button_locator)
    soa_report_page.wait_alert_is_present()
    alert_text = soa_report_page.get_alert_text()
    soa_report_page.accept_alert()
    assert "Initiate SOA report sending successfully" == alert_text

    # VALIDATE SOA REPORT EMAILS BUTTON
    soa_report_page.click_on_element(SoaReportLocators.soa_report_emails_button_data_qa)
    assert "eskimi.com/admin/invoicesEmails/soaEmails" in driver.current_url
    assert True is soa_report_page.is_element_present(SoaReportLocators.soa_report_email_page_title_locator)
    generic_modules.step_info(
        "[END - RTB-7930] Validate Initiate sending report functionality and redirection to SOA report emails work")

    generic_modules.step_info("[START - RTB-7932] Validate SOA Report Emails page works")

    # VALIDATE FILTERS OPTIONS
    soa_report_emails_page_filter_field_labels = (SoaReportLocators.sender_label, SoaReportLocators.receiver_label)
    for field_label in soa_report_emails_page_filter_field_labels:
        assert soa_report_page.is_specific_filter_field_available(
            field_label)

    # VALIDATE SENDER FILTER
    rows_info = soa_report_page.get_element_text(SoaReportLocators.rows_info_locator)
    soa_report_page.select_from_modal(SoaReportLocators.sender_option, SoaReportLocators.sender_label)
    assert SoaReportLocators.sender_option == soa_report_page.get_value_from_specific_grid_column(
        SoaReportLocators.soa_report_email_table_wrapper_div_id, SoaReportLocators.sender_label)

    # VALIDATE RECEIVER FILTER
    soa_report_page.check_uncheck_all_from_from_modal(SoaReportLocators.sender_label, check_all=False)
    soa_report_page.select_from_modal("Test Automation Company", SoaReportLocators.receiver_label)
    assert "Test Automation Company" == soa_report_page.get_value_from_specific_grid_column(
        SoaReportLocators.soa_report_email_table_wrapper_div_id, SoaReportLocators.receiver_label)

    # VALIDATE CLEAR ALL BUTTON
    soa_report_page.click_on_element(SoaReportLocators.soa_report_email_clear_all_button_locator)
    assert "Select any" == soa_report_page.get_element_text(SoaReportLocators.sender_filter_field_locator)
    assert "Select any" == soa_report_page.get_element_text(SoaReportLocators.receiver_filter_field_locator)
    assert rows_info == soa_report_page.get_element_text(SoaReportLocators.rows_info_locator)
    assert "0" == soa_report_page.get_attribute_value(SoaReportLocators.filter_count_email_log_data_qa,
                                                      attribute_name="data-count")
    # VALIDATE SEARCH FIELD
    soa_report_page.set_value_into_element(SoaReportLocators.search_field_data_qa, SoaReportLocators.sender_option)
    assert SoaReportLocators.sender_option == soa_report_page.get_value_from_specific_grid_column(
        SoaReportLocators.soa_report_email_table_wrapper_div_id, SoaReportLocators.sender_label)
    soa_report_page.set_value_into_element(SoaReportLocators.search_field_data_qa,
                                           "Test Automation Company")
    assert "Test Automation Company" == soa_report_page.get_value_from_specific_grid_column(
        SoaReportLocators.soa_report_email_table_wrapper_div_id, SoaReportLocators.receiver_label)
    generic_modules.step_info("[END - RTB-7932] Validate SOA Report Emails page works")
