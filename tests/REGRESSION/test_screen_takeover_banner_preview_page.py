import json
import os
import time

from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from configurations import generic_modules
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.sidebar.sidebar import DashboardSidebarPage
from PIL import Image
from PIL import ImageChops
from utils.page_names_enum import PageNames


def test_regression_screen_takeover_banner_preview_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    generic_modules.step_info("[START - RTB-7782] Validate “Floating/screentakeover” preview page functionality")

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)

    # CREATE CAMPAIGN WITH SCREEN TAKEOVER CREATIVE
    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_data['landing_and_creatives'][
        'creative'] = "Screen takeover banner 444"
    campaign_data['name_and_type'][
        'campaign_name'] = 'Automation Screen Takeover Preview Banner'
    campaign_page.provide_mandatory_field_campaign_data_and_save(campaign_data, "Save")
    assert "Saved successfully." in campaign_settings_page.get_success_message()

    campaign_settings_page.search_and_click_on_campaign_name(
        campaign_data['name_and_type']['campaign_name'],
        index=1)

    # ENTERING PREVIEW PAGE
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_in_browser_locator)
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_copy_icon)
    time.sleep(3)
    campaign_page.take_screenshot(
        'desktop_actual_view_screenshot_screentakeover_banner.png')
    campaign_page.change_resolution(
        'desktop_actual_view_screenshot_screentakeover_banner.png')
    campaign_settings_page.click_on_element(
        CampaignSettingsLocator.preview_toggle_locator)
    time.sleep(4)
    campaign_page.take_screenshot(
        'mobile_actual_view_screenshot_screentakeover_banner.png')
    campaign_page.change_resolution(
        'mobile_actual_view_screenshot_screentakeover_banner.png')

    # IMAGES VERIFICATION
    screenshot_folder = 'tests_screenshots'
    view_types = ['desktop', 'mobile']
    # ESTIMATED THRESHOLD
    threshold = 4.5
    try:
        # ITERATE THROUGH EACH VIEW TYPE
        for view_type in view_types:
            expected_screenshot_filename = f'{view_type}_view_screenshot_screentakeover_banner.png'
            actual_screenshot_filename = f'{view_type}_actual_view_screenshot_screentakeover_banner.png'
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
                    message = f"{view_type.capitalize()} view: Images match! Difference in Percentage: " \
                              f"{percentage_diff:.2f}%"
                    print("Pass:", message)
                    assert True, message
                else:
                    message = f"{view_type.capitalize()} view: Images do not match. Difference in Percentage : " \
                              f"{percentage_diff:.2f}%"
                    print("Fail:", message)
                    assert False, message
            finally:
                # CLOSE THE ACTUAL IMAGE IF IT WAS OPENED
                actual_image.close()
    finally:
        # REMOVE THE ACTUAL IMAGES REGARDLESS OF THE OUTCOME
        for view_type in view_types:
            actual_screenshot_filename = f'{view_type}_actual_view_screenshot_screentakeover_banner.png'
            actual_image_path = os.path.join(screenshot_folder,
                                             actual_screenshot_filename)
            if os.path.exists(actual_image_path):
                os.remove(actual_image_path)

    # CAMPAIGN CLEAN UP
    campaign_page.go_back()
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(
        campaign_data['name_and_type']['campaign_name'],
        index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()
    generic_modules.step_info("[END - RTB-7782] Validate “Floating/screentakeover” preview page functionality")
