from selenium.webdriver.common.by import By


class BrandSafetyFormLocators:
    # [Start] locators
    title_field_locator = (By.XPATH, "//input[@data-qa='brand-safety-title-input']")
    keywords_upload_locator = (By.XPATH, "//input[@data-qa='brand-safety-file-input']")
    save_button_locator = (By.XPATH, "//button[@data-qa='brand-safety-save-btn']")
    cancel_link_locator = (
        By.XPATH, "//a[@data-qa='brand-safety-cancel-btn']")
    # [End] locators

    # [Start] label names
    context_checkboxes_label = "Context options"
    # [End] label names

    # [Start] Attribute values
    default_data_qa = "brand-safety-default-select"
    status_data_qa = "brand-safety-status-select"
    # [End] Attribute values
