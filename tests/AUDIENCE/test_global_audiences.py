import json
import time

from configurations import generic_modules
from locators.audience.audience_list_locator import AudienceListLocators
from locators.audience.audience_form_locator import AudienceFormLocators
from pages.audience.audience_form import DspDashboardAudienceForm
from pages.audience.audience_list import DspDashboardAudienceList
from pages.base_page import BasePage
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.compare import CompareUtils as CompareUtil
from utils.page_names_enum import PageNames


def test_dashboard_audience_add_global_audiences(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    audiences_list_page = DspDashboardAudienceList(driver)
    audiences_form_page = DspDashboardAudienceForm(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    base_page = BasePage(driver)

    # [START] CREATION OF BEHAVIORAL USER INTERESTS TYPE AUDIENCE
    # PROVIDED AUDIENCE DATA IN GUI
    generic_modules.step_printer("BEHAVIORAL USER INTERESTS TYPE AUDIENCE")
    with open(
            'assets/audiences/audiences_behavioral_user_interests_data.json') as json_file:
        audiences_behavioral_user_interests_data = json.load(json_file)
    audiences_behavioral_user_interests_data['general_information'][
        'audience_name'] = \
        audiences_behavioral_user_interests_data[
            'general_information'][
            'audience_name'] + generic_modules.get_random_string(5)
    # AUDIENCE CREATION
    audiences_url = (config['credential']['url'] +
                     config['global-audience-creation-page']['global-audience-creation-url'])
    sidebar_navigation.navigate_to_page(PageNames.GLOBAL_AUDIENCES)
    audiences_list_page.navigate_to_add_audience()
    audiences_form_page.provide_behavioral_user_interest_audience_data_and_save(
        audiences_behavioral_user_interests_data)
    assert "Audience created successfully!" in audiences_list_page.get_success_message()
    # DATA VERIFICATION
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.dmp_audience_groups_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_behavioral_user_interests_data[
            'general_information'][
            'audience_name'], "Edit")
    checkbox_status = audiences_form_page.wait_until_checkbox_selected_with_retry(
        AudienceFormLocators.autos_vehicles_checkbox_locator)
    pulled_audiences_behavioral_user_interests_data_gui = \
        audiences_form_page.get_behavioral_user_interest_audience_information(
            audiences_behavioral_user_interests_data)
    # Temporarily added this if condition due to issue https://eskimidev.atlassian.net/browse/RTB-9624
    if checkbox_status == '':
        audiences_behavioral_user_interests_data['general_information']['verticals'] = ''
    assert pulled_audiences_behavioral_user_interests_data_gui == audiences_behavioral_user_interests_data
    audiences_form_page.click_on_element(
        AudienceFormLocators.cancel_button_locator)
    # AUDIENCE CLEAN UP (BEHAVIORAL USER INTERESTS)
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.dmp_audience_groups_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_behavioral_user_interests_data[
            'general_information'][
            'audience_name'],
        "Delete")
    assert "Successfully deleted 1 audiences" in audiences_list_page.get_success_message()
    # [END] CREATION OF BEHAVIORAL USER INTERESTS TYPE AUDIENCE

    # [START] CREATION OF RETARGETING (APPS/SITES VISITORS) TYPE AUDIENCE
    # PROVIDED AUDIENCE DATA IN GUI
    generic_modules.step_printer(
        "RETARGETING (APPS/SITES VISITORS) TYPE AUDIENCE")
    with open(
            'assets/audiences/audiences_retargeting_apps_sites_visitors_data.json') as json_file:
        audiences_retargeting_apps_sites_visitors_data = json.load(
            json_file)
    audiences_retargeting_apps_sites_visitors_data['general_information'][
        'audience_name'] = \
        audiences_retargeting_apps_sites_visitors_data[
            'general_information'][
            'audience_name'] + generic_modules.get_random_string(5)
    # AUDIENCE CREATION
    driver.get(audiences_url)
    audiences_form_page.provide_retargeting_apps_sites_visitors_audience_data_and_save(
        audiences_retargeting_apps_sites_visitors_data,
        upload_csv=True)
    assert "Audience created successfully!" in audiences_list_page.get_success_message()
    # DATA VERIFICATION
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.dmp_audience_groups_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_retargeting_apps_sites_visitors_data[
            'general_information'][
            'audience_name'], "Edit")
    pulled_audiences_retargeting_apps_sites_visitors_data = \
        audiences_form_page.get_retargeting_apps_sites_visitors_audience_information()
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_audiences_retargeting_apps_sites_visitors_data,
        audiences_retargeting_apps_sites_visitors_data)
    # AUDIENCE CLEAN UP (RETARGETING (APPS/SITES VISITORS))
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.dmp_audience_groups_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_retargeting_apps_sites_visitors_data[
            'general_information'][
            'audience_name'],
        "Delete")
    assert "Successfully deleted 1 audiences" in audiences_list_page.get_success_message()
    # [END] CREATION OF RETARGETING (APPS/SITES VISITORS) TYPE AUDIENCE

    # [START] CREATION OF RETARGETING (SITE FIRST PARTY) TYPE AUDIENCE
    # PROVIDED AUDIENCE DATA IN GUI
    generic_modules.step_printer(
        "RETARGETING (SITE FIRST PARTY) TYPE AUDIENCE")
    with open(
            'assets/audiences/audiences_retargeting_site_first_party_data.json') as json_file:
        audiences_retargeting_site_first_party_data = json.load(
            json_file)
    audiences_retargeting_site_first_party_data['general_information'][
        'audience_name'] = \
        audiences_retargeting_site_first_party_data[
            'general_information'][
            'audience_name'] + generic_modules.get_random_string(5)
    # AUDIENCE CREATION
    driver.get(audiences_url)
    audiences_form_page.provide_retargeting_site_first_party_audience_data_and_save(
        audiences_retargeting_site_first_party_data)
    assert "Audience created successfully!" in audiences_list_page.get_success_message()
    # DATA VERIFICATION
    time.sleep(2)
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.first_party_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_retargeting_site_first_party_data[
            'general_information'][
            'audience_name'], "Edit", tab_id=2)
    audiences_retargeting_site_first_party_gui_data = \
        audiences_form_page.get_retargeting_site_first_party_audience_information()
    remove_if_url_contains = \
        audiences_retargeting_site_first_party_gui_data[
            'general_information'][
            'remove_if_url_contains'].split('×')
    audiences_retargeting_site_first_party_gui_data['general_information'][
        'remove_if_url_contains'] = \
        remove_if_url_contains[1]
    assert "All data verification is successful" == CompareUtil.verify_data(
        audiences_retargeting_site_first_party_gui_data,
        audiences_retargeting_site_first_party_data)
    # AUDIENCE CLEAN UP (RETARGETING (GEOLOCATION))
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.first_party_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_retargeting_site_first_party_data[
            'general_information'][
            'audience_name'],
        "Delete", tab_id=2)
    assert "Successfully deleted 1 audiences" in audiences_list_page.get_success_message()
    # [END] CREATION OF RETARGETING (SITE FIRST PARTY) TYPE AUDIENCE

    # [START] CREATION OF USER IDS LIST TYPE AUDIENCE
    # PROVIDED AUDIENCE DATA IN GUI
    generic_modules.step_printer("USER IDS LIST TYPE AUDIENCE")
    with open(
            'assets/audiences/audiences_user_ids_list_data.json') as json_file:
        audiences_user_ids_list_data = json.load(json_file)
    audiences_user_ids_list_data['general_information']['audience_name'] = \
        audiences_user_ids_list_data['general_information'][
            'audience_name'] + generic_modules.get_random_string(5)
    # AUDIENCE CREATION
    driver.get(audiences_url)
    audiences_form_page.provide_user_ids_list_audience_data_and_save(
        audiences_user_ids_list_data)
    assert "Audience created successfully!" in audiences_list_page.get_success_message()
    # DATA VERIFICATION
    time.sleep(2)
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.first_party_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_user_ids_list_data['general_information'][
            'audience_name'],
        "Edit", tab_id=2)
    audiences_user_ids_list_gui_data = \
        audiences_form_page.get_user_ids_list_audience_information()
    assert "All data verification is successful" == CompareUtil.verify_data(
        audiences_user_ids_list_gui_data, audiences_user_ids_list_data)
    # AUDIENCE CLEAN UP (USER IDS LIST)
    base_page.click_on_specific_tab(tab_name_or_data_qa=AudienceListLocators.first_party_tab_data_qa)
    audiences_list_page.search_and_action_global_audience(
        audiences_user_ids_list_data['general_information'][
            'audience_name'],
        "Delete", tab_id=2)
    assert "Successfully deleted 1 audiences" in audiences_list_page.get_success_message()
    # [END] CREATION OF USER IDS LIST TYPE AUDIENCE
