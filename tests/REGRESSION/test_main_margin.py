import json
import time
import pytest
from decimal import Decimal, ROUND_HALF_UP

import math
from selenium.webdriver.common.keys import Keys

from configurations import generic_modules
from locators.all_campaigns.all_campaign_locators import AllCampaignFormLocators
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_list_locator import CampaignListLocators
from locators.campaign.campaign_mass_approve_form_locators import CampaignMassApproveFormLocators
from locators.campaign.campaign_mass_edit_form_locator import CampaignMassEditFormLocator
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from locators.clients.client_management_locator import ClientManagementLocator
from locators.report.report_page_locator import ReportPageLocators
from pages.all_campaigns.all_campaigns_form import DashboardAllCampaignForm
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_approve_form import \
    DspDashboardCampaignsMassApprove
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.clients.client_management import DashboardClientManagement
from pages.navbar.navbar import DashboardNavbar
from pages.report.report_page import DashboardReportPage
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils
from utils.redis import RedisUtils
from utils.page_names_enum import PageNames

campaign_id = []
api_campaign = {'name': '', 'id': ''}
bid_cpm = ''
daily_budget = ''
daily_spend = ''
total_budget = ''
total_spend = ''
campaign_name_list = []
second_api_campaign = {'name': ''}
campaign_name = ''
live_campaign_id = ''
total_budget_from_campaign_edit = ''
updated_main_margin = ''
bid_from_campaign_edit = ''
total_remaining_budget = ''
decimal_updated_main_margin = 0.00
bid_from_campaign_edit_in_usd = ''
creative_type = ''
report_data_admin_view_based_on_cost = []
report_data_admin_view_based_on_revenue = []
report_data_client_view_based_on_cost = []
report_data_client_view_based_on_revenue = []
client_name = ''
selected_budget = ''
total_budget_from_approve = 0.00
daily_budget_from_approve_page = 0.00


@pytest.mark.dependency()
def test_regression_campaign_main_margin_enabled(login_by_user_type, open_database_connection):
    global campaign_id, bid_cpm, api_campaign, daily_budget, daily_spend, total_budget, total_spend, \
        campaign_name_list, second_api_campaign, bid_from_campaign_edit, total_budget_from_campaign_edit, \
        campaign_name, total_budget_from_approve
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    with open('assets/campaign/redis_data/redis_data_for_campaign_main_margin_enabled.json') as json_file:
        redis_data_for_campaign_main_margin_enabled = json.load(json_file)
    with open('assets/campaign/campaign_db_data_for_agency_client_user.json') as json_file:
        expected_campaign_data_db = json.load(json_file)

    print("[START] [RTB-8507] Verify rule for the campaign with the enabled main margin")
    print("[START] CREATE FEW CAMPAIGNS BY API")
    api_campaign = CampaignUtils.create_campaign_by_api_with_current_date(config, user_type="agency-client")
    campaign_id = CampaignUtils.pull_campaign_id_from_db(api_campaign['name'], db_connection, user_id="7718")
    second_api_campaign = CampaignUtils.create_campaign_by_api_with_current_date(config, user_type="agency-client")
    campaign_name_list = [api_campaign['name'], second_api_campaign['name']]
    print("[END] CREATE FEW CAMPAIGNS BY API")

    print("[START] CAMPAIGN DATA VERIFICATION IN DB")
    pulled_campaign_data_db = CampaignUtils.pull_campaign_data_from_db_without_status(
        api_campaign['name'], db_connection, user_id="7718")
    print(pulled_campaign_data_db)
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] CAMPAIGN DATA VERIFICATION IN DB")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")
    campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
        'campaign-approve-url'].format(str(campaign_id[0]['id']))
    driver.get(campaign_approve_url)
    main_margin = campaign_approve_form.get_attribute_value(CampaignApproveLocators.main_margin_locator, "value")
    daily_spend = '0.00'
    total_spend = '0.00'
    bid_cpm = '{:.2f}'.format(api_campaign['bid'])
    daily_budget = '{:.2f}'.format(api_campaign['budget']['daily'])
    total_budget = '{:.2f}'.format(api_campaign['budget']['total'])
    creatives_bids_from_approve_page = campaign_approve_form.get_creatives_bids()
    for creative_bid in creatives_bids_from_approve_page:
        creative_bid = creative_bid.split('$')[1]
        assert creative_bid == bid_cpm
    bid_from_approve_page = campaign_approve_form.get_bid()
    assert bid_cpm == bid_from_approve_page
    daily_budget_from_approve = campaign_approve_form.get_daily_budget()
    assert daily_budget == daily_budget_from_approve
    daily_spend_from_approve = campaign_approve_form.get_daily_spend()
    assert daily_spend == daily_spend_from_approve
    total_budget_from_approve = campaign_approve_form.get_total_budget()
    assert Decimal(total_budget) == Decimal(total_budget_from_approve)
    total_spend_from_approve = campaign_approve_form.get_total_spend()
    assert total_spend == total_spend_from_approve
    campaign_approve_form.click_approve_button()
    campaign_approve_form.click_on_element(
        CampaignApproveLocators.ignore_button_locator, locator_to_be_appeared=AllCampaignFormLocators.filter_btn)
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.set_value_into_element(AllCampaignFormLocators.search_filter_locator, campaign_id[0]['id'])
    all_campaign_form.wait_for_presence_of_element(AllCampaignFormLocators.search_filter_locator).send_keys(Keys.ENTER)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    bid_from_all_campaigns = all_campaign_form.get_element_text(AllCampaignFormLocators.table_row_bid_by_xpath.format(
        campaign_id[0]['id']), locator_initialization=True).split("$")[1]
    assert bid_cpm == bid_from_all_campaigns
    daily_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_daily_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert daily_budget == daily_budget_from_all_campaigns
    total_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_total_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert total_budget == total_budget_from_all_campaigns
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.select_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa,
                                                                option_to_select="AutomationAgencyClientUser")
    campaign_settings_page.search_and_click_on_campaign_name(api_campaign['name'], index=1,
                                                             click_on_campaign_name=False)
    campaign_settings_page.wait_for_spinner_load()
    bid_from_campaign_settings = campaign_settings_page.get_bid_cpm(campaign_id[0]['id'])
    assert bid_cpm == bid_from_campaign_settings
    daily_budget_from_campaign_settings = campaign_settings_page.get_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_settings
    daily_spend_from_campaign_settings = campaign_settings_page.get_today_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_settings
    total_budget_from_campaigns_setting = campaign_settings_page.get_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_setting
    total_spend_from_campaign_settings = campaign_settings_page.get_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_settings
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id[0]['id']))
    driver.get(campaign_edit_url)
    bid_from_campaign_edit = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_edit
    daily_budget_from_campaign_edit = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_edit
    total_budget_from_campaign_edit = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_edit
    creatives_bids_from_campaign_edit = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_edit:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.three_dot_of_campaign_xpath.format(api_campaign['name']))
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.campaign_list_duplicate_locator.format(campaign_id[0]['id']))
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + api_campaign['name'], action='edit')
    bid_from_campaign_duplicate = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_duplicate
    daily_budget_from_campaign_duplicate = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_duplicate
    total_budget_from_campaign_duplicate = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_duplicate
    creatives_bids_from_campaign_duplicate = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_duplicate:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign",
        switch_to_new_window=True)
    bid_from_mass_edit = campaign_page.get_text_or_value_from_list(
        CampaignMassEditFormLocator.bid_fields_locator, attribute_name="value")
    for bid in bid_from_mass_edit:
        assert bid == bid_cpm
    daily_budget_from_mass_edit = campaign_page.get_text_or_value_from_list(
        CampaignMassEditFormLocator.daily_budget_fields_locator)
    for budget in daily_budget_from_mass_edit:
        assert budget == daily_budget
    total_budget_from_mass_edit = campaign_page.get_text_or_value_from_list(
        CampaignMassEditFormLocator.total_budget_fields_locator)
    for budget in total_budget_from_mass_edit:
        assert budget == total_budget
    campaign_list_page.close_the_current_window_and_back_to_previous_window()
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")

    if "qa-testing" in config['credential']['url']:
        print("[START] REDIS DATA VERIFICATION")
        payment_page.add_budget_into_specific_client(config['credential']['agency-client-username'], 10)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, (campaign_id[0]['id']),
                                                                           key="winConfig")
        assert campaign_id[0]['id'] == redis_data['campaignId']
        main_margin_percentages = int(main_margin) / 100
        campaign_daily_budget = int(api_campaign['budget']['daily'])
        redis_daily_budget = campaign_daily_budget - (campaign_daily_budget * main_margin_percentages)
        assert redis_daily_budget == redis_data['budget']['currency']['daily']
        campaign_total_budget = int(api_campaign['budget']['total'])
        redis_total_budget = campaign_total_budget - (campaign_total_budget * main_margin_percentages)
        assert redis_total_budget == redis_data['budget']['currency']['total']
        redis_data['budget']['currency']['daily'] = ""
        redis_data['budget']['currency']['total'] = ""
        redis_data['campaignId'] = ""
        redis_data['user']['targetDmpIds'] = []

        assert redis_data_for_campaign_main_margin_enabled == redis_data
        print("[END] REDIS DATA VERIFICATION")


@pytest.mark.dependency(depends=['test_regression_campaign_main_margin_enabled'])
def test_regression_campaign_main_margin_enabled_two(login_by_user_type, open_database_connection):
    global campaign_id, bid_cpm, api_campaign, daily_budget, daily_spend, total_budget, total_spend, \
        campaign_name_list, second_api_campaign, bid_from_campaign_edit, total_budget_from_campaign_edit, \
        campaign_name, total_budget_from_approve
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    navbar = DashboardNavbar(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)

    navbar.login_as("AutomationAgencyUser")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")
    campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
        'campaign-approve-url'].format(str(campaign_id[0]['id']))
    driver.get(campaign_approve_url)
    creatives_bids_from_approve_page = campaign_approve_form.get_creatives_bids()
    for creative_bid in creatives_bids_from_approve_page:
        creative_bid = creative_bid.split('$')[1]
        assert creative_bid == bid_cpm
    bid_from_approve_page = campaign_approve_form.get_bid()
    assert bid_cpm == bid_from_approve_page
    daily_budget_from_approve = campaign_approve_form.get_daily_budget()
    assert daily_budget == daily_budget_from_approve
    daily_spend_from_approve = campaign_approve_form.get_daily_spend()
    assert daily_spend == daily_spend_from_approve
    total_budget_from_approve = campaign_approve_form.get_total_budget()
    assert Decimal(total_budget) == Decimal(total_budget_from_approve)
    total_spend_from_approve = campaign_approve_form.get_total_spend()
    assert total_spend == total_spend_from_approve
    campaign_approve_form.click_on_element(CampaignApproveLocators.cancel_button_locator)
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.select_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa,
                                                                option_to_select="AutomationAgencyClientUser")
    campaign_settings_page.search_and_click_on_campaign_name(api_campaign['name'], index=1,
                                                             click_on_campaign_name=False)
    campaign_settings_page.wait_for_spinner_load()
    bid_from_campaign_settings = campaign_settings_page.get_bid_cpm(campaign_id[0]['id'])
    assert bid_cpm == bid_from_campaign_settings
    daily_budget_from_campaign_settings = campaign_settings_page.get_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_settings
    daily_spend_from_campaign_settings = campaign_settings_page.get_today_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_settings
    total_budget_from_campaigns_setting = campaign_settings_page.get_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_setting
    total_spend_from_campaign_settings = campaign_settings_page.get_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_settings
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id[0]['id']))
    driver.get(campaign_edit_url)
    bid_from_campaign_edit = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_edit
    daily_budget_from_campaign_edit = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_edit
    total_budget_from_campaign_edit = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_edit
    creatives_bids_from_campaign_edit = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_edit:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.three_dot_of_campaign_xpath.format(api_campaign['name']))
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.campaign_list_duplicate_locator.format(campaign_id[0]['id']))
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + api_campaign['name'], action='edit')
    bid_from_campaign_duplicate = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_duplicate
    daily_budget_from_campaign_duplicate = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_duplicate
    total_budget_from_campaign_duplicate = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_duplicate
    creatives_bids_from_campaign_duplicate = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_duplicate:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    # FILTER COLUMNS NOT WORKING AND WE CAN"T SEE TOTAL BUDGET, registered a bug
    # https://eskimidev.atlassian.net/browse/RTB-8586
    # campaign_list_page.select_item_from_campaign_multi_action_menu(
    #     "Mass edit campaign",
    #     switch_to_new_window=True)
    # total_budget_from_mass_edit = campaign_page.get_text_or_value_from_list(
    #     CampaignMassEditFormLocator.total_budget_fields_locator, attribute_name="value")
    # for budget in total_budget_from_mass_edit:
    #     assert budget == total_budget
    # campaign_list_page.close_the_current_window_and_back_to_previous_window()
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")

    navbar.logout_as()
    navbar.login_as("AutomationAgencyClientUser")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGNS LIST PAGE")
    campaign_list_page.search_and_action(api_campaign['name'])
    daily_budget_from_campaign_list = campaign_list_page.get_campaign_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_list
    daily_spend_from_campaign_list = campaign_list_page.get_campaign_daily_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_list
    total_budget_from_campaigns_list = campaign_list_page.get_campaign_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_list
    total_spend_from_campaign_list = campaign_list_page.get_campaign_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_list
    e_cpm_from_campaign_list = campaign_list_page.get_element_text(
        CampaignListLocators.e_cpm_xpath.format(campaign_id[0]['id']), locator_initialization=True)
    assert '$ 0.00' == e_cpm_from_campaign_list
    e_cpc_from_campaign_list = campaign_list_page.get_element_text(
        CampaignListLocators.e_cpc_xpath.format(campaign_id[0]['id']), locator_initialization=True)
    assert '$ 0.00' == e_cpc_from_campaign_list
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGNS LIST PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.set_value_into_element(AllCampaignFormLocators.search_filter_locator, campaign_id[0]['id'])
    all_campaign_form.wait_for_presence_of_element(AllCampaignFormLocators.search_filter_locator).send_keys(Keys.ENTER)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    bid_from_all_campaigns = all_campaign_form.get_element_text(AllCampaignFormLocators.table_row_bid_by_xpath.format(
        campaign_id[0]['id']), locator_initialization=True).split("$")[1]
    assert bid_cpm == bid_from_all_campaigns
    daily_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_daily_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert daily_budget == daily_budget_from_all_campaigns
    total_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_total_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert total_budget == total_budget_from_all_campaigns
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.search_and_click_on_campaign_name(api_campaign['name'], index=1,
                                                             click_on_campaign_name=False)
    campaign_settings_page.wait_for_spinner_load()
    bid_from_campaign_settings = campaign_settings_page.get_bid_cpm(campaign_id[0]['id'])
    assert bid_cpm == bid_from_campaign_settings
    daily_budget_from_campaign_settings = campaign_settings_page.get_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_settings
    daily_spend_from_campaign_settings = campaign_settings_page.get_today_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_settings
    total_budget_from_campaigns_setting = campaign_settings_page.get_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_setting
    total_spend_from_campaign_settings = campaign_settings_page.get_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_settings
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id[0]['id']))
    driver.get(campaign_edit_url)
    bid_from_campaign_edit = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_edit
    daily_budget_from_campaign_edit = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_edit
    total_budget_from_campaign_edit = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_edit
    creatives_bids_from_campaign_edit = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_edit:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] CAMPAIGN CLEAN UP")
    campaign_id_from_db = CampaignUtils.pull_campaign_id_from_db(api_campaign['name'], db_connection, user_id="7718")
    status = CampaignUtils.delete_campaign_by_api(config, campaign_id_from_db[0]['id'])
    assert True is status
    second_campaign_id_from_db = CampaignUtils.pull_campaign_id_from_db(second_api_campaign['name'], db_connection,
                                                                        user_id="7718")
    status = CampaignUtils.delete_campaign_by_api(config, second_campaign_id_from_db[0]['id'])
    assert True is status
    print("[END] CAMPAIGN CLEAN UP")
    print("[END] [RTB-8507] Verify rule for the campaign with the enabled main margin")


@pytest.mark.dependency()
def test_regression_campaign_main_margin_edited(login_by_user_type, open_database_connection):
    global api_campaign, campaign_id, second_api_campaign, campaign_name_list, daily_spend, total_spend, bid_cpm, \
        daily_budget, total_budget, bid_from_campaign_edit, total_budget_from_campaign_edit, campaign_name, \
        total_budget_from_approve
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    with open('assets/campaign/redis_data/redis_data_for_campaign_main_margin_enabled.json') as json_file:
        redis_data_for_campaign_main_margin_enabled = json.load(json_file)
    with open('assets/campaign/campaign_db_data_for_agency_client_user.json') as json_file:
        expected_campaign_data_db = json.load(json_file)

    print("[START] [RTB-8508] Verify rule for the campaign with the edited main margin")
    print("[START] CREATE FEW CAMPAIGNS BY API")
    api_campaign = CampaignUtils.create_campaign_by_api_with_current_date(config, user_type="agency-client")
    campaign_id = CampaignUtils.pull_campaign_id_from_db(api_campaign['name'], db_connection, user_id="7718")
    second_api_campaign = CampaignUtils.create_campaign_by_api_with_current_date(config, user_type="agency-client")
    campaign_name_list = [api_campaign['name'], second_api_campaign['name']]
    print("[END] CREATE FEW CAMPAIGNS BY API")

    print("[START] EDIT MAIN MARGIN")
    campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
        'campaign-approve-url'].format(str(campaign_id[0]['id']))
    driver.get(campaign_approve_url)
    main_margin = "20"
    campaign_approve_form.set_value_into_element(CampaignApproveLocators.main_margin_locator, main_margin)
    campaign_approve_form.click_approve_button()
    # ASSERTION FOR THE ABSENCE OF THE MAIN MARGIN MODAL
    assert False is campaign_approve_form.is_element_present(CampaignApproveLocators.publish_change_button_locator,
                                                             time_out=3)
    campaign_approve_form.accept_creative_size_pop_up()
    print("[END] EDIT MAIN MARGIN")

    print("[START] CAMPAIGN DATA VERIFICATION IN DB")
    pulled_campaign_data_db = CampaignUtils.pull_campaign_data_from_db_without_status(
        api_campaign['name'], db_connection, user_id="7718")
    print(pulled_campaign_data_db)
    expected_campaign_data_db['margin_main'] = Decimal(main_margin)
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] CAMPAIGN DATA VERIFICATION IN DB")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")
    campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
        'campaign-approve-url'].format(str(campaign_id[0]['id']))
    driver.get(campaign_approve_url)
    daily_spend = '0.00'
    total_spend = '0.00'
    bid_cpm = '{:.2f}'.format(api_campaign['bid'])
    daily_budget = '{:.2f}'.format(api_campaign['budget']['daily'])
    total_budget = '{:.2f}'.format(api_campaign['budget']['total'])
    creatives_bids_from_approve_page = campaign_approve_form.get_creatives_bids()
    for creative_bid in creatives_bids_from_approve_page:
        creative_bid = creative_bid.split('$')[1]
        assert creative_bid == bid_cpm
    bid_from_approve_page = campaign_approve_form.get_bid()
    assert bid_cpm == bid_from_approve_page
    daily_budget_from_approve = campaign_approve_form.get_daily_budget()
    assert daily_budget == daily_budget_from_approve
    daily_spend_from_approve = campaign_approve_form.get_daily_spend()
    assert daily_spend == daily_spend_from_approve
    total_budget_from_approve = campaign_approve_form.get_total_budget()
    assert Decimal(total_budget) == Decimal(total_budget_from_approve)
    total_spend_from_approve = campaign_approve_form.get_total_spend()
    assert total_spend == total_spend_from_approve
    campaign_approve_form.click_on_element(CampaignApproveLocators.cancel_button_locator)
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.set_value_into_element(AllCampaignFormLocators.search_filter_locator, campaign_id[0]['id'])
    all_campaign_form.wait_for_presence_of_element(AllCampaignFormLocators.search_filter_locator).send_keys(Keys.ENTER)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    bid_from_all_campaigns = all_campaign_form.get_element_text(AllCampaignFormLocators.table_row_bid_by_xpath.format(
        campaign_id[0]['id']), locator_initialization=True).split("$")[1]
    assert bid_cpm == bid_from_all_campaigns
    daily_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_daily_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert daily_budget == daily_budget_from_all_campaigns
    total_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_total_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert total_budget == total_budget_from_all_campaigns
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.select_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa,
                                                                option_to_select="AutomationAgencyClientUser")
    campaign_settings_page.search_and_click_on_campaign_name(api_campaign['name'], index=1,
                                                             click_on_campaign_name=False)
    campaign_settings_page.wait_for_spinner_load()
    bid_from_campaign_settings = campaign_settings_page.get_bid_cpm(campaign_id[0]['id'])
    assert bid_cpm == bid_from_campaign_settings
    daily_budget_from_campaign_settings = campaign_settings_page.get_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_settings
    daily_spend_from_campaign_settings = campaign_settings_page.get_today_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_settings
    total_budget_from_campaigns_setting = campaign_settings_page.get_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_setting
    total_spend_from_campaign_settings = campaign_settings_page.get_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_settings
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id[0]['id']))
    driver.get(campaign_edit_url)
    bid_from_campaign_edit = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_edit
    daily_budget_from_campaign_edit = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_edit
    total_budget_from_campaign_edit = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_edit
    creatives_bids_from_campaign_edit = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_edit:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.three_dot_of_campaign_xpath.format(api_campaign['name']))
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.campaign_list_duplicate_locator.format(campaign_id[0]['id']))
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + api_campaign['name'], action='edit')
    bid_from_campaign_duplicate = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_duplicate
    daily_budget_from_campaign_duplicate = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_duplicate
    total_budget_from_campaign_duplicate = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_duplicate
    creatives_bids_from_campaign_duplicate = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_duplicate:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign",
        switch_to_new_window=True)
    bid_from_mass_edit = campaign_page.get_text_or_value_from_list(
        CampaignMassEditFormLocator.bid_fields_locator, attribute_name="value")
    for bid in bid_from_mass_edit:
        assert bid == bid_cpm
    daily_budget_from_mass_edit = campaign_page.get_text_or_value_from_list(
        CampaignMassEditFormLocator.daily_budget_fields_locator)
    for budget in daily_budget_from_mass_edit:
        assert budget == daily_budget
    total_budget_from_mass_edit = campaign_page.get_text_or_value_from_list(
        CampaignMassEditFormLocator.total_budget_fields_locator)
    for budget in total_budget_from_mass_edit:
        assert budget == total_budget
    campaign_list_page.close_the_current_window_and_back_to_previous_window()
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")

    if "qa-testing" in config['credential']['url']:
        print("[START] REDIS DATA VERIFICATION")
        payment_page.add_budget_into_specific_client(config['credential']['agency-client-username'], 10)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, (campaign_id[0]['id']),
                                                                           key="winConfig")
        assert campaign_id[0]['id'] == redis_data['campaignId']
        main_margin_percentages = int(main_margin) / 100
        campaign_daily_budget = int(api_campaign['budget']['daily'])
        redis_daily_budget = campaign_daily_budget - (campaign_daily_budget * main_margin_percentages)
        assert redis_daily_budget == redis_data['budget']['currency']['daily']
        campaign_total_budget = int(api_campaign['budget']['total'])
        redis_total_budget = campaign_total_budget - (campaign_total_budget * main_margin_percentages)
        assert redis_total_budget == redis_data['budget']['currency']['total']
        redis_data['budget']['currency']['daily'] = ""
        redis_data['budget']['currency']['total'] = ""
        redis_data['campaignId'] = ""
        redis_data['user']['targetDmpIds'] = []

        assert redis_data_for_campaign_main_margin_enabled == redis_data
        print("[END] REDIS DATA VERIFICATION")


@pytest.mark.dependency(depends=['test_regression_campaign_main_margin_edited'])
def test_regression_campaign_main_margin_edited_two(login_by_user_type, open_database_connection):
    global api_campaign, campaign_id, second_api_campaign, campaign_name_list, daily_spend, total_spend, bid_cpm, \
        daily_budget, total_budget, campaign_name, bid_from_campaign_edit, total_budget_from_campaign_edit, \
        total_budget_from_approve
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    navbar = DashboardNavbar(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)

    navbar.login_as("AutomationAgencyUser")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")
    campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
        'campaign-approve-url'].format(str(campaign_id[0]['id']))
    driver.get(campaign_approve_url)
    creatives_bids_from_approve_page = campaign_approve_form.get_creatives_bids()
    for creative_bid in creatives_bids_from_approve_page:
        creative_bid = creative_bid.split('$')[1]
        assert creative_bid == bid_cpm
    bid_from_approve_page = campaign_approve_form.get_bid()
    assert bid_cpm == bid_from_approve_page
    daily_budget_from_approve = campaign_approve_form.get_daily_budget()
    assert daily_budget == daily_budget_from_approve
    daily_spend_from_approve = campaign_approve_form.get_daily_spend()
    assert daily_spend == daily_spend_from_approve
    total_budget_from_approve = campaign_approve_form.get_total_budget()
    assert Decimal(total_budget) == Decimal(total_budget_from_approve)
    total_spend_from_approve = campaign_approve_form.get_total_spend()
    assert total_spend == total_spend_from_approve
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN APPROVE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.select_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa,
                                                                option_to_select="AutomationAgencyClientUser")
    campaign_settings_page.search_and_click_on_campaign_name(api_campaign['name'], index=1,
                                                             click_on_campaign_name=False)
    campaign_settings_page.wait_for_spinner_load()
    bid_from_campaign_settings = campaign_settings_page.get_bid_cpm(campaign_id[0]['id'])
    assert bid_cpm == bid_from_campaign_settings
    daily_budget_from_campaign_settings = campaign_settings_page.get_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_settings
    daily_spend_from_campaign_settings = campaign_settings_page.get_today_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_settings
    total_budget_from_campaigns_setting = campaign_settings_page.get_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_setting
    total_spend_from_campaign_settings = campaign_settings_page.get_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_settings
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id[0]['id']))
    driver.get(campaign_edit_url)
    bid_from_campaign_edit = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_edit
    daily_budget_from_campaign_edit = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_edit
    total_budget_from_campaign_edit = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_edit
    creatives_bids_from_campaign_edit = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_edit:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.three_dot_of_campaign_xpath.format(api_campaign['name']))
    campaign_list_page.click_element_execute_script(
        CampaignSettingsLocator.campaign_list_duplicate_locator.format(campaign_id[0]['id']))
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + api_campaign['name'], action='edit')
    bid_from_campaign_duplicate = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_duplicate
    daily_budget_from_campaign_duplicate = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_duplicate
    total_budget_from_campaign_duplicate = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_duplicate
    creatives_bids_from_campaign_duplicate = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_duplicate:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN DUPLICATE PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    # FILTER COLUMNS NOT WORKING AND WE CAN"T SEE TOTAL BUDGET, registered a bug
    # https://eskimidev.atlassian.net/browse/RTB-8586
    # campaign_list_page.select_item_from_campaign_multi_action_menu(
    #     "Mass edit campaign",
    #     switch_to_new_window=True)
    # total_budget_from_mass_edit = campaign_page.get_text_or_value_from_list(
    #     CampaignMassEditFormLocator.total_budget_fields_locator, attribute_name="value")
    # for budget in total_budget_from_mass_edit:
    #     assert budget == total_budget
    # campaign_list_page.close_the_current_window_and_back_to_previous_window()
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN MASS EDIT PAGE")

    navbar.logout_as()
    navbar.login_as("AutomationAgencyClientUser")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGNS LIST PAGE")
    campaign_list_page.search_and_action(api_campaign['name'])
    daily_budget_from_campaign_list = campaign_list_page.get_campaign_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_list
    daily_spend_from_campaign_list = campaign_list_page.get_campaign_daily_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_list
    total_budget_from_campaigns_list = campaign_list_page.get_campaign_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_list
    total_spend_from_campaign_list = campaign_list_page.get_campaign_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_list
    e_cpm_from_campaign_list = campaign_list_page.get_element_text(
        CampaignListLocators.e_cpm_xpath.format(campaign_id[0]['id']), locator_initialization=True)
    assert '$ 0.00' == e_cpm_from_campaign_list
    e_cpc_from_campaign_list = campaign_list_page.get_element_text(
        CampaignListLocators.e_cpc_xpath.format(campaign_id[0]['id']), locator_initialization=True)
    assert '$ 0.00' == e_cpc_from_campaign_list
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGNS LIST PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.set_value_into_element(AllCampaignFormLocators.search_filter_locator, campaign_id[0]['id'])
    all_campaign_form.wait_for_presence_of_element(AllCampaignFormLocators.search_filter_locator).send_keys(Keys.ENTER)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    bid_from_all_campaigns = all_campaign_form.get_element_text(AllCampaignFormLocators.table_row_bid_by_xpath.format(
        campaign_id[0]['id']), locator_initialization=True).split("$")[1]
    assert bid_cpm == bid_from_all_campaigns
    daily_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_daily_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert daily_budget == daily_budget_from_all_campaigns
    total_budget_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_total_budget_by_xpath.format(campaign_id[0]['id']),
        locator_initialization=True).split("$")[2]
    assert total_budget == total_budget_from_all_campaigns
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN ALL CAMPAIGNS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.search_and_click_on_campaign_name(api_campaign['name'], index=1,
                                                             click_on_campaign_name=False)
    campaign_settings_page.wait_for_spinner_load()
    bid_from_campaign_settings = campaign_settings_page.get_bid_cpm(campaign_id[0]['id'])
    assert bid_cpm == bid_from_campaign_settings
    daily_budget_from_campaign_settings = campaign_settings_page.get_daily_budget(campaign_id[0]['id'])
    assert daily_budget == daily_budget_from_campaign_settings
    daily_spend_from_campaign_settings = campaign_settings_page.get_today_spend(campaign_id[0]['id'])
    assert daily_spend == daily_spend_from_campaign_settings
    total_budget_from_campaigns_setting = campaign_settings_page.get_total_budget(campaign_id[0]['id'])
    assert total_budget == total_budget_from_campaigns_setting
    total_spend_from_campaign_settings = campaign_settings_page.get_total_spend(campaign_id[0]['id'])
    assert total_spend == total_spend_from_campaign_settings
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN SETTINGS PAGE")

    print("[START] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id[0]['id']))
    driver.get(campaign_edit_url)
    bid_from_campaign_edit = campaign_page.get_bid_cpm()
    assert bid_cpm == bid_from_campaign_edit
    daily_budget_from_campaign_edit = campaign_page.get_estimated_budget()
    assert daily_budget == daily_budget_from_campaign_edit
    total_budget_from_campaign_edit = campaign_page.get_budget_amount()
    assert total_budget == total_budget_from_campaign_edit
    creatives_bids_from_campaign_edit = campaign_page.get_creatives_bids()
    for creative_bid in creatives_bids_from_campaign_edit:
        assert creative_bid == str(api_campaign['bid'])
    campaign_page.click_save_cancel_or_draft("cancel")
    print("[END] METRICS RELATED TO BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] CAMPAIGN CLEAN UP")
    campaign_id_from_db = CampaignUtils.pull_campaign_id_from_db(api_campaign['name'], db_connection, user_id="7718")
    status = CampaignUtils.delete_campaign_by_api(config, campaign_id_from_db[0]['id'])
    assert True is status
    second_campaign_id_from_db = CampaignUtils.pull_campaign_id_from_db(second_api_campaign['name'], db_connection,
                                                                        user_id="7718")
    status = CampaignUtils.delete_campaign_by_api(config, second_campaign_id_from_db[0]['id'])
    assert True is status
    print("[END] CAMPAIGN CLEAN UP")
    print("[END] [RTB-8508] Verify rule for the campaign with the edited main margin")


@pytest.mark.dependency
def test_regression_edit_main_margin_from_approval_page(login_by_user_type, open_database_connection):
    global campaign_name, live_campaign_id, creative_type, bid_from_campaign_edit, bid_from_campaign_edit_in_usd, \
        total_budget_from_campaign_edit, report_data_admin_view_based_on_cost, \
        report_data_admin_view_based_on_revenue, report_data_client_view_based_on_revenue, \
        report_data_client_view_based_on_cost, updated_main_margin, decimal_updated_main_margin, \
        total_remaining_budget, client_name, selected_budget, total_budget_from_approve, daily_budget_from_approve_page
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-8848] Verify that user is able to change the main margin on approval page")

    if "qa-testing" in config['credential']['url']:
        print("[START] GET CAMPAIGN FROM DB")
        live_campaign_id = CampaignUtils.pull_specific_campaign_id_from_db(db_connection)
        user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
        payment_page.display_budget_information(user_id)
        print("[END] GET CAMPAIGN FROM DB")

        print("[START] GET SPENT FROM REDIS")
        amount_already_spent = redis_page.get_total_spent_amount(redis_connection, live_campaign_id)
        print("[END] GET SPENT FROM REDIS")

        print("[START] GET DATA FROM EDIT PAGE BEFORE EDITING MAIN MARGIN")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        campaign_name = campaign_page.get_text_using_tag_attribute(
            campaign_page.input_tag, campaign_page.id_attribute, CampaignFormLocators.campaign_field_id)
        creative_type = campaign_page.get_text_using_tag_attribute(campaign_page.span_tag, campaign_page.id_attribute,
                                                                   CampaignFormLocators.type_field_id)
        bid_from_campaign_edit = campaign_page.get_bid_cpm()
        bid_from_campaign_edit_in_usd = campaign_page.get_bid_in_usd()
        selected_budget = campaign_page.get_selected_budget()
        print("[END] GET DATA FROM EDIT PAGE BEFORE EDITING MAIN MARGIN")

        print("[START] GET DATA FROM APPROVAL PAGE AND SELECT REPORT OPTIONS")
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(live_campaign_id))
        driver.get(campaign_approve_url)
        client_name = campaign_approve_form.get_element_text(CampaignApproveLocators.client_name_data_qa)
        client_name = client_name.split("(", 1)[0].strip()
        campaign_approve_form.select_budget_related_metrics_to_see_it_in_report()
        campaign_approve_form.click_approve_button()
        campaign_approve_form.accept_creative_size_pop_up()
        print("[END] GET DATA FROM APPROVAL PAGE AND SELECT REPORT OPTIONS")

        print("[START] GET DATA FROM REPORT PAGE BEFORE EDITING MAIN MARGIN")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
            report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost = \
            report_page.generate_different_reports_and_get_data(campaign_name, live_campaign_id)
        print("[END] GET DATA FROM REPORT PAGE BEFORE EDITING MAIN MARGIN")

        print("[START] EDIT MAIN MARGIN AND APPROVE")
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(live_campaign_id))
        driver.get(campaign_approve_url)
        # CALCULATION
        current_main_margin = float(campaign_approve_form.get_attribute_value(
            CampaignApproveLocators.main_margin_locator, "value"))
        total_budget_from_approve = campaign_approve_form.get_total_budget()
        daily_budget_from_approve_page = campaign_approve_form.get_daily_budget()
        max_allowed_main_margin = campaign_approve_form.get_calculated_max_allowed_main_margin(
            total_budget_from_approve, amount_already_spent)

        generic_modules.step_info(
            "[START - RTB-8849] Verify when the main margin % is too high and cannot be updated in approval page")
        too_high_main_margin = campaign_approve_form.get_too_high_main_margin(max_allowed_main_margin)
        campaign_approve_form.set_value_into_element(CampaignApproveLocators.main_margin_locator, too_high_main_margin)
        campaign_approve_form.click_approve_button()
        assert "The main margin cannot exceed {}%. Please increase the campaign’s total budget first.".format(
            max_allowed_main_margin) in campaign_approve_form.get_element_text(
            CampaignApproveLocators.error_message_locator)
        generic_modules.step_info(
            "[END - RTB-8849] Verify when the main margin % is too high and cannot be updated in approval page")

        updated_main_margin = campaign_approve_form.get_updated_main_margin(current_main_margin,
                                                                            max_allowed_main_margin)
        campaign_approve_form.set_value_into_element(CampaignApproveLocators.main_margin_locator, updated_main_margin)
        decimal_updated_main_margin = updated_main_margin / 100
        total_remaining_budget = campaign_approve_form.get_total_remaining_budget(
            total_budget_from_approve, amount_already_spent, decimal_updated_main_margin)
        campaign_approve_form.click_approve_button()
        time.sleep(2)
        assert True is campaign_approve_form.is_element_displayed(
            CampaignApproveLocators.main_margin_changes_modal_title_locator)
        total_remaining_budget_from_modal = campaign_approve_form.get_element_text(
            CampaignApproveLocators.modal_message_locator)
        assert str(total_remaining_budget) in total_remaining_budget_from_modal
        campaign_approve_form.click_on_element(CampaignApproveLocators.main_margin_changes_modal_confirm_btn_locator)
        print("[END] EDIT MAIN MARGIN AND APPROVE")


@pytest.mark.dependency(depends=['test_regression_edit_main_margin_from_approval_page'])
def test_regression_edit_main_margin_from_approval_page_two(login_by_user_type, open_database_connection):
    global campaign_name, live_campaign_id, creative_type, bid_from_campaign_edit, bid_from_campaign_edit_in_usd, \
        total_budget_from_campaign_edit, report_data_admin_view_based_on_cost, \
        report_data_admin_view_based_on_revenue, report_data_client_view_based_on_revenue, \
        report_data_client_view_based_on_cost, updated_main_margin, decimal_updated_main_margin, \
        total_remaining_budget, client_name, selected_budget, total_budget_from_approve, daily_budget_from_approve_page
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    if "qa-testing" in config['credential']['url']:
        print("[START] TOTAL BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")
        campaign_list_page.reload_campaign_list_page()
        navbar.impersonate_user(client_name)
        campaign_list_page.select_all_status()
        campaign_list_page.search_and_action(campaign_name)
        today_spend = float(campaign_list_page.get_campaign_daily_spend(live_campaign_id))
        total_budget_from_campaign_list = campaign_list_page.get_campaign_total_budget(live_campaign_id)
        assert float(total_budget_from_approve) == float(total_budget_from_campaign_list)
        print("[END] TOTAL BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")

        print("[START] UPDATED MAIN MARGIN VERIFICATION IN DB")
        pulled_updated_main_margin_db = CampaignUtils.pull_campaign_main_margin_from_db(live_campaign_id, db_connection)
        assert updated_main_margin == int(pulled_updated_main_margin_db)
        print("[END] UPDATED MAIN MARGIN VERIFICATION IN DB")

        print("[START] METRICS RELATED TO BUDGET VERIFICATION IN EDIT PAGE")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
        bid_after_main_margin_update_from_ui = campaign_page.get_text_using_tag_attribute(
            campaign_page.input_tag, campaign_page.id_attribute, CampaignFormLocators.bid_cpm_field_id)
        daily_budget_after_main_margin_update_db = CampaignUtils.pull_campaign_daily_budget_from_db(
            live_campaign_id, db_connection)
        daily_remaining_budget = Decimal(daily_budget_after_main_margin_update_db - today_spend).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP)
        budget_after_main_margin_update = float(campaign_page.get_budget_amount())
        estimated_budget_from_ui = campaign_page.get_estimated_budget()
        if selected_budget == 'total':
            remaining_total_budget_from_ui = campaign_page.get_remaining_budget()
            daily_budget_after_main_margin_update = (float(remaining_total_budget_from_ui) + today_spend) / float(
                remaining_days)
            assert total_budget_from_approve == budget_after_main_margin_update
            assert float("{:.2f}".format(daily_budget_after_main_margin_update)) == float(estimated_budget_from_ui)
            assert float(remaining_total_budget_from_ui) == float(total_remaining_budget)
        else:
            assert float("{:.2f}".format(budget_after_main_margin_update)) == float(daily_budget_from_approve_page)
            remaining_daily_budget_from_ui = campaign_page.get_remaining_budget()
            assert float(remaining_daily_budget_from_ui) == float(daily_remaining_budget)
            assert total_budget_from_approve == float(estimated_budget_from_ui)
        assert bid_after_main_margin_update_from_ui == bid_from_campaign_edit
        print("[END] METRICS RELATED TO BUDGET VERIFICATION IN EDIT PAGE")

        print("[START] REDIS DATA VERIFICATION")
        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, live_campaign_id,
                                                                           key="winConfig")
        assert int(live_campaign_id) == redis_data['campaignId']
        redis_daily_budget = float(daily_budget_after_main_margin_update_db) - (
                float(daily_budget_after_main_margin_update_db) * decimal_updated_main_margin)
        assert round(redis_daily_budget, 4) == redis_data['budget']['currency']['daily']
        redis_total_budget = float(total_budget_from_approve) - (
                float(total_budget_from_approve) * decimal_updated_main_margin)
        assert round(redis_total_budget, 4) == redis_data['budget']['currency']['total']

        redis_data_from_campaign_rule = redis_page.establish_connection_and_get_campaign_rule(redis_connection,
                                                                                              live_campaign_id)
        calculated_bid = campaign_page.get_calculated_bid(bid_from_campaign_edit_in_usd, decimal_updated_main_margin)
        for creative_data in redis_data_from_campaign_rule.get(creative_type.lower(), []):
            if 'bid' in creative_data:
                bid_value = creative_data['bid']
                bid_from_redis = math.floor(bid_value * 100) / 100
                assert Decimal(calculated_bid).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) == Decimal(
                    bid_from_redis).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        print("[END] REDIS DATA VERIFICATION")

        print("[START] BUDGET RELATED METRICS VERIFICATION IN REPORT PAGE")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        updated_main_margin_report_data_admin_view_based_on_cost, \
            updated_main_margin_report_data_admin_view_based_on_revenue, \
            updated_main_margin_report_data_client_view_based_on_revenue, \
            updated_main_margin_report_data_client_view_based_on_cost = \
            report_page.generate_different_reports_and_get_data(campaign_name, live_campaign_id)

        report_page.verify_dicts(report_data_admin_view_based_on_cost,
                                 updated_main_margin_report_data_admin_view_based_on_cost)
        report_page.verify_dicts(report_data_admin_view_based_on_revenue,
                                 updated_main_margin_report_data_admin_view_based_on_revenue)
        report_page.verify_dicts(report_data_client_view_based_on_cost,
                                 updated_main_margin_report_data_client_view_based_on_cost)
        report_page.verify_dicts(report_data_client_view_based_on_revenue,
                                 updated_main_margin_report_data_client_view_based_on_revenue)

        report_page.select_dropdown_value(ReportPageLocators.spent_select_data_qa,
                                          "Spent based on revenue with margin")
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa)
        updated_main_margin_report_data_client_view_based_on_revenue_with_margin = \
            report_page.get_report_budget_related_metrics_data()
        report_page.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, "Admin view")
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa)
        updated_main_margin_report_data_admin_view_based_on_revenue_with_margin = \
            report_page.get_report_budget_related_metrics_data()

        calculated_metrics_dict = report_page.get_calculated_metrics(live_campaign_id, db_connection,
                                                                     decimal_updated_main_margin)
        report_page.verify_dicts(calculated_metrics_dict,
                                 updated_main_margin_report_data_client_view_based_on_revenue_with_margin)
        report_page.verify_dicts(calculated_metrics_dict,
                                 updated_main_margin_report_data_admin_view_based_on_revenue_with_margin)
        print("[END] BUDGET RELATED METRICS VERIFICATION IN REPORT PAGE")

        generic_modules.step_info(
            "[END - RTB-8848] Verify that user is able to change the main margin on approval page")


@pytest.mark.dependency()
def test_regression_edit_main_margin_from_client_management_page(login_by_user_type, open_database_connection):
    global live_campaign_id, campaign_name, creative_type, bid_from_campaign_edit, bid_from_campaign_edit_in_usd, \
        total_budget_from_campaign_edit, client_name, updated_main_margin, decimal_updated_main_margin, \
        total_remaining_budget, report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
        report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost, selected_budget, \
        total_budget_from_approve, daily_budget_from_approve_page
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    client_management_page = DashboardClientManagement(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    generic_modules.step_info(
        "[START - RTB-8853] Verify that user is able to change the main margin on client management page")

    if "qa-testing" in config['credential']['url']:
        print("[START] GET CAMPAIGN FROM DB")
        live_campaign_id = CampaignUtils.pull_specific_campaign_id_from_db(db_connection)
        user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
        payment_page.display_budget_information(user_id)
        print("[END] GET CAMPAIGN FROM DB")

        print("[START] GET SPENT FROM REDIS")
        amount_already_spent = redis_page.get_total_spent_amount(redis_connection, live_campaign_id)
        print("[END] GET SPENT FROM REDIS")

        print("[START] GET DATA FROM EDIT PAGE BEFORE EDITING MAIN MARGIN")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        campaign_name = campaign_page.get_text_using_tag_attribute(campaign_page.input_tag, campaign_page.id_attribute,
                                                                   CampaignFormLocators.campaign_field_id)
        creative_type = campaign_page.get_text_using_tag_attribute(campaign_page.span_tag, campaign_page.id_attribute,
                                                                   CampaignFormLocators.type_field_id)
        bid_from_campaign_edit = campaign_page.get_bid_cpm()
        bid_from_campaign_edit_in_usd = campaign_page.get_bid_in_usd()
        selected_budget = campaign_page.get_selected_budget()
        print("[END] GET DATA FROM EDIT PAGE BEFORE EDITING MAIN MARGIN")

        print("[START] GET DATA FROM APPROVAL PAGE AND SELECT REPORT OPTIONS")
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(live_campaign_id))
        driver.get(campaign_approve_url)
        client_name = campaign_approve_form.get_element_text(CampaignApproveLocators.client_name_data_qa)
        client_name = client_name.split("(", 1)[0].strip()
        campaign_approve_form.select_budget_related_metrics_to_see_it_in_report()
        # Calculation
        current_main_margin = float(campaign_approve_form.get_attribute_value(
            CampaignApproveLocators.main_margin_locator, "value"))
        total_budget_from_approve = campaign_approve_form.get_total_budget()
        daily_budget_from_approve_page = campaign_approve_form.get_daily_budget()
        max_allowed_main_margin = campaign_approve_form.get_calculated_max_allowed_main_margin(
            total_budget_from_approve, amount_already_spent)
        too_high_main_margin = campaign_approve_form.get_too_high_main_margin(max_allowed_main_margin)
        updated_main_margin = campaign_approve_form.get_updated_main_margin(current_main_margin,
                                                                            max_allowed_main_margin)
        decimal_updated_main_margin = updated_main_margin / 100
        total_remaining_budget = campaign_approve_form.get_total_remaining_budget(
            total_budget_from_approve, amount_already_spent, decimal_updated_main_margin)
        campaign_approve_form.click_approve_button()
        campaign_approve_form.accept_creative_size_pop_up()
        print("[END] GET DATA FROM APPROVAL PAGE AND SELECT REPORT OPTIONS")

        print("[START] GET DATA FROM REPORT PAGE BEFORE EDITING MAIN MARGIN")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
            report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost = \
            report_page.generate_different_reports_and_get_data(campaign_name, live_campaign_id)
        print("[END] GET DATA FROM REPORT PAGE BEFORE EDITING MAIN MARGIN")

        print("[START] EDIT MAIN MARGIN AND APPROVE IN CLIENT MANAGEMENT PAGE")
        navbar.impersonate_user('AutomationAdminUser')
        sidebar_page.navigate_to_page(PageNames.CLIENTS)
        campaign_name_with_id = campaign_name + " (" + str(live_campaign_id) + ")"

        generic_modules.step_info("[START - RTB-8855] Verify when the main margin % is too high and cannot be "
                                  "updated in client management page")
        client_management_page.provide_client_info_and_save(client_name, campaign_name_with_id,
                                                            float(too_high_main_margin))
        assert "The main margin cannot exceed {}%. Please increase the campaign’s total budget first.".format(
            max_allowed_main_margin) in client_management_page.get_element_text(
            ClientManagementLocator.error_message_locator)
        generic_modules.step_info("[END - RTB-8855] Verify when the main margin % is too high and cannot be "
                                  "updated in client management page")

        client_management_page.provide_client_info_and_save(client_name, campaign_name_with_id, updated_main_margin)
        time.sleep(1)
        assert True is client_management_page.is_element_displayed(
            ClientManagementLocator.main_margin_changes_modal_title_locator)
        total_remaining_budget_from_modal = client_management_page.get_element_text(
            ClientManagementLocator.modal_message_locator)
        assert str(total_remaining_budget) in total_remaining_budget_from_modal
        client_management_page.click_on_element(ClientManagementLocator.main_margin_changes_modal_confirm_btn_locator)
        assert "Margin saved successfully!" in client_management_page.get_element_text(
            ClientManagementLocator.success_message_data_qa)
        print("[END] EDIT MAIN MARGIN AND APPROVE IN CLIENT MANAGEMENT PAGE")


@pytest.mark.dependency(depends=['test_regression_edit_main_margin_from_client_management_page'])
def test_regression_edit_main_margin_from_client_management_page_two(login_by_user_type, open_database_connection):
    global live_campaign_id, campaign_name, creative_type, bid_from_campaign_edit, bid_from_campaign_edit_in_usd, \
        total_budget_from_campaign_edit, client_name, updated_main_margin, decimal_updated_main_margin, \
        total_remaining_budget, report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
        report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost, selected_budget, \
        total_budget_from_approve, daily_budget_from_approve_page
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    if "qa-testing" in config['credential']['url']:
        print("[START] TOTAL BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")
        campaign_list_page.reload_campaign_list_page()
        navbar.impersonate_user(client_name)
        campaign_list_page.select_all_status()
        campaign_list_page.search_and_action(campaign_name)
        today_spend = float(campaign_list_page.get_campaign_daily_spend(live_campaign_id))
        total_budget_from_campaign_list = campaign_list_page.get_campaign_total_budget(live_campaign_id)
        assert float(total_budget_from_approve) == float(total_budget_from_campaign_list)
        print("[END] TOTAL BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")

        print("[START] UPDATED MAIN MARGIN VERIFICATION IN DB")
        pulled_updated_main_margin_db = CampaignUtils.pull_campaign_main_margin_from_db(live_campaign_id, db_connection)
        assert updated_main_margin == int(pulled_updated_main_margin_db)
        print("[END] UPDATED MAIN MARGIN VERIFICATION IN DB")

        print("[START] METRICS RELATED TO BUDGET VERIFICATION IN EDIT PAGE")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
        bid_after_main_margin_update_from_ui = campaign_page.get_text_using_tag_attribute(
            campaign_page.input_tag, campaign_page.id_attribute, CampaignFormLocators.bid_cpm_field_id)
        daily_budget_after_main_margin_update_db = CampaignUtils.pull_campaign_daily_budget_from_db(
            live_campaign_id, db_connection)
        daily_remaining_budget = Decimal(daily_budget_after_main_margin_update_db - today_spend).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP)
        budget_after_main_margin_update = float(campaign_page.get_budget_amount())
        estimated_budget_from_ui = campaign_page.get_estimated_budget()
        if selected_budget == 'total':
            remaining_total_budget_from_ui = campaign_page.get_remaining_budget()
            daily_budget_after_main_margin_update = (float(remaining_total_budget_from_ui) + today_spend) / float(
                remaining_days)
            assert total_budget_from_approve == budget_after_main_margin_update
            assert float("{:.2f}".format(daily_budget_after_main_margin_update)) == float(estimated_budget_from_ui)
            assert float(remaining_total_budget_from_ui) == float(total_remaining_budget)
        else:
            assert float("{:.2f}".format(budget_after_main_margin_update)) == float(daily_budget_from_approve_page)
            remaining_daily_budget_from_ui = campaign_page.get_remaining_budget()
            assert float(remaining_daily_budget_from_ui) == float(daily_remaining_budget)
            assert total_budget_from_approve == float(estimated_budget_from_ui)
        assert bid_after_main_margin_update_from_ui == bid_from_campaign_edit
        print("[END] METRICS RELATED TO BUDGET VERIFICATION IN EDIT PAGE")

        print("[START] REDIS DATA VERIFICATION")
        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, live_campaign_id,
                                                                           key="winConfig")
        assert int(live_campaign_id) == redis_data['campaignId']
        redis_daily_budget = float(daily_budget_after_main_margin_update_db) - (
                float(daily_budget_after_main_margin_update_db) * decimal_updated_main_margin)
        assert round(redis_daily_budget, 4) == redis_data['budget']['currency']['daily']
        redis_total_budget = float(total_budget_from_approve) - (
                float(total_budget_from_approve) * decimal_updated_main_margin)
        assert round(redis_total_budget, 4) == redis_data['budget']['currency']['total']

        redis_data_from_campaign_rule = redis_page.establish_connection_and_get_campaign_rule(redis_connection,
                                                                                              live_campaign_id)
        calculated_bid = campaign_page.get_calculated_bid(bid_from_campaign_edit_in_usd, decimal_updated_main_margin)
        for creative_data in redis_data_from_campaign_rule.get(creative_type.lower(), []):
            if 'bid' in creative_data:
                bid_value = creative_data['bid']
                bid_from_redis = math.floor(bid_value * 100) / 100
                assert Decimal(calculated_bid).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) == Decimal(
                    bid_from_redis).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        print("[END] REDIS DATA VERIFICATION")

        print("[START] BUDGET RELATED METRICS VERIFICATION IN REPORT PAGE")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        updated_main_margin_report_data_admin_view_based_on_cost, \
            updated_main_margin_report_data_admin_view_based_on_revenue, \
            updated_main_margin_report_data_client_view_based_on_revenue, \
            updated_main_margin_report_data_client_view_based_on_cost = \
            report_page.generate_different_reports_and_get_data(campaign_name, live_campaign_id)

        report_page.verify_dicts(report_data_admin_view_based_on_cost,
                                 updated_main_margin_report_data_admin_view_based_on_cost)
        report_page.verify_dicts(report_data_admin_view_based_on_revenue,
                                 updated_main_margin_report_data_admin_view_based_on_revenue)
        report_page.verify_dicts(report_data_client_view_based_on_cost,
                                 updated_main_margin_report_data_client_view_based_on_cost)
        report_page.verify_dicts(report_data_client_view_based_on_revenue,
                                 updated_main_margin_report_data_client_view_based_on_revenue)

        report_page.select_dropdown_value(ReportPageLocators.spent_select_data_qa,
                                          "Spent based on revenue with margin")
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa)
        updated_main_margin_report_data_client_view_based_on_revenue_with_margin = \
            report_page.get_report_budget_related_metrics_data()
        report_page.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, "Admin view")
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa)
        updated_main_margin_report_data_admin_view_based_on_revenue_with_margin = \
            report_page.get_report_budget_related_metrics_data()

        calculated_metrics_dict = report_page.get_calculated_metrics(live_campaign_id, db_connection,
                                                                     decimal_updated_main_margin)
        report_page.verify_dicts(calculated_metrics_dict,
                                 updated_main_margin_report_data_client_view_based_on_revenue_with_margin)
        report_page.verify_dicts(calculated_metrics_dict,
                                 updated_main_margin_report_data_admin_view_based_on_revenue_with_margin)
        print("[END] BUDGET RELATED METRICS VERIFICATION IN REPORT PAGE")

        generic_modules.step_info(
            "[END - RTB-8853] Verify that user is able to change the main margin on client management page")


@pytest.mark.dependency()
def test_regression_edit_main_margin_from_mass_approve_page(login_by_user_type, open_database_connection):
    global live_campaign_id, campaign_name, creative_type, bid_from_campaign_edit, bid_from_campaign_edit_in_usd, \
        total_budget_from_campaign_edit, updated_main_margin, decimal_updated_main_margin, total_remaining_budget, \
        report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
        report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost, client_name, \
        selected_budget, total_budget_from_approve, daily_budget_from_approve_page
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_mass_approve_page = DspDashboardCampaignsMassApprove(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)

    print("[START] CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI")
    with open('assets/campaign/campaign_mass_approve_apply_all_data.json') as json_file:
        campaign_mass_approve_data = json.load(json_file)
    print("[END] CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI")

    print("[START - RTB-8851] Verify that user is able to change the main margin on mass-approval page")

    if "qa-testing" in config['credential']['url']:
        print("[START] GET CAMPAIGN FROM DB")
        live_campaign_ids = CampaignUtils.pull_few_live_campaign_ids_for_the_same_user_from_db(db_connection)
        live_campaign_id = live_campaign_ids[0]
        second_live_campaign_id = live_campaign_ids[1]
        user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
        payment_page.display_budget_information(user_id)
        print("[END] GET CAMPAIGN FROM DB")

        print("[START] GET SPENT FROM REDIS")
        amount_already_spent = redis_page.get_total_spent_amount(redis_connection, live_campaign_id)
        print("[END] GET SPENT FROM REDIS")

        print("[START] GET DATA FROM EDIT PAGE BEFORE EDITING MAIN MARGIN")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        campaign_name = campaign_page.get_text_using_tag_attribute(campaign_page.input_tag, campaign_page.id_attribute,
                                                                   CampaignFormLocators.campaign_field_id)
        creative_type = campaign_page.get_text_using_tag_attribute(campaign_page.span_tag, campaign_page.id_attribute,
                                                                   CampaignFormLocators.type_field_id)
        bid_from_campaign_edit = campaign_page.get_bid_cpm()
        bid_from_campaign_edit_in_usd = campaign_page.get_bid_in_usd()
        selected_budget = campaign_page.get_selected_budget()
        print("[END] GET DATA FROM EDIT PAGE BEFORE EDITING MAIN MARGIN")

        print("[START] GET DATA FROM APPROVAL PAGE AND SELECT REPORT OPTIONS")
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(live_campaign_id))
        driver.get(campaign_approve_url)
        client_name = campaign_approve_form.get_element_text(CampaignApproveLocators.client_name_data_qa)
        client_name = client_name.split("(", 1)[0].strip()
        campaign_approve_form.select_budget_related_metrics_to_see_it_in_report()
        # Calculation
        current_main_margin = float(campaign_approve_form.get_attribute_value(
            CampaignApproveLocators.main_margin_locator, "value"))
        total_budget_from_approve = campaign_approve_form.get_total_budget()
        daily_budget_from_approve_page = campaign_approve_form.get_daily_budget()
        max_allowed_main_margin = campaign_approve_form.get_calculated_max_allowed_main_margin(
            total_budget_from_approve, amount_already_spent)
        too_high_main_margin = campaign_approve_form.get_too_high_main_margin(max_allowed_main_margin)
        updated_main_margin = campaign_approve_form.get_updated_main_margin(current_main_margin,
                                                                            max_allowed_main_margin)
        decimal_updated_main_margin = updated_main_margin / 100
        total_remaining_budget = campaign_approve_form.get_total_remaining_budget(
            total_budget_from_approve, amount_already_spent, decimal_updated_main_margin)
        campaign_approve_form.click_approve_button()
        campaign_approve_form.accept_creative_size_pop_up()
        print("[END] GET DATA FROM APPROVAL PAGE AND SELECT REPORT OPTIONS")

        print("[START] GET DATA FROM REPORT PAGE BEFORE EDITING MAIN MARGIN")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
            report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost = \
            report_page.generate_different_reports_and_get_data(campaign_name, live_campaign_id)
        print("[END] GET DATA FROM REPORT PAGE BEFORE EDITING MAIN MARGIN")

        print("[START] EDIT MAIN MARGIN AND APPROVE IN MASS APPROVE PAGE")
        campaign_mass_approve_url = config['credential']['url'] + config['campaign-mass-approve-page'][
            'campaign-mass-approve-url'].format(str(live_campaign_id), second_live_campaign_id)
        driver.get(campaign_mass_approve_url)
        second_campaign_name = CampaignUtils.pull_campaign_name_from_db(second_live_campaign_id, db_connection)
        campaigns_name_list = [campaign_name, second_campaign_name]
        campaign_mass_approve_page.provide_campaign_mass_approve_advertiser_name(campaigns_name_list,
                                                                                 campaign_mass_approve_data)
        print(
            "[START - RTB-8852] Verify when the main margin % is too high and cannot be updated in mass-approval page")
        campaign_mass_approve_page.click_on_element(
            CampaignMassApproveFormLocators.ad_exchanges_xpath.format(live_campaign_id), locator_initialization=True)
        campaign_mass_approve_page.set_value_into_element(
            CampaignMassApproveFormLocators.main_margin_input_xpath.format(live_campaign_id), too_high_main_margin,
            locator_initialization=True)
        time.sleep(1)
        campaign_mass_approve_page.click_on_element(CampaignMassApproveFormLocators.ad_exchanges_ok_btn_xpath.
                                                    format(live_campaign_id), locator_initialization=True)
        campaign_mass_approve_page.click_on_element(CampaignMassApproveFormLocators.approve_button_locator)
        campaign_approve_form.click_on_element(
            CampaignMassApproveFormLocators.main_margin_changes_modal_confirm_btn_locator)
        campaign_mass_approve_page.wait_for_spinner_load()
        assert "The main margin cannot exceed {}%. Please increase the campaign’s total budget first.".format(
            max_allowed_main_margin) in campaign_mass_approve_page.get_element_text(
            CampaignMassApproveFormLocators.error_message_locator)
        assert False is campaign_mass_approve_page.is_element_present(
            CampaignMassApproveFormLocators.error_message_for_specific_campaign_xpath.format(
                second_live_campaign_id), locator_initialization=True)
        print("[END - RTB-8852] Verify when the main margin % is too high and cannot be updated in mass-approval page")
        campaign_mass_approve_page.provide_campaign_mass_approve_advertiser_name(campaigns_name_list,
                                                                                 campaign_mass_approve_data)
        campaign_mass_approve_page.click_on_element(
            CampaignMassApproveFormLocators.ad_exchanges_xpath.format(live_campaign_id), locator_initialization=True)
        campaign_mass_approve_page.set_value_into_element(
            CampaignMassApproveFormLocators.main_margin_input_xpath.format(live_campaign_id), updated_main_margin,
            locator_initialization=True)
        time.sleep(1)
        campaign_mass_approve_page.click_on_element(CampaignMassApproveFormLocators.ad_exchanges_ok_btn_xpath.
                                                    format(live_campaign_id), locator_initialization=True)
        campaign_mass_approve_page.click_on_element(CampaignMassApproveFormLocators.approve_button_locator)
        time.sleep(1)
        assert True is campaign_mass_approve_page.is_element_displayed(
            CampaignMassApproveFormLocators.main_margin_changes_modal_title_locator)
        assert "The total remaining budget will be recalculated for each campaign." in \
               campaign_mass_approve_page.get_element_text(
                   CampaignMassApproveFormLocators.main_margin_modal_message_locator)
        campaign_approve_form.click_on_element(
            CampaignMassApproveFormLocators.main_margin_changes_modal_confirm_btn_locator)
        assert "Successfully approved campaigns." in campaign_list_page.get_success_message()
        driver.get(campaign_mass_approve_url)
        first_campaign_advertiser_name = campaign_mass_approve_page.get_element_text(
            CampaignMassApproveFormLocators.advertiser_name_xpath.format(live_campaign_id), locator_initialization=True)
        second_campaign_advertiser_name = campaign_mass_approve_page.get_element_text(
            CampaignMassApproveFormLocators.advertiser_name_xpath.format(second_live_campaign_id),
            locator_initialization=True)
        assert campaign_mass_approve_data['main_settings']['advertiser_name'] == first_campaign_advertiser_name == \
               second_campaign_advertiser_name
        print("[END] EDIT MAIN MARGIN AND APPROVE IN MASS APPROVE PAGE")


@pytest.mark.dependency(depends=['test_regression_edit_main_margin_from_mass_approve_page'])
def test_regression_edit_main_margin_from_mass_approve_page_two(login_by_user_type, open_database_connection):
    global live_campaign_id, campaign_name, creative_type, bid_from_campaign_edit, bid_from_campaign_edit_in_usd, \
        total_budget_from_campaign_edit, updated_main_margin, decimal_updated_main_margin, total_remaining_budget, \
        report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
        report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost, client_name, \
        selected_budget, total_budget_from_approve, daily_budget_from_approve_page
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    if "qa-testing" in config['credential']['url']:
        print("[START] TOTAL BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")
        campaign_list_page.reload_campaign_list_page()
        navbar.impersonate_user(client_name)
        campaign_list_page.select_all_status()
        campaign_list_page.search_and_action(campaign_name)
        today_spend = float(campaign_list_page.get_campaign_daily_spend(live_campaign_id))
        total_budget_from_campaign_list = campaign_list_page.get_campaign_total_budget(live_campaign_id)
        assert float(total_budget_from_approve) == float(total_budget_from_campaign_list)
        print("[END] TOTAL BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")

        print("[START] UPDATED MAIN MARGIN VERIFICATION IN DB")
        pulled_updated_main_margin_db = CampaignUtils.pull_campaign_main_margin_from_db(live_campaign_id, db_connection)
        assert updated_main_margin == int(pulled_updated_main_margin_db)
        print("[END] UPDATED MAIN MARGIN VERIFICATION IN DB")

        print("[START] METRICS RELATED TO BUDGET VERIFICATION IN EDIT PAGE")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
        bid_after_main_margin_update_from_ui = campaign_page.get_text_using_tag_attribute(
            campaign_page.input_tag, campaign_page.id_attribute, CampaignFormLocators.bid_cpm_field_id)
        daily_budget_after_main_margin_update_db = CampaignUtils.pull_campaign_daily_budget_from_db(
            live_campaign_id, db_connection)
        daily_remaining_budget = Decimal(daily_budget_after_main_margin_update_db - today_spend).quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP)
        budget_after_main_margin_update = float(campaign_page.get_budget_amount())
        estimated_budget_from_ui = campaign_page.get_estimated_budget()
        if selected_budget == 'total':
            remaining_total_budget_from_ui = campaign_page.get_remaining_budget()
            daily_budget_after_main_margin_update = (float(remaining_total_budget_from_ui) + today_spend) / float(
                remaining_days)
            assert total_budget_from_approve == budget_after_main_margin_update
            assert float("{:.2f}".format(daily_budget_after_main_margin_update)) == float(estimated_budget_from_ui)
            assert float(remaining_total_budget_from_ui) == float(total_remaining_budget)
        else:
            assert float("{:.2f}".format(budget_after_main_margin_update)) == float(daily_budget_from_approve_page)
            remaining_daily_budget_from_ui = campaign_page.get_remaining_budget()
            assert float(remaining_daily_budget_from_ui) == float(daily_remaining_budget)
            assert total_budget_from_approve == float(estimated_budget_from_ui)
        assert bid_after_main_margin_update_from_ui == bid_from_campaign_edit
        print("[END] METRICS RELATED TO BUDGET VERIFICATION IN EDIT PAGE")

        print("[START] REDIS DATA VERIFICATION")
        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, live_campaign_id,
                                                                           key="winConfig")
        assert int(live_campaign_id) == redis_data['campaignId']
        redis_daily_budget = float(daily_budget_after_main_margin_update_db) - (
                float(daily_budget_after_main_margin_update_db) * decimal_updated_main_margin)
        assert round(redis_daily_budget, 4) == redis_data['budget']['currency']['daily']
        redis_total_budget = float(total_budget_from_approve) - (
                float(total_budget_from_approve) * decimal_updated_main_margin)
        assert round(redis_total_budget, 4) == redis_data['budget']['currency']['total']

        redis_data_from_campaign_rule = redis_page.establish_connection_and_get_campaign_rule(redis_connection,
                                                                                              live_campaign_id)
        calculated_bid = campaign_page.get_calculated_bid(bid_from_campaign_edit_in_usd, decimal_updated_main_margin)
        for creative_data in redis_data_from_campaign_rule.get(creative_type.lower(), []):
            if 'bid' in creative_data:
                bid_value = creative_data['bid']
                bid_from_redis = math.floor(bid_value * 100) / 100
                assert Decimal(calculated_bid).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) == Decimal(
                    bid_from_redis).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        print("[END] REDIS DATA VERIFICATION")

        print("[START] BUDGET RELATED METRICS VERIFICATION IN REPORT PAGE")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        updated_main_margin_report_data_admin_view_based_on_cost, \
            updated_main_margin_report_data_admin_view_based_on_revenue, \
            updated_main_margin_report_data_client_view_based_on_revenue, \
            updated_main_margin_report_data_client_view_based_on_cost = \
            report_page.generate_different_reports_and_get_data(campaign_name, live_campaign_id)

        report_page.verify_dicts(report_data_admin_view_based_on_cost,
                                 updated_main_margin_report_data_admin_view_based_on_cost)
        report_page.verify_dicts(report_data_admin_view_based_on_revenue,
                                 updated_main_margin_report_data_admin_view_based_on_revenue)
        report_page.verify_dicts(report_data_client_view_based_on_cost,
                                 updated_main_margin_report_data_client_view_based_on_cost)
        report_page.verify_dicts(report_data_client_view_based_on_revenue,
                                 updated_main_margin_report_data_client_view_based_on_revenue)

        report_page.select_dropdown_value(ReportPageLocators.spent_select_data_qa,
                                          "Spent based on revenue with margin")
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa)
        updated_main_margin_report_data_client_view_based_on_revenue_with_margin = \
            report_page.get_report_budget_related_metrics_data()
        report_page.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, "Admin view")
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa)
        updated_main_margin_report_data_admin_view_based_on_revenue_with_margin = \
            report_page.get_report_budget_related_metrics_data()

        calculated_metrics_dict = report_page.get_calculated_metrics(live_campaign_id, db_connection,
                                                                     decimal_updated_main_margin)
        report_page.verify_dicts(calculated_metrics_dict,
                                 updated_main_margin_report_data_client_view_based_on_revenue_with_margin)
        report_page.verify_dicts(calculated_metrics_dict,
                                 updated_main_margin_report_data_admin_view_based_on_revenue_with_margin)
        print("[END] BUDGET RELATED METRICS VERIFICATION IN REPORT PAGE")

    print("[END - RTB-8851] Verify that user is able to change the main margin on mass-approval page")
