import copy
import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException

from configurations.generic_modules import step_printer
from locators.io.invoice_form_locator import InvoiceFormLocators
from pages.base_page import BasePage
from utils.io import IoUtils

invoice_information = {'invoice_main_information': {}, 'client_profile': {},
                       'billing_entity': {}, 'invoice_object': {},
                       'total_media_budget': {}, 'billing_information': {}}
payment_information = {'payment_information': {}}


class DspDashboardInvoiceForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_invoice_data_and_save(self, invoice_data,
                                      edit_invoice=False):
        step_printer("INVOICE_MAIN_INFORMATION")
        self.provide_invoice_main_information(invoice_data)

        step_printer("INVOICE_CLIENT_PROFILE")
        self.provide_invoice_client_profile_info(invoice_data,
                                                 edit_invoice)

        if edit_invoice:
            step_printer("INVOICE_CLIENT_PROFILE")
            self.provide_invoice_billing_entity_info(invoice_data)

        step_printer("INVOICE_OBJECT")
        self.provide_invoice_object_info(invoice_data)

        step_printer('INVOICE_TOTAL_MEDIA_BUDGET')
        self.provide_invoice_total_media_budget_info(invoice_data)

        step_printer('INVOICE_BILLING_INFORMATION')
        self.provide_invoice_billing_information(invoice_data,
                                                 edit_invoice)

    def provide_invoice_main_information(self, invoice_data):
        self.set_value_into_specific_input_field(InvoiceFormLocators.invoice_title_label,
                                                 invoice_data['invoice_main_information'][
                                                     'invoice_title'])

    def provide_invoice_client_profile_info(self, invoice_data,
                                            edit_invoice=False):
        if edit_invoice:
            self.set_value_into_specific_input_field(InvoiceFormLocators.email_label,
                                                     invoice_data['client_profile']['email'])
            self.set_value_into_specific_input_field(InvoiceFormLocators.contact_label,
                                                     invoice_data['client_profile']['contact'])
        else:
            self.select_dropdown_value(InvoiceFormLocators.client_label, invoice_data['client_profile'][
                'client'])
            time.sleep(self.FIVE_SEC_DELAY)

    def provide_invoice_billing_entity_info(self, invoice_data):
        self.select_dropdown_value(InvoiceFormLocators.sales_manager_label, invoice_data['billing_entity'][
            'sales_manager'])
        time.sleep(self.TWO_SEC_DELAY)

    def provide_invoice_object_info(self, invoice_data):
        self.select_from_modal(invoice_data['invoice_object']['campaign'], InvoiceFormLocators.campaign_label)
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.class_attribute,
                                          InvoiceFormLocators.form_control_media_budget_class,
                                          invoice_data[
                                              'invoice_object'][
                                              'media_budget'])
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(
            InvoiceFormLocators.channel_dropdown_locator)
        self.set_value_into_element(
            InvoiceFormLocators.channel_text_field_locator,
            invoice_data['invoice_object'][
                'channel_service'] + Keys.ENTER)

    def provide_invoice_total_media_budget_info(self, invoice_data):
        self.set_value_into_specific_input_field(InvoiceFormLocators.notes_label,
                                                 invoice_data['total_media_budget']['notes'], True)
        self.select_dropdown_value(InvoiceFormLocators.io_execution_comment_label, invoice_data['total_media_budget'][
            'io_execution_comment'])

    def provide_invoice_billing_information(self, invoice_data,
                                            edit_invoice=False):
        if edit_invoice:
            self.check_uncheck_specific_checkbox(InvoiceFormLocators.use_notice_text_on_invoice_label,
                                                 bool(invoice_data['billing_information'][
                                                          'currency']))
        self.select_dropdown_value(InvoiceFormLocators.currency_label, invoice_data['billing_information'][
            'currency'])
        self.set_value_into_specific_input_field(InvoiceFormLocators.vat_label, invoice_data[
            'billing_information'][
            'vat'])
        self.set_value_into_element(
            InvoiceFormLocators.discount_field_locator,
            invoice_data['billing_information'][
                'discount'])
        self.select_dropdown_value(InvoiceFormLocators.invoice_object_label, invoice_data['billing_information'][
            'invoice_object'])
        if self.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
            self.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                       'Client requested invoice early')
        self.click_on_save_and_generate_invoice_button(
            locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
        self.wait_for_visibility_of_element(
            InvoiceFormLocators.success_message_locator)

    def get_success_message(self):
        return self.get_element_text(
            InvoiceFormLocators.success_message_locator)

    def get_invoice_information_from_gui(self, invoice_data):
        self.reset_invoice_information()
        time.sleep(self.TWO_SEC_DELAY)
        self.get_invoice_main_information(invoice_data)
        self.get_invoice_client_profile_info()
        self.get_invoice_billing_entity_info()
        self.get_invoice_object_info()
        self.get_invoice_total_media_budget_info()
        self.get_invoice_billing_information()
        return invoice_information

    def get_invoice_main_information(self, invoice_data):
        locator = (By.XPATH, "//input[@value='" +
                   invoice_data['invoice_main_information'][
                       'invoice_title'] + "']")
        self.wait_for_visibility_of_element(locator)
        invoice_information['invoice_main_information'][
            'invoice_title'] = self.get_value_from_specific_input_field(InvoiceFormLocators.invoice_title_label)

    def get_invoice_client_profile_info(self):
        invoice_information['client_profile'][
            'client'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            InvoiceFormLocators.select2_client_container_id)
        invoice_information['client_profile'][
            'email'] = self.get_value_from_specific_input_field(InvoiceFormLocators.email_label)
        invoice_information['client_profile'][
            'contact'] = self.get_value_from_specific_input_field(InvoiceFormLocators.contact_label)

    def get_invoice_billing_entity_info(self):
        invoice_information['billing_entity'][
            'company_profile'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            InvoiceFormLocators.select2_company_profile_container_id)
        invoice_information['billing_entity'][
            'sales_manager'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            InvoiceFormLocators.select2_sales_manager_container_id)

    def get_invoice_object_info(self):
        invoice_information['invoice_object'][
            'campaign'] = self.get_selected_value_of_modal_from_field(select_tag_id_or_class="",
                                                                      field_label_or_data_qa=InvoiceFormLocators.campaign_label)
        invoice_information['invoice_object'][
            'media_budget'] = self.get_text_using_tag_attribute(
            self.input_tag, self.class_attribute,
            InvoiceFormLocators.form_control_media_budget_class)
        invoice_information['invoice_object'][
            'channel_service'] = self.get_element_text(
            InvoiceFormLocators.channel_dropdown_locator)

    def get_invoice_total_media_budget_info(self):
        invoice_information['total_media_budget'][
            'total_media_budget_amount'] = self.get_text_using_tag_attribute(
            self.div_tag, self.class_attribute,
            InvoiceFormLocators.first_total_media_budget_class)
        invoice_information['total_media_budget'][
            'io_execution_comment'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            InvoiceFormLocators.select2_io_execution_comment_id_container_id)
        invoice_information['total_media_budget'][
            'notes'] = self.get_value_from_specific_input_field(InvoiceFormLocators.notes_label, is_textarea=True)

    def get_invoice_billing_information(self):
        invoice_information['billing_information'][
            'currency'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            InvoiceFormLocators.select2_currency_container_id)
        invoice_information['billing_information'][
            'use_notice_text_on_invoice_checkbox_status'] = \
            self.get_checkbox_status(InvoiceFormLocators.use_notice_text_on_invoice_label, value="1")
        self.click_on_element(
            InvoiceFormLocators.payment_details_section_locator)
        invoice_information['billing_information'][
            'currency_rate'] = self.get_value_from_specific_input_field(InvoiceFormLocators.currency_rate_label)
        invoice_information['billing_information'][
            'vat'] = self.get_value_from_specific_input_field(InvoiceFormLocators.vat_label)
        invoice_information['billing_information'][
            'discount'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            InvoiceFormLocators.discount_name)
        invoice_information['billing_information'][
            'invoice_object'] = self.get_attribute_value(
            InvoiceFormLocators.invoice_object_dropdown_selected_item_locator,
            self.title_attribute)
        invoice_information['billing_information'][
            'payment_term_days'] = self.get_value_from_specific_input_field(InvoiceFormLocators.payment_term_days_label)

    def calculate_and_verify_vat_discount_and_total_amount_from_ui(self,
                                                                   invoice_edit_data):
        total_media_budget = float(
            invoice_edit_data['total_media_budget'][
                'total_media_budget_amount'])
        expected_discount_percentage = float(
            invoice_edit_data['billing_information']['discount'])
        expected_vat_percentage = float(
            invoice_edit_data['billing_information']['vat'])
        expected_discount_amount = (
                                           total_media_budget * expected_discount_percentage) / 100
        expected_vat_amount = (
                                      total_media_budget * expected_vat_percentage) / 100
        time.sleep(5)
        ui_base_amount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.base_amount_label)
        ui_discount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.discount_label)
        ui_vat = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.vat_label)
        ui_total_amount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.total_amount_label)

        ui_base_amount_1 = ui_base_amount.split("$")
        actual_base_amount = float(ui_base_amount_1[1])
        ui_discount_1 = ui_discount.split("$")
        actual_discount = float(ui_discount_1[1])
        ui_vat_1 = ui_vat.split("$")
        actual_vat = float(ui_vat_1[1])
        ui_total_amount_1 = ui_total_amount.split("$")
        actual_total_amount = float(ui_total_amount_1[1])

        calculated_total_amount = actual_base_amount - actual_discount + actual_vat

        if expected_discount_amount == actual_discount and expected_vat_amount == actual_vat and \
                calculated_total_amount == actual_total_amount:
            return True
        else:
            return False

    def add_payment_into_invoice(self, payment_data):
        self.click_on_specific_button(InvoiceFormLocators.add_payment_button,
                                      locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
        time.sleep(2)
        self.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, payment_data[
            'payment_information']['amount_paid'])
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.id_attribute,
                                          InvoiceFormLocators.paid_vat_id,
                                          payment_data[
                                              'payment_information'][
                                              'vat'])
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.id_attribute,
                                          InvoiceFormLocators.paid_charges_id,
                                          payment_data[
                                              'payment_information'][
                                              'bank_charges'])
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.id_attribute,
                                          InvoiceFormLocators.paid_taxes_id,
                                          payment_data[
                                              'payment_information'][
                                              'taxes'])
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.id_attribute,
                                          InvoiceFormLocators.paid_rebate_id,
                                          payment_data[
                                              'payment_information'][
                                              'rebate'])
        self.click_on_specific_button(InvoiceFormLocators.save_button)

    def get_payment_data(self, table_number="1", row_number="1"):
        self.reset_payment_information()
        self.click_on_element(
            InvoiceFormLocators.totals_and_payments_group_locator)
        time.sleep(1)
        amount_paid = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.paid_amount_label, table_number,
            row_number)
        vat = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.vat_2_label, table_number,
            row_number)
        bank_charges = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.bank_charges_2_label, table_number,
            row_number)
        tax = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.tax_label, table_number,
            row_number)
        discount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.discount_label, table_number,
            row_number)
        total = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.total_label, table_number,
            row_number)
        balance = self.get_element_text(
            InvoiceFormLocators.balance_field_locator)
        status = self.get_element_text(
            InvoiceFormLocators.status_locator)

        amount_paid_1 = amount_paid.split("$")
        actual_amount_paid = amount_paid_1[1]
        vat_1 = vat.split("$")
        actual_vat = vat_1[1]
        bank_charges_1 = bank_charges.split("$")
        actual_bank_charges = bank_charges_1[1]
        tax_1 = tax.split("$")
        actual_tax = tax_1[1]
        discount_1 = discount.split("$")
        actual_discount = discount_1[1]
        total_1 = total.split("$")
        actual_total = total_1[1]
        balance_1 = balance.split("$")
        actual_balance = balance_1[1]

        payment_information['payment_information'][
            'amount_paid'] = actual_amount_paid
        payment_information['payment_information']['vat'] = actual_vat
        payment_information['payment_information'][
            'bank_charges'] = actual_bank_charges
        payment_information['payment_information'][
            'taxes'] = actual_tax
        payment_information['payment_information'][
            'rebate'] = actual_discount
        payment_information['payment_information'][
            'total'] = actual_total
        payment_information['payment_information'][
            'balance'] = actual_balance
        payment_information['payment_information']['status'] = status
        return payment_information

    def get_payments_grid_column_index(self, div_id, column_name,
                                       table_number="1"):
        index = 0
        locators = (By.XPATH,
                    "//div[@id='" + div_id + "']//thead[" + table_number + "]//tr[1]//th")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        for index in range(len(elements)):
            column_locator = (By.XPATH,
                              "//div[@id='" + div_id + "']//thead[" + table_number + "]//tr[1]//th[" + str(
                                  index + 1) + "]")
            if self.get_element_text(
                    column_locator) == column_name:
                index = index + 1
                break
        return index

    def get_value_from_payments_grid_column(self, div_id, column_name,
                                            table_number="1",
                                            row_number="1"):
        index = self.get_payments_grid_column_index(div_id,
                                                    column_name,
                                                    table_number)
        locator = (
            By.XPATH,
            "//div[@id='" + div_id + "']//tbody[" + table_number + "]//tr[" + row_number + "]//td[" + str(
                index) + "]")
        value = self.get_element_text(locator)
        return str(value)

    def get_payment_data_after_credit_note(self):
        self.reset_payment_information()
        amount_paid = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.paid_amount_label, "2",
            "1")
        vat = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.vat_2_label, "2", "1")
        bank_charges = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.bank_charges_2_label, "2",
            "1")
        tax = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.tax_label, "2", "1")
        discount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.discount_label, "2", "1")
        total = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.total_label, "2", "1")
        credit = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.credit_label, "2", "1")

        second_paid_amount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.paid_amount_label, "2",
            "2")
        second_vat = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.vat_2_label, "2", "2")
        second_bank_charges = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.bank_charges_2_label, "2",
            "2")
        second_tax = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.tax_label, "2", "2")
        second_discount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.discount_label, "2", "2")
        second_total = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.total_label, "2", "2")
        second_credit = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.credit_label, "2", "2")

        total_paid_amount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.paid_amount_label, "2",
            "3")
        total_vat = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.vat_2_label, "2", "3")
        total_bank_charges = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.bank_charges_2_label, "2",
            "3")
        total_tax = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.tax_label, "2", "3")
        total_discount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.discount_label, "2", "3")
        total_amount = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.total_label, "2", "3")
        total_credit = self.get_value_from_payments_grid_column(
            InvoiceFormLocators.form_step_box_i_6_div_id,
            InvoiceFormLocators.credit_label, "2", "3")

        balance = self.get_element_text(
            InvoiceFormLocators.balance_field_2_locator)

        payment_information['payment_information'][
            'paid_amount'] = amount_paid
        payment_information['payment_information']['vat'] = vat
        payment_information['payment_information'][
            'bank_charges'] = bank_charges
        payment_information['payment_information']['tax'] = tax
        payment_information['payment_information'][
            'discount'] = discount
        payment_information['payment_information']['total'] = total
        payment_information['payment_information']['credit'] = credit

        payment_information['payment_information'][
            'second_paid_amount'] = second_paid_amount
        payment_information['payment_information'][
            'second_vat'] = second_vat
        payment_information['payment_information'][
            'second_bank_charges'] = second_bank_charges
        payment_information['payment_information'][
            'second_tax'] = second_tax
        payment_information['payment_information'][
            'second_discount'] = second_discount
        payment_information['payment_information'][
            'second_total'] = second_total
        payment_information['payment_information'][
            'second_credit'] = second_credit

        payment_information['payment_information'][
            'total_paid_amount'] = total_paid_amount
        payment_information['payment_information'][
            'total_vat'] = total_vat
        payment_information['payment_information'][
            'total_bank_charges'] = total_bank_charges
        payment_information['payment_information'][
            'total_tax'] = total_tax
        payment_information['payment_information'][
            'total_discount'] = total_discount
        payment_information['payment_information'][
            'total_amount'] = total_amount
        payment_information['payment_information'][
            'total_credit'] = total_credit

        payment_information['payment_information']['balance'] = balance
        return payment_information

    def provide_invoice_data_for_multi_io_and_save(self, second_io_name,
                                                   invoice_data):
        self.select_from_modal(second_io_name, InvoiceFormLocators.select_io_label, click_uncheck_all=False)
        time.sleep(self.TWO_SEC_DELAY)
        self.set_value_into_element(
            InvoiceFormLocators.media_budget_field_locator.format(
                2),
            invoice_data['invoice_info'][
                'media_budget_for_second_io'],
            locator_initialization=True)
        time.sleep(self.TWO_SEC_DELAY)
        self.select_dropdown_value(InvoiceFormLocators.io_execution_comment_label,
                                   invoice_data['invoice_info']['io_execution_comment'])
        self.click_on_element(
            InvoiceFormLocators.billing_information_group_locator)
        self.click_on_element(
            InvoiceFormLocators.payment_details_section_locator)
        self.click_on_element(
            InvoiceFormLocators.buttons_group_locator)
        self.set_value_into_specific_input_field(InvoiceFormLocators.vat_label, invoice_data['invoice_info'][
            'vat'], tab_out=True)
        self.set_value_into_element(
            InvoiceFormLocators.discount_field_locator,
            invoice_data['invoice_info']['discount'])
        if self.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
            self.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                       'Client requested invoice early')
        self.click_on_save_and_generate_invoice_button(
            locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
        self.wait_for_visibility_of_element(
            InvoiceFormLocators.success_message_locator)
        return self.driver.current_url

    def get_payment_table_specific_row_and_column_data(self, table_no,
                                                       column_name,
                                                       row_number):
        index = 0
        column_names_locator = (
            By.XPATH,
            "//div[@id='form-step-box-i-6']//table[" + str(
                table_no) + "]//thead[" + str(
                table_no) + "]//tr//th")
        columns_elements = self.wait_for_presence_of_all_elements_located(
            column_names_locator)
        for element in columns_elements:
            column = element.text
            if column_name.lower() == column.lower():
                index = columns_elements.index(element)
                index = index + 1
                break
        column_value_locator = (By.XPATH,
                                "//div[@id='form-step-box-i-6']//table[" + str(
                                    table_no) + "]//tbody[" + str(
                                    table_no) + "]//tr[" + str(
                                    row_number) + "]//td[" + str(
                                    index) + "]")
        return self.get_element_text(column_value_locator)

    def get_invoice_information_from_gui_for_multi_io(self, invoice_data,
                                                      second_invoice=False):
        gui_invoice_data = copy.deepcopy(invoice_data)

        if second_invoice is False:
            gui_invoice_data['invoice_info'][
                'actual_media_budget_for_third_io_first_invoice'] = self.get_element_text(
                InvoiceFormLocators.media_budget_actual_amount_locator.format(
                    1), locator_initialization=True)
        elif second_invoice:
            gui_invoice_data['invoice_info'][
                'actual_media_budget_for_first_io_second_invoice'] = self.get_element_text(
                InvoiceFormLocators.media_budget_actual_amount_locator.format(
                    1), locator_initialization=True)

        gui_invoice_data['invoice_info'][
            'actual_media_budget_for_second_io'] = self.get_element_text(
            InvoiceFormLocators.media_budget_actual_amount_locator.format(
                2),
            locator_initialization=True)
        gui_invoice_data['invoice_info']['base_amount'] = \
            self.get_payment_table_specific_row_and_column_data(1,
                                                                "Base amount",
                                                                1)
        gui_invoice_data['invoice_info']['discount_in_payment'] = \
            self.get_payment_table_specific_row_and_column_data(1,
                                                                "Discount",
                                                                1)
        gui_invoice_data['invoice_info']['vat_in_payment'] = \
            self.get_payment_table_specific_row_and_column_data(1,
                                                                "VAT",
                                                                1)
        gui_invoice_data['invoice_info']['total_amount_in_payment'] = \
            self.get_payment_table_specific_row_and_column_data(1,
                                                                "Total amount",
                                                                1)
        return gui_invoice_data

    def get_text_from_specific_media_budget_table(self, tr_id,
                                                  td_class_attribute_value,
                                                  row_number=1):
        locator = (
            By.XPATH,
            "(//tr[@id='" + tr_id + "']//td[@class='" + td_class_attribute_value + "'])[" + str(
                row_number) + "]")
        time.sleep(self.TWO_SEC_DELAY)
        text = self.wait_for_presence_of_element(locator).text
        return text

    @staticmethod
    def reset_invoice_information():
        global invoice_information
        invoice_information = {'invoice_main_information': {},
                               'client_profile': {},
                               'billing_entity': {},
                               'invoice_object': {},
                               'total_media_budget': {},
                               'billing_information': {}}

    @staticmethod
    def reset_payment_information():
        global payment_information
        payment_information = {'payment_information': {}}

    def click_on_save_and_generate_invoice_button(self,
                                                  time_out=20,
                                                  max_retries=3,
                                                  locator_to_be_appeared=None):
        retries = 0
        wait_time = 20
        while retries < max_retries:
            try:
                self.click_on_element(InvoiceFormLocators.buttons_group_locator)
                if retries > 0:
                    element = self.wait_for_presence_of_element(
                        InvoiceFormLocators.save_and_generate_invoice_button_data_qa,
                        time_out=wait_time)
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    self.wait_for_presence_of_element(InvoiceFormLocators.save_and_generate_invoice_button_data_qa,
                                                      time_out=wait_time)
                    if 'http://rtb.local/admin' in self.driver.current_url:
                        time.sleep(1)
                        self.scroll_into_view(InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
                        time.sleep(1)
                    self.wait_for_element_to_be_clickable(
                        InvoiceFormLocators.save_and_generate_invoice_button_data_qa).click()
                time.sleep(self.ONE_SEC_DELAY)
                if self.is_alert_popup_available(1):
                    self.accept_alert()

                cancel_button_locator = (By.XPATH, "//button[@data-bb-handler='Cancel']")
                if self.is_element_present(cancel_button_locator, time_out=1):
                    self.click_on_element(cancel_button_locator)

                ignore_button_locator = (By.XPATH, "//button[@data-bb-handler='cancel']")
                if self.is_element_present(ignore_button_locator, time_out=1):
                    self.click_on_element(ignore_button_locator)

                if locator_to_be_appeared is not None:
                    if '//' in locator_to_be_appeared[1] or By.ID == locator_to_be_appeared[0]:
                        formed_locator_to_be_appeared = locator_to_be_appeared
                    else:
                        formed_locator_to_be_appeared = (By.XPATH, "//*[@data-qa='" + locator_to_be_appeared + "']")
                    WebDriverWait(self.driver, timeout=time_out, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            formed_locator_to_be_appeared))
                return
            except TimeoutException:
                retries += 1

    def navigate_to_specific_invoice_and_update_date_and_media_budget(self, config, invoice_ids, db_connection):
        for invoice_id in invoice_ids:
            total_invoice_amount = IoUtils.pull_total_invoice_amount(invoice_id, db_connection)
            if total_invoice_amount != 0:
                invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
                    invoice_id)
                self.driver.get(invoice_form_url)
                if self.is_alert_popup_available(self.ONE_SEC_DELAY):
                    self.accept_alert()
                self.click_on_element(
                    InvoiceFormLocators.date_field_locator)
                self.wait_for_presence_of_element(
                    InvoiceFormLocators.date_field_locator).send_keys(
                    Keys.COMMAND + 'a')
                time.sleep(self.ONE_SEC_DELAY)
                self.wait_for_presence_of_element(
                    InvoiceFormLocators.date_field_locator).send_keys(
                    Keys.DELETE)
                time.sleep(self.ONE_SEC_DELAY)
                element = self.wait_for_presence_of_element(InvoiceFormLocators.date_field_locator)
                self.driver.execute_script("arguments[0].value = arguments[1]", element,
                                           self.get_specific_date_with_specific_format(
                                               "%d %b, %Y",
                                               days_to_subtract=120))
                media_budgets_expand_icon_statuses = self.wait_for_presence_of_all_elements_located(
                    InvoiceFormLocators.media_budgets_expand_icon_statues_locator)
                for media_budgets_expand_icon_status in media_budgets_expand_icon_statuses:
                    index_num = media_budgets_expand_icon_statuses.index(media_budgets_expand_icon_status)
                    if index_num == 0:
                        start_date = self.get_specific_date_with_specific_format("%d %b, %Y", days_to_subtract=120)
                        end_date = self.get_specific_date_with_specific_format("%d %b, %Y", days_to_subtract=100)
                        period = start_date + ' - ' + end_date
                        if self.get_attribute_value(
                                InvoiceFormLocators.media_budgets_expand_icon_status_locator.format(str(
                                    index_num + 1)), attribute_name='data-toggle',
                                locator_initialization=True) == 'collapse':
                            self.click_on_element(InvoiceFormLocators.media_budgets_expand_icon_locator.format(str(
                                index_num + 1)), locator_initialization=True,
                                locator_to_be_appeared=InvoiceFormLocators.period_locator)
                            time.sleep(self.ONE_SEC_DELAY)
                        self.set_value_into_element(
                            InvoiceFormLocators.media_budget_locators.format(str(index_num + 1)),
                            '0',
                            locator_initialization=True)
                        self.set_value_into_element(InvoiceFormLocators.period_locators.format(str(index_num + 1)),
                                                    period,
                                                    locator_initialization=True)
                    else:
                        self.click_on_element(InvoiceFormLocators.media_budget_remove_locators.format(str(2)),
                                              locator_initialization=True)
                self.select_dropdown_value(InvoiceFormLocators.io_execution_comment_label,
                                           'E: Performance evaluation')
                if self.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
                    self.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                               'Client requested invoice early')
                self.click_on_save_and_generate_invoice_button(
                    locator_to_be_appeared=InvoiceFormLocators.success_message_locator)

    def navigate_to_specific_invoice_and_add_country(self, config, invoice_ids, country_list):
        for invoice_id in invoice_ids:
            invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
                invoice_id)
            self.driver.get(invoice_form_url)
            if self.is_alert_popup_available(self.ONE_SEC_DELAY):
                self.accept_alert()
            country_list_ui = self.get_specific_media_table_column_data_from_invoice(
                InvoiceFormLocators.country_row_info_data_qa)
            expected_country_list = list(set(country_list_ui))
            expected_country_list = sorted(expected_country_list)

            if expected_country_list != country_list:
                media_budgets_expand_icon_statuses = self.wait_for_presence_of_all_elements_located(
                    InvoiceFormLocators.media_budgets_expand_icon_statues_locator)

                if (len(country_list) - len(media_budgets_expand_icon_statuses)) >= 0:
                    media_budget_to_add = len(country_list) - len(media_budgets_expand_icon_statuses)
                    for add_count in range(1, media_budget_to_add + 1):
                        self.click_on_element(InvoiceFormLocators.media_budget_first_plus_button_locator)

                for country in country_list:
                    index_num = country_list.index(country)
                    if self.get_attribute_value(
                            InvoiceFormLocators.media_budgets_expand_icon_status_locator.format(str(
                                index_num + 1)), attribute_name='data-toggle',
                            locator_initialization=True) == 'collapse':
                        self.click_on_element(InvoiceFormLocators.media_budgets_expand_icon_locator.format(str(
                            index_num + 1)), locator_initialization=True,
                            locator_to_be_appeared=InvoiceFormLocators.period_locator)
                        time.sleep(self.ONE_SEC_DELAY)
                        self.select_dropdown_value(InvoiceFormLocators.country_select_data_qa.format(str(
                            index_num + 1)), country, index=(index_num + 1))
                if self.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
                    self.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                               'Client requested invoice early')
                self.click_on_save_and_generate_invoice_button(
                    locator_to_be_appeared=InvoiceFormLocators.success_message_locator)

    def get_specific_media_table_column_data_from_invoice(self, column_data_qa):
        data_list = []
        locators = (By.XPATH, "//*[@data-qa='" + column_data_qa + "']")
        elements = self.wait_for_presence_of_all_elements_located(locators)
        for element in elements:
            data_list.append(element.text)
        return data_list

    def get_country_wise_total_media_budget_from_invoice(self):
        data_dict = {}
        country_locators = (By.XPATH, "//*[@data-qa='" + InvoiceFormLocators.country_row_info_data_qa + "']")
        country_elements = self.wait_for_presence_of_all_elements_located(country_locators)
        media_budget_locators = (By.XPATH, "//*[@data-qa='" + InvoiceFormLocators.media_budget_info_data_qa + "']")
        media_budget_elements = self.wait_for_presence_of_all_elements_located(media_budget_locators)
        for country_element in country_elements:
            key = country_element.text
            if key not in data_dict:
                data_dict[key] = []
            index = country_elements.index(country_element)
            data_dict[country_element.text].append(media_budget_elements[index].text)

        for country, values in data_dict.items():
            data_dict[country] = [round(float(value.replace(',', '')), 2) for value in values]

        total_data = {country: sum(values) for country, values in data_dict.items()}
        return total_data
