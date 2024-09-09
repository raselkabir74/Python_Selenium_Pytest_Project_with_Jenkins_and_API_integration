from selenium.webdriver.common.by import By


class BillingEntitiesFormLocators:
    # [Start] locators
    save_button_locator = (By.XPATH, "//button[@data-qa='company-profile-save-btn']")
    cancel_button_locator = (By.XPATH, "//a[@data-qa='company-profile-cancel-btn']")
    country_value_locator = (
        By.XPATH,
        "//select[@data-qa='company-profile-country-select']/..//span[@class='select2-selection__rendered']")
    vat_locator = (By.XPATH, "//input[@data-qa='company-profile-igst-vat-input']")
    # [End] locators

    # [Start] label names
    title_data_qa = "company-profile-title-input"
    company_name_data_qa = "company-profile-name-input"
    address_data_qa = "company-profile-address-input"
    postcode_data_qa = "company-profile-postcode-input"
    country_data_qa = "company-profile-country-select"
    phone_number_data_qa = "company-profile-phone-number-input"
    registration_number_data_qa = "company-profile-reg-number-input"
    vat_code_data_qa = "company-profile-vat-code-input"
    bank_number_data_qa = "company-profile-bank-account-number-input"
    # [End] label names
