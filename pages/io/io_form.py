import copy
import re
import time
from datetime import datetime, timedelta

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from configurations.generic_modules import step_printer
from locators.io.io_form_locator import IoFormLocators
from pages.base_page import BasePage

io_information = {'io_main_information': {}, 'client_profile': {},
                  'billing_entity': {}, 'io_object': {},
                  'total_media_budget': {}, 'billing_information': {}}


class DspDashboardIoForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_io_data_and_save(self, io_data, edit_io=False):
        step_printer("IO_MAIN_INFORMATION")
        self.provide_io_main_information(io_data)

        step_printer("IO_CLIENT_PROFILE")
        self.provide_io_client_profile_info(io_data, edit_io)

        if edit_io:
            step_printer("IO_BILLING_ENTITY")
            self.provide_io_billing_entity_info(io_data)

        step_printer("IO_OBJECT")
        self.provide_io_object_info(io_data, edit_io)

        step_printer('IO_TOTAL_MEDIA_BUDGET')
        self.provide_io_total_media_budget_info(io_data)

        step_printer('IO_BILLING_INFORMATION')
        self.provide_io_billing_information(io_data)
        return self.driver.current_url

    def provide_multi_io_data_and_save(self, io_data, index):
        multi_io_information = copy.deepcopy(io_data)
        step_printer(
            "IO_MAIN_INFORMATION for the iteration: " + str(
                index) + "")
        self.provide_io_main_information(multi_io_information)
        if index == 1:
            self.click_on_element(
                IoFormLocators.date_field_data_qa)
            self.wait_for_presence_of_element(
                IoFormLocators.date_field_data_qa).send_keys(
                Keys.COMMAND + 'a')
            self.wait_for_presence_of_element(
                IoFormLocators.date_field_data_qa).send_keys(
                Keys.DELETE)
            self.set_value_into_specific_input_field(IoFormLocators.io_date_data_qa,
                                                     self.get_specific_date_with_specific_format(
                                                         "%d %b, %Y",
                                                         days_to_subtract=1), tab_out=True)

        step_printer("IO_CLIENT_PROFILE for the iteration: " + str(
            index) + "")
        self.provide_io_client_profile_info(multi_io_information)

        step_printer("IO_OBJECT for the iteration: " + str(index) + "")
        media_budget = multi_io_information['io_object'][
            'media_budget']
        final_media_budget = media_budget.split(",")
        multi_io_information['io_object']['media_budget'] = \
            final_media_budget[
                index].strip()
        self.provide_io_object_info_using_js(multi_io_information)

        step_printer(
            "IO_BILLING_INFORMATION for the iteration: " + str(
                index) + "")
        currency = multi_io_information['billing_information'][
            'currency']
        final_currency = currency.split(",")
        multi_io_information['billing_information']['currency'] = \
            final_currency[index].strip()
        self.provide_io_billing_information(multi_io_information,
                                            for_multi_io=True)
        return self.driver.current_url

    def provide_io_main_information(self, io_data):
        self.set_value_into_specific_input_field(IoFormLocators.io_title_input_data_qa, io_data[
            'io_main_information'][
            'io_title'])

    def provide_io_client_profile_info(self, io_data, edit_io=False):
        if edit_io:
            self.set_value_into_specific_input_field(IoFormLocators.email_input_data_qa,
                                                     io_data['client_profile']['email'])
            self.set_value_into_specific_input_field(IoFormLocators.contact_input_data_qa,
                                                     io_data['client_profile']['contact'])
        else:
            self.select_dropdown_value(IoFormLocators.client_select_data_qa, io_data['client_profile'][
                'client'])
            time.sleep(self.FIVE_SEC_DELAY)

    def provide_io_billing_entity_info(self, io_data):
        self.select_dropdown_value(IoFormLocators.sales_manager_select_data_qa, io_data['billing_entity'][
            'sales_manager'])
        time.sleep(self.TWO_SEC_DELAY)

    def provide_io_object_info(self, io_data, edit_io=False):
        self.select_from_modal(io_data['io_object']['campaign'], IoFormLocators.campaign_select_data_qa)
        time.sleep(self.TWO_SEC_DELAY)
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.data_qa_attribute,
                                          IoFormLocators.media_budget_input_data_qa.format("1"),
                                          io_data['io_object'][
                                              'media_budget'])
        time.sleep(self.TWO_SEC_DELAY)
        if edit_io:
            self.click_on_element(
                IoFormLocators.channel_dropdown_item_locator)
        else:
            self.click_on_element(
                IoFormLocators.channel_dropdown_locator)
        self.set_value_into_element(
            IoFormLocators.channel_text_field_locator,
            io_data['io_object'][
                'channel_service'] + Keys.ENTER)
        if not edit_io:
            self.select_dropdown_value(IoFormLocators.country_select_data_qa, io_data['io_object']['country'])

    def provide_io_object_info_using_js(self, io_data, edit_io=False):
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=IoFormLocators.campaign_select_data_qa,
            option_to_select=io_data['io_object']['campaign'])
        time.sleep(self.TWO_SEC_DELAY)
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.data_qa_attribute,
                                          IoFormLocators.media_budget_input_data_qa.format("1"),
                                          io_data['io_object'][
                                              'media_budget'])
        time.sleep(self.TWO_SEC_DELAY)
        if edit_io:
            self.click_on_element(
                IoFormLocators.channel_dropdown_item_locator)
        else:
            self.click_on_element(
                IoFormLocators.channel_dropdown_locator)
        self.set_value_into_element(
            IoFormLocators.channel_text_field_locator,
            io_data['io_object'][
                'channel_service'] + Keys.ENTER)
        if not edit_io:
            self.select_dropdown_value(IoFormLocators.country_select_data_qa, io_data['io_object']['country'])

    def provide_io_total_media_budget_info(self, io_data):
        self.set_value_into_specific_input_field(IoFormLocators.notes_textarea_data_qa, io_data['total_media_budget'][
            'notes'], True)
        self.select_dropdown_value(IoFormLocators.io_execution_comment_select_data_qa, io_data['total_media_budget'][
            'io_execution_comment'])

    def provide_io_billing_information(self, io_data, for_multi_io=False):
        if for_multi_io is False:
            self.select_specific_radio_button(
                io_data['billing_information'][
                    'invoice_payment_type'])
            self.select_dropdown_value(IoFormLocators.invoice_status_select_data_qa, io_data['billing_information'][
                'invoice_status'])
        self.select_dropdown_value(IoFormLocators.currency_select_data_qa, io_data['billing_information'][
            'currency'])
        time.sleep(2)
        if self.is_alert_popup_available(2):
            self.accept_alert()
        self.set_value_into_specific_input_field(IoFormLocators.vat_field_data_qa, io_data[
            'billing_information'][
            'vat'], tab_out=True)
        self.set_value_into_element(
            IoFormLocators.discount_field_data_qa,
            io_data['billing_information']['discount'])
        self.click_on_save_and_generate_io_button(
            locator_to_be_appeared=IoFormLocators.success_message_data_qa)
        self.wait_for_visibility_of_element(
            IoFormLocators.success_message_data_qa)

    def get_success_message(self):
        return self.get_element_text(
            IoFormLocators.success_message_data_qa)

    def get_io_information_from_gui(self, io_data):
        self.reset_io_information()
        time.sleep(self.TWO_SEC_DELAY)
        self.get_io_main_information(io_data)
        self.get_io_client_profile_info()
        self.get_io_billing_entity_info()
        self.get_io_object_info()
        self.get_io_total_media_budget_info()
        self.get_io_billing_information()
        return io_information

    def get_io_main_information(self, io_data):
        locator = (By.XPATH,
                   "//input[@value='" + io_data['io_main_information'][
                       'io_title'] + "']")
        self.wait_for_visibility_of_element(locator)
        io_information['io_main_information'][
            'io_title'] = self.get_value_from_specific_input_field(IoFormLocators.io_title_input_data_qa)

    def get_io_client_profile_info(self):
        io_information['client_profile'][
            'client'] = self.get_selected_options_using_js_code(IoFormLocators.client_select_data_qa)
        io_information['client_profile'][
            'email'] = self.get_value_from_specific_input_field(IoFormLocators.email_input_data_qa)
        io_information['client_profile'][
            'contact'] = self.get_value_from_specific_input_field(IoFormLocators.contact_input_data_qa)
        io_information['client_profile'][
            'responsible_adOps'] = self.get_selected_options_using_js_code(
            IoFormLocators.responsible_adops_input_data_qa)
        io_information['client_profile'][
            'client_company'] = self.get_selected_options_using_js_code(IoFormLocators.client_company_select_data_qa)

    def get_io_billing_entity_info(self):
        io_information['billing_entity'][
            'company_profile'] = self.get_selected_options_using_js_code(IoFormLocators.company_profile_select_data_qa)
        io_information['billing_entity'][
            'sales_manager'] = self.get_selected_options_using_js_code(IoFormLocators.sales_manager_select_data_qa)

    def get_io_object_info(self):
        io_information['io_object'][
            'campaign'] = self.get_selected_options_using_js_code(IoFormLocators.campaign_select_data_qa)
        io_information['io_object'][
            'media_budget'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            IoFormLocators.media_budget_input_data_qa.format("1"))
        io_information['io_object'][
            'channel_service'] = self.get_element_text(
            IoFormLocators.channel_dropdown_item_locator)
        io_information['io_object'][
            'country'] = self.get_text_using_tag_attribute(
            self.td_tag,
            self.data_qa_attribute,
            IoFormLocators.country_row_info_data_qa)
        io_information['io_object'][
            'campaign_type'] = self.get_text_using_tag_attribute(
            self.td_tag, self.data_qa_attribute,
            IoFormLocators.campaign_type_info_data_qa)

    def get_io_total_media_budget_info(self):
        io_information['total_media_budget'][
            'total_media_budget_amount'] = self.get_text_using_tag_attribute(
            self.div_tag, self.data_qa_attribute,
            IoFormLocators.total_media_budget_info_data_qa)
        io_information['total_media_budget'][
            'io_execution_comment'] = self.get_selected_options_using_js_code(
            IoFormLocators.io_execution_comment_select_data_qa)
        io_information['total_media_budget'][
            'notes'] = self.get_value_from_specific_input_field(IoFormLocators.notes_textarea_data_qa, is_textarea=True)

    def get_io_billing_information(self):
        io_information['billing_information'][
            'invoice_payment_type'] = self.get_element_text(
            IoFormLocators.payment_type_checked_radio_button_locator)
        io_information['billing_information'][
            'currency'] = self.get_selected_options_using_js_code(IoFormLocators.currency_select_data_qa)
        io_information['billing_information'][
            'invoice_status'] = self.get_text_or_value_from_single_selected_option(
            IoFormLocators.invoice_status_selected_item_data_qa)
        io_information['billing_information'][
            'send_feedback_after_io_closed_checkbox_status'] = \
            self.get_checkbox_status(IoFormLocators.send_feedback_after_io_closed_data_qa, value="1")
        io_information['billing_information'][
            'signed_io_checkbox_status'] = \
            self.get_checkbox_status(IoFormLocators.signed_io_check_data_qa, value="1")
        self.click_on_element(
            IoFormLocators.payment_details_section_data_qa, locator_to_be_appeared=IoFormLocators.vat_field_data_qa)
        io_information['billing_information'][
            'currency_rate'] = self.get_value_from_specific_input_field(IoFormLocators.currency_rate_label)
        io_information['billing_information'][
            'vat'] = self.get_value_from_specific_input_field(IoFormLocators.vat_field_data_qa)
        io_information['billing_information'][
            'discount'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            IoFormLocators.discount_field_data_qa)
        io_information['billing_information'][
            'payment_term_days'] = self.get_value_from_specific_input_field(
            IoFormLocators.payment_term_days_input_data_qa)

    def get_specific_finance_profile_status(self, label_or_data_qa):
        locator = (
            By.XPATH, "//li[contains(text(), '" + label_or_data_qa + "')] | //li[@data-qa='" + label_or_data_qa + "']")
        text = self.get_element_text(locator)
        fin_text = text.split(":")
        return fin_text[1].strip()

    def click_on_specific_form_nav_option(self, option_name):
        locator = (
            By.XPATH,
            "//a[normalize-space()='" + option_name + "']")
        self.click_on_element(locator,
                              click_on_presence_of_element=True)

    def get_text_from_specific_media_budget_table(self, tr_id,
                                                  td_class_or_data_qa_attribute_value,
                                                  row_number=1):
        locator = (
            By.XPATH,
            "(//tr[@id='" + tr_id + "']//td[@data-qa='" + td_class_or_data_qa_attribute_value + "'])[" + str(
                row_number) + "]")
        text = self.wait_for_presence_of_element(locator).text
        return text

    def get_last_invoice_date(self, date_format):
        date_str = self.get_current_date_with_specific_format(
            date_format)
        date = datetime.strptime(date_str, date_format).date()
        if 1 <= date.day <= 5:
            today = datetime.today()
            first_day_of_month = today.replace(day=1)
            last_day_of_previous_month = first_day_of_month - timedelta(
                days=1)
            date1 = last_day_of_previous_month.strftime(
                date_format)
            return str(date1)
        else:
            return self.get_current_date_with_specific_format(
                date_format)

    @staticmethod
    def reset_io_information():
        global io_information
        io_information = {'io_main_information': {},
                          'client_profile': {},
                          'billing_entity': {}, 'io_object': {},
                          'total_media_budget': {},
                          'billing_information': {}}

    def get_selected_and_formatted_date(self, locator):
        class_name = self.get_attribute_value(locator, "class")
        date_match = re.search(r"d_(\d+)", class_name)
        selected_date = date_match.group(1)
        formatted_date = f"{selected_date[:4]}-{selected_date[4:6]}-{selected_date[6:]}"
        return formatted_date

    def get_specific_media_table_column_data(self, column_data_qa):
        data_list = []
        locators = (By.XPATH, "//*[@data-qa='" + column_data_qa + "']")
        elements = self.wait_for_presence_of_all_elements_located(locators)
        for element in elements:
            data_list.append(element.text)
        return data_list

    def get_country_wise_total_media_budget(self):
        data_dict = {}
        country_locators = (By.XPATH, "//*[@data-qa='" + IoFormLocators.country_row_info_data_qa + "']")
        country_elements = self.wait_for_presence_of_all_elements_located(country_locators)
        media_budget_locators = (By.XPATH, "//*[@data-qa='" + IoFormLocators.media_budget_info_data_qa + "']")
        media_budget_elements = self.wait_for_presence_of_all_elements_located(media_budget_locators)
        for country_element in country_elements:
            key = country_element.text
            if key not in data_dict:
                data_dict[key] = []
            index = country_elements.index(country_element)
            data_dict[country_element.text].append(media_budget_elements[index].text)

        for country, values in data_dict.items():
            data_dict[country] = [float(value.replace(',', '')) for value in values]

        total_data = {country: sum(values) for country, values in data_dict.items()}
        return total_data

    def click_on_save_and_generate_io_button(self,
                                             time_out=20,
                                             max_retries=3,
                                             locator_to_be_appeared=None):
        retries = 0
        wait_time = 20
        while retries < max_retries:
            try:
                self.click_on_element(IoFormLocators.buttons_group_data_qa)
                if retries > 0:
                    element = self.wait_for_presence_of_element(IoFormLocators.save_and_generate_io_button_data_qa,
                                                                time_out=wait_time)
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    self.wait_for_presence_of_element(IoFormLocators.save_and_generate_io_button_data_qa,
                                                      time_out=wait_time)
                    if 'http://rtb.local/admin' in self.driver.current_url:
                        time.sleep(1)
                        self.scroll_into_view(IoFormLocators.save_and_generate_io_button_data_qa)
                        time.sleep(1)
                    self.wait_for_element_to_be_clickable(
                        IoFormLocators.save_and_generate_io_button_data_qa).click()
                if self.is_alert_popup_available(self.ONE_SEC_DELAY):
                    self.accept_alert()

                ignore_button_locator = (By.XPATH, "//button[@data-bb-handler='cancel']")
                if self.is_element_present(ignore_button_locator, time_out=1):
                    self.click_on_element(ignore_button_locator)

                if self.is_alert_popup_available(self.ONE_SEC_DELAY):
                    self.accept_alert()
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

    def navigate_to_specific_io_and_update_date(self, config, io_ids):
        for io_id in io_ids:
            io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
            self.driver.get(io_form_url)
            if self.is_alert_popup_available(self.ONE_SEC_DELAY):
                self.accept_alert()
            self.click_on_element(
                IoFormLocators.date_field_data_qa)
            self.wait_for_presence_of_element(
                IoFormLocators.date_field_data_qa).send_keys(
                Keys.COMMAND + 'a')
            time.sleep(self.ONE_SEC_DELAY)
            self.wait_for_presence_of_element(
                IoFormLocators.date_field_data_qa).send_keys(
                Keys.DELETE)
            time.sleep(self.ONE_SEC_DELAY)
            element = self.wait_for_presence_of_element(IoFormLocators.date_field_data_qa)
            self.driver.execute_script("arguments[0].value = arguments[1]", element,
                                       self.get_specific_date_with_specific_format(
                                           "%d %b, %Y",
                                           days_to_subtract=120))
            self.click_on_save_and_generate_io_button(
                locator_to_be_appeared=IoFormLocators.success_message_data_qa)
