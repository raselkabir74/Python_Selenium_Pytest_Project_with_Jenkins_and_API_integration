import json
import time

from configurations import generic_modules
from locators.all_campaigns.all_campaign_locators import AllCampaignFormLocators
from pages.all_campaigns.all_campaigns_form import DashboardAllCampaignForm
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.page_names_enum import PageNames
from utils.compare import CompareUtils


def test_regression_all_campaigns(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)

    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    statuses = ['Pending', 'Live', 'Stopped', 'Daily Cap', 'Budget Limit',
                'Ready', 'Expired', 'Rejected', 'Deleted',
                'Draft']
    creative_types = ['Banner', 'Native', 'Video', 'Native video',
                      'Engagement',
                      'Carousel', 'Audio']
    expected_url_functions = ['optimisation', 'reporting', 'acampaigns', 'acampaigns',
                              'deletePending', '1']
    # Enabling, to verify if RTB-8823 fixed
    assert all_campaign_form.all_statuses_verification(statuses)
    all_campaign_form.clear_all()
    assert all_campaign_form.user_filter_verification(config,
                                                      AllCampaignFormLocators.user_option)
    all_campaign_form.clear_all()
    assert all_campaign_form.country_filter_verification(AllCampaignFormLocators.country_option)
    all_campaign_form.clear_all()
    assert all_campaign_form.all_creative_type_verification(creative_types)
    all_campaign_form.clear_all()
    assert all_campaign_form.last_approved_by_verification(
        'Eskimi - Arunas B.')
    all_campaign_form.clear_all()
    assert all_campaign_form.search_verification('Video Events Creative')
    all_campaign_form.clear_all()
    pulled_url_functions = all_campaign_form.verify_three_dot_options(
        'AutomationAdminUser')
    assert 'All data verification is successful' == CompareUtils.verify_data(
        pulled_url_functions,
        expected_url_functions)
    all_campaign_form.clear_all()
    generic_modules.step_info(
        "[START - RTB-7991] "
        "Validate filter options are working properly in the All Campaigns page individually")
    all_campaign_form.change_status_filter(
        AllCampaignFormLocators.status_live_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    all_campaign_form.select_dropdown_value(AllCampaignFormLocators.rows_per_page_label,
                                            AllCampaignFormLocators.hundred_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    assert "Live" == all_campaign_form.get_text_or_value_from_list(
        AllCampaignFormLocators.all_campaign_list_status_locator,
        AllCampaignFormLocators.status_live_option)
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.change_user_filter(AllCampaignFormLocators.user_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator,
                                            wait_for_loading_spinner_to_start=5)
    assert "AutomationAdminUser" == all_campaign_form.get_text_or_value_from_list(
        AllCampaignFormLocators.all_campaign_list_user_locator,
        AllCampaignFormLocators.user_option)
    all_campaign_form.clear_all()
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.change_country_filter(AllCampaignFormLocators.country_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator,
                                            wait_for_loading_spinner_to_start=5)
    all_campaign_form.select_dropdown_value(AllCampaignFormLocators.rows_per_page_label,
                                            AllCampaignFormLocators.hundred_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator,
                                            wait_for_loading_spinner_to_start=10)
    time.sleep(all_campaign_form.TWO_SEC_DELAY)
    assert "Bangladesh" == all_campaign_form.get_text_or_value_from_list(
        AllCampaignFormLocators.all_campaign_list_country_locator,
        AllCampaignFormLocators.country_option, attribute_name=all_campaign_form.title_attribute)
    all_campaign_form.clear_all()
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.change_creative_type_filter(AllCampaignFormLocators.creative_type_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator,
                                            wait_for_loading_spinner_to_start=5)
    all_campaign_form.select_dropdown_value(AllCampaignFormLocators.rows_per_page_label,
                                            AllCampaignFormLocators.hundred_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator,
                                            wait_for_loading_spinner_to_start=10)
    time.sleep(all_campaign_form.TWO_SEC_DELAY)
    assert "Banner" == all_campaign_form.get_text_or_value_from_list(
        AllCampaignFormLocators.all_campaign_list_creative_type_locator,
        AllCampaignFormLocators.creative_type_option, attribute_name=all_campaign_form.title_attribute)
    all_campaign_form.clear_all()
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_all_option)
    all_campaign_form.change_last_approved_filter(AllCampaignFormLocators.user_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    all_campaign_form.select_dropdown_value(AllCampaignFormLocators.rows_per_page_label,
                                            AllCampaignFormLocators.hundred_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    assert "AutomationAdminUser" == all_campaign_form.get_text_or_value_from_list(
        AllCampaignFormLocators.all_campaign_list_last_approved_locator,
        AllCampaignFormLocators.user_option)
    generic_modules.step_info(
        "[END - RTB-7991] "
        "Validate filter options are working properly in the All Campaigns page individually")
    generic_modules.step_info(
        "[START - RTB-8083] Validate Filters and Clear all buttons, filtered value count]")
    all_campaign_form.clear_all()
    all_campaign_form.change_creative_type_filter(AllCampaignFormLocators.creative_type_option)
    all_campaign_form.wait_for_spinner_load(spinner_locator=AllCampaignFormLocators.processing_locator)
    assert '2' == all_campaign_form.get_attribute_value(AllCampaignFormLocators.filter_btn, 'data-count')
    all_campaign_form.clear_all()
    assert '1' == all_campaign_form.get_attribute_value(AllCampaignFormLocators.filter_btn, 'data-count')
    assert 'Pending' == all_campaign_form.get_text_or_value_from_selected_option(
        AllCampaignFormLocators.status_filter_locator)
    assert 'All users' == all_campaign_form.get_attribute_value(AllCampaignFormLocators.user_filter_locator,
                                                                'data-placeholder', locator_initialization=False)
    assert 'Country' == all_campaign_form.get_attribute_value(AllCampaignFormLocators.country_filter_locator,
                                                              'data-placeholder', locator_initialization=False)
    assert 'Creative type' == all_campaign_form.get_attribute_value(AllCampaignFormLocators.creative_type_filter_locator,
                                                                    'data-placeholder', locator_initialization=False)
    assert 'Last approved by' == all_campaign_form.get_attribute_value(
        AllCampaignFormLocators.last_approved_filter_locator, 'data-placeholder', locator_initialization=False)
    filter_area_visibility = all_campaign_form.is_visible(AllCampaignFormLocators.filter_area)
    all_campaign_form.click_on_element(AllCampaignFormLocators.filter_btn)
    all_campaign_form.wait_for_element_to_be_invisible(AllCampaignFormLocators.filter_area, time_out=5)
    assert filter_area_visibility != all_campaign_form.is_visible(AllCampaignFormLocators.filter_area, time_out=5)
    generic_modules.step_info(
        "[END - RTB-8083] Validate Filters and Clear all buttons, filtered value count]")


def test_regression_all_campaigns_columns_validation(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    with open('assets/campaign/campaign_approve_data.json', encoding='utf-8') as json_file:
        campaign_approve_data = json.load(json_file)
    generic_modules.step_info(
        "[START - RTB-7992] Validate ID column is showing proper ID number"
        "[START - RTB-7993] Validate All Campaign page table is showing proper campaign data]")
    # CREATE CAMPAIGN BY API
    campaign_data = CampaignUtil.create_campaign_by_api(config)
    campaign_data['userId'] = int(campaign_data['userId'])
    campaign_data['campaignId'] = str(campaign_data['campaignId'])
    campaign_data['campaign_type'] = 'Display Ads'
    campaign_data['creative_type'] = 'Banner'
    campaign_data['status'] = 'Pen.'
    campaign_data['bid'] = float(campaign_data['bid'])
    campaign_data['budget']['daily'] = float(campaign_data['budget']['daily'])
    campaign_data['budget']['total'] = float(campaign_data['budget']['total'])
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.search_by_value(campaign_data['campaignId'])
    pulled_campaign_data_gui = all_campaign_form.get_all_campaign_data_from_table(campaign_data['campaignId'])
    for key, value in pulled_campaign_data_gui.items():
        assert key in campaign_data and pulled_campaign_data_gui[key] == value, f"Assertion failed for key: {key}"
    generic_modules.step_info(
        "[END - RTB-7993] Validate All Campaign page table is showing proper campaign data]"
        "[START - RTB-8080] Validate All Campaign page table is showing proper Last Approved By data]")
    # APPROVE THE CAMPAIGN
    campaign_approve_data = CampaignUtil.process_campaign_approve_data(
        campaign_approve_data,
        single_approve=True)
    campaign_approve_form.navigate_to_approve_campaign_page(campaign_data['campaignId'])
    campaign_approve_form.approve_campaign(campaign_approve_data)
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.search_by_value(campaign_data['campaignId'])
    campaign_data['status'] = 'Rea.'
    campaign_data['approved_by'] = 'AutomationAdminUser'
    pulled_campaign_data_gui = all_campaign_form.get_all_campaign_data_from_table(campaign_data['campaignId'])
    for key, value in pulled_campaign_data_gui.items():
        assert key in campaign_data and pulled_campaign_data_gui[key] == value, f"Assertion failed for key: {key}"
    generic_modules.step_info(
        "[END - RTB-8080] Validate All Campaign page table is showing proper Last Approved By data]")
    generic_modules.step_info(
        "[START - RTB-8084] Validate column's values are clickable]")
    assert all_campaign_form.verify_redirect_to_campaign_edit_page(config, campaign_data['campaignId'],
                                                                   campaign_data['name'])
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.search_by_value(campaign_data['campaignId'])
    assert all_campaign_form.verify_redirect_to_campaign_approve_page(campaign_data['campaignId'])
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    assert all_campaign_form.verify_redirect_to_campaign_list_page_after_change_account()
    generic_modules.step_info(
        "[END - RTB-8084] Validate column's values are clickable]")


def test_regression_all_campaigns_three_dot_options_validation(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)

    generic_modules.step_info(
        "[START - RTB-8085] Validate Targeting Optimisation, Report, Confirm campaign options from the three dot icon]")

    # TARGETING OPTIMISATION, REPORT, CONFIRM CAMPAIGN OPTIONS VALIDATION
    campaign_data = CampaignUtil.create_campaign_by_api(config)
    campaign_data['campaignId'] = str(campaign_data['campaignId'])
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    assert all_campaign_form.verify_redirect_to_target_optimisation(campaign_data['campaignId'])
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    assert all_campaign_form.verify_redirect_to_reports(campaign_data['campaignId'])
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    assert all_campaign_form.verify_redirect_to_approve_page_after_confirm(campaign_data['campaignId'])
    generic_modules.step_info(
        "[END - RTB-8085] Validate Targeting Optimisation, Report, Confirm campaign options from the three dot icon]")

    generic_modules.step_info("[START - RTB-8086] Validate Reject Campaign options from the three dot icon]")

    # REJECT CAMPAIGN OPTION VALIDATION
    sidebar_navigation.navigate_to_page(PageNames.ALL_CAMPAIGNS)
    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.reject_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.reject_popup_x_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.reject_popup_x_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.reject_popup_x_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    time.sleep(2)
    assert False is all_campaign_form.is_element_displayed(AllCampaignFormLocators.reject_popup_locator)

    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.reject_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.reject_popup_x_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.reject_popup_close_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.reject_popup_close_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    time.sleep(2)
    assert False is all_campaign_form.is_element_displayed(AllCampaignFormLocators.reject_popup_locator)

    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.reject_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.reject_popup_x_btn_locator)
    textbox_text = all_campaign_form.get_element_text(AllCampaignFormLocators.textbox_locator)
    assert "" == textbox_text
    all_campaign_form.click_on_element(AllCampaignFormLocators.submit_btn_locator)
    assert "Reason is required" == all_campaign_form.get_element_text(
        AllCampaignFormLocators.reject_reason_message_locator)
    all_campaign_form.set_value_into_element(AllCampaignFormLocators.textbox_locator, "Test")
    all_campaign_form.click_on_element(AllCampaignFormLocators.submit_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    assert "Campaign rejected!" in all_campaign_form.get_element_text(AllCampaignFormLocators.alert_message_locator)
    all_campaign_form.search_by_value(campaign_data['campaignId'])
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_rejected_option)
    assert int(campaign_data['campaignId']) == int(all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_id_xpath.format(campaign_data['campaignId']), locator_initialization=True))
    generic_modules.step_info("[END - RTB-8086] Validate Reject Campaign options from the three dot icon]")

    generic_modules.step_info("[START - RTB-8087] Validate Delete Campaign options from the three dot icon]")

    # DELETE CAMPAIGN OPTION VALIDATION
    all_campaign_form.wait_for_spinner_load()
    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.delete_popup_close_btn_locator)
    time.sleep(1)
    assert "Are you sure you want to DELETE this campaign?" == all_campaign_form.get_element_text(
        AllCampaignFormLocators.delete_popup_message_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.delete_popup_close_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_popup_close_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    assert False is all_campaign_form.is_element_displayed(AllCampaignFormLocators.delete_popup_locator)

    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.delete_popup_close_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.delete_popup_no_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_popup_no_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    assert False is all_campaign_form.is_element_displayed(AllCampaignFormLocators.delete_popup_locator)

    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.delete_popup_close_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.delete_popup_yes_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_popup_yes_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    assert "Campaign deleted!" in all_campaign_form.get_element_text(AllCampaignFormLocators.alert_message_locator)
    all_campaign_form.search_by_value(campaign_data['campaignId'])
    all_campaign_form.verify_filter_area_visible(AllCampaignFormLocators.status_deleted_option)
    all_campaign_form.change_status_filter(AllCampaignFormLocators.status_deleted_option)
    assert int(campaign_data['campaignId']) == int(all_campaign_form.get_element_text(
        AllCampaignFormLocators.table_row_id_xpath.format(campaign_data['campaignId']), locator_initialization=True))

    generic_modules.step_info("[END - RTB-8087] Validate Delete Campaign options from the three dot icon]")

    generic_modules.step_info("[START - RTB-8088] Validate Remove Completely options from the three dot icon]")

    # REMOVE COMPLETELY OPTION VALIDATION
    all_campaign_form.wait_for_spinner_load()
    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.remove_completely_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.remove_popup_x_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.remove_popup_x_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.remove_popup_x_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    assert False is all_campaign_form.is_element_displayed(AllCampaignFormLocators.remove_popup_locator)

    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.remove_completely_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.remove_popup_x_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.delete_popup_no_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_popup_no_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    assert False is all_campaign_form.is_element_displayed(AllCampaignFormLocators.remove_popup_locator)

    all_campaign_form.click_on_element(AllCampaignFormLocators.three_dot_locator.format(campaign_data['campaignId']),
                                       locator_initialization=True,
                                       locator_to_be_appeared=AllCampaignFormLocators.three_dot_modal_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.remove_completely_campaign_locator.format(
        campaign_data['campaignId']), locator_initialization=True,
        locator_to_be_appeared=AllCampaignFormLocators.remove_popup_x_btn_locator)
    assert all_campaign_form.is_visible(AllCampaignFormLocators.delete_popup_yes_btn_locator)
    all_campaign_form.click_on_element(AllCampaignFormLocators.delete_popup_yes_btn_locator,
                                       locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)
    all_campaign_form.search_by_value(campaign_data['campaignId'])
    assert all_campaign_form.is_visible(AllCampaignFormLocators.no_data_for_defined_criteria_locator)

    generic_modules.step_info("[END - RTB-8088] Validate Remove Completely options from the three dot icon]")
