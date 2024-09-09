import copy
import json
import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from configurations import generic_modules
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from utils.campaigns import CampaignUtils as CampaignUtil


def test_dashboard_campaign_list_campaign_cancel_or_draft_functionality(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_cancel_or_draft.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data_copy = copy.deepcopy(campaign_data)
    campaign_data_copy['name_and_type']['campaign_name'] = \
        campaign_data_copy['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    campaign_data_copy['platforms_telco_and_devices'] = {}
    campaign_data_copy['deals_and_packages'] = {}
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(campaign_data_copy)
    campaign_page.provide_launch_date_and_budget_info(campaign_data_copy)
    campaign_page.click_on_element(
        CampaignFormLocators.button_group_locator)
    try:
        campaign_page.click_on_element(
            CampaignFormLocators.cancel_button_locator)
        WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                       'Timed out waiting for alert to appear')
        alert = driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("Alert not present")
    assert "Campaign settings" in campaign_settings_page.get_campaign_settings_link_text()
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(campaign_data_copy)
    campaign_page.provide_location_and_audiences_info_using_js(campaign_data_copy)
    campaign_page.click_save_cancel_or_draft("Draft")
    campaign_page.wait_for_visibility_of_element(
        CampaignSettingsLocator.success_message_locator)
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()

    # DRAFT STATUS VERIFICATION
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(
        campaign_data_copy['name_and_type']['campaign_name'], 'None')
    assert "Draft" in campaign_list_page.get_draft_status_text()
    campaign_list_page.search_and_action(
        campaign_data_copy['name_and_type']['campaign_name'], 'Edit')
    campaign_data_copy['campaign_goal_info']['campaign_goal'] = "1"
    campaign_page.click_on_element(CampaignFormLocators.campaign_goal.
    format(
        campaign_data_copy['campaign_goal_info']['campaign_goal']),
        locator_initialization=True)
    campaign_page.provide_launch_date_and_budget_info(campaign_data_copy)
    campaign_page.provide_landing_and_creatives_info(campaign_data_copy)
    campaign_page.click_save_cancel_or_draft("Save")
    campaign_page.click_on_element(CampaignFormLocators.confirm_button_alert_locator,
                                   locator_to_be_appeared=CampaignSettingsLocator.success_message_locator)

    # DATA VERIFICATION
    pulled_campaign_data_db = CampaignUtil.pull_campaign_id_from_db(
        campaign_data_copy['name_and_type']['campaign_name'], db_connection)
    created_campaign_url = campaign_settings_page.navigate_to_created_campaign(
        pulled_campaign_data_db, config)
    campaign_page.go_to_url(created_campaign_url[0])
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.campaign_goal_section_locator)
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.campaign_goal_section_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.campaign_goal_section_locator)
    assert "1" == campaign_page.get_text_using_tag_attribute(
        campaign_page.input_tag, campaign_page.id_attribute,
        CampaignFormLocators.campaign_goal_id)
    pulled_campaign_data_gui = campaign_page.get_campaign_information_for_draft_campaign(
        campaign_data_copy,
        goal_not_available=True)
    campaign_data_copy['campaign_goal_info'] = {}
    print("Pulled data :",
          generic_modules.ordered(pulled_campaign_data_gui))
    print("Given data :", generic_modules.ordered(campaign_data_copy))
    assert campaign_data_copy == pulled_campaign_data_gui

    # CLEAN UP
    campaign_list_page.search_and_action(
        campaign_data_copy['name_and_type']['campaign_name'], 'Delete')
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()


def test_dashboard_draft_campaign_without_budget(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)

    print("[START] RTB-8956 Total & Daily Budget rework in Single Campaign form II")
    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_draft_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    campaign_data['launch_date_and_budget']['total_budget'] = ""
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] DRAFT CAMPAIGN WITH MANDATORY FIELDS CREATION")
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_using_js(campaign_data, "draft")
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()
    print("[END] DRAFT CAMPAIGN WITH MANDATORY FIELDS CREATION")

    print("[START] MASS PUBLISH CAMPAIGN")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Publish campaigns")
    assert "Unable to publish any campaigns. Please try again." in campaign_list_page.get_danger_message()
    print("[END] MASS PUBLISH CAMPAIGN")

    print("[START] EDIT CAMPAIGN AND DUPLICATE")
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Edit')
    campaign_page.click_on_element(CampaignFormLocators.daily_budget_radio_btn_data_qa)
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa, campaign_data[
        'launch_date_and_budget']['daily_budget'])
    campaign_page.click_save_cancel_or_draft("Save")
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Duplicate')
    assert "1 campaigns were duplicated successfully." in campaign_list_page.get_success_message()
    print("[END] EDIT CAMPAIGN AND DUPLICATE")

    print("[START] VERIFY DUPLICATED CAMPAIGN DATA")
    copied_campaign_name = "Copy of " + campaign_data['name_and_type']['campaign_name']
    campaign_list_page.search_and_action(copied_campaign_name, action='edit')
    campaign_data['launch_date_and_budget']['daily_budget_selected'] = "True"
    campaign_data['launch_date_and_budget']['total_budget'] = "54.54"
    campaign_data['name_and_type']['campaign_name'] = copied_campaign_name
    pulled_campaign_data_gui = campaign_page.get_campaign_information(campaign_data)
    pulled_campaign_data_gui['brand_safety']['brand_safety_keywords'] = "automation_brand_safety (17 keywords)"
    pulled_campaign_data_gui['brand_safety']['contextual_keywords'] = "automation_brand_safety (17 keywords)"
    assert campaign_data == pulled_campaign_data_gui
    print("[END] VERIFY DUPLICATED CAMPAIGN DATA")
    print("[END] RTB-8956 Total & Daily Budget rework in Single Campaign form II")
