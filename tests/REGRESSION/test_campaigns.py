import json
import re
import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from configurations import generic_modules
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_list_locator import CampaignListLocators
from locators.campaign.campaign_mass_approve_form_locators import CampaignMassApproveFormLocators
from locators.campaign.campaign_mass_edit_form_locator import CampaignMassEditFormLocator
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from locators.all_campaigns.all_campaign_locators import AllCampaignFormLocators
from pages.base_page import BasePage
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.all_campaigns.all_campaigns_form import DashboardAllCampaignForm
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_approve_form import \
    DspDashboardCampaignsMassApprove
from pages.campaign.campaign_mass_duplicate_form import \
    DspDashboardCampaignsMassDuplicate
from pages.campaign.campaign_mass_edit_form import \
    DspDashboardCampaignsMassEdit
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.compare import CompareUtils as CompareUtil
from utils.io import IoUtils
from utils.redis import RedisUtils
from utils.page_names_enum import PageNames

created_campaign_url = []


def test_regression_add_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_approve_page = DspDashboardCampaignApprove(driver)
    redis_page = RedisUtils(config, driver)

    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] GETTING EXPECTED DB DATA")
    with open('assets/campaign/campaign_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    print("[END] GETTING EXPECTED DB DATA")

    print("[START] GETTING EXPECTED REDIS DATA")
    with open('assets/campaign/redis_data/redis_data_for_general_campaign_creation.json') as json_file:
        redis_data_for_general_campaign_creation = json.load(json_file)
    with open('assets/campaign/redis_data/redis_data_for_campaign_main_margin_disabled.json') as json_file:
        redis_data_for_campaign_main_margin_disabled = json.load(json_file)
    print("[END] GETTING EXPECTED REDIS DATA")

    print("[START] GET IMPRESSION FOR CTR FROM DB")
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)
    print("[END] GET IMPRESSION FOR CTR FROM DB")

    print("[START] GET IMPRESSION FOR SR FROM DB")
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)
    print("[END] GET IMPRESSION FOR SR FROM DB")

    print("CAMPAIGN CREATION")
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save(campaign_data, "Save")
    assert "Saved successfully." in campaign_settings_page.get_success_message()

    print("[START] DATA VERIFICATION")
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign_data['name_and_type']['campaign_name'],
        index=1)
    campaign_view.perform_action("Edit")
    assert '' == campaign_page.get_checkbox_status(CampaignFormLocators.ad_exchanges_traffic_junky_checkbox_label)
    assert '' == campaign_page.get_checkbox_status(CampaignFormLocators.ad_exchanges_traffic_stars_checkbox_label)
    pulled_campaign_data_gui = campaign_page.get_campaign_information(
        campaign_data)
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        campaign_data['name_and_type']['campaign_name'], db_connection)
    campaign_data['deals_and_packages']['packages'] = [
        'Kids and Family-Oriented Games (Open Auction and PMP)',
        'Include only']
    print("Pulled data :",
          generic_modules.ordered(pulled_campaign_data_gui))
    print("Given data :", generic_modules.ordered(campaign_data))
    print("Expected DB data :", expected_campaign_data_db)
    print("Pulled DB data :", pulled_campaign_data_db)
    assert campaign_data == pulled_campaign_data_gui
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] DATA VERIFICATION")

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8275] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name_and_type']['campaign_name'],
                                                            db_connection)
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(campaign_id[0]['id']))
        driver.get(campaign_approve_url)
        campaign_approve_page.check_uncheck_specific_checkbox(CampaignApproveLocators.Test_QA_margin_label, True,
                                                              without_text=True)
        campaign_approve_page.click_approve_button()
        campaign_approve_page.click_on_element(
            CampaignApproveLocators.creative_size_pop_up_ignore_locator)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == redis_data['id']
        assert campaign_data['name_and_type']['campaign_name'] == redis_data['name']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""
        redis_data['targeting']['dmp']['cities'] = []

        assert redis_data_for_general_campaign_creation == redis_data

        redis_data_for_budget = redis_page.establish_connection_and_get_campaign_rule(
            redis_connection, (campaign_id[0]['id']), key="winConfig")
        print(redis_data_for_budget)
        assert campaign_id[0]['id'] == redis_data_for_budget['campaignId']
        assert float(campaign_data['launch_date_and_budget']['total_budget']) == \
               redis_data_for_budget['budget']['currency']['total']
        redis_data_for_budget['campaignId'] = ""
        redis_data_for_budget['user']['targetDmpIds'] = []

        assert redis_data_for_campaign_main_margin_disabled == redis_data_for_budget
        print("[END] [RTB-8275] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

    print("[START] CAMPAIGN CLEAN UP")
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign_data['name_and_type']['campaign_name'],
        index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()
    print("[END] CAMPAIGN CLEAN UP")


def test_regression_duplicate_and_edit_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_approve_page = DspDashboardCampaignApprove(driver)
    redis_page = RedisUtils(config, driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    global created_campaign_url

    print("[START] DATA PREPARATION FOR DUPLICATE CAMPAIGN")
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)

    with open('assets/campaign/redis_data/redis_data_for_single_duplicate_campaign_creation.json') as json_file:
        redis_data_for_single_duplicate_campaign_creation = json.load(json_file)

    campaign_duplicate_data['name_and_type']['campaign_name'] = \
        campaign_duplicate_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(
            5)
    print("[END] DATA PREPARATION FOR DUPLICATE CAMPAIGN")

    print("[START] DUPLICATE EXISTING CAMPAIGN")
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        config['campaign'][
            'campaign-name-for-single-edit-and-duplicate'],
        index=1)
    campaign_view.perform_action("Duplicate")
    assert "1 campaigns were duplicated successfully." in campaign_settings_page.get_success_message()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + config['campaign']['campaign-name-for-single-edit-and-duplicate'],
                                         action='edit')
    campaign_page.provide_campaign_data_and_save_using_js(campaign_duplicate_data, "Save", duplicate_campaign=True)
    pulled_campaign_data_db = CampaignUtil.pull_campaign_id_from_db(
        campaign_duplicate_data['name_and_type']['campaign_name'], db_connection)
    created_campaign_url = campaign_settings_page.navigate_to_created_campaign(
        pulled_campaign_data_db, config)
    campaign_page.go_to_url(created_campaign_url[0])
    print("[END] DUPLICATE EXISTING CAMPAIGN")

    print("[START] GET IMPRESSION FOR CTR FROM DB")
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_duplicate_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)
    print("[END] GET IMPRESSION FOR CTR FROM DB")

    print("[START] GET IMPRESSION FOR SR FROM DB")
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_duplicate_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)
    print("[END] GET IMPRESSION FOR SR FROM DB")

    print("[START] DATA VERIFICATION")
    pulled_duplicate_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
        campaign_duplicate_data)
    campaign_duplicate_data['deals_and_packages']['packages'] = [
        'Kids and Family-Oriented Games (Open Auction and PMP)',
        'Include only']
    print("Pulled data :",
          generic_modules.ordered(pulled_duplicate_campaign_data_gui))
    print("Given data :", generic_modules.ordered(campaign_duplicate_data))
    assert campaign_duplicate_data == pulled_duplicate_campaign_data_gui
    print("[END] DATA VERIFICATION")

    print("[START] EDIT EXISTING CAMPAIGN")
    print("[START] DATA PREPARATION FOR EDIT CAMPAIGN")
    with open('assets/campaign/campaign_edit_data.json') as json_file:
        campaign_edit_data = json.load(json_file)
    campaign_edit_data['name_and_type']['campaign_name'] = \
        campaign_edit_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    print("[END] DATA PREPARATION FOR EDIT CAMPAIGN")

    print("[START] EDIT EXISTING CAMPAIGN")
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_page.go_to_url(created_campaign_url[0])
    campaign_page.provide_campaign_data_and_save_using_js(campaign_edit_data,
                                                          "Save",
                                                          edit_campaign=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    print("[END] EDIT EXISTING CAMPAIGN")

    print("[START] DATA VERIFICATION")
    campaign_page.go_to_url(created_campaign_url[0])
    pulled_edited_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
        campaign_edit_data)
    campaign_edit_data['deals_and_packages']['packages'] = [
        'Kids and Family-Oriented Games (Open Auction and PMP)',
        'Include only']
    print("Pulled data :",
          generic_modules.ordered(pulled_edited_campaign_data_gui))
    print("Given data :", generic_modules.ordered(campaign_edit_data))
    assert campaign_edit_data == pulled_edited_campaign_data_gui
    print("[END] DATA VERIFICATION")

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8276] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_edit_data['name_and_type']['campaign_name'],
                                                            db_connection)
        time.sleep(1)
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(campaign_id[0]['id']))

        campaign_page.go_to_url(created_campaign_url[0])
        campaign_page.click_on_element(
            CampaignFormLocators.time_and_day_scheduling_locator)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.specific_time_and_day_scheduling_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.specific_time_and_day_scheduling_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.specific_time_and_day_scheduling_for_tuesday_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.time_and_day_scheduling_save_button_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.publish_button_locator,
            locator_to_be_appeared=CampaignSettingsLocator.success_message_locator)

        driver.get(campaign_approve_url)
        campaign_approve_page.check_uncheck_specific_checkbox(CampaignApproveLocators.Test_QA_margin_label, True,
                                                              without_text=True)
        campaign_approve_page.click_approve_button()
        campaign_approve_page.click_on_element(
            CampaignApproveLocators.creative_size_pop_up_ignore_locator)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == redis_data['id']
        assert campaign_edit_data['name_and_type']['campaign_name'] == redis_data['name']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_single_duplicate_campaign_creation == redis_data
        print("[END] [RTB-8276] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

    print("[START] CAMPAIGN CLEAN UP")
    campaign_info = CampaignUtil.pull_campaign_id_from_db(campaign_edit_data['name_and_type']['campaign_name'],
                                                          db_connection)
    time.sleep(1)
    status = CampaignUtil.delete_campaign_by_api(config, campaign_info[0]['id'])
    assert True is status
    print("[END] CAMPAIGN CLEAN UP")
    print("[END] EDIT EXISTING CAMPAIGN")


def test_regression_campaign_approve(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    with open('assets/campaign/campaign_approve_data.json') as json_file:
        provided_campaign_approve_data = json.load(json_file)
    with open('assets/campaign/redis_data/redis_data_for_api_campaign_creation.json') as json_file:
        redis_data_for_api_campaign_creation = json.load(json_file)

    print("[START] CREATE CAMPAIGN BY API")
    campaign = CampaignUtil.create_campaign_by_api_with_current_date(config)
    campaign_settings_page.select_all_status()
    # APPROVE THE CAMPAIGN
    provided_campaign_approve_data = CampaignUtil.process_campaign_approve_data(
        provided_campaign_approve_data,
        single_approve=True)
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign['name'],
        index=1)
    campaign_view.perform_action("Approve")
    campaign_approve_form.approve_campaign(provided_campaign_approve_data)
    campaign_settings_page.move_to_campaign_settings_page()
    print("[END] CREATE CAMPAIGN BY API")

    print("[START] VERIFY THE DATA")
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign['name'],
        index=1)
    campaign_view.perform_action("Approve")
    assert "Pending" not in campaign_approve_form.get_campaign_status()
    pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_data(
        deal_margin=False)
    provided_campaign_approve_data['info'] = []
    provided_campaign_approve_data['main_settings'][
        'advertisement_category'] = ["IAB19 Technology & Computing"]
    print("Pulled data :",
          generic_modules.ordered(pulled_campaign_approve_data))
    print("Given data :",
          generic_modules.ordered(provided_campaign_approve_data))
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_campaign_approve_data,
        provided_campaign_approve_data)
    print("[END] VERIFY THE DATA")

    print("[START] [RTB-8414] Campaigns email reports grouped by IO")
    # VERIFY DATA WITH DB
    io_number = re.search(r'\d+', provided_campaign_approve_data["main_settings"]["io"]).group()
    email_report_settings_from_db = IoUtils.pull_email_reports_settings_from_db(io_number, db_connection)
    assert "campaign" == email_report_settings_from_db['view_by']
    assert '["xls","pdf"]' == email_report_settings_from_db['attachments']
    assert 3 == email_report_settings_from_db['frequency']
    assert 15 == email_report_settings_from_db['hour']
    assert 1 == email_report_settings_from_db['status']
    assert 6 == email_report_settings_from_db['weekday']
    print("[END] [RTB-8414] Campaigns email reports grouped by IO")

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8277] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign['name'], db_connection)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == redis_data['id']
        assert campaign['name'] == redis_data['name']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_api_campaign_creation == redis_data
        print("[END] [RTB-8277] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

    print("[START] CAMPAIGN CLEAN UP")
    first_campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign['name'], db_connection)
    status = CampaignUtil.delete_campaign_by_api(config, first_campaign_id[0]['id'])
    assert True is status
    print("[END] CAMPAIGN CLEAN UP")


def test_regression_campaign_mass_duplicate_and_edit(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    base_page = BasePage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    campaign_mass_approve_form = DspDashboardCampaignsMassApprove(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    # [START] MASS DUPLICATE EXISTING CAMPAIGNS
    # CAMPAIGN MASS DUPLICATE DATA TO PROVIDE IN GUI
    with open(
            'assets/campaign/campaign_mass_duplicate_data.json') as json_file:
        campaign_mass_duplicate_data = json.load(json_file)
    with open('assets/campaign/redis_data/redis_data_for_campaign_mass_duplicate_and_edit.json') as json_file:
        redis_data_for_campaign_mass_duplicate_and_edit = json.load(json_file)
    # MASS DUPLICATE EXISTING CAMPAIGNS
    campaign_name_list_before_mass_duplicate = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign'],
        operation="before mass duplicate "
                  "operation")
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign'],
        operation="mass duplicate and edit")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_list_table_length()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(
        config['campaign'][
            'campaign-name-prefix-for-mass-edit-and-duplicate'])
    for campaign_name in campaign_name_list_before_mass_duplicate:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Duplicate campaigns")
    assert "campaigns were duplicated successfully" in campaign_list_page.get_success_message()
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_mass_edit_data_and_save(campaign_name_list=campaign_name_list,
                                                                     duplicate_campaigns=True)
    assert "Changes saved successfully" in campaign_list_page.get_success_message()

    # GET IMPRESSION FOR CTR FROM DB
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_mass_duplicate_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)

    # GET IMPRESSION FOR SR FROM DB
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_mass_duplicate_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)

    # DATA VERIFICATION
    for campaign_name in campaign_name_list:
        campaign_mass_duplicate_data['name_and_type'][
            'campaign_name'] = campaign_name
        campaign_list_page.search_and_action(campaign_name, "Edit")
        pulled_mass_duplicate_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
            campaign_mass_duplicate_data)
        campaign_mass_duplicate_data['deals_and_packages'][
            'packages'] = [
            'Kids and Family-Oriented Games (Open Auction and PMP)',
            'Include only']
        print("Pulled duplicate data :",
              generic_modules.ordered(
                  pulled_mass_duplicate_campaign_data_gui))
        print("Given duplicate data :",
              generic_modules.ordered(campaign_mass_duplicate_data))
        assert campaign_mass_duplicate_data == pulled_mass_duplicate_campaign_data_gui
    base_page.close_the_current_window_and_back_to_previous_window()
    # [END] MASS DUPLICATE EXISTING CAMPAIGNS

    # [START] MASS EDIT EXISTING CAMPAIGNS
    # EDIT CAMPAIGN DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_mass_edit_data.json') as json_file:
        campaign_mass_edit_data = json.load(json_file)
    # EDIT EXISTING CAMPAIGNS
    campaign_name_list_to_edit = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign'],
        operation="mass duplicate and edit")
    campaign_list_page.search_and_action(
        config['campaign'][
            'campaign-name-prefix-after-mass-duplicate'],
        force_reload=True)
    for campaign_name in campaign_name_list:
        campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection)
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox_draft_campaigns(
            campaign_id=str(campaign_id[0]['id']),
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_mass_edit_data_and_save(
        campaign_name_list_to_edit,
        campaign_mass_edit_data=campaign_mass_edit_data)
    assert "Changes saved successfully" in campaign_list_page.get_success_message()

    # GET IMPRESSION FOR CTR FROM DB
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_mass_edit_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)

    # GET IMPRESSION FOR SR FROM DB
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_mass_edit_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)

    # DATA VERIFICATION
    for campaign_name in campaign_name_list_to_edit:
        campaign_mass_edit_data['name_and_type'][
            'campaign_name'] = campaign_name
        campaign_list_page.search_and_action(campaign_name, "Edit")
        pulled_mass_edit_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
            campaign_mass_edit_data)
        campaign_mass_edit_data['deals_and_packages']['packages'] = [
            'Kids and Family-Oriented Games (Open Auction and PMP)',
            'Include only']
        print("Pulled edit data :",
              generic_modules.ordered(
                  pulled_mass_edit_campaign_data_gui))
        print("Provided edit data :",
              generic_modules.ordered(campaign_mass_edit_data))
        assert pulled_mass_edit_campaign_data_gui == campaign_mass_edit_data

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8318] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        base_page.close_the_current_window_and_back_to_previous_window()
        campaign_list_page.select_item_from_campaign_multi_action_menu(
            "Publish campaigns", switch_to_new_window=False)
        assert "campaigns were published successfully." in campaign_list_page.get_success_message()
        for campaign_name in campaign_name_list_to_edit:
            campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection)
            campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox_draft_campaigns(
                campaign_id=str(campaign_id[0]['id']),
                check_the_checkbox=True)
        campaign_list_page.select_item_from_campaign_multi_action_menu(
            "Mass approve campaign", switch_to_new_window=True)
        campaign_mass_approve_form.click_on_element(
            CampaignMassApproveFormLocators.approve_button_locator)
        campaign_mass_approve_form.click_on_element(
            CampaignMassApproveFormLocators.ignor_button_locator)
        assert "Successfully approved campaigns." in campaign_list_page.get_success_message()

        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        for campaign_name in campaign_name_list_to_edit:
            campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection)
            redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
            assert campaign_id[0]['id'] == redis_data['id']
            assert campaign_name == redis_data['name']
            redis_data['id'] = ""
            redis_data['name'] = ""
            redis_data['contentCategories'] = []
            redis_data['user']['targetDmpIds'] = []
            redis_data['targeting']['endEpochSecond'] = ""
            redis_data['targeting']['startEpochSecond'] = ""

            assert redis_data_for_campaign_mass_duplicate_and_edit == redis_data
        print("[END] [RTB-8318] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

    # CAMPAIGN CLEAN UP
    base_page.close_the_current_window_and_back_to_previous_window()
    campaign_list_page.search_and_action(
        config['campaign'][
            'campaign-name-prefix-after-mass-duplicate'],
        force_reload=True)
    for campaign_name in campaign_name_list_to_edit:
        campaign_mass_edit_data['name_and_type'][
            'campaign_name'] = campaign_name
        campaign_list_page.search_and_action(campaign_name, "Delete")
        assert "Campaign deleted successfully" in campaign_list_page.get_success_message()
    # [END] MASS EDIT EXISTING CAMPAIGNS


def test_regression_campaign_mass_duplicate_and_edit_apply_all(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    base_page = BasePage(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_mass_duplicate_page = DspDashboardCampaignsMassDuplicate(
        driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    campaign_mass_approve_form = DspDashboardCampaignsMassApprove(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    # [START] MASS DUPLICATE EXISTING CAMPAIGNS
    # CAMPAIGN MASS DUPLICATE DATA TO PROVIDE IN GUI
    with open(
            'assets/regression_tests/campaign_mass_duplicate_apply_all.json') as json_file:
        campaign_mass_duplicate_data_apply_all = json.load(json_file)
    with open('assets/campaign/redis_data/redis_data_for_campaign_mass_duplicate_and_edit_apply_all.json') as json_file:
        redis_data_for_campaign_mass_duplicate_and_edit_apply_all = json.load(json_file)
    # MASS DUPLICATE EXISTING CAMPAIGNS
    campaign_name_list_before_mass_duplicate = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign'],
        operation="before mass duplicate "
                  "operation")
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign'],
        operation="mass duplicate and edit")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_list_table_length()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(
        config['campaign'][
            'campaign-name-prefix-for-mass-edit-and-duplicate'])
    for campaign_name in campaign_name_list_before_mass_duplicate:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Duplicate campaigns")
    assert "campaigns were duplicated successfully" in campaign_list_page.get_success_message()
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_mass_edit_data_apply_all_and_save(campaign_name_list=campaign_name_list,
                                                                               campaign_mass_edit_data=campaign_mass_duplicate_data_apply_all)
    assert "Changes saved successfully" in campaign_list_page.get_success_message()

    # GET IMPRESSION FOR CTR FROM DB
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_mass_duplicate_data_apply_all['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)

    # GET IMPRESSION FOR SR FROM DB
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_mass_duplicate_data_apply_all['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)

    # DATA VERIFICATION
    for campaign_name in campaign_name_list:
        campaign_mass_duplicate_data_apply_all['name_and_type'][
            'campaign_name'] = campaign_name
        campaign_list_page.search_and_action(campaign_name, "Edit")
        pulled_mass_duplicate_campaign_data_gui = campaign_mass_duplicate_page. \
            get_campaign_information_for_mass_duplicate_apply_all(campaign_mass_duplicate_data_apply_all)
        print("Pulled data :",
              generic_modules.ordered(
                  pulled_mass_duplicate_campaign_data_gui))
        print("Given data :",
              generic_modules.ordered(
                  campaign_mass_duplicate_data_apply_all))
        assert pulled_mass_duplicate_campaign_data_gui == campaign_mass_duplicate_data_apply_all
    base_page.close_the_current_window_and_back_to_previous_window()

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8319] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        campaign_list_page.select_item_from_campaign_multi_action_menu(
            "Publish campaigns", switch_to_new_window=False)
        assert "campaigns were published successfully." in campaign_list_page.get_success_message()
        for campaign_name in campaign_name_list:
            campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection)
            campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox_draft_campaigns(
                campaign_id=str(campaign_id[0]['id']),
                check_the_checkbox=True)
        campaign_list_page.select_item_from_campaign_multi_action_menu(
            "Mass approve campaign", switch_to_new_window=True)
        campaign_mass_approve_form.click_on_element(
            CampaignMassApproveFormLocators.approve_button_locator)
        campaign_mass_approve_form.click_on_element(
            CampaignMassApproveFormLocators.ignor_button_locator)
        assert "Successfully approved campaigns." in campaign_list_page.get_success_message()

        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        for campaign_name in campaign_name_list:
            campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection)
            redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
            assert campaign_id[0]['id'] == redis_data['id']
            assert campaign_name == redis_data['name']
            redis_data['id'] = ""
            redis_data['name'] = ""
            redis_data['contentCategories'] = []
            redis_data['user']['targetDmpIds'] = []
            redis_data['targeting']['endEpochSecond'] = ""
            redis_data['targeting']['startEpochSecond'] = ""

            assert redis_data_for_campaign_mass_duplicate_and_edit_apply_all == redis_data
            print("[END] [RTB-8319] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        base_page.close_the_current_window_and_back_to_previous_window()

    # CAMPAIGN CLEAN UP
    campaign_list_page.search_and_action(
        config['campaign'][
            'campaign-name-prefix-after-mass-duplicate'],
        force_reload=True)
    for campaign_name in campaign_name_list:
        campaign_list_page.search_and_action(campaign_name, "Delete")
        assert "Campaign deleted successfully" in campaign_list_page.get_success_message()
    campaign_settings_page.move_to_campaign_settings_page()
    # [END] MASS EDIT EXISTING CAMPAIGNS


def test_regression_campaign_mass_approve(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_mass_approve_page = DspDashboardCampaignsMassApprove(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_view = DspDashboardCampaignView(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    print("[START] CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI")
    with open(
            'assets/campaign/campaign_mass_approve_data.json') as json_file:
        campaign_mass_approve_data = json.load(json_file)
        private_deal_id = 12992
        deal_margin = 46

    with open('assets/campaign/redis_data/redis_data_for_mass_campaign_approve.json') as json_file:
        redis_data_for_mass_campaign_approve = json.load(json_file)
    print("[END] CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI")

    print("[START] DATA PREPARATION FOR CAMPAIGN PRIVATE MARKETPLACE AND CREATIVE SET")
    with open('assets/campaign/campaign_data.json') as json_file:
        provided_campaign_data = json.load(json_file)
    print("[END] DATA PREPARATION FOR CAMPAIGN PRIVATE MARKETPLACE AND CREATIVE SET")

    global created_campaign_url

    if "qa-testing" in config['credential']['url']:
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)

    print("[START] CREATE CAMPAIGN BY API")
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign-mass-approve'])
    for campaign_name in campaign_name_list:
        CampaignUtil.create_campaign_by_api_with_current_date(config,
                                                              mass_campaign_name=campaign_name)
        pulled_campaign_data_db = CampaignUtil.pull_campaign_id_from_db(
            campaign_name, db_connection)
        created_campaign_url = campaign_settings_page.navigate_to_created_campaign(
            pulled_campaign_data_db, config)
        campaign_page.go_to_url(created_campaign_url[0])

        # ADD PRIVATE MARKETPLACE AND CHANGE CREATIVE SET
        campaign_page.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.private_marketplace_label_locator,
            option_to_select="Private auction - Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile ($3.98)")
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
        campaign_settings_page.move_to_campaign_settings_page()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    print("[END] CREATE CAMPAIGN BY API")

    print("[START] CAMPAIGN MASS APPROVE")
    campaign_mass_approve_data = CampaignUtil.process_campaign_approve_data(
        campaign_mass_approve_data)
    campaign_list_page.search_and_action(config['campaign-mass-approve'][
                                             'campaign-name-prefix-for-mass-approve'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass approve campaign", switch_to_new_window=True)
    campaign_mass_approve_page.provide_campaign_mass_approve_data_and_save(
        campaign_name_list,
        campaign_mass_approve_data)
    assert "Successfully approved campaigns." in campaign_list_page.get_success_message()
    print("[END] CAMPAIGN MASS APPROVE")

    print("[START] VERIFY DATA")
    campaign_list_page.select_all_status()
    for campaign_name in campaign_name_list:
        campaign_list_page.search_and_action(campaign_name, "Approve")
        assert "Pending" not in campaign_approve_form.get_campaign_status()
        pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_data(
            mass_approve=True,
            deal_margin=True)
        pulled_campaign_approve_data['main_settings'][
            'advertisement_category'] = 'IAB19 Technology & Computing'
        print("Pulled data :",
              generic_modules.ordered(pulled_campaign_approve_data))
        print("Given data :",
              generic_modules.ordered(campaign_mass_approve_data))
        campaign_mass_approve_data['reporting_and_budget']['total_budget'] = 80.0
        assert pulled_campaign_approve_data == campaign_mass_approve_data
        campaign_list_page.reload_campaign_list_page()
    for campaign_name in campaign_name_list:
        pulled_deal_data_db = CampaignUtil.pull_deal_margin_value_from_db(
            campaign_name, db_connection)
        for deal_margin_data in pulled_deal_data_db:
            private_deal_id_from_db = \
                list(deal_margin_data.items())[0][1]
            assert private_deal_id_from_db == private_deal_id
            deal_margin_from_db = \
                list(deal_margin_data.items())[1][1]
            assert deal_margin_from_db == deal_margin
    print("[END] VERIFY DATA")

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8320] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        for campaign_name in campaign_name_list:
            campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection)
            redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
            assert campaign_id[0]['id'] == redis_data['id']
            assert campaign_name == redis_data['name']
            redis_data['id'] = ""
            redis_data['name'] = ""
            redis_data['contentCategories'] = []
            redis_data['user']['targetDmpIds'] = []
            redis_data['targeting']['endEpochSecond'] = ""
            redis_data['targeting']['startEpochSecond'] = ""
            assert redis_data_for_mass_campaign_approve == redis_data
        print("[END] [RTB-8320] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

    print("[START] CAMPAIGN CLEAN UP")
    campaign_list_page.search_and_action(config['campaign-mass-approve'][
                                             'campaign-name-prefix-for-mass-approve'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Delete")
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()
    print("[END] CAMPAIGN CLEAN UP")


def test_regression_campaign_settings(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    with open('assets/campaign/campaign_settings_data.json') as json_file:
        campaign_settings_data = json.load(json_file)
    campaign_settings_data['name'] = campaign_settings_data[
                                         'name'] + generic_modules.get_random_string(
        5)

    # CREATE CAMPAIGN BY API
    campaign = CampaignUtil.create_campaign_by_api(config)

    # UPDATE DATA IN CAMPAIGN SETTINGS PAGE
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.update_campaign_setting_data_single(
        campaign['campaignId'], campaign_settings_data)

    # VERIFY DATA
    pulled_campaign_data = campaign_settings_page.get_campaign_data(
        campaign['campaignId'])
    print("Pulled data :", generic_modules.ordered(pulled_campaign_data))
    print("Given data :", generic_modules.ordered(campaign_settings_data))
    assert pulled_campaign_data == campaign_settings_data

    # CAMPAIGN CLEAN UP
    status = CampaignUtil.delete_campaign_by_api(config, campaign['campaignId'])
    assert True is status


def test_regression_campaign_pmp_only(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    with open('assets/campaign/redis_data/redis_data_for_pmp_only_campaign_creation.json') as json_file:
        redis_data_for_api_campaign_creation = json.load(json_file)

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8244] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        api_campaign = CampaignUtil.create_campaign_by_api_with_current_date(config)
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        campaign_id = CampaignUtil.pull_campaign_id_from_db(api_campaign['name'], db_connection)
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(campaign_id[0]['id']))
        driver.get(campaign_edit_url)
        campaign_page.click_on_element(CampaignFormLocators.private_marketplace_section_locator)
        campaign_page.wait_for_element_to_be_clickable(CampaignFormLocators.private_marketplace_selection_locator)
        campaign_page.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.private_marketplace_label_locator,
            option_to_select=campaign_data['deals_and_packages']['private_marketplace'])
        campaign_page.click_on_element(CampaignFormLocators.private_marketplace_only_checkbox)
        campaign_page.scroll_to_specific_element(
            CampaignFormLocators.publish_button_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.publish_button_locator)
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.publish_button_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.publish_button_locator)
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(campaign_id[0]['id']))
        driver.get(campaign_approve_url)
        campaign_approve_form.click_on_element(CampaignApproveLocators.ad_exchange_check_all_locator)
        campaign_approve_form.click_approve_button()
        campaign_approve_form.click_on_element(
            CampaignApproveLocators.creative_size_pop_up_ignore_locator)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == redis_data['id']
        assert api_campaign['name'] == redis_data['name']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_api_campaign_creation == redis_data
        print("[END] [RTB-8244] CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

        print("[START] CAMPAIGN CLEAN UP")
        second_campaign_id = CampaignUtil.pull_campaign_id_from_db(api_campaign['name'], db_connection)
        status = CampaignUtil.delete_campaign_by_api(config, second_campaign_id[0]['id'])
        assert True is status
        print("[END] CAMPAIGN CLEAN UP")


def test_regression_publish_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    global created_campaign_url

    print("[START] RTB-8480 DATA PREPARATION FOR DUPLICATE CAMPAIGN")
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)
    print("[START] GETTING EXPECTED DB DATA")
    with open('assets/campaign/campaign_draft_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    print("[END] GETTING EXPECTED DB DATA")

    campaign_duplicate_data['name_and_type']['campaign_name'] = \
        campaign_duplicate_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(
            5)
    print("[END] DATA PREPARATION FOR DUPLICATE CAMPAIGN")

    print("[START] PUBLISH CAMPAIGN")
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        config['campaign'][
            'campaign-name-for-single-edit-and-duplicate'],
        index=1)
    campaign_view.perform_action("Duplicate")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + config['campaign']['campaign-name-for-single-edit-and-duplicate'],
                                         action='edit')
    campaign_page.provide_campaign_data_and_save_using_js(campaign_duplicate_data,
                                                          "draft",
                                                          duplicate_campaign=True)
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_duplicate_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Publish campaigns")
    assert "1 campaigns were published successfully." in campaign_list_page.get_success_message()
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        campaign_duplicate_data['name_and_type']['campaign_name'],
        db_connection)
    print("Expected DB data :", expected_campaign_data_db)
    print("Pulled DB data :", pulled_campaign_data_db)
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] PUBLISH CAMPAIGN")
    print("[START] CAMPAIGN CLEAN UP")
    campaign_info = CampaignUtil.pull_campaign_id_from_db(
        campaign_duplicate_data['name_and_type']['campaign_name'],
        db_connection)
    time.sleep(1)
    status = CampaignUtil.delete_campaign_by_api(config, campaign_info[0]['id'])
    assert True is status
    print("[END] RTB-8480 CAMPAIGN CLEAN UP")


def test_regression_new_duplicate_workflow_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    global created_campaign_url

    print("[START] RTB-8573 DATA PREPARATION FOR DUPLICATE CAMPAIGN")
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)
    print("[START] GETTING EXPECTED DB DATA")
    with open('assets/campaign/campaign_draft_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    print("[END] GETTING EXPECTED DB DATA")

    campaign_duplicate_data['name_and_type']['campaign_name'] = \
        campaign_duplicate_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(
            5)
    print("[END] DATA PREPARATION FOR DUPLICATE CAMPAIGN")

    print("[START] NEW MASS DUPLICATE CAMPAIGN")
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        config['campaign'][
            'campaign-name-for-single-edit-and-duplicate'],
        index=1)
    campaign_view.perform_action("Duplicate")
    assert "1 campaigns were duplicated successfully." in campaign_settings_page.get_success_message()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + config['campaign']['campaign-name-for-single-edit-and-duplicate'],
                                         action='edit')
    campaign_page.provide_campaign_data_and_save_using_js(campaign_duplicate_data,
                                                          "save",
                                                          duplicate_campaign=True)
    assert "Saved successfully. Click here to approve the campaign." in campaign_settings_page.get_success_message()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_duplicate_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Duplicate campaigns")
    print("VALIDATE PREFIX 'COPY OF' AND STATUS DRAFT")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    original_campaign_name = campaign_duplicate_data['name_and_type']['campaign_name']
    copied_campaign_name = "Copy of " + original_campaign_name

    campaign_list_page.search_and_action(copied_campaign_name)
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Publish campaigns")
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        copied_campaign_name,
        db_connection)
    print("Expected DB data :", expected_campaign_data_db)
    print("Pulled DB data :", pulled_campaign_data_db)
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] NEW MASS DUPLICATE CAMPAIGN")
    print("[START] CAMPAIGN CLEAN UP")
    campaign_info = CampaignUtil.pull_campaign_id_from_db(
        campaign_duplicate_data['name_and_type']['campaign_name'],
        db_connection)
    time.sleep(1)
    status = CampaignUtil.delete_campaign_by_api(config, campaign_info[0]['id'])
    assert True is status
    print("[END] RTB-8573 CAMPAIGN CLEAN UP")


def test_regression_draft_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)

    generic_modules.step_info("[START - RTB-8735] Verify draft campaigns after structural change")

    with open('assets/campaign/campaign_draft_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    with open('assets/campaign/campaign_mandatory_fields_only_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    expected_campaign_list_data = {}
    expected_all_campaigns_data = {}

    # DRAFT CAMPAIGN WITH MANDATORY FIELDS CREATION
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.select_dropdown_value(CampaignFormLocators.type_label,
                                        dropdown_item=campaign_data['name_and_type']['creative_type'])
    campaign_page.set_value_into_element(CampaignFormLocators.campaign_name_input_field_locator,
                                         campaign_data['name_and_type']['campaign_name'])
    time.sleep(10)
    campaign_page.click_save_cancel_or_draft("draft")
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(campaign_data['name_and_type']['campaign_name'],
                                                                 db_connection, status=14)
    print("Expected DB data :", expected_campaign_data_db)
    print("Pulled DB data :", pulled_campaign_data_db)
    assert expected_campaign_data_db == pulled_campaign_data_db

    # DATA VERIFICATION IN EDIT PAGE
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Edit')
    campaign_page.wait_for_visibility_of_element(CampaignFormLocators.creative_type_dropdown_locator)
    time.sleep(1)
    pulled_creative_type = campaign_page.get_text_using_tag_attribute(
        campaign_page.span_tag, campaign_page.id_attribute, CampaignFormLocators.type_field_id)
    pulled_campaign_name = campaign_page.get_text_using_tag_attribute(
        campaign_page.input_tag, campaign_page.id_attribute, CampaignFormLocators.campaign_field_id)
    assert campaign_data['name_and_type']['creative_type'] == pulled_creative_type
    assert campaign_data['name_and_type']['campaign_name'] == pulled_campaign_name

    # DATA VERIFICATION IN CAMPAIGN LIST PAGE
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name_and_type']['campaign_name'], db_connection)
    expected_campaign_list_data['campaign_id'] = str(campaign_id[0]['id'])
    expected_campaign_list_data['campaign_status'] = "Draft"
    expected_campaign_list_data['campaign_name'] = campaign_data['name_and_type']['campaign_name']
    expected_campaign_list_data['campaign_type'] = campaign_data['name_and_type']['campaign_type']
    expected_campaign_list_data['creative_type'] = campaign_data['name_and_type']['creative_type']
    pulled_campaign_list_data_gui = campaign_list_page.get_campaign_mandatory_information(campaign_id[0]['id'])
    assert expected_campaign_list_data == pulled_campaign_list_data_gui

    # DATA VERIFICATION IN CAMPAIGN MASS EDIT PAGE
    campaign_list_page.check_uncheck_specific_grid_row_checkbox_for_draft(
        CampaignListLocators.campaign_table_id, check_the_checkbox=True,
        column_value_to_identify_column=campaign_data['name_and_type']['campaign_name'], )
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    time.sleep(1)
    pulled_creative_type_from_mass_edit = campaign_mass_edit_page.get_element_text(
        CampaignMassEditFormLocator.creative_type_locator)
    pulled_campaign_type_from_mass_edit = campaign_mass_edit_page.get_element_text(
        CampaignMassEditFormLocator.campaign_type_locator)
    pulled_campaign_name_from_mass_edit = campaign_mass_edit_page.get_element_text(
        CampaignMassEditFormLocator.campaign_name_data_qa)
    assert campaign_data['name_and_type']['creative_type'] == pulled_creative_type_from_mass_edit
    assert campaign_data['name_and_type']['campaign_type'] == pulled_campaign_type_from_mass_edit
    assert campaign_data['name_and_type']['campaign_name'] == pulled_campaign_name_from_mass_edit
    campaign_mass_edit_page.close_the_current_window_and_back_to_previous_window()

    # DATA VERIFICATION IN ALL CAMPAIGNS PAGE
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.search_by_value(campaign_id[0]['id'])
    all_campaign_form.wait_for_spinner_load()
    pulled_creative_type_from_all_campaigns = all_campaign_form.get_attribute_value(
        AllCampaignFormLocators.table_row_creatives_type_xpath.format(campaign_id[0]['id']), "title",
        locator_initialization=True)
    pulled_campaign_type_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_campaign_type_xpath.format(campaign_id[0]['id']), locator_initialization=True)
    pulled_campaign_name_from_all_campaigns = all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_campaign_name_xpath.format(campaign_id[0]['id']), locator_initialization=True)
    assert campaign_data['name_and_type']['creative_type'] == pulled_creative_type_from_all_campaigns
    assert campaign_data['name_and_type']['campaign_type'] == pulled_campaign_type_from_all_campaigns
    assert campaign_data['name_and_type']['campaign_name'] == pulled_campaign_name_from_all_campaigns

    # DRAFT CAMPAIGN WITH ALL FIELDS CREATION
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    with open('assets/campaign/campaign_db_draft_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)

    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_using_js(campaign_data, "draft")
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(campaign_data['name_and_type']['campaign_name'],
                                                                 db_connection, status=14)
    print("Expected DB data :", expected_campaign_data_db)
    print("Pulled DB data :", pulled_campaign_data_db)
    assert expected_campaign_data_db == pulled_campaign_data_db

    # DATA VERIFICATION IN EDIT PAGE
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Edit')
    pulled_draft_campaign_data_gui = campaign_page.get_campaign_information(campaign_data)
    pulled_draft_campaign_data_gui['brand_safety']['brand_safety_keywords'] = "automation_brand_safety (17 keywords)"
    pulled_draft_campaign_data_gui['brand_safety']['contextual_keywords'] = "automation_brand_safety (17 keywords)"
    print("Pulled draft campaign data :", generic_modules.ordered(pulled_draft_campaign_data_gui))
    print("Given draft campaign data :", generic_modules.ordered(campaign_data))
    assert campaign_data == pulled_draft_campaign_data_gui

    # DATA VERIFICATION IN CAMPAIGN LIST PAGE
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name_and_type']['campaign_name'], db_connection)
    expected_campaign_list_data['campaign_id'] = str(campaign_id[0]['id'])
    expected_campaign_list_data['campaign_name'] = campaign_data['name_and_type']['campaign_name']
    expected_campaign_list_data['campaign_country'] = campaign_data['location_and_audiences']['country_name']
    expected_campaign_list_data['start_date'] = campaign_page.get_current_date_with_specific_format("%d %b, %Y")
    expected_campaign_list_data['end_date'] = campaign_page.get_specific_date_with_specific_format(
        "%d %b, %Y", days_to_add=6)
    expected_campaign_list_data['daily_budget'] = "{:.2f}".format(
        float(campaign_data['launch_date_and_budget']['daily_budget']))
    expected_campaign_list_data['total_budget'] = "{:.2f}".format(
        float(campaign_data['launch_date_and_budget']['total_budget']))
    pulled_campaign_list_data_gui = campaign_list_page.get_campaign_all_information(campaign_id[0]['id'])
    assert expected_campaign_list_data == pulled_campaign_list_data_gui

    # DATA VERIFICATION IN ALL CAMPAIGNS PAGE
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.search_by_value(campaign_id[0]['id'])
    all_campaign_form.wait_for_spinner_load()
    expected_all_campaigns_data['campaignId'] = str(campaign_id[0]['id'])
    expected_all_campaigns_data['name'] = campaign_data['name_and_type']['campaign_name']
    expected_all_campaigns_data['campaign_type'] = campaign_data['name_and_type']['campaign_type']
    expected_all_campaigns_data['creative_type'] = campaign_data['name_and_type']['creative_type']
    expected_all_campaigns_data['country'] = campaign_data['location_and_audiences']['country_name']
    expected_all_campaigns_data['status'] = 'Dra.'
    expected_all_campaigns_data['budget'] = {}
    expected_all_campaigns_data['budget']['daily'] = float(campaign_data['launch_date_and_budget']['daily_budget'])
    expected_all_campaigns_data['budget']['total'] = float(campaign_data['launch_date_and_budget']['total_budget'])
    pulled_campaign_data_gui = all_campaign_form.get_all_campaign_data_from_table(campaign_id[0]['id'])
    keys_to_delete = ['userId', 'bid', 'approved_by']
    for key in keys_to_delete:
        if key in pulled_campaign_data_gui:
            del pulled_campaign_data_gui[key]

    for key, value in pulled_campaign_data_gui.items():
        assert key in expected_all_campaigns_data and pulled_campaign_data_gui[key] == value, \
            f"Assertion failed for key: {key}"

    generic_modules.step_info("[END - RTB-8735] Verify draft campaigns after structural change")


def test_regression_impression_trackers_after_mass_edit(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    base_page = BasePage(driver)

    # CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_mass_edit_data_for_regression.json') as json_file:
        campaign_mass_edit_data = json.load(json_file)

    # CREATE CAMPAIGN BY API
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign-mass-edit-for-tracking'], operation="mass edit")
    for campaign_name in campaign_name_list:
        CampaignUtil.create_campaign_by_api(config,
                                            mass_campaign_name=campaign_name)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    # CAMPAIGN MASS APPROVE APPLY ALL
    campaign_list_page.search_and_action(config['campaign-mass-edit-for-tracking'][
                                             'campaign-name-prefix-for-mass-edit'])
    campaign_mass_edit_data['platforms_telco_and_devices']['mobile_operator'] = "Banglalink - Bangladesh"
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_mass_edit_data_and_save(
        campaign_name_list,
        campaign_mass_edit_data=campaign_mass_edit_data, mass_edit_only=False)
    campaign_mass_edit_data['landing_and_creatives']['creative'] = "Automation Banner Creative Eskimi"
    campaign_mass_edit_page.setting_value_into_creatives_column(
        CampaignMassEditFormLocator.campaign_mass_edit_form_id,
        campaign_mass_edit_data[
            'landing_and_creatives']['creative'], row_number="3")
    campaign_mass_edit_page.click_on_element(CampaignMassEditFormLocator.second_campaign_creative_locator)
    campaign_mass_edit_page.click_on_element(CampaignMassEditFormLocator.creative_toggle_icon_locator)
    time.sleep(campaign_mass_edit_page.ONE_SEC_DELAY)
    campaign_mass_edit_page.click_on_element(CampaignMassEditFormLocator.impression_per_creative_locator,
                                             locator_to_be_appeared=CampaignMassEditFormLocator.impression_add_more_button_locator)
    campaign_mass_edit_page.click_on_element(CampaignFormLocators.impression_add_more_button_locator,
                                             locator_to_be_appeared=CampaignMassEditFormLocator.pixel_input_locator)
    campaign_mass_edit_page.set_value_into_element(CampaignMassEditFormLocator.pixel_input_locator,
                                                   campaign_mass_edit_data['landing_and_creatives'][
                                                       "impression_tracking_pixel"])
    campaign_mass_edit_page.click_on_element(
        CampaignMassEditFormLocator.edit_campaign_creative_single_ok_button_locator)
    campaign_mass_edit_page.scroll_to_specific_element(
        CampaignMassEditFormLocator.save_button_locator)
    time.sleep(campaign_mass_edit_page.ONE_SEC_DELAY)
    campaign_mass_edit_page.wait_for_presence_of_element(
        CampaignMassEditFormLocator.save_button_locator)
    campaign_mass_edit_page.wait_for_element_to_be_clickable(
        CampaignMassEditFormLocator.save_button_locator)
    campaign_mass_edit_page.click_on_element(
        CampaignMassEditFormLocator.save_button_locator)
    assert "Changes saved successfully" in campaign_list_page.get_success_message()
    campaign_list_page.select_all_status()
    # DATA VERIFICATION

    campaign_name = campaign_name_list[0]
    campaign_mass_edit_data['name_and_type'][
        'campaign_name'] = campaign_name
    campaign_list_page.search_and_action(campaign_name, "Edit")
    pulled_mass_edit_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt_for_mass_edit(
        campaign_mass_edit_data)
    campaign_mass_edit_data['landing_and_creatives']['creative'] = "CampaignCreationSelenium"
    campaign_mass_edit_data['location_and_audiences'] = {}
    print("Pulled edit data :",
          generic_modules.ordered(
              pulled_mass_edit_campaign_data_gui))
    print("Provided edit data :",
          generic_modules.ordered(campaign_mass_edit_data))
    assert pulled_mass_edit_campaign_data_gui == campaign_mass_edit_data
    base_page.close_the_current_window_and_back_to_previous_window()

    campaign_name = campaign_name_list[1]
    campaign_mass_edit_data['name_and_type'][
        'campaign_name'] = campaign_name
    campaign_list_page.search_and_action(campaign_name, "Edit")
    pulled_mass_edit_campaign_data_gui = campaign_page.get_campaign_landing_and_creatives_only()
    campaign_mass_edit_data['brand_safety'] = {}
    campaign_mass_edit_data['name_and_type'] = {}
    campaign_mass_edit_data['campaign_purpose'] = {}
    campaign_mass_edit_data['launch_date_and_budget'] = {}
    campaign_mass_edit_data['platforms_telco_and_devices'] = {}
    campaign_mass_edit_data['landing_and_creatives']['creative'] = "Automation Banner Creative Eskimi"

    expected_data_without_pixel = campaign_mass_edit_data.copy()
    del expected_data_without_pixel['landing_and_creatives']['impression_tracking_pixel']
    print("Pulled edit data :",
          generic_modules.ordered(
              pulled_mass_edit_campaign_data_gui))
    print("Provided edit data :",
          generic_modules.ordered(expected_data_without_pixel))
    assert pulled_mass_edit_campaign_data_gui == expected_data_without_pixel
    # CAMPAIGN CLEAN UP
    campaign_list_page.search_and_action(config['campaign-mass-edit-for-tracking'][
                                             'campaign-name-prefix-for-mass-edit'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Delete")
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()


def test_regression_mass_edit(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)

    print("[START] RTB-8942 Verify campaign data on single/mass edit and approve pages")
    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
        campaign_data['name_and_type']['campaign_name'] = \
            campaign_data['name_and_type']['campaign_name'] + generic_modules.get_random_string(5)
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] DATA PREPARATION FOR MASS EDIT")
    with open('assets/campaign/campaign_mass_edit_and_verification_data.json') as json_file:
        campaign_mass_edit_data = json.load(json_file)
    print("[END] DATA PREPARATION FOR MASS EDIT")

    print("[START] GETTING EXPECTED DATA FROM EDIT")
    with open('assets/campaign/campaign_data_after_mass_edit.json') as json_file:
        expected_campaign_edit_data = json.load(json_file)
    print("[END] GETTING EXPECTED DATA FROM EDIT")

    print("[START] GETTING EXPECTED DATA FROM APPROVE")
    with open('assets/campaign/campaign_approve_all_data.json') as json_file:
        expected_campaign_approve_data = json.load(json_file)
    print("[END] GETTING EXPECTED DATA FROM APPROVE")

    print("[START] CAMPAIGN CREATION")
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_using_js(campaign_data, action='save')
    print("[END] CAMPAIGN CREATION")

    print("[START] CAMPAIGN MASS EDIT")
    campaign_name_list = [campaign_data['name_and_type']['campaign_name']]
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
        campaign_name=campaign_data['name_and_type']['campaign_name'],
        check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    mass_edit_url = driver.current_url
    campaign_mass_edit_page.provide_campaign_mass_edit_data_and_save(campaign_name_list,
                                                                     campaign_mass_edit_data=campaign_mass_edit_data)
    print("[END] CAMPAIGN MASS EDIT")

    print("[START] DATA VERIFICATION IN CAMPAIGN MASS EDIT PAGE")
    driver.get(mass_edit_url)
    pulled_campaign_mass_edit_data = campaign_mass_edit_page.get_campaign_information_for_mass_edit()
    campaign_mass_edit_data['name_and_type']['campaign_name'] = campaign_data['name_and_type']['campaign_name']
    pulled_campaign_mass_edit_data['launch_date_and_budget']['daily_budget_selected'] = ""
    assert campaign_mass_edit_data == pulled_campaign_mass_edit_data
    campaign_mass_edit_page.close_the_current_window_and_back_to_previous_window()
    print("[END] DATA VERIFICATION IN CAMPAIGN MASS EDIT PAGE")

    print("[START] DATA VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_list_page.search_and_action(
        campaign_data['name_and_type']['campaign_name'], 'Edit')
    pulled_campaign_edit_data = campaign_page.get_campaign_information(expected_campaign_edit_data)
    expected_campaign_edit_data['name_and_type']['campaign_name'] = campaign_data['name_and_type']['campaign_name']
    assert expected_campaign_edit_data == pulled_campaign_edit_data
    print("[END] DATA VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] DATA VERIFICATION IN CAMPAIGN APPROVE PAGE")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'approve')
    pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_all_data(mass_approve=True)
    expected_campaign_approve_data['info']['campaign_name'] = campaign_data['name_and_type']['campaign_name']
    assert expected_campaign_approve_data == pulled_campaign_approve_data
    print("[END] DATA VERIFICATION IN CAMPAIGN APPROVE PAGE")
    print("[END] RTB-8942 Verify campaign data on single/mass edit and approve pages")
