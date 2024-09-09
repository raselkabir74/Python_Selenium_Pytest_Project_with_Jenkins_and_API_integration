from selenium.webdriver.common.by import By


class BulkUserSignUpFormLocators:
    # [Start] locators
    password_locator = (By.ID, 'password')
    repeat_password_locator = (By.ID, 'password_confirmation')
    account_name_locator = (By.ID, 'account_name')
    contact_person_full_name_locator = (By.ID, 'contact_person_full_name')
    contact_person_phone_locator = (By.ID, 'contact_person_phone')
    submit_button_locator = (By.ID, 'submitBtn')
    login_button_locator = (By.XPATH, "//a[normalize-space()='Login']")
    # [End] locators
