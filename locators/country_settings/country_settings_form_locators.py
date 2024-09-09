from selenium.webdriver.common.by import By


class CountrySettingsLocators:
    # [START] data-qa attribute values
    add_new_country_button_locator = "add-new-country-btn"
    save_all_button_locator = "save-all-btn"
    # [START] data-qa attribute values
    # [Start] locators
    ok_button_modal_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    success_message_locator = (
        By.XPATH,
        "//div[@class='alert alert-success js-submit-status']")
    # [End] locators

    # [Start] attributes
    cpc_checkbox_xpath = "//tr[@title='{}']//label[normalize-space()='CPC']//input"
    cross_icon_xpath = "//tr[@title='{}']//i"
    cpc_maximum_cpc_input_xpath = "//tr[@title='{}']//label[normalize-space()='CPC']//..//..//label[normalize-space()='Maximum CPC:']//..//input"
    cpc_minimum_impression_learn_xpath = "//tr[@title='{}']//label[normalize-space()='CPC']//..//..//label[normalize-space()='Minimum impressions per placement to learn:']//..//input"
    cpc_minimum_spend_learn_xpath = "//tr[@title='{}']//label[normalize-space()='CPC']//..//..//label[normalize-space()='Minimum spend per placement to learn:']//..//input"
    # [End] attributes

    # [Start] labels
    select_country_label = "Please select specific country"
    # [End] labels
