from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from locators.io.invoice_list_locator import InvoiceListLocators
from locators.io.invoice_form_locator import InvoiceFormLocators
from pages.base_page import BasePage
from datetime import datetime


class DspDashboardInvoiceList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def click_on_specific_invoice(self, invoice_title):
        locator = (By.XPATH,
                   "//div[text()='" + invoice_title + "']/..//following-sibling::td[4]")
        self.wait_for_element_to_be_clickable(locator)
        self.click_on_element(locator, locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)

    def get_last_invoice_date_from_list(self, locator):
        date_elements = self.driver.find_elements(*locator)
        invoices_dates_list = [element.text for element in
                               date_elements]

        last_date = None
        for date_str in invoices_dates_list:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            if last_date is None or date_obj > last_date:
                last_date = date_obj

        return last_date.strftime("%d %b, %Y") if last_date else None
