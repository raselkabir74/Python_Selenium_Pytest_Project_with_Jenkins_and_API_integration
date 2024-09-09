from selenium.webdriver.common.by import By


class IndexLocator:
    # [Start] locators
    username_locator = (By.ID, 'username')
    password_locator = (By.ID, 'password')
    stage_env_message_locator = (
        By.XPATH, "//span[@class='nav' and contains(text(), 'THIS IS STAGING ENVIRONMENT. USE AT YOUR OWN RISK')]")
    submit_btn_locator = (By.XPATH, "//button[@type='submit']")
    # [End] locators

    # [Start] labels
    terms_and_conditions_checkbox_label = 'I have read and accepted the Terms and Conditions'
    # [End] labels
