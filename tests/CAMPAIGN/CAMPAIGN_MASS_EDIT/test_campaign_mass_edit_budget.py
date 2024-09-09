import json

from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_edit_form import \
    DspDashboardCampaignsMassEdit
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.page_names_enum import PageNames
from locators.campaign.campaign_mass_edit_form_locator import CampaignMassEditFormLocator
from locators.campaign.campaign_list_locator import CampaignListLocators


def test_dashboard_edit_budget_in_mass_edit_page(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_data_daily_budget.json') as json_file:
        campaign_data = json.load(json_file)
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] DATA PREPARATION FOR MASS EDIT")
    with open('assets/campaign/campaign_mass_edit_data.json') as json_file:
        campaign_mass_edit_data = json.load(json_file)
    print("[END] DATA PREPARATION FOR MASS EDIT")

    print("[START] GETTING EXPECTED DB DATA")
    with open('assets/campaign/campaign_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    print("[END] GETTING EXPECTED DB DATA")

    print("[START] RTB-9006 Total & Daily Budget rework in Mass Campaign form")
    print("[START] CAMPAIGN CREATION")
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign-mass-edit-for-tracking'], operation="mass edit")
    for campaign_data['name_and_type']['campaign_name'] in campaign_name_list:
        campaign_settings_page.navigate_to_add_campaign_group()
        campaign_page.provide_campaign_data_and_save(campaign_data, "Save")
        assert "Saved successfully." in campaign_settings_page.get_success_message()
    print("[END] CAMPAIGN CREATION")

    print("[START] DATA VERIFICATION IN CAMPAIGNS LIST")
    campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name_and_type']['campaign_name'], db_connection)
    campaign_id = campaign_id[0]['id']
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGNS_LIST)
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    estimated_total_budget = float(campaign_data['launch_date_and_budget']['daily_budget']) * 6
    total_budget_before_edit = campaign_list_page.get_campaign_total_budget(campaign_id)
    daily_budget_before_edit = campaign_list_page.get_campaign_daily_budget(campaign_id)
    assert estimated_total_budget == float(total_budget_before_edit)
    assert campaign_data['launch_date_and_budget']['daily_budget'] == daily_budget_before_edit
    print("[END] DATA VERIFICATION IN CAMPAIGNS LIST")

    print("[START] CAMPAIGN MASS EDIT")
    campaign_list_page.search_and_action(config['campaign-mass-edit-for-tracking']['campaign-name-for-mass-edit-1'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_budget_apply_all_and_save(campaign_mass_edit_data)
    campaign_mass_edit_page.wait_for_element_to_be_clickable(CampaignMassEditFormLocator.save_button_locator)
    campaign_mass_edit_page.click_on_element(CampaignMassEditFormLocator.save_button_locator,
                                             locator_to_be_appeared=CampaignListLocators.success_message_locator)
    print("[END] CAMPAIGN MASS EDIT")

    print("[START] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")
    campaign_mass_edit_page.close_the_current_window_and_back_to_previous_window()
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGNS_LIST)
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    estimated_daily_budget = float(campaign_mass_edit_data['launch_date_and_budget']['total_budget']) / 6
    total_budget_after_edit = campaign_list_page.get_campaign_total_budget(campaign_id)
    daily_budget_after_edit = campaign_list_page.get_campaign_daily_budget(campaign_id)
    assert campaign_mass_edit_data['launch_date_and_budget']['total_budget'] == total_budget_after_edit
    assert estimated_daily_budget == float(daily_budget_after_edit)
    total_spend = campaign_list_page.get_campaign_total_spend(campaign_id)
    daily_spend = campaign_list_page.get_campaign_daily_spend(campaign_id)
    assert "0.00" == total_spend
    assert "0.00" == daily_spend
    print("[END] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")

    print("[START] DATA VERIFICATION IN EDIT PAGE AND DB")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id))
    driver.get(campaign_edit_url)
    pulled_campaign_data_gui = campaign_page.get_campaign_information(
        campaign_data)
    campaign_data['launch_date_and_budget']['daily_budget'] = '10.00'
    campaign_data['launch_date_and_budget']['total_budget'] = \
        campaign_mass_edit_data['launch_date_and_budget']['total_budget']
    campaign_data['launch_date_and_budget']['daily_budget_selected'] = ''
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        campaign_data['name_and_type']['campaign_name'], db_connection)
    expected_campaign_data_db['budget_daily_currency'] = float(campaign_data['launch_date_and_budget']['daily_budget'])
    expected_campaign_data_db['budget_total_currency'] = float(campaign_data['launch_date_and_budget']['total_budget'])
    assert campaign_data == pulled_campaign_data_gui
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] DATA VERIFICATION IN EDIT PAGE AND DB")
    print("[END] RTB-9006 Total & Daily Budget rework in Mass Campaign form")
