from selenium.webdriver.common.by import By


class BudgetLocators:
    # [Start] locators
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    amount_field_locator = (By.XPATH, "//input[@placeholder='Amount']")
    budget_amount_locator = (By.XPATH, "//a[@class='nav-link']")
    # [End] locators

    # [Start] labels
    add_payment_label = "Add Payment"
    add_label = "Add"
    # [End] labels

    # [Start] attributes
    user_filter_xpath = "//select[@data-placeholder='User']"
    amount_placeholder = "Amount"
    # [End] attributes
