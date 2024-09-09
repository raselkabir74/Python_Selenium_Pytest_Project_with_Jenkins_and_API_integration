from selenium.webdriver.common.by import By


class IoListLocators:
    # [START] data-qa attribute values
    create_io_button_data_qa = 'create-new-io-btn'
    title_field_data_qa = 'io-title-input'
    search_field_data_qa = 'search-filter-input'
    logs_dropdown_icon_data_qa = 'logs-arrow-btn'
    payment_actions_data_qa = 'payment-actions-item'
    comment_textarea_data_qa = 'other-comment-textarea'
    client_account_data_qa = 'client-account-select'
    client_company_data_qa = 'client-company-select'
    company_group_data_qa = 'company-group-select'
    eskimi_billing_entity_data_qa = 'eskimi-billing-entity-select'
    sent_data_qa = 'sent-select'
    paid_data_qa = 'paid-select'
    expired_data_qa = 'expired-select'
    bill_status_data_qa = 'bill-status-select'
    io_period_data_qa = 'io-period-select'
    invoice_period_data_qa = 'invoice-period-select'
    credit_invoice_data_qa = 'credit-invoice-select'
    io_signed_data_qa = 'io-signed-select'
    responsible_adops_data_qa = 'responsible-adops-select'
    sales_person_data_qa = 'sales-person-select'
    sales_team_data_qa = 'sales-team-select'
    account_manager_data_qa = 'account-manager-select'
    io_campaign_status_data_qa = 'io-campaign-status-select'
    io_deadline_data_qa = 'io-deadline-select'
    io_execution_comment_data_qa = 'io-execution-comment-select'
    io_warning_message_data_qa = 'io-warning-message-select'
    three_dot_data_qa = 'item-action-{}'
    edit_io_data_qa = 'item-action-Edit IO-{}'
    proforma_data_qa = 'item-action-Proforma-{}'
    invoice_data_qa = 'item-action-Invoice-{}'
    add_invoice_data_qa = 'item-action-Add invoice-{}'
    add_proforma_data_qa = 'item-action-Add proforma-{}'
    invoice_issued_data_qa = 'item-action-Invoice issued-{}'
    edit_execution_comment_data_qa = 'item-action-Edit execution comment (internal)-{}'
    signed_io_checkbox_data_qa = 'signed-check-{}'
    # [END] data-qa attribute values

    # [Start] locators
    first_grid_item_locator = (
        By.XPATH, "//table[@id='campaigns-io-table']//tbody//tr//a")
    total_row_count_locator = (
        By.XPATH, "//div[@id='campaigns-io-table_info']")
    no_data_for_defined_criteria_locator = (
        By.XPATH, "//td[normalize-space()='No data for defined criteria.']")
    execution_comment_form_locator = (
        By.XPATH, "//div[label='Execution comment form']")
    update_execution_comment_button_locator = (
        By.XPATH, "//button[text()='Update execution comment']")
    cancel_button_locator = (By.XPATH, "//button[text()='Cancel']")
    add_proforma_locator = (By.XPATH, "(//a[@title='Add proforma'])[1]")
    edit_io_locator = (By.XPATH, "(//a[@title='Edit IO'])[1]")
    invoice_locator = (By.XPATH, "(//a[@title='Invoice'])[1]")
    # [End] locators

    # [Start] label names
    edit_execution_comment_label = "Edit execution comment (internal)"
    client_label = "Client"
    title_label = "Title"
    io_warning_label = "IO warning"
    responsible_adops_label = "Responsible adops"
    sales_manager_label = "Sales manager"
    sales_team_label = "Sales team"
    account_manager_label = "Account manager"
    campaigns_label = "Campaigns"
    campaign_status_label = "Campaign status"
    deadline_label = "Deadline"
    io_date_label = "IO date"
    amount_label = "Amount"
    io_execution_comment_label = "IO execution comment"
    io_campaign_execution_comment_label = "IO-campaign execution comment (internal)"
    adjusted_io_amount_label = "Adjusted IO amount"
    adjusted_io_amount_usd_label = "Adjusted IO amount in USD"
    amount_in_usd_label = "Amount in USD"
    country_label = "Country"
    invoice_number_label = "Invoice #"
    proforma_label = "Proforma"
    invoice_sent_label = "Invoice sent"
    campaign_start_date_label = "Campaign start date"
    campaign_end_date_label = "Campaign end date"
    campaign_left_to_spent = "Left to spent"
    paid_status_label = "Paid status"
    spent_amount_label = "Spent amount (RM)"
    # [End] label names

    # [Start] Attribute values
    io_number_link_xpath = "(//div[text()='{}']/../..//td[1]/a[@href])[1]"
    campaigns_io_table_wrapper_div_id = "campaigns-io-table_wrapper"
    # [End] Attribute values

    # [Start] Options
    test_automation_company_data = "Test Automation Company"
    other_comment_option = "Other: Comment"
    interim_invoice_option = "Interim invoice"
    # [End] Options
