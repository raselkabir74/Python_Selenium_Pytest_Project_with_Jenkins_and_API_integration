from selenium.webdriver.common.by import By


class InvoiceFormLocators:
    # [Start] data-qa attribute values
    save_and_generate_invoice_button_data_qa = "save-and-generate-invoice-btn"
    # [START] data-qa attribute values

    # [Start] locators
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    back_to_list_locator = (
        By.XPATH, "//a[normalize-space()='BACK TO LIST']")
    invoice_object_dropdown_selected_item_locator = (
        By.XPATH, "//span[contains(@id, 'select2-invoice_object')]")
    payment_details_section_locator = (
        By.XPATH,
        "//span[normalize-space()='Payment details' and @class='tab2-selection__rendered']")
    discount_field_locator = (By.ID, "discount-percentage")
    balance_field_locator = (
        By.XPATH,
        "//div[@id='form-step-box-i-6']//tbody[2]//tr[4]//td[2]")
    balance_field_2_locator = (
        By.XPATH,
        "//div[@id='form-step-box-i-6']//tbody[2]//tr[5]//td[2]")
    status_locator = (By.XPATH, "//p[@class='form-status-paid']")
    totals_and_payments_group_locator = (
        By.XPATH, "//a[normalize-space()='Totals & payments']")
    billing_information_group_locator = (
        By.XPATH, "//a[normalize-space()='Billing information']")
    buttons_group_locator = (By.XPATH, "//a[normalize-space()='Buttons']")
    media_budget_plus_button_locator = (
        By.XPATH, "//span[@class='custom-button add']/i")
    channel_dropdown_locator = (
        By.XPATH,
        "//label[normalize-space()='Channel / Service']/..//span[@class='select2-selection__rendered']")
    channel_second_dropdown_locator = (
        By.XPATH,
        "(//label[normalize-space()='Channel / Service']/..//span[@class='select2-selection__rendered'])[2]")
    channel_text_field_locator = (
        By.XPATH, "//input[@class='select2-search__field']")
    send_invoice_button_locator = (
        By.XPATH, "//a[normalize-space()='Send invoice']")
    paid_amount_field_locator = (By.ID, "paid-amount")
    add_payment_locator = (
        By.XPATH, "//a[normalize-space()='Add payment']")
    save_add_payment_button_locator = (By.XPATH, "//button[text()='Save']")
    amount_paid_locator = (By.XPATH, "//input[@id='paid-amount']")
    media_budget_io_number_locator = (By.XPATH, "//span[text()='[2]']//..//span[@class='media-budget-io-number']")
    second_media_budget_table_locator = (By.ID, "tr_serial2_id")
    date_field_locator = (By.ID, "date-picker-field-0")
    created_by_info_locator = (By.XPATH, "//li[contains(text(), 'Created by: ')]")
    last_updated_by_info_locator = (By.XPATH, "//li[contains(text(), 'Last updated by: ')]")
    created_info_locator = (By.XPATH, "//li[contains(text(), 'Created: ')]")
    last_updated_info_locator = (By.XPATH, "//li[contains(text(), 'Last updated: ')]")
    invoice_title_field_locator = (By.XPATH, "//label[contains(text(), 'Invoice title')]/..//input")
    invoice_page_title_locator = (By.ID, "page-title")
    media_budgets_locator = "(//*[contains(@data-qa, 'media-budget-input-')])[{}]"
    period_locator = (By.XPATH, "//*[contains(@data-qa, 'period-input-')]")
    period_locators = "(//*[contains(@data-qa, 'period-input-')])[{}]"
    media_budget_locators = "(//*[contains(@data-qa, 'media-budget-input-')])[{}]"
    media_budget_remove_locators = "(//*[contains(@data-qa, 'media-budget-remove-icon-')])[{}]"
    media_budgets_expand_icon_statues_locator = (By.XPATH, "//*[contains(@data-qa, 'media-budget-arrow-icon-')]/..")
    media_budgets_expand_icon_status_locator = "(//*[contains(@data-qa, 'media-budget-arrow-icon-')]/..)[{}]"
    media_budgets_expand_icon_locator = "(//*[contains(@data-qa, 'media-budget-arrow-icon-')]//b)[{}]"
    media_budgets_info_locator = (By.XPATH, "//*[contains(@data-qa, 'media-budget-info-')]")
    delete_button_locator = (By.XPATH, "//a[contains(text(), 'Delete')]")
    media_budget_first_plus_button_locator = (By.XPATH, "(//*[contains(@data-qa, 'media-budget-add-icon')])[1]")
    manual_invoicing_reason_locator = (By.XPATH, "//label[contains(., 'Manual invoicing reason')]/..//select")
    # [End] locators

    # [Start] label names
    invoice_title_label = "Invoice title"
    date_label = "Date"
    campaign_label = "Campaign"
    client_label = "Client"
    sales_manager_label = "Sales manager"
    country_label = "Country"
    campaign_type_label = "Campaign type"
    clicks_label = "Clicks"
    channel_class = "channel"
    cpm_rate_class = "cpm_rate"
    impressions_class = "impressions"
    notes_label = "Notes (PDF)"
    currency_label = "Currency"
    vat_label = "VAT"
    delete_label = "Delete"
    email_label = "Email"
    contact_label = "Contact"
    use_notice_text_on_invoice_label = "Use notice text on invoice"
    currency_rate_label = "Currency rate"
    payment_term_days_label = "Payment term (days)"
    invoice_object_label = "Invoice object"
    manual_invoicing_reason_label = "Manual invoicing reason"
    amount_paid_label = "Amount paid"
    paid_amount_label = "Paid amount"
    tax_label = "Tax"
    discount_label = "Discount"
    vat_2_label = "Vat"
    base_amount_label = "Base amount"
    total_amount_label = "Total amount"
    bank_charges_2_label = "Bank charges"
    total_label = "Total"
    credit_label = "Credit"
    select_io_label = "Select IO"
    io_execution_comment_label = "IO-campaign execution comment (internal)"
    tr_serial1_id = "tr-serial1"
    tr_serial2_id = "tr-serial2"
    total_currency_class = "total_currency"
    # [End] label names

    # [Start] Button names
    credit_note_button = "Add credit note"
    add_payment_button = "Add payment"
    save_button = "Save"
    # [End] Button names

    # [Start] Attribute values
    select2_client_container_id = "select2-client-container"
    select2_company_profile_container_id = "select2-company_profile-container"
    select2_sales_manager_container_id = "select2-sales_manager-container"
    select2_company_id_container_id = "select2-company_id-container"
    form_control_media_budget_class = "form-control media-budget"
    first_total_media_budget_class = "span8 first total-media-budget"
    select2_currency_container_id = "select2-currency-container"
    select2_io_execution_comment_id_container_id = "select2-io_execution_comment_id-container"
    country_row_class = "country_row"
    campaign_type_class = "campaign_type"
    discount_name = "discount"
    form_step_box_i_6_div_id = "form-step-box-i-6"
    paid_vat_id = "paid-vat"
    paid_charges_id = "paid-charges"
    paid_taxes_id = "paid-taxes"
    paid_rebate_id = "paid-rebate"
    media_budget_actual_amount_locator = \
        "(//label[contains(., 'Media budget')]/..//span[@class='media-budget-io-amount'])[{}]"
    media_budget_field_locator = \
        "(//label[@class='media-budget-label']/..//input[contains(@name, 'invoice_media_budgets')])[{}]"
    first_invoice_number_class = "first invoice-number"
    io_number_id = "io-number"
    media_budget_io_number_class = "media-budget-io-number"
    media_budget_arrow_xpath = "(//span[@class='media-selection__arrow']/b)[{}]"
    media_budget_remove_button_xpath = "(//span[@class='custom-button remove']/i)[{}]"
    yes_button_locator = "//button[text()='Yes']"
    total_media_budget_info_data_qa = "total-media-budget-info"
    country_row_info_data_qa = "country-row-info"
    campaign_type_info_data_qa = "campaign-type-info"
    media_budget_info_data_qa = "total-currency-info"
    country_select_data_qa = "country-select-"
    user_wise_media_budget_xpath = "//span[@title='{}']/../../../../..//div[@class='form-group']//div[" \
                                   "@class='part']//input"
    media_budget_amount_xpath = "//span[@class='media-budget-io-number' and text()='{}']/following-sibling::span"
    invoice_title_input_data_qa = "invoice-title-input"
    comment_input_data_qa = "comment-textarea"
    # [End] Attribute values
