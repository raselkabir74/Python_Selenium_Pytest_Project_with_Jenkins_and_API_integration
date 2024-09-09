from collections import defaultdict
from datetime import date, timedelta, datetime

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class DspDashboardSoaReport(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def is_specific_filter_field_available(self, filter_label_data_qa):
        locator = (
            By.XPATH, "//label[normalize-space()='" + filter_label_data_qa +
            "']/..//span[@class='mselect-selection__rendered'] | //select[@data-qa='" + filter_label_data_qa +
            "']/..//span[@class='select2-selection__rendered'] | //select[@data-qa='" + filter_label_data_qa +
            "']/..//span[@class='mselect-selection__rendered']")
        return self.is_element_present(locator)

    def check_if_the_invoice_is_in_the_list(self, locator, invoice_number):
        self.wait_for_visibility_of_all_elements_located(locator)
        elements = self.driver.find_elements(*locator)
        elements_list = [element.text for element in elements]
        if invoice_number in elements_list:
            return invoice_number
        else:
            return None

    def clear_specific_filter_option_from_soa_report_page(self, field_name):
        locator = (
            By.XPATH, "//label[normalize-space()='" + field_name +
            "']/..//span[@class='select2-selection__clear'] | //select[@data-qa='" + field_name +
            "']/..//span[@class='select2-selection__clear']")
        self.click_on_element(locator)

    def get_amount_and_currency_list_from_specific_columns(self, amount_locator, currency_locator):
        self.wait_for_visibility_of_all_elements_located(amount_locator)
        self.wait_for_visibility_of_all_elements_located(currency_locator)
        amounts = [element.text for element in self.driver.find_elements(*amount_locator)]
        currencies = [element.text for element in self.driver.find_elements(*currency_locator)]
        invoice_amount_currency_list = list(zip(amounts, currencies))
        return invoice_amount_currency_list

    def get_calculated_total_amount_by_currency(self, invoice_amount_currency_list):
        total_amounts = defaultdict(float)
        for amount, currency in invoice_amount_currency_list:
            if amount == '-':
                amount = '0'
            amount = amount.replace(',', '')
            amount_value = float(amount)
            total_amounts[currency] += amount_value
        formatted_total_amounts = {currency: '{:.2f}'.format(amount) for currency, amount in total_amounts.items()}
        return formatted_total_amounts

    def get_total_row_amount(self, total_row_locator):
        locator = (By.XPATH, "//*[@data-qa='" + total_row_locator + "']")
        self.wait_for_visibility_of_element(locator)
        element = self.driver.find_element(*locator)
        summary_text = element.text
        lines = summary_text.split('\n')
        total_amounts = {}
        for line in lines:
            parts = line.split(' : ')
            if len(parts) == 2:
                currency, amount_str = parts
                total_amounts[currency] = amount_str
        return total_amounts

    def get_last_month_date_with_format(self, date_format):
        today = date.today()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        formatted_date = last_day_of_last_month.strftime(date_format)
        return str(formatted_date)

    def get_invoice_period(self):
        current_date_str = self.get_current_date_with_specific_format("%d %b, %Y")
        current_date = datetime.strptime(current_date_str, "%d %b, %Y").day
        if 1 <= current_date <= 5:
            return self.get_last_month_date_with_format("%Y-%m")
        elif 6 <= current_date <= 31:
            return self.get_current_date_with_specific_format("%Y-%m")
        else:
            return None
