from selenium.webdriver.common.by import By


class CreditNoteFormLocators:
    # [Start] locators
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    back_to_invoice_list_locator = (
        By.XPATH, "//a[normalize-space()='BACK TO INVOICE LIST']")
    save_button_locator = (By.XPATH, "//input[@value='Save']")
    credit_type_field_locator = (
        By.XPATH,
        "//label[normalize-space()='Credit type']/..//span[@id='select2-client-container']")
    client_company_field_locator = (
        By.XPATH,
        "//label[normalize-space()='Client company']/..//span[@id='select2-client-container']")
    company_profile_field_locator = (
        By.XPATH,
        "//label[normalize-space()='Company profile']/..//span[@id='select2-company_profile-container']")
    calender_icon_locator = (
        By.XPATH,
        "//i[@class='fas fa-calendar-alt calendar-related-icon']")
    today_date_locator = (
        By.XPATH, "//td[contains(@class, 'datepickerToday')]")
    client_type_field_locator = (By.ID, "client")
    # [End] locators

    # [Start] label names
    credit_type_label = "Credit type"
    payment_note_label = "Credit/payment notes (internal)"
    credit_note_label = "Notes in credit PDF"
    date_label = "Date"
    # [End] label names

    # [Start] Attribute values
    form_control_credit_amount_class = "form-control credit-amount"
    first_invoice_number_class = "first invoice-number"
    invoice_main_information_attribute = "//a[normalize-space()='Invoice main information']"
    # [End] Attribute values
