import time

from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from locators.campaign.campaign_approve_form_locator import \
    CampaignApproveLocators
from locators.campaign.campaign_mass_approve_form_locators import \
    CampaignMassApproveFormLocators
from pages.base_page import BasePage


class DspDashboardCampaignsMassApprove(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_campaign_mass_approve_data_and_save(self,
                                                    campaign_name_list,
                                                    mass_approve_campaign_data,
                                                    deal_margin_disabled=False):
        self.wait_for_visibility_of_element(
            CampaignMassApproveFormLocators.mass_approve_header_locator)
        for iteration in range(len(campaign_name_list)):
            # INSERTION ORDER
            if deal_margin_disabled:
                self.select_dropdown_value_from_specific_form_grid(
                    CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                    CampaignMassApproveFormLocators.insertion_order_column_mandatory,
                    mass_approve_campaign_data[
                        'main_settings']['io'],
                    str(iteration + 2),
                    search_option_available=False)
            else:
                self.select_dropdown_value_from_specific_form_grid(
                    CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                    CampaignMassApproveFormLocators.insertion_order_column,
                    mass_approve_campaign_data[
                        'main_settings']['io'],
                    str(iteration + 2),
                    search_option_available=False)
            # ADVERTISER NAME
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertiser_name_column,
                mass_approve_campaign_data['main_settings'][
                    'advertiser_name'],
                str(iteration + 2))
            # ADVERTISEMENT CATEGORY
            self.click_link_of_specific_column_of_specific_row_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertisement_category_column,
                str(iteration + 2))
            self.dropdown_selection(
                CampaignMassApproveFormLocators.advertisement_category_modal_xpath.format(
                    str(iteration)),
                dropdown_item=
                mass_approve_campaign_data['main_settings'][
                    'advertisement_category'])
            self.click_ok_button_of_specific_column_modal_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertisement_category_column,
                str(iteration + 2))
            # AD EXCHANGE
            self.click_link_of_specific_column_of_specific_row_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.ad_exchange_column,
                str(iteration + 2))
            self.check_uncheck_specific_form_grid_row_checkbox_modal(
                CampaignMassApproveFormLocators.margin_type_label,
                True,
                value=
                mass_approve_campaign_data['ad_exchange'][
                    'margin_type_value'],
                row_number=str(iteration + 2))
            self.check_uncheck_specific_form_grid_row_checkbox_modal(
                CampaignMassApproveFormLocators.ad_exchange_name_label,
                bool(mass_approve_campaign_data['ad_exchange'][
                         'eskimi_margin']),
                row_number=str(iteration + 2))
            ad_exchange_margin_text_locator = CampaignMassApproveFormLocators.ad_exchange_text_field_xpath.format(
                CampaignMassApproveFormLocators.ad_exchange_name_label,
                str(iteration + 2))
            self.set_value_into_element(
                ad_exchange_margin_text_locator,
                mass_approve_campaign_data[
                    'ad_exchange'][
                    'eskimi_margin_value'],
                locator_initialization=True)
            self.click_ok_button_of_specific_column_modal_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.ad_exchange_column,
                str(iteration + 2))
            # MULTIPLE BIDS PER SECOND
            self.check_uncheck_specific_form_grid_row_checkbox(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.multiple_bids_per_user_second_column,
                bool(mass_approve_campaign_data[
                         'optimization_and_tracking'][
                         'multiple_bids_per_second']),
                str(iteration + 2))

            time.sleep(self.FIVE_SEC_DELAY)
            if deal_margin_disabled is False:
                # Private Deals
                self.click_link_of_specific_column_of_specific_row_from_grid(
                    CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                    CampaignMassApproveFormLocators.private_deals_column,
                    str(iteration + 2))
                deal_margin_text_locator = CampaignMassApproveFormLocators.deal_margin_text_field_xpath.format(
                    str(iteration + 1))
                time.sleep(self.TWO_SEC_DELAY)
                try:
                    if self.is_element_present(
                            deal_margin_text_locator,
                            locator_initialization=True):
                        self.set_value_into_element(
                            deal_margin_text_locator,
                            mass_approve_campaign_data[
                                'info'][
                                'deal_margin'],
                            locator_initialization=True)
                except TimeoutException:
                    self.click_ok_button_of_specific_column_modal_from_grid(
                        CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                        CampaignMassApproveFormLocators.private_deals_column,
                        str(iteration + 2))
                    self.click_link_of_specific_column_of_specific_row_from_grid(
                        CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                        CampaignMassApproveFormLocators.private_deals_column,
                        str(iteration + 2))
                    deal_margin_text_locator = CampaignMassApproveFormLocators.deal_margin_text_field_xpath.format(
                        str(iteration + 1))
                    time.sleep(self.TWO_SEC_DELAY)
                    self.set_value_into_element(
                        deal_margin_text_locator,
                        mass_approve_campaign_data[
                            'info']['deal_margin'],
                        locator_initialization=True)
                self.click_ok_button_of_specific_column_modal_from_grid(
                    CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                    CampaignMassApproveFormLocators.private_deals_column,
                    str(iteration + 2))
        self.click_on_element(
            CampaignMassApproveFormLocators.approve_button_locator)

    def provide_campaign_mass_approve_data_and_save_apply_all(self,
                                                              mass_approve_campaign_data,
                                                              deal_margin_disabled=False):
        self.wait_for_visibility_of_element(
            CampaignMassApproveFormLocators.mass_approve_header_locator)
        index = 0
        # INSERTION ORDER
        if deal_margin_disabled:
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.insertion_order_column_mandatory,
                mass_approve_campaign_data['main_settings'][
                    'io'],
                str(index + 1), search_option_available=False)
        else:
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.insertion_order_column,
                mass_approve_campaign_data['main_settings'][
                    'io'],
                str(index + 1),
                search_option_available=False)
        # ADVERTISEMENT CATEGORY
        self.click_link_of_specific_column_of_specific_row_from_grid(
            CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
            CampaignMassApproveFormLocators.advertisement_category_column,
            str(index + 1))
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(
            CampaignMassApproveFormLocators.specific_adv_category_locator)
        self.click_ok_button_of_specific_column_modal_from_grid(
            CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
            CampaignMassApproveFormLocators.advertisement_category_column,
            str(index + 1))
        # MULTIPLE BIDS PER SECOND
        self.check_uncheck_specific_form_grid_row_checkbox(
            CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
            CampaignMassApproveFormLocators.multiple_bids_per_user_second_column,
            bool(mass_approve_campaign_data[
                     'optimization_and_tracking'][
                     'multiple_bids_per_second']),
            str(index + 1))
        # AD EXCHANGE
        self.click_link_of_specific_column_of_specific_row_from_grid(
            CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
            CampaignMassApproveFormLocators.ad_exchange_column,
            str(index + 1))
        self.check_uncheck_specific_form_grid_row_checkbox_modal(
            CampaignMassApproveFormLocators.margin_type_label,
            True,
            value=mass_approve_campaign_data['ad_exchange'][
                'margin_type_value'],
            row_number=str(index + 1))
        self.check_uncheck_specific_form_grid_row_checkbox_modal(
            CampaignMassApproveFormLocators.ad_exchange_name_label,
            bool(mass_approve_campaign_data['ad_exchange'][
                     'eskimi_margin']),
            row_number=str(index + 1))
        ad_exchange_margin_text_locator = CampaignMassApproveFormLocators.ad_exchange_text_field_xpath.format(
            CampaignMassApproveFormLocators.ad_exchange_name_label,
            str(index + 1))
        self.set_value_into_element(ad_exchange_margin_text_locator,
                                    mass_approve_campaign_data[
                                        'ad_exchange'][
                                        'eskimi_margin_value'],
                                    locator_initialization=True)
        self.click_ok_button_of_specific_column_modal_from_grid(
            CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
            CampaignMassApproveFormLocators.ad_exchange_column,
            str(index + 1))
        self.click_on_element(
            CampaignMassApproveFormLocators.exchange_prompt_ok_button_locator)
        self.click_on_element(
            CampaignMassApproveFormLocators.approve_button_locator)

    def provide_campaign_mass_approve_advertiser_name(self, campaign_name_list, mass_approve_campaign_data):
        self.wait_for_visibility_of_element(
            CampaignMassApproveFormLocators.mass_approve_header_locator)
        for iteration in range(len(campaign_name_list)):
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertiser_name_column,
                mass_approve_campaign_data['main_settings'][
                    'advertiser_name'],
                str(iteration + 2))
