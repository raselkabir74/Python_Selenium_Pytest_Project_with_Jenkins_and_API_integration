import json
import time

from selenium.webdriver.common.keys import Keys

from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.campaign.campaign_form import DspDashboardCampaignsForm


def test_dashboard_campaign_list_add_campaign_landing_and_creatives(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)

    # SELECT A CREATIVE
    campaign_data['name_and_type']['creative_type'] = "Video"
    campaign_page.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=campaign_data['name_and_type'][
        'creative_type'])
    campaign_page.set_value_into_specific_input_field(CampaignFormLocators.bid_cpm_label,
                                                      campaign_data['launch_date_and_budget']['bid_cpm'])

    # SELECT CREATIVE TYPE
    dropdown_items = [
        {
            "dropdown_item": "Android App download",
            "assert_text": "Google Play Store ID (e.g. your.package.id)",
            "locator": CampaignFormLocators.app_input_field_locator
        },
        {
            "dropdown_item": "App download (Adjust tracking)",
            "assert_text": "Adjust App ID (e.g. abcdef)",
            "locator": CampaignFormLocators.app_input_field2_locator
        },
        {
            "dropdown_item": "Click to action: CALL",
            "assert_text": "International phone number or short code (e.g. +123456789)",
            "locator": CampaignFormLocators.call_input_field_locator
        },
        {
            "dropdown_item": "Click to action: SMS",
            "assert_text": "International phone number or short code (e.g. +123456789)",
            "locator": CampaignFormLocators.call_input_field_locator
        },
        {
            "dropdown_item": 'Click to action: USSD',
            "assert_text": "USSD code (e.g. *999*1#)",
            "locator": CampaignFormLocators.ussd_input_field_locator
        },
        {
            "dropdown_item": 'Landing page',
            "assert_text": "Landing page URL (e.g. https://www.yoursite.com/?click_id={eucid})",
            "locator": CampaignFormLocators.landing_page_url_locator
        }

    ]
    for item in dropdown_items:
        campaign_page.select_dropdown_value(CampaignFormLocators.url_type_label, dropdown_item=item["dropdown_item"])
        assert item[
                   "assert_text"] == campaign_page.get_attribute_value(
            item["locator"], 'placeholder')

    # CLICK URL
    campaign_page.set_value_into_element(
        CampaignFormLocators.click_url_input_field_locator,
        campaign_data['landing_and_creatives']['click_url'])
    campaign_page.click_on_element(
        CampaignFormLocators.click_url_parameters_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.add_utm_parameters_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.add_parameter_locator)
    campaign_page.set_value_into_element(CampaignFormLocators.key_locator,
                                         'Key')
    campaign_page.set_value_into_element(
        CampaignFormLocators.value_locator,
        "111")

    # UPDATED CLICK URL VERIFICATION
    updated_click_url = "https://business.eskimi.com?utm_source=eskimi&utm_medium=cpm&utm_campaign={" \
                        "campaign_title}&utm_term={creative_size}&utm_content=eskimidsp_{site_id}&Key=111"
    assert updated_click_url in campaign_page.get_text_using_tag_attribute(
        campaign_page.input_tag,
        campaign_page.id_attribute,
        CampaignFormLocators.click_url_field_id)

    # AD DOMAIN
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.ad_domain_field_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.ad_domain_field_locator)
    campaign_page.click_on_element(
        CampaignFormLocators.ad_domain_field_locator)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.ad_domain_search_field_locator)
    campaign_page.wait_for_visibility_of_element(
        CampaignFormLocators.ad_domain_search_field_locator)
    campaign_page.wait_for_element_to_be_clickable(
        CampaignFormLocators.ad_domain_search_field_locator)
    campaign_page.set_value_into_element(
        CampaignFormLocators.ad_domain_search_field_locator,
        campaign_data['landing_and_creatives']['ad_domain'])
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.ad_domain_search_field_locator).send_keys(
        Keys.ENTER)
    time.sleep(campaign_page.ONE_SEC_DELAY)
    assert campaign_data['landing_and_creatives'][
               'ad_domain'] == campaign_page.get_text_using_tag_attribute(
        campaign_page.span_tag,
        campaign_page.id_attribute,
        CampaignFormLocators.ad_domain_field_id)

    # CREATIVE_SELECTION AND PER CREATIVE VERIFICATION
    campaign_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=CampaignFormLocators.selected_creative_sets_selection_label,
        option_to_select=campaign_data['landing_and_creatives']['creative'])
    time.sleep(campaign_page.TWO_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.creative_url_toggle)
    time.sleep(campaign_page.TWO_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.click_url_per_creative_locator)
    time.sleep(campaign_page.TWO_SEC_DELAY)
    campaign_page.click_on_element(
        CampaignFormLocators.creative_click_url_cp)
    assert campaign_data['landing_and_creatives'][
               'creative'] == campaign_page.get_selected_options_using_js_code(
        CampaignFormLocators.selected_creative_sets_selection_label)
