from selenium.webdriver.common.by import By


class BrandSafetyListLocators:
    # [Start] locators
    add_button_locator = (
        By.XPATH, "//a[@data-qa='brand-safety-create-btn']")
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    search_field_locator = (By.XPATH, "//input[@data-qa='brand-safety-search-input']")
    # [End] locators

    # [Start] attribute values
    brand_safety_option_edit_link_xpath = "//a[normalize-space(text())='{}' and @data-qa='brand-safety-title'] "
    three_dot_of_campaign_xpath = "//a[contains(text(), '{}')]/..//..//a[contains(@data-qa, 'item-action-')]//i"
    keyword_count_xpath = "//a[contains(text(), '{}')]/..//..//a[@data-qa='brand-safety-count']"
    # [End] attribute values

    # [Start] Attribute names
    delete_data_qa = "item-action-Delete-"
    # [End] Attribute names
