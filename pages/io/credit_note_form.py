import time

from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.credit_note_form_locator import CreditNoteFormLocators
from pages.base_page import BasePage

credit_note_information = {'credit_note_information': {}}


class DspDashboardICreditNoteForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def add_credit_note_into_invoice(self, credit_note_data):
        retry_count = 0
        max_retry_count = 3
        self.click_on_specific_button(InvoiceFormLocators.credit_note_button,
                                      locator_to_be_appeared=CreditNoteFormLocators.client_type_field_locator)
        while retry_count < max_retry_count:
            self.set_value_into_specific_input_field(CreditNoteFormLocators.date_label,
                                                     self.get_current_date_with_specific_format(
                                                         "%d %b, %Y"), tab_out=True)
            time.sleep(2)
            self.click_element_execute_script(
                CreditNoteFormLocators.invoice_main_information_attribute)
            self.click_on_element(
                CreditNoteFormLocators.calender_icon_locator)
            time.sleep(2)
            self.click_on_element(
                CreditNoteFormLocators.today_date_locator)
            self.select_dropdown_value(CreditNoteFormLocators.credit_type_label,
                                       credit_note_data['credit_note_information'][
                                           'credit_type'])
            self.set_text_using_tag_attribute(self.input_tag,
                                              self.class_attribute,
                                              CreditNoteFormLocators.form_control_credit_amount_class,
                                              credit_note_data[
                                                  'credit_note_information'][
                                                  'credit_amount'])
            self.set_value_into_specific_input_field(CreditNoteFormLocators.payment_note_label, credit_note_data[
                'credit_note_information']['payment_note'], is_textarea=True)
            self.set_value_into_specific_input_field(CreditNoteFormLocators.credit_note_label, credit_note_data[
                'credit_note_information']['credit_note'], is_textarea=True)
            self.click_on_element(
                CreditNoteFormLocators.save_button_locator)
            status = self.is_visible(CreditNoteFormLocators.success_message_locator, time_out=5)
            if status:
                credit_invoice_number = self.get_text_using_tag_attribute(
                    self.div_tag,
                    self.class_attribute,
                    CreditNoteFormLocators.first_invoice_number_class)
                return credit_invoice_number
            else:
                self.driver.refresh()
                time.sleep(2)
                retry_count += 1

    def get_success_message(self):
        return self.get_element_text(
            CreditNoteFormLocators.success_message_locator)

    def get_credit_invoice_data(self):
        credit_note_information['credit_note_information'][
            'credit_type'] = self.get_element_text(
            CreditNoteFormLocators.credit_type_field_locator)
        credit_note_information['credit_note_information'][
            'client_company'] = self.get_element_text(
            CreditNoteFormLocators.client_company_field_locator)
        credit_note_information['credit_note_information'][
            'company_profile'] = self.get_element_text(
            CreditNoteFormLocators.company_profile_field_locator)
        credit_note_information['credit_note_information'][
            'credit_amount'] = self.get_text_using_tag_attribute(
            self.input_tag, self.class_attribute,
            CreditNoteFormLocators.form_control_credit_amount_class)
        credit_note_information['credit_note_information'][
            'payment_note'] = \
            self.get_value_from_specific_input_field(CreditNoteFormLocators.payment_note_label, is_textarea=True)
        credit_note_information['credit_note_information'][
            'credit_note'] = \
            self.get_value_from_specific_input_field(CreditNoteFormLocators.credit_note_label, is_textarea=True)
        return credit_note_information
