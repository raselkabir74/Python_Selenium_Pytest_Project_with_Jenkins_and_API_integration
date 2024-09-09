import re

from locators.budget.budget_locator import BudgetLocators
from pages.base_page import BasePage
from pages.navbar.navbar import DashboardNavbar


class DspDashboardAddPayment(BasePage):

    def __init__(self, config, driver):
        super().__init__(driver)
        self.config = config

    def add_budget_into_specific_client(self, client_name, amount_to_add):
        navbar_page = DashboardNavbar(self.driver)
        budget_value = None
        budget_url = self.config['credential']['url'] + self.config['budget-page']['budget-page-url']
        budget = self.get_element_text(BudgetLocators.budget_amount_locator)
        match = re.search(r'\d+', budget)
        if match:
            budget_value = int(match.group())
        if "qa-testing" in self.config['credential']['url']:
            navbar_page.impersonate_user(name=client_name)
            if budget_value < 10:
                self.driver.get(budget_url)
                self.select_from_modal_form_using_js_code(BudgetLocators.user_filter_xpath, client_name)
                self.wait_for_spinner_load()
                self.add_payment(amount_to_add)

    def add_payment(self, amount_to_add):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + base_url + self.config['cron-jobs'][
                           'budget-add-cron-job']
        self.click_on_specific_button(BudgetLocators.add_payment_label,
                                      locator_to_be_appeared=BudgetLocators.amount_field_locator)
        self.set_text_using_tag_attribute(self.input_tag, self.placeholder_tag, BudgetLocators.amount_placeholder,
                                          str(amount_to_add))
        self.click_on_specific_button(BudgetLocators.add_label,
                                      locator_to_be_appeared=BudgetLocators.success_message_locator)
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])

    def display_budget_information(self, user_id):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + self.config['debugger_credentials']['debugging-username'] + ":" + self.config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + self.config['cron-jobs'][
                           'budget-related-cron-job'].format(str(user_id))
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])
