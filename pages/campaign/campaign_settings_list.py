import time
import re

from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

campaign_information = {}


class DspDashboardCampaignsSettings(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_loading_campaigns(self):
        try:
            self.wait_for_visibility_of_element(
                CampaignSettingsLocator.loader_locator,
                time_out=6)
        except:
            self.wait_for_element_to_be_invisible(
                CampaignSettingsLocator.loader_locator)
        self.wait_for_element_to_be_invisible(
            CampaignSettingsLocator.loader_locator)

    def search_campaign(self, campaign_id):
        self.set_value_into_element(
            CampaignSettingsLocator.search_box_locator,
            campaign_id)
        self.click_on_element(
            CampaignSettingsLocator.campaign_search_button_locator)
        self.wait_for_loading_campaigns()

    def navigate_to_created_campaign(self, db_data, config):
        campaign_url = []
        for campaigns in db_data:
            for campaign_id in campaigns.values():
                campaign_url.append(config['credential'][
                                        'url'] + "/admin/campaigns/form?id={}".format(
                    campaign_id))
        return campaign_url

    def get_success_message(self):
        time.sleep(self.TWO_SEC_DELAY)
        return self.get_element_text(
            CampaignSettingsLocator.success_message_locator)

    def select_all_status(self):
        status_selected = self.get_text_using_tag_attribute(
            self.span_tag,
            self.id_attribute,
            CampaignSettingsLocator.status_dropdown_id)
        if status_selected != "All":
            self.click_on_element(
                CampaignSettingsLocator.status_dropdown_locator)
            self.click_on_element(
                CampaignSettingsLocator.all_status_option_locator)

    def move_to_campaign_settings_page(self):
        time.sleep(self.TWO_SEC_DELAY)
        self.click_element_execute_script(
            CampaignSettingsLocator.campaign_settings_navigation)

    def search_and_click_on_campaign_name(self, campaign_name, index,
                                          click_on_campaign_name=True):
        time.sleep(self.TWO_SEC_DELAY)
        try:
            self.wait_for_visibility_of_element(
                CampaignSettingsLocator.campaign_search_field_locator)
        except TimeoutException:
            self.driver.refresh()
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_visibility_of_element(
                CampaignSettingsLocator.campaign_search_field_locator)
        self.set_value_into_element(
            CampaignSettingsLocator.campaign_search_field_locator,
            campaign_name)
        self.wait_for_presence_of_element(
            CampaignSettingsLocator.campaign_search_button_locator)
        self.wait_for_element_to_be_clickable(
            CampaignSettingsLocator.campaign_search_button_locator)
        self.click_on_element(
            CampaignSettingsLocator.campaign_search_button_locator)
        try:
            self.wait_for_visibility_of_element(CampaignSettingsLocator.
            campaign_name_xpath_locator.format(
                campaign_name, str(index)),
                locator_initialization=True)
        except TimeoutException:
            self.driver.refresh()
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_visibility_of_element(
                CampaignSettingsLocator.campaign_search_field_locator)
            self.set_value_into_element(
                CampaignSettingsLocator.campaign_search_field_locator,
                campaign_name)
            self.wait_for_presence_of_element(
                CampaignSettingsLocator.campaign_search_button_locator)
            self.wait_for_element_to_be_clickable(
                CampaignSettingsLocator.campaign_search_button_locator)
            self.click_on_element(
                CampaignSettingsLocator.campaign_search_button_locator)
            self.wait_for_visibility_of_element(CampaignSettingsLocator.
            campaign_name_xpath_locator.format(
                campaign_name, str(index)),
                locator_initialization=True)
        if click_on_campaign_name:
            self.click_element_execute_script(
                CampaignSettingsLocator.campaign_name_xpath_locator.format(
                    campaign_name,
                    str(index)))

    def get_stopped_status_text(self):
        return self.get_element_text(
            CampaignSettingsLocator.campaign_stopped_status_locator)

    def navigate_to_add_campaign_group(self):
        self.wait_for_presence_of_element(
            CampaignSettingsLocator.btn_create_locator)
        self.wait_for_visibility_of_element(
            CampaignSettingsLocator.btn_create_locator)
        self.wait_for_element_to_be_clickable(
            CampaignSettingsLocator.btn_create_locator)
        self.click_on_element(
            CampaignSettingsLocator.btn_create_locator)

    def get_campaign_settings_link_text(self):
        self.wait_for_presence_of_element(
            CampaignSettingsLocator.campaign_settings_locator)
        self.wait_for_visibility_of_element(
            CampaignSettingsLocator.campaign_settings_locator)
        return self.get_element_text(
            CampaignSettingsLocator.campaign_settings_locator)

    def update_single_campaign_name(self, campaign_id, campaign_name):
        self.click_icon_table(str(campaign_id),
                              CampaignSettingsLocator.campaign_name_title)
        self.set_value_into_element(
            CampaignSettingsLocator.campaign_name_edit_field_locator,
            campaign_name)
        self.click_element_execute_script(
            CampaignSettingsLocator.modal_save_button_xpath)
        self.wait_for_loading_campaigns()

    def update_single_campaign_bid_cpm(self, campaign_id, bid_cpm):
        self.click_icon_table(str(campaign_id),
                              CampaignSettingsLocator.bid_cpm_title)
        self.wait_for_visibility_of_element(
            CampaignSettingsLocator.apply_to_all_creative_label_locator)
        self.click_on_element(
            CampaignSettingsLocator.bid_cpm_edit_field_locator)
        self.set_value_into_element(
            CampaignSettingsLocator.bid_cpm_edit_field_locator,
            bid_cpm)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_element_execute_script(
            CampaignSettingsLocator.modal_save_button_xpath)
        self.wait_for_loading_campaigns()

    def update_single_campaign_landing_page(self, campaign_id,
                                            landing_page):
        self.click_icon_table(str(campaign_id),
                              CampaignSettingsLocator.landing_page_title)
        self.click_on_element(
            CampaignSettingsLocator.click_url_edit_field_locator)
        self.set_value_into_element(
            CampaignSettingsLocator.click_url_edit_field_locator,
            landing_page)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(
            CampaignSettingsLocator.ad_domain_locator)
        self.wait_for_presence_of_element(
            CampaignSettingsLocator.tick_or_cross_sign_click_url_locator)
        self.set_value_into_element(
            CampaignSettingsLocator.ad_domain_search_field_locator,
            "dsp.eskimi.com")
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_presence_of_element(
            CampaignSettingsLocator.ad_domain_search_field_locator).send_keys(
            Keys.ENTER)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_element_execute_script(
            CampaignSettingsLocator.modal_save_button_xpath)
        self.wait_for_loading_campaigns()

    def update_single_campaign_creative_set(self, campaign_id,
                                            creative_set_name):
        self.click_icon_table(str(campaign_id),
                              CampaignSettingsLocator.creative_set_title)
        self.select_from_modal(creative_set_name, CampaignSettingsLocator.creative_set_label)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_element_execute_script(
            CampaignSettingsLocator.modal_save_button_xpath)
        self.wait_for_loading_campaigns()

    def update_campaign_setting_data_single(self, campaign_id,
                                            campaign_settings_data):
        self.wait_for_loading_campaigns()
        self.search_campaign(campaign_id)
        self.update_single_campaign_name(campaign_id,
                                         campaign_settings_data[
                                             'name'])
        self.update_single_campaign_bid_cpm(campaign_id,
                                            campaign_settings_data[
                                                'bid_cpm'])
        self.update_single_campaign_landing_page(campaign_id,
                                                 campaign_settings_data[
                                                     'landing_page'])
        self.update_single_campaign_creative_set(campaign_id,
                                                 campaign_settings_data[
                                                     'creative_set'])

    def get_campaign_data(self, campaign_id):
        campaign_information[
            'name'] = self.get_column_text_campaign_settings_table(
            str(campaign_id),
            CampaignSettingsLocator.campaign_name_title)
        campaign_information[
            'bid_cpm'] = self.get_column_text_campaign_settings_table(
            str(campaign_id),
            CampaignSettingsLocator.bid_cpm_title)
        campaign_information[
            'landing_page'] = self.get_column_text_campaign_settings_table(
            str(campaign_id),
            CampaignSettingsLocator.landing_page_title)
        campaign_information[
            'creative_set'] = self.get_column_text_campaign_settings_table(
            str(campaign_id),
            CampaignSettingsLocator.creative_set_title,
            data_attribute=False)
        return campaign_information

    def click_icon_table(self, campaign_id, field_title):
        element = self.driver.find_element(By.XPATH,
                                           "//a[@data-id='" + campaign_id + "']/i[@class='fas fa-pencil-alt' and @title='" + field_title + "']")
        self.driver.execute_script("arguments[0].click();", element)

    def get_column_text_campaign_settings_table(self, campaign_id,
                                                field_title,
                                                data_attribute=True):
        if data_attribute:
            locator = (By.XPATH,
                       "//a[@data-id='" + campaign_id + "']/i[@class='fas fa-pencil-alt' and @title='" + field_title + "']/..")
            return self.wait_for_presence_of_element(
                locator).get_attribute(
                "data-value")
        else:
            locator = (By.XPATH,
                       "//*[@data-id='" + campaign_id + "']//i[@title='" + field_title + "']/../..//span")
            return self.get_element_text(locator)

    def get_total_budget(self, campaign_id):
        budget = self.get_element_text(CampaignSettingsLocator.total_budget_data_qa.format(campaign_id))
        match = re.search(r'[\d,]*\.\d+', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return cleaned_budget

    def get_daily_budget(self, campaign_id):
        budget = self.get_element_text(CampaignSettingsLocator.daily_budget_data_qa.format(campaign_id))
        match = re.search(r'[\d,]*\.\d+', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return cleaned_budget

    def get_bid_cpm(self, campaign_id):
        bid_cpm = self.get_element_text(CampaignSettingsLocator.bid_cpm_id.format(campaign_id),
                                        locator_initialization=True)
        bid_cpm = re.sub(r'[^\d.]', '', bid_cpm)
        return bid_cpm

    def get_total_spend(self, campaign_id):
        spend = self.get_element_text(CampaignSettingsLocator.total_spend_data_qa.format(campaign_id))
        spend = re.sub(r'[^\d.]', '', spend)
        return spend

    def get_today_spend(self, campaign_id):
        spend = self.get_element_text(CampaignSettingsLocator.today_spend_data_qa.format(campaign_id))
        spend = re.sub(r'[^\d.]', '', spend)
        return spend

    def get_total_remaining_budget(self, campaign_id):
        budget = self.get_element_text(CampaignSettingsLocator.remaining_total_data_qa.format(campaign_id))
        match = re.search(r'\d+(\.\d*)?', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return float(cleaned_budget)

    def get_daily_remaining_budget(self, campaign_id):
        budget = self.get_element_text(CampaignSettingsLocator.remaining_today_data_qa.format(campaign_id))
        match = re.search(r'\d+(\.\d*)?', budget)
        cleaned_budget = match.group(0).replace(',', '') if match else None
        return float(cleaned_budget)
