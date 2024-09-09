import time
import re

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By

from configurations import generic_modules
from locators.campaign.campaign_list_locator import CampaignListLocators
from pages.base_page import BasePage
from datetime import datetime

campaign_information = {}


class DspDashboardCampaignsList(BasePage):

    def __init__(self, config, driver):
        super().__init__(driver)
        self.driver = driver
        self.config = config

    def reload_campaign_list_page(self):
        self.driver.get(generic_modules.BASE_URL)
        try:
            self.wait_alert_is_present(time_out=5)
            self.accept_alert()
            self.wait_for_element_to_be_clickable(
                CampaignListLocators.campaign_search_field_locator)
        except TimeoutException:
            self.wait_for_element_to_be_clickable(
                CampaignListLocators.campaign_search_field_locator)

    def select_all_status(self):
        status_selected = self.get_text_using_tag_attribute(
            self.span_tag,
            self.id_attribute,
            CampaignListLocators.status_dropdown_id)
        if status_selected != "All":
            self.click_on_element(
                CampaignListLocators.status_dropdown_locator)
            self.click_on_element(
                CampaignListLocators.all_status_option_locator)
            time.sleep(self.ONE_SEC_DELAY)

    def get_draft_status_text(self):
        return self.get_element_text(
            CampaignListLocators.campaign_list_draft_status)

    def get_success_message(self):
        return self.get_element_text(
            CampaignListLocators.success_message_locator)

    def get_warning_message(self):
        return self.get_element_text(
            CampaignListLocators.warning_message_locator)

    def get_danger_message(self):
        return self.get_element_text(
            CampaignListLocators.danger_message_locator)

    def search_and_action(self, campaign_name, action="None",
                          force_reload=False):
        try:
            if force_reload:
                self.reload_campaign_list_page()
                time.sleep(self.TWO_SEC_DELAY)
                self.set_value_into_element(
                    CampaignListLocators.campaign_search_field_locator,
                    campaign_name)
            else:
                self.set_value_into_element(
                    CampaignListLocators.campaign_search_field_locator,
                    campaign_name)
        except Exception:
            self.reload_campaign_list_page()
            self.set_value_into_element(
                CampaignListLocators.campaign_search_field_locator,
                campaign_name)
        self.wait_for_visibility_of_element(
            CampaignListLocators.three_dot_of_campaign_xpath.format(
                campaign_name),
            locator_initialization=True)
        if action != 'None':
            self.click_element_execute_script(
                CampaignListLocators.three_dot_of_campaign_xpath.format(
                    campaign_name))
            time.sleep(self.TWO_SEC_DELAY)
        if action.lower() == 'edit':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_element_execute_script(
                CampaignListLocators.campaign_list_edit_locator)
        elif action.lower() == 'delete':
            self.click_element_execute_script(
                CampaignListLocators.campaign_list_delete_locator)
            self.click_on_element(
                CampaignListLocators.confirm_button_alert_locator)
        elif action.lower() == 'approve':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_element_execute_script(
                CampaignListLocators.campaign_list_approve_locator)
        elif action.lower() == 'duplicate':
            self.click_element_execute_script(
                CampaignListLocators.campaign_list_duplicate_locator)
        elif action.lower() == 'campaign goals':
            self.click_on_three_dot_option(
                CampaignListLocators.campaign_goals_label,
                CampaignListLocators.campaign_table_id)

    def check_uncheck_campaign_list_grid_row_checkbox(self,
                                                      campaign_name="",
                                                      check_the_checkbox=False,
                                                      check_all_checkbox=False):
        self.check_uncheck_specific_grid_row_checkbox(
            CampaignListLocators.campaign_table_id,
            check_all_checkbox=check_all_checkbox,
            check_the_checkbox=check_the_checkbox,
            column_value_to_identify_column=campaign_name)

    def select_item_from_campaign_multi_action_menu(self,
                                                    item_name_to_select,
                                                    switch_to_new_window=False):
        self.select_item_from_multi_action_menu(
            CampaignListLocators.campaign_multi_actions_menu_id,
            item_name_to_select)
        time.sleep(self.TWO_SEC_DELAY)
        if item_name_to_select == "Delete":
            self.click_on_element(
                CampaignListLocators.confirm_button_alert_locator)
        if switch_to_new_window:
            self.switch_to_new_window()

    def get_campaign_id(self, campaign_id):
        return self.get_element_text(CampaignListLocators.campaign_id_data_qa.format(campaign_id))

    def get_campaign_status(self, campaign_id):
        return self.get_element_text(CampaignListLocators.campaign_status_locator.format(campaign_id),
                                     locator_initialization=True)

    def get_campaign_name(self, campaign_id):
        return self.get_element_text(CampaignListLocators.campaign_name_locator.format(campaign_id),
                                     locator_initialization=True)

    def get_campaign_type(self, campaign_id):
        return self.get_element_text(CampaignListLocators.campaign_type_locator.format(campaign_id),
                                     locator_initialization=True)

    def get_creative_type(self, campaign_id):
        self.wait_for_visibility_of_element(CampaignListLocators.creative_type_locator.format(campaign_id),
                                            locator_initialization=True)
        return self.get_attribute_value(CampaignListLocators.creative_type_locator.format(campaign_id),
                                        "title", locator_initialization=True)

    def get_campaign_country(self, campaign_id):
        return self.get_attribute_value(CampaignListLocators.campaign_country_locator.format(campaign_id),
                                        "title", locator_initialization=True)

    def get_campaign_start_date(self, campaign_id):
        return self.get_element_text(CampaignListLocators.start_date_locator.format(campaign_id),
                                     locator_initialization=True)

    def get_campaign_end_date(self):
        return self.get_value_from_specific_grid_column(
            CampaignListLocators.campaigns_list_table_wrapper_div_id, CampaignListLocators.campaign_end_date_label)

    def get_campaign_daily_budget(self, campaign_id):
        budget = self.get_element_text(CampaignListLocators.daily_budget_data_qa.format(campaign_id))
        match = re.search(r'[\d,]*\.\d+', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return cleaned_budget

    def get_campaign_total_budget(self, campaign_id):
        budget = self.get_element_text(CampaignListLocators.total_budget_data_qa.format(campaign_id))
        match = re.search(r'[\d,]*\.\d+', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return cleaned_budget

    def get_campaign_daily_spend(self, campaign_id):
        spend = self.get_element_text(CampaignListLocators.today_spend_data_qa.format(campaign_id))
        return re.sub(r'[^\d.]', '', spend)

    def get_campaign_total_spend(self, campaign_id):
        spend = self.get_element_text(CampaignListLocators.total_spend_data_qa.format(campaign_id))
        return re.sub(r'[^\d.]', '', spend)

    def get_campaign_remaining_total_budget(self, campaign_id):
        budget = self.get_element_text(CampaignListLocators.remaining_total_data_qa.format(campaign_id))
        match = re.search(r'\d+(\.\d*)?', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return float(cleaned_budget)

    def get_campaign_remaining_today_budget(self, campaign_id):
        budget = self.get_element_text(CampaignListLocators.remaining_today_data_qa.format(campaign_id))
        match = re.search(r'\d+(\.\d*)?', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return float(cleaned_budget)

    def get_campaign_total_budget_from_total_line(self):
        budget = self.get_element_text(CampaignListLocators.total_budget_total_line_data_qa)
        return re.sub(r'[^\d.]', '', budget).replace(',', '')

    def get_campaign_daily_budget_from_total_line(self):
        budget = self.get_element_text(CampaignListLocators.daily_budget_total_line_data_qa)
        return re.sub(r'[^\d.]', '', budget).replace(',', '')

    def get_campaign_total_spend_from_total_line(self):
        spend = self.get_element_text(CampaignListLocators.total_spend_total_line_data_qa)
        spend = re.sub(r'[^\d.]', '', spend).replace(',', '')
        return float(spend)

    def get_campaign_today_spend_from_total_line(self):
        spend = self.get_element_text(CampaignListLocators.today_spend_total_line_data_qa)
        spend = re.sub(r'[^\d.]', '', spend).replace(',', '')
        return float(spend)

    def get_campaign_mandatory_information(self, campaign_id):
        self.reset_campaign_information()
        time.sleep(self.ONE_SEC_DELAY)
        campaign_information['campaign_id'] = self.get_campaign_id(campaign_id)
        campaign_information['campaign_status'] = self.get_campaign_status(campaign_id)
        campaign_information['campaign_name'] = self.get_campaign_name(campaign_id)
        campaign_information['campaign_type'] = self.get_campaign_type(campaign_id)
        campaign_information['creative_type'] = self.get_creative_type(campaign_id)
        return campaign_information

    def get_campaign_all_information(self, campaign_id):
        self.reset_campaign_information()
        time.sleep(self.ONE_SEC_DELAY)
        campaign_information['campaign_id'] = self.get_campaign_id(campaign_id)
        campaign_information['campaign_status'] = self.get_campaign_status(campaign_id)
        campaign_information['campaign_name'] = self.get_campaign_name(campaign_id)
        campaign_information['campaign_type'] = self.get_campaign_type(campaign_id)
        campaign_information['creative_type'] = self.get_creative_type(campaign_id)
        campaign_information['campaign_country'] = self.get_campaign_country(campaign_id)
        campaign_information['start_date'] = self.get_campaign_start_date(campaign_id)
        campaign_information['end_date'] = self.get_campaign_end_date()
        campaign_information['daily_budget'] = self.get_campaign_daily_budget(campaign_id)
        campaign_information['total_budget'] = self.get_campaign_total_budget(campaign_id)
        return campaign_information

    def check_uncheck_specific_grid_row_checkbox_for_draft(self, parent_div_id, check_the_checkbox,
                                                           check_all_checkbox=False,
                                                           column_value_to_identify_column=""):
        if check_all_checkbox:
            checkbox_locator = "(//div[@id='" + parent_div_id + "']//tr[1]//input[@type='checkbox'])[1]"
        else:
            checkbox_locator = "//div[@id='" + parent_div_id + "']//div[normalize-space()='" + \
                               column_value_to_identify_column + "']/..//..//..//input[@type='checkbox']"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != check_the_checkbox:
            self.click_on_element(checkbox_locator)

    def select_list_table_length(self, length='100'):
        self.select_dropdown_value(CampaignListLocators.rows_per_page_label, length)

    def check_uncheck_campaign_list_grid_row_checkbox_draft_campaigns(self,
                                                      campaign_id="",
                                                      check_the_checkbox=False,
                                                      check_all_checkbox=False):
        self.check_uncheck_specific_grid_row_checkbox(
            CampaignListLocators.campaign_table_id,
            check_all_checkbox=check_all_checkbox,
            check_the_checkbox=check_the_checkbox,
            data_qa_attribute_id=campaign_id)

    def filter_campaigns_by_status(self, campaign_status):
        self.select_dropdown_value(CampaignListLocators.campaign_status_select_data_qa,
                                   campaign_status, select_by_value=False)

    @staticmethod
    def reset_campaign_information():
        global campaign_information
        campaign_information = {}

    def get_campaign_duration(self, campaign_id):
        start_date = self.get_campaign_start_date(campaign_id)
        start_date = datetime.strptime(start_date, "%d %b, %Y")
        end_date = self.get_campaign_end_date()
        end_date = datetime.strptime(end_date, "%d %b, %Y")
        campaign_duration = (end_date - start_date).days
        campaign_duration = campaign_duration + 1
        return campaign_duration

    def get_calculated_daily_budget(self, campaign_id, remaining_days):
        total_budget = self.get_campaign_total_budget(campaign_id)
        total_spend = self.get_campaign_total_spend(campaign_id)
        today_spend = self.get_campaign_daily_spend(campaign_id)
        daily_budget = (float(total_budget) - float(total_spend) + float(today_spend)) / remaining_days
        return round(daily_budget, 2)

    def get_calculated_total_budget(self, campaign_id, remaining_days):
        daily_budget = self.get_campaign_daily_budget(campaign_id)
        total_spend = self.get_campaign_total_spend(campaign_id)
        today_spend = self.get_campaign_daily_spend(campaign_id)
        remaining_daily_budget = float(daily_budget) - float(today_spend)
        total_budget = float(total_spend) + remaining_daily_budget + (float(daily_budget) * (remaining_days - 1))
        return round(total_budget, 2)

    def run_change_campaign_status_cron_job(self, campaign_id, status_number):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + base_url + self.config['cron-jobs']['campaign-status-change-cron-job'].format(
            campaign_id, status_number)
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])

    def run_manage_daily_cap_cron_job(self, campaign_id):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + base_url + self.config['cron-jobs']['manage-daily-cap-cron-job'].format(
            campaign_id)
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])

    def run_manage_status_cron_job(self, campaign_id):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + base_url + self.config['cron-jobs']['manage-status-cron-job'].format(
            campaign_id)
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])

    def run_recalculate_daily_cron_job(self, campaign_id):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + base_url + self.config['cron-jobs']['recalculate-daily-cron-job'].format(
            campaign_id)
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])

    def run_site_count_cron_job(self, campaign_id):
        base_url = (self.config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + base_url + self.config['cron-jobs']['site-count-cron-job'].format(
            campaign_id)
        self.driver.get(cron_job_url)
        self.driver.get(self.config['credential']['url'])
