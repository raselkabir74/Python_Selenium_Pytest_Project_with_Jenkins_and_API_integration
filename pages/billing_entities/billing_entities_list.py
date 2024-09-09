from locators.billing_entities.billing_entities_list_locators import \
    BillingEntitiesListLocators
from pages.base_page import BasePage

billing_entities_information = {}


class DashboardBillingEntitiesList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_billing_entities_form(self):
        self.click_on_element(
            BillingEntitiesListLocators.btn_create_locator)

    def get_success_message(self):
        return self.get_element_text(
            BillingEntitiesListLocators.success_message_locator)

    def get_empty_search_result_text(self, billing_entities_name):
        self.set_value_into_element(
            BillingEntitiesListLocators.search_box_locator,
            billing_entities_name)
        return self.get_element_text(
            BillingEntitiesListLocators.empty_row_locator)

    def action_billing_entities(self, billing_entities_name,
                                is_edit=False):
        self.set_value_into_element(
            BillingEntitiesListLocators.search_box_locator,
            billing_entities_name)
        self.click_on_element(
            BillingEntitiesListLocators.three_dot_xpath.format(
                billing_entities_name),
            locator_initialization=True)
        if is_edit:
            self.click_on_element(
                BillingEntitiesListLocators.edit_xpath.format(
                    billing_entities_name),
                locator_initialization=True)
        else:
            self.click_on_element(
                BillingEntitiesListLocators.delete_xpath.format(
                    billing_entities_name),
                locator_initialization=True)
            self.click_on_element(
                BillingEntitiesListLocators.confirm_button_alert_locator)
