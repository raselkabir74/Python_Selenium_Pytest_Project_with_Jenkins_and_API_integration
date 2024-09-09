from selenium.webdriver.common.by import By


class PaymentsLogLocators:
    delete_button_locator = (
        By.XPATH,
        "//td[normalize-space()='Test Automation Company']/..//td[@class='not-export-col']//a")
    yes_button_locator = (
        By.XPATH,
        "//button[@class='btn btn-success' and normalize-space()='Yes']")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
