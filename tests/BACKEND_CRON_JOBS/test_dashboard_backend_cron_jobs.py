import json
from configurations import generic_modules
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_list_locator import CampaignListLocators
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from locators.sites_categoires.site_cetagories_locators import SiteCategoriesLocators
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.budget.add_payment import DspDashboardAddPayment
from pages.site_categories.site_categories_page import DashboardSiteCategories
from utils.campaigns import CampaignUtils
from utils.page_names_enum import PageNames
from utils.sites_categories import SitesCategoriesUtils


def test_regression_dashboard_backend_cron_job_for_campaign_status_change(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    generic_modules.step_info("[START - RTB-9404] Validate campaign status change and manage daily cap cron jobs")
    print("[START] GET CAMPAIGN ID AND RUN CRON JOB")
    live_campaign_id = CampaignUtils.pull_campaign_with_specific_status_id_from_db(db_connection)
    campaign_list_page.run_change_campaign_status_cron_job(live_campaign_id, 6)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(live_campaign_id)
    assert "Bud." == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
    print("[END] GET CAMPAIGN ID AND RUN CRON JOB")

    print("[START] EDIT TOTAL BUDGET")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    current_budget = campaign_page.get_budget_amount()
    new_budget = float(current_budget) + 10
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa, new_budget)
    campaign_page.click_save_cancel_or_draft(action='save')
    if campaign_page.is_element_present(CampaignFormLocators.credit_limit_exceeded_modal):
        campaign_page.click_on_element(CampaignFormLocators.campaign_goal_reset_no_locator)
    campaign_list_page.search_and_action(live_campaign_id)
    campaign_list_page.get_element_text(CampaignListLocators.campaign_list_draft_status)
    assert "Live" == campaign_list_page.get_campaign_status(live_campaign_id)
    print("[END] EDIT TOTAL BUDGET")
    generic_modules.step_info("[END - RTB-9404] Validate campaign status change and manage daily cap cron jobs")


def test_regression_dashboard_backend_cron_job_for_manage_daily_cap(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    generic_modules.step_info("[START - RTB-9404] Validate campaign status change and manage daily cap cron jobs")
    print("[START] GET CAMPAIGN ID AND RUN CRON JOB")
    live_campaign_id = CampaignUtils.pull_campaign_with_specific_status_id_from_db(db_connection)
    campaign_list_page.run_change_campaign_status_cron_job(live_campaign_id, 8)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(live_campaign_id)
    assert "Dai." == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
    print("[END] GET CAMPAIGN ID AND RUN CRON JOB")

    print("[START] RUN MANAGE DAILY CAP CRON JOB")
    campaign_list_page.run_manage_daily_cap_cron_job(live_campaign_id)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(live_campaign_id)
    assert "Live" == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
    print("[END] RUN MANAGE DAILY CAP CRON JOB")
    generic_modules.step_info("[END - RTB-9404] Validate campaign status change and manage daily cap cron jobs")


def test_regression_dashboard_manage_inactive_campaign_status_cron_job(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    generic_modules.step_info("[START - RTB-9411] Validate campaign manage status cron job")
    print("[START] GET CAMPAIGN ID AND RUN CRON JOB")
    inactive_campaign_id = CampaignUtils.pull_inactive_live_campaign_id_from_db(db_connection, status='12')
    if inactive_campaign_id is None:
        live_campaign_id = CampaignUtils.pull_inactive_live_campaign_id_from_db(db_connection, status='1')
        campaign_list_page.run_change_campaign_status_cron_job(live_campaign_id, 12)
        sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
        campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
        campaign_settings_page.search_campaign(live_campaign_id)
        assert True is campaign_settings_page.is_element_displayed(
            CampaignSettingsLocator.campaign_inactive_status_locator)
        campaign_id = live_campaign_id
    else:
        campaign_id = inactive_campaign_id
    campaign_list_page.run_manage_status_cron_job(campaign_id)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(campaign_id)
    assert "Live" == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
    print("[END] GET CAMPAIGN ID AND RUN CRON JOB")
    generic_modules.step_info("[END - RTB-9411] Validate campaign manage status cron job")


def test_regression_dashboard_manage_ready_campaign_status_cron_job(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    generic_modules.step_info("[START - RTB-9411] Validate campaign manage status cron job")
    print("[START] GET CAMPAIGN ID AND RUN CRON JOB")
    ready_campaign_id = CampaignUtils.pull_ready_live_campaign_id_from_db(db_connection, status='5')
    if ready_campaign_id is None:
        live_campaign_id = CampaignUtils.pull_ready_live_campaign_id_from_db(db_connection, status='1')
        if live_campaign_id is None:
            live_campaign_id = CampaignUtils.pull_ready_live_campaign_id_from_db(db_connection, status='11')
        campaign_list_page.run_change_campaign_status_cron_job(live_campaign_id, 5)
        sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
        campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
        campaign_settings_page.search_campaign(live_campaign_id)
        assert "Rea." == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
        campaign_id = live_campaign_id
    else:
        campaign_id = ready_campaign_id
    campaign_list_page.run_manage_status_cron_job(campaign_id)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(campaign_id)
    assert "Live" == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
    print("[END] GET CAMPAIGN ID AND RUN CRON JOB")
    generic_modules.step_info("[END - RTB-9411] Validate campaign manage status cron job")


def test_regression_dashboard_manage_expired_campaign_status_cron_job(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    generic_modules.step_info("[START - RTB-9411] Validate campaign manage status cron job")
    print("[START] GET CAMPAIGN ID AND RUN CRON JOB")
    live_campaign_id = CampaignUtils.pull_expired_live_campaign_id_from_db(db_connection, status='1')
    if live_campaign_id is None:
        expired_campaign_id = CampaignUtils.pull_expired_live_campaign_id_from_db(db_connection, status='7')
        campaign_list_page.run_change_campaign_status_cron_job(expired_campaign_id, 1)
        sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
        campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
        campaign_settings_page.search_campaign(expired_campaign_id)
        assert "Live" == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
        campaign_id = expired_campaign_id
    else:
        campaign_id = live_campaign_id
    campaign_list_page.run_manage_status_cron_job(campaign_id)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(campaign_id)
    assert "Exp." == campaign_settings_page.get_element_text(CampaignSettingsLocator.campaign_status_locator)
    print("[END] GET CAMPAIGN ID AND RUN CRON JOB")
    generic_modules.step_info("[END - RTB-9411] Validate campaign manage status cron job")


def test_regression_dashboard_budget_recalculate_cron_job(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)

    generic_modules.step_info("[START - RTB-9418] Budget recalculate CRON")
    print("[START] GET CAMPAIGN ID")
    live_campaign_id = CampaignUtils.pull_campaign_with_specific_status_id_from_db(db_connection)
    user_id = CampaignUtils.pull_campaign_user_id_from_db(live_campaign_id, db_connection)
    payment_page.display_budget_information(user_id)
    print("[END] GET CAMPAIGN ID")

    print("[START] GET CAMPAIGN SPEND")
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.deselect_all_from_modal_form_using_js_code(CampaignSettingsLocator.user_filter_data_qa)
    campaign_settings_page.search_campaign(live_campaign_id)
    total_spend = campaign_settings_page.get_total_spend(live_campaign_id)
    today_spend = campaign_settings_page.get_today_spend(live_campaign_id)
    print("[END] GET CAMPAIGN SPEND")

    print("[START] GET ESTIMATED BUDGET AND RUN CRON JOB")
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    remaining_days = campaign_page.calculate_remaining_days(db_connection, live_campaign_id)
    selected_budget_type = campaign_page.get_selected_budget()
    budget_amount = campaign_page.get_budget_amount()
    if selected_budget_type == "total":
        estimated_budget = (float(budget_amount) - float(total_spend) + float(today_spend)) / float(remaining_days)
    else:
        remaining_daily_budget = float(budget_amount) - float(today_spend)
        estimated_budget = \
            float(total_spend) + remaining_daily_budget + (float(budget_amount) * float(remaining_days - 1))
    if round(estimated_budget, 2) == float(campaign_page.get_estimated_budget()):
        pass
    else:
        campaign_list_page.run_recalculate_daily_cron_job(live_campaign_id)
    campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
        str(live_campaign_id))
    driver.get(campaign_edit_url)
    assert round(estimated_budget, 2) == float(campaign_page.get_estimated_budget())
    print("[END] GET ESTIMATED BUDGET AND RUN CRON JOB")
    generic_modules.step_info("[END - RTB-9418] Budget recalculate CRON")


def test_regression_dashboard_cron_job_for_site_count(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    site_category_page = DashboardSiteCategories(driver)

    generic_modules.step_info("[START - RTB-9406] Validate site count cron job")

    with open('assets/sites_categories/sites_categories_data.json') as json_file:
        sites_categories_data = json.load(json_file)
    sites_categories_data['sites_categories_data']['category_name'] = \
        sites_categories_data['sites_categories_data']['category_name'] + generic_modules.get_random_string(5)

    print("[START] CREATE APP/SITE CATEGORY AND RUN CRON JOB")
    print("Disabling on other environments because of issue https://eskimidev.atlassian.net/browse/RTB-9610")
    if "qa-testing" in config['credential']['url']:
        sidebar_navigation.navigate_to_page(PageNames.SITES_CATEGORIES)
        site_category_page.create_new_app_site_category(sites_categories_data)
        assert "File uploaded successfully. We will notify through email, when processing will complete." in \
            site_category_page.get_element_text(SiteCategoriesLocators.successful_message_data_qa)
        site_category_page.click_on_element(SiteCategoriesLocators.cancel_btn)
        sites_category_id = SitesCategoriesUtils.pull_sites_categories_id_from_db(db_connection, sites_categories_data[
            'sites_categories_data']['category_name'])
        site_category_page.search_and_action(sites_categories_data['sites_categories_data']['category_name'],
                                            sites_category_id)
        count_before_run_cron = site_category_page.get_element_text(SiteCategoriesLocators.app_sites_count_locator)
        campaign_list_page.run_site_count_cron_job(sites_category_id)
        sidebar_navigation.navigate_to_page(PageNames.SITES_CATEGORIES)
        site_category_page.search_and_action(sites_categories_data['sites_categories_data']['category_name'],
                                            sites_category_id)
        count_after_run_cron = site_category_page.get_element_text(SiteCategoriesLocators.app_sites_count_locator)
        assert int(count_after_run_cron) == int(count_before_run_cron) + 4
        print("[END] CREATE APP/SITE CATEGORY AND RUN CRON JOB")

        print("[START] DELETE APP/SITE CATEGORY")
        site_category_page.search_and_action(sites_categories_data['sites_categories_data']['category_name'],
                                            sites_category_id, action='delete')
        print("[END] DELETE APP/SITE CATEGORY")
        generic_modules.step_info("[END - RTB-9406] Validate site count cron job")
