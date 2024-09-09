from selenium.webdriver.common.by import By


class UserListLocators:
    # [START] data-qa attribute values
    add_user_button_data_qa = "add-user-btn"
    bulk_user_button_data_qa = "add-bulk-user-btn"
    success_message_data_qa = "alert"
    search_box_data_qa = "search-btn"
    # [END] data-qa attribute values

    # [Start] locators
    processing_loader_locator = (
        By.XPATH, "//div[@id='users-table_processing']")
    three_dot_locator = (By.XPATH,
                         "//table[@id='users-table']//tr[@data-row-id='0']//td[@class='dropdown actions']//a")
    delete_option_locator = (By.XPATH, "//a[contains(@data-qa, 'item-action-Delete')]")
    edit_option_locator = (By.XPATH, "//a[contains(@data-qa, 'item-action-Edit')]")
    alert_confirm_button_locator = (
        By.XPATH,
        "//button[@data-bb-handler='confirm' and @type ='button']")
    # [End] locators
