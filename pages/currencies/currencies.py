from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from locators.currencies.currencies_locator import CurrenciesLocators
from pages.base_page import BasePage


class DspDashboardCurrencies(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def find_element(self, locator, locator_initialization=False, time_out=5):
        if locator_initialization:
            if "//" in locator:
                element = self.driver.find_element(By.XPATH,
                                                   locator)
            else:
                element = self.driver.find_element(By.ID,
                                                   locator)
        else:
            if '//' in locator[1] or By.ID == locator[0]:
                locator = locator
            else:
                locator = (By.XPATH, "//*[@data-qa='" + locator + "']")
            element = WebDriverWait(self.driver, time_out).until(
                EC.presence_of_element_located(locator),
                "Web element was not available within the specific "
                "time out. "
                "Locator: '" + str(locator) + "'")
        return element.find_element(*locator)

    def click_on_adjust(self):
        self.click_on_element(CurrenciesLocators.three_dot_locator)
        self.click_on_element(CurrenciesLocators.adjust_locator)
