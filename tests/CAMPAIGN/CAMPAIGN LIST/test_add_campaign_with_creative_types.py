import json

from configurations import generic_modules
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.campaigns import CampaignUtils as CampaignUtil


def test_dashboard_campaign_list_add_campaign_with_creative_types(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_multiple_creatives_type.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)

    # GET IMPRESSION FOR CTR FROM DB
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)

    # GET IMPRESSION FOR SR FROM DB
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)

    creative_types = campaign_data['name_and_type']['creative_type']
    for creative_type in creative_types:
        campaign_data['name_and_type']['creative_type'] = creative_type
        campaign_data['name_and_type']['campaign_name'] = \
            campaign_data['name_and_type'][
                'campaign_name'] + generic_modules.get_random_string(
                5)
        # CAMPAIGN CREATION
        campaign_url = (config['credential']['url']
                        + config['campaign-creation-page']['campaign-creation-url'])
        driver.get(campaign_url)
        campaign_page.provide_name_and_type_info(campaign_data)
        campaign_page.provide_campaign_objective(campaign_data)
        campaign_page.provide_launch_date_and_budget_info(
            campaign_data)
        campaign_page.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.country_label,
            option_to_select=campaign_data['location_and_audiences'][
                'country_name'])
        campaign_page.provide_landing_and_creatives_info_using_js(campaign_data)
        campaign_page.click_save_cancel_or_draft("Save")
        assert "Saved successfully." in campaign_settings_page.get_success_message()

        # DATA VERIFICATION
        campaign_list_page.reload_campaign_list_page()
        campaign_list_page.select_all_status()
        campaign_list_page.search_and_action(
            campaign_data['name_and_type']['campaign_name'],
            'Edit')
        pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_creatives(
            campaign_data)
        print("Pulled data :",
              generic_modules.ordered(pulled_campaign_data_gui))
        print("Given data :", generic_modules.ordered(campaign_data))
        assert campaign_data == pulled_campaign_data_gui

        # CAMPAIGN CLEAN UP
        campaign_list_page.reload_campaign_list_page()
        campaign_list_page.select_all_status()
        campaign_list_page.search_and_action(
            campaign_data['name_and_type']['campaign_name'],
            'Delete')
        assert "Campaign deleted successfully" in campaign_view.get_success_message()
        campaign_settings_page.move_to_campaign_settings_page()
