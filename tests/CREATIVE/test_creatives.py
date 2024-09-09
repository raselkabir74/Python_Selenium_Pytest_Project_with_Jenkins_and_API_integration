import json
import time
import os
from PIL import Image, ImageChops
from configurations import generic_modules
from locators.creative.creative_form_locator import CreativeFormLocators
from locators.creative.creative_list_locator import CreativeListLocators
from pages.base_page import BasePage
from pages.creatives.creative_form import DspDashboardCreativeForm
from pages.creatives.creative_list import DspDashboardCreativeList
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.creatives import CreativesUtils
from utils.page_names_enum import PageNames


def test_dashboard_creative_copy_creative_to_another_user_banner(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open('assets/creatives/creatives_banner_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_file_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        banner_creative_data)
    creative_form_page.provide_info_into_add_creative_file_banner_form(
        banner_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(str(creative_set_id)))
    creative_list_page.click_on_element(
        CreativeFormLocators.copy_to_another_button_data_qa.format(creative_set_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)

    # VERIFY CURRENT USERS CREATIVE CREATIONS WITH LIST AND EDIT PAGE
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_banner_creative_information_from_form_page(
        banner_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        banner_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    # VERIFY COPIED USERS CREATIVE CREATIONS  WITH LIST AND EDIT PAGE
    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(banner_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_banner_creative_information_from_form_page(
        banner_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        banner_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_copy_creative_to_another_user_video(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creatives_ibv_video_data.json') as json_file:
        ibv_video_creative_data = json.load(json_file)
    ibv_video_creative_data['general_information']['title'] = \
        ibv_video_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_ibv_video_grid_data.json') as json_file:
        ibv_video_creative_grid_data = json.load(json_file)
    ibv_video_creative_grid_data['general_information']['title'] = \
        ibv_video_creative_data['general_information'][
            'title']
    # CREATE IBV VIDEO TYPE CREATIVE
    sidebar_navigation.navigate_to_page(PageNames.CREATIVE_SETS)
    creative_list_page.navigate_to_add_creative()
    creative_form_page.provide_info_into_add_creative_set_form(
        ibv_video_creative_data)
    creative_id = creative_form_page.provide_info_into_add_creative_ibv_video_form(
        ibv_video_creative_data)
    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(
        ibv_video_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.copy_to_another_button_data_qa.format(creative_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    # VERIFY CURRENT USERS CREATIVE CREATIONS WITH LIST AND EDIT PAGE
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        ibv_video_creative_grid_data)
    creative_list_page.search_and_action(
        ibv_video_creative_data['general_information']['title'],
        "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_ibv_video_creative_information_from_form_page(
        ibv_video_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        ibv_video_creative_data)
    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        ibv_video_creative_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(ibv_video_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    # VERIFY COPIED USERS CREATIVE CREATIONS  WITH LIST AND EDIT PAGE
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        ibv_video_creative_grid_data)
    creative_list_page.search_and_action(
        ibv_video_creative_data['general_information']['title'],
        "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_ibv_video_creative_information_from_form_page(
        ibv_video_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        ibv_video_creative_data)
    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        ibv_video_creative_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_copy_creative_to_another_user_native(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)

    with open('assets/creatives/creatives_native_data.json') as json_file:
        native_creative_data = json.load(json_file)
    with open(
            'assets/creatives/creatives_native_data_copy_account.json') as json_file:
        native_creative_data_copy_account = json.load(json_file)
    native_creative_data['general_information']['title'] = \
        native_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_native_grid_data.json') as json_file:
        native_creative_data_from_grid = json.load(json_file)
    native_creative_data_from_grid['general_information']['title'] = \
        native_creative_data['general_information'][
            'title']

    # CREATE NATIVE TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        native_creative_data, creatives_format=False)
    creative_id = creative_form_page.provide_info_into_add_creative_native_form(
        native_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(
        native_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.copy_to_another_button_data_qa.format(creative_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)

    # VERIFY CURRENT USERS CREATIVE CREATIONS WITH LIST AND EDIT PAGE
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    if 'http://rtb.local/admin' in driver.current_url:
        native_creative_data_from_grid['general_information']['dimensions'] = \
            pulled_creative_data_from_grid['general_information']['dimensions']
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        native_creative_data_from_grid)
    creative_list_page.search_and_action(
        native_creative_data['general_information']['title'], "Edit")
    base_page.wait_for_visibility_of_element(
        CreativeFormLocators.icon_image_dimension_locator)
    pulled_creative_data_from_gui = creative_form_page.get_native_creative_information_from_form_page(
        native_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        native_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        native_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    # VERIFY COPIED USERS CREATIVE CREATIONS  WITH LIST AND EDIT PAGE
    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(native_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        native_creative_data_from_grid)
    creative_list_page.search_and_action(
        native_creative_data['general_information']['title'], "Edit")
    base_page.wait_for_visibility_of_element(
        CreativeFormLocators.icon_image_dimension_locator)
    pulled_creative_data_from_gui = creative_form_page.get_native_creative_information_from_form_page_for_copy(
        native_creative_data_copy_account)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        native_creative_data_copy_account)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        native_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_copy_creative_to_another_user_engagement(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)

    with open(
            'assets/creatives/creatives_engagement_data.json') as json_file:
        engagement_creative_data = json.load(json_file)
    engagement_creative_data['general_information']['title'] = \
        engagement_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_engagement_grid_data.json') as json_file:
        engagement_creative_data_from_grid = json.load(json_file)
    engagement_creative_data_from_grid['general_information']['title'] = \
        engagement_creative_data['general_information']['title']

    # CREATE ENGAGEMENT TYPE CREATIVE
    sidebar_navigation.navigate_to_page(PageNames.CREATIVE_SETS)
    creative_list_page.navigate_to_add_creative()
    creative_form_page.provide_info_into_add_creative_set_form(
        engagement_creative_data, creatives_format=False)
    creative_id = creative_form_page.provide_info_into_add_creative_engagement_form(engagement_creative_data)
    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(
        engagement_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.copy_to_another_button_data_qa.format(creative_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    # VERIFY CURRENT USERS CREATIVE CREATIONS WITH LIST AND EDIT PAGE
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        engagement_creative_data_from_grid)
    creative_list_page.search_and_action(
        engagement_creative_data['general_information']['title'],
        "Edit")
    base_page.wait_for_visibility_of_element(
        CreativeFormLocators.dimensions_locator)
    pulled_creative_data_from_gui = creative_form_page.get_engagement_creative_information_from_form_page(
        engagement_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        engagement_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        engagement_creative_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    # VERIFY COPIED USERS CREATIVE CREATIONS  WITH LIST AND EDIT PAGE
    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(engagement_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        engagement_creative_data_from_grid)
    creative_list_page.search_and_action(
        engagement_creative_data['general_information']['title'],
        "Edit")
    base_page.wait_for_visibility_of_element(
        CreativeFormLocators.dimensions_locator)
    pulled_creative_data_from_gui = creative_form_page.get_engagement_creative_information_from_form_page(
        engagement_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        engagement_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(engagement_creative_data['general_information']['title'], "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_copy_creative_to_another_user_native_video(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)

    with open('assets/creatives/creatives_native_video_data.json') as json_file:
        native_video_creative_data = json.load(json_file)
    native_video_creative_data['general_information']['title'] = native_video_creative_data['general_information'][
                                                                     'title'] + generic_modules.get_random_string(5)
    with open('assets/creatives/creatives_native_video_grid_data.json') as json_file:
        native_video_creative_data_from_grid = json.load(json_file)
    native_video_creative_data_from_grid['general_information']['title'] = \
        native_video_creative_data['general_information'][
            'title']

    # CREATE NATIVE VIDEO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(native_video_creative_data)
    creative_id = creative_form_page.provide_info_into_add_creative_native_video_form(native_video_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(native_video_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_id))
    creative_list_page.click_on_element(CreativeFormLocators.copy_to_another_button_data_qa.format(creative_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(CreativeFormLocators.confirm_button_locator)
    creative_list_page.search_and_action(native_video_creative_data['general_information']['title'], "Edit")
    base_page.wait_for_visibility_of_element(CreativeFormLocators.icon_image_dimension_locator)
    pulled_creative_data_from_gui = creative_form_page.get_native_video_creative_information_from_form_page(
        native_video_creative_data)
    assert generic_modules.ordered(pulled_creative_data_from_gui) == generic_modules.ordered(
        native_video_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(native_video_creative_data['general_information']['title'], "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    # VERIFY COPIED USERS CREATIVE CREATIONS  WITH LIST AND EDIT PAGE
    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(native_video_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(pulled_creative_data_from_grid) == generic_modules.ordered(
        native_video_creative_data_from_grid)

    creative_list_page.search_and_action(native_video_creative_data['general_information']['title'], "Edit")
    base_page.wait_for_visibility_of_element(CreativeFormLocators.icon_image_dimension_locator)
    pulled_creative_data_from_gui = creative_form_page.get_native_video_creative_information_from_form_page(
        native_video_creative_data)
    assert generic_modules.ordered(pulled_creative_data_from_gui) == generic_modules.ordered(
        native_video_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(native_video_creative_data['general_information']['title'], "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_copy_creative_to_another_user_audio(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open('assets/creatives/creatives_audio_data.json') as json_file:
        audio_creative_data = json.load(json_file)
    audio_creative_data['general_information']['title'] = audio_creative_data['general_information'][
                                                              'title'] + generic_modules.get_random_string(5)
    with open('assets/creatives/creatives_audio_grid_data.json') as json_file:
        audio_creative_data_from_grid = json.load(json_file)
    audio_creative_data_from_grid['general_information']['title'] = \
        audio_creative_data['general_information'][
            'title']

    # CREATE AUDIO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(audio_creative_data)
    creative_id = creative_form_page.provide_info_into_add_creative_audio_form(audio_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(audio_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_id))
    creative_list_page.click_on_element(CreativeFormLocators.copy_to_another_button_data_qa.format(creative_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(CreativeFormLocators.confirm_button_locator)
    creative_list_page.search_and_action(audio_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_audio_creative_information_from_form_page(
        audio_creative_data)
    assert generic_modules.ordered(pulled_creative_data_from_gui) == generic_modules.ordered(
        audio_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(audio_creative_data['general_information']['title'], "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    # VERIFY COPIED USERS CREATIVE CREATIONS WITH LIST AND EDIT PAGE
    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(audio_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid(no_preview=True)
    assert generic_modules.ordered(pulled_creative_data_from_grid) == generic_modules.ordered(
        audio_creative_data_from_grid)

    creative_list_page.search_and_action(audio_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_audio_creative_information_from_form_page(
        audio_creative_data)
    assert generic_modules.ordered(pulled_creative_data_from_gui) == generic_modules.ordered(
        audio_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(audio_creative_data['general_information']['title'], "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_banner_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open('assets/creatives/creatives_banner_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_file_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        banner_creative_data)
    creative_form_page.provide_info_into_add_creative_file_banner_form(
        banner_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            banner_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_video_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open(
            'assets/creatives/creatives_ibv_video_data.json') as json_file:
        ibv_video_creative_data = json.load(json_file)
    ibv_video_creative_data['general_information']['title'] = \
        ibv_video_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_ibv_video_grid_data.json') as json_file:
        ibv_video_creative_grid_data = json.load(json_file)
    ibv_video_creative_grid_data['general_information']['title'] = \
        ibv_video_creative_data['general_information'][
            'title']

    # CREATE IBV VIDEO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        ibv_video_creative_data)
    creative_form_page.provide_info_into_add_creative_ibv_video_form(
        ibv_video_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(
            ibv_video_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.search_and_action(
        ibv_video_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    ibv_video_creative_grid_data['general_information']['title'] = \
        ibv_video_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        ibv_video_creative_grid_data)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            ibv_video_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_native_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open('assets/creatives/creatives_native_data.json') as json_file:
        native_creative_data = json.load(json_file)
    native_creative_data['general_information']['title'] = \
        native_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_native_grid_data.json') as json_file:
        native_creative_data_from_grid = json.load(json_file)
    native_creative_data_from_grid['general_information']['title'] = \
        native_creative_data['general_information'][
            'title']

    # CREATE NATIVE TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        native_creative_data, creatives_format=False)
    creative_form_page.provide_info_into_add_creative_native_form(
        native_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(native_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(native_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.search_and_action(
        native_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    native_creative_data_from_grid['general_information']['title'] = \
        native_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        native_creative_data_from_grid)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            native_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_preserve_banner_type_creative(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    connection = open_database_connection
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open('assets/creatives/creatives_banner_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_file_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        banner_creative_data)
    creative_form_page.provide_info_into_add_creative_file_banner_form(
        banner_creative_data)

    # SELECTING PRESERVE OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.preserve_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    assert "Creative set and all creatives marked as reserved" in \
           creative_list_page.get_element_text(CreativeListLocators.info_message_data_qa)
    preserve_status = 1
    creative_title = banner_creative_data['general_information']['title']
    assert preserve_status == CreativesUtils.pull_creative_preserve_status_from_db(creative_title, connection)

    # SELECTING UNPRESERVE OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.unpreserve_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    assert "Creative set and all creatives marked as unreserved" in \
           creative_list_page.get_element_text(CreativeListLocators.info_message_data_qa)
    unpreserve_status = 0
    assert unpreserve_status == CreativesUtils.pull_creative_preserve_status_from_db(creative_title, connection)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_engagement_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open('assets/creatives/creatives_engagement_data.json') as json_file:
        engagement_creative_data = json.load(json_file)
    engagement_creative_data['general_information']['title'] = \
        engagement_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_engagement_grid_data.json') as json_file:
        engagement_creative_data_from_grid = json.load(json_file)
    engagement_creative_data_from_grid['general_information']['title'] = \
        engagement_creative_data['general_information'][
            'title']

    # CREATE ENGAGEMENT TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        engagement_creative_data, creatives_format=False)
    creative_form_page.provide_info_into_add_creative_engagement_form(engagement_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.search_and_action(
        engagement_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(
            engagement_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(
            engagement_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    engagement_creative_data_from_grid['general_information']['title'] = \
        engagement_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        engagement_creative_data_from_grid)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            engagement_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_audio_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open('assets/creatives/creatives_audio_data.json') as json_file:
        audio_creative_data = json.load(json_file)
    audio_creative_data['general_information']['title'] = \
        audio_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_audio_grid_data.json') as json_file:
        audio_creative_grid_data = json.load(json_file)
    audio_creative_grid_data['general_information']['title'] = \
        audio_creative_data['general_information'][
            'title']

    # CREATE AUDIO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        audio_creative_data)
    creative_form_page.provide_info_into_add_creative_audio_form(
        audio_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(audio_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.search_and_action(
        audio_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid(no_preview=True)
    audio_creative_grid_data['general_information']['title'] = \
        audio_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        audio_creative_grid_data)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            audio_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_carousel_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open(
            'assets/creatives/creatives_carousel_data.json') as json_file:
        carousel_creative_data = json.load(json_file)
    carousel_creative_data['general_information']['title'] = \
        carousel_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_carousel_grid_data.json') as json_file:
        carousel_creative_data_from_grid = json.load(json_file)
    carousel_creative_data_from_grid['general_information']['title'] = \
        carousel_creative_data['general_information']['title']

    # CREATE CAROUSEL TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        carousel_creative_data, creatives_format=False)
    creative_form_page.provide_info_into_add_creative_carousel_form(
        carousel_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.search_and_action(
        carousel_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(
            carousel_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(
            carousel_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    carousel_creative_data_from_grid['general_information']['title'] = \
        carousel_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        carousel_creative_data_from_grid)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            carousel_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_native_video_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open(
            'assets/creatives/creatives_native_video_data.json') as json_file:
        native_video_creative_data = json.load(json_file)
    native_video_creative_data['general_information']['title'] = \
        native_video_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_native_video_grid_data.json') as json_file:
        native_video_creative_data_from_grid = json.load(json_file)
    native_video_creative_data_from_grid['general_information']['title'] = \
        native_video_creative_data['general_information'][
            'title']

    # CREATE NATIVE VIDEO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        native_video_creative_data)
    creative_form_page.provide_info_into_add_creative_native_video_form(
        native_video_creative_data)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.search_and_action(
        native_video_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(
            native_video_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(
            native_video_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    # Added time.sleep because of this issue https://eskimidev.atlassian.net/browse/RTB-8149
    if "qa-testing" in config['credential']['url']:
        time.sleep(60)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    native_video_creative_data_from_grid['general_information']['title'] = \
        native_video_creative_data['general_information'][
            'title'] + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        native_video_creative_data_from_grid)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            native_video_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_duplicate_rich_media_banner_type_creative_new_flow(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_rich_media_new_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER RICH MEDIA TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
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
        navbar.impersonate_user('AutomationAgencyClientUser')
    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath, CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    creative_form_page.click_on_element(CreativeFormLocators.creative_btn_data_qa)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    if 'http://rtb.local/admin' in driver.current_url:
        creative_list_page.wait_for_element_to_be_invisible(CreativeFormLocators.loading_spinner_locator, time_out=6000)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.wait_for_creative_count_to_be_updated()
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.duplicate_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_title)
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data_from_grid['general_information'][
            'title'] + '_Shake & brake_320x480' + ' (1)'
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)

    # CREATIVE CLEAN UP
    for _ in range(2):
        creative_list_page.search_and_action(
            banner_creative_data['general_information']['title'],
            "Delete",
            force_reload=True)
        assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_preserve_rich_media_banner_type_creative_new_flow(login_by_user_type,
                                                                              open_database_connection):
    config, driver, redis_connection = login_by_user_type
    connection = open_database_connection
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_rich_media_new_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER RICH MEDIA TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
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
        navbar.impersonate_user('AutomationAgencyClientUser')
    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath, CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    creative_form_page.click_on_element(CreativeFormLocators.creative_btn_data_qa)

    # SELECTING PRESERVE OPTION FROM CREATIVE LIST PAGE
    if 'http://rtb.local/admin' in driver.current_url:
        creative_list_page.wait_for_element_to_be_invisible(CreativeFormLocators.loading_spinner_locator, time_out=6000)
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_set_title)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_set_id = creative_list_page.get_attribute_value(
        CreativeListLocators.specific_creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_set_id = (creative_set_id.split("id="))[1]
    creative_list_page.wait_for_creative_count_to_be_updated()
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.preserve_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    assert "Creative set and all creatives marked as reserved" in \
           creative_list_page.get_element_text(CreativeListLocators.info_message_data_qa)
    preserve_status = 1
    creative_title = banner_creative_data_from_grid['general_information']['title'] + '_Shake & brake_320x480'
    assert preserve_status == CreativesUtils.pull_creative_preserve_status_from_db(creative_title, connection)

    # SELECTING UNPRESERVE OPTION FROM CREATIVE LIST PAGE
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.unpreserve_button_data_qa.format(creative_set_id))
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)
    assert "Creative set and all creatives marked as unreserved" in \
           creative_list_page.get_element_text(CreativeListLocators.info_message_data_qa)
    unpreserve_status = 0
    assert unpreserve_status == CreativesUtils.pull_creative_preserve_status_from_db(creative_title, connection)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_copy_rich_media_banner_type_creative_new_flow(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_rich_media_new_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER RICH MEDIA TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
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
        navbar.impersonate_user('AutomationAgencyClientUser')
    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    creative_form_page.click_on_element(CreativeFormLocators.creative_btn_data_qa)

    # SELECTING COPY OPTION FROM CREATIVE LIST PAGE
    if 'http://rtb.local/admin' in driver.current_url:
        creative_list_page.wait_for_element_to_be_invisible(CreativeFormLocators.loading_spinner_locator, time_out=6000)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'])
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_id = creative_list_page.get_attribute_value(
        CreativeListLocators.creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_id = creative_id.split("/")[-1]
    creative_list_page.click_on_element(
        CreativeFormLocators.creative_list_three_dot_data_qa.format(str(creative_id)))
    creative_list_page.click_on_element(
        CreativeFormLocators.copy_to_another_button_data_qa.format(creative_id))
    creative_list_page.select_from_modal('AutomationClientUser')
    creative_list_page.click_on_element(
        CreativeFormLocators.confirm_button_locator)

    # VERIFY CURRENT USERS CREATIVE CREATIONS WITH LIST AND EDIT PAGE
    creative_list_page.wait_for_status_to_be_updated()
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data_from_grid['general_information'][
            'title'] + '_Shake & brake_320x480'
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_rich_media_banner_creative_information_from_form_page(
        banner_creative_data, creative_id)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        banner_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()

    # VERIFY COPIED USERS CREATIVE CREATIONS  WITH LIST AND EDIT PAGE
    navbar.impersonate_user('AutomationClientUser')
    creative_list_page.search_and_action(banner_creative_data['general_information']['title'])
    creative_list_page.click_on_element(CreativeFormLocators.list_first_iteam_locator)
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    copied_creative_id = creative_list_page.get_attribute_value(
        CreativeListLocators.creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    copied_creative_id = copied_creative_id.split("/")[-1]
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_rich_media_banner_creative_information_from_form_page(
        banner_creative_data, copied_creative_id)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        banner_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_dashboard_creative_rich_media_banner_type_multiple_creative_new_flow(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_rich_media_new_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER RICH MEDIA TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
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
        navbar.impersonate_user('AutomationAgencyClientUser')
    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    # 2ND CREATIVE SETUP
    creative_form_page.click_on_element(CreativeFormLocators.multi_rm_creative_add_btn)
    creative_form_page.click_on_element(CreativeFormLocators.rm_2nd_size_data_qa)
    creative_form_page.click_on_element(CreativeFormLocators.rm_size_dimension_data_qa)
    creative_form_page.click_on_element(CreativeFormLocators.select_2nd_template_data_qa)
    creative_form_page.click_on_element(CreativeFormLocators.select_pixel_page_template_checkbox_data_qa)
    creative_form_page.click_on_element(CreativeFormLocators.template_btn_data_qa)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_2nd_rm)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_2nd_rm_1)
    creative_form_page.click_on_element(CreativeFormLocators.creative_btn_data_qa)

    # DATA VERIFICATION
    if 'http://rtb.local/admin' in driver.current_url:
        creative_list_page.wait_for_element_to_be_invisible(CreativeFormLocators.loading_spinner_locator,
                                                            time_out=6000)
    creative_list_page.wait_for_presence_of_element(
        CreativeListLocators.creative_id_locator.format(banner_creative_data['general_information']['title']),
        locator_initialization=True, time_out=60)
    creative_id = creative_list_page.get_attribute_value(
        CreativeListLocators.creative_id_locator.format(banner_creative_data['general_information']['title']),
        attribute_name=creative_list_page.href_tag, locator_initialization=True)
    creative_id = creative_id.split("/")[-1]
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_rich_media_banner_creative_information_from_form_page(
        banner_creative_data, creative_id)
    print("pulled_campaign_data_gui",
          generic_modules.ordered(pulled_creative_data_from_gui))
    print("campaign_data           ",
          generic_modules.ordered(banner_creative_data))
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        banner_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_rich_media_banner_creative_sets(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_rich_media_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER RICH MEDIA TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
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
        navbar.impersonate_user('AutomationAgencyClientUser')
    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath, CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    creative_form_page.click_on_element(CreativeFormLocators.creative_btn_data_qa)
    # DATA VERIFICATION
    if 'http://rtb.local/admin' in driver.current_url:
        creative_list_page.wait_for_element_to_be_invisible(CreativeFormLocators.loading_spinner_locator,
                                                            time_out=6000)
    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete")
    assert "Creative deleted successfully" in creative_list_page.get_success_message()
    creative_form_page.click_on_element(CreativeFormLocators.creative_sets_breadcrumb_locator)
    # CREATIVE SET CLEAN UP
    creative_list_page.search_and_action(banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_rich_media_banner_creation_actions(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    navbar = DashboardNavbar(driver)

    with open(
            'assets/creatives/creative_rm_banner_new_flow_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)

    # CREATE BANNER RICH MEDIA TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
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
    # CREATIVE SET CREATION
    creative_form_page.provide_info_into_add_creative_set_form(banner_creative_data)
    creative_form_page.wait_for_presence_of_element(CreativeFormLocators.select_template_data_qa)
    # The assertion is failing because the message appears only briefly, making it difficult for the test to catch it.
    # The message will be moved to the new creative page; the task number is not known yet.
    # assert "Creative set created successfully" == creative_form_page.get_element_text(
    #     CreativeFormLocators.creative_set_message_locator)
    creative_form_page.click_on_element(CreativeFormLocators.creative_sets_breadcrumb_locator)
    creative_sets_titles_list = creative_list_page.get_text_or_value_from_list(
        CreativeListLocators.creative_sets_titles_list_locator)
    assert banner_creative_data['general_information']['title'] in creative_sets_titles_list

    # NEW CREATIVE CREATION
    creative_list_page.add_creative_into_creative_set(banner_creative_data)
    creative_form_page.provide_info_into_add_creative_rm_banner_form_new()
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath, CreativeFormLocators.target_xpath)
    creative_form_page.drag_and_drop_for_dashboard(CreativeFormLocators.source_xpath,
                                                   CreativeFormLocators.target_xpath_1)
    assert creative_form_page.is_element_displayed(CreativeFormLocators.template_preview_data_qa)

    # SCREENSHOTS VERIFICATION
    creative_form_page.click_on_element(CreativeFormLocators.template_preview_data_qa)
    time.sleep(2)
    creative_form_page.take_screenshot(
        'mobile_actual_view_shake&brake_template_preview_screenshot.png')
    creative_form_page.change_resolution(
        'mobile_actual_view_shake&brake_template_preview_screenshot.png')
    creative_form_page.click_on_element(CreativeFormLocators.desktop_radio_btn_data_qa)
    time.sleep(2)
    creative_form_page.take_screenshot(
        'desktop_actual_view_shake&brake_template_preview_screenshot.png')
    creative_form_page.change_resolution(
        'desktop_actual_view_shake&brake_template_preview_screenshot.png')
    creative_form_page.click_on_element(CreativeFormLocators.real_size_btn_data_qa)
    time.sleep(2)
    creative_form_page.take_screenshot(
        'real_size_actual_view_shake&brake_template_preview_screenshot.png')
    creative_form_page.change_resolution(
        'real_size_actual_view_shake&brake_template_preview_screenshot.png')

    screenshot_folder = 'tests_screenshots'
    view_types = ['mobile', 'desktop', 'real_size']
    threshold = 1.65

    try:
        for view_type in view_types:
            expected_screenshot_filename = f'{view_type}_view_shake&brake_template_preview_screenshot.png'
            actual_screenshot_filename = f'{view_type}_actual_view_shake&brake_template_preview_screenshot.png'
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
            actual_screenshot_filename = f'{view_type}_actual_view_shake&brake_template_preview_screenshot.png'
            actual_image_path = os.path.join(screenshot_folder, actual_screenshot_filename)
            if os.path.exists(actual_image_path):
                os.remove(actual_image_path)

    # TEMPLATE REMOVAL
    creative_form_page.click_on_element(CreativeFormLocators.remove_template_btn_data_qa)
    creative_form_page.click_on_element(CreativeFormLocators.remove_btn_data_qa)
    assert False is creative_form_page.is_element_present(CreativeFormLocators.template_preview_data_qa)
    assert False is creative_form_page.is_element_present(CreativeFormLocators.target_xpath,
                                                          locator_initialization=True)
    assert False is creative_form_page.is_element_present(CreativeFormLocators.target_xpath_1,
                                                          locator_initialization=True)
    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


