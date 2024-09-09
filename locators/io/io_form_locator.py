from selenium.webdriver.common.by import By


class IoFormLocators:
    # [Start] locators
    media_budgets_input_locator = (By.XPATH, "//*[contains(@data-qa, 'media-budget-input-')]")
    invoice_locator = (By.XPATH, "//*[@data-qa='invoices-info']//a")
    back_to_list_locator = (
        By.XPATH, "//a[normalize-space()='BACK TO LIST']")
    selected_date_locator = (
        By.XPATH,
        "//div[@class='datepickerContainer']//td[contains(@class, 'datepickerSelected')]")
    seven_days_option_locator = (
        By.XPATH, "(//a[normalize-space()='7 Days,'])[1]")
    second_fourteen_days_option_locator = (
        By.XPATH, "(//a[normalize-space()='14 Days,'])[2]")
    second_yesterday_option_locator = (
        By.XPATH, "(//a[normalize-space()='Yesterday,'])[2]")
    second_media_budget_table_locator = (By.ID, "tr_serial2_id")
    channel_dropdown_locator = (
        By.XPATH, "//span[@class='select2-selection__placeholder']")
    channel_dropdown_item_locator = (
        By.XPATH,
        "//label[normalize-space()='Channel / Service']/..//span[@class='select2-selection__rendered']")
    channel_text_field_locator = (
        By.XPATH, "//input[@class='select2-search__field']")
    define_missing_fields_warning_message_locator = (By.XPATH,
                                                     "//li[normalize-space()='Please define missing fields: Company "
                                                     "profile, IO title, Date, Client, Client company, Email, Contact, "
                                                     "Currency rate, Sales manager.']")
    select_button_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    campaign_locator = (By.XPATH,
                        "//label[contains(text(), 'Campaign')]/..//span[@class='mselect-selection']")
    payment_type_checked_radio_button_locator = (
        By.XPATH, "//label[contains(text(), 'Invoice/payment type')]/..//input[@checked='checked']/..")
    # [End] locators

    # [Start] label names
    delete_label = "Delete"
    currency_rate_label = "Currency rate"
    io_main_information_label = "IO main information"
    client_profile_label = "Client profile"
    billing_entity_label = "Billing entity"
    io_object_label = "IO object"
    total_media_budget_label = "Total media budget"
    billing_information_label = "Billing information"
    button_label = "Buttons"
    close_label = "Close"
    campaign_cost_label = "Campaign cost"
    actual_spend_label = "Actual spend"
    # [End] label names

    # [Start] Attribute values
    io_main_info_xpath = "//h6[normalize-space()='IO main information']"
    client_profile_xpath = "//h6[normalize-space()='Client profile']"
    billing_entity_xpath = "//h6[normalize-space()='Billing entity']"
    io_object_xpath = "//h6[normalize-space()='IO object']"
    total_media_budget_xpath = "//h6[normalize-space()='Total media budget']"
    billing_information_xpath = "//h6[normalize-space()='Billing information']"
    tr_serial1_id = "tr-serial1"
    tr_serial2_id = "tr-serial2"
    select2_client_container_id = "select2-client-container"
    # [End] Attribute values

    # [START] data-qa attribute values
    media_budget_arrow_icon_data_qa = "media-budget-arrow-icon-{}"
    media_budget_remove_icon_data_qa = "media-budget-remove-icon-{}"
    date_from_row_info_data_qa = "date-from-row-info"
    total_currency_info_data_qa = "total-currency-info"
    cpm_rate_info_data_qa = "cpm-rate-info"
    goal_info_data_qa = "goal-info"
    date_to_row_info_data_qa = "date-to-row-info"
    media_budget_arrow_data_qa = "media-budget-arrow-icon-2"
    insertion_order_info_data_qa = "insertion-order-id"
    discount_field_data_qa = "discount-input"
    save_and_generate_io_button_data_qa = "save-and-generate-io-btn"
    success_message_data_qa = "alert"
    invoice_status_selected_item_data_qa = "invoice-status-select"
    payment_details_section_data_qa = "payment-details-arrow-btn"
    date_field_data_qa = "date-input"
    vat_field_data_qa = "vat-input"
    period_field_data_qa = "period-input-1"
    second_period_field_data_qa = "period-input-2"
    status_data_qa = "paid-status"
    media_budget_plus_button_data_qa = "media-budget-add-icon-1"
    comment_text_field_data_qa = "comment-textarea"
    created_by_info_data_qa = "created-by-info"
    last_updated_by_info_data_qa = "last-update-by-info"
    created_info_data_qa = "created-info"
    last_updated_info_data_qa = "last-updated-info"
    create_invoice_button_data_qa = "create-invoice-btn"
    io_execution_update_info_data_qa = "io-execution-last-update-info"
    download_button_data_qa = "download-btn"
    download_io_button_data_qa = "io-btn"
    io_date_data_qa = "date-input"
    io_title_input_data_qa = "io-title-input"
    client_select_data_qa = "client-select"
    sales_manager_select_data_qa = "sales-manager-select"
    campaign_select_data_qa = "campaigns-select"
    country_select_data_qa = "country-select-1"
    second_country_select_data_qa = "country-select-2"
    campaign_type_select_data_qa = "campaign-type-select-1"
    second_campaign_type_select_data_qa = "campaign-type-select-2"
    notes_textarea_data_qa = "notes-textarea"
    currency_select_data_qa = "currency-select"
    invoice_status_select_data_qa = "invoice-status-select"
    email_input_data_qa = "email-input"
    contact_input_data_qa = "contact-input"
    send_feedback_after_io_closed_data_qa = "feedback-email-check"
    signed_io_check_data_qa = "signed-check"
    payment_term_days_input_data_qa = "payment-term-days-input"
    create_invoice_btn_data_qa = "create-invoice-btn"
    credit_limit_info_data_qa = "credit-limit-level-info"
    overdue_info_data_qa = "overdue"
    finance_balance_info_data_qa = "finance-balance-info"
    open_ios_amount_info_data_qa = "open-ios-amount-info"
    open_ios_info_data_qa = "open-ios-info"
    last_invoice_info_data_qa = "last-invoice-info"
    last_payment_info_data_qa = "last-payment-info"
    discount_info_data_qa = "discount-info"
    rebate_info_data_qa = "rebate-info"
    bonus_info_data_qa = "bonus-info"
    tax_info_data_qa = "tax-info"
    io_execution_comment_select_data_qa = "io-execution-comment-select"
    responsible_adops_input_data_qa = "responsible-adops-select"
    client_company_select_data_qa = "client-company-select"
    company_profile_select_data_qa = "company-profile-select"
    goal_input_data_qa = "goal-input-{}"
    media_budget_input_data_qa = "media-budget-input-{}"
    campaign_status_info_data_qa = "campaign-status-info"
    total_io_amount_info_data_qa = "total-io-amount-info"
    total_io_amount_usd_info_data_qa = "total-io-amount-in-usd-info"
    total_amount_invoiced_info_data_qa = "total-amount-invoiced-info"
    left_amount_to_invoice_info_data_qa = "left-amount-to-invoice-info"
    total_spent_amount_info_data_qa = "total-spent-amount-info"
    spent_last_month_info_data_qa = "spent-last-month-info"
    invoices_info_data_qa = "invoices-info"
    country_row_info_data_qa = "country-row-info"
    campaign_type_info_data_qa = "campaign-type-info"
    total_media_budget_info_data_qa = "total-media-budjet-info"
    media_budget_info_data_qa = "total-currency-info"
    channel_info_data_qa = "channel-info"
    buttons_group_data_qa = "form-nav-step-Buttons"
    user_wise_media_budget_xpath = "//span[@title='{}']/../../../../..//div[@class='form-group']//div[" \
                                   "@class='part']//input"
    # [END] data-qa attribute values
