import json

from configurations import generic_modules
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_approve_form import \
    DspDashboardCampaignsMassApprove
from utils.campaigns import CampaignUtils as CampaignUtil


def test_dashboard_campaign_approve_campaign_mass_approve_apply_all(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_mass_approve_page = DspDashboardCampaignsMassApprove(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)

    # CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_mass_approve_apply_all_data.json') as json_file:
        campaign_mass_approve_data = json.load(json_file)

    # CREATE CAMPAIGN BY API
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign-mass-approve'])
    for campaign_name in campaign_name_list:
        CampaignUtil.create_campaign_by_api(config,
                                            mass_campaign_name=campaign_name)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    # CAMPAIGN MASS APPROVE APPLY ALL
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
    campaign_mass_approve_page.provide_campaign_mass_approve_data_and_save_apply_all(
        campaign_mass_approve_data)
    assert "Successfully approved campaigns." in campaign_list_page.get_success_message()
    # VERIFY DATA
    campaign_list_page.select_all_status()
    for campaign_name in campaign_name_list:
        campaign_list_page.search_and_action(campaign_name, "Approve")
        assert "Pending" not in campaign_approve_form.get_campaign_status()
        pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_data(
            mass_approve=True)
        campaign_mass_approve_data['main_settings'][
            'advertiser_name'] = ''
        campaign_mass_approve_data['info'] = {}
        campaign_mass_approve_data['main_settings'][
            'advertisement_category'] = [
            'IAB19 Technology & Computing']
        print("Pulled data :",
              generic_modules.ordered(pulled_campaign_approve_data))
        print("Given data :",
              generic_modules.ordered(campaign_mass_approve_data))
        assert pulled_campaign_approve_data == campaign_mass_approve_data
        campaign_list_page.reload_campaign_list_page()

    # CAMPAIGN CLEAN UP
    campaign_list_page.search_and_action(config['campaign-mass-approve'][
                                             'campaign-name-prefix-for-mass-approve'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Delete")
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()
