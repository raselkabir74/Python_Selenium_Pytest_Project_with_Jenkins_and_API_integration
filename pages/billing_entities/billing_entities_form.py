from locators.billing_entities.billing_entities_form_locators import \
    BillingEntitiesFormLocators
from pages.base_page import BasePage

billing_entities_information = {}


class DashboardBillingEntitiesForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_and_save_data(self, data):
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.title_data_qa, data['title'])
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.company_name_data_qa, data['company_name'])
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.address_data_qa, data['address'],
                                                 is_textarea=True)
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.postcode_data_qa, data['postcode'])
        self.select_dropdown_value(BillingEntitiesFormLocators.country_data_qa, data['country'])
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.phone_number_data_qa, data['phone_number'])
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.registration_number_data_qa,
                                                 data['registration_number'])
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.vat_code_data_qa, data['vat_code'])
        self.set_value_into_specific_input_field(BillingEntitiesFormLocators.bank_number_data_qa, data['bank_number'])
        self.click_on_element(
            BillingEntitiesFormLocators.save_button_locator)

    def get_billing_entities_data(self):
        global billing_entities_information
        billing_entities_information[
            'title'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.title_data_qa)
        billing_entities_information[
            'company_name'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.company_name_data_qa)
        billing_entities_information[
            'address'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.address_data_qa,
                                                                  is_textarea=True)
        billing_entities_information[
            'postcode'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.postcode_data_qa)
        billing_entities_information[
            'country'] = self.get_element_text(
            BillingEntitiesFormLocators.country_value_locator)
        billing_entities_information[
            'phone_number'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.phone_number_data_qa)
        billing_entities_information[
            'registration_number'] = self.get_value_from_specific_input_field(
            BillingEntitiesFormLocators.registration_number_data_qa)
        billing_entities_information[
            'vat_code'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.vat_code_data_qa)
        billing_entities_information[
            'bank_number'] = self.get_value_from_specific_input_field(BillingEntitiesFormLocators.bank_number_data_qa)
        self.click_on_element(
            BillingEntitiesFormLocators.cancel_button_locator)
        return billing_entities_information
