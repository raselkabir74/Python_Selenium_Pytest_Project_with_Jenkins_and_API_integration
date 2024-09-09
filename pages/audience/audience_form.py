import os
import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait

from configurations import generic_modules
from locators.audience.audience_form_locator import AudienceFormLocators
from pages.base_page import BasePage

behavioral_user_interest_audience_information = {'general_information': {}}
audience_group_audience_information = {'general_information': {}}
retargeting_apps_sites_visitors_audience_information = {'general_information': {}}
retargeting_geolocation_audience_information = {'general_information': {}}
retargeting_site_first_party_audience_information = {'general_information': {}}
user_ids_list_audience_information = {'general_information': {}}


class DspDashboardAudienceForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_behavioral_user_interest_audience_data_and_save(self,
                                                                audience_data):
        time.sleep(self.TWO_SEC_DELAY)
        self.set_value_into_specific_input_field(AudienceFormLocators.name_field_data_qa,
                                                 audience_data['general_information']['audience_name'])
        self.set_value_into_specific_input_field(AudienceFormLocators.description_field_data_qa,
                                                 audience_data['general_information']['description'], is_textarea=True)
        time.sleep(self.TWO_SEC_DELAY)
        self.select_dropdown_value(AudienceFormLocators.type_field_data_qa, audience_data['general_information'][
            'audience_type'])
        self.select_dropdown_value(AudienceFormLocators.country_field_data_qa, audience_data['general_information'][
            'country'])
        self.check_uncheck_specific_checkbox(audience_data['general_information']['verticals'], do_check=True)
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal(audience_data['general_information']['users'], AudienceFormLocators.users_field_data_qa,
                               is_delay='yes')
        self.scroll_to_specific_element(
            AudienceFormLocators.save_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(AudienceFormLocators.save_button_locator)

    def get_behavioral_user_interest_audience_information(self,
                                                          audience_data):
        debug_mode = "JENKINS_URL" not in os.environ
        self.reset_behavioral_user_interest_audience_information()
        behavioral_user_interest_audience_information[
            'general_information'][
            'audience_name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            AudienceFormLocators.audience_field_name_data_qa)
        behavioral_user_interest_audience_information[
            'general_information'][
            'description'] = self.get_text_using_tag_attribute(
            self.textarea_tag, self.data_qa_attribute,
            AudienceFormLocators.description_data_qa)
        behavioral_user_interest_audience_information[
            'general_information'][
            'audience_type'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.type_container_id)
        behavioral_user_interest_audience_information[
            'general_information'][
            'country'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.country_container_id)
        behavioral_user_interest_audience_information[
            'general_information'][
            'verticals'] = self.get_selected_checkbox_name_from_a_section(
            AudienceFormLocators.verticals_id,
            span_is_present=True)
        if debug_mode:
            behavioral_user_interest_audience_information[
                'general_information'][
                'users'] = self.get_selected_value_of_modal_from_field(AudienceFormLocators.form_control_class,
                                                                       AudienceFormLocators.users_field_data_qa)
        else:
            behavioral_user_interest_audience_information[
                'general_information'][
                'users'] = \
                audience_data['general_information']['users']
        self.scroll_to_specific_element(
            AudienceFormLocators.cancel_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        return behavioral_user_interest_audience_information

    def provide_audience_group_audience_data_and_save(self, audience_data):
        self.set_value_into_specific_input_field(AudienceFormLocators.name_field_data_qa,
                                                 audience_data['general_information']['audience_name'])
        self.set_value_into_specific_input_field(AudienceFormLocators.description_field_data_qa,
                                                 audience_data['general_information']['description'], is_textarea=True)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.type_field_data_qa,
            option_to_select=audience_data['general_information'][
                'audience_type'])
        self.select_dropdown_value(AudienceFormLocators.audience_list_field_name,
                                   audience_data['general_information']['audience_list'])
        self.click_on_element(AudienceFormLocators.add_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.users_field_data_qa,
            option_to_select=audience_data['general_information']['users'])
        self.scroll_to_specific_element(
            AudienceFormLocators.save_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(AudienceFormLocators.save_button_locator)

    def get_audience_group_audience_information(self):
        self.reset_audience_group_audience_information()
        audience_group_audience_information['general_information'][
            'audience_name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            AudienceFormLocators.audience_field_name_data_qa)
        audience_group_audience_information['general_information'][
            'description'] = self.get_text_using_tag_attribute(
            self.textarea_tag, self.data_qa_attribute,
            AudienceFormLocators.description_data_qa)
        audience_group_audience_information['general_information'][
            'audience_type'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.type_container_id)
        audience_group_audience_information['general_information'][
            'audience_list'] = self.get_element_text(
            AudienceFormLocators.selected_first_item_locator)
        audience_group_audience_information['general_information'][
            'users'] = self.get_selected_value_of_modal_from_field(AudienceFormLocators.form_control_class,
                                                                   AudienceFormLocators.users_field_data_qa)
        self.click_on_element(
            AudienceFormLocators.cancel_button_locator)
        return audience_group_audience_information

    def provide_retargeting_apps_sites_visitors_audience_data_and_save(
            self,
            audience_data,
            upload_csv=False):
        self.set_value_into_specific_input_field(AudienceFormLocators.name_field_data_qa,
                                                 audience_data['general_information']['audience_name'])
        self.set_value_into_specific_input_field(AudienceFormLocators.description_field_data_qa,
                                                 audience_data['general_information']['description'], is_textarea=True)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.type_field_data_qa,
            option_to_select=audience_data['general_information'][
                'audience_type'])
        self.select_specific_date_range(
            AudienceFormLocators.date_field_data_qa,
            "7 Days")
        self.select_dropdown_value(AudienceFormLocators.rule_field_data_qa, audience_data['general_information'][
            'rule'])
        self.set_value_into_specific_input_field(AudienceFormLocators.user_validity_field_data_qa,
                                                 audience_data['general_information']['user_validity'])
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.country_form_field_data_qa,
            option_to_select=audience_data['general_information']['country'])
        if upload_csv is False:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=AudienceFormLocators.exchange_field_data_qa,
                option_to_select=audience_data['general_information']['exchange'])
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=AudienceFormLocators.type_form_field_data_qa,
                option_to_select=audience_data['general_information']['type'])
        self.select_dropdown_value(AudienceFormLocators.generate_insights_report_field_data_qa,
                                   audience_data['general_information'][
                                       'generate_insights_report'])
        if upload_csv:
            self.wait_for_presence_of_element(
                AudienceFormLocators.csv_file_upload_locator).send_keys(
                os.path.join(os.getcwd(),
                             'assets/audiences/apps_sites_csv_file.csv'))
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.users_field_data_qa,
            option_to_select=audience_data['general_information']['users'])
        self.scroll_to_specific_element(
            AudienceFormLocators.save_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(AudienceFormLocators.save_button_locator)

    def get_retargeting_apps_sites_visitors_audience_information(self):
        self.reset_retargeting_apps_sites_visitors_audience_information()
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'audience_name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            AudienceFormLocators.audience_field_name_data_qa)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'description'] = self.get_text_using_tag_attribute(
            self.textarea_tag, self.data_qa_attribute,
            AudienceFormLocators.description_data_qa)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'audience_type'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.type_container_id)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'rule'] = self.get_text_or_value_from_selected_option(
            AudienceFormLocators.rule_field_data_qa)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'user_validity'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute,
            AudienceFormLocators.user_validity_minutes_id)
        retargeting_apps_sites_visitors_audience_information[
            'general_information']['user_validity_dropdown_vale'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              AudienceFormLocators.select2_validity_type_container_id)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'country'] = self.get_selected_value_of_modal_from_field(
            field_label_or_data_qa=AudienceFormLocators.country_form_field_data_qa)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'exchange'] = self.get_selected_value_of_modal_from_field(
            field_label_or_data_qa=AudienceFormLocators.exchange_field_data_qa, select_any_value=True)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'type'] = self.get_selected_value_of_modal_from_field(
            field_label_or_data_qa=AudienceFormLocators.type_form_field_data_qa, select_any_value=True)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'selected_apps_sites'] = self.is_multiple_apps_sites_selected()
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'generate_insights_report'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.select2_generate_insight_form_container_id)
        retargeting_apps_sites_visitors_audience_information[
            'general_information'][
            'users'] = self.get_selected_value_of_modal_from_field(AudienceFormLocators.form_control_class,
                                                                   AudienceFormLocators.users_field_data_qa)
        self.click_on_element(
            AudienceFormLocators.cancel_button_locator)
        return retargeting_apps_sites_visitors_audience_information

    def is_multiple_apps_sites_selected(self):
        locators = (By.XPATH,
                    "//span[@class='select2-selection select2-selection--multiple']//li[@class='select2-selection__choice']")
        elements = self.wait_for_presence_of_all_elements_located(
            locators)
        if len(elements) > 1:
            return 'True'
        else:
            return 'False'

    def provide_retargeting_geolocation_audience_data_and_save(self,
                                                               audience_data,
                                                               upload_csv=False):
        self.set_value_into_specific_input_field(AudienceFormLocators.name_field_data_qa,
                                                 audience_data['general_information']['audience_name'])
        self.set_value_into_specific_input_field(AudienceFormLocators.description_field_data_qa,
                                                 audience_data['general_information']['description'], is_textarea=True)
        self.select_dropdown_value(AudienceFormLocators.type_field_data_qa, audience_data['general_information'][
            'audience_type'])
        self.select_specific_date_range(
            AudienceFormLocators.date_field_data_qa,
            "7 Days")
        self.set_value_into_specific_input_field(AudienceFormLocators.user_validity_field_data_qa,
                                                 audience_data['general_information']['user_validity'])
        self.select_dropdown_value(AudienceFormLocators.method_field_data_qa, audience_data['general_information'][
            'method'])
        self.select_dropdown_value(AudienceFormLocators.generate_insights_report_field_data_qa,
                                   audience_data['general_information'][
                                       'generate_insights_report'])
        if upload_csv:
            self.wait_for_presence_of_element(
                AudienceFormLocators.csv_file_upload_locator).send_keys(
                os.path.join(os.getcwd(),
                             'assets/audiences/locations_csv_file.csv'))
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.users_field_data_qa,
            option_to_select=audience_data['general_information']['users'])
        self.scroll_to_specific_element(
            AudienceFormLocators.save_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(AudienceFormLocators.save_button_locator)

    def get_retargeting_geolocation_audience_information(self):
        self.reset_retargeting_geolocation_audience_information()
        retargeting_geolocation_audience_information[
            'general_information'][
            'audience_name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            AudienceFormLocators.audience_field_name_data_qa)
        retargeting_geolocation_audience_information[
            'general_information'][
            'description'] = self.get_text_using_tag_attribute(
            self.textarea_tag, self.data_qa_attribute,
            AudienceFormLocators.description_data_qa)
        retargeting_geolocation_audience_information[
            'general_information'][
            'audience_type'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.type_container_id)
        retargeting_geolocation_audience_information[
            'general_information'][
            'user_validity'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute,
            AudienceFormLocators.user_validity_minutes_id)
        retargeting_geolocation_audience_information[
            'general_information'][
            'user_validity_dropdown_vale'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              AudienceFormLocators.select2_validity_type_container_id)
        retargeting_geolocation_audience_information[
            'general_information'][
            'method'] = \
            self.get_text_or_value_from_selected_option(
                AudienceFormLocators.method_field_data_qa)
        retargeting_geolocation_audience_information[
            'general_information'][
            'selected_locations'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.amount_locations_id)
        retargeting_geolocation_audience_information[
            'general_information'][
            'generate_insights_report'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.select2_generate_insight_form_container_id)
        retargeting_geolocation_audience_information[
            'general_information'][
            'users'] = self.get_selected_value_of_modal_from_field(AudienceFormLocators.form_control_class,
                                                                   AudienceFormLocators.users_field_data_qa)
        self.click_on_element(AudienceFormLocators.nav_button_locator)
        self.click_on_element(
            AudienceFormLocators.cancel_button_locator)
        return retargeting_geolocation_audience_information

    def provide_retargeting_site_first_party_audience_data_and_save(self,
                                                                    audience_data):
        self.set_value_into_specific_input_field(AudienceFormLocators.name_field_data_qa,
                                                 audience_data['general_information']['audience_name'])
        self.set_value_into_specific_input_field(AudienceFormLocators.description_field_data_qa,
                                                 audience_data['general_information']['description'], is_textarea=True)
        self.select_dropdown_value(AudienceFormLocators.type_field_data_qa, audience_data['general_information'][
            'audience_type'])
        self.select_specific_date_range(
            AudienceFormLocators.date_field_data_qa,
            "7 Days")
        self.select_dropdown_value(AudienceFormLocators.rule_field_data_qa, audience_data['general_information'][
            'rule'])
        self.set_value_into_element(
            AudienceFormLocators.remove_if_url_contains_field_locator,
            audience_data['general_information'][
                'remove_if_url_contains'])
        self.wait_for_presence_of_element(
            AudienceFormLocators.remove_if_url_contains_field_locator).send_keys(
            Keys.ENTER)
        self.set_value_into_specific_input_field(AudienceFormLocators.user_validity_field_data_qa,
                                                 audience_data['general_information']['user_validity'])
        self.select_dropdown_value(AudienceFormLocators.generate_insights_report_field_data_qa,
                                   audience_data['general_information'][
                                       'generate_insights_report'])
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.users_field_data_qa,
            option_to_select=audience_data['general_information']['users'])
        self.scroll_to_specific_element(
            AudienceFormLocators.save_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(AudienceFormLocators.save_button_locator)

    def get_retargeting_site_first_party_audience_information(self):
        self.reset_retargeting_site_first_party_audience_information()
        retargeting_site_first_party_audience_information[
            'general_information'][
            'audience_name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            AudienceFormLocators.audience_field_name_data_qa)
        retargeting_site_first_party_audience_information[
            'general_information'][
            'description'] = self.get_text_using_tag_attribute(
            self.textarea_tag, self.data_qa_attribute,
            AudienceFormLocators.description_data_qa)
        retargeting_site_first_party_audience_information[
            'general_information'][
            'audience_type'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.type_container_id)
        retargeting_site_first_party_audience_information[
            'general_information'][
            'rule'] = self.get_text_or_value_from_selected_option(
            AudienceFormLocators.rule_field_data_qa)
        retargeting_site_first_party_audience_information[
            'general_information'][
            'user_validity'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute,
            AudienceFormLocators.user_validity_minutes_id)
        retargeting_site_first_party_audience_information[
            'general_information']['user_validity_dropdown_vale'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              AudienceFormLocators.select2_validity_type_container_id)
        retargeting_site_first_party_audience_information[
            'general_information']['remove_if_url_contains'] = \
            self.get_text_using_tag_attribute(self.li_tag,
                                              self.class_attribute,
                                              AudienceFormLocators.select2_selection_choice_class)
        retargeting_site_first_party_audience_information[
            'general_information'][
            'generate_insights_report'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.select2_generate_insight_form_container_id)
        retargeting_site_first_party_audience_information[
            'general_information'][
            'users'] = self.get_selected_value_of_modal_from_field(AudienceFormLocators.form_control_class,
                                                                   AudienceFormLocators.users_field_data_qa)
        self.click_on_element(
            AudienceFormLocators.cancel_button_locator)
        return retargeting_site_first_party_audience_information

    def provide_user_ids_list_audience_data_and_save(self, audience_data):
        self.set_value_into_specific_input_field(AudienceFormLocators.name_field_data_qa,
                                                 audience_data['general_information']['audience_name'])
        self.set_value_into_specific_input_field(AudienceFormLocators.description_field_data_qa,
                                                 audience_data['general_information']['description'], is_textarea=True)
        self.select_dropdown_value(AudienceFormLocators.type_field_data_qa, audience_data['general_information'][
            'audience_type'])
        self.wait_for_presence_of_element(
            AudienceFormLocators.csv_file_upload_locator).send_keys(
            os.path.join(os.getcwd(),
                         'assets/audiences/id_list_csv_file.csv'))
        self.select_dropdown_value(AudienceFormLocators.generate_insights_report_field_data_qa,
                                   audience_data['general_information'][
                                       'generate_insights_report'])
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=AudienceFormLocators.users_field_data_qa,
            option_to_select=audience_data['general_information']['users'])
        self.scroll_to_specific_element(
            AudienceFormLocators.save_button_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(AudienceFormLocators.save_button_locator)

    def get_user_ids_list_audience_information(self):
        self.reset_user_ids_list_audience_information()
        user_ids_list_audience_information['general_information'][
            'audience_name'] = self.get_text_using_tag_attribute(
            self.input_tag, self.data_qa_attribute,
            AudienceFormLocators.audience_field_name_data_qa)
        user_ids_list_audience_information['general_information'][
            'description'] = self.get_text_using_tag_attribute(
            self.textarea_tag, self.data_qa_attribute,
            AudienceFormLocators.description_data_qa)
        user_ids_list_audience_information['general_information'][
            'audience_type'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.type_container_id)
        user_ids_list_audience_information['general_information'][
            'generate_insights_report'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            AudienceFormLocators.select2_generate_insight_form_container_id)
        user_ids_list_audience_information['general_information'][
            'users'] = self.get_selected_value_of_modal_from_field(AudienceFormLocators.form_control_class,
                                                                   AudienceFormLocators.users_field_data_qa)
        self.click_on_element(
            AudienceFormLocators.cancel_button_locator)
        return user_ids_list_audience_information

    @staticmethod
    def reset_behavioral_user_interest_audience_information():
        global behavioral_user_interest_audience_information
        behavioral_user_interest_audience_information = {'general_information': {}}

    @staticmethod
    def reset_audience_group_audience_information():
        global audience_group_audience_information
        audience_group_audience_information = {'general_information': {}}

    @staticmethod
    def reset_retargeting_apps_sites_visitors_audience_information():
        global retargeting_apps_sites_visitors_audience_information
        retargeting_apps_sites_visitors_audience_information = {'general_information': {}}

    @staticmethod
    def reset_retargeting_geolocation_audience_information():
        global retargeting_geolocation_audience_information
        retargeting_geolocation_audience_information = {'general_information': {}}

    @staticmethod
    def reset_retargeting_site_first_party_audience_information():
        global retargeting_site_first_party_audience_information
        retargeting_site_first_party_audience_information = {'general_information': {}}

    @staticmethod
    def reset_user_ids_list_audience_information():
        global user_ids_list_audience_information
        user_ids_list_audience_information = {'general_information': {}}

    def wait_until_checkbox_selected_with_retry(self, checkbox_locator):
        retry_count = 0
        max_retry_count = 3
        while retry_count < max_retry_count:
            try:
                status = self.get_checkbox_status_for_specific_checkbox(checkbox_locator)
                if status == 'True':
                    return status
                time.sleep(self.ONE_SEC_DELAY)
            except Exception as e:
                print(f"Attempt {retry_count + 1} failed: {e}")
            retry_count += 1
            time.sleep(self.TWO_SEC_DELAY)
        return ''

    def reload_audience_form_page(self):
        url = self.driver.current_url
        self.driver.get(url)
        time.sleep(self.TWO_SEC_DELAY)
