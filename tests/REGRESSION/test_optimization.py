import bisect
import copy
import json
import os
from decimal import Decimal
import time

from configurations import generic_modules
from locators.optimization.optimization_locators import OptimizationLocators
from pages.base_page import BasePage
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.navbar.navbar import DashboardNavbar
from pages.optimization.optimization import DspDashboardOptimization
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.redis import RedisUtils
from utils.currency import CurrencyUtils
from utils.page_names_enum import PageNames


def test_regression_optimization(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    campaign_id_list = {
        'BOTY Video DSP campaign - 22 April - 10 May - Low bid (ID: 124330)',
        'BOTY Video DSP campaign - 10 March - 09 April - SSP (ID: 119471)',
        'BOTY Video DSP campaign - 22 April - 10 May - SSP (ID: 124327)',
        'BOTY Video DSP campaign - 08 October- 07 November - SSP (ID: 101095)'}
    navbar.impersonate_user('Webcoupers - GLO')
    side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
    base_page.select_multiple_item_from_modal(campaign_id_list, OptimizationLocators.campaign_label)
    base_page.select_dropdown_value(OptimizationLocators.spent_label, "", True,
                                    OptimizationLocators.spent_based_on_cost_dropdown_item_value)
    optimization_page.select_specific_date_range_for_optimisation("all,")

    # [START] OPTIMISE BY EXCHANGE
    base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                    OptimizationLocators.optimise_by_exchange_dropdown_item_value)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "pause",
                                                                   group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=False,
                                                 group_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "play",
                                                                   group_and_single_action=True)

    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_exchange_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=False,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_exchange_dropdown_item_value,
        "play",
        group_and_single_action=True)

    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True,
                                                 bulk_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "pause",
                                                                   bulk_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=False,
                                                 bulk_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "play",
                                                                   bulk_action=True)
    # [END] OPTIMISE BY EXCHANGE

    # [START] OPTIMISE BY CREATIVE
    base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                    OptimizationLocators.optimise_by_creative_dropdown_item_value)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_creative_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=False,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_creative_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=True,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_creative_dropdown_item_value,
        "pause",
        bulk_action=True)

    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=False,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_creative_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=True,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_creative_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                 is_play=False,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_creative_dropdown_item_value,
        "play",
        bulk_action=True)
    # [END] OPTIMISE BY CREATIVE

    # [START] OPTIMISE BY APP/SITE NAME
    base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                    OptimizationLocators.optimise_by_app_site_name_dropdown_item_value)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    if base_page.is_element_present(
            OptimizationLocators.grid_locator,
            base_page.FIVE_SEC_DELAY):
        base_page.wait_for_visibility_of_element(
            OptimizationLocators.app_site_column_locator,
            time_out=base_page.ONE_MINUTE)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
            "pause",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=False,
                                                     single_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
            "play",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True,
                                                     bulk_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
            "pause",
            bulk_action=True)

        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=False,
                                                     group_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
            "play",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True,
                                                     single_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
            "pause",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=False,
                                                     bulk_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
            "play",
            bulk_action=True)
    else:
        print("No data to perform optimisation")
    # [END] OPTIMISE BY APP/SITE NAME

    # [START] OPTIMISE BY PLACEMENT
    base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                    OptimizationLocators.optimise_by_placement_dropdown_item_value)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    if base_page.is_element_present(
            OptimizationLocators.grid_locator,
            base_page.FIVE_SEC_DELAY):
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_placement_dropdown_item_value,
            "pause",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=False,
                                                     single_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_placement_dropdown_item_value,
            "play",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=True,
                                                     bulk_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_placement_dropdown_item_value,
            "pause",
            bulk_action=True)

        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=False,
                                                     group_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_placement_dropdown_item_value,
            "play",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=True,
                                                     single_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_placement_dropdown_item_value,
            "pause",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                     is_play=False,
                                                     bulk_action=True)
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_placement_dropdown_item_value,
            "play",
            bulk_action=True)
    else:
        print("No data to perform optimisation")
    # [END] OPTIMISE BY PLACEMENT


def test_regression_optimization_filters_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    file_name_part = ""
    download_dir = os.path.join(os.getcwd(), "downloads")

    generic_modules.step_info(
        "[START - RTB-8208] Validate filter and advanced filter options are available in the page]")
    side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
    optimization_page.click_on_element(OptimizationLocators.add_advance_search_options_btn_locator,
                                       locator_to_be_appeared=OptimizationLocators.include_exclude_locator)
    optimization_page_filter_options_locators = (OptimizationLocators.group_by_date_id,
                                                 OptimizationLocators.include_option_id,
                                                 OptimizationLocators.source_medium_id,
                                                 OptimizationLocators.containing_id,
                                                 OptimizationLocators.enter_value_here_id,
                                                 OptimizationLocators.x_btn_xpath)
    for locator in optimization_page_filter_options_locators:
        assert optimization_page.is_element_present(locator, locator_initialization=True)
    generic_modules.step_info(
        "[END - RTB-8208] Validate filter and advanced filter options are available in the page]")

    generic_modules.step_info(
        "[START - RTB-8209] Validate filter options and advanced filter are working properly]")
    navbar.impersonate_user('Webcoupers - GLO')
    campaign_id = "119468"
    creative_title = "Glo Boty 03-31"
    optimization_page.select_from_modal(campaign_id, OptimizationLocators.campaign_label)
    optimization_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                            OptimizationLocators.optimise_by_creative_dropdown_item_value)
    optimization_page.select_dropdown_value(OptimizationLocators.spent_label, "", True,
                                            OptimizationLocators.spent_based_on_cost_dropdown_item_value)
    optimization_page.select_specific_date_range_for_optimisation("all,")
    optimization_page.click_on_element(OptimizationLocators.search_button_locator)
    optimization_page.wait_for_spinner_load()
    assert campaign_id == optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_cell_xpath.format("1", "3"), locator_initialization=True)[0]
    assert creative_title == optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_cell_xpath.format("1", "2"), locator_initialization=True)[0]
    creative_id = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_cell_xpath.format("1", "1"), locator_initialization=True)[0]
    spent_from_db = "$" + CampaignUtil.pull_campaign_spent_based_on_cost_from_db(campaign_id, creative_id, db_connection)
    assert spent_from_db == optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_cell_xpath.format("1", "21"), locator_initialization=True)[0]
    optimization_page.click_on_element(OptimizationLocators.add_advance_search_options_btn_locator,
                                       locator_to_be_appeared=OptimizationLocators.include_exclude_locator)
    optimization_page.dropdown_selection(OptimizationLocators.source_medium_xpath, dropdown_item="Impressions")
    optimization_page.dropdown_selection(OptimizationLocators.containing_xpath, dropdown_item="Greater Than")
    optimization_page.set_value_into_element(OptimizationLocators.enter_value_here_id, '300',
                                             locator_initialization=True)
    optimization_page.click_on_element(OptimizationLocators.search_button_locator)
    optimization_page.wait_for_spinner_load()
    assert '300' < optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "5"),
        locator_initialization=True)[0]
    optimization_page.click_on_element(OptimizationLocators.clear_all_btn_locator)
    generic_modules.step_info(
        "[END - RTB-8209] Validate filter options and advanced filter are working properly]")

    generic_modules.step_info(
        "[START - RTB-8213] Validate Export Excel functionality")
    try:
        campaign_id_list = ['BOTY Video DSP campaign - 22 April - 10 May - Low bid (ID: 124330)']
        base_page.select_from_modal_form_using_js_code(OptimizationLocators.campaign_label,
                                                       option_list_to_select=campaign_id_list)
        optimization_page.select_specific_date_range_for_optimisation("all,")
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(OptimizationLocators.export_excel_btn_locator)
        base_page.wait_for_spinner_load()
        current_date = base_page.get_current_date_with_specific_format("%Y-%m-%d")
        file_name_part = current_date + "_optimisation_"
        assert base_page.is_a_file_with_specific_file_name_part_available_into_a_folder(
            download_dir, file_name_part)
        actual_size_in_bytes = base_page.get_file_size(download_dir, file_name_part + "*")
        assert "12000" > str(actual_size_in_bytes) > "10000"
    finally:
        base_page.delete_file(download_dir, file_name_part + "*")
    generic_modules.step_info(
        "[START - RTB-8278] Validate Export CSV functionality")
    try:
        base_page.click_on_element(OptimizationLocators.export_csv_btn_locator)
        base_page.wait_for_spinner_load()
        current_date = base_page.get_current_date_with_specific_format("%Y-%m-%d")
        file_name_part = current_date + "_optimisation_"
        assert base_page.is_a_file_with_specific_file_name_part_available_into_a_folder(
            download_dir, file_name_part)
        actual_size_in_bytes = base_page.get_file_size(download_dir, file_name_part + "*")
        assert "3000" > str(actual_size_in_bytes) > "1000"
    finally:
        base_page.delete_file(download_dir, file_name_part + "*")

    try:
        campaign_id_list = [
            'BOTY Video DSP campaign - 22 April - 10 May - Low bid (ID: 124330)',
            'BOTY Video DSP campaign - 10 March - 09 April - SSP (ID: 119471)',
            'BOTY Video DSP campaign - 22 April - 10 May - SSP (ID: 124327)',
            'BOTY Video DSP campaign - 08 October- 07 November - SSP (ID: 101095)']
        base_page.select_from_modal_form_using_js_code_without_retry(OptimizationLocators.campaign_label,
                                                                     option_list_to_select=campaign_id_list)
        base_page.select_dropdown_value(OptimizationLocators.spent_label, "", True,
                                        OptimizationLocators.spent_based_on_cost_dropdown_item_value)
        optimization_page.select_specific_date_range_for_optimisation("all,")
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_exchange_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(OptimizationLocators.export_excel_btn_locator)
        base_page.wait_for_spinner_load()
        assert base_page.is_a_file_with_specific_file_name_part_available_into_a_folder(
            download_dir, file_name_part)
        actual_size_in_bytes = base_page.get_file_size(download_dir, file_name_part + "*")
        assert "14000" > str(actual_size_in_bytes) > "11000"
    finally:
        base_page.delete_file(download_dir, file_name_part + "*")
    try:
        base_page.click_on_element(OptimizationLocators.export_csv_btn_locator)
        base_page.wait_for_spinner_load()
        assert base_page.is_a_file_with_specific_file_name_part_available_into_a_folder(
            download_dir, file_name_part)
        actual_size_in_bytes = base_page.get_file_size(download_dir, file_name_part + "*")
        assert "3000" > str(actual_size_in_bytes) > "1000"
    finally:
        base_page.delete_file(download_dir, file_name_part + "*")

    generic_modules.step_info(
        "[END - RTB-8213] Validate Export Excel functionality")
    generic_modules.step_info(
        "[END - RTB-8278] Validate Export CSV functionality")


def test_regression_optimization_campaign_table_data_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    navbar = DashboardNavbar(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    generic_modules.step_info("[START - RTB-8279] Validate campaign table data I")

    navbar.impersonate_user('Webcoupers - GLO')
    side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
    campaign_id = "73950"
    exchange_id = "2"
    exchange_name = "Doubleclick"
    campaign_name = "*777# DSP campaign - 05 Mar - 08 Apr - Broad - Click to USSD"
    optimization_page.select_from_modal_form_using_js_code(
        OptimizationLocators.campaign_label, option_to_select=campaign_name + " (ID: " + campaign_id + ")")
    optimization_page.select_specific_date_range_for_optimisation("all,")
    optimization_page.click_on_element(OptimizationLocators.search_button_locator)
    optimization_page.wait_for_spinner_load()

    # ID VALIDATION
    exchange_id_from_db = str(CampaignUtil.pull_exchange_id_from_db(exchange_name, db_connection))
    exchange_id_from_table = optimization_page.get_element_text(
        OptimizationLocators.exchange_id_xpath.format(exchange_id), locator_initialization=True)
    assert exchange_id_from_db == exchange_id_from_table

    # EXCHANGE VALIDATION
    exchange_from_db = CampaignUtil.pull_exchange_name_from_db(exchange_id, db_connection)
    exchange_from_table = optimization_page.get_element_text(OptimizationLocators.exchange_xpath.format(exchange_id),
                                                             locator_initialization=True)
    assert exchange_from_db == exchange_from_table

    # CAMPAIGN VALIDATION
    campaign_id_from_db = CampaignUtil.pull_campaign_id_from_db(campaign_name, db_connection, user_id="1187")
    formatted_campaign_id_from_db = str(campaign_id_from_db[0]['id'])
    campaign_id_from_table = optimization_page.get_element_text(OptimizationLocators.campaign_id_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)
    assert formatted_campaign_id_from_db == campaign_id_from_table

    # BIDS VALIDATION
    bids_from_db = int(CampaignUtil.pull_campaign_bids_from_db(campaign_id, exchange_id, db_connection))
    bids_from_table = optimization_page.get_element_text(OptimizationLocators.bids_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace(',', '')
    assert bids_from_db == int(bids_from_table)

    # IMPRESSIONS VALIDATION
    impressions_from_db = int(CampaignUtil.pull_campaign_impressions_from_db(campaign_id, exchange_id, db_connection))
    impressions_from_table = optimization_page.get_element_text(OptimizationLocators.impressions_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace(',', '')
    assert impressions_from_db == int(impressions_from_table)

    # WIN RATE VALIDATION
    win_rate = (impressions_from_db / bids_from_db * 100)
    formatted_win_rate = '{:.2f}%'.format(round(win_rate, 2))
    assert formatted_win_rate == optimization_page.get_element_text(OptimizationLocators.win_rate_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)

    # VIEWS VALIDATION
    views_from_db = int(CampaignUtil.pull_campaign_views_from_db(campaign_id, exchange_id, db_connection))
    views_from_table = optimization_page.get_element_text(OptimizationLocators.views_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace(',', '')
    assert views_from_db == int(views_from_table)

    # VIEWABILITY VALIDATION
    viewability = (views_from_db / impressions_from_db * 100)
    formatted_viewability = '{:.2f}%'.format(round(viewability, 2))
    assert formatted_viewability == optimization_page.get_element_text(OptimizationLocators.viewability_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)

    # CLICKS VALIDATION
    clicks_from_db = int(CampaignUtil.pull_campaign_clicks_from_db(campaign_id, exchange_id, db_connection))
    clicks_from_table = optimization_page.get_element_text(OptimizationLocators.clicks_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace(',', '')
    assert clicks_from_db == int(clicks_from_table)

    generic_modules.step_info("[END - RTB-8279] Validate campaign table data I")

    generic_modules.step_info("[START - RTB-8280] Validate campaign table data II")

    # CTR VALIDATION
    ctr = clicks_from_db / impressions_from_db * 100
    formatted_ctr = '{:.2f}%'.format(round(ctr, 2))
    assert formatted_ctr == optimization_page.get_element_text(OptimizationLocators.ctr_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)

    # SPENT VALIDATION
    spent_from_db = round(CampaignUtil.pull_campaign_spent_based_on_revenue_from_db(campaign_id, exchange_id, db_connection), 2)
    spent_from_table = optimization_page.get_element_text(OptimizationLocators.spent_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("$", '')
    assert spent_from_db == Decimal(spent_from_table)

    # CPM VALIDATION
    cpm = spent_from_db / impressions_from_db * 1000
    formatted_cpm = '${:.2f}'.format(round(cpm, 2))
    assert formatted_cpm == optimization_page.get_element_text(OptimizationLocators.cpm_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)

    # OTHER VALUES VALIDATION
    engaged_sessions = optimization_page.get_element_text(OptimizationLocators.engaged_sessions_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)
    sr = optimization_page.get_element_text(OptimizationLocators.sr_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("%", '')
    conversions = optimization_page.get_element_text(OptimizationLocators.conversions_xpath.format(
        exchange_id, campaign_id), locator_initialization=True)
    cr = optimization_page.get_element_text(OptimizationLocators.cr_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("%", '')
    tech_fee = optimization_page.get_element_text(OptimizationLocators.tech_fee_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("$", '')
    cpc = optimization_page.get_element_text(OptimizationLocators.cpc_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("$", '')
    cps = optimization_page.get_element_text(OptimizationLocators.cps_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("$", '')
    cpa = optimization_page.get_element_text(OptimizationLocators.cpa_xpath.format(
        exchange_id, campaign_id), locator_initialization=True).replace("$", '')
    values_from_table_list = [engaged_sessions, sr, conversions, cr, tech_fee, cpc, cps, cpa]
    for value in values_from_table_list:
        assert optimization_page.is_non_negative_decimal(value), f"{value} is not a non-negative decimal."

    generic_modules.step_info("[END - RTB-8280] Validate campaign table data II")


def test_regression_optimization_rule_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)
    if "qa-testing" in config['credential']['url']:
        print("[START] [RTB-8275] Validate campaign rules after stopping/starting optimisation")
        print("[START] GET EXPECTED REDIS DATA")
        with open('assets/campaign/redis_data/redis_data_for_optimisation_campaign.json') as json_file:
            redis_data_for_optimisation_campaign = json.load(json_file)
        print("[END] GET EXPECTED REDIS DATA")

        campaign_data = {'id': 188073, 'name_and_type': {}}
        campaign_data['name_and_type']['campaign_name'] = 'FOJ Promo -15 Nov - 14 Dec - Traffic'
        impersonate_user = 'Webcoupers - GLO'
        currency_id = '102'
        currency_rate = CurrencyUtils.pull_currency_rate_data_db(currency_id, db_connection)
        redis_data_for_optimisation_campaign['user']['currencyRate'] = int(currency_rate[0])

        print("[START] IMPERSONATE USER AND ADD BUDGET")
        navbar.impersonate_user(impersonate_user)
        payment_page.add_budget_into_specific_client(impersonate_user, 1000)
        print("[END] IMPERSONATE USER AND ADD BUDGET")

        print("[START] UPDATE CAMPAIGN DATE TO TODAY")
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page'][
            'campaign-edit-url'].format(str(campaign_data['id']))
        driver.get(campaign_edit_url)
        campaign_page.provide_launch_date_and_budget_info(campaign_data, edit_campaign=True)
        campaign_page.click_save_cancel_or_draft('save')
        print("[END] UPDATE CAMPAIGN DATE TO TODAY")

        print("[START] PAUSE CAMPAIGN APP/SITE")
        side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
        base_page.select_multiple_item_from_modal([str(campaign_data['id'])],
                                                  OptimizationLocators.campaign_label)
        base_page.select_dropdown_value(OptimizationLocators.spent_label, "",
                                        True,
                                        OptimizationLocators.spent_based_on_cost_dropdown_item_value)
        optimization_page.select_specific_date_range_for_optimisation("all,")
        base_page.select_dropdown_value(
            OptimizationLocators.optimise_by_label,
            "", True,
            OptimizationLocators.optimise_by_app_site_name_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        first_element_id = base_page.get_value_from_specific_grid_column(
            OptimizationLocators.optimisation_table_wrapper_div_id, OptimizationLocators.id_label)
        second_element_id = base_page.get_value_from_specific_grid_column(
            OptimizationLocators.optimisation_table_wrapper_div_id, OptimizationLocators.id_label,
            row_number="2")
        redis_data_for_app_sites = copy.deepcopy(redis_data_for_optimisation_campaign)
        action_btn_value = base_page.get_attribute_value(
            locator=OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
            attribute_name='data-action', locator_initialization=True)
        second_line_action_btn_value = base_page.get_attribute_value(
            locator=OptimizationLocators.action_btn.format(int(second_element_id), int(campaign_data['id'])),
            attribute_name='data-action', locator_initialization=True)
        if action_btn_value == 'start':
            base_page.click_on_element(
                OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
                locator_initialization=True)
        else:
            base_page.click_on_element(
                OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
                locator_initialization=True)
            if second_line_action_btn_value == 'stop':
                base_page.click_on_element(
                    OptimizationLocators.action_btn.format(int(second_element_id), int(campaign_data['id'])),
                    locator_initialization=True)
            bisect.insort(redis_data_for_app_sites['targeting']['sites']['exclude'], int(first_element_id))
        redis_data_for_app_sites['dspConfig']['exchanges'] = ""
        redis_data_for_app_sites['creativeSets'] = ""
        redis_data_for_app_sites['html'] = ""
        # necessary evil to hold while rules in redis sync
        time.sleep(2)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_data['id'])
        assert campaign_data['id'] == redis_data['id']
        assert campaign_data['name_and_type']['campaign_name'] == redis_data['name']
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""
        redis_data['dspConfig']['exchanges'] = ""
        redis_data['creativeSets'] = ""
        redis_data['html'] = ""
        redis_data['user']['targetDmpIds'] = []

        assert redis_data_for_app_sites == redis_data
        print("[END] PAUSE CAMPAIGN APP/SITE")

        print("[START] PAUSE CAMPAIGN EXCHANGE")
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label,
                                        "",
                                        True,
                                        OptimizationLocators.optimise_by_exchange_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        first_element_id = base_page.get_value_from_specific_grid_column(
            OptimizationLocators.optimisation_table_wrapper_div_id, OptimizationLocators.id_label)
        action_btn_value = base_page.get_attribute_value(
            locator=OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
            attribute_name='data-action', locator_initialization=True)
        redis_data_for_exchange = copy.deepcopy(redis_data_for_optimisation_campaign)
        if action_btn_value == 'start':
            base_page.click_on_element(
                OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
                locator_initialization=True)
        else:
            base_page.click_on_element(
                OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
                locator_initialization=True)
            redis_data_for_exchange['dspConfig']['exchanges'].remove(int(first_element_id))
        time.sleep(2)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_data['id'])
        assert redis_data_for_exchange['dspConfig']['exchanges'] == redis_data['dspConfig']['exchanges']
        print("[END] PAUSE CAMPAIGN EXCHANGE")

        print("[START] PAUSE CAMPAIGN CREATIVES")
        base_page.select_dropdown_value(
            OptimizationLocators.optimise_by_label,
            "", True,
            OptimizationLocators.optimise_by_creative_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        first_element_id = base_page.get_value_from_specific_grid_column(
            OptimizationLocators.optimisation_table_wrapper_div_id, OptimizationLocators.id_label)
        action_btn_value = base_page.get_attribute_value(
            locator=OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
            attribute_name='data-action', locator_initialization=True)
        redis_data_for_creatives = copy.deepcopy(redis_data_for_optimisation_campaign)
        if action_btn_value == 'start':
            base_page.click_on_element(
                OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
                locator_initialization=True)
        else:
            base_page.click_on_element(
                OptimizationLocators.action_btn.format(int(first_element_id), int(campaign_data['id'])),
                locator_initialization=True)
            optimization_page.remove_creative_from_set_by_id(redis_data_for_creatives['creativeSets'],
                                                             int(first_element_id))
            optimization_page.remove_creative_from_html_by_id(redis_data_for_creatives['html'], int(first_element_id))
        time.sleep(3)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_data['id'])
        optimization_page.update_bid_to_empty_string(redis_data['html'])
        assert redis_data_for_creatives['creativeSets'] == redis_data['creativeSets']
        assert redis_data_for_creatives['html'] == redis_data['html']
        print("[END] PAUSE CAMPAIGN CREATIVES")
        print("[END] [RTB-8275] Validate campaign rules after stopping/starting optimisation")
