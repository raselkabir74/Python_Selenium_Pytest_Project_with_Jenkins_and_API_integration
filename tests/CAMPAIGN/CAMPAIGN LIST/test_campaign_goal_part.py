import json

from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings


def test_dashboard_campaign_list_campaign_goal_part(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    new_campaign_group = DspDashboardCampaignsSettings(driver)
    campaign_page = DspDashboardCampaignsForm(driver)

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)

    new_campaign_group.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(campaign_data)

    assert campaign_page.is_element_displayed(
        CampaignFormLocators.campaign_goal_locator_awareness,
        locator_initialization=False)
    assert campaign_page.is_element_displayed(
        CampaignFormLocators.campaign_goal_locator_traffic,
        locator_initialization=False)
    assert campaign_page.is_element_displayed(
        CampaignFormLocators.campaign_goal_locator_engagement,
        locator_initialization=False)
    assert campaign_page.is_element_displayed(
        CampaignFormLocators.campaign_goal_locator_other,
        locator_initialization=False)
