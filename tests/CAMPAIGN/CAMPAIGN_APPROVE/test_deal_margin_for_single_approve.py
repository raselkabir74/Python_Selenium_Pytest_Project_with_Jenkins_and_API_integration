import copy
import json
import time

from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configurations import generic_modules
from locators.campaign.campaign_approve_form_locator import \
    CampaignApproveLocators
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from locators.io.io_form_locator import IoFormLocators
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.navbar.navbar import DashboardNavbar
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.budget.add_payment import DspDashboardAddPayment
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.redis import RedisUtils
from utils.page_names_enum import PageNames


def test_dashboard_campaign_approve_single_approve_deal_margin_enabled(login_by_user_type, open_database_connection):
    """
    Log in as an admin who has deal margin enabled from User Settings.
    Create a campaign using API. Approve the campaign with default
    deal margin value 40.
    """

    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    # DATA PREPARATION FOR CAMPAIGN_APPROVE
    with open('assets/campaign/campaign_approve_data.json') as json_file:
        provided_campaign_approve_data = json.load(json_file)
    provided_campaign_approve_data_with_deal_margin = copy.deepcopy(
        provided_campaign_approve_data)
    provided_campaign_approve_data_with_deal_margin[
        'private_deal_id'] = 12992
    provided_campaign_approve_data_with_deal_margin['deal_margin'] = 40

    # DATA PREPARATION FOR CAMPAIGN PRIVATE MARKETPLACE AND CREATIVE SET
    with open('assets/campaign/campaign_data.json') as json_file:
        provided_campaign_data = json.load(json_file)

    # DATA PREPARATION FOR REDIS
    with open('assets/campaign/redis_data/redis_data_for_campaign_with_deal_margin_enabled.json') as json_file:
        redis_data_for_campaign_with_deal_margin_enabled = json.load(json_file)

    # CREATE CAMPAIGN BY API
    campaign = CampaignUtil.create_campaign_by_api_with_current_date(config)
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign['name'],
        index=1)
    campaign_view.perform_action("Edit")

    # ADD PRIVATE MARKETPLACE AND CHANGE CREATIVE SET
    campaign_page.click_on_element(CampaignFormLocators.ad_exchanges_section_locator)
    campaign_page.check_uncheck_specific_checkbox(CampaignFormLocators.ad_exchanges_anzu_ingame_checkbox_label,
                                                  do_check=True)
    campaign_page.scroll_to_specific_element(
        CampaignFormLocators.private_marketplace_section_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.private_marketplace_section_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.private_marketplace_label_locator,
        option_to_select="Private auction - Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile ($3.98)")
    campaign_page.scroll_to_specific_element(
        CampaignFormLocators.creative_set_selection_locator)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.creative_set_selection_locator)
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.creative_set_selection_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.creative_set_selection_locator)
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.selected_creative_sets_selection_label,
        option_to_select=provided_campaign_data['landing_and_creatives']['creative'])
    campaign_view.scroll_to_specific_element(
        CampaignFormLocators.publish_button_locator)
    time.sleep(campaign_view.TWO_SEC_DELAY)
    campaign_view.wait_for_presence_of_element(
        CampaignFormLocators.publish_button_locator)
    campaign_view.wait_for_element_to_be_clickable(
        CampaignFormLocators.publish_button_locator)
    try:
        campaign_view.click_on_element(
            CampaignFormLocators.publish_button_locator)
        WebDriverWait(campaign_view.driver, 10).until(
            EC.alert_is_present(),
            'Timed out waiting for alert to appear')
        alert = campaign_view.driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("Alert not present")
    # SEARCH CAMPAIGN AND APPROVE
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign['name'],
        index=1)
    campaign_view.perform_action("Approve")
    deal_margin_value_from_user_settings = campaign_approve_form.get_attribute_value(
        CampaignApproveLocators.
        deal_margin_locator, "value")
    assert '50' == deal_margin_value_from_user_settings
    campaign_approve_form.set_value_into_element(
        CampaignApproveLocators.deal_margin_locator,
        provided_campaign_approve_data_with_deal_margin['deal_margin'])
    campaign_approve_form.click_on_element(
        CampaignApproveLocators.approve_button_locator)
    campaign_approve_form.click_on_element(
        CampaignApproveLocators.ignore_button_locator)

    # PULL DEAL MARGIN DATA FROM DB FOR ASSERTION
    pulled_deal_data_db = CampaignUtil.pull_deal_margin_value_from_db(
        campaign['name'], db_connection)
    for deal_margin_data in pulled_deal_data_db:
        private_deal_id_from_db = list(deal_margin_data.items())[0][1]
        assert private_deal_id_from_db == \
               provided_campaign_approve_data_with_deal_margin[
                   'private_deal_id']
        deal_margin_from_db = list(deal_margin_data.items())[1][1]
        assert deal_margin_from_db == \
               provided_campaign_approve_data_with_deal_margin[
                   'deal_margin']

    # REDIS DATA VERIFICATION
    if "qa-testing" in config['credential']['url']:
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign['campaignId'])
        assert campaign['campaignId'] == redis_data['id']
        assert campaign['name'] == redis_data['name']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_campaign_with_deal_margin_enabled == redis_data

    # DELETE CAMPAIGN
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign['name'],
        index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()


def test_dashboard_campaign_approve_single_approve_deal_margin_disabled(login_by_user_type, open_database_connection):
    """
    Log in as an agency user who does not have deal margin enabled from User Settings.
    Create a campaign. Approve the campaign with default deal margin for this user, value 54.
    """

    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    navbar_page = DashboardNavbar(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_view = DspDashboardCampaignView(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    # DATA PREPARATION FOR IO CREATION
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data_copy = copy.deepcopy(io_data)
    io_data_copy['io_main_information']['io_title'] = \
        io_data_copy['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data_copy['client_profile']['client'] = 'AutomationAgencyUser'

    # DATA PREPARATION FOR CAMPAIGN CREATION
    with open('assets/campaign/campaign_data.json') as json_file:
        provided_campaign_data = json.load(json_file)
    provided_campaign_data_with_deal_margin = copy.deepcopy(
        provided_campaign_data)
    provided_campaign_data_with_deal_margin['name_and_type'][
        'campaign_name'] = \
        provided_campaign_data_with_deal_margin['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    provided_campaign_data_with_deal_margin['landing_and_creatives'][
        'creative'] = \
        'Automation Banner Creative Eskimi New'
    provided_campaign_data_with_deal_margin['private_deal_id'] = 12992
    provided_campaign_data_with_deal_margin['deal_margin'] = 54

    # DATA PREPARATION FOR REDIS
    with open('assets/campaign/redis_data/redis_data_for_campaign_with_deal_margin_disabled.json') as json_file:
        redis_data_for_campaign_with_deal_margin_disabled = json.load(json_file)

    # ADD BUDGET
    if "qa-testing" in config['credential']['url']:
        navbar_page.impersonate_user("AutomationAgencyUser")
        payment_page.add_budget_into_specific_client("AutomationAgencyUser", 10)

    # IMPERSONATE
    navbar_page.login_as("AutomationAgencyUser")

    # CAMPAIGN CREATION
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(
        provided_campaign_data_with_deal_margin)
    campaign_page.provide_campaign_objective(
        provided_campaign_data_with_deal_margin)
    campaign_page.provide_launch_date_and_budget_info(
        provided_campaign_data_with_deal_margin)
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.country_label,
        option_to_select=provided_campaign_data_with_deal_margin[
            'location_and_audiences'][
            'country_name'])
    campaign_page.scroll_to_specific_element(
        CampaignFormLocators.deals_packages_section_locator)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.deals_packages_section_locator)
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.deals_packages_section_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.deals_packages_section_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.deals_packages_section_locator)
    campaign_page.scroll_to_specific_element(
        CampaignFormLocators.private_marketplace_section_locator)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.private_marketplace_section_locator)
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.private_marketplace_section_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.private_marketplace_section_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.private_marketplace_section_locator)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.private_marketplace_selection_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.private_marketplace_selection_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.private_marketplace_selection_locator,
        locator_to_be_appeared=CampaignFormLocators.modal_search_field_locator)
    campaign_page.select_from_modal(
        search_text="Private auction - Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile ($4.33)")
    campaign_page.provide_landing_and_creatives_info(
        provided_campaign_data_with_deal_margin)
    campaign_view.scroll_to_specific_element(CampaignFormLocators.publish_button_locator)
    time.sleep(campaign_view.TWO_SEC_DELAY)
    campaign_view.wait_for_presence_of_element(
        CampaignFormLocators.publish_button_locator)
    campaign_view.wait_for_element_to_be_clickable(
        CampaignFormLocators.publish_button_locator)
    try:
        campaign_view.click_on_element(
            CampaignFormLocators.publish_button_locator)
        WebDriverWait(campaign_view.driver, 10).until(
            EC.alert_is_present(),
            'Timed out waiting for alert to appear')
        alert = campaign_view.driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("Alert not present")

    # CHANGE USER FILTER (In ideal case, we should not be doing this, as after impersonation, user filter
    # should automatically be taking the impersonated user )
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.user_selector)
    campaign_settings_page.select_from_modal(search_text="AutomationAgencyUser")
    campaign_settings_page.wait_for_element_to_be_clickable(
        CampaignSettingsLocator.campaign_search_button_locator)
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.campaign_search_button_locator)

    # CREATE IO AND GET IO
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.navigate_to_add_io()
    io_form_page.provide_io_main_information(io_data_copy)
    io_form_page.select_dropdown_value(IoFormLocators.client_select_data_qa, io_data_copy['client_profile'][
        'client'])
    time.sleep(2)
    io_form_page.click_on_save_and_generate_io_button()
    io_form_page.wait_for_visibility_of_element(
        IoFormLocators.success_message_data_qa)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()
    insertion_order = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag, io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    io = io_data_copy['io_main_information'][
             'io_title'] + " #" + insertion_order
    campaign_list_page.reload_campaign_list_page()

    # APPROVE CAMPAIGN
    campaign_list_page.search_and_action(
        provided_campaign_data_with_deal_margin['name_and_type'][
            'campaign_name'], "Approve")
    campaign_approve_form.select_dropdown_value(CampaignApproveLocators.insertion_order_label, dropdown_item=io)
    campaign_approve_form.scroll_to_specific_element(
        CampaignApproveLocators.approve_button_locator)
    time.sleep(campaign_approve_form.TWO_SEC_DELAY)
    campaign_approve_form.click_on_element(
        CampaignApproveLocators.approve_button_locator)
    time.sleep(campaign_approve_form.TWO_SEC_DELAY)
    campaign_approve_form.click_on_element(
        CampaignApproveLocators.ignore_button_locator)

    # PULL DEAL MARGIN DATA FROM DB FOR ASSERTION
    pulled_deal_data_db = CampaignUtil.pull_deal_margin_value_from_db(
        provided_campaign_data_with_deal_margin['name_and_type'][
            'campaign_name'], db_connection)
    for i in pulled_deal_data_db:
        private_deal_id_from_db = list(i.items())[0][1]
        assert private_deal_id_from_db == \
               provided_campaign_data_with_deal_margin[
                   'private_deal_id']
        deal_margin_from_db = list(i.items())[1][1]
        assert deal_margin_from_db == \
               provided_campaign_data_with_deal_margin[
                   'deal_margin']

    # REDIS DATA VERIFICATION
    if "qa-testing" in config['credential']['url']:
        campaign_id = CampaignUtil.pull_campaign_id_from_db(
            provided_campaign_data_with_deal_margin['name_and_type']['campaign_name'], db_connection, user_id="7716")
        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == redis_data['id']
        assert provided_campaign_data_with_deal_margin['name_and_type']['campaign_name'] == redis_data['name']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_campaign_with_deal_margin_disabled == redis_data

    # DELETE CAMPAIGN
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(
        provided_campaign_data_with_deal_margin['name_and_type'][
            'campaign_name'],
        index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()
