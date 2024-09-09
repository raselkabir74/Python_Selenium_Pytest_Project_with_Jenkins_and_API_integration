import json
import time
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.navbar.navbar import DashboardNavbar
from utils.currency import CurrencyUtils


def test_dashboard_campaign_list_campaign_launch_date_and_budget(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_regression_data.json') as json_file:
        campaign_regression_data = json.load(json_file)

    # VERIFY DAILY BUDGET BASED ON DATE, TIME_AND_DAY_SCHEDULING, BID CPM AND TOTAL BUDGET
    navbar.impersonate_user('Webcoupers - GLO')
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.select_specific_date_range(
        CampaignFormLocators.date_label,
        "7 Days")
    campaign_page.click_on_element(
        CampaignFormLocators.time_and_day_scheduling_locator)
    time.sleep(campaign_page.TWO_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.specific_time_and_day_scheduling_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.time_and_day_scheduling_save_button_locator)
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.bid_cpm_label,
                                                      campaign_regression_data['launch_date_and_budget']['bid_cpm'])
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.budget_input_data_qa,
                                                      campaign_regression_data['launch_date_and_budget'][
                                                          'total_budget'])
    assert campaign_regression_data['launch_date_and_budget'][
               'daily_budget'] in campaign_page.get_estimated_budget()

    # VERIFY IN USD VALUE AND CURRENCY BASED ON USER SETTINGS FOR BUDGET
    assert "₦" in campaign_page.get_element_text(
        CampaignFormLocators.estimated_budget_currency_locator)

    # VERIFY IN USD VALUE AND CURRENCY BASED ON USER SETTINGS FOR BID CPM
    currency_rate = float(CurrencyUtils.pull_specific_currency_rate_data_db(
        102, db_connection))
    bid_cpm_in_usd = float(campaign_regression_data['launch_date_and_budget']['bid_cpm']) / currency_rate
    bid_cpm_in_usd_str = "{:.2f}".format(bid_cpm_in_usd)
    assert bid_cpm_in_usd_str in campaign_page.get_element_text(
        CampaignFormLocators.bid_cpm_in_usd_locator)
    assert "₦" in campaign_page.get_element_text(
        CampaignFormLocators.bid_cpm_currency_locator)

    # VERIFY 'START CAMPAIGN AFTER APPROVAL' IS CHECKED BY DEFAULT
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.start_campaign_after_approval_locator)
    assert "true" in campaign_page.get_attribute_value(
        CampaignFormLocators.start_campaign_after_approval_locator,
        "checked")

    # VERIFY WARNING MESSAGE IF BID CPM NOT IN RANGE
    bid_cpm = 0.1
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.bid_cpm_label, bid_cpm)
    assert "Bid (CPM) must be between 1 to 14000" in \
           campaign_page.get_element_text(
               CampaignFormLocators.bid_cpm_error_message_locator)
