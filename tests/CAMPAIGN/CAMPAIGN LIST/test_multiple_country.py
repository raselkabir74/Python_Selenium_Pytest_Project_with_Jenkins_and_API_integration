import json
from configurations import generic_modules
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.campaigns import CampaignUtils as CampaignUtil


def test_dashboard_campaign_list_multiple_country_multiple_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_multiple_country_data.json') as json_file:
        campaign_multiple_country_data = json.load(json_file)
    campaign_name = campaign_multiple_country_data['name_and_type'][
                        'campaign_name'] + generic_modules.get_random_string(
        5)
    campaign_multiple_country_data['name_and_type'][
        'campaign_name'] = campaign_name

    # GET IMPRESSION FOR CTR FROM DB
    pulled_ctr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=2)
    for country_settings_data in pulled_ctr_data_from_country_settings_db:
        min_impression_ctr = list(country_settings_data.items())[0][1]
        campaign_multiple_country_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_ctr'] = \
            str(min_impression_ctr)

    # GET IMPRESSION FOR SR FROM DB
    pulled_sr_data_from_country_settings_db = CampaignUtil.pull_goal_data_from_db(
        db_connection, country_id=21, goal_type=10)
    for country_settings_data in pulled_sr_data_from_country_settings_db:
        min_impression_sr = list(country_settings_data.items())[0][1]
        campaign_multiple_country_data['campaign_goal_info'][
            'minimum_imp_per_placement_to_learn_sr'] = str(
            min_impression_sr)

    # CREATE MULTIPLE CAMPAIGNS WITH MULTIPLE COUNTRIES
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_for_multiple_platform_and_multiple_country(
        campaign_multiple_country_data, "Save", multi_country=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    pulled_campaign_data_db = CampaignUtil.pull_campaign_id_from_db(
        campaign_multiple_country_data['name_and_type'][
            'campaign_name'], db_connection)
    created_campaign_url = campaign_settings_page.navigate_to_created_campaign(
        pulled_campaign_data_db, config)

    # DATA VERIFICATION
    campaign_settings_page.select_all_status()
    multiple_country_name_data = [" - BD/Eskimi", " - AF/Eskimi"]
    for country_name_in_campaign in multiple_country_name_data:
        if country_name_in_campaign == " - BD/Eskimi":
            campaign_page.go_to_url(created_campaign_url[1])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_country(
                campaign_multiple_country_data)
            campaign_multiple_country_data['name_and_type'][
                'campaign_name'] = campaign_name + country_name_in_campaign
            campaign_multiple_country_data[
                'location_and_audiences'][
                'country_name'] = "Bangladesh"
            campaign_multiple_country_data[
                'location_and_audiences'][
                'city_name'] = "Dhaka - Bangladesh"
            campaign_multiple_country_data[
                'location_and_audiences'][
                'state_name'] = "Dhaka division - Bangladesh"
            campaign_multiple_country_data[
                'platforms_telco_and_devices'][
                'mobile_operator'] = "Robi - Bangladesh"
            campaign_multiple_country_data[
                'platforms_telco_and_devices'][
                'multiple_operation_sim_card'] = "Robi - Bangladesh"
            campaign_multiple_country_data[
                'platforms_telco_and_devices'][
                'operator_churn'] = "Robi - Bangladesh"
            campaign_multiple_country_data['deals_and_packages'][
                'packages'] = [
                'Kids and Family-Oriented Games (Open Auction and PMP)',
                'Include only']
            campaign_multiple_country_data['deals_and_packages'][
                'private_marketplace'] = 'Private auction - Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile ($3.98)'
            print("multiple country data",
                  generic_modules.ordered(
                      campaign_multiple_country_data))
            print("pulled data gui      ",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert generic_modules.ordered(
                pulled_campaign_data_gui) == generic_modules.ordered(
                campaign_multiple_country_data)

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_country_data['name_and_type']
                ['campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
        elif country_name_in_campaign == " - AF/Eskimi":
            campaign_page.go_to_url(created_campaign_url[0])
            pulled_campaign_data_gui = campaign_page.get_campaign_information_for_multiple_country(
                campaign_multiple_country_data)
            campaign_multiple_country_data['name_and_type'][
                'campaign_name'] = campaign_name + country_name_in_campaign
            campaign_multiple_country_data[
                'location_and_audiences'][
                'country_name'] = "Afghanistan"
            campaign_multiple_country_data[
                'location_and_audiences'][
                'city_name'] = "Kunduz - Afghanistan"
            campaign_multiple_country_data[
                'location_and_audiences'][
                'state_name'] = "Badakhshan - Afghanistan"
            campaign_multiple_country_data[
                'platforms_telco_and_devices'][
                'mobile_operator'] = "AWCC - Afghanistan"
            campaign_multiple_country_data[
                'platforms_telco_and_devices'][
                'multiple_operation_sim_card'] = "AWCC - Afghanistan"
            campaign_multiple_country_data[
                'platforms_telco_and_devices'][
                'operator_churn'] = "AWCC - Afghanistan"
            campaign_multiple_country_data['deals_and_packages'][
                'private_marketplace'] = 'Private auction - Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile ($3.98)'
            print("multiple country data",
                  generic_modules.ordered(
                      campaign_multiple_country_data))
            print("pulled data gui      ",
                  generic_modules.ordered(
                      pulled_campaign_data_gui))
            assert generic_modules.ordered(
                pulled_campaign_data_gui) == generic_modules.ordered(
                campaign_multiple_country_data)

            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(
                campaign_multiple_country_data['name_and_type']
                ['campaign_name'], index=1)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
