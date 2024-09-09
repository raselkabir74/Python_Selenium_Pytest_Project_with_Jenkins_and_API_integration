from selenium.webdriver.common.by import By


class CompanyFormLocators:
    # [START] data-qa attribute values
    company_name_locator = "official-company-name-input"
    country_dropdown_locator = (By.ID, 'select2-country-container')
    company_address_textarea_locator = "company-address-textarea"
    company_registration_number_locator = "company-registration-number-input"
    company_vat_id_locator = "company-vat-id-input"
    company_financial_contact_name_locator = "company-financial-contact-name-input"
    company_financial_contact_email_locator = "company-financial-contact-email-input"
    company_financial_phone_number_locator = "finance-phone-number-input"
    company_payment_term_locator = "payment-term-days-input"
    company_discount_locator = "discount-input"
    company_rebate_locator = "rebate-input"
    company_bonus_locator = "bonus-input"
    company_tax_locator = "tax-input"
    save_button_locator = "save-btn"
    cancel_button_locator = "cancel-btn"
    auto_invoicing_add_btn = "auto-invoicing-add-btn"
    final_credit_limit_locator = "final-credit-limit-with-vat-usd-input"
    billing_type_locator = "billing-type-radio-Pre-paid"
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    group_all_client_radio_button_locator = (By.XPATH,
                                             "(//input[@data-qa='how-group-invoice-media-budgets-radio-3'])[1]")
    auto_billing_remove_button_locator = (By.XPATH, "//i[@data-qa='auto-invoicing-remove-btn']")
    ok_button_locator = (By.XPATH, "//button[@data-bb-handler='ok']")
    # [START] data-qa attribute values

    # [Start] labels
    country_label = 'country-select'
    collection_person_label = 'Collection person'
    auto_billing_users_label = 'Auto billing users?'
    select_client_main_account_for_io_invoice_label = 'Select client main account for IO/Invoice'
    client_tier_label = 'Client Tier'
    end_of_month_interim_invoices_label = 'End of month (+interim invoices)'
    end_of_io_budgets_spend_campaign_status_complete_label = 'End of IO budgets spend (campaign status = complete)'
    one_line_dsp_services_default_label = 'One line "DSP services" (default)'
    by_media_budget_and_country_label = 'By media budget and country'
    group_all_client_ios_under_one_invoice_label = "Group all client io's under one invoice"
    grouping_by_account_and_io_label = "Grouping by account and IO"
    group_all_client_account_self_service_label = 'Group all client accounts under one invoice (always a new ' \
                                                  'IO+invoice(dedicated for self-service))'
    # [End] labels

    # [Start] Attributes
    collection_person_dropdown_locator = (By.ID, 'select2-collection_person_id-container')
    client_tier_dropdown_locator = (By.ID, 'select2-tier-container')
    credit_limit_id = "credit_limit"
    manually_reviewed_credit_limit_percentage_id = "manually_reviewed_credit_limit_percentage"
    # [End] Attributes
