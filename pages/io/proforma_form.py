import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.common import NoSuchElementException

from configurations.generic_modules import step_printer
from locators.io.proforma_form_locator import ProformaFormLocators
from pages.base_page import BasePage

proforma_information = {'proforma_main_information': {}, 'client_profile': {},
                        'billing_entity': {},
                        'proforma_object': {}, 'total_media_budget': {},
                        'billing_information': {}}


class DspDashboardProformaForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_proforma_data_and_save(self, proforma_data,
                                       edit_proforma=False):
        step_printer("PROFORMA_MAIN_INFORMATION")
        self.provide_proforma_main_information(proforma_data)

        step_printer("PROFORMA_CLIENT_PROFILE")
        self.provide_proforma_client_profile_info(proforma_data,
                                                  edit_proforma)

        if edit_proforma:
            step_printer("PROFORMA_BILLING_ENTITY")
            self.provide_proforma_billing_entity_info(
                proforma_data)

        step_printer("PROFORMA_OBJECT")
        self.provide_proforma_object_info(proforma_data, edit_proforma)

        step_printer('PROFORMA_TOTAL_MEDIA_BUDGET')
        self.provide_proforma_total_media_budget_info(proforma_data)

        step_printer('PROFORMA_BILLING_INFORMATION')
        self.provide_proforma_billing_information(proforma_data)

    def provide_proforma_main_information(self, proforma_data):
        self.set_value_into_specific_input_field(ProformaFormLocators.proforma_title_data_qa,
                                                 proforma_data['proforma_main_information'][
                                                     'proforma_title'])

    def provide_proforma_client_profile_info(self, proforma_data,
                                             edit_proforma=False):
        if edit_proforma:
            self.set_value_into_specific_input_field(ProformaFormLocators.email_data_qa,
                                                     proforma_data['client_profile']['email'])
            self.set_value_into_specific_input_field(ProformaFormLocators.contact_data_qa,
                                                     proforma_data['client_profile']['contact'])
        else:
            self.select_dropdown_value(ProformaFormLocators.client_data_qa, proforma_data['client_profile'][
                'client'])
            time.sleep(self.FIVE_SEC_DELAY)

    def provide_proforma_billing_entity_info(self, proforma_data):
        self.select_dropdown_value(ProformaFormLocators.sales_manager_data_qa, proforma_data['billing_entity'][
            'sales_manager'])
        time.sleep(self.TWO_SEC_DELAY)

    def provide_proforma_object_info(self, proforma_data,
                                     edit_proforma=False):
        self.select_from_modal(proforma_data['proforma_object']['campaign'], ProformaFormLocators.campaign_data_qa)
        time.sleep(self.TWO_SEC_DELAY)
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.data_qa_attribute,
                                          ProformaFormLocators.form_control_media_budget_data_qa,
                                          proforma_data[
                                              'proforma_object'][
                                              'media_budget'])
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(
            ProformaFormLocators.channel_dropdown_locator)
        self.set_value_into_element(
            ProformaFormLocators.channel_text_field_locator,
            proforma_data['proforma_object'][
                'channel_service'] + Keys.ENTER)
        if not edit_proforma:
            self.select_dropdown_value(ProformaFormLocators.country_data_qa, proforma_data['proforma_object'][
                'country'])

    def provide_proforma_total_media_budget_info(self, proforma_data):
        self.set_value_into_specific_input_field(ProformaFormLocators.notes_data_qa,
                                                 proforma_data['total_media_budget']['notes'], True)
        self.select_dropdown_value(ProformaFormLocators.io_execution_comment_data_qa,
                                   proforma_data['total_media_budget'][
                                       'io_execution_comment'])

    def provide_proforma_billing_information(self, proforma_data):
        self.select_dropdown_value(ProformaFormLocators.currency_data_qa, proforma_data[
            'billing_information'][
            'currency'])
        self.select_dropdown_value(ProformaFormLocators.invoice_status_data_qa, proforma_data['billing_information'][
            'invoice_status'])
        is_expand = self.get_attribute_value(
            ProformaFormLocators.billing_info_dropdown_locator,
            "aria-expanded")
        if is_expand == 'false':
            self.click_on_element(
                ProformaFormLocators.billing_info_dropdown_locator)
        self.set_value_into_specific_input_field(ProformaFormLocators.vat_data_qa,
                                                 proforma_data['billing_information']['vat'])
        self.set_value_into_element(
            ProformaFormLocators.discount_field_locator,
            proforma_data['billing_information']['discount'])
        self.select_dropdown_value(ProformaFormLocators.invoice_object_data_qa, proforma_data['billing_information'][
            'invoice_object'])
        self.click_on_save_and_generate_proforma_button(
            locator_to_be_appeared=ProformaFormLocators.success_message_locator)
        self.wait_for_visibility_of_element(
            ProformaFormLocators.success_message_locator)

    def get_success_message(self):
        return self.get_element_text(
            ProformaFormLocators.success_message_locator)

    def get_proforma_information_from_gui(self, proforma_data):
        self.reset_proforma_information()
        time.sleep(self.TWO_SEC_DELAY)
        self.get_proforma_main_information(proforma_data)
        self.get_proforma_client_profile_info()
        self.get_proforma_billing_entity_info()
        self.get_proforma_object_info()
        self.get_proforma_total_media_budget_info()
        self.get_proforma_billing_information()
        return proforma_information

    def get_proforma_main_information(self, proforma_data):
        locator = (By.XPATH, "//input[@value='" +
                   proforma_data['proforma_main_information'][
                       'proforma_title'] + "']")
        self.wait_for_visibility_of_element(locator)
        proforma_information['proforma_main_information'][
            'proforma_title'] = self.get_value_from_specific_input_field(ProformaFormLocators.proforma_title_data_qa)

    def get_proforma_client_profile_info(self):
        proforma_information['client_profile'][
            'client'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            ProformaFormLocators.select2_client_container_id)
        proforma_information['client_profile'][
            'email'] = self.get_value_from_specific_input_field(ProformaFormLocators.email_data_qa)
        proforma_information['client_profile'][
            'contact'] = self.get_value_from_specific_input_field(ProformaFormLocators.contact_data_qa)

    def get_proforma_billing_entity_info(self):
        proforma_information['billing_entity'][
            'company_profile'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            ProformaFormLocators.select2_company_profile_container_id)
        proforma_information['billing_entity'][
            'sales_manager'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            ProformaFormLocators.select2_sales_manager_container_id)

    def get_proforma_object_info(self):
        proforma_information['proforma_object'][
            'campaign'] = self.get_selected_value_of_modal_from_field(select_tag_id_or_class="",
                                                                      field_label_or_data_qa=ProformaFormLocators.campaign_data_qa)
        proforma_information['proforma_object'][
            'media_budget'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            ProformaFormLocators.form_control_media_budget_data_qa)
        proforma_information['proforma_object'][
            'channel_service'] = self.get_element_text(
            ProformaFormLocators.channel_dropdown_locator)
        proforma_information['proforma_object'][
            'country'] = self.get_text_using_tag_attribute(
            self.td_tag, self.data_qa_attribute,
            ProformaFormLocators.country_row_data_qa)
        proforma_information['proforma_object'][
            'campaign_type'] = self.get_text_using_tag_attribute(
            self.td_tag, self.data_qa_attribute,
            ProformaFormLocators.campaign_type_data_qa)

    def get_proforma_total_media_budget_info(self):
        proforma_information['total_media_budget'][
            'total_media_budget_amount'] = self.get_text_using_tag_attribute(
            self.div_tag, self.data_qa_attribute,
            ProformaFormLocators.first_total_media_budget_data_qa)
        proforma_information['total_media_budget'][
            'io_execution_comment'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            ProformaFormLocators.select2_io_execution_comment_id_container_id)
        proforma_information['total_media_budget'][
            'notes'] = self.get_value_from_specific_input_field(ProformaFormLocators.notes_data_qa, is_textarea=True)

    def get_proforma_billing_information(self):
        proforma_information['billing_information'][
            'currency'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            ProformaFormLocators.select2_currency_container_id)
        proforma_information['billing_information'][
            'invoice_status'] = self.get_element_text(
            ProformaFormLocators.invoice_status_selected_item_locator)
        self.click_on_element(
            ProformaFormLocators.payment_details_section_locator)
        proforma_information['billing_information'][
            'currency_rate'] = self.get_value_from_specific_input_field(ProformaFormLocators.currency_rate_data_qa)
        proforma_information['billing_information'][
            'vat'] = self.get_value_from_specific_input_field(ProformaFormLocators.vat_data_qa)
        proforma_information['billing_information'][
            'discount'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            ProformaFormLocators.discount_data_qa)
        proforma_information['billing_information'][
            'invoice_object'] = self.get_attribute_value(
            ProformaFormLocators.invoice_object_dropdown_selected_item_locator,
            self.title_attribute)
        proforma_information['billing_information'][
            'payment_term_days'] = self.get_value_from_specific_input_field(
            ProformaFormLocators.payment_term_days_data_qa)

    @staticmethod
    def reset_proforma_information():
        global proforma_information
        proforma_information = {'proforma_main_information': {},
                                'client_profile': {},
                                'billing_entity': {},
                                'proforma_object': {},
                                'total_media_budget': {},
                                'billing_information': {}}

    def click_on_save_and_generate_proforma_button(self,
                                                   time_out=20,
                                                   max_retries=3,
                                                   locator_to_be_appeared=None):
        retries = 0
        wait_time = 20
        while retries < max_retries:
            try:
                self.click_on_element(ProformaFormLocators.buttons_group_locator)
                if retries > 0:
                    element = self.wait_for_presence_of_element(
                        ProformaFormLocators.save_and_generate_proforma_button_data_qa,
                        time_out=wait_time)
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    self.wait_for_presence_of_element(ProformaFormLocators.save_and_generate_proforma_button_data_qa,
                                                      time_out=wait_time)
                    if 'http://rtb.local/admin' in self.driver.current_url:
                        time.sleep(1)
                        self.scroll_into_view(ProformaFormLocators.save_and_generate_proforma_button_data_qa)
                        time.sleep(1)
                    self.wait_for_element_to_be_clickable(
                        ProformaFormLocators.save_and_generate_proforma_button_data_qa).click()
                time.sleep(self.ONE_SEC_DELAY)
                try:
                    ignore_button = self.driver.find_element(By.XPATH, "//button[@data-bb-handler='cancel']")
                    ignore_button.click()
                except NoSuchElementException:
                    pass
                if locator_to_be_appeared is not None:
                    WebDriverWait(self.driver, timeout=time_out, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            locator_to_be_appeared))
                if self.is_alert_popup_available(1):
                    self.accept_alert()
                return
            except TimeoutException:
                retries += 1
