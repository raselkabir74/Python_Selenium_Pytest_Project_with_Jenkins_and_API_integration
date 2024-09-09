import json

from configurations import generic_modules
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.campaigns import CampaignUtils as CampaignUtil
from locators.campaign.campaign_form_locator import CampaignFormLocators
from utils.redis import RedisUtils


def test_regression_add_campaign_ingame(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_approve_page = DspDashboardCampaignApprove(driver)
    redis_page = RedisUtils(config, driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/campaign/campaign_data_ingame.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    print("[START] GETTING EXPECTED REDIS DATA")
    with open('assets/campaign/redis_data/redis_data_for_ingame_campaign_creation.json') as json_file:
        redis_data_for_general_campaign_creation = json.load(json_file)
    print("[END] GETTING EXPECTED REDIS DATA")
    campaign_data['name_and_type']['campaign_type'] = "In-Game"
    campaign_data['platforms_telco_and_devices'][
        'ad_placement_type'] = "App"
    campaign_data['deals_and_packages']['ad_exchange_checkbox'] = \
        ['AdInMo (In-Game)', 'Adverty (In-Game)', 'Anzu (In-Game)',
         'Gadsme (In-Game)']

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

    # CAMPAIGN CREATION
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)
    campaign_page.provide_campaign_data_and_save_using_js(campaign_data, "Save",
                                                          ingame=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()

    # DATA VERIFICATION
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(
        campaign_data['name_and_type']['campaign_name'], 'Edit')
    pulled_campaign_data_gui = campaign_page.get_campaign_information_for_ingame_campaign(
        campaign_data, ingame=True)
    campaign_data['deals_and_packages']['packages'] = \
        ['Kids and Family-Oriented Games (Open Auction and PMP)',
         'Include only']
    print("Pulled data :",
          generic_modules.ordered(pulled_campaign_data_gui))
    print("Given data :", generic_modules.ordered(campaign_data))
    assert pulled_campaign_data_gui == campaign_data

    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8274] IN GAME CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name_and_type']['campaign_name'], db_connection)
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(campaign_id[0]['id']))
        driver.get(campaign_approve_url)
        campaign_approve_page.click_on_element(CampaignApproveLocators.ad_exchange_check_all_locator)
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
        print("[END] [RTB-8274] IN GAME CAMPAIGN APPROVE AND REDIS DATA VERIFICATION")

    # CAMPAIGN CLEAN UP
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(
        campaign_data['name_and_type']['campaign_name'], 'Delete')
    assert "Campaign deleted successfully" in campaign_view.get_success_message()


def test_regression_verify_checked_ad_exchanges(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    campaign_data['name_and_type']['campaign_type'] = "In-Game"

    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)
    campaign_page.provide_name_and_type_info(campaign_data, ingame=True)
    campaign_page.navigate_to_ad_exchanges_section()

    assert campaign_page.get_checkbox_status(CampaignFormLocators.ad_exchanges_adinmo_ingame_checkbox_label,
                                             without_text=True)
    assert campaign_page.get_checkbox_status(CampaignFormLocators.ad_exchanges_adverty_ingame_checkbox_label,
                                             without_text=True)
    assert campaign_page.get_checkbox_status(CampaignFormLocators.ad_exchanges_anzu_ingame_checkbox_label,
                                             without_text=True)
    assert campaign_page.get_checkbox_status(CampaignFormLocators.ad_exchanges_gadsme_ingame_checkbox_label,
                                             without_text=True)
