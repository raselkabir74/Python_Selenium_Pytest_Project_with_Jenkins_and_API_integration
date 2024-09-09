from selenium.webdriver.common.by import By


class SoaReportLocators:
    # [START] data-qa attribute values
    client_account_data_qa = 'client-account-select'
    client_company_data_qa = 'client-company-select'
    io_data_qa = 'io-select'
    eskimi_billing_entity_data_qa = 'eskimi-billing-entity-select'
    sent_data_qa = 'sent-select'
    paid_data_qa = 'paid-select'
    expired_data_qa = 'expired-select'
    io_period_data_qa = 'io-period-select'
    invoice_period_data_qa = 'invoice-period-select'
    credit_invoice_data_qa = 'credit-invoice-select'
    io_signed_data_qa = 'io-signed-select'
    currency_data_qa = 'currency-select'
    filter_count_data_qa = 'filter-toggler'
    filter_count_email_log_data_qa = 'filters-btn'
    export_excel_button_data_qa = 'export-excel-btn'
    export_pdf_button_data_qa = "export-pdf-btn"
    initiate_sending_report_button_data_qa = 'initiate-sending-report-btn'
    soa_report_emails_button_data_qa = 'soa-reeport-email-btn'
    clear_all_button_data_qa = 'clear-all-btn'
    period_data_qa = 'period-input'
    account_name_checkbox_data_qa = 'account-name-check'
    client_company_name_checkbox_data_qa = 'client-company-name-check'
    tax_split_deduction_checkbox_data_qa = 'tax-split-check'
    total_row_for_invoice_amount_data_qa = 'total-invoice-amount-info'
    second_total_row_for_invoice_amount_data_qa = 'total-invoice-amount-footer-info'
    total_row_for_paid_amount_data_qa = 'total-paid-amount-info'
    second_total_row_for_paid_amount_data_qa = 'total-paid-amount-footer-info'
    total_row_for_credit_amount_data_qa = 'total-credit-amount-info'
    second_total_row_for_credit_amount_data_qa = 'total-credit-amount-footer-info'
    total_row_for_deduction_data_qa = 'total-deduction-info'
    second_total_row_for_deduction_data_qa = 'total-deduction-footer-info'
    total_row_for_balance_data_qa = 'total-balance-info'
    second_total_row_for_balance_data_qa = 'total-balance-footer-info'
    account_name_rows_data_qa = (By.XPATH, "//a[contains(@data-qa, 'name')]")
    search_field_data_qa = 'search-input'
    # [END] data-qa attribute values

    # [Start] label
    rows_per_page_label = 'Rows per page '
    sender_label = 'Sender'
    receiver_label = 'Receiver'
    # [End] label

    # [Start] Locators
    save_sending_report_button_locator = (By.XPATH, "//button[@class='btn btn btn-sm btn-primary success']")
    account_name_column_locator = (By.XPATH, "//th[@aria-label='Account name: activate to sort column ascending']")
    client_company_name_column_locator = (By.XPATH,
                                          "//th[@aria-label='Client company name: activate to sort column ascending']")
    invoice_number_column_locator = (By.XPATH, "//a[contains(@data-qa, 'invoice')]")
    currency_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'currncy')]")
    invoice_amount_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'invoice-amount')]")
    paid_amount_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'amount-paid')]")
    credit_amount_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'credit-amount')]")
    deduction_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'deduction')]")
    balance_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'balance')]")
    deduction_column_locator = (By.XPATH, "//th[@aria-label='Deduction']")
    no_data_for_defined_criteria_locator = (By.XPATH, "//td[normalize-space()='No data for defined criteria.']")
    client_company_name_rows_locator = (By.XPATH, "//span[contains(@data-qa, 'client-company-name')]")
    soa_report_email_page_title_locator = (By.XPATH, "//h3[@class='title']")
    sender_filter_field_locator = (By.XPATH,
                                   "//label[normalize-space()='Sender']/..//span[@class='mselect-selection__rendered']")
    receiver_filter_field_locator = (By.XPATH, "//label[normalize-space()='Receiver']/..//span["
                                               "@class='mselect-selection__rendered']")
    soa_report_email_clear_all_button_locator = (By.XPATH, "//a[@class='clear-all-btn float-right']")
    rows_info_locator = (By.ID, 'invoice-soa-email-log-table_info')
    # [End] Locators

    # [Start] Options
    all_option = "All"
    sender_option = "Eskimi - Skaidre"
    # [End] Options

    # [Start] Attribute values
    soa_report_email_table_wrapper_div_id = 'invoice-soa-email-log-table_wrapper'
    # [End] Attribute values
