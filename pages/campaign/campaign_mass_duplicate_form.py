import os
import time
import re

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.base_page import BasePage
from selenium.webdriver.common.by import By

campaign_information = {}


class DspDashboardCampaignsMassDuplicate(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_campaign_name_and_type(self):
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.creative_type_dropdown_locator)
        campaign_information['name_and_type'][
            'platform_type'] = self.get_attribute_value(
            CampaignFormLocators.platform_type_locator, "title")
        campaign_information['name_and_type'][
            'creative_type'] = self.get_text_using_tag_attribute(
            self.span_tag,
            self.id_attribute,
            CampaignFormLocators.
            type_field_id)

        campaign_information['name_and_type'][
            'campaign_type'] = self.get_element_text(
            CampaignFormLocators.campaign_type_dropdown_locator)
        campaign_information['name_and_type'][
            'campaign_name'] = self.get_text_using_tag_attribute(
            self.input_tag,
            self.id_attribute,
            CampaignFormLocators.
            campaign_field_id)

    def get_campaign_objective(self, campaign_data):
        # GET CAMPAIGN GOAL
        special_chars = ['{', '}', '"']
        campaign_information['campaign_goal_info'][
            'campaign_goal'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute,
            CampaignFormLocators.campaign_goal_id)
        campaign_information['campaign_goal_info'][
            'primary_objective'] = self.get_text_using_tag_attribute(
            self.input_tag,
            self.id_attribute,
            CampaignFormLocators.primary_objective_attribute_value)
        campaign_information['campaign_goal_info'][
            'secondary_objectives'] = self.get_text_using_tag_attribute(
            self.input_tag,
            self.id_attribute,
            CampaignFormLocators.secondary_objective_attribute_value)
        for sc in special_chars:
            campaign_information['campaign_goal_info'][
                'primary_objective'] = \
                campaign_information['campaign_goal_info'][
                    'primary_objective'].replace(sc, "")
            campaign_information['campaign_goal_info'][
                'secondary_objectives'] = \
                campaign_information['campaign_goal_info'][
                    'secondary_objectives'].replace(sc, "")
        campaign_information['campaign_goal_info'][
            'pre_optimisation'] = self.get_attribute_value(
            CampaignFormLocators.primary_objective_optimisation_slider_locator,
            'checked')
        campaign_information['campaign_goal_info'][
            'auto_opt_checkbox'] = self.get_selected_checkbox_name_from_a_section(
            CampaignFormLocators.auto_optimisation_section_id,
            multiple=True)
        # CTR
        campaign_information['campaign_goal_info'][
            'minimum_ctr'] = self.get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['campaign_goal_info'][
                'auto_opt_checkbox'][0], "",
            first_field_value=True)
        campaign_information['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = self. \
            get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['campaign_goal_info'][
                'auto_opt_checkbox'][0],
            CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label)
        # SR
        campaign_information['campaign_goal_info'][
            'minimum_sr'] = self.get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['campaign_goal_info'][
                'auto_opt_checkbox'][1], "",
            first_field_value=True)
        campaign_information['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = self.get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['campaign_goal_info'][
                'auto_opt_checkbox'][1],
            CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label)
        # IMPRESSION
        campaign_information['campaign_goal_info'][
            'impression_amount'] = self.get_text_using_tag_attribute(
            self.input_tag, self.class_attribute,
            CampaignFormLocators.impression_field_class)
        campaign_information['campaign_goal_info'][
            'impression_click'] = self.get_text_using_tag_attribute(
            self.input_tag, self.class_attribute,
            CampaignFormLocators.impression_click_field_class)
        campaign_information['campaign_goal_info'][
            'impression_time'] = self.get_text_using_tag_attribute(
            self.input_tag, self.class_attribute,
            CampaignFormLocators.capping_amount_field_class)

    def get_campaign_launch_date_and_budget(self):
        campaign_information['launch_date_and_budget'][
            'bid_cpm'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute,
            CampaignFormLocators.bid_cpm_field_id)
        campaign_information['launch_date_and_budget']['daily_budget_selected'] = self.get_checkbox_status(
            CampaignFormLocators.daily_budget_radio_btn_data_qa)
        if campaign_information['launch_date_and_budget']['daily_budget_selected'] == "True":
            campaign_information['launch_date_and_budget'][
                'daily_budget'] = self.get_budget_amount()
            campaign_information['launch_date_and_budget'][
                'total_budget'] = self.get_estimated_budget()
        else:
            campaign_information['launch_date_and_budget'][
                'total_budget'] = self.get_budget_amount()
            campaign_information['launch_date_and_budget'][
                'daily_budget'] = self.get_estimated_budget()

    def get_campaign_location_and_audiences(self):
        campaign_information['location_and_audiences'][
            'country_name'] = self.get_selected_options_using_js_code(CampaignFormLocators.country_label)
        campaign_information['location_and_audiences'][
            'audience_include'] = self.get_element_text(
            CampaignFormLocators.audience_include_value_locator)
        campaign_information['location_and_audiences'][
            'audience_exclude'] = self.get_element_text(
            CampaignFormLocators.audience_exclude_value_locator)
        campaign_information['location_and_audiences'][
            'age'] = self.get_selected_options_using_js_code(CampaignFormLocators.age_label)
        campaign_information['location_and_audiences'][
            'gender'] = self.get_selected_options_using_js_code(CampaignFormLocators.gender_label)
        campaign_information['location_and_audiences'][
            'language'] = self.get_selected_options_using_js_code(CampaignFormLocators.languages_label)
        campaign_information['location_and_audiences'][
            'sec'] = self.get_selected_options_using_js_code(CampaignFormLocators.sec_socio_economic_class_groups_label)

    def get_campaign_brand_safety(self):
        campaign_information['brand_safety'][
            'brand_safety'] = self.get_selected_options_using_js_code(CampaignFormLocators.brand_safety_label)
        campaign_information['brand_safety'][
            'contextual_targeting'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.contextual_targeting_label)

    def get_campaign_platforms_telco_and_devices(self, campaign_data):
        debug_mode = "JENKINS_URL" not in os.environ
        campaign_information['platforms_telco_and_devices'][
            'ad_placement_type'] = self.get_selected_checkbox_name_from_a_section(
            section_div_id=CampaignFormLocators.ad_placement_type_section_id)
        campaign_information['platforms_telco_and_devices'][
            'ip_address/ranges'] = self.get_element_text(
            CampaignFormLocators.ip_ranges_input_field_locator)
        campaign_information['platforms_telco_and_devices'][
            'device_type'] = self.get_selected_options_using_js_code(CampaignFormLocators.device_type_label)
        campaign_information['platforms_telco_and_devices'][
            'device_os'] = self.get_selected_options_using_js_code(CampaignFormLocators.device_os_label)
        campaign_information['platforms_telco_and_devices'][
            'device_brand'] = self.get_selected_options_using_js_code(CampaignFormLocators.device_brands_label)
        campaign_information['platforms_telco_and_devices'][
            'device_model'] = self.get_selected_options_using_js_code(CampaignFormLocators.device_models_label)
        campaign_information['platforms_telco_and_devices'][
            'browser'] = self.get_selected_options_using_js_code(CampaignFormLocators.device_browsers_label)
        campaign_information['platforms_telco_and_devices'][
            'device_cost_range'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.device_cost_ranges_label)
        campaign_information['platforms_telco_and_devices'][
            'sim_amount'] = self.get_selected_checkbox_name_from_a_section(
            CampaignFormLocators.sim_amount_section_id)
        if not debug_mode:
            campaign_information['platforms_telco_and_devices'][
                'device_connection'] = \
                campaign_data['platforms_telco_and_devices'][
                    'device_connection']
            campaign_information['platforms_telco_and_devices'][
                'network_connection'] = \
                campaign_data['platforms_telco_and_devices'][
                    'network_connection']
        else:
            campaign_information['platforms_telco_and_devices'][
                'device_connection'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.device_connection_section_id)
            campaign_information['platforms_telco_and_devices'][
                'network_connection'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.network_connection_section_id)
        campaign_information['platforms_telco_and_devices'][
            'mobile_data_consumption'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.mobile_data_consumption_label)

    def get_campaign_deals_and_packages(self, ingame=False):
        if ingame is False:
            campaign_information['deals_and_packages'][
                'ad_exchange_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.exchanges_section_id)
        else:
            campaign_information['deals_and_packages'][
                'ad_exchange_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.exchanges_section_id,
                multiple=True)
        campaign_information['deals_and_packages'][
            'ad_placement_position_checkbox'] = self.get_selected_checkbox_name_from_a_section(
            CampaignFormLocators.ad_placement_positions_section_id)
        # PRIVATE MARKETPLACE
        campaign_information['deals_and_packages'][
            'private_marketplace'] = self.get_selected_value_of_modal_from_field(
            select_tag_id_or_class=CampaignFormLocators.private_marketplace_dropdown_id)

    def get_campaign_landing_and_creatives(self):
        campaign_information['landing_and_creatives'][
            'click_url'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute,
            CampaignFormLocators.click_url_field_id)
        campaign_information['landing_and_creatives'][
            'ad_domain'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            CampaignFormLocators.ad_domain_field_id)
        campaign_information['landing_and_creatives'][
            'creative'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.selected_creative_sets_selection_label)

    def get_campaign_information_for_mass_duplicate_apply_all(self,
                                                              campaign_data):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.TWO_SEC_DELAY)
        self.get_campaign_objective(campaign_data)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences()
        self.get_campaign_platforms_telco_and_devices(campaign_data)
        self.get_campaign_deals_and_packages(campaign_data)
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator,
            locator_to_be_appeared=CampaignFormLocators.cancel_button_locator)
        self.wait_for_presence_of_element(
            CampaignFormLocators.cancel_button_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.cancel_button_locator)
        try:
            self.click_on_element(
                CampaignFormLocators.cancel_button_locator)
            WebDriverWait(self.driver, 5).until(
                EC.alert_is_present(),
                'Timed out waiting for alert to appear')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("Alert not present")
        return campaign_information

    @staticmethod
    def reset_campaign_information():
        global campaign_information
        campaign_information = {'name_and_type': {},
                                'campaign_goal_info': {},
                                'launch_date_and_budget': {},
                                'location_and_audiences': {},
                                'brand_safety': {},
                                'campaign_purpose': {},
                                'platforms_telco_and_devices': {},
                                'deals_and_packages': {},
                                'landing_and_creatives': {}}

    def get_value_from_specific_input_field_under_auto_optimisation(self,
                                                                    checkbox_name,
                                                                    field_name="",
                                                                    first_field_value=False):
        if first_field_value:
            locator = (By.XPATH,
                       "(//label[normalize-space()='" + checkbox_name + "']/..//..//input)[2]")
        else:
            locator = (By.XPATH,
                       "//label[normalize-space()='" + checkbox_name + "']/..//..//label[normalize-space("
                                                                       ")='" + field_name + "']/..//input")
        return self.get_element_text(locator, input_tag=True)

    def get_budget_amount(self):
        budget = self.get_attribute_value(CampaignFormLocators.budget_input_data_qa, "value")
        budget = budget.replace(",", "")
        return budget

    def get_estimated_budget(self):
        budget = self.get_element_text(CampaignFormLocators.estimated_budget_data_qa)
        return re.sub(r'[^\d.]', '', re.sub(r'\(.*?\)', '', budget))
