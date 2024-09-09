import json
import time
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.creative.creative_form_locator import CreativeFormLocators
from pages.navbar.navbar import DashboardNavbar


def test_dashboard_campaign_list_campaign_name_and_type(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED CAMPAIGN DATA IN GUI
    with open(
            'assets/regression_tests/campaign_regression_data.json') as json_file:
        campaign_regression_data = json.load(json_file)
    campaign_url = (config['credential']['url']
                    + config['campaign-creation-page']['campaign-creation-url'])
    driver.get(campaign_url)
    # VERIFY CREATIVE TYPES FOR PLATFORMS
    platform_names = ['eskimi', 'facebook', 'youtube', 'adwords']
    for name in platform_names:
        available_options = []
        expected_options = []
        campaign_page.click_on_element(
            CampaignFormLocators.platform_type_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.platform_name.format(name),
            locator_initialization=True)
        time.sleep(1)
        creative_type_dropdown = Select(
            driver.find_element(By.XPATH,
                                "//select[@id='js-campaign-type']"))
        creative_type_dropdown_options = creative_type_dropdown.options
        for option in creative_type_dropdown_options:
            available_options.append(option.text)
        if name == 'eskimi':
            expected_options = ['Please Select', 'Banner',
                                'Native', 'Video',
                                'Native video', 'Audio']
        elif name == 'facebook':
            expected_options = ['Please Select', 'Native', 'Video',
                                'Engagement', 'Carousel']
        elif name == 'youtube':
            expected_options = ['Please Select', 'Video']
        elif name == 'adwords':
            expected_options = ['Please Select', 'Banner', 'Video']
        for expected_option in expected_options:
            assert expected_option in available_options
        available_options.clear()

    # VERIFY CREATIVE TYPES FOR PLATFORMS END
    campaign_settings_page.move_to_campaign_settings_page()
    try:
        WebDriverWait(campaign_page.driver, 5).until(
            EC.alert_is_present(),
            'Timed out waiting for alert to appear')
        alert = campaign_page.driver.switch_to.alert
        alert.accept()
    except TimeoutException:
        print("Alert not present")

    campaign_settings_page.navigate_to_add_campaign_group()
    navbar.impersonate_user('Webcoupers - GLO')

    # UNAVAILABLE CREATIVE POP-UP WARNING VERIFICATION
    creative_type = campaign_regression_data['name_and_type'][
        'creative_type']
    try:
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.creative_type_dropdown_locator,
            campaign_page.HALF_MINUTE)
    finally:
        campaign_page.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=creative_type)
    assert "Hey! We noticed that your account doesn't have " + \
           campaign_regression_data['name_and_type'][
               'creative_type'].lower() \
           + " creatives uploaded. Please upload creatives and then continue the campaign setup." \
           in campaign_page.get_unavailable_creative_type_alert_message()

    # ADD CREATIVE BUTTON FUNCTIONALITY VERIFICATION
    campaign_page.click_on_element(
        CampaignFormLocators.add_creative_from_popup_locator)
    creative_type = campaign_regression_data['name_and_type'][
        'creative_type']
    assert creative_type in campaign_page.get_selected_options_using_js_code(
        CreativeFormLocators.creative_format_data_qa)

    # DEFAULT 'DISPLAY ADS' VALUE VERIFICATION FOR 'CAMPAIGN TYPE'
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=creative_type)
    campaign_page.click_on_element(
        CampaignFormLocators.cancel_creative_from_popup_locator)
    campaign_page.wait_for_presence_of_element(
        CampaignFormLocators.campaign_type_dropdown_locator)
    assert "Display Ads" in campaign_page.get_element_text(
        CampaignFormLocators.campaign_type_dropdown_locator)

    # 'IN-GAME' TYPE CAMPAIGN AVAILABILITY VERIFICATION BASED ON 'CAMPAIGN TYPE'
    creative_types = ['Banner', 'Video']
    for creative_type in creative_types:
        campaign_regression_data['name_and_type'][
            'creative_type'] = creative_type
        campaign_page.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=creative_type)
        campaign_page.select_dropdown_value(CampaignFormLocators.campaign_type_label,
                                            campaign_regression_data['name_and_type'][
                                                'campaign_type'])
        assert "In-Game" in campaign_page.get_element_text(
            CampaignFormLocators.campaign_type_dropdown_locator)

    # CAMPAIGN NAME VALIDATION MESSAGE VERIFICATION
    campaign_page.click_on_element(
        CampaignFormLocators.publish_button_locator)
    assert "Campaign name is required" in campaign_page.get_element_text(
        CampaignFormLocators.
        campaign_name_mandatory_message_locator)
