import json
from configurations import generic_modules
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.campaigns import CampaignUtils as CampaignUtil


def test_dashboard_campaign_list_multiple_platform_multiple_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_multiple_platform_data.json') as json_file:
        campaign_multiple_platform_data = json.load(json_file)
    campaign_name = campaign_multiple_platform_data['name_and_type'][
                        'campaign_name'] + generic_modules.get_random_string(
        5)
    campaign_multiple_platform_data['name_and_type'][
        'campaign_name'] = campaign_name

    # GET IMPRESSION FOR CTR FROM DB
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_multiple_platform_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = str(
            min_impression_ctr)

    # GET IMPRESSION FOR SR FROM DB
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_multiple_platform_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)

    # CREATE MULTIPLE CAMPAIGNS WITH MULTIPLE PLATFORMS
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_for_multiple_platform_and_multiple_country(
        campaign_multiple_platform_data, "Save",
        multi_platform=True, multi_country=False)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    pulled_campaign_data_db = CampaignUtil.pull_campaign_id_from_db(
        campaign_multiple_platform_data['name_and_type'][
            'campaign_name'], db_connection)
    created_campaign_url = campaign_settings_page.navigate_to_created_campaign(
        pulled_campaign_data_db, config)

    # DATA VERIFICATION
    campaign_settings_page.select_all_status()
    multiple_platform_name_data = [" - BD/Eskimi", " - BD/Facebook",
                                   " - BD/Youtube", " - BD/Adwords"]
    for platform_name_in_campaign in multiple_platform_name_data:
        if platform_name_in_campaign == " - BD/Eskimi":
            campaign_page.go_to_url(created_campaign_url[0])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_platforms(
                campaign_multiple_platform_data)
            campaign_multiple_platform_data['name_and_type'][
                'campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_multiple_platform_data['name_and_type'][
                'platform_type'] = "Eskimi"
            print("Given data :",
                  generic_modules.ordered(
                      campaign_multiple_platform_data))
            print("Pulled data :",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert pulled_campaign_data_gui == campaign_multiple_platform_data

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_platform_data[
                    'name_and_type'][
                    'campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
        elif platform_name_in_campaign == " - BD/Facebook":
            campaign_page.go_to_url(created_campaign_url[1])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_platforms(
                campaign_multiple_platform_data,
                goal_not_available=True)
            campaign_multiple_platform_data['name_and_type'][
                'campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_multiple_platform_data['name_and_type'][
                'platform_type'] = "Facebook"
            campaign_multiple_platform_data[
                'campaign_goal_info'] = {}
            print("Given data :",
                  generic_modules.ordered(
                      campaign_multiple_platform_data))
            print("Pulled data :",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert pulled_campaign_data_gui == campaign_multiple_platform_data

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_platform_data[
                    'name_and_type'][
                    'campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
        elif platform_name_in_campaign == " - BD/Youtube":
            campaign_page.go_to_url(created_campaign_url[2])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_platforms(
                campaign_multiple_platform_data,
                goal_not_available=True)
            campaign_multiple_platform_data['name_and_type'][
                'campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_multiple_platform_data['name_and_type'][
                'platform_type'] = "Youtube"
            campaign_multiple_platform_data[
                'campaign_goal_info'] = {}
            print("Given data :",
                  generic_modules.ordered(
                      campaign_multiple_platform_data))
            print("Pulled data :",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert pulled_campaign_data_gui == campaign_multiple_platform_data

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_platform_data[
                    'name_and_type'][
                    'campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
        elif platform_name_in_campaign == " - BD/Adwords":
            campaign_page.go_to_url(created_campaign_url[3])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_platforms(
                campaign_multiple_platform_data,
                goal_not_available=True)
            campaign_multiple_platform_data['name_and_type'][
                'campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_multiple_platform_data['name_and_type'][
                'platform_type'] = "Adwords"
            campaign_multiple_platform_data[
                'campaign_goal_info'] = {}
            print("Given data :",
                  generic_modules.ordered(
                      campaign_multiple_platform_data))
            print("Pulled data :",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert pulled_campaign_data_gui == campaign_multiple_platform_data

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_platform_data[
                    'name_and_type'][
                    'campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
        elif platform_name_in_campaign == " - BD/Tiktok":
            campaign_page.go_to_url(created_campaign_url[4])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_platforms(
                campaign_multiple_platform_data,
                goal_not_available=True)
            campaign_multiple_platform_data['name_and_type'][
                'campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_multiple_platform_data['name_and_type'][
                'platform_type'] = "Tiktok"
            campaign_multiple_platform_data[
                'campaign_goal_info'] = {}
            print("Given data :",
                  generic_modules.ordered(
                      campaign_multiple_platform_data))
            print("Pulled data :",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert pulled_campaign_data_gui == campaign_multiple_platform_data

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_platform_data[
                    'name_and_type']
                ['campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
