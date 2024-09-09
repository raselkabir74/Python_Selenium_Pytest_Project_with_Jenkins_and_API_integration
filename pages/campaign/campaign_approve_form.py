import time
import math
import re

from pages.base_page import BasePage
from locators.campaign.campaign_approve_form_locator import \
    CampaignApproveLocators
from configurations import generic_modules
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

campaign_approve_information = {}
campaign_approve_url = '{}/admin/acampaigns/view?id={}'


class DspDashboardCampaignApprove(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_approve_campaign_page(self, campaign_id):
        self.driver.get(campaign_approve_url.format(generic_modules.BASE_URL, campaign_id))

    def provide_main_settings_info(self, main_settings_data):
        # INSERTION ORDER
        self.select_dropdown_value(CampaignApproveLocators.insertion_order_label,
                                   dropdown_item=main_settings_data['io'])
        # ADVERTISER NAME
        self.select_dropdown_value(CampaignApproveLocators.advertiser_name_label,
                                   dropdown_item=main_settings_data['advertiser_name'])
        # ADVERTISEMENT CATEGORY
        self.deselect_all_dropdown_value(
            CampaignApproveLocators.advertiser_category_label)
        self.select_dropdown_value(CampaignApproveLocators.advertiser_category_label, dropdown_item=main_settings_data[
            'advertisement_category'])

    def provide_reporting_and_budget_info(self, reporting_and_budget_data):
        # EMAIL REPORT
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.email_report_label,
                                             bool(reporting_and_budget_data['email_report'][
                                                      'is_checked']))
        self.select_dropdown_value(CampaignApproveLocators.email_report_frequency_label,
                                   dropdown_item=reporting_and_budget_data['email_report'][
                                       'report_frequency'])
        self.select_dropdown_value(CampaignApproveLocators.email_report_hour_label,
                                   dropdown_item=reporting_and_budget_data['email_report'][
                                       'report_hour'])
        self.select_dropdown_value(CampaignApproveLocators.email_report_day_label,
                                   dropdown_item=reporting_and_budget_data['email_report'][
                                       'report_day'])
        # GROUP BY IO
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.group_by_io_label,
                                             bool(reporting_and_budget_data['group_by_io'][
                                                      'is_checked']))
        self.click_on_element(
            CampaignApproveLocators.button_alert_ok_locator)
        self.select_dropdown_value(CampaignApproveLocators.group_by_io_label,
                                   dropdown_item=reporting_and_budget_data['group_by_io'][
                                       'view_by'])
        # EMAIL ATTACHMENT
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.email_attachments_label,
                                             bool(reporting_and_budget_data['email_attachment'][
                                                      'xls'][
                                                      'is_checked']), value="xls")
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.email_attachments_label,
                                             bool(reporting_and_budget_data['email_attachment'][
                                                      'pdf'][
                                                      'is_checked']), value="pdf")
        # GENERATE INSIGHT REPORT
        self.select_dropdown_value(CampaignApproveLocators.generate_insight_report_label,
                                   dropdown_item=reporting_and_budget_data[
                                       'generate_insight_report'])
        # TECH FEE
        self.set_value_into_element(
            CampaignApproveLocators.tech_fee_locator,
            reporting_and_budget_data['tech_fee'])

    def provide_optimisation_and_tracking_info(self,
                                               optimization_and_tracking_data):
        # IMPRESSION PERFORMANCE METRIC
        self.click_on_element(
            CampaignApproveLocators.impression_performance_metric_locator)
        self.set_value_into_element(
            CampaignApproveLocators.impression_performance_metric_viewability_locator,
            optimization_and_tracking_data[
                'impression_performance_metric'][
                'viewability'])
        self.set_value_into_element(
            CampaignApproveLocators.impression_performance_metric_ctr,
            optimization_and_tracking_data[
                'impression_performance_metric'][
                'ctr'])
        self.set_value_into_element(
            CampaignApproveLocators.impression_performance_metric_vcr,
            optimization_and_tracking_data[
                'impression_performance_metric'][
                'vcr'])
        # CUSTOM IMPRESSION TRACKING
        self.click_on_element(
            CampaignApproveLocators.custom_impression_tracking_locator)
        self.select_dropdown_value_from_div(self.id_attribute,
                                            CampaignApproveLocators.custom_impression_tracking_dropdown_id,
                                            dropdown_item=optimization_and_tracking_data[
                                                'custom_impression_tracking'][
                                                'option'])
        self.click_on_element(
            CampaignApproveLocators.add_more_custom_impression_tracking_locator)
        self.set_value_into_element(
            CampaignApproveLocators.custom_impression_tracking_textarea_locator,
            optimization_and_tracking_data[
                'custom_impression_tracking'][
                'value'])
        # VIEWABILITY AND VIDEO SUPPORT
        self.click_on_element(
            CampaignApproveLocators.viewability_and_video_support_locator)
        self.check_uncheck_specific_checkbox(optimization_and_tracking_data[
                                                 'viewability_and_video_support'], True)
        # VIDEO PLAYER REQUIREMENTS
        self.click_on_element(
            CampaignApproveLocators.video_player_requirement_locator)
        self.check_uncheck_specific_checkbox(optimization_and_tracking_data[
                                                 'vide_player_requirement'], True)
        # MRAID SUPPORT
        self.click_on_element(
            CampaignApproveLocators.mraid_support_locator)
        self.check_uncheck_specific_checkbox(optimization_and_tracking_data['mraid_support'], True)
        # MULTIPLE BID PER SECOND
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.multiple_bid_per_second_label,
                                             bool(optimization_and_tracking_data[
                                                      'multiple_bids_per_second']))
        # ENHANCED REACH METRICS
        self.set_value_into_element(
            CampaignApproveLocators.enhanced_min_reach_locator,
            optimization_and_tracking_data[
                'enhanced_reach_metric']['min'])
        self.set_value_into_element(
            CampaignApproveLocators.enhanced_max_reach_locator,
            optimization_and_tracking_data[
                'enhanced_reach_metric']['max'])

    def provide_ad_exchange_info(self, ad_exchange_data):
        # AD EXCHANGE
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.margin_type_label, True,
                                             value=ad_exchange_data['margin_type_value'])
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.ad_exchange_margin_label,
                                             bool(ad_exchange_data['eskimi_margin']), without_text=True)
        self.set_value_into_element(
            CampaignApproveLocators.ad_exchange_margin_text_xpath.format(
                CampaignApproveLocators.ad_exchange_margin_label),
            ad_exchange_data['eskimi_margin_value'],
            locator_initialization=True)

    def click_approve_button(self):
        self.click_on_element(
            CampaignApproveLocators.approve_button_locator)

    def approve_campaign(self, campaign_approve_data):
        self.provide_main_settings_info(
            campaign_approve_data['main_settings'])
        self.provide_reporting_and_budget_info(
            campaign_approve_data['reporting_and_budget'])
        self.provide_optimisation_and_tracking_info(
            campaign_approve_data['optimization_and_tracking'])
        self.provide_ad_exchange_info(
            campaign_approve_data['ad_exchange'])
        self.click_approve_button()
        self.click_on_element(
            CampaignApproveLocators.creative_size_pop_up_ignore_locator)

    def get_info_data(self):
        time.sleep(self.TWO_SEC_DELAY)
        self.scroll_to_specific_element(
            CampaignApproveLocators.private_deals_locator)
        time.sleep(self.ONE_SEC_DELAY)
        try:
            if self.is_element_present(CampaignApproveLocators.private_deals_locator):
                campaign_approve_information['info'][
                    'private_deal'] = self.get_element_text \
                    (CampaignApproveLocators.private_deals_locator)
        except Exception:
            self.driver.refresh()
            time.sleep(self.TWO_SEC_DELAY)
            self.scroll_to_specific_element(
                CampaignApproveLocators.private_deals_locator)
            time.sleep(self.ONE_SEC_DELAY)
            campaign_approve_information['info'][
                'private_deal'] = self.get_element_text \
                (CampaignApproveLocators.private_deals_locator)
        campaign_approve_information['info'][
            'deal_margin'] = self.get_attribute_value \
            (CampaignApproveLocators.deal_margin_locator,
             "value")

    def get_main_setting_data(self):
        # INSERTION ORDER
        campaign_approve_information['main_settings'][
            'io'] = self.get_text_using_tag_attribute(
            self.span_tag,
            self.id_attribute,
            CampaignApproveLocators.io_id)
        # ADVERTISER NAME
        campaign_approve_information['main_settings'][
            'advertiser_name'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute,
            CampaignApproveLocators.advertiser_name_id)
        # ADVERTISEMENT CATEGORY
        campaign_approve_information['main_settings'][
            'advertisement_category'] = self.get_advertisement_category()

    def get_reporting_and_budget_data(self, mass_approve=False):
        if not mass_approve:
            # EMAIL REPORT
            campaign_approve_information['reporting_and_budget'][
                'email_report'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.email_report_label)
            campaign_approve_information['reporting_and_budget'][
                'email_report'][
                'report_frequency'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.email_report_frequency_label)
            campaign_approve_information['reporting_and_budget'][
                'email_report'][
                'report_hour'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.email_report_hour_label)
            campaign_approve_information['reporting_and_budget'][
                'email_report'][
                'report_day'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.email_report_day_label)
            # GROUP BY IO
            campaign_approve_information['reporting_and_budget'][
                'group_by_io'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.group_by_io_label)
            campaign_approve_information['reporting_and_budget'][
                'group_by_io'][
                'view_by'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.group_by_io_label)
            # EMAIL ATTACHMENT
            campaign_approve_information['reporting_and_budget'][
                'email_attachment']['xls'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.email_attachments_label, value="xls")
            campaign_approve_information['reporting_and_budget'][
                'email_attachment']['pdf'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.email_attachments_label, value="pdf")
            # GENERATE INSIGHT REPORT
            campaign_approve_information['reporting_and_budget'][
                'generate_insight_report'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.generate_insight_report_label)
        # BID
        campaign_approve_information['reporting_and_budget']['bid'] = self.get_bid()
        # BUDGET
        campaign_approve_information['reporting_and_budget']['total_budget'] = self.get_total_budget()
        campaign_approve_information['reporting_and_budget']['daily_budget'] = self.get_daily_budget()
        # TECH FEE
        campaign_approve_information['reporting_and_budget'][
            'tech_fee'] = self.get_element_text(
            CampaignApproveLocators.tech_fee_locator,
            input_tag=True)
        if mass_approve:
            del \
                campaign_approve_information[
                    'reporting_and_budget'][
                    'email_report']
            del \
                campaign_approve_information[
                    'reporting_and_budget'][
                    'group_by_io']
            del \
                campaign_approve_information[
                    'reporting_and_budget'][
                    'email_attachment']['xls']
            del \
                campaign_approve_information[
                    'reporting_and_budget'][
                    'email_attachment']['pdf']
            del \
                campaign_approve_information[
                    'reporting_and_budget'][
                    'email_attachment']

    def get_optimisation_and_tracking_data(self, mass_approve=False):
        if not mass_approve:
            # IMPRESSION PERFORMANCE METRIC
            campaign_approve_information[
                'optimization_and_tracking'][
                'impression_performance_metric'][
                'viewability'] = self.get_element_text(
                CampaignApproveLocators.impression_performance_metric_viewability_locator,
                input_tag=True)
            campaign_approve_information[
                'optimization_and_tracking'][
                'impression_performance_metric'][
                'ctr'] = self.get_element_text(
                CampaignApproveLocators.impression_performance_metric_ctr,
                input_tag=True)
            campaign_approve_information[
                'optimization_and_tracking'][
                'impression_performance_metric'][
                'vcr'] = self.get_element_text(
                CampaignApproveLocators.impression_performance_metric_vcr,
                input_tag=True)
            # CUSTOM IMPRESSION TRACKING
            campaign_approve_information[
                'optimization_and_tracking'][
                'custom_impression_tracking'][
                'option'] = self.get_element_text(
                CampaignApproveLocators.custom_impression_tracking_dropdown_xpath,
                locator_initialization=True)
            campaign_approve_information[
                'optimization_and_tracking'][
                'custom_impression_tracking'][
                'value'] = self.get_element_text(
                CampaignApproveLocators.custom_impression_tracking_text_xpath,
                locator_initialization=True)
            # VIEWABILITY AND VIDEO SUPPORT
            campaign_approve_information[
                'optimization_and_tracking'][
                'viewability_and_video_support'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.viewability_and_video_support_div_id,
                label_is_parent=True)
            # VIDEO PLAYER REQUIREMENTS
            campaign_approve_information[
                'optimization_and_tracking'][
                'vide_player_requirement'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.video_player_requirement_div_id,
                label_is_parent=True)
            # MRAID SUPPORT
            campaign_approve_information[
                'optimization_and_tracking'][
                'mraid_support'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.mraid_support_div_id,
                label_is_parent=True)
            # ANTI FRAUD SETTINGS
            campaign_approve_information[
                'optimization_and_tracking'][
                'anti_fraud_setting'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.anti_fraud_setting_div_id,
                label_is_parent=True, multiple=True)
            # ENHANCED REACH METRICS
            campaign_approve_information[
                'optimization_and_tracking'][
                'enhanced_reach_metric'][
                'min'] = self.get_element_text(
                CampaignApproveLocators.enhanced_min_reach_locator,
                input_tag=True)
            campaign_approve_information[
                'optimization_and_tracking'][
                'enhanced_reach_metric'][
                'max'] = self.get_element_text(
                CampaignApproveLocators.enhanced_max_reach_locator,
                input_tag=True)
        # GOALS
        campaign_approve_information['optimization_and_tracking'][
            'goals'][
            'type'] = self.get_element_text(
            CampaignApproveLocators.goal_type_locator)
        campaign_approve_information['optimization_and_tracking'][
            'goals'][
            'pre_optimisation'] = self.get_element_text(
            CampaignApproveLocators.goal_pre_optimisation_locator)
        # MULTIPLE BID PER SECOND
        campaign_approve_information['optimization_and_tracking'][
            'multiple_bids_per_second'] = self.get_checkbox_status(
            CampaignApproveLocators.multiple_bid_per_second_label)
        if mass_approve:
            del campaign_approve_information[
                'optimization_and_tracking'][
                'impression_performance_metric']
            del campaign_approve_information[
                'optimization_and_tracking'][
                'custom_impression_tracking']
            del campaign_approve_information[
                'optimization_and_tracking'][
                'enhanced_reach_metric']
            del campaign_approve_information[
                'optimization_and_tracking'][
                'campaign_run_on_eskimi']

    def get_ad_exchange_data(self):
        # AD EXCHANGE
        campaign_approve_information['ad_exchange'][
            'margin_type_value'] = self.get_checked_element_value_attribute(
            CampaignApproveLocators.margin_type_label)
        campaign_approve_information['ad_exchange'][
            'eskimi_margin'] = self.get_checkbox_status(CampaignApproveLocators.ad_exchange_margin_label,
                                                        without_text=True)
        campaign_approve_information['ad_exchange'][
            'eskimi_margin_value'] = self.get_element_text(
            CampaignApproveLocators.ad_exchange_margin_text_xpath.format(
                CampaignApproveLocators.ad_exchange_margin_label),
            input_tag=True, locator_initialization=True)

    @staticmethod
    def reset_campaign_approve_information():
        # RESET CAMPAIGN_APPROVE INFORMATION BEFORE GETTING DATA
        global campaign_approve_information
        campaign_approve_information = {'info': {},
                                        'main_settings': {},
                                        'reporting_and_budget': {
                                            'email_report': {},
                                            'group_by_io': {},
                                            'email_attachment': {
                                                'xls': {},
                                                'pdf': {}}},
                                        'optimization_and_tracking': {
                                            'goals': {},
                                            'impression_performance_metric': {},
                                            'custom_impression_tracking': {},
                                            'enhanced_reach_metric': {},
                                            'campaign_run_on_eskimi': {}},
                                        'ad_exchange': {}}

    def get_campaign_approve_data(self, mass_approve=False,
                                  deal_margin=False):
        self.reset_campaign_approve_information()
        if deal_margin:
            self.get_info_data()
        self.get_main_setting_data()
        self.get_reporting_and_budget_data(mass_approve)
        self.get_optimisation_and_tracking_data(mass_approve)
        self.get_ad_exchange_data()
        return campaign_approve_information

    def get_campaign_status(self):
        return self.get_element_text(
            CampaignApproveLocators.campaign_status_data_qa)

    def click_delete_button(self):
        self.click_on_element(
            CampaignApproveLocators.delete_button_locator)
        self.wait_alert_is_present()
        self.accept_alert()

    def get_advertisement_category(self, value=False):
        elements = self.wait_for_presence_of_all_elements_located(
            CampaignApproveLocators.advertise_category_locator)
        options = []
        for index in range(len(elements)):
            if elements[index].is_selected():
                if value:
                    options.append(
                        str(elements[
                            index].get_attribute(
                            'value')).strip())
                else:
                    options.append(str(
                        elements[index].text).strip())
        return options

    def select_budget_related_metrics_to_see_it_in_report(self):
        self.click_on_element(CampaignApproveLocators.table_and_kpi_dropdown_data_qa)
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.spent_checkbox_data_qa, do_check=True)
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.cpm_data_qa, do_check=True)
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.cpc_data_qa, do_check=True)
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.cpe_data_qa, do_check=True)

    def accept_creative_size_pop_up(self):
        try:
            ignore_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Ignore')]")
            ignore_button.click()
        except NoSuchElementException:
            pass

    def get_total_budget(self):
        total_budget_from_approve_page = self.get_element_text(
            CampaignApproveLocators.daily_total_budget_locator)
        total_budget_from_approve = re.findall(r'[\d,.]+', total_budget_from_approve_page.split('\n')[1])[2]
        total_budget_from_approve = float(total_budget_from_approve.replace(',', ''))
        return total_budget_from_approve

    def get_daily_budget(self):
        daily_budget_from_approve_page = self.get_element_text(
            CampaignApproveLocators.daily_total_budget_locator)
        daily_budget_from_approve = re.findall(r'\d+\.\d+', daily_budget_from_approve_page.split('\n')[0])[2]
        daily_budget_from_approve = daily_budget_from_approve.replace(',', '')
        return daily_budget_from_approve

    def get_daily_spend(self):
        daily_budget_from_approve_page = self.get_element_text(
            CampaignApproveLocators.daily_total_budget_locator)
        daily_spend_text_match = re.search(r'Daily: \$([\d.]+)', daily_budget_from_approve_page)
        daily_spend_from_approve = daily_spend_text_match.group(1)
        return daily_spend_from_approve

    def get_total_spend(self):
        total_budget_from_approve_page = self.get_element_text(
            CampaignApproveLocators.daily_total_budget_locator)
        total_spend_text_match = re.search(r'Total: \$([\d.]+)', total_budget_from_approve_page)
        total_spend_from_approve = total_spend_text_match.group(1)
        return total_spend_from_approve

    def get_bid(self):
        bid = self.get_element_text(CampaignApproveLocators.bid_locator).split()[0].replace('$', '')
        return bid

    def get_creatives_bids(self):
        creatives_bids = self.get_text_or_value_from_list(CampaignApproveLocators.creatives_bid_locator)
        return creatives_bids

    @staticmethod
    def get_calculated_max_allowed_main_margin(total_budget, amount_already_spent):
        max_allowed_main_margin = (total_budget - amount_already_spent) / total_budget * 100
        max_allowed_main_margin = math.floor(max_allowed_main_margin * 100) / 100
        return max_allowed_main_margin

    @staticmethod
    def get_too_high_main_margin(max_allowed_main_margin):
        too_high_main_margin = round(max_allowed_main_margin + 0.01, 2)
        return too_high_main_margin

    @staticmethod
    def get_updated_main_margin(current_main_margin, max_allowed_main_margin):
        updated_main_margin = round((current_main_margin + float(max_allowed_main_margin)) / 2)
        return updated_main_margin

    @staticmethod
    def get_total_remaining_budget(total_budget, amount_already_spent, updated_main_margin):
        total_remaining_budget = total_budget - (amount_already_spent / (1 - updated_main_margin))
        return round(total_remaining_budget, 2)

    def get_success_message(self):
        time.sleep(self.TWO_SEC_DELAY)
        return self.get_element_text(
            CampaignApproveLocators.success_message_data_qa)

    def get_campaign_approve_all_data(self, mass_approve=False):
        self.reset_campaign_approve_information()
        campaign_approve_information['info']['status'] = self.get_campaign_status()
        campaign_approve_information['info']['partner'] = self.get_element_text(
            CampaignApproveLocators.client_name_data_qa)
        campaign_approve_information['info']['creative_type'] = self.get_element_text(
            CampaignApproveLocators.creative_type_data_qa)
        campaign_name = self.get_element_text(
            CampaignApproveLocators.campaign_name_data_qa)
        campaign_approve_information['info']['campaign_name'] = campaign_name.split('(')[0].strip()
        campaign_approve_information['info']['ad_domain'] = self.get_element_text(
            CampaignApproveLocators.ad_domain_data_qa)
        campaign_approve_information['info']['landing_page'] = self.get_element_text(
            CampaignApproveLocators.landing_page_data_qa)
        campaign_approve_information['info']['campaign_purpose'] = self.get_element_text(
            CampaignApproveLocators.campaign_purpose_data_qa)
        campaign_approve_information['info']['countries'] = self.get_element_text(
            CampaignApproveLocators.countries_data_qa)
        campaign_approve_information['info']['states'] = self.get_element_text(CampaignApproveLocators.states_locator)
        campaign_approve_information['info']['cities'] = self.get_element_text(CampaignApproveLocators.cities_locator)
        campaign_approve_information['info']['contextual_targeting_apps_sites'] = self.get_element_text(
            CampaignApproveLocators.contextual_targeting_apps_sites_data_qa)
        campaign_approve_information['info']['contextual_targeting_keywords'] = self.get_element_text(
            CampaignApproveLocators.contextual_targeting_keywords_data_qa)
        campaign_approve_information['info']['mobile_operators'] = self.get_element_text(
            CampaignApproveLocators.mobile_operators_data_qa)
        campaign_approve_information['info']['packages'] = self.get_element_text(
            CampaignApproveLocators.packages_data_qa)
        campaign_approve_information['info']['device_types'] = self.get_element_text(
            CampaignApproveLocators.device_types_data_qa)
        campaign_approve_information['info']['oses'] = self.get_element_text(CampaignApproveLocators.oses_data_qa)
        campaign_approve_information['info']['device_brands'] = self.get_element_text(
            CampaignApproveLocators.device_brands_data_qa)
        campaign_approve_information['info']['device_models'] = self.get_element_text(
            CampaignApproveLocators.device_models_data_qa)
        campaign_approve_information['info']['advanced_telecom_targeting'] = self.get_element_text(
            CampaignApproveLocators.advanced_telecom_targeting_data_qa)
        campaign_approve_information['info']['audiences'] = self.get_element_text(
            CampaignApproveLocators.audiences_data_qa)
        campaign_approve_information['info']['demographic'] = self.get_element_text(
            CampaignApproveLocators.demographic_data_qa)
        campaign_approve_information['info']['languages'] = self.get_element_text(
            CampaignApproveLocators.languages_data_qa)
        campaign_approve_information['info']['sec'] = self.get_element_text(
            CampaignApproveLocators.sec_data_qa)
        campaign_approve_information['info']['device_cost_ranges'] = self.get_element_text(
            CampaignApproveLocators.device_cost_ranges_data_qa)
        campaign_approve_information['info']['ad_exchanges'] = self.get_element_text(
            CampaignApproveLocators.ad_exhanges_data_qa)
        campaign_approve_information['info']['content_types'] = self.get_element_text(
            CampaignApproveLocators.content_types_data_qa)
        campaign_approve_information['info']['private_deal'] = self.get_element_text(
            CampaignApproveLocators.private_deals_locator)
        campaign_approve_information['info']['deal_margin'] = self.get_attribute_value(
            CampaignApproveLocators.deal_margin_locator, "value")
        self.get_main_setting_data()
        self.get_reporting_and_budget_data(mass_approve)
        self.get_optimisation_and_tracking_data(mass_approve)
        self.get_ad_exchange_data()
        return campaign_approve_information
