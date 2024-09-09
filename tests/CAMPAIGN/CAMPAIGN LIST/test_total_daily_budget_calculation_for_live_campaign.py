from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.sidebar.sidebar import DashboardSidebarPage, PageNames
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from utils.campaigns import CampaignUtils


def test_dashboard_total_daily_budget_calculation_for_live_campaign_with_main_margin(login_by_user_type,
                                                                                     open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    print("[START] RTB-9371 Estimated budget recalculation after the budget type switch")
    print("[START] GET CAMPAIGN FROM DB")
    live_campaign_id = CampaignUtils.pull_specific_campaign_id_from_db(db_connection)
    user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
    payment_page.display_budget_information(user_id)
    print("[END] GET CAMPAIGN FROM DB")

    print("[START] GET SPENT FROM CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(live_campaign_id)
    total_spend = float(campaign_settings_page.get_total_spend(live_campaign_id))
    daily_spend = float(campaign_settings_page.get_today_spend(live_campaign_id))
    print("[END] GET SPENT FROM CAMPAIGN SETTINGS PAGE")

    print("[START] EDIT CAMPAIGN")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
    selected_budget_before = campaign_page.get_selected_budget()
    estimated_budget_before_switch = campaign_page.get_estimated_budget()
    campaign_page.switch_budget(selected_budget_before)
    selected_budget_after = campaign_page.get_selected_budget()
    calculated_estimated_budget_after_switch = campaign_page.get_total_daily_estimated_budget_for_live_campaign(
        selected_budget_after, estimated_budget_before_switch, total_spend, daily_spend,
        remaining_days)
    estimated_budget_after_switch_from_ui = campaign_page.get_estimated_budget()
    assert round(calculated_estimated_budget_after_switch, 2) == float(estimated_budget_after_switch_from_ui)
    campaign_page.click_save_cancel_or_draft("save")
    if campaign_page.is_element_present(CampaignFormLocators.credit_limit_exceeded_modal):
        campaign_page.click_on_element(CampaignFormLocators.campaign_goal_reset_no_locator)
    print("[END] EDIT CAMPAIGN")

    print("[START] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(live_campaign_id)
    total_budget_after_edit = campaign_list_page.get_campaign_total_budget(live_campaign_id)
    daily_budget_after_edit = campaign_list_page.get_campaign_daily_budget(live_campaign_id)
    if selected_budget_after == 'total':
        assert round(calculated_estimated_budget_after_switch, 2) == float(daily_budget_after_edit)
        assert float(estimated_budget_before_switch) == float(total_budget_after_edit)
    else:
        assert round(calculated_estimated_budget_after_switch, 2) == float(total_budget_after_edit)
        assert float(estimated_budget_before_switch) == float(daily_budget_after_edit)
    print("[END] DATA VERIFICATION IN CAMPAIGNS LIST AFTER EDIT")

    print("[START] ESTIMATED AMOUNT VERIFICATION IN EDIT PAGE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    estimated_budget_from_ui = campaign_page.get_estimated_budget()
    assert round(calculated_estimated_budget_after_switch, 2) == float(estimated_budget_from_ui)
    print("[END] ESTIMATED AMOUNT VERIFICATION IN EDIT PAGE")
    print("[END] RTB-9371 Estimated budget recalculation after the budget type switch")


def test_dashboard_total_daily_budget_calculation_for_live_campaign_with_end_day_today(login_by_user_type,
                                                                                       open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    print("[START] RTB-9462 Estimated budget calculation for last day campaign")
    print("[START] GET CAMPAIGN FROM DB")
    live_campaign_id = CampaignUtils.pull_live_campaign_with_end_day_today_tomorrow_id_from_db(db_connection)
    user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
    payment_page.display_budget_information(user_id)
    print("[END] GET CAMPAIGN FROM DB")

    print("[START] GET SPENT FROM CAMPAIGN SETTINGS PAGE")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(live_campaign_id)
    total_spend = float(campaign_settings_page.get_total_spend(live_campaign_id))
    daily_spend = float(campaign_settings_page.get_today_spend(live_campaign_id))
    print("[END] GET SPENT FROM CAMPAIGN SETTINGS PAGE")

    print("[START] ESTIMATED TOTAL/DAILY BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")
    campaign_list_page.run_recalculate_daily_cron_job(live_campaign_id)
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
    budget_amount = campaign_page.get_budget_amount()
    selected_budget_type = campaign_page.get_selected_budget()
    calculated_estimated_budget = campaign_page.get_total_daily_estimated_budget_for_live_campaign(
        selected_budget_type, budget_amount, total_spend, daily_spend, remaining_days, set_value=False)
    estimated_budget_before_switch = campaign_page.get_estimated_budget()
    assert round(calculated_estimated_budget, 2) == float(estimated_budget_before_switch)
    print("[END] ESTIMATED TOTAL/DAILY BUDGET VERIFICATION IN CAMPAIGN EDIT PAGE")

    print("[START] ESTIMATED TOTAL/DAILY BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(live_campaign_id)
    if selected_budget_type == 'total':
        assert round(calculated_estimated_budget, 2) == float(campaign_list_page.get_campaign_daily_budget(
            live_campaign_id))
    else:
        assert round(calculated_estimated_budget, 2) == float(campaign_list_page.get_campaign_total_budget(
            live_campaign_id))
    print("[END] ESTIMATED TOTAL/DAILY BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")

    print("[START] CHANGE BUDGET TYPE")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    campaign_page.switch_budget(selected_budget_type)
    selected_budget_after = campaign_page.get_selected_budget()
    calculated_estimated_budget_after_switch = campaign_page.get_total_daily_estimated_budget_for_live_campaign(
        selected_budget_after, estimated_budget_before_switch, total_spend, daily_spend,
        remaining_days)
    estimated_budget_after_switch_from_ui = campaign_page.get_estimated_budget()
    assert round(calculated_estimated_budget_after_switch, 2) == float(estimated_budget_after_switch_from_ui)
    campaign_page.click_save_cancel_or_draft("Save")
    if campaign_page.is_element_present(CampaignFormLocators.credit_limit_exceeded_modal):
        campaign_page.click_on_element(CampaignFormLocators.campaign_goal_reset_no_locator)
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()
    print("[END] CHANGE BUDGET TYPE")

    print("[START] ESTIMATED TOTAL/DAILY BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(live_campaign_id)
    if selected_budget_type == 'total':
        assert round(calculated_estimated_budget, 2) == float(campaign_list_page.get_campaign_daily_budget(
            live_campaign_id))
    else:
        assert round(calculated_estimated_budget, 2) == float(campaign_list_page.get_campaign_total_budget(
            live_campaign_id))
    print("[END] ESTIMATED TOTAL/DAILY BUDGET VERIFICATION IN CAMPAIGN LIST PAGE")
    print("[END] RTB-9462 Estimated budget calculation for last day campaign")
