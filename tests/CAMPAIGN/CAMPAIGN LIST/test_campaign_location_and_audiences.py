import json
import time
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from locators.campaign.campaign_form_locator import CampaignFormLocators


def test_dashboard_campaign_list_campaign_location_and_audiences(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_regression_data.json') as json_file:
        campaign_regression_data = json.load(json_file)
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)
    campaign_page.click_on_element(
        CampaignFormLocators.audience_section_locator)

    # VERIFY AUDIENCE APPEARANCE BASED ON SELECTED AUDIENCE GROUP
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.audience_include_label_locator,
        option_to_select=campaign_regression_data['location_and_audiences']['audience_include'])
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.audience_include_value_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    assert campaign_regression_data['location_and_audiences'][
               'audience_include'] in campaign_page.get_element_text(
        CampaignFormLocators.audience_include_value_locator)
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.audience_group_exclude_label_locator,
        option_to_select=campaign_regression_data['location_and_audiences']['audience_group_exclude'])
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.audience_exclude_value_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    assert campaign_regression_data['location_and_audiences'][
               'audience_exclude'] in campaign_page.get_element_text(
        CampaignFormLocators.audience_exclude_value_locator)

    # VERIFY SELECTED VALUE IN 'INCLUDE' NOT AVAILABLE IN 'EXCLUDE' AND VICE VERSA
    campaign_page.click_on_element(
        CampaignFormLocators.audience_include_selection_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.set_value_into_element(
        CampaignFormLocators.audience_include_search_locator,
        campaign_regression_data['location_and_audiences'][
            "audience_exclude"])
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.audience_include_warning_message_locator)
    assert "No result found" in campaign_page.get_element_text(
        CampaignFormLocators.audience_include_warning_message_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.audience_include_cancel_button_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.audience_exclude_selection_locator)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.audience_exclude_search_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.set_value_into_element(
        CampaignFormLocators.audience_exclude_search_locator,
        campaign_regression_data['location_and_audiences'][
            "audience_include"])
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.audience_exclude_warning_message_locator)
    assert "No result found" in campaign_page.get_element_text(
        CampaignFormLocators.audience_exclude_warning_message_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.audience_exclude_cancel_button_locator)
