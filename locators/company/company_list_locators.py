from selenium.webdriver.common.by import By


class CompanyListLocators:
    # [START] data-qa attribute values
    add_company_button_locator_data_qa = "add-new-company-btn"
    success_message_locator_data_qa = "alert"
    search_box_locator_data_qa = "filter-search-input"
    # [End] data-qa attribute values
    # [Start] locators
    delete_option_locator = (By.XPATH, "//a[@title='Delete']")
    edit_option_locator = (By.XPATH, "//a[@title='Edit']")
    alert_confirm_button_locator = (
        By.XPATH,
        "//button[@data-bb-handler='confirm' and @type ='button']")
    no_record_message_locator = (
        By.XPATH, "//td[@class='dataTables_empty']")
    # [End] locators

    # [Start] attributes
    three_dot_locator_xpath = "//table[@id='companies-table']//span[normalize-space()='{}']//..//..//..//td[@class='dropdown actions']"
    # [End] attributes
