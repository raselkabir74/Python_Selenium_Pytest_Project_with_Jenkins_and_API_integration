import json
import os
import time

from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from pages.creatives.creative_form import DspDashboardCreativeForm
from pages.creatives.creative_list import DspDashboardCreativeList
from configurations import generic_modules
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.sidebar.sidebar import DashboardSidebarPage
from PIL import Image
from PIL import ImageChops
from utils.page_names_enum import PageNames


def test_regression_banner_preview_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    with open('assets/creatives/creatives_banner_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)

    # DATA PREPARATION FOR CAMPAIGN CREATION
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)

    # CREATE BANNER TYPE CREATIVE

    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    banner_creative_data['general_information'][
        'title'] = "Test Preview Banner_" + generic_modules.get_random_string(5)
    creative_form_page.provide_info_into_add_creative_set_form(
        banner_creative_data)
    creative_form_page.provide_info_into_add_creative_file_banner_form(
        banner_creative_data)
    campaign_settings_page.wait_for_visibility_of_element(
        CampaignSettingsLocator.creative_three_dot)
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_data['landing_and_creatives'][
        'creative'] = banner_creative_data['general_information']['title']
    campaign_data['name_and_type'][
        'campaign_name'] = 'Automation Preview Banner'
    campaign_page.provide_mandatory_field_campaign_data_and_save(campaign_data,
                                                           "Save")
    assert "Saved successfully." in campaign_settings_page.get_success_message()

    campaign_settings_page.search_and_click_on_campaign_name(
        campaign_data['name_and_type']['campaign_name'],
        index=1)
    # ENTERING PREVIEW PAGE
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_in_browser_locator)
    campaign_settings_page.switch_to_iframe(CampaignSettingsLocator.iframe_locator)
    campaign_settings_page.wait_for_visibility_of_element(
        CampaignSettingsLocator.preview_ad_div_locator)
    campaign_settings_page.switch_to_default_content()
    time.sleep(4)
    campaign_page.take_screenshot(
        'desktop_actual_view_screenshot_banner.png')
    campaign_page.change_resolution(
        'desktop_actual_view_screenshot_banner.png')
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_toggle_locator)
    time.sleep(4)
    campaign_page.take_screenshot(
        'mobile_actual_view_screenshot_banner.png')
    campaign_page.change_resolution(
        'mobile_actual_view_screenshot_banner.png')
    # IMAGES VERIFICATION
    screenshot_folder = 'tests_screenshots'
    view_types = ['desktop', 'mobile']
    # ESTIMATED THRESHOLD
    threshold = 4.1
    try:
        # ITERATE THROUGH EACH VIEW TYPE
        for view_type in view_types:
            expected_screenshot_filename = f'{view_type}_view_screenshot_banner.png'
            actual_screenshot_filename = f'{view_type}_actual_view_screenshot_banner.png'
            # OPEN THE EXPECTED IMAGE
            expected_image_path = os.path.join(screenshot_folder,
                                               expected_screenshot_filename)
            expected_image = Image.open(expected_image_path)
            # OPEN THE ACTUAL IMAGE
            actual_image_path = os.path.join(screenshot_folder,
                                             actual_screenshot_filename)
            actual_image = Image.open(actual_image_path)
            try:
                # CALCULATE THE DIFFERENCE BETWEEN THE IMAGES
                diff = ImageChops.difference(expected_image,
                                             actual_image)
                # CALCULATE THE PERCENTAGE DIFFERENCE
                percentage_diff = (sum(
                    sum(pixel) for pixel in
                    diff.getdata()) / (
                                           255.0 * expected_image.width * expected_image.height)) * 100
                # COMPARE THE PERCENTAGE DIFFERENCE WITH THE THRESHOLD
                if percentage_diff <= threshold:
                    message = f"{view_type.capitalize()} view: Images match! Difference in Percentage: {percentage_diff:.2f}%"
                    print("Pass:", message)
                    assert True, message
                else:
                    message = f"{view_type.capitalize()} view: Images do not match. Difference in Percentage : {percentage_diff:.2f}%"
                    print("Fail:", message)
                    assert False, message
            finally:
                # CLOSE THE ACTUAL IMAGE IF IT WAS OPENED
                actual_image.close()
    finally:
        # REMOVE THE ACTUAL IMAGES REGARDLESS OF THE OUTCOME
        for view_type in view_types:
            actual_screenshot_filename = f'{view_type}_actual_view_screenshot_banner.png'
            actual_image_path = os.path.join(screenshot_folder,
                                             actual_screenshot_filename)
            if os.path.exists(actual_image_path):
                os.remove(actual_image_path)

    # HEADER URL VERIFICATION
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_platform_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://www.eskimi.com/blog" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_ad_gallery_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://www.eskimi.com/gallery" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_manual_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://manual.eskimi.com/" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_book_demo_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://www.eskimi.com/book-demo" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    # CAMPAIGN CLEAN UP
    campaign_page.go_back()
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign_data['name_and_type']['campaign_name'],
        index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()

    # CREATIVE CLEAN UP
    sidebar_navigation.navigate_to_page(PageNames.CREATIVE_SETS)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()
