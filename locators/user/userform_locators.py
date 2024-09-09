from selenium.webdriver.common.by import By


class UserFormLocators:
    # [START] data-qa attribute values
    username_data_qa = "login-input"
    password_data_qa = "plain-password-input"
    repeat_password_data_qa = "repeat-password-input"
    account_name_data_qa = "account-name-input"
    email_data_qa = "email-input"
    contact_person_full_name_data_qa = "contact-person-full-name-input"
    contact_person_email_data_qa = "contact-person-email-input"
    contact_person_phone_data_qa = "contact-person-phone-input"
    currency_rate_data_qa = "currency-rate-input"
    min_bid_data_qa = "min-bid-input"
    max_bid_data_qa = "max-bid-input"
    tech_fee_data_qa = "tech-fee-input"
    discount_field_data_qa = "discount_agency-input"
    check_all_billing_button_data_qa = "billing-check-all-btn"
    billing_all_io_proforma_invoice_checkbox_data_qa = 'tmp-billing-option-1'
    billing_clients_management_margins_checkbox_data_qa = 'tmp-billing-option-2'
    billing_io_view_its_clients_only_checkbox_data_qa = 'tmp-billing-option-4'
    billing_invoice_create_and_view_its_clients_checkbox_data_qa = 'tmp-billing-option-128'
    add_execution_comment_to_io_invoice_proforma_checkbox_data_qa = 'tmp-billing-option-4194304'
    # [END] data-qa attribute values

    # [Start] locators
    country_dropdown_locator = (
        By.XPATH, "//span[@id='select2-country-container']")
    company_dropdown_locator = (
        By.XPATH, "//span[@id='select2-company-container']")
    currency_dropdown_locator = (
        By.XPATH, "//span[@id='select2-currency-container']")
    save_button_locator = (By.XPATH, "//button[@type='submit']")
    cancel_button_locator = (By.XPATH, "//button[@type='reset']")
    billing_settings_locator = (
        By.XPATH, "//a[normalize-space()='Billing settings']")
    finance_options_section_expand_icon_locator = (
        By.XPATH,
        "//span[normalize-space()='Finance options']/following-sibling::span")
    currency_and_margins_section_locator = (
        By.XPATH, "//a[contains(text(), 'Currency & Margins')]")
    select_child_acc_user_search_locator = (By.XPATH, "//input[@class='search-select form-control']")
    child_acc_checkbox_xpath = "//span[@data-value='{}']"
    select_btn_locator = (By.XPATH, "//button[@class='btn btn btn-primary mselect-submit-selected']")
    select_user_locator = (By.XPATH, "//span[@data-qa='child-accounts-select']")
    # [End] locators

    # [Start] labels
    country_label = 'Country'
    company_label = 'Official company (organization) name'
    sales_manager_label = 'Sales manager'
    responsible_adops_label = 'Responsible adops'
    account_manager_label = 'Account manager'
    currency_label = 'Currency'
    all_users_label = 'All users'
    # [End] labels
