from selenium.webdriver.common.by import By


class TrackingPixelLocators:
    tracking_data_qa = 'tracking-select'
    conversion_data_qa = 'tracking-checkbox-2'
    audience_text_locator = (By.XPATH, "(//div[@class='ace_content'])[1]")
    conversion_text_locator = (By.XPATH, "(//div[@class='ace_content'])[2]")
    example_text_locator = (By.XPATH, "(//div[@class='ace_content'])[3]")

