import re
from decimal import Decimal, ROUND_HALF_UP

from configurations import generic_modules
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from locators.report.report_page_locator import ReportPageLocators
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.navbar.navbar import DashboardNavbar
from pages.report.report_page import DashboardReportPage
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils
from utils.redis import RedisUtils
from utils.page_names_enum import PageNames


def test_dashboard_edit_main_margin_for_campaign_with_fixed_cpm(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)
    report_page = DashboardReportPage(driver)
    sidebar_page = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)
    campaign = {}

    generic_modules.step_info("[START - RTB-8856] Verify that correct amount of fixed CPM is displayed in report page")

    if "qa-testing" in config['credential']['url']:
        print("[START] GET CAMPAIGN FROM DB")
        campaign['campaign_id'] = CampaignUtils.pull_campaign_id_with_fixed_cpm_from_db(db_connection)
        campaign['campaign_name'] = CampaignUtils.pull_campaign_name_from_db(campaign['campaign_id'], db_connection)
        campaign['user_id'] = CampaignUtils.pull_campaign_user_id_from_db(campaign['campaign_id'], db_connection)
        campaign['main_margin_update_today'] = CampaignUtils.check_main_margin_changes_today(db_connection,
                                                                                              campaign['campaign_id'])
        campaign['client_name'] = CampaignUtils.pull_user_name_from_db(db_connection, campaign['user_id'])

        payment_page.display_budget_information(campaign['user_id'])
        print("[END] GET CAMPAIGN FROM DB")

        print("[START] GET SPENT FROM REDIS")
        campaign['campaign_total_spent'] = redis_page.get_total_spent_amount(redis_connection, campaign['campaign_id'])
        print("[END] GET SPENT FROM REDIS")

        print("[START] EDIT MAIN MARGIN AND APPROVE")
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(campaign['campaign_id']))
        driver.get(campaign_approve_url)
        campaign['fixed_cpm_value'] = round(float(campaign_approve_form.get_attribute_value(
            CampaignApproveLocators.reporting_type_input_data_qa, "value")), 2)
        campaign['fixed_cpm_currency'] = campaign_approve_form.get_element_text(
            CampaignApproveLocators.reporting_type_currency_locator)
        campaign['main_margin'] = float(campaign_approve_form.get_attribute_value(
            CampaignApproveLocators.main_margin_locator, "value"))
        campaign['total_budget'] = campaign_approve_form.get_total_budget()
        max_allowed_main_margin = campaign_approve_form.get_calculated_max_allowed_main_margin(
            campaign['total_budget'], campaign['campaign_total_spent'])
        updated_main_margin = campaign_approve_form.get_updated_main_margin(campaign['main_margin'],
                                                                            max_allowed_main_margin)
        campaign_approve_form.set_value_into_element(CampaignApproveLocators.main_margin_locator, updated_main_margin)
        campaign_approve_form.click_approve_button()
        campaign_approve_form.click_on_element(CampaignApproveLocators.main_margin_changes_modal_confirm_btn_locator)
        navbar.impersonate_user(campaign['client_name'])
        print("[END] EDIT MAIN MARGIN AND APPROVE")

        print("[START] FIXED CPM VERIFICATION IN REPORT PAGE")
        sidebar_page.navigate_to_page(PageNames.REPORTS)
        if campaign['fixed_cpm_currency'] == "$":
            based_on_revenue_option = "Spent based on revenue"
            based_on_revenue_with_margin_option = "Spent based on revenue with margin"
        else:
            based_on_revenue_option = "Spent based on revenue ({})".format(campaign['fixed_cpm_currency'])
            based_on_revenue_with_margin_option = \
            "Spent based on revenue with margin ({})".format(campaign['fixed_cpm_currency'])
        report_page.generate_specific_report(campaign['campaign_name'], campaign['campaign_id'], "Admin view", based_on_revenue_option)
        cpm_based_on_revenue_from_report = report_page.get_element_text(ReportPageLocators.cpm_amount_data_qa)
        cpm_based_on_revenue_from_report = float(
            re.sub(r'[^\d.,]', '', cpm_based_on_revenue_from_report).replace(',', ''))
        decimal_current_main_margin = campaign['main_margin'] / 100
        old_cpm_without_margin = campaign['fixed_cpm_value'] * (1 - decimal_current_main_margin)
        old_cpm_without_margin = Decimal(old_cpm_without_margin).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        decimal_updated_main_margin = updated_main_margin / 100
        new_cpm_without_margin = campaign['fixed_cpm_value'] * (1 - decimal_updated_main_margin)
        new_cpm_without_margin = Decimal(new_cpm_without_margin).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if False is campaign['main_margin_update_today']:
            assert float(old_cpm_without_margin) == cpm_based_on_revenue_from_report

        report_page.select_dropdown_value(ReportPageLocators.spent_select_data_qa, based_on_revenue_with_margin_option)
        report_page.click_on_element(ReportPageLocators.update_report_button_data_qa,
                                     locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        cpm_with_margin_from_report = report_page.get_element_text(ReportPageLocators.cpm_amount_data_qa)
        cpm_with_margin_from_report = float(re.sub(r'[^\d.,]', '', cpm_with_margin_from_report).replace(',', ''))
        assert float(campaign['fixed_cpm_value']) == cpm_with_margin_from_report
        print("[END] FIXED CPM VERIFICATION IN REPORT PAGE")

        print("[START] FIXED CPM VERIFICATION IN DB")
        pulled_fixed_cpm = round(CampaignUtils.pull_fixed_cpm_from_db(db_connection, campaign['campaign_id']), 2)
        assert float(campaign['fixed_cpm_value']) == float(pulled_fixed_cpm)
        print("[END] FIXED CPM VERIFICATION IN DB")

        print("[START] REDIS DATA VERIFICATION")
        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign['campaign_id'],
                                                                           key="campaignSettings")
        fixed_cmp_from_redis = redis_data['reporting']['price']['currency']
        fixed_cmp_from_redis = float(fixed_cmp_from_redis) * 1000
        formatted_fixed_cpm_from_redis = Decimal(fixed_cmp_from_redis).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        assert float(new_cpm_without_margin) == float(formatted_fixed_cpm_from_redis)
        print("[END] REDIS DATA VERIFICATION")

    generic_modules.step_info("[END - RTB-8856] Verify that correct amount of fixed CPM is displayed in report page")
