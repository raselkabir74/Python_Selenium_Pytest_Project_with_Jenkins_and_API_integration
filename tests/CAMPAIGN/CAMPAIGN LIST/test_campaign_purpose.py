import json
import time

from pages.campaign.campaign_form import DspDashboardCampaignsForm
from locators.campaign.campaign_form_locator import CampaignFormLocators


def test_dashboard_campaign_list_campaign_purpose(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_regression_data.json') as json_file:
        campaign_regression_data = json.load(json_file)
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)

    # VERIFY CAMPAIGN PURPOSE AND PRIMARY OPERATOR SELECTION
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.country_label,
        option_to_select=campaign_regression_data['location_and_audiences']['country_name'])
    campaign_page.click_on_element(CampaignFormLocators.platforms_telco_devices_group_locator,
                                   locator_to_be_appeared=CampaignFormLocators.ad_placement_type_locator)
    if (campaign_page.get_attribute_value(CampaignFormLocators.advance_targeting_selection_locator, "aria-expanded")
            == "false"):
        campaign_page.click_on_element(CampaignFormLocators.advance_targeting_selection_locator,
                                       locator_to_be_appeared=CampaignFormLocators.campaign_purpose_label)
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.campaign_purpose_label,
        option_to_select=campaign_regression_data['campaign_purpose']['campaign_purpose'])

    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.primary_operator_label,
        option_to_select=campaign_regression_data['campaign_purpose']['primary_operator'])
    time.sleep(3)
    assert campaign_regression_data['campaign_purpose'][
               'campaign_purpose'] in campaign_page.get_text_using_tag_attribute(
        campaign_page.span_tag,
        campaign_page.id_attribute,
        CampaignFormLocators.
        campaign_purpose_field_id)

    assert campaign_regression_data['campaign_purpose'][
               'primary_operator'] in campaign_page.get_text_using_tag_attribute(
        campaign_page.span_tag,
        campaign_page.id_attribute,
        CampaignFormLocators.
        primary_operator_field_id)

    # VERIFY ALERT MESSAGE IN CAMPAIGN PURPOSE FOR MULTIPLE COUNTRY
    campaign_regression_data['location_and_audiences'][
        'country_name'] = "Bangladesh"
    campaign_page.select_from_modal(campaign_regression_data['location_and_audiences'][
                                        'country_name'], CampaignFormLocators.country_label, click_uncheck_all=False)
    time.sleep(3)
    assert "Select one country to set Telco objective and Primary operator" in campaign_page.get_element_text(
        CampaignFormLocators.campaign_purpose_warning_message_locator)
