import json

from configurations import generic_modules
from locators.creative.creative_form_locator import CreativeFormLocators
from locators.creative.creative_list_locator import CreativeListLocators
from pages.base_page import BasePage
from pages.creatives.creative_form import DspDashboardCreativeForm
from pages.creatives.creative_list import DspDashboardCreativeList
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_regression_add_banner_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

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
    sidebar_navigation.navigate_to_page(PageNames.CREATIVE_SETS)
    creative_list_page.navigate_to_add_creative()
    creative_form_page.provide_info_into_add_creative_set_form(
        banner_creative_data)
    creative_form_page.provide_info_into_add_creative_file_banner_form(
        banner_creative_data)

    # DATA VERIFICATION
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


def test_regression_add_native_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    base_page = BasePage(driver)

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

    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
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


def test_regression_add_native_video_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
    base_page = BasePage(driver)

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
    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        native_video_creative_data_from_grid)

    creative_list_page.search_and_action(
        native_video_creative_data['general_information']['title'],
        "Edit")
    base_page.wait_for_visibility_of_element(
        CreativeFormLocators.icon_image_dimension_locator)
    pulled_creative_data_from_gui = creative_form_page.get_native_video_creative_information_from_form_page(
        native_video_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        native_video_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        native_video_creative_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_regression_add_engagement_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)
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
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        engagement_creative_data, creatives_format=False)
    creative_form_page.provide_info_into_add_creative_engagement_form(engagement_creative_data)

    # DATA VERIFICATION
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


def test_regression_add_carousel_type_creative(login_by_user_type):
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

    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        carousel_creative_data_from_grid)
    creative_list_page.search_and_action(
        carousel_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_carousel_creative_information_from_form_page(
        carousel_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        carousel_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        carousel_creative_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_regression_add_ibv_video_type_creative(login_by_user_type):
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

    # DATA VERIFICATION
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


def test_regression_add_vast_ibv_video_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open(
            'assets/creatives/creatives_vast_ibv_video_data.json') as json_file:
        vast_ibv_video_creative_data = json.load(json_file)
    vast_ibv_video_creative_data['general_information']['title'] = \
        vast_ibv_video_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    creative_to_delete = \
        vast_ibv_video_creative_data['general_information'][
            'title']
    with open(
            'assets/creatives/creatives_vast_ibv_video_grid_data.json') as json_file:
        vast_ibv_video_creative_grid_data = json.load(json_file)
    with open(
            'assets/creatives/creatives_ibv_video_data.json') as json_file:
        ibv_video_creative_data = json.load(json_file)
    ibv_video_creative_data['general_information']['title'] = \
        vast_ibv_video_creative_data['general_information'][
            'title'] + " (IBV)"
    vast_ibv_video_creative_grid_data['general_information_for_vast'][
        'title'] = \
        vast_ibv_video_creative_data['general_information'][
            'title'] + " (VAST)"
    vast_ibv_video_creative_grid_data['general_information_for_ibv'][
        'title'] = \
        vast_ibv_video_creative_data['general_information'][
            'title'] + " (IBV)"

    # CREATE VAST + IBV VIDEO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        vast_ibv_video_creative_data)
    creative_form_page.provide_info_into_add_creative_vast_ibv_video_form(
        vast_ibv_video_creative_data)

    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    creative_list_page.wait_for_status_to_be_updated(row_number="2")
    creative_list_page.search_and_action(
        vast_ibv_video_creative_data['general_information'][
            'title'] + " (VAST)")
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid(
        no_preview=True)
    assert generic_modules.ordered(pulled_creative_data_from_grid[
                                       'general_information']) == generic_modules.ordered(
        vast_ibv_video_creative_grid_data[
            'general_information_for_vast'])
    creative_list_page.search_and_action(
        vast_ibv_video_creative_data['general_information'][
            'title'] + " (IBV)")
    pulled_creative_data_from_grid_2 = creative_list_page.get_creative_information_from_grid()
    assert generic_modules.ordered(pulled_creative_data_from_grid_2[
                                       'general_information']) == generic_modules.ordered(
        vast_ibv_video_creative_grid_data[
            'general_information_for_ibv'])

    driver.refresh()
    creative_list_page.search_and_action(
        vast_ibv_video_creative_grid_data[
            'general_information_for_vast'][
            'title'],
        "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_vast_video_creative_information_from_form_page(
        vast_ibv_video_creative_data)
    vast_ibv_video_creative_data['general_information']['title'] = \
        vast_ibv_video_creative_data['general_information'][
            'title'] + " (VAST)"
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        vast_ibv_video_creative_data)

    creative_list_page.search_and_action(
        vast_ibv_video_creative_grid_data[
            'general_information_for_ibv'][
            'title'],
        "Edit")
    pulled_creative_data_from_gui_2 = creative_form_page.get_ibv_video_creative_information_from_form_page(
        ibv_video_creative_data)
    ibv_video_creative_data['general_information'][
        'playback_checkbox_status'] = ''
    assert generic_modules.ordered(
        pulled_creative_data_from_gui_2) == generic_modules.ordered(
        ibv_video_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(creative_to_delete, "Delete",
                                         force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_regression_add_vast_video_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open(
            'assets/creatives/creatives_vast_video_data.json') as json_file:
        vast_video_creative_data = json.load(json_file)
    vast_video_creative_data['general_information']['title'] = \
        vast_video_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_vast_video_grid_data.json') as json_file:
        vast_video_creative_grid_data = json.load(json_file)
    vast_video_creative_grid_data['general_information']['title'] = \
        vast_video_creative_data['general_information'][
            'title']

    # CREATE VAST VIDEO TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        vast_video_creative_data)
    creative_form_page.provide_info_into_add_creative_vast_video_form(
        vast_video_creative_data)

    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid(
        no_preview=True)
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        vast_video_creative_grid_data)
    creative_list_page.search_and_action(
        vast_video_creative_data['general_information']['title'],
        "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_vast_video_creative_information_from_form_page(
        vast_video_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        vast_video_creative_data)

    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        vast_video_creative_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_regression_add_audio_creative(login_by_user_type):
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
    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid(
        no_preview=True)
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        audio_creative_grid_data)
    creative_list_page.search_and_action(
        audio_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_audio_creative_information_from_form_page(
        audio_creative_data)
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        audio_creative_data)
    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        audio_creative_grid_data['general_information']['title'],
        "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_regression_add_javascript_tag_banner_type_creative(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    creative_form_page = DspDashboardCreativeForm(driver)
    creative_list_page = DspDashboardCreativeList(driver)

    with open(
            'assets/creatives/creative_javascript_tag_banner_data.json') as json_file:
        banner_creative_data = json.load(json_file)
    banner_creative_data['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title'] + generic_modules.get_random_string(5)
    with open(
            'assets/creatives/creatives_javascript_tag_banner_grid_data.json') as json_file:
        banner_creative_data_from_grid = json.load(json_file)
    banner_creative_data_from_grid['general_information']['title'] = \
        banner_creative_data['general_information'][
            'title']

    # CREATE BANNER JAVASCRIPT TAG TYPE CREATIVE
    creative_url = (config['credential']['url']
                    + config['creative-creation-page']['creative-creation-url'])
    driver.get(creative_url)
    creative_form_page.provide_info_into_add_creative_set_form(
        banner_creative_data)
    creative_form_page.provide_info_into_add_creative_javascript_tag_banner_form(
        banner_creative_data)

    # DATA VERIFICATION
    creative_list_page.wait_for_status_to_be_updated()
    pulled_creative_data_from_grid = creative_list_page.get_creative_information_from_grid()
    banner_creative_data_from_grid['general_information'][
        'title'] = creative_list_page.get_value_from_specific_grid_column(
        CreativeListLocators.creatives_table_wrapper_div_id,
        CreativeListLocators.title_column, a_tag=True,
        row_number="1")
    if 'http://rtb.local/admin' in driver.current_url:
        banner_creative_data_from_grid['general_information']['preview'] = \
            pulled_creative_data_from_grid['general_information']['preview']
    assert generic_modules.ordered(
        pulled_creative_data_from_grid) == generic_modules.ordered(
        banner_creative_data_from_grid)
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Edit")
    pulled_creative_data_from_gui = creative_form_page.get_javascript_tag_banner_creative_information_from_form_page(
        banner_creative_data)
    banner_creative_data['general_information'][
        'title'] = creative_form_page.get_text_using_tag_attribute(
        creative_form_page.input_tag,
        creative_form_page.name_attribute,
        CreativeFormLocators.title_name)
    print(banner_creative_data['general_information']['title'])
    print("pulled_campaign_data_gui",
          generic_modules.ordered(pulled_creative_data_from_gui))
    print("campaign_data           ",
          generic_modules.ordered(banner_creative_data))
    assert generic_modules.ordered(
        pulled_creative_data_from_gui) == generic_modules.ordered(
        banner_creative_data)
    banner_creative_data['general_information'][
        'title'] = "automation_ui_testing_"
    # CREATIVE CLEAN UP
    creative_list_page.search_and_action(
        banner_creative_data['general_information']['title'], "Delete",
        force_reload=True)
    assert "Creative set deleted successfully" in creative_list_page.get_success_message()


def test_regression_add_rich_media_banner_type_creative_new_flow(login_by_user_type):
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
        creative_list_page.wait_for_element_to_be_invisible(CreativeFormLocators.loading_spinner_locator, time_out=6000)
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
