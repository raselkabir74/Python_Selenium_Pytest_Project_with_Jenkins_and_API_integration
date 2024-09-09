import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from locators.campaign.campaign_mass_edit_form_locator import \
    CampaignMassEditFormLocator
from locators.campaign.campaign_list_locator import CampaignListLocators
from pages.base_page import BasePage

campaign_information = {}


class DspDashboardCampaignsMassEdit(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_campaign_mass_edit_data_and_save(self, campaign_name_list,
                                                 campaign_mass_edit_data=None,
                                                 duplicate_campaigns=False, mass_edit_only=True):
        self.wait_for_visibility_of_element(
            CampaignMassEditFormLocator.edit_campaign_header_locator)
        for index, campaign_name in enumerate(campaign_name_list):
            index_value = str(index + 2) if len(campaign_name_list) > 1 else str(index + 1)
            # SETTING VALUE INTO ALL INPUT FIELDS
            if duplicate_campaigns:
                self.set_value_into_specific_form_grid_input_field(
                    CampaignMassEditFormLocator.campaign_mass_edit_form_id,
                    CampaignMassEditFormLocator.name_column,
                    campaign_name_list[index],
                    index_value)
                # UPDATING PERIOD TO 7 DAYS
                self.change_launch_date_to_seven_day_period(str(index))
            else:
                self.setting_value_into_all_form_grid_input_field(
                    campaign_name_list, campaign_mass_edit_data,
                    index_value)
                # SETTING VALUE INTO BUDGET COLUMN
                self.setting_value_into_budget_column(CampaignMassEditFormLocator.campaign_mass_edit_form_id,
                                                      campaign_mass_edit_data, index_value)
                # SETTING VALUE INTO DROPDOWN FIELD
                self.select_dropdown_value_from_specific_form_grid(
                    CampaignMassEditFormLocator.campaign_mass_edit_form_id,
                    CampaignMassEditFormLocator.ad_domain_column,
                    campaign_mass_edit_data[
                        'landing_and_creatives']['ad_domain'],
                    index_value)
                # SETTING VALUE INTO ALL MODALS
                self.setting_value_into_all_modal_field(
                    campaign_mass_edit_data,
                    index_value)
                # SETTING VALUE INTO CREATIVES COLUMN
                self.setting_value_into_creatives_column(
                    CampaignMassEditFormLocator.campaign_mass_edit_form_id,
                    campaign_mass_edit_data[
                        'landing_and_creatives']['creative'],
                    index_value)
                time.sleep(self.TWO_SEC_DELAY)
        # SAVE DATA
        if mass_edit_only:
            self.scroll_to_specific_element(
                CampaignMassEditFormLocator.save_button_locator)
            time.sleep(self.ONE_SEC_DELAY)
            self.wait_for_presence_of_element(
                CampaignMassEditFormLocator.save_button_locator)
            self.wait_for_element_to_be_clickable(
                CampaignMassEditFormLocator.save_button_locator)
            self.click_on_element(
                CampaignMassEditFormLocator.save_button_locator)

    def provide_campaign_mass_edit_data_apply_all_and_save(self,
                                                           campaign_name_list,
                                                           campaign_mass_edit_data):
        self.wait_for_visibility_of_element(
            CampaignMassEditFormLocator.edit_campaign_header_locator)
        for iteration in range(len(campaign_name_list)):
            self.set_value_into_specific_form_grid_input_field(
                CampaignMassEditFormLocator.campaign_mass_edit_form_id,
                CampaignMassEditFormLocator.name_column,
                campaign_name_list[iteration],
                str(iteration + 2))
        self.change_lunch_date_to_seven_day_period_apply_all()
        self.set_value_into_element(
            CampaignMassEditFormLocator.edit_campaign_bid_cpm_apply_all_locator,
            campaign_mass_edit_data['launch_date_and_budget'][
                'bid_cpm'])
        self.provide_campaign_budget_apply_all_and_save(campaign_mass_edit_data)
        self.click_on_element(
            CampaignMassEditFormLocator.edit_campaign_creative_apply_all_locator)
        self.click_on_element(
            CampaignMassEditFormLocator.edit_campaign_creative_search_locator)
        self.click_on_element(
            CampaignMassEditFormLocator.creative_dropdown_value.format(
                campaign_mass_edit_data[
                    'landing_and_creatives']['creative']),
            locator_initialization=True)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(
            CampaignMassEditFormLocator.edit_campaign_creative_ok_button_locator)
        if self.is_element_present(CampaignMassEditFormLocator.confirm_button_alert_locator, time_out=1):
            self.click_on_element(CampaignMassEditFormLocator.confirm_button_alert_locator)
        time.sleep(4)
        self.set_value_into_element(
            CampaignMassEditFormLocator.edit_campaign_landings_apply_all_locator,
            campaign_mass_edit_data['landing_and_creatives'][
                'click_url'])
        time.sleep(4)
        self.click_on_element(
            CampaignMassEditFormLocator.edit_campaign_ad_domain_apply_all_locator)
        self.set_value_into_element(
            CampaignMassEditFormLocator.edit_campaign_apply_all_search_button_locator,
            campaign_mass_edit_data['landing_and_creatives'][
                'ad_domain'])
        time.sleep(1)
        self.wait_for_presence_of_element(CampaignMassEditFormLocator.
                                          edit_campaign_apply_all_search_button_locator).send_keys(
            Keys.ENTER)
        # SAVE DATA
        self.wait_for_presence_of_element(
            CampaignMassEditFormLocator.save_button_locator)
        self.wait_for_element_to_be_clickable(
            CampaignMassEditFormLocator.save_button_locator)
        self.click_on_element(
            CampaignMassEditFormLocator.save_button_locator)

    def setting_value_into_all_form_grid_input_field(self,
                                                     campaign_name_list,
                                                     campaign_mass_edit_data,
                                                     row_number):
        self.set_value_into_specific_form_grid_input_field(
            CampaignMassEditFormLocator.campaign_mass_edit_form_id,
            CampaignMassEditFormLocator.name_column,
            campaign_name_list[int(row_number) - 2],
            str(row_number))
        self.set_value_into_specific_form_grid_input_field(
            CampaignMassEditFormLocator.campaign_mass_edit_form_id,
            CampaignMassEditFormLocator.bid_cpm_column,
            campaign_mass_edit_data['launch_date_and_budget'][
                'bid_cpm'],
            str(row_number))
        self.set_value_into_specific_form_grid_input_field(
            CampaignMassEditFormLocator.campaign_mass_edit_form_id,
            CampaignMassEditFormLocator.landings_column,
            campaign_mass_edit_data['landing_and_creatives'][
                'click_url'],
            str(row_number))

    def setting_value_into_budget_column(self, form_tag_id, campaign_mass_edit_data, row_number="1"):
        adjusted_row_number = str(int(row_number) + 1) if row_number == "1" else row_number
        index = self.get_specific_form_grid_column_index(form_tag_id, CampaignMassEditFormLocator.budget_column)
        edit_locator = (
            By.XPATH, "//form[@id='" + form_tag_id + "']//tbody//tr[" + str(row_number) + "]//td[" + str(index) +
            "]//i")
        self.click_on_element(edit_locator)
        time.sleep(self.ONE_SEC_DELAY)
        if campaign_mass_edit_data['launch_date_and_budget']['daily_budget_selected'] == "True":
            self.click_on_element(
                CampaignMassEditFormLocator.daily_budget_radio_btn_data_qa.format(int(adjusted_row_number) - 2))
            time.sleep(self.ONE_SEC_DELAY)
            self.set_value_into_element(
                CampaignMassEditFormLocator.budget_amount_input_data_qa.format(int(adjusted_row_number) - 2),
                campaign_mass_edit_data['launch_date_and_budget']['daily_budget'])
        else:
            self.click_on_element(
                CampaignMassEditFormLocator.total_budget_radio_btn_data_qa.format(int(adjusted_row_number) - 2))
            time.sleep(self.ONE_SEC_DELAY)
            self.set_value_into_element(
                CampaignMassEditFormLocator.budget_amount_input_data_qa.format(int(adjusted_row_number) - 2),
                campaign_mass_edit_data['launch_date_and_budget']['total_budget'])
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(CampaignMassEditFormLocator.budget_save_btn_data_qa.format(int(adjusted_row_number) - 2))

    def setting_value_into_all_modal_field(self, campaign_mass_edit_data,
                                           row_number):
        self.select_value_from_specific_form_grid_modal(
            CampaignMassEditFormLocator.campaign_mass_edit_form_id,
            CampaignMassEditFormLocator.sec_column,
            campaign_mass_edit_data['location_and_audiences'][
                'sec'],
            str(row_number))
        mobile_operator = \
            campaign_mass_edit_data['platforms_telco_and_devices'][
                'mobile_operator']
        mobile_operator = mobile_operator.split(" - ")
        self.select_value_from_specific_form_grid_modal(
            CampaignMassEditFormLocator.campaign_mass_edit_form_id,
            CampaignMassEditFormLocator.operators_column,
            mobile_operator[0], str(row_number))

    def setting_value_into_creatives_column(self, form_tag_id,
                                            column_value_to_select,
                                            row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         CampaignMassEditFormLocator.creatives_column)
        button_locator = (By.XPATH,
                          "//form[@id='" + form_tag_id + "']//tbody//tr[" + str(
                              row_number) + "]//td[" +
                          str(index) + "]//a")
        if int(row_number) == 1:
            adjusted_row_number = 1
        else:
            adjusted_row_number = int(row_number) - 1
        cross_button_locator = (
            By.XPATH,
            "(//span[@class='select2-selection__choice__remove'])[" + str(adjusted_row_number) + "]")
        input_field_locator = (
            By.XPATH,
            "(//ul[@class='select2-selection__rendered']//input)[" + str(adjusted_row_number) + "]")
        self.click_on_element(button_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(cross_button_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.set_value_into_element(input_field_locator,
                                    column_value_to_select)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_presence_of_element(
            input_field_locator).send_keys(
            Keys.ENTER)
        time.sleep(self.ONE_SEC_DELAY)
        self.click_on_element(
            CampaignMassEditFormLocator.edit_campaign_creative_single_ok_button_locator)

    def get_campaign_name_and_type(self):
        time.sleep(self.TWO_SEC_DELAY)
        campaign_information['name_and_type']['creative_type'] = \
            self.get_element_text(CampaignMassEditFormLocator.creative_type_locator)
        campaign_information['name_and_type']['campaign_type'] = \
            self.get_element_text(CampaignMassEditFormLocator.campaign_type_locator)
        campaign_information['name_and_type']['campaign_name'] = \
            self.get_element_text(CampaignMassEditFormLocator.campaign_name_data_qa)

    def get_campaign_launch_date_and_budget(self):
        campaign_information['launch_date_and_budget'][
            'bid_cpm'] = self.get_attribute_value(
            CampaignMassEditFormLocator.bid_fields_locator, attribute_name="value")
        campaign_information['launch_date_and_budget'][
            'total_budget'] = self.get_total_budget()
        campaign_information['launch_date_and_budget'][
            'daily_budget'] = self.get_daily_budget()

    def get_campaign_location_and_audiences(self):
        campaign_information['location_and_audiences'][
            'country_name'] = self.get_element_text(CampaignMassEditFormLocator.country_locator)
        campaign_information['location_and_audiences'][
            'sec'] = self.get_element_text(CampaignMassEditFormLocator.sec_locator)

    def get_campaign_platforms_telco_and_devices(self):
        campaign_information['platforms_telco_and_devices']['mobile_operator'] = self.get_element_text(
            CampaignMassEditFormLocator.operators_locator)

    def get_campaign_landing_and_creatives(self):
        campaign_information['landing_and_creatives']['creative'] = \
            self.get_campaign_creatives(CampaignMassEditFormLocator.campaign_mass_edit_form_id)
        campaign_information['landing_and_creatives'][
            'click_url'] = self.get_element_text(CampaignMassEditFormLocator.landings_input_data_qa)
        campaign_information['landing_and_creatives'][
            'ad_domain'] = self.get_element_text(CampaignMassEditFormLocator.ad_domain_id, locator_initialization=True)

    def get_campaign_creatives(self, form_tag_id):
        index = self.get_specific_form_grid_column_index(form_tag_id,
                                                         CampaignMassEditFormLocator.creatives_column)
        button_locator = (By.XPATH,
                          "//form[@id='" + form_tag_id + "']//tbody//tr[1]//td[" + str(index) + "]//a")
        self.click_on_element(button_locator)
        time.sleep(self.ONE_SEC_DELAY)
        creatives = self.get_attribute_value(CampaignMassEditFormLocator.selected_creatives_locator,
                                             attribute_name='title')
        self.click_on_element(
            CampaignMassEditFormLocator.edit_campaign_creative_single_ok_button_locator)
        return creatives

    def get_campaign_information_for_mass_edit(self):
        self.reset_campaign_information()
        self.get_campaign_name_and_type()
        self.get_campaign_launch_date_and_budget()
        self.get_campaign_landing_and_creatives()
        self.get_campaign_location_and_audiences()
        self.get_campaign_platforms_telco_and_devices()
        return campaign_information

    @staticmethod
    def reset_campaign_information():
        global campaign_information
        campaign_information = {'name_and_type': {},
                                'launch_date_and_budget': {},
                                'landing_and_creatives': {},
                                'location_and_audiences': {},
                                'platforms_telco_and_devices': {}}

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

    def get_daily_budget(self):
        campaign_daily_budget = self.get_element_text(CampaignMassEditFormLocator.daily_budget_fields_locator)
        return campaign_daily_budget

    def get_total_budget(self):
        campaign_total_budget = self.get_element_text(CampaignMassEditFormLocator.total_budget_fields_locator)
        return campaign_total_budget

    def provide_campaign_budget_and_save(self, campaign_name_list, campaign_mass_edit_data=None):
        self.wait_for_visibility_of_element(
            CampaignMassEditFormLocator.edit_campaign_header_locator)
        for index, campaign_name in enumerate(campaign_name_list):
            self.setting_value_into_budget_column(CampaignMassEditFormLocator.campaign_mass_edit_form_id,
                                                  campaign_mass_edit_data, str(index + 2))
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_element_to_be_clickable(
            CampaignMassEditFormLocator.save_button_locator)
        self.click_on_element(
            CampaignMassEditFormLocator.save_button_locator,
            locator_to_be_appeared=CampaignListLocators.success_message_locator)

    def provide_campaign_budget_apply_all_and_save(self, campaign_mass_edit_data):
        self.click_on_element(CampaignMassEditFormLocator.edit_campaign_budget_btn_apply_all_data_qa)
        if campaign_mass_edit_data['launch_date_and_budget']['daily_budget_selected'] == "True":
            self.click_on_element(CampaignMassEditFormLocator.daily_budget_radio_btn_apply_all_data_qa)
            self.set_value_into_element(
                CampaignMassEditFormLocator.edit_campaign_budget_apply_all_data_qa,
                campaign_mass_edit_data['launch_date_and_budget'][
                    'daily_budget'])
        else:
            self.click_on_element(CampaignMassEditFormLocator.total_budget_radio_btn_apply_all_data_qa)
            self.set_value_into_element(
                CampaignMassEditFormLocator.edit_campaign_budget_apply_all_data_qa,
                campaign_mass_edit_data['launch_date_and_budget'][
                    'total_budget'])
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_element_to_be_clickable(CampaignMassEditFormLocator.budget_save_btn_apply_all_data_qa)
        self.click_on_element(CampaignMassEditFormLocator.budget_save_btn_apply_all_data_qa)

    def change_launch_date_to_seven_day_period(self, row_number="1"):
        self.click_on_element(CampaignMassEditFormLocator.date_picker_data_qa.format(int(row_number)))
        self.click_on_element(CampaignMassEditFormLocator.seven_days_period_locator.format(int(row_number)),
                              locator_initialization=True)

    def change_lunch_date_to_seven_day_period_apply_all(self):
        self.click_on_element(CampaignMassEditFormLocator.data_picker_apply_all_data_qa)
        self.click_on_element(CampaignMassEditFormLocator.seven_days_period_locator_apply_all,
                              locator_initialization=True)
