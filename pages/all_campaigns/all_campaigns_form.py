from urllib.parse import parse_qs
from urllib.parse import urlparse

from selenium.webdriver.common.keys import Keys

from locators.all_campaigns.all_campaign_locators import \
    AllCampaignFormLocators
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.navbar.navbar_locators import NavbarLocators
from locators.optimization.optimization_locators import OptimizationLocators
from locators.report.report_page_locator import ReportPageLocators
from pages.base_page import BasePage

campaign_information = {'budget': {}}


class DashboardAllCampaignForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def get_status_verification(self, status):
        return status == self.get_element_text(
            AllCampaignFormLocators.table_row_status_xpath.format(self.get_first_row_campaign_id()),
            locator_initialization=True)

    def change_status_filter(self, status_name):
        self.verify_filter_area_visible(AllCampaignFormLocators.status_filter_locator)
        self.select_dropdown_value(
            AllCampaignFormLocators.status_filter_locator,
            status_name)

    def change_user_filter(self, user_name):
        self.verify_filter_area_visible(AllCampaignFormLocators.user_filter_locator)
        self.select_dropdown_value(
            AllCampaignFormLocators.user_filter_locator,
            user_name)

    def change_country_filter(self, country_name):
        self.verify_filter_area_visible(AllCampaignFormLocators.country_filter_locator)
        self.select_dropdown_value(
            AllCampaignFormLocators.country_filter_locator,
            country_name)

    def all_statuses_verification(self, statuses):
        for status in statuses:
            if status == 'Pending':
                self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
                self.get_status_verification(status)
            else:
                self.change_status_filter(status)
                self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
                self.get_status_verification(status)
        return True

    def get_user_id(self, campaign_id):
        return self.get_url_function(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.table_row_login_as_btn_xpath.format(campaign_id),
                locator_initialization=True).get_attribute(
                'href'),
            parameter_name='admin_id')

    def user_filter_verification(self, config, user_name):
        self.change_user_filter(user_name)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.change_status_filter(AllCampaignFormLocators.status_all_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        first_row_id = self.get_first_row_campaign_id()
        user_id = self.get_user_id(first_row_id)
        url_segment = self.wait_for_visibility_of_element(
            AllCampaignFormLocators.table_row_login_as_btn_xpath.format(first_row_id),
            locator_initialization=True).get_attribute('href')
        url_function = self.get_path_segment(url_segment, 1)
        method_name = self.get_path_segment(url_segment, 2)
        if user_id == config['credential']['user-id'] and url_function == 'campaigns' and method_name == 'settings':
            return True
        else:
            return False

    def country_filter_verification(self, country_name):
        self.change_country_filter(country_name)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.change_user_filter(AllCampaignFormLocators.user_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.change_status_filter(AllCampaignFormLocators.status_all_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        return country_name == self.get_attribute_value(
            AllCampaignFormLocators.table_row_country_xpath.format(
                self.get_first_row_campaign_id()), 'title',
            locator_initialization=True)

    def change_creative_type_filter(self, creative_type):
        self.verify_filter_area_visible(AllCampaignFormLocators.creative_type_filter_locator)
        self.select_dropdown_value(
            AllCampaignFormLocators.creative_type_filter_locator,
            creative_type)

    def get_creative_type_verification(self, creative_type):
        return creative_type == self.get_attribute_value(
            AllCampaignFormLocators.table_row_creatives_type_xpath.format(self.get_first_row_campaign_id()), 'title',
            locator_initialization=True)

    def all_creative_type_verification(self, creative_types):
        self.change_status_filter(AllCampaignFormLocators.status_all_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        for creative_type in creative_types:
            self.change_creative_type_filter(creative_type)
            self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
            self.get_creative_type_verification(creative_type)
        return True

    def change_last_approved_filter(self, user_name):
        self.verify_filter_area_visible(AllCampaignFormLocators.last_approved_filter_locator)
        self.select_dropdown_value(
            AllCampaignFormLocators.last_approved_filter_locator,
            user_name)

    def last_approved_by_verification(self, user_name):
        self.change_status_filter(AllCampaignFormLocators.status_all_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.change_last_approved_filter(user_name)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        return user_name == self.get_element_text(
            AllCampaignFormLocators.table_row_last_approved_by_xpath.format(
                self.get_first_row_campaign_id()),
            locator_initialization=True)

    def search_by_value(self, value):
        self.change_status_filter(AllCampaignFormLocators.status_all_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.change_user_filter(AllCampaignFormLocators.user_option)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.set_value_into_element(
            AllCampaignFormLocators.search_filter_locator,
            value)
        self.wait_for_presence_of_element(
            AllCampaignFormLocators.search_filter_locator).send_keys(
            Keys.ENTER)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)

    def search_verification(self, search_text):
        self.search_by_value(search_text)
        url_segment = self.wait_for_visibility_of_element(
            AllCampaignFormLocators.table_row_campaign_name_xpath.format(self.get_first_row_campaign_id()),
            locator_initialization=True).get_attribute('href')
        url_function = self.get_path_segment(url_segment, 1)
        method_name = self.get_path_segment(url_segment, 2)
        if url_function == 'acampaigns' and method_name == 'view':
            return True
        else:
            return False

    def verify_three_dot_options(self, user_name):
        url_functions = []
        self.change_user_filter(user_name)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
        self.click_on_element(
            AllCampaignFormLocators.three_dot_locator.format(self.get_first_row_campaign_id()),
            locator_initialization=True)
        url_functions.append(self.get_path_segment(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.targeting_optimization_locator.format(self.get_first_row_campaign_id()),
                locator_initialization=True).get_attribute('href'), 1))
        url_functions.append(self.get_path_segment(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.view_report_locator.format(self.get_first_row_campaign_id()),
                locator_initialization=True).get_attribute('href'), 1))
        url_functions.append(self.get_path_segment(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.confirm_campaign_locator.format(self.get_first_row_campaign_id()),
                locator_initialization=True).get_attribute('href'), 1))
        url_functions.append(self.get_path_segment(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.reject_campaign_locator.format(self.get_first_row_campaign_id()),
                locator_initialization=True).get_attribute('href'), 1))
        url_functions.append(self.get_path_segment(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.delete_campaign_locator.format(self.get_first_row_campaign_id()),
                locator_initialization=True).get_attribute('data-url'), 2))
        url_functions.append(self.get_url_function(
            self.wait_for_visibility_of_element(
                AllCampaignFormLocators.remove_completely_campaign_locator.format(self.get_first_row_campaign_id()),
                locator_initialization=True).get_attribute('data-url'), 'remove'))
        return url_functions

    @staticmethod
    def get_url_function(url, parameter_name):
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)[parameter_name][0]
        return captured_value

    @staticmethod
    def get_path_segment(url, index):
        parsed_url = urlparse(url)
        path_segments = parsed_url.path.strip('/').split('/')
        return path_segments[index] if index < len(path_segments) else None

    def clear_all(self):
        self.click_on_element(
            AllCampaignFormLocators.clear_all_locator)
        self.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)

    def get_first_row_campaign_id(self):
        return self.get_value_from_specific_grid_column(
            AllCampaignFormLocators.all_campaigns_table_wrapper_div_id, AllCampaignFormLocators.campaign_id_label,
            a_tag=True)

    @staticmethod
    def reset_campaign_information():
        global campaign_information
        campaign_information = {'budget': {}}

    def get_all_campaign_data_from_table(self, campaign_id):
        self.reset_campaign_information()
        campaign_information['campaignId'] = str(
            self.get_element_text(AllCampaignFormLocators.table_row_id_xpath.format(campaign_id),
                                  locator_initialization=True))
        campaign_information['name'] = self.get_element_text(
            AllCampaignFormLocators.table_row_campaign_name_xpath.format(campaign_id), locator_initialization=True)
        campaign_information['campaign_type'] = self.get_element_text(
            AllCampaignFormLocators.table_row_campaign_type_xpath.format(campaign_id), locator_initialization=True)
        campaign_information['creative_type'] = self.get_attribute_value(
            AllCampaignFormLocators.table_row_creatives_type_xpath.format(campaign_id), 'title',
            locator_initialization=True)
        campaign_information['country'] = self.get_element_text(
            AllCampaignFormLocators.table_row_country_xpath.format(campaign_id), locator_initialization=True).lower()
        campaign_information['userId'] = int(self.get_user_id(campaign_id))
        campaign_information['bid'] = float(
            self.get_element_text(AllCampaignFormLocators.table_row_bid_by_xpath.format(campaign_id),
                                  locator_initialization=True).split("$")[1])
        campaign_information['budget']['daily'] = float(
            self.get_element_text(AllCampaignFormLocators.table_row_daily_budget_by_xpath.format(campaign_id),
                                  locator_initialization=True).split("$")[2])
        campaign_information['budget']['total'] = float(
            self.get_element_text(AllCampaignFormLocators.table_row_total_budget_by_xpath.format(campaign_id),
                                  locator_initialization=True).split("$")[2])
        campaign_information['status'] = self.get_element_text(
            AllCampaignFormLocators.table_row_status_xpath.format(campaign_id), locator_initialization=True)
        approved_by = self.get_element_text(
            AllCampaignFormLocators.table_row_last_approved_by_xpath.format(campaign_id), locator_initialization=True)
        if approved_by:
            campaign_information['approved_by'] = approved_by
        return campaign_information

    def verify_redirect_to_campaign_edit_page(self, config, campaign_id, campaign_name):
        self.click_on_element(AllCampaignFormLocators.table_row_id_xpath.format(campaign_id),
                              locator_initialization=True,
                              locator_to_be_appeared=CampaignFormLocators.campaign_name_locator)
        current_url_function = self.driver.current_url
        parsed_url = urlparse(current_url_function)
        expected_path = '/admin/campaigns/form'
        if parsed_url.path != expected_path:
            return False
        current_url_admin_id = self.get_url_function(self.driver.current_url, parameter_name='admin_id')
        current_url_campaign_id = self.get_url_function(self.driver.current_url, parameter_name='id')
        return current_url_campaign_id == campaign_id and current_url_admin_id == \
            config['credential']['user-id'] and self.get_element_text(
                CampaignFormLocators.campaign_name_locator) == campaign_name

    def verify_redirect_to_campaign_approve_page(self, campaign_id):
        self.click_on_element(AllCampaignFormLocators.table_row_campaign_name_xpath.format(campaign_id),
                              locator_initialization=True, locator_to_be_appeared=CampaignApproveLocators.campaign_id)
        current_url_function = self.driver.current_url
        parsed_url = urlparse(current_url_function)
        expected_path = '/admin/acampaigns/view'
        if parsed_url.path != expected_path:
            return False
        current_url_campaign_id = self.get_url_function(self.driver.current_url, parameter_name='id')
        return current_url_campaign_id == campaign_id and self.get_element_text(
            CampaignApproveLocators.campaign_id) == campaign_id

    def verify_redirect_to_campaign_list_page_after_change_account(self):
        firs_row_username = self.get_element_text(
            AllCampaignFormLocators.table_row_login_as_xpath.format(
                self.get_first_row_campaign_id()),
            locator_initialization=True).split('(')[0].strip()
        self.click_on_element(
            AllCampaignFormLocators.table_row_login_as_btn_xpath.format(self.get_first_row_campaign_id()),
            locator_initialization=True)
        current_url_function = self.driver.current_url
        parsed_url = urlparse(current_url_function)
        expected_path = '/admin/campaigns/settings'
        if parsed_url.path != expected_path:
            return False
        return self.get_element_text(NavbarLocators.account_dropdown_locator) == firs_row_username

    def verify_redirect_to_target_optimisation(self, campaign_id):
        self.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_id),
                              locator_initialization=True)
        self.click_on_element(AllCampaignFormLocators.targeting_optimization_locator.format(campaign_id),
                              locator_initialization=True,
                              locator_to_be_appeared=OptimizationLocators.search_button_locator)
        current_url_function = self.driver.current_url
        parsed_url = urlparse(current_url_function)
        expected_path = '/admin/optimisation'
        if parsed_url.path != expected_path:
            return False
        return campaign_id == self.get_text_or_value_from_selected_option(
            OptimizationLocators.campaign_label, value=True)

    def verify_redirect_to_reports(self, campaign_id):
        self.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_id),
                              locator_initialization=True)
        self.click_on_element(AllCampaignFormLocators.view_report_locator.format(campaign_id),
                              locator_initialization=True,
                              locator_to_be_appeared=ReportPageLocators.report_title_locator)
        current_url_function = self.driver.current_url
        parsed_url = urlparse(current_url_function)
        expected_path = '/admin/reporting'
        if parsed_url.path != expected_path:
            return False
        return campaign_id == self.get_text_or_value_from_selected_option(
            ReportPageLocators.campaign_select_data_qa, value=True)

    def verify_redirect_to_approve_page_after_confirm(self, campaign_id):
        self.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_id),
                              locator_initialization=True)
        self.click_on_element(AllCampaignFormLocators.confirm_campaign_locator.format(campaign_id),
                              locator_initialization=True, locator_to_be_appeared=CampaignApproveLocators.campaign_id)
        current_url_function = self.driver.current_url
        parsed_url = urlparse(current_url_function)
        expected_path = '/admin/acampaigns/view'
        if parsed_url.path != expected_path:
            return False
        current_url_campaign_id = self.get_url_function(self.driver.current_url, parameter_name='id')
        return current_url_campaign_id == campaign_id and self.get_element_text(
            CampaignApproveLocators.campaign_id) == campaign_id

    def verify_filter_area_visible(self, locator_to_be_appeared):
        style = self.get_attribute_value(AllCampaignFormLocators.filter_area, "style", locator_initialization=False)
        if style == "display: none;":
            self.click_on_element(AllCampaignFormLocators.filter_btn, locator_initialization=False,
                                  locator_to_be_appeared=locator_to_be_appeared)
