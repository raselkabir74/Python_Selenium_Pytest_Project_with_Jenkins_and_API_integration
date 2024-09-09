import json
import time
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from locators.campaign.campaign_mass_edit_form_locator import CampaignMassEditFormLocator
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.navbar.navbar import DashboardNavbar
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from configurations import generic_modules


def test_dashboard_campaign_list_new_duplicate_workflow_campaign(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)

    campaign_duplicate_data['name_and_type']['campaign_name'] = "AutomationNewDuplicateBannerCampaign"

    print("[START] NEW MASS DUPLICATE CAMPAIGN WITH DIFFERENT CAMPAIGNS TYPE")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_duplicate_data['name_and_type']['campaign_name'])
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Duplicate campaigns")
    campaign_list_page.select_all_status()
    original_campaign_name = campaign_duplicate_data['name_and_type']['campaign_name']
    copied_campaign_name = "Copy of " + original_campaign_name
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Publish campaigns")
    assert "campaigns were published successfully." in campaign_settings_page.get_success_message()
    print("[START] NEW MASS DUPLICATE CAMPAIGN WITH DIFFERENT CAMPAIGNS TYPE")
    campaign_list_page.filter_campaigns_by_status('Pending')
    campaign_list_page.search_and_action(copied_campaign_name)
    time.sleep(1)
    campaign_list_page.click_on_element(CampaignSettingsLocator.data_checkbox_all)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Delete")
    assert "Campaign deleted successfully" in campaign_settings_page.get_success_message()

def test_dashboard_campaign_new_duplicate_workflow_for_agency_user(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    navbar_page = DashboardNavbar(driver)
    with open('assets/campaign/campaign_duplicate_data_for_agency_user.json') as json_file:
        campaign_duplicate_data = json.load(json_file)
    campaign_duplicate_data['name_and_type']['campaign_name'] = \
        campaign_duplicate_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    
    generic_modules.step_info("[START - RTB-9338] Verify campaign duplication flow for agency account user")
    navbar_page.login_as("AutomationAgencyUser")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(config['campaign']['campaign-name-for-duplicate-for-agency-user'],
                                         action="Duplicate")
    assert "1 campaigns were duplicated successfully." in campaign_settings_page.get_success_message()
    campaign_list_page.select_item_from_campaign_multi_action_menu("Mass edit campaign",
                                                                   switch_to_new_window=True)
    campaign_list_page.set_value_into_specific_form_grid_input_field(
        CampaignMassEditFormLocator.campaign_mass_edit_form_id,
        CampaignMassEditFormLocator.name_column,
        campaign_duplicate_data['name_and_type']['campaign_name'])
    campaign_list_page.click_on_element(CampaignMassEditFormLocator.save_button_locator)
    campaign_list_page.close_the_current_window_and_back_to_previous_window()
    campaign_list_page.search_and_action(
        campaign_duplicate_data['name_and_type']['campaign_name'], 'Edit', force_reload=True)
    pulled_campaign_edit_data = campaign_page.get_campaign_information(campaign_duplicate_data)
    assert campaign_duplicate_data == pulled_campaign_edit_data
    generic_modules.step_info("[END - RTB-9338] Verify campaign duplication flow for agency account user")
