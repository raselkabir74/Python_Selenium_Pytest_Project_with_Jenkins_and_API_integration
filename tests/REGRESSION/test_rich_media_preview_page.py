import json
import os
import time
from PIL import Image, ImageChops
from locators.creative.creative_form_locator import CreativeFormLocators
from locators.campaign.campaign_settings_locator import CampaignSettingsLocator
from pages.creatives.creative_form import DspDashboardCreativeForm
from pages.creatives.creative_list import DspDashboardCreativeList
from configurations import generic_modules
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.navbar.navbar import DashboardNavbar
from utils.page_names_enum import PageNames


def test_regression_rich_media_preview_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    navbar = DashboardNavbar(driver)
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    with open('assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = banner_creative_data['general_information'][
                                                               'title'] + generic_modules.get_random_string(5)

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = campaign_data['name_and_type'][
                                                          'campaign_name'] + generic_modules.get_random_string(5)

    creative_url = config['credential']['url'] + config['creative-creation-page']['creative-creation-url']
    driver.get(creative_url)
    banner_creative_data['general_information'][
        'title'] = "Test Preview Rich Media_" + generic_modules.get_random_string(5)
    # IMPERSONATE DIFFERENT USER BECAUSE WE IN STAGE IF WE UPLOAD A IMAGE IT WILL SHOW AS BROKER IN OTHER STAGE AND
    # WE CANNOT REMOVE THOSE , SO TO HANDLE THIS SCENARIO I IMPLEMENT THIS WAY THAT FOR SPECIFIC WE USE DIFFERENT USER.
    if "dspdi" in config['credential']['url']:
        navbar.impersonate_user('1 Life - Rook Digital')
    elif "dsphv.eskimi.com" in config['credential']['url']:
        navbar.impersonate_user('100 NairaShop NG')
    elif "dspsh.eskimi.com" in config['credential']['url']:
        navbar.impersonate_user('Ada Asia TH - SCB ABACUS')
    elif "-qa-testing" in config['credential']['url']:
        navbar.impersonate_user('102 - Eshio Joseph')
    elif "-stage" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - MSB')
    elif "dspuat" in config['credential']['url']:
        navbar.impersonate_user('102 - Eshio Joseph')
    elif "dspaam" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - Anadolu Bank')
    elif "dspanv" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - Anavarza Bal')
    elif "dspap" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - Luxell')
    elif "dspav" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - MSB')
    elif "dspawc" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - Onur Market')
    elif "dspds" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - Pastavilla')
    elif "dspgb" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - RS Oto Ekspertiz')
    elif "dspep" in config['credential']['url']:
        navbar.impersonate_user('13 Brave - STK')
    elif "dspjv" in config['credential']['url']:
        navbar.impersonate_user('13 Brave -Turkcell')
    elif "dspmg" in config['credential']['url']:
        navbar.impersonate_user('102 - Eshio Joseph')
    elif "dspnj" in config['credential']['url']:
        navbar.impersonate_user('ABA Bank - Reporting')
    elif "dsptp" in config['credential']['url']:
        navbar.impersonate_user('ABA Bank 1')
    else:
        navbar.impersonate_user('102 - Eshio Joseph')

    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath, CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    creative_form_page.click_on_element(CreativeFormLocators.creative_btn_data_qa)
    creative_list_page.click_on_element(CreativeFormLocators.creative_sets_breadcrumb_locator)
    creative_list_page.wait_for_creative_count_to_be_updated()

    sidebar_navigation.navigate_to_page(PageNames.CAMPAIGN_SETTINGS)
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_data['landing_and_creatives']['creative'] = banner_creative_data['general_information']['title']
    campaign_data['name_and_type']['campaign_name'] = 'Automation Preview Rich Media'
    campaign_page.provide_mandatory_field_campaign_data_and_save(campaign_data, "Save")

    assert "Saved successfully." in campaign_settings_page.get_success_message()

    campaign_settings_page.search_and_click_on_campaign_name(campaign_data['name_and_type']['campaign_name'], index=1)
    campaign_settings_page.click_on_element(CampaignSettingsLocator.preview_in_browser_locator)
    campaign_settings_page.switch_to_iframe(CampaignSettingsLocator.iframe_locator)
    campaign_settings_page.wait_for_visibility_of_element(CampaignSettingsLocator.preview_ad_div_locator)
    campaign_settings_page.switch_to_default_content()

    time.sleep(4)
    campaign_page.take_screenshot('desktop_actual_view_screenshot_rich_media.png')
    campaign_page.change_resolution('desktop_actual_view_screenshot_rich_media.png')
    campaign_settings_page.click_on_element(CampaignSettingsLocator.preview_toggle_locator)
    time.sleep(4)
    campaign_page.take_screenshot('mobile_actual_view_screenshot_rich_media.png')
    campaign_page.change_resolution('mobile_actual_view_screenshot_rich_media.png')

    screenshot_folder = 'tests_screenshots'
    view_types = ['desktop', 'mobile']
    threshold = 4.1

    try:
        for view_type in view_types:
            expected_screenshot_filename = f'{view_type}_view_screenshot_rich_media.png'
            actual_screenshot_filename = f'{view_type}_actual_view_screenshot_rich_media.png'
            expected_image_path = os.path.join(screenshot_folder, expected_screenshot_filename)
            expected_image = Image.open(expected_image_path).convert("RGBA")
            actual_image_path = os.path.join(screenshot_folder, actual_screenshot_filename)
            actual_image = Image.open(actual_image_path).convert("RGBA")

            try:
                diff = ImageChops.difference(expected_image, actual_image)
                percentage_diff = (sum(sum(pixel) for pixel in diff.getdata()) / (
                            255.0 * expected_image.width * expected_image.height)) * 100

                if percentage_diff <= threshold:
                    message = f"{view_type.capitalize()} view: Images match! Difference in Percentage: {percentage_diff:.2f}%"
                    print("Pass:", message)
                    assert True, message
                else:
                    message = f"{view_type.capitalize()} view: Images do not match. Difference in Percentage: {percentage_diff:.2f}%"
                    print("Fail:", message)
                    assert False, message
            finally:
                actual_image.close()
    finally:
        for view_type in view_types:
            actual_screenshot_filename = f'{view_type}_actual_view_screenshot_rich_media.png'
            actual_image_path = os.path.join(screenshot_folder, actual_screenshot_filename)
            if os.path.exists(actual_image_path):
                os.remove(actual_image_path)

    campaign_settings_page.click_on_element(CampaignSettingsLocator.preview_platform_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://www.eskimi.com/blog" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_settings_page.click_on_element(CampaignSettingsLocator.preview_ad_gallery_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://www.eskimi.com/gallery" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_settings_page.click_on_element(CampaignSettingsLocator.preview_manual_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://manual.eskimi.com/" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_settings_page.click_on_element(CampaignSettingsLocator.preview_book_demo_url_locator)
    campaign_settings_page.switch_to_new_window()
    assert "https://www.eskimi.com/book-demo" in driver.current_url
    campaign_settings_page.close_the_current_window_and_back_to_previous_window()

    campaign_page.go_back()
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_data['name_and_type']['campaign_name'], index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()

    sidebar_navigation.navigate_to_page(PageNames.CREATIVE_SETS)
    creative_list_page.search_and_action(banner_creative_data['general_information']['title'], "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()
