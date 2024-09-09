import json

from configurations import generic_modules
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_list_locator import CampaignListLocators
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_edit_form import \
    DspDashboardCampaignsMassEdit
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.redis import RedisUtils
from utils.page_names_enum import PageNames


def test_regression_edit_budget_in_mass_edit_page(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] DATA PREPARATION FOR MASS EDIT")
    with open('assets/campaign/campaign_mass_edit_daily_budget_data.json') as json_file:
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
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    estimated_daily_budget = float(campaign_data['launch_date_and_budget']['total_budget']) / 6
    total_budget_before_edit = campaign_list_page.get_campaign_total_budget(campaign_id)
    daily_budget_before_edit = campaign_list_page.get_campaign_daily_budget(campaign_id)
    assert campaign_data['launch_date_and_budget']['total_budget'] == total_budget_before_edit
    assert estimated_daily_budget == float(daily_budget_before_edit)
    print("[END] DATA VERIFICATION IN CAMPAIGNS LIST")

    print("[START] CAMPAIGN MASS EDIT")
    campaign_list_page.search_and_action(config['campaign-mass-edit-for-tracking']['campaign-name-for-mass-edit-1'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_budget_and_save(campaign_name_list, campaign_mass_edit_data)
    print("[END] CAMPAIGN MASS EDIT")

    print("[START] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")
    campaign_mass_edit_page.close_the_current_window_and_back_to_previous_window()
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGNS_LIST)
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    estimated_total_budget = float(campaign_mass_edit_data['launch_date_and_budget']['daily_budget']) * 6
    total_budget_after_edit = campaign_list_page.get_campaign_total_budget(campaign_id)
    daily_budget_after_edit = campaign_list_page.get_campaign_daily_budget(campaign_id)
    assert campaign_mass_edit_data['launch_date_and_budget']['daily_budget'] == daily_budget_after_edit
    assert estimated_total_budget == float(total_budget_after_edit)
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
        campaign_mass_edit_data)
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        campaign_data['name_and_type']['campaign_name'], db_connection)
    campaign_data['launch_date_and_budget']['daily_budget'] = \
        campaign_mass_edit_data['launch_date_and_budget']['daily_budget']
    campaign_data['launch_date_and_budget']['total_budget'] = \
        campaign_mass_edit_data['launch_date_and_budget']['total_budget']
    campaign_data['launch_date_and_budget']['daily_budget_selected'] = \
        campaign_mass_edit_data['launch_date_and_budget']['daily_budget_selected']
    expected_campaign_data_db['budget_daily_currency'] = float(campaign_data['launch_date_and_budget']['daily_budget'])
    expected_campaign_data_db['budget_total_currency'] = float(campaign_data['launch_date_and_budget']['total_budget'])
    assert campaign_data == pulled_campaign_data_gui
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] DATA VERIFICATION IN EDIT PAGE AND DB")
    print("[END] RTB-9006 Total & Daily Budget rework in Mass Campaign form")


def test_regression_total_daily_budget_calculation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)

    print("[START] DATA PREPARATION FOR CAMPAIGN CREATION")
    with open('assets/campaign/campaign_mandatory_data.json') as json_file:
        campaign_data = json.load(json_file)
        campaign_data['name_and_type']['campaign_name'] = \
            campaign_data['name_and_type']['campaign_name'] + generic_modules.get_random_string(5)
    print("[END] DATA PREPARATION FOR CAMPAIGN CREATION")

    print("[START] GETTING EXPECTED DB DATA")
    with open('assets/campaign/campaign_mandatory_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    print("[END] GETTING EXPECTED DB DATA")

    print("[START] RTB-8955 Total & Daily Budget rework in Single Campaign form I")
    print("[START] CAMPAIGN CREATION")
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_mandatory_campaign_data_and_save(campaign_data)
    estimated_daily_budget = float(campaign_data['launch_date_and_budget']['total_budget']) / 6
    estimated_daily_budget_from_ui = campaign_page.get_estimated_budget()
    assert str(estimated_daily_budget) == estimated_daily_budget_from_ui
    campaign_page.click_save_cancel_or_draft("save")
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    print("[END] CAMPAIGN CREATION")

    print("[START] DATA VERIFICATION IN CAMPAIGNS LIST")
    campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name_and_type']['campaign_name'], db_connection)
    campaign_id = campaign_id[0]['id']
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    total_budget_before_edit = campaign_list_page.get_campaign_total_budget(campaign_id)
    daily_budget_before_edit = campaign_list_page.get_campaign_daily_budget(campaign_id)
    assert campaign_data['launch_date_and_budget']['total_budget'] == total_budget_before_edit
    assert str(estimated_daily_budget) == daily_budget_before_edit
    total_spend = campaign_list_page.get_campaign_total_spend(campaign_id)
    daily_spend = campaign_list_page.get_campaign_daily_spend(campaign_id)
    assert "0.00" == total_spend
    assert "0.00" == daily_spend
    print("[END] DATA VERIFICATION IN CAMPAIGNS LIST")

    print("[START] DATA VERIFICATION IN EDIT PAGE AND DB")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(campaign_id))
    driver.get(campaign_edit_url)
    pulled_campaign_data_gui = campaign_page.get_campaign_mandatory_information(campaign_data)
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        campaign_data['name_and_type']['campaign_name'], db_connection)
    assert campaign_data == pulled_campaign_data_gui
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] DATA VERIFICATION IN EDIT PAGE AND DB")

    print("[START] CAMPAIGN EDIT")
    campaign_page.click_on_element(CampaignFormLocators.daily_budget_radio_btn_data_qa)
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa, campaign_data[
        'launch_date_and_budget']['daily_budget'])
    estimated_total_budget = float(campaign_data['launch_date_and_budget']['daily_budget']) * 6
    estimated_total_budget_from_ui = campaign_page.get_estimated_budget()
    assert estimated_total_budget == float(estimated_total_budget_from_ui)
    campaign_page.click_save_cancel_or_draft("save")
    print("[END] CAMPAIGN EDIT")

    print("[START] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'])
    total_budget_after_edit = campaign_list_page.get_campaign_total_budget(campaign_id)
    daily_budget_after_edit = campaign_list_page.get_campaign_daily_budget(campaign_id)
    assert campaign_data['launch_date_and_budget']['daily_budget'] == daily_budget_after_edit
    assert estimated_total_budget == float(total_budget_after_edit)
    total_spend = campaign_list_page.get_campaign_total_spend(campaign_id)
    daily_spend = campaign_list_page.get_campaign_daily_spend(campaign_id)
    assert "0.00" == total_spend
    assert "0.00" == daily_spend
    print("[END] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")

    print("[START] DATA VERIFICATION IN APPROVE PAGE AND DB")
    campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
        'campaign-approve-url'].format(str(campaign_id))
    driver.get(campaign_approve_url)
    assert campaign_data['launch_date_and_budget']['daily_budget'] == campaign_approve_form.get_daily_budget()
    assert estimated_total_budget == campaign_approve_form.get_total_budget()
    assert daily_spend == campaign_approve_form.get_daily_spend()
    assert total_spend == campaign_approve_form.get_total_spend()
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(
        campaign_data['name_and_type']['campaign_name'], db_connection)
    assert expected_campaign_data_db == pulled_campaign_data_db
    print("[END] DATA VERIFICATION IN APPROVE PAGE AND DB")
    print("[END] RTB-8955 Total & Daily Budget rework in Single Campaign form I")


def test_regression_total_daily_budget_calculation_for_live_campaign(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    redis_page = RedisUtils(config, driver)

    if "qa-testing" in config['credential']['url']:
        print("[START] RTB-8955 Total & Daily Budget rework in Single Campaign form I")
        print("[START] GET CAMPAIGN FROM DB")
        live_campaign_id = CampaignUtils.pull_live_campaign_without_main_margin_id_from_db(db_connection)
        user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
        payment_page.display_budget_information(user_id)
        print("[END] GET CAMPAIGN FROM DB")

        print("[START] GET SPENT FROM REDIS")
        total_spent_from_redis = redis_page.get_total_spent_amount(redis_connection, live_campaign_id)
        daily_spent_from_redis = redis_page.get_today_spent_amount(redis_connection, live_campaign_id)
        print("[END] GET SPENT FROM REDIS")

        print("[START] EDIT CAMPAIGN")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(live_campaign_id))
        driver.get(campaign_edit_url)
        remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
        selected_budget_before = campaign_page.get_selected_budget()
        calculated_remaining_budget = campaign_page.get_total_daily_remaining_budget(
            selected_budget_before, daily_spent_from_redis, total_spent_from_redis)
        remaining_budget_from_ui = campaign_page.get_remaining_budget()
        assert calculated_remaining_budget == float(remaining_budget_from_ui)
        estimated_budget_before_switch = campaign_page.get_estimated_budget()
        campaign_page.switch_budget(selected_budget_before)
        selected_budget_after = campaign_page.get_selected_budget()
        calculated_estimated_budget_after_switch = campaign_page.get_total_daily_estimated_budget_for_live_campaign(
            selected_budget_after, estimated_budget_before_switch, total_spent_from_redis, daily_spent_from_redis,
            remaining_days)
        estimated_budget_after_switch_from_ui = campaign_page.get_estimated_budget()
        assert round(calculated_estimated_budget_after_switch, 2) == float(estimated_budget_after_switch_from_ui)
        calculated_remaining_budget_after_switch = campaign_page.get_total_daily_remaining_budget(
            selected_budget_after, daily_spent_from_redis, total_spent_from_redis)
        remaining_budget_after_switch_from_ui = campaign_page.get_remaining_budget()
        assert calculated_remaining_budget_after_switch == float(remaining_budget_after_switch_from_ui)
        campaign_page.click_save_cancel_or_draft("save")
        if campaign_page.is_element_present(CampaignFormLocators.credit_limit_exceeded_modal):
            campaign_page.click_on_element(CampaignFormLocators.campaign_goal_reset_no_locator)
        print("[END] EDIT CAMPAIGN")

        print("[START] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")
        sidebar_navigation.navigate_to_page(PageNames.CAMPAIGNS_LIST)
        campaign_list_page.select_all_status()
        campaign_list_page.search_and_action(live_campaign_id)
        total_budget_after_edit = campaign_list_page.get_campaign_total_budget(live_campaign_id)
        daily_budget_after_edit = campaign_list_page.get_campaign_daily_budget(live_campaign_id)
        total_budget = campaign_list_page.get_calculated_total_budget(live_campaign_id, remaining_days)
        daily_budget = campaign_list_page.get_calculated_daily_budget(live_campaign_id, remaining_days)
        assert total_budget == float(total_budget_after_edit) == \
               float(campaign_list_page.get_campaign_total_budget_from_total_line())
        assert daily_budget == float(daily_budget_after_edit) == \
               float(campaign_list_page.get_campaign_daily_budget_from_total_line())
        total_spend = campaign_list_page.get_campaign_total_spend(live_campaign_id)
        daily_spend = campaign_list_page.get_campaign_daily_spend(live_campaign_id)
        assert round(total_spent_from_redis, 2) == float(total_spend) == \
               float(campaign_list_page.get_campaign_total_spend_from_total_line())
        assert round(daily_spent_from_redis, 2) == float(daily_spend) == \
               float(campaign_list_page.get_campaign_today_spend_from_total_line())
        remaining_today_budget = campaign_list_page.get_campaign_remaining_today_budget(live_campaign_id)
        if selected_budget_after == 'total':
            remaining_total_budget = campaign_list_page.get_campaign_remaining_total_budget(live_campaign_id)
            assert remaining_total_budget == calculated_remaining_budget_after_switch
            assert remaining_today_budget == calculated_remaining_budget
            assert "est." in campaign_list_page.get_element_text(CampaignListLocators.remaining_today_data_qa.format(
                live_campaign_id))
            assert "est." in campaign_list_page.get_element_text(CampaignListLocators.daily_budget_data_qa.format(
                live_campaign_id))
        else:
            assert remaining_today_budget == calculated_remaining_budget_after_switch
            assert "est." in campaign_list_page.get_element_text(CampaignListLocators.total_budget_data_qa.format(
                live_campaign_id))
        print("[END] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")

        print("[START] DATA VERIFICATION IN CAMPAIGN SETTINGS AFTER EDIT")
        sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
        campaign_settings_page.search_campaign(live_campaign_id)
        total_budget_after_edit_from_settings = campaign_settings_page.get_total_budget(live_campaign_id)
        daily_budget_after_edit_from_settings = campaign_settings_page.get_daily_budget(live_campaign_id)
        assert total_budget == float(total_budget_after_edit_from_settings)
        assert daily_budget == float(daily_budget_after_edit_from_settings)
        total_spend_from_settings = campaign_settings_page.get_total_spend(live_campaign_id)
        daily_spend_from_settings = campaign_settings_page.get_today_spend(live_campaign_id)
        assert round(total_spent_from_redis, 2) == float(total_spend_from_settings)
        assert round(daily_spent_from_redis, 2) == float(daily_spend_from_settings)
        remaining_today_budget_from_settings = campaign_settings_page.get_daily_remaining_budget(live_campaign_id)
        if selected_budget_after == 'total':
            remaining_total_budget_from_settings = campaign_settings_page.get_total_remaining_budget(live_campaign_id)
            assert remaining_total_budget_from_settings == calculated_remaining_budget_after_switch
            assert remaining_today_budget_from_settings == calculated_remaining_budget
            assert "est." in campaign_settings_page.get_element_text(
                CampaignSettingsLocator.remaining_today_data_qa.format(live_campaign_id))
            assert "est." in campaign_settings_page.get_element_text(
                CampaignSettingsLocator.daily_budget_data_qa.format(live_campaign_id))
        else:
            assert remaining_today_budget_from_settings == calculated_remaining_budget_after_switch
            assert "est." in campaign_settings_page.get_element_text(
                CampaignSettingsLocator.total_budget_data_qa.format(live_campaign_id))
        print("[END] DATA VERIFICATION IN CAMPAIGN SETTINGS AFTER EDIT")
        print("[END] RTB-8955 Total & Daily Budget rework in Single Campaign form I")

        print("[START] RTB-8956 Total & Daily Budget rework in Single Campaign form II")
        driver.get(campaign_edit_url)
        campaign_page.click_on_element(CampaignFormLocators.total_budget_radio_btn_data_qa)
        new_total_budget = total_spent_from_redis - 1
        campaign_page.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa, new_total_budget)
        campaign_page.click_save_cancel_or_draft("save")
        if campaign_page.is_element_present(CampaignFormLocators.credit_limit_exceeded_modal):
            campaign_page.click_on_element(CampaignFormLocators.campaign_goal_reset_no_locator)
        assert "Total Budget must be at least {}".format(total_spend) == campaign_page.get_element_text(
            CampaignFormLocators.total_budget_warning_message_locator)
        print("[END] RTB-8956 Total & Daily Budget rework in Single Campaign form II")
