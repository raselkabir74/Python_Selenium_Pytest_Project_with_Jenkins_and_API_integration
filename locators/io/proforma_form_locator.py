from selenium.webdriver.common.by import By


class ProformaFormLocators:
    # [Start] data-qa attribute values
    save_and_generate_proforma_button_data_qa = "save-and-generate-proforma-btn"
    # [End] data-qa attribute values

    # [Start] locators
    discount_field_locator = (By.XPATH, "//input[@data-qa='discount-input']")
    invoice_object_dropdown_selected_item_locator = (
        By.XPATH, "//select[@data-qa='invoice-object-service-type-select']/..//span[@title]")
    buttons_group_locator = (By.XPATH, "//li[@data-qa='form-nav-step-Buttons']//a")
    save_and_sync_with_io_button_locator = (By.XPATH, "//input[@data-qa='save-and-sync-with-io-btn']")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    back_to_list_locator = (By.XPATH, "//a[normalize-space()='BACK TO LIST']")
    invoice_status_selected_item_locator = (By.XPATH, "//select[@data-qa='invoice-status-select']/..//span[@title]")
    payment_details_section_locator = (By.XPATH, "//span[@data-qa='payment-details-arrow-icon']")
    confirmation_yes_button_locator = (By.XPATH,
                                       "//div[text()='Are you sure you want to add another proforma for "
                                       "this IO?']/../..//button[normalize-space()='Yes']")
    status_locator = (By.XPATH, "//p[@class='form-status-paid']")
    channel_dropdown_locator = (By.XPATH,
                                "//select[@data-qa='channel-select-1']/..//span[@class='select2-selection__rendered']")
    channel_text_field_locator = (By.XPATH, "//input[@class='select2-search__field']")
    billing_info_dropdown_locator = (
        By.XPATH, "//h6[normalize-space()='Billing information']/..//div[@data-target='#ac-payment-details']")
    add_payment_locator = (By.XPATH, "//a[@data-qa='add-payment-btn']")
    save_add_payment_button_locator = (By.XPATH, "//button[text()='Save']")
    invoices_xpath = "//a[text()='{}']"
    proforma_title_locator = (By.XPATH, "//input[@data-qa='proforma-title-input']")
    amount_paid_locator = (By.XPATH, "//label[@data-qa='amount-paid-label']/..//input")
    # [End] locators

    # [Start] label names
    amount_paid_label = "Amount paid"
    # [End] label names

    # [Start] Attribute values
    currency_data_qa = "currency-select"
    invoice_status_data_qa = "invoice-status-select"
    vat_data_qa = "vat-input"
    email_data_qa = "email-input"
    contact_data_qa = "contact-input"
    invoice_object_data_qa = "invoice-object-service-type-select"
    currency_rate_data_qa = "currency-rate-select"
    payment_term_days_data_qa = "payment-term-days-input"
    io_execution_comment_data_qa = "io-execution-comment-select"
    campaign_data_qa = "campaigns-select"
    country_data_qa = "country-select-1"
    notes_data_qa = "notes-textarea"
    proforma_title_data_qa = "proforma-title-input"
    client_data_qa = "client-select"
    sales_manager_data_qa = "sales-manager-select"
    select2_client_container_id = "select2-client-container"
    select2_responsible_adops_container_id = "select2-responsible_adops-container"
    select2_company_profile_container_id = "select2-company_profile-container"
    select2_sales_manager_container_id = "select2-sales_manager-container"
    select2_io_execution_comment_id_container_id = "select2-io_execution_comment_id-container"
    country_row_data_qa = "country-row-info"
    campaign_type_data_qa = "campaign-type-info"
    first_total_media_budget_data_qa = "total-media-budget-info"
    select2_currency_container_id = "select2-currency-container"
    discount_data_qa = "discount-input"
    form_control_media_budget_data_qa = "media-budget-input-1"
    # [End] Attribute values
