import json
import time
from configurations import generic_modules
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from locators.campaign.campaign_form_locator import CampaignFormLocators
from utils.campaigns import CampaignUtils as CampaignUtil


def test_mass_publish_campaign_draft_pending_partial_message(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    print("[START] RTB-8480 DATA PREPARATION FOR DUPLICATE CAMPAIGN")
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)

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
    assert "1 campaigns were duplicated successfully." in campaign_settings_page.get_success_message()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action("Copy of " + config['campaign']['campaign-name-for-single-edit-and-duplicate'],
                                         action='edit')
    campaign_page.provide_campaign_data_and_save_using_js(campaign_duplicate_data,
                                                          "save",
                                                          duplicate_campaign=True)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_duplicate_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Duplicate campaigns")
    campaign_list_page.search_and_action(campaign_duplicate_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Publish campaigns")
    assert "1 campaigns were published successfully." in campaign_list_page.get_success_message()
    print("[START] CAMPAIGN CLEAN UP")
    campaign_info = CampaignUtil.pull_campaign_id_from_db(campaign_duplicate_data['name_and_type']['campaign_name'],
                                                          db_connection)
    time.sleep(1)
    status = CampaignUtil.delete_campaign_by_api(config, campaign_info[0]['id'])
    assert True is status
    print("[END] RTB-8480 CAMPAIGN CLEAN UP")


def test_mass_publish_campaign_draft_partial_message(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_page = DspDashboardCampaignsForm(driver)

    print("[START] RTB-8480 DATA PREPARATION FOR DUPLICATE CAMPAIGN")
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)

    campaign_duplicate_data['name_and_type']['campaign_name'] = \
        campaign_duplicate_data['name_and_type'][
            'campaign_name'] + 'draft_' + generic_modules.get_random_string(
            5)
    print("[END] DATA PREPARATION FOR DUPLICATE CAMPAIGN")

    print("[START] PUBLISH CAMPAIGN")
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_using_js(campaign_duplicate_data, 'draft', draft_campaign = True)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(config['campaign'][
            'campaign-name-for-single-edit-and-duplicate-draft'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Duplicate campaigns")
    time.sleep(1)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action('Copy of ' + config['campaign'][
            'campaign-name-for-single-edit-and-duplicate-draft'], action='edit')
    campaign_page.provide_campaign_data_and_save_using_js(campaign_duplicate_data, 'draft', duplicate_campaign = True)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_duplicate_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Publish campaigns")
    assert "1 campaigns were successfully published," in campaign_list_page.get_warning_message()
    print("[START] CAMPAIGN CLEAN UP")
    campaign_info = CampaignUtil.pull_campaign_id_from_db(campaign_duplicate_data['name_and_type']['campaign_name'],
                                                          db_connection)
    time.sleep(1)
    for campaign in campaign_info:
        CampaignUtil.delete_campaign_by_api(config, campaign['id'])
    print("[END] RTB-8480 CAMPAIGN CLEAN UP")
