from selenium.webdriver.common.by import By


class AudienceListLocators:
    # [Start] locators
    add_audience_button_locator = (
        By.XPATH, "//a[@data-qa='add-audience-btn']")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    audience_search_field_locator = (By.XPATH, "//input[@data-qa='search-filter-input']")
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    # [End] locators

    # [Start] Attribute values
    edit_data_qa = "item-action-Edit-"
    delete_data_qa = "item-action-Delete-"
    dmp_audience_groups_tab_data_qa = "audience-tab-DMP audience groups"
    first_party_tab_data_qa = "audience-tab-First party"
    three_dot_of_audience_xpath = "//a[contains(text(), '{}')]//..//..//..//i[@class='fas fa-ellipsis-v']"
    checkbox_audience_xpath = "//a[contains(text(), '{}')]//..//..//input"
    edit_link_xpath = "//div[@id='tab-id-{}']//a[@data-qa='edit-audience-btn']"
    delete_link_xpath = "//div[@id='tab-id-{}']//a[@data-qa='delete-audience-btn']"
    # [End] Attribute values
