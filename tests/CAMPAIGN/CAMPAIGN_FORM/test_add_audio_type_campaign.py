import json

from configurations import generic_modules
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators


def test_dashboard_add_audio_type_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)

    print("[START] RTB-9368 Verify audio type campaign creation and approve")
    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_data_audio.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    campaign_data['name_and_type']['creative_type'] = "Audio"
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] CAMPAIGN CREATION")
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)
    campaign_page.provide_campaign_data_and_save(campaign_data, "Save", audio=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    print("[END] CAMPAIGN CREATION")

    print("[START] CAMPAIGN APPROVE")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'approve')
    campaign_approve_form.click_approve_button()
    campaign_approve_form.click_on_element(
        CampaignApproveLocators.ignore_button_locator)
    print("[END] CAMPAIGN APPROVE")

    print("[START] DATA VERIFICATION")
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'edit')
    pulled_campaign_data = campaign_page.get_campaign_information(campaign_data, audio=True)
    assert campaign_data == pulled_campaign_data
    print("[END] DATA VERIFICATION")
    print("[END] RTB-9368 Verify audio type campaign creation and approve")
