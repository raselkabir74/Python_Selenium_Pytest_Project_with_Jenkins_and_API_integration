from selenium.webdriver.common.by import By


class BillingEntitiesListLocators:
    # [Start] locators
    btn_create_locator = (By.XPATH,
                          "//a[@data-qa='add-new-profile-btn']")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    search_box_locator = (By.ID, 'filter_name')
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    empty_row_locator = (By.XPATH, "//td[@class='dataTables_empty']")
    # [End] locators

    # [Start] Attributes
    three_dot_xpath = "//td[text()='{}']/..//a[contains(@data-qa, 'action-')]//i"
    edit_xpath = "//td[text()='{}']/..//a[@role='button']//..//a[contains(@data-qa, 'edit-')]"
    delete_xpath = "//td[text()='{}']/..//a[@role='button']//..//a[contains(@data-qa, 'delete-')]"
    # [End] Attributes
