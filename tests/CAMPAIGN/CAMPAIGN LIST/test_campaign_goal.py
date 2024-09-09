import copy
import json
import time

from selenium.common import TimeoutException

from pages.campaign.campaign_form import DspDashboardCampaignsForm
from locators.campaign.campaign_form_locator import CampaignFormLocators


def test_dashboard_campaign_list_campaign_goal(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data_copy = copy.deepcopy(campaign_data)
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)
    campaign_data_copy['name_and_type']['platform_type'] = ['facebook',
                                                            'youtube',
                                                            'adwords']

    # GOALS NOT AVAILABLE FOR PLATFORMS APART FROM ESKIMI
    campaign_page.click_on_element(
        CampaignFormLocators.platform_type_locator)
    for platform_type in campaign_data_copy['name_and_type'][
        'platform_type']:
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.platform_name.format(
                platform_type),
            locator_initialization=True)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.platform_name.format(
                platform_type),
            locator_initialization=True)
        campaign_page.click_on_element(
            CampaignFormLocators.platform_name.format(
                platform_type),
            locator_initialization=True)
        assert False == campaign_page.is_element_displayed(
            CampaignFormLocators.campaign_goal_section_locator)

    # GOAL MANDATORY MESSAGE
    campaign_data_copy['name_and_type']['platform_type'] = 'eskimi'
    campaign_data_copy['name_and_type']['creative_type'] = 'Video'
    campaign_page.click_on_element(
        CampaignFormLocators.platform_name.format(
            campaign_data_copy['name_and_type']['platform_type']),
        locator_initialization=True)
    try:
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.creative_type_dropdown_locator,
            campaign_page.HALF_MINUTE)
    finally:
        campaign_page.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=campaign_data_copy[
            'name_and_type'][
            'creative_type'])
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.button_group_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.button_group_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.publish_button_locator)
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.publish_button_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.publish_button_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    try:
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.
            campaign_goal_mandatory_message_locator)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.
            campaign_goal_mandatory_message_locator)
        campaign_page.scroll_to_specific_element(
            CampaignFormLocators.campaign_goal_mandatory_message_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        assert "Goal type is required" in campaign_page.get_element_text(
            CampaignFormLocators.
            campaign_goal_mandatory_message_locator)
    except TimeoutException:
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.button_group_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        campaign_page.click_on_element(
            CampaignFormLocators.button_group_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.publish_button_locator)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.publish_button_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.publish_button_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.
            campaign_goal_mandatory_message_locator)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.
            campaign_goal_mandatory_message_locator)
        campaign_page.scroll_to_specific_element(
            CampaignFormLocators.campaign_goal_mandatory_message_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        assert "Goal type is required" in campaign_page.get_element_text(
            CampaignFormLocators.
            campaign_goal_mandatory_message_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.campaign_goal.format(
            campaign_data_copy['campaign_goal_info'][
                'campaign_goal']),
        locator_initialization=True)
    assert "Primary objective is required" in campaign_page.get_element_text(
        CampaignFormLocators.primary_objective_mandatory_message_locator)
    campaign_page.provide_campaign_objective(campaign_data_copy)
    campaign_goal_traffic = '3'
    campaign_page.click_on_element(
        CampaignFormLocators.campaign_goal.format(
            campaign_goal_traffic),
        locator_initialization=True)
    campaign_page.click_on_element(
        CampaignFormLocators.campaign_goal_reset_no_locator)
    assert '2' == campaign_page.get_attribute_value(
        CampaignFormLocators.selected_campaign_goal_locator, 'value')
    campaign_page.click_on_element(
        CampaignFormLocators.campaign_goal.format(
            campaign_goal_traffic),
        locator_initialization=True)
    campaign_page.click_on_element(
        CampaignFormLocators.campaign_goal_reset_yes_locator)
    assert '3' == campaign_page.get_attribute_value(
        CampaignFormLocators.selected_campaign_goal_locator, 'value')

    # CURRENCY AND PERCENTAGE SYMBOL VALIDATION
    campaign_data_copy['campaign_goal_info'][
        'primary_objective'] = "cpc_currency:2"
    primary_objective = campaign_data_copy['campaign_goal_info'][
        'primary_objective'].split(':')
    campaign_page.click_on_element_using_tag_attribute(
        campaign_page.div_tag,
        CampaignFormLocators.goal_attribute,
        primary_objective[0])
    assert '$' in campaign_page.get_element_text(
        CampaignFormLocators.primary_objective_symbol_locator)
    campaign_data_copy['campaign_goal_info'][
        'secondary_objectives'] = "ctr:2"
    secondary_objective = campaign_data_copy['campaign_goal_info'][
        'secondary_objectives'].split(':')
    campaign_page.click_on_element_using_tag_attribute(
        campaign_page.div_tag,
        CampaignFormLocators.goal_attribute,
        secondary_objective[0])
    assert '%' in campaign_page.get_element_text(
        CampaignFormLocators.secondary_objective_symbol_locator)
