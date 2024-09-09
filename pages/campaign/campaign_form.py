import os
import time
import math
import re

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configurations.generic_modules import step_printer
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.base_page import BasePage
from utils.campaigns import CampaignUtils
from datetime import datetime

campaign_information = {}


class DspDashboardCampaignsForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_name_and_type_info(self, campaign_data,
                                   duplicate_or_edit_campaign=False,
                                   multi_platform=False,
                                   ingame=False):
        time.sleep(self.TWO_SEC_DELAY)
        if multi_platform:
            platforms = campaign_data['name_and_type'][
                'platform_type']
            for platform in platforms:
                self.click_on_element(
                    CampaignFormLocators.platform_name.format(
                        platform.lower()),
                    locator_initialization=True)
        if duplicate_or_edit_campaign is False:
            creative_type = campaign_data['name_and_type'][
                'creative_type']
            try:
                self.wait_for_presence_of_element(
                    CampaignFormLocators.creative_type_dropdown_locator,
                    self.HALF_MINUTE)
                self.wait_for_element_to_be_clickable(
                    CampaignFormLocators.creative_type_dropdown_locator)
            finally:
                self.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=creative_type)
        if ingame:
            self.select_dropdown_value(CampaignFormLocators.campaign_type_label, campaign_data['name_and_type'][
                'campaign_type'])
        self.wait_for_presence_of_element(
            CampaignFormLocators.creative_type_dropdown_locator,
            self.HALF_MINUTE)
        self.set_value_into_element(
            CampaignFormLocators.campaign_name_input_field_locator,
            campaign_data['name_and_type']['campaign_name'])

    def provide_campaign_objective(self, campaign_data,
                                   edit_campaign=False, audio=False):
        # SELECT CAMPAIGN GOAL
        if edit_campaign is False:
            self.click_on_element(
                CampaignFormLocators.campaign_goal.format(
                    campaign_data['campaign_goal_info'][
                        'campaign_goal']),
                locator_initialization=True)
        # SELECT PRIMARY OBJECTIVE AND SET VALUE
        primary_objective = campaign_data['campaign_goal_info'][
            'primary_objective'].split(':')
        self.click_on_element_using_tag_attribute(self.div_tag,
                                                  CampaignFormLocators.goal_attribute,
                                                  primary_objective[0])
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.id_attribute,
                                          CampaignFormLocators.primary_objective_input_attribute,
                                          primary_objective[1])
        self.click_on_element(
            CampaignFormLocators.primary_objective_value_set_button_locator)
        # SELECT SECONDARY OBJECTIVES AND SET VALUES
        secondary_objectives = campaign_data['campaign_goal_info'][
            'secondary_objectives'].split(',')
        for index, sec_obj in enumerate(secondary_objectives):
            objective = sec_obj.split(':')
            self.click_on_element_using_tag_attribute(self.div_tag,
                                                      CampaignFormLocators.goal_attribute,
                                                      objective[0])
            self.set_text_using_tag_attribute(self.input_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.secondary_objective_input_attribute,
                                              objective[1])
            self.click_on_element(
                    CampaignFormLocators.secondary_objective_value_set_button_locator)
            if index < len(secondary_objectives) - 1:
                self.click_on_element(CampaignFormLocators.secondary_objective_add_additional_locator)
        if audio is False:
            if edit_campaign is False:
                # IMPRESSION_CAPPING
                self.click_on_element(
                    CampaignFormLocators.impression_capping_section_locator)
                self.click_on_element(
                    CampaignFormLocators.default_impression_capping_checkbox)
        self.set_value_into_element(
            CampaignFormLocators.impression_input_field_locator,
            campaign_data['campaign_goal_info'][
                'impression_amount'])
        self.set_value_into_element(
            CampaignFormLocators.impression_click_input_field_locator,
            campaign_data['campaign_goal_info'][
                'impression_click'])
        self.set_value_into_element(
            CampaignFormLocators.impression_time_input_field_locator,
            campaign_data['campaign_goal_info']['impression_time'])
        if edit_campaign:
            self.set_value_into_specific_input_field_under_auto_optimisation(
                campaign_data['campaign_goal_info'][
                    'auto_opt_checkbox'][0],
                campaign_data['campaign_goal_info'][
                    'minimum_ctr'], "", True)
            self.set_value_into_specific_input_field_under_auto_optimisation(
                campaign_data['campaign_goal_info'][
                    'auto_opt_checkbox'][0],
                campaign_data['campaign_goal_info'][
                    'minimum_imp_per_placement_to_learn_ctr'],
                CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label)

    def provide_launch_date_and_budget_info(self, campaign_data,
                                            duplicate_campaign=False,
                                            start_campaign_approval=False,
                                            multi_platform=False,
                                            edit_campaign=False):
        self.click_on_element(CampaignFormLocators.date_field_locator)
        self.click_on_element(
            CampaignFormLocators.seven_days_date_range_locator)
        if duplicate_campaign is False:
            if multi_platform is False:
                self.click_on_element(
                    CampaignFormLocators.time_and_day_scheduling_locator)
                self.wait_for_presence_of_element(
                    CampaignFormLocators.specific_time_and_day_scheduling_locator)
                self.click_on_element(
                    CampaignFormLocators.specific_time_and_day_scheduling_locator)
                self.click_on_element(
                    CampaignFormLocators.time_and_day_scheduling_save_button_locator)
            if edit_campaign is False:
                self.set_value_into_specific_input_field(
                    CampaignFormLocators.bid_cpm_label,
                    campaign_data['launch_date_and_budget'][
                        'bid_cpm'])
                if campaign_data['launch_date_and_budget']['daily_budget_selected'] == "True":
                    self.click_on_element(CampaignFormLocators.daily_budget_radio_btn_data_qa)
                    self.set_value_into_specific_input_field(
                        CampaignFormLocators.budget_input_data_qa,
                        campaign_data['launch_date_and_budget']['daily_budget'])
                else:
                    self.set_value_into_specific_input_field(
                        CampaignFormLocators.budget_input_data_qa,
                        campaign_data['launch_date_and_budget']['total_budget'])
            if start_campaign_approval:
                self.click_on_element(
                    CampaignFormLocators.start_campaign_after_approval_locator)

    def provide_location_and_audiences_info_using_js(self, campaign_data, edit_campaign=False):
        if edit_campaign is False:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.country_label,
                option_to_select=campaign_data['location_and_audiences'][
                    'country_name'])
        # AUDIENCE
        if edit_campaign is False:
            self.scroll_to_specific_element(CampaignFormLocators.audience_section_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.audience_section_locator)
            self.click_on_element(CampaignFormLocators.audience_section_locator)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.audience_include_label_locator,
            option_to_select=campaign_data['location_and_audiences']['audience_include'])
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.audience_exclude_label_locator,
            option_to_select=campaign_data['location_and_audiences']['audience_exclude'])
        if edit_campaign is False:
            self.scroll_to_specific_element(CampaignFormLocators.demographic_section_locator)
            self.click_on_element(CampaignFormLocators.demographic_section_locator)
        # CITY
        time.sleep(self.ONE_SEC_DELAY)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.city_section_locator)
        self.click_on_element(CampaignFormLocators.city_section_locator)
        self.wait_for_presence_of_element(CampaignFormLocators.city_selection_locator)
        self.wait_for_visibility_of_element(CampaignFormLocators.city_selection_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.city_selection_locator)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.city_label_locator,
            option_to_select=campaign_data['location_and_audiences'][
                'city_name'])
        # AGE
        self.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=CampaignFormLocators.age_label,
                                                  option_to_select=campaign_data['location_and_audiences']['age'])
        # GENDER
        self.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=CampaignFormLocators.gender_label,
                                                  option_to_select=campaign_data['location_and_audiences']['gender'])
        # LANGUAGE
        self.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=CampaignFormLocators.languages_label,
                                                  option_to_select=campaign_data['location_and_audiences']['language'])
        # SEC (socio-economic class) groups
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.sec_socio_economic_class_groups_label,
            option_to_select=campaign_data['location_and_audiences']['sec'])
        # STATE
        self.wait_for_element_to_be_clickable(CampaignFormLocators.state_section_locator)
        self.click_on_element(CampaignFormLocators.state_section_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.state_selection_locator)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.state_label_locator,
            option_to_select=campaign_data['location_and_audiences']['state_name'])

    def provide_location_and_audiences_info_for_mul_platform_and_country_using_js(
            self,
            campaign_data,
            multi_platform=False,
            multi_country=False):
        if multi_platform is True:
            if multi_country is True:
                self.select_multiple_item_from_modal(campaign_data[
                                                         'location_and_audiences'][
                                                         'country_name'], CampaignFormLocators.country_label)
            else:
                self.select_from_modal(campaign_data[
                                           'location_and_audiences'][
                                           'country_name'], CampaignFormLocators.country_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['location_and_audiences'][
                                                     'country_name'], CampaignFormLocators.country_label)
            # For city loading
            city_values = campaign_data['location_and_audiences'][
                'city_name']
            self.click_on_element(
                CampaignFormLocators.city_section_locator)
            for city in city_values:
                self.wait_for_element_to_be_clickable(
                    CampaignFormLocators.city_selection_locator)
                self.click_on_element(
                    CampaignFormLocators.city_selection_locator)
                self.select_from_modal_for_multiple_country(
                    search_text=city)
            state_values = campaign_data['location_and_audiences'][
                'state_name']
            self.click_on_element(
                CampaignFormLocators.state_section_locator)
            for state in state_values:
                self.wait_for_element_to_be_clickable(
                    CampaignFormLocators.state_selection_locator)
                self.click_on_element(
                    CampaignFormLocators.state_selection_locator)
                self.select_from_modal_for_multiple_country(
                    search_text=state)
            self.click_on_element(
                CampaignFormLocators.demographic_section_locator)
            # AUDIENCE
            self.click_on_element(
                CampaignFormLocators.audience_section_locator)
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.audience_include_label_locator,
                option_to_select=campaign_data['location_and_audiences']['audience_include'])
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.audience_exclude_label_locator,
                option_to_select=campaign_data['location_and_audiences']['audience_exclude'])
            # AGE
            self.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=CampaignFormLocators.age_label,
                                                      option_to_select=campaign_data['location_and_audiences']['age'])
            # GENDER
            self.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=CampaignFormLocators.gender_label,
                                                      option_to_select=campaign_data['location_and_audiences'][
                                                          'gender'])
            # LANGUAGE
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.languages_label,
                option_to_select=campaign_data['location_and_audiences'][
                    'language'])
            # SEC (socio-economic class) groups
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.sec_socio_economic_class_groups_label,
                option_to_select=campaign_data['location_and_audiences']['sec'])

    def provide_location_and_audiences_info(self, campaign_data,
                                            edit_campaign=False):
        if edit_campaign is False:
            self.select_from_modal(campaign_data['location_and_audiences'][
                                       'country_name'], CampaignFormLocators.country_label)
        # CITY
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.city_section_locator)
        self.click_on_element(
            CampaignFormLocators.city_section_locator,
            locator_to_be_appeared=CampaignFormLocators.city_selection_locator)
        self.wait_for_presence_of_element(
            CampaignFormLocators.city_selection_locator)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.city_selection_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.city_selection_locator)
        self.click_on_element(
            CampaignFormLocators.city_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences'][
            'city_name'], selection_locator=CampaignFormLocators.city_selection_locator)
        # STATE
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.state_section_locator)
        self.click_on_element(
            CampaignFormLocators.state_section_locator,
            locator_to_be_appeared=CampaignFormLocators.state_selection_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.state_selection_locator)
        self.click_on_element(
            CampaignFormLocators.state_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences'][
            'state_name'], selection_locator=CampaignFormLocators.state_selection_locator)
        # AUDIENCE
        if edit_campaign is False:
            self.scroll_to_specific_element(
                CampaignFormLocators.audience_section_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.audience_section_locator)
            self.click_on_element(
                CampaignFormLocators.audience_section_locator)
        self.click_on_element(
            CampaignFormLocators.audience_include_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences'][
            'audience_include'], selection_locator=CampaignFormLocators.audience_include_selection_locator)
        self.click_on_element(
            CampaignFormLocators.audience_exclude_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences'][
            'audience_exclude'], selection_locator=CampaignFormLocators.audience_exclude_selection_locator)
        if edit_campaign is False:
            self.scroll_to_specific_element(
                CampaignFormLocators.demographic_section_locator)
            self.click_on_element(
                CampaignFormLocators.demographic_section_locator)
        # AGE
        self.select_from_modal(campaign_data['location_and_audiences']['age'], CampaignFormLocators.age_label)
        # GENDER
        self.select_from_modal(campaign_data['location_and_audiences']['gender'], CampaignFormLocators.gender_label)
        # LANGUAGE
        self.select_from_modal(campaign_data['location_and_audiences']['language'],
                               CampaignFormLocators.languages_label)
        # SEC (socio-economic class) groups
        self.select_from_modal(campaign_data['location_and_audiences']['sec'],
                               CampaignFormLocators.sec_socio_economic_class_groups_label)

    def provide_brand_safety_info(self, campaign_data):
        self.click_on_element(CampaignFormLocators.brand_safety_item_select)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.brand_safety_keywords_label,
            option_to_select=campaign_data['brand_safety'][
                'brand_safety_keywords'])
        time.sleep(2)
        self.click_on_element(CampaignFormLocators.contextual_targeting_app_site_section)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.contextual_keywords_label,
            option_to_select=campaign_data['brand_safety'][
                'contextual_keywords'])

    def provide_location_and_audiences_info_for_mul_platform_and_country(
            self,
            campaign_data,
            multi_platform=False,
            multi_country=False):
        if multi_platform is True:
            if multi_country is True:
                self.select_multiple_item_from_modal(campaign_data[
                                                         'location_and_audiences'][
                                                         'country_name'], CampaignFormLocators.country_label)
            else:
                self.select_from_modal(campaign_data[
                                           'location_and_audiences'][
                                           'country_name'], CampaignFormLocators.country_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['location_and_audiences'][
                                                     'country_name'], CampaignFormLocators.country_label)
            # For city loading
            city_values = campaign_data['location_and_audiences'][
                'city_name']
            self.click_on_element(
                CampaignFormLocators.city_section_locator)
            for city in city_values:
                self.wait_for_element_to_be_clickable(
                    CampaignFormLocators.city_selection_locator)
                self.click_on_element(
                    CampaignFormLocators.city_selection_locator)
                self.select_from_modal_for_multiple_country(
                    search_text=city)
            state_values = campaign_data['location_and_audiences'][
                'state_name']
            self.click_on_element(
                CampaignFormLocators.state_section_locator)
            for state in state_values:
                self.wait_for_element_to_be_clickable(
                    CampaignFormLocators.state_selection_locator)
                self.click_on_element(
                    CampaignFormLocators.state_selection_locator)
                self.select_from_modal_for_multiple_country(
                    search_text=state)
            self.click_on_element(
                CampaignFormLocators.demographic_section_locator)
            # AUDIENCE
            self.click_on_element(
                CampaignFormLocators.audience_section_locator)
            self.click_on_element(
                CampaignFormLocators.audience_include_selection_locator)
            self.select_from_modal(search_text=campaign_data['location_and_audiences'][
                'audience_include'], selection_locator=CampaignFormLocators.audience_include_selection_locator)
            self.click_on_element(
                CampaignFormLocators.audience_exclude_selection_locator)
            self.select_from_modal(search_text=campaign_data['location_and_audiences'][
                'audience_exclude'], selection_locator=CampaignFormLocators.audience_exclude_selection_locator)
            # AGE
            self.select_from_modal(campaign_data['location_and_audiences']['age'], CampaignFormLocators.age_label)
            # GENDER
            self.select_from_modal(campaign_data['location_and_audiences'][
                                       'gender'], CampaignFormLocators.gender_label)
            # LANGUAGE
            self.select_from_modal(campaign_data['location_and_audiences'][
                                       'language'], CampaignFormLocators.languages_label)
            # SEC (socio-economic class) groups
            self.select_from_modal(campaign_data['location_and_audiences']['sec'],
                                   CampaignFormLocators.sec_socio_economic_class_groups_label)

    def provide_platforms_telco_and_devices_info(self, campaign_data,
                                                 edit_campaign=False,
                                                 multi_country=False, audio=False):
        if audio is False:
            if edit_campaign is False:
                self.click_on_element(
                    CampaignFormLocators.platforms_telco_devices_group_locator,
                    locator_to_be_appeared=CampaignFormLocators.ad_placement_type_locator)
                self.wait_for_element_to_be_clickable(
                    CampaignFormLocators.ad_placement_type_locator)
                self.click_on_element(
                    CampaignFormLocators.ad_placement_type_locator)
            # PLACEMENT_TYPE
            self.check_uncheck_specific_checkbox(CampaignFormLocators.placement_type_app, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.placement_type_site, False)
            self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices'][
                                                     'ad_placement_type'], True)
        if audio:
            self.click_on_element(
                CampaignFormLocators.platforms_telco_devices_group_locator)
        # OPERATOR
        if multi_country is False:
            self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                       'mobile_operator'], CampaignFormLocators.mobile_operators_isp_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices'][
                                                     'mobile_operator'],
                                                 CampaignFormLocators.mobile_operators_isp_label)
        # IP ADDRESSES/RANGES
        if audio is False:
            if edit_campaign is False:
                self.click_on_element(
                    CampaignFormLocators.ip_ranges_section_locator)
            self.set_value_into_element(
                CampaignFormLocators.ip_ranges_input_field_locator,
                campaign_data['platforms_telco_and_devices'][
                    'ip_address/ranges'])
        # DEVICE
        self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                   'device_type'], CampaignFormLocators.device_type_label)
        # OS
        self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                   'device_os'], CampaignFormLocators.device_os_label)
        time.sleep(self.FIVE_SEC_DELAY)
        # BRAND
        if edit_campaign is False:
            self.click_on_element(
                CampaignFormLocators.device_brands_section_locator,
                locator_to_be_appeared=CampaignFormLocators.device_brands_selection_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_presence_of_element(
                CampaignFormLocators.device_brands_selection_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.device_brands_selection_locator)
        self.wait_for_presence_of_element(
            CampaignFormLocators.device_brands_selection_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.device_brands_selection_locator)
        self.scroll_to_specific_element(
            CampaignFormLocators.device_brands_selection_locator)
        self.click_on_element(
            CampaignFormLocators.device_brands_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                   'device_brand'],
                               selection_locator=CampaignFormLocators.device_brands_selection_locator)
        # MODEL
        time.sleep(self.TWO_SEC_DELAY)
        if edit_campaign is False:
            self.wait_for_presence_of_element(
                CampaignFormLocators.device_models_section_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.device_models_section_locator)
            self.click_on_element(
                CampaignFormLocators.device_models_section_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.device_models_selection_locator)
        self.wait_for_presence_of_element(
            CampaignFormLocators.device_models_selection_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.device_models_selection_locator)
        self.scroll_to_specific_element(
            CampaignFormLocators.device_models_selection_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(
            CampaignFormLocators.device_models_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                   'device_model'],
                               selection_locator=CampaignFormLocators.device_models_selection_locator)
        if audio is False:
            # BROWSER
            self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                       'browser'], CampaignFormLocators.device_browsers_label)
        # DEVICE_COST_RANGES
        self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                   'device_cost_range'], CampaignFormLocators.device_cost_ranges_label)

    def provide_platforms_telco_and_devices_info_using_js(self, campaign_data, edit_campaign=False,
                                                          multi_country=False):
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.platforms_telco_devices_group_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_placement_type_locator)
            self.click_on_element(CampaignFormLocators.ad_placement_type_locator)
        # PLACEMENT_TYPE
        self.check_uncheck_specific_checkbox("App", False)
        self.check_uncheck_specific_checkbox("Site", False)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['ad_placement_type'], True)
        # OPERATOR
        if multi_country is False:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.mobile_operators_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices']['mobile_operator'])
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices']['mobile_operator'],
                                                 CampaignFormLocators.mobile_operators_isp_label)

        # IP ADDRESSES/RANGES
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.ip_ranges_section_locator)
        self.set_value_into_element(CampaignFormLocators.ip_ranges_input_field_locator,
                                    campaign_data['platforms_telco_and_devices']['ip_address/ranges'])
        # DEVICE
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.device_type_label,
            option_to_select=campaign_data['platforms_telco_and_devices'][
                'device_type'])
        # OS
        self.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=CampaignFormLocators.device_os_label,
                                                  option_to_select=campaign_data['platforms_telco_and_devices'][
                                                      'device_os'])
        time.sleep(self.TWO_SEC_DELAY)
        # BRAND
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.device_brands_section_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_presence_of_element(CampaignFormLocators.device_brands_selection_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_brands_selection_locator)
        self.wait_for_presence_of_element(CampaignFormLocators.device_brands_selection_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.device_brands_selection_locator)
        self.scroll_to_specific_element(CampaignFormLocators.device_brands_selection_locator)
        time.sleep(self.TWO_SEC_DELAY)
        try:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.device_brands_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices'][
                    'device_brand'])
        except TimeoutException:
            self.wait_for_presence_of_element(CampaignFormLocators.device_brands_selection_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_brands_selection_locator)
            self.scroll_to_specific_element(CampaignFormLocators.device_brands_selection_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.device_brands_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices'][
                    'device_brand'])
        # MODEL
        time.sleep(self.TWO_SEC_DELAY)
        if edit_campaign is False:
            self.wait_for_presence_of_element(CampaignFormLocators.device_models_section_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_models_section_locator)
            self.click_on_element(CampaignFormLocators.device_models_section_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_models_selection_locator)
        self.wait_for_presence_of_element(CampaignFormLocators.device_models_selection_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.device_models_selection_locator)
        # temporary sleep to check if we still get error for device model selection
        time.sleep(self.ONE_SEC_DELAY)
        self.scroll_to_specific_element(CampaignFormLocators.device_models_selection_locator)
        time.sleep(self.TWO_SEC_DELAY)
        try:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.device_models_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices'][
                    'device_model'])
        except TimeoutException:
            self.wait_for_presence_of_element(CampaignFormLocators.device_models_selection_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_models_selection_locator)
            self.scroll_to_specific_element(CampaignFormLocators.device_models_selection_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.device_models_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices'][
                    'device_model'])

        # BROWSER
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.device_browsers_label,
            option_to_select=campaign_data['platforms_telco_and_devices'][
                'browser'])
        # DEVICE_COST_RANGES
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.device_cost_ranges_label,
            option_to_select=campaign_data['platforms_telco_and_devices'][
                'device_cost_range'])

    def provide_advanced_telecom_targeting_info(self, campaign_data,
                                                edit_campaign=False,
                                                multi_country=False):
        if edit_campaign is False:
            if (self.get_attribute_value(
                    CampaignFormLocators.advance_targeting_selection_locator,
                    "aria-expanded")
                    == "false"):
                self.click_on_element(
                    CampaignFormLocators.advance_targeting_selection_locator)
            # SIM_AMOUNT
            if (self.get_attribute_value(
                    CampaignFormLocators.sim_amount_selection_locator,
                    "aria-expanded")
                    == "false"):
                self.click_on_element(
                    CampaignFormLocators.sim_amount_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.one_sim_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_sims_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_sims_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_sims_checkbox_label, False)
        if (self.get_attribute_value(
                CampaignFormLocators.sim_amount_selection_locator,
                "aria-expanded")
                == "false"):
            self.click_on_element(
                CampaignFormLocators.sim_amount_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices'][
                                                 'sim_amount'], True)
        # DEVICE_CONNECTION
        if edit_campaign is False:
            if (self.get_attribute_value(
                    CampaignFormLocators.device_connection_selection_locator,
                    "aria-expanded")
                    == "false"):
                self.click_on_element(
                    CampaignFormLocators.device_connection_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_g_supporting_devices_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_g_supporting_devices_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_g_supporting_devices_checkbox_label, False)
        if (self.get_attribute_value(
                CampaignFormLocators.device_connection_selection_locator,
                "aria-expanded")
                == "false"):
            self.click_on_element(
                CampaignFormLocators.device_connection_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices'][
                                                 'device_connection'], True)
        if edit_campaign is False:
            self.click_on_device_and_network_connection_specific_radio_button(
                campaign_data[
                    'platforms_telco_and_devices'][
                    'device_connection'],
                CampaignFormLocators.only_radio_button_label)

        # NETWORK_CONNECTION
        if edit_campaign is False:
            if (self.get_attribute_value(
                    CampaignFormLocators.network_connection_selection_locator,
                    "aria-expanded")
                    == "false"):
                self.click_on_element(
                    CampaignFormLocators.network_connection_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_g_network_connection_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_g_network_connection_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_g_network_connection_checkbox_label, False)
        if (self.get_attribute_value(
                CampaignFormLocators.network_connection_selection_locator,
                "aria-expanded")
                == "false"):
            self.click_on_element(
                CampaignFormLocators.network_connection_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices'][
                                                 'network_connection'], True)
        if edit_campaign is False:
            self.click_on_device_and_network_connection_specific_radio_button(
                campaign_data[
                    'platforms_telco_and_devices'][
                    'network_connection'],
                CampaignFormLocators.only_radio_button_label)
        # MULTIPLE_SIM
        if multi_country is False:
            self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                       'multiple_operation_sim_card'],
                                   CampaignFormLocators.multiple_operator_sim_card_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices'][
                                                     'multiple_operation_sim_card'],
                                                 CampaignFormLocators.multiple_operator_sim_card_label)
        # CAMPAIGN PURPOSE FOR TELCO
        self.select_dropdown_value(CampaignFormLocators.campaign_purpose_label,
                                   dropdown_item=campaign_data['campaign_purpose'][
                                       'campaign_purpose'])
        self.select_dropdown_value(CampaignFormLocators.primary_operator_label,
                                   dropdown_item=campaign_data['campaign_purpose'][
                                       'primary_operator'])
        # DATA_CONSUMPTION
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.mobile_data_consumption_label_locator,
            option_to_select=campaign_data['platforms_telco_and_devices']['mobile_data_consumption'])
        # OPERATOR_CHURN
        if multi_country is False:
            self.select_from_modal(campaign_data['platforms_telco_and_devices'][
                                       'operator_churn'], CampaignFormLocators.operator_churn_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices'][
                                                     'operator_churn'], CampaignFormLocators.operator_churn_label)

    def provide_advanced_telecom_targeting_info_using_js(self, campaign_data, edit_campaign=False, multi_country=False):
        if edit_campaign is False:
            if (self.get_attribute_value(CampaignFormLocators.advance_targeting_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.advance_targeting_selection_locator)
            # SIM_AMOUNT
            if (self.get_attribute_value(CampaignFormLocators.sim_amount_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.sim_amount_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.one_sim_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_sims_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_sims_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_sims_checkbox_label, False)
        if (self.get_attribute_value(CampaignFormLocators.sim_amount_selection_locator, "aria-expanded")
                == "false"):
            self.click_on_element(CampaignFormLocators.sim_amount_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['sim_amount'], True)
        # DEVICE_CONNECTION
        if edit_campaign is False:
            if (self.get_attribute_value(CampaignFormLocators.device_connection_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.device_connection_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_g_supporting_devices_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_g_supporting_devices_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_g_supporting_devices_checkbox_label, False)
        if (self.get_attribute_value(CampaignFormLocators.device_connection_selection_locator, "aria-expanded")
                == "false"):
            self.click_on_element(CampaignFormLocators.device_connection_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['device_connection'], True)
        if edit_campaign is False:
            self.click_on_device_and_network_connection_specific_radio_button(campaign_data[
                                                                                  'platforms_telco_and_devices'][
                                                                                  'device_connection'],
                                                                              CampaignFormLocators.only_radio_button_label)

        # NETWORK_CONNECTION
        if edit_campaign is False:
            if (self.get_attribute_value(CampaignFormLocators.network_connection_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.network_connection_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_g_network_connection_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_g_network_connection_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_g_network_connection_checkbox_label, False)
        if (self.get_attribute_value(CampaignFormLocators.network_connection_selection_locator, "aria-expanded")
                == "false"):
            self.click_on_element(CampaignFormLocators.network_connection_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['network_connection'], True)
        if edit_campaign is False:
            self.click_on_device_and_network_connection_specific_radio_button(campaign_data[
                                                                                  'platforms_telco_and_devices'][
                                                                                  'network_connection'],
                                                                              CampaignFormLocators.only_radio_button_label)
        # MULTIPLE_SIM
        if multi_country is False:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.multiple_operator_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices']['multiple_operation_sim_card'])
            # CAMPAIGN PURPOSE FOR TELCO
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.campaign_purpose_label,
                option_to_select=campaign_data['campaign_purpose']['campaign_purpose'])
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.primary_operator_label,
                option_to_select=campaign_data['campaign_purpose']['primary_operator'])
        else:
            self.select_multiple_item_from_modal(
                campaign_data['platforms_telco_and_devices']['multiple_operation_sim_card'],
                CampaignFormLocators.multiple_operator_sim_card_label)
        # DATA_CONSUMPTION
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.mobile_data_consumption_label_locator,
            option_to_select=campaign_data['platforms_telco_and_devices']['mobile_data_consumption'])
        # OPERATOR_CHURN
        if multi_country is False:
            self.select_from_modal_form_using_js_code(
                field_label_or_xpath_or_data_qa=CampaignFormLocators.operator_churn_label_locator,
                option_to_select=campaign_data['platforms_telco_and_devices']['operator_churn'])
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices']['operator_churn'],
                                                 CampaignFormLocators.operator_churn_label)

    def provide_deals_packages_info(self, campaign_data,
                                    edit_campaign=False,
                                    ingame=False,
                                    multi_creative=False, audio=False):
        if edit_campaign is False:
            self.wait_for_presence_of_element(
                CampaignFormLocators.deals_packages_section_locator)
            self.wait_for_visibility_of_element(
                CampaignFormLocators.deals_packages_section_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.deals_packages_section_locator)
            self.click_on_element(
                CampaignFormLocators.deals_packages_section_locator)
        # AD_EXCHANGE
        if ingame is False:
            if edit_campaign is False:
                self.click_on_element(
                    CampaignFormLocators.ad_exchanges_section_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.ad_exchanges_uncheck_all_button_locator)
            self.click_on_element(
                CampaignFormLocators.ad_exchanges_uncheck_all_button_locator)
            self.check_uncheck_specific_checkbox(campaign_data['deals_and_packages'][
                                                     'ad_exchange_checkbox'], True)
        # PLACEMENT_POSITION
        if audio is False:
            if multi_creative is False:
                if edit_campaign is False:
                    self.click_on_element(
                        CampaignFormLocators.ad_placement_positions_section_locator)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.above_the_fold_checkbox_label, False)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.below_the_fold_checkbox_label, False)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.footer_sticky_ad_checkbox_label, False)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.full_screen_checkbox_label, False)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.header_sticky_ad_checkbox_label, False)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.other_checkbox_label, False)
                self.check_uncheck_specific_checkbox(CampaignFormLocators.sidebar_sticky_ad_checkbox_label, False)
                self.check_uncheck_specific_checkbox(campaign_data['deals_and_packages'][
                                                         'ad_placement_position_checkbox'], True)
        # PACKAGES
        if edit_campaign is False:
            self.click_on_element(
                CampaignFormLocators.packages_section_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.packages_uncheck_all_button_locator)
        self.click_on_element(
            CampaignFormLocators.packages_uncheck_all_button_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.package_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.packages_include_only_selector)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.packages_include_only_selector)
        self.click_on_element(
            CampaignFormLocators.packages_include_only_selector)
        if edit_campaign:
            self.click_on_element(
                CampaignFormLocators.packages_include_only_selector)
        # PRIVATE MARKETPLACE
        if edit_campaign is False:
            self.click_on_element(
                CampaignFormLocators.private_marketplace_section_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.private_marketplace_selection_locator)
        self.click_on_element(
            CampaignFormLocators.private_marketplace_selection_locator,
            locator_to_be_appeared=CampaignFormLocators.uncheck_all_button_locator)
        self.select_from_modal(search_text=campaign_data['deals_and_packages'][
            'private_marketplace'], selection_locator=CampaignFormLocators.private_marketplace_selection_locator)

    def provide_deals_packages_info_using_js(self, campaign_data, edit_campaign=False, ingame=False,
                                             multi_creative=False):
        if edit_campaign is False:
            self.wait_for_presence_of_element(CampaignFormLocators.deals_packages_section_locator)
            self.wait_for_visibility_of_element(CampaignFormLocators.deals_packages_section_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.deals_packages_section_locator)
            self.click_on_element(CampaignFormLocators.deals_packages_section_locator)
        # AD_EXCHANGE
        if ingame is False:
            if edit_campaign is False:
                self.click_on_element(CampaignFormLocators.ad_exchanges_section_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_exchanges_uncheck_all_button_locator)
            self.click_on_element(CampaignFormLocators.ad_exchanges_uncheck_all_button_locator)
            self.check_uncheck_specific_checkbox(campaign_data['deals_and_packages']['ad_exchange_checkbox'], True)
        # PLACEMENT_POSITION
        if multi_creative is False:
            if edit_campaign is False:
                self.click_on_element(CampaignFormLocators.ad_placement_positions_section_locator)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.above_the_fold_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.below_the_fold_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.footer_sticky_ad_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.full_screen_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.header_sticky_ad_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.other_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.sidebar_sticky_ad_checkbox_label, False)
            self.check_uncheck_specific_checkbox(campaign_data['deals_and_packages']['ad_placement_position_checkbox'],
                                                 True)
        # PACKAGES
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.packages_section_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.packages_uncheck_all_button_locator)
        self.click_on_element(CampaignFormLocators.packages_uncheck_all_button_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.package_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_visibility_of_element(CampaignFormLocators.packages_include_only_selector)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.packages_include_only_selector)
        self.click_on_element(CampaignFormLocators.packages_include_only_selector)
        if edit_campaign:
            self.click_on_element(CampaignFormLocators.packages_include_only_selector)
        # PRIVATE MARKETPLACE
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.private_marketplace_section_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.private_marketplace_selection_locator)
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.private_marketplace_label_locator,
            option_to_select=campaign_data['deals_and_packages']['private_marketplace'])

    def provide_landing_and_creatives_info(self, campaign_data):
        # CLICK URL
        self.wait_for_presence_of_element(
            CampaignFormLocators.click_url_input_field_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.click_url_input_field_locator)
        self.set_value_into_element(
            CampaignFormLocators.click_url_input_field_locator,
            campaign_data['landing_and_creatives']['click_url'])
        time.sleep(self.TWO_SEC_DELAY)
        # AD DOMAIN
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.ad_domain_field_locator)
        self.click_on_element(
            CampaignFormLocators.ad_domain_field_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_presence_of_element(
            CampaignFormLocators.ad_domain_search_field_locator)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.ad_domain_search_field_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.ad_domain_search_field_locator)
        self.set_value_into_element(
            CampaignFormLocators.ad_domain_search_field_locator,
            campaign_data['landing_and_creatives']['ad_domain'])
        self.wait_for_presence_of_element(
            CampaignFormLocators.ad_domain_search_field_locator).send_keys(
            Keys.ENTER)
        # CREATIVE_SELECTION
        self.select_from_modal(campaign_data['landing_and_creatives']['creative'],
                               CampaignFormLocators.selected_creative_sets_selection_label)
        time.sleep(self.TWO_SEC_DELAY)
        try:
            self.click_on_element(
                CampaignFormLocators.creative_toggle_icon_locator)
        except TimeoutException:
            self.select_from_modal(campaign_data['landing_and_creatives']['creative'],
                                   CampaignFormLocators.selected_creative_sets_selection_label)
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(
                CampaignFormLocators.creative_toggle_icon_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.scroll_to_specific_element(
            CampaignFormLocators.impression_per_creative_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(
            CampaignFormLocators.impression_per_creative_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(
            CampaignFormLocators.impression_add_more_button_locator)
        self.set_value_into_element(
            CampaignFormLocators.pixel_input_locator,
            campaign_data['landing_and_creatives'][
                "impression_tracking_pixel"])

    def provide_landing_and_creatives_info_using_js(self, campaign_data):
        # CLICK URL
        self.wait_for_presence_of_element(CampaignFormLocators.click_url_input_field_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.click_url_input_field_locator)
        self.set_value_into_element(CampaignFormLocators.click_url_input_field_locator,
                                    campaign_data['landing_and_creatives']['click_url'])
        time.sleep(self.TWO_SEC_DELAY)
        # AD DOMAIN
        self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_domain_field_locator)
        self.click_on_element(CampaignFormLocators.ad_domain_field_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_presence_of_element(CampaignFormLocators.ad_domain_search_field_locator)
        self.wait_for_visibility_of_element(CampaignFormLocators.ad_domain_search_field_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_domain_search_field_locator)
        self.set_value_into_element(CampaignFormLocators.ad_domain_search_field_locator,
                                    campaign_data['landing_and_creatives']['ad_domain'])
        self.wait_for_presence_of_element(CampaignFormLocators.ad_domain_search_field_locator).send_keys(Keys.ENTER)
        # CREATIVE_SELECTION
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.selected_creative_sets_selection_label,
            option_to_select=campaign_data['landing_and_creatives']['creative'])
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.creative_toggle_icon_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.impression_per_creative_locator,
                              locator_to_be_appeared=CampaignFormLocators.impression_add_more_button_locator)
        self.click_on_element(CampaignFormLocators.impression_add_more_button_locator,
                              locator_to_be_appeared=CampaignFormLocators.pixel_input_locator)
        self.set_value_into_element(CampaignFormLocators.pixel_input_locator,
                                    campaign_data['landing_and_creatives']["impression_tracking_pixel"])

    def click_save_cancel_or_draft(self, action=None):
        action = action.lower() if action else 'none'
        if action == 'save':
            self.scroll_to_specific_element(
                CampaignFormLocators.publish_button_locator)
            time.sleep(self.ONE_SEC_DELAY)
            self.wait_for_presence_of_element(
                CampaignFormLocators.publish_button_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.publish_button_locator)
            self.click_on_element(
                CampaignFormLocators.publish_button_locator)
        elif action == 'cancel':
            self.scroll_to_specific_element(
                CampaignFormLocators.cancel_button_locator)
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
        elif action == 'draft':
            self.scroll_to_specific_element(
                CampaignFormLocators.draft_button_locator)
            time.sleep(self.ONE_SEC_DELAY)
            self.wait_for_presence_of_element(
                CampaignFormLocators.draft_button_locator)
            self.wait_for_visibility_of_element(
                CampaignFormLocators.draft_button_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.draft_button_locator)
            try:
                self.click_on_element(
                    CampaignFormLocators.draft_button_locator)
                WebDriverWait(self.driver, 5).until(
                    EC.alert_is_present(),
                    'Timed out waiting for alert to appear')
                alert = self.driver.switch_to.alert
                alert.accept()
            except TimeoutException:
                print("Alert not present")
        else:
            pass

    def provide_campaign_data_and_save(self, campaign_data, action,
                                       edit_campaign=False,
                                       duplicate_campaign=False,
                                       multi_platform=False, ingame=False,
                                       multi_creative=False, audio=False):
        if duplicate_campaign:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data,
                                            duplicate_or_edit_campaign=True)
            step_printer("LAUNCH_DATE_AND_BUDGET")
            self.provide_launch_date_and_budget_info(campaign_data,
                                                     duplicate_campaign=True)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)
        else:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data,
                                            edit_campaign,
                                            multi_platform, ingame)
            step_printer("CAMPAIGN GOAL")
            self.provide_campaign_objective(campaign_data,
                                            edit_campaign, audio)
            step_printer("LAUNCH_DATE_AND_BUDGET")
            self.provide_launch_date_and_budget_info(campaign_data)
            step_printer("LOCATION_AND_AUDIENCES")
            self.provide_location_and_audiences_info(campaign_data,
                                                     edit_campaign)
            step_printer('BRAND SAFETY')
            self.provide_brand_safety_info(campaign_data)
            self.wait_for_presence_of_element(
                CampaignFormLocators.platforms_telco_devices_group_locator)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.platforms_telco_devices_group_locator)
            step_printer('PLATFORMS_TELCO_AND_DEVICES')
            self.provide_platforms_telco_and_devices_info(
                campaign_data,
                edit_campaign=edit_campaign, audio=audio)
            step_printer('ADVANCED_TELECOM_TARGETING')
            self.provide_advanced_telecom_targeting_info(
                campaign_data,
                edit_campaign)
            step_printer('DEALS_PACKAGES')
            self.provide_deals_packages_info(campaign_data,
                                             edit_campaign,
                                             ingame,
                                             multi_creative, audio)
            step_printer('LANDING_AND_CREATIVES')
            self.provide_landing_and_creatives_info(campaign_data)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)

    def provide_campaign_data_and_save_using_js(self, campaign_data, action, edit_campaign=False,
                                                duplicate_campaign=False, multi_platform=False, ingame=False,
                                                multi_creative=False, draft_campaign=False):

        if draft_campaign:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data, duplicate_or_edit_campaign=False)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)
        elif duplicate_campaign:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data, duplicate_or_edit_campaign=True)
            step_printer("LAUNCH_DATE_AND_BUDGET")
            self.provide_launch_date_and_budget_info(campaign_data, duplicate_campaign=True)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)
        else:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data, edit_campaign, multi_platform, ingame)
            step_printer("CAMPAIGN GOAL")
            self.provide_campaign_objective(campaign_data, edit_campaign)
            step_printer("LAUNCH_DATE_AND_BUDGET")
            self.provide_launch_date_and_budget_info(campaign_data)
            step_printer("LOCATION_AND_AUDIENCES")
            self.provide_location_and_audiences_info_using_js(campaign_data, edit_campaign)
            self.wait_for_presence_of_element(CampaignFormLocators.platforms_telco_devices_group_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.platforms_telco_devices_group_locator)
            step_printer('PLATFORMS_TELCO_AND_DEVICES')
            self.provide_platforms_telco_and_devices_info_using_js(campaign_data, edit_campaign)
            step_printer('ADVANCED_TELECOM_TARGETING')
            self.provide_advanced_telecom_targeting_info_using_js(campaign_data, edit_campaign)
            step_printer('DEALS_PACKAGES')
            self.provide_deals_packages_info_using_js(campaign_data, edit_campaign, ingame, multi_creative)
            step_printer('LANDING_AND_CREATIVES')
            self.provide_landing_and_creatives_info_using_js(campaign_data)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)

    def provide_mandatory_campaign_data_and_save(self, campaign_data,
                                                 action=None):
        step_printer("NAME_AND_TYPE")
        self.provide_name_and_type_info(campaign_data)
        step_printer("CAMPAIGN GOAL")
        self.provide_campaign_objective(campaign_data)
        step_printer("LAUNCH_DATE_AND_BUDGET")
        self.provide_launch_date_and_budget_info(campaign_data)
        step_printer("LOCATION_AND_AUDIENCES")
        self.provide_location_and_audiences_info_using_js(campaign_data)
        step_printer('LANDING_AND_CREATIVES')
        self.provide_landing_and_creatives_info_using_js(campaign_data)
        step_printer('SAVE, CANCEL OR DRAFT')
        self.click_save_cancel_or_draft(action)

    def provide_mandatory_field_campaign_data_and_save(self, campaign_data, action):
        step_printer("NAME_AND_TYPE")
        creative_type = campaign_data['name_and_type'][
            'creative_type']
        try:
            self.wait_for_presence_of_element(
                CampaignFormLocators.creative_type_dropdown_locator,
                self.HALF_MINUTE)
            self.wait_for_element_to_be_clickable(
                CampaignFormLocators.creative_type_dropdown_locator)
        finally:
            self.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=creative_type)
        self.wait_for_presence_of_element(
            CampaignFormLocators.creative_type_dropdown_locator,
            self.HALF_MINUTE)
        self.set_value_into_element(
            CampaignFormLocators.campaign_name_input_field_locator,
            campaign_data['name_and_type']['campaign_name'])
        step_printer("CAMPAIGN GOAL")
        self.click_on_element(
            CampaignFormLocators.campaign_goal.format(
                campaign_data['campaign_goal_info'][
                    'campaign_goal']),
            locator_initialization=True)
        # SELECT PRIMARY OBJECTIVE AND SET VALUE
        primary_objective = campaign_data['campaign_goal_info'][
            'primary_objective'].split(':')
        self.click_on_element_using_tag_attribute(self.div_tag,
                                                  CampaignFormLocators.goal_attribute,
                                                  primary_objective[0])
        self.set_text_using_tag_attribute(self.input_tag,
                                          self.id_attribute,
                                          CampaignFormLocators.primary_objective_input_attribute,
                                          primary_objective[1])
        self.click_on_element(
            CampaignFormLocators.primary_objective_value_set_button_locator)
        step_printer("LAUNCH_DATE_AND_BUDGET")
        self.click_on_element(CampaignFormLocators.date_field_locator)
        self.click_on_element(
            CampaignFormLocators.seven_days_date_range_locator)
        self.set_value_into_specific_input_field(
            CampaignFormLocators.bid_cpm_label,
            campaign_data['launch_date_and_budget'][
                'bid_cpm'])
        if campaign_data['launch_date_and_budget']['daily_budget_selected'] == "True":
            self.click_on_element(CampaignFormLocators.daily_budget_radio_btn_data_qa)
            self.set_value_into_specific_input_field(
                CampaignFormLocators.budget_input_data_qa,
                campaign_data['launch_date_and_budget']['daily_budget'])
        else:
            self.set_value_into_specific_input_field(
                CampaignFormLocators.budget_input_data_qa,
                campaign_data['launch_date_and_budget']['total_budget'])
        step_printer("LOCATION_AND_AUDIENCES")
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.country_label,
            option_to_select=campaign_data['location_and_audiences'][
                'country_name'])
        step_printer('LANDING_AND_CREATIVES')
        # CLICK URL
        self.wait_for_presence_of_element(CampaignFormLocators.click_url_input_field_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.click_url_input_field_locator)
        self.set_value_into_element(CampaignFormLocators.click_url_input_field_locator,
                                    campaign_data['landing_and_creatives']['click_url'])
        time.sleep(self.TWO_SEC_DELAY)
        # AD DOMAIN
        self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_domain_field_locator)
        self.click_on_element(CampaignFormLocators.ad_domain_field_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_presence_of_element(CampaignFormLocators.ad_domain_search_field_locator)
        self.wait_for_visibility_of_element(CampaignFormLocators.ad_domain_search_field_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_domain_search_field_locator)
        self.set_value_into_element(CampaignFormLocators.ad_domain_search_field_locator,
                                    campaign_data['landing_and_creatives']['ad_domain'])
        self.wait_for_presence_of_element(CampaignFormLocators.ad_domain_search_field_locator).send_keys(Keys.ENTER)
        # CREATIVE_SELECTION
        self.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.selected_creative_sets_selection_label,
            option_to_select=campaign_data['landing_and_creatives']['creative'])
        step_printer('SAVE, CANCEL OR DRAFT')
        self.click_save_cancel_or_draft(action)

    def get_unavailable_creative_type_alert_message(self):
        self.wait_for_presence_of_element(
            CampaignFormLocators.unavailable_creative_type_alert_locator)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.unavailable_creative_type_alert_locator)
        return self.get_element_text(
            CampaignFormLocators.unavailable_creative_type_alert_locator)

    def provide_campaign_data_and_save_for_multiple_platform_and_multiple_country(
            self, campaign_data, action,
            multi_platform=False,
            multi_country=False):
        step_printer("NAME_AND_TYPE")
        self.provide_name_and_type_info(campaign_data,
                                        multi_platform=multi_platform)
        step_printer("CAMPAIGN GOAL")
        self.provide_campaign_objective(campaign_data)
        step_printer("LAUNCH_DATE_AND_BUDGET")
        self.provide_launch_date_and_budget_info(campaign_data,
                                                 multi_platform=multi_platform)
        step_printer("LOCATION_AND_AUDIENCES")
        self.provide_location_and_audiences_info_for_mul_platform_and_country_using_js(
            campaign_data,
            multi_platform=multi_platform,
            multi_country=multi_country)
        if multi_platform is False:
            step_printer('PLATFORMS_TELCO_AND_DEVICES')
            self.provide_platforms_telco_and_devices_info_using_js(
                campaign_data,
                multi_country=multi_country)
            step_printer('ADVANCED_TELECOM_TARGETING')
            self.provide_advanced_telecom_targeting_info_using_js(
                campaign_data,
                multi_country=multi_country)
            step_printer('DEALS_PACKAGES')
            self.provide_deals_packages_info_using_js(campaign_data)
        step_printer('LANDING_AND_CREATIVES')
        self.provide_landing_and_creatives_info_using_js(campaign_data)
        step_printer('SAVE, CANCEL OR DRAFT')
        self.click_save_cancel_or_draft(action)

    def get_campaign_name_and_type(self):
        time.sleep(self.ONE_SEC_DELAY)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.creative_type_dropdown_locator)
        campaign_information['name_and_type'][
            'platform_type'] = self.get_attribute_value(
            CampaignFormLocators.platform_type_locator, "title")
        campaign_information['name_and_type']['creative_type'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.type_field_id)
        campaign_information['name_and_type'][
            'campaign_type'] = self.get_element_text(
            CampaignFormLocators.campaign_type_dropdown_locator)
        campaign_information['name_and_type']['campaign_name'] = \
            self.get_text_using_tag_attribute(self.input_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.campaign_field_id)

    def get_campaign_objective(self, campaign_data,
                               goal_not_available=False, audio=False):
        if goal_not_available is False:
            # GET CAMPAIGN GOAL
            special_chars = ['{', '}', '"']
            campaign_information['campaign_goal_info'][
                'campaign_goal'] = self.get_text_using_tag_attribute(
                self.input_tag,
                self.id_attribute,
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
                    campaign_information[
                        'campaign_goal_info'][
                        'primary_objective'].replace(
                        sc, "")
                campaign_information['campaign_goal_info'][
                    'secondary_objectives'] = \
                    campaign_information[
                        'campaign_goal_info'][
                        'secondary_objectives'].replace(
                        sc, "")
            campaign_information['campaign_goal_info'][
                'pre_optimisation'] = self.get_attribute_value(
                CampaignFormLocators.primary_objective_optimisation_slider_locator,
                'checked')
            # Auto Opt Checkbox
            campaign_information['campaign_goal_info'][
                'auto_opt_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.auto_optimisation_section_id,
                multiple=True)
            if audio is False:
                # CTR
                campaign_information['campaign_goal_info'][
                    'minimum_ctr'] = self.get_value_from_specific_input_field_under_auto_optimisation(
                    campaign_data['campaign_goal_info'][
                        'auto_opt_checkbox'][0],
                    "", first_field_value=True)
                campaign_information['campaign_goal_info'][
                    'minimum_imp_per_placement_to_learn_ctr'] = \
                    self.get_value_from_specific_input_field_under_auto_optimisation(
                        campaign_data['campaign_goal_info'][
                            'auto_opt_checkbox'][
                            0],
                        CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label)
                # SR
                campaign_information['campaign_goal_info'][
                    'minimum_sr'] = self.get_value_from_specific_input_field_under_auto_optimisation(
                    campaign_data['campaign_goal_info'][
                        'auto_opt_checkbox'][1],
                    "", first_field_value=True)
                campaign_information['campaign_goal_info'][
                    'minimum_imp_per_placement_to_learn_sr'] = \
                    self.get_value_from_specific_input_field_under_auto_optimisation(
                        campaign_data['campaign_goal_info'][
                            'auto_opt_checkbox'][
                            1],
                        CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label)
            # IMPRESSION
            campaign_information['campaign_goal_info'][
                'impression_amount'] = self.get_text_using_tag_attribute(
                self.input_tag, self.class_attribute,
                CampaignFormLocators.impression_field_class)
            campaign_information['campaign_goal_info'][
                'impression_click'] = self.get_text_using_tag_attribute(
                self.input_tag, self.class_attribute,
                CampaignFormLocators.
                    impression_click_field_class)
            campaign_information['campaign_goal_info'][
                'impression_time'] = self.get_text_using_tag_attribute(
                self.input_tag, self.class_attribute,
                CampaignFormLocators.capping_amount_field_class)

    def get_campaign_launch_date_and_budget(self):
        campaign_information['launch_date_and_budget']['bid_cpm'] = \
            self.get_text_using_tag_attribute(self.input_tag,
                                              self.id_attribute,
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
        campaign_information['launch_date_and_budget']['daily_budget_pacing'] = \
            self.get_checkbox_status(CampaignFormLocators.budget_pacing_even_data_qa)

    def get_campaign_location_and_audiences(self):
        campaign_information['location_and_audiences'][
            'country_name'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.country_label)
        campaign_information['location_and_audiences'][
            'city_name'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.city_label_locator)
        campaign_information['location_and_audiences'][
            'state_name'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.state_label_locator)
        campaign_information['location_and_audiences'][
            'audience_include'] = self.get_element_text(
            CampaignFormLocators.audience_include_value_locator)
        campaign_information['location_and_audiences'][
            'audience_exclude'] = self.get_element_text(
            CampaignFormLocators.audience_exclude_value_locator)
        campaign_information['location_and_audiences'][
            'age'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.age_label)
        campaign_information['location_and_audiences'][
            'gender'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.gender_label)
        campaign_information['location_and_audiences'][
            'language'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.languages_label)
        campaign_information['location_and_audiences'][
            'sec'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.sec_socio_economic_class_groups_label)

    def get_campaign_brand_safety(self):
        campaign_information['brand_safety']['brand_safety_keywords'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.brand_safety_keywords_label)
        campaign_information['brand_safety']['contextual_keywords'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.contextual_keywords_label)

    def get_campaign_location_and_audiences_for_multiple_platforms(self):
        campaign_information['location_and_audiences'][
            'country_name'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.country_label)

    def get_campaign_purpose(self):
        campaign_information['campaign_purpose']['campaign_purpose'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.campaign_purpose_field_id)
        campaign_information['campaign_purpose']['primary_operator'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.primary_operator_field_id)

    def get_campaign_platforms_telco_and_devices(self, campaign_data, audio=False):
        debug_mode = "JENKINS_URL" not in os.environ
        if audio is False:
            campaign_information['platforms_telco_and_devices'][
                'ad_placement_type'] = self.get_selected_checkbox_name_from_a_section(
                section_div_id=CampaignFormLocators.ad_placement_type_section_id)
            campaign_information['platforms_telco_and_devices'][
                'ip_address/ranges'] = self.get_element_text(
                CampaignFormLocators.ip_ranges_input_field_locator)
        campaign_information['platforms_telco_and_devices'][
            'mobile_operator'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.mobile_operators_isp_label)
        campaign_information['platforms_telco_and_devices'][
            'device_type'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.device_type_label)
        campaign_information['platforms_telco_and_devices'][
            'device_os'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.device_os_label)
        campaign_information['platforms_telco_and_devices'][
            'device_brand'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.device_brands_label)
        campaign_information['platforms_telco_and_devices'][
            'device_model'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.device_models_label)
        if audio is False:
            campaign_information['platforms_telco_and_devices'][
                'browser'] = self.get_selected_options_using_js_code(
                CampaignFormLocators.device_browsers_label)
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
            'multiple_operation_sim_card'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.multiple_operator_sim_card_label)
        campaign_information['platforms_telco_and_devices'][
            'mobile_data_consumption'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.mobile_data_consumption_label)
        campaign_information['platforms_telco_and_devices'][
            'operator_churn'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.operator_churn_label)

    def get_campaign_deals_and_packages(self, ingame=False, audio=False):
        if ingame is False:
            campaign_information['deals_and_packages'][
                'ad_exchange_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.exchanges_section_id)
        else:
            campaign_information['deals_and_packages'][
                'ad_exchange_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.exchanges_section_id,
                multiple=True)
        if audio is False:
            campaign_information['deals_and_packages'][
                'ad_placement_position_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.ad_placement_positions_section_id)
        # PACKAGE
        self.wait_for_visibility_of_element(
            CampaignFormLocators.package_locator)
        campaign_information['deals_and_packages'][
            'packages'] = self.get_selected_checkbox_name_from_a_section(
            CampaignFormLocators.packages_section_id,
            multiple=True)
        campaign_information['deals_and_packages'][
            'package_include'] = self.get_element_text(
            CampaignFormLocators.packages_include_only_selector)
        # PRIVATE MARKETPLACE
        campaign_information['deals_and_packages'][
            'private_marketplace'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.private_marketplace_label_locator)

    def get_campaign_landing_and_creatives(self):
        campaign_information['landing_and_creatives']['click_url'] = \
            self.get_text_using_tag_attribute(self.input_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.click_url_field_id)
        campaign_information['landing_and_creatives']['ad_domain'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.ad_domain_field_id)
        campaign_information['landing_and_creatives'][
            'creative'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.selected_creative_sets_selection_label)
        self.click_on_element(
            CampaignFormLocators.creative_toggle_icon_locator)
        self.wait_for_visibility_of_element(
            CampaignFormLocators.pixel_get_input_locator)
        campaign_information['landing_and_creatives'][
            'impression_tracking_pixel'] = self.get_element_text(
            CampaignFormLocators.pixel_get_input_locator)

    def get_campaign_landing_and_creatives_only(self):
        self.reset_campaign_information()
        campaign_information['landing_and_creatives']['click_url'] = \
            self.get_text_using_tag_attribute(self.input_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.click_url_field_id)
        campaign_information['landing_and_creatives']['ad_domain'] = \
            self.get_text_using_tag_attribute(self.span_tag,
                                              self.id_attribute,
                                              CampaignFormLocators.ad_domain_field_id)
        campaign_information['landing_and_creatives'][
            'creative'] = self.get_selected_options_using_js_code(
            CampaignFormLocators.selected_creative_sets_selection_label)
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

    def get_campaign_information_with_multiple_attempt(self, campaign_data,
                                                       multi_platform=False,
                                                       multi_country=False,
                                                       draft_campaign=False):
        self.reset_campaign_information()
        if self.get_campaign_information(campaign_data, multi_platform,
                                         multi_country,
                                         draft_campaign) is False:
            self.driver.refresh()
            self.get_campaign_information(campaign_data,
                                          multi_platform,
                                          multi_country,
                                          draft_campaign)
        return campaign_information

    def get_campaign_information(self, campaign_data, multi_platform=False,
                                 multi_country=False,
                                 draft_campaign=False, audio=False):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data, audio=audio)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences()
        self.get_campaign_brand_safety()
        if multi_platform is False:
            if draft_campaign is False:
                self.get_campaign_platforms_telco_and_devices(
                    campaign_data, audio)
                if multi_country is False:
                    self.get_campaign_purpose()
                self.get_campaign_deals_and_packages(audio=audio)
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def get_campaign_mandatory_information(self, campaign_data):
        self.reset_campaign_information()
        del campaign_information['brand_safety']
        del campaign_information['campaign_purpose']
        del campaign_information['deals_and_packages']
        del campaign_information['platforms_telco_and_devices']
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences()
        self.get_campaign_landing_and_creatives()
        return campaign_information

    def get_campaign_information_for_multiple_country(self, campaign_data):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences()
        self.get_campaign_platforms_telco_and_devices(campaign_data)
        self.get_campaign_deals_and_packages()
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def get_campaign_information_for_draft_campaign(self, campaign_data,
                                                    goal_not_available=False):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data, goal_not_available)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences()
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def get_campaign_information_for_ingame_campaign(self, campaign_data,
                                                     ingame=False):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences()
        self.get_campaign_platforms_telco_and_devices(campaign_data)
        self.get_campaign_purpose()
        self.get_campaign_deals_and_packages(ingame)
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
        self.wait_for_presence_of_element(
            CampaignFormLocators.cancel_button_locator)
        self.wait_for_element_to_be_clickable(
            CampaignFormLocators.cancel_button_locator)
        try:
            self.click_on_element(
                CampaignFormLocators.cancel_button_locator)
            WebDriverWait(self.driver, 10).until(
                EC.alert_is_present(),
                'Timed out waiting for alert to appear')
            alert = self.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("Alert not present")
        finally:
            self.driver.refresh()
        return campaign_information

    def get_campaign_information_for_multiple_creatives(self,
                                                        campaign_data):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences_for_multiple_platforms()
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def get_campaign_information_for_multiple_platforms(self,
                                                        campaign_data,
                                                        goal_not_available=False):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data, goal_not_available)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences_for_multiple_platforms()
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def get_campaign_information_for_multiple_platforms_multiple_countries(
            self, campaign_data,
            goal_not_available=False):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_objective(campaign_data, goal_not_available)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_location_and_audiences_for_multiple_platforms()
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def click_on_device_and_network_connection_specific_radio_button(self,
                                                                     checkbox_name,
                                                                     radio_button_name):
        locator = (By.XPATH,
                   "//label[normalize-space()='" + checkbox_name + "']/..//following-sibling::div[1]"
                                                                   "//label[""normalize-space()='" +
                   radio_button_name + "']")

        self.click_on_element(locator)

    def set_value_into_specific_input_field_under_auto_optimisation(self,
                                                                    checkbox_name,
                                                                    text,
                                                                    field_name="",
                                                                    first_field=False):
        if first_field:
            locator = (By.XPATH,
                       "(//label[normalize-space()='" + checkbox_name + "']/..//..//input)[2]")
        else:
            locator = (By.XPATH,
                       "//label[normalize-space()='" + checkbox_name + "']/..//..//label[normalize-space("
                                                                       ")='" + field_name + "']/..//input")
        self.set_value_into_element(locator, text)

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

    def navigate_to_ad_exchanges_section(self):
        self.click_on_element(
            CampaignFormLocators.deals_packages_section_locator)
        self.click_on_element(
            CampaignFormLocators.ad_exchanges_section_locator)

    def get_campaign_information_with_multiple_attempt_for_mass_edit(self, campaign_data):
        self.reset_campaign_information()
        if self.get_campaign_information_edit(campaign_data) is False:
            self.driver.refresh()
            self.get_campaign_information_edit(campaign_data)
        return campaign_information

    def get_campaign_information_edit(self, campaign_data):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        time.sleep(self.ONE_SEC_DELAY)
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_brand_safety()
        self.get_campaign_platforms_telco_and_devices(campaign_data)
        self.get_campaign_purpose()
        self.get_campaign_landing_and_creatives()
        self.click_on_element(
            CampaignFormLocators.button_group_locator)
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

    def get_bid_in_usd(self):
        bid_currency = self.get_element_text(CampaignFormLocators.bid_cpm_currency_locator)
        if bid_currency == "$":
            bid_in_usd = self.get_bid_cpm()
        else:
            bid_in_usd = self.get_element_text(CampaignFormLocators.bid_cpm_in_usd_locator)
            bid_in_usd = re.sub(r'[^\d.]', '', bid_in_usd)
        return bid_in_usd

    @staticmethod
    def get_calculated_bid(bid_amount, updated_main_margin):
        calculated_bid = float(bid_amount) * (1 - updated_main_margin)
        calculated_bid = math.floor(calculated_bid * 100) / 100
        return calculated_bid

    def switch_budget(self, selected_budget):
        if selected_budget == 'total':
            self.click_on_element(CampaignFormLocators.daily_budget_radio_btn_data_qa)
        else:
            self.click_on_element(CampaignFormLocators.total_budget_radio_btn_data_qa)

    def get_budget_amount(self):
        budget = self.get_attribute_value(CampaignFormLocators.budget_input_data_qa, "value")
        budget = budget.replace(",", "")
        return budget

    def get_estimated_budget(self):
        time.sleep(self.TWO_SEC_DELAY)
        budget = self.get_element_text(CampaignFormLocators.estimated_budget_data_qa)
        return re.sub(r'[^\d.]', '', re.sub(r'\(.*?\)', '', budget))

    def get_remaining_budget(self):
        time.sleep(self.ONE_SEC_DELAY)
        budget = self.get_element_text(CampaignFormLocators.remaining_budget_data_qa)
        return re.sub(r'[^\d.]', '', re.sub(r'\(.*?\)', '', budget))

    def get_bid_cpm(self):
        bid_cpm = self.get_attribute_value(CampaignFormLocators.bid_cpm_label, "value")
        return bid_cpm

    def get_creatives_bids(self):
        creatives_bids = self.get_text_or_value_from_list(CampaignFormLocators.creatives_bids_locator,
                                                          attribute_name="value")
        return creatives_bids

    def calculate_remaining_days(self, db_connection, campaign_id):
        date_to_str = str(CampaignUtils.pull_campaign_end_date_from_db(db_connection, campaign_id))
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
        current_date_str = self.get_current_date_with_specific_format('%Y-%m-%d')
        current_date = datetime.strptime(current_date_str, '%Y-%m-%d').date()
        if date_to > current_date:
            remaining_days = (date_to - current_date).days
        else:
            remaining_days = 0
        remaining_days = max(0, remaining_days + 1)
        return remaining_days

    def get_selected_budget(self):
        element = self.wait_for_presence_of_element(CampaignFormLocators.total_budget_radio_btn_data_qa)
        if element.is_selected():
            return "total"
        return "daily"

    def get_total_daily_remaining_budget(self, selected_budget, daily_spent, total_spent):
        budget_from_ui = self.get_budget_amount()
        if selected_budget == 'total':
            remaining_total_budget = float(budget_from_ui) - total_spent
            return round(remaining_total_budget, 2)
        else:
            remaining_daily_budget = float(budget_from_ui) - daily_spent
            return round(remaining_daily_budget, 2)

    def get_total_daily_estimated_budget_for_live_campaign(self, selected_budget, estimated_budget, total_spent,
                                                           daily_spent, remaining_days, set_value=True):
        if selected_budget == 'total':
            if set_value:
                self.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa, estimated_budget)
            estimated_daily_budget = (float(estimated_budget) - total_spent + daily_spent) / float(remaining_days)
            return estimated_daily_budget
        else:
            remaining_daily_budget = float(estimated_budget) - daily_spent
            if set_value:
                self.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa, estimated_budget)
            estimated_total_budget = \
                total_spent + remaining_daily_budget + (float(estimated_budget) * float(remaining_days - 1))
            return estimated_total_budget
