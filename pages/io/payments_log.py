from locators.io.payments_log_locator import PaymentsLogLocators
from pages.base_page import BasePage


class DspDashboardPaymentsLog(BasePage):
    def get_success_message(self):
        return self.get_element_text(
            PaymentsLogLocators.success_message_locator)
