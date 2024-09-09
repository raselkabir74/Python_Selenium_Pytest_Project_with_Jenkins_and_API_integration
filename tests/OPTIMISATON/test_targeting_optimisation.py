import time

from selenium.webdriver import Keys

from configurations import generic_modules
from locators.optimization.optimization_locators import OptimizationLocators
from pages.base_page import BasePage
from pages.navbar.navbar import DashboardNavbar
from pages.optimization.optimization import DspDashboardOptimization
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_dashboard_optimization_search_validation(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    navbar = DashboardNavbar(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    generic_modules.step_info("[START - RTB-8210] Validate search field I")

    campaign_id_list = [
        '*777# DSP campaign - 05 Mar - 08 Apr - apps (ID: 73951)',
        '*777# DSP campaign - 05 Mar - 08 Apr - Broad - Click to USSD (ID: 73950)',
        '*777# DSP campaign - 05 Mar - 08 Apr - Broad - Competitors/Wifi (ID: 73949)',
        '*777# DSP campaign - 05 Mar - 08 Apr - device price TOP sites - Click to USSD (ID: 73948)',
        '*777# DSP campaign - 05 Mar - 08 Apr - device price TOP sites - Competitors/Wifi (ID: 73945)']
    navbar.impersonate_user('Webcoupers - GLO')
    side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
    optimization_page.select_from_modal_form_using_js_code(OptimizationLocators.campaign_label,
                                                           option_list_to_select=campaign_id_list)
    optimization_page.select_dropdown_value(OptimizationLocators.spent_label, "", True,
                                            OptimizationLocators.spent_based_on_cost_dropdown_item_value)
    optimization_page.select_specific_date_range_for_optimisation("all,")
    optimization_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                            OptimizationLocators.optimise_by_exchange_dropdown_item_value)
    optimization_page.click_on_element(OptimizationLocators.search_button_locator)

    generic_modules.step_info("[START - RTB-8416] Validate search field with exchange name")
    print("[START] Validate search field with exchange name")
    exchange_name = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_cell_xpath.format("1", "2"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, exchange_name[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    exchange_name_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_column_all_cell_xpath.format("2"), locator_initialization=True)
    assert exchange_name[0] in exchange_name_list
    print("[END] Validate search field with exchange name")
    generic_modules.step_info("[END - RTB-8416] Validate search field with exchange name")

    print("[START] Validate search field with exchange id")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    exchange_id = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_cell_xpath.format("2", "1"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, exchange_id[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    exchange_id_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_column_all_cell_xpath.format("1"), locator_initialization=True)
    assert exchange_id[0] in exchange_id_list
    print("[END] Validate search field with exchange id")

    print("[START] Validate search field with Campaign id")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    campaign_id = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "3"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, campaign_id[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    campaign_id_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "3"), locator_initialization=True)
    assert campaign_id[0] in campaign_id_list
    print("[END] Validate search field with Campaign id")

    print("[START] Validate search field with Bid value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    bids = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "4"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, bids[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    bid_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "4"),
        locator_initialization=True)
    assert bids[0] in bid_list
    print("[END] Validate search field with Bid value")

    print("[START] Validate search field with Impression value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    impression = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "5"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, impression[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    impression_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "5"),
        locator_initialization=True)
    assert impression[0] in impression_list
    print("[END] Validate search field with Impression value")

    print("[START] Validate search field with Win rate value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    win_rates = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "6"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, win_rates[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    win_rate_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "6"),
        locator_initialization=True)
    assert win_rates[0] in win_rate_list
    print("[END] Validate search field with Win rate value")

    print("[START] Validate search field with Views value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    views = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "7"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, views[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    view_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "7"),
        locator_initialization=True)
    assert views[0] in view_list
    print("[END] Validate search field with Views value")

    print("[START] Validate search field with Clicks value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    clicks = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "9"), locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, clicks[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    click_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "9"),
        locator_initialization=True)
    assert clicks[0] in click_list
    print("[END] Validate search field with Clicks value")

    print("[START] Validate search field with CTR value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    ctrs = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "10"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, ctrs[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    ctr_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "10"),
        locator_initialization=True)
    assert ctrs[0] in ctr_list
    print("[END] Validate search field with CTR value")

    print("[START] Validate search field with Engaged sessions value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    engaged_sessions = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "11"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, engaged_sessions[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    engaged_session_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "11"),
        locator_initialization=True)
    assert engaged_sessions[0] in engaged_session_list
    print("[END] Validate search field with Engaged sessions value")

    print("[START] Validate search field with SR value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    srs = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "12"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, srs[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    sr_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1 ", "12"),
        locator_initialization=True)
    assert srs[0] in sr_list
    print("[END] Validate search field with SR value")

    generic_modules.step_info("[END - RTB-8210] Validate search field I")


def test_dashboard_optimization_search_validation_two(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    navbar = DashboardNavbar(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    generic_modules.step_info("[START - RTB-8211] Validate search field II")

    campaign_id_list = [
        '*777# DSP campaign - 05 Mar - 08 Apr - apps (ID: 73951)',
        '*777# DSP campaign - 05 Mar - 08 Apr - Broad - Click to USSD (ID: 73950)',
        '*777# DSP campaign - 05 Mar - 08 Apr - Broad - Competitors/Wifi (ID: 73949)',
        '*777# DSP campaign - 05 Mar - 08 Apr - device price TOP sites - Click to USSD (ID: 73948)',
        '*777# DSP campaign - 05 Mar - 08 Apr - device price TOP sites - Competitors/Wifi (ID: 73945)']
    navbar.impersonate_user('Webcoupers - GLO')
    side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
    optimization_page.select_from_modal_form_using_js_code(OptimizationLocators.campaign_label,
                                                           option_list_to_select=campaign_id_list)
    optimization_page.select_dropdown_value(OptimizationLocators.spent_label, "", True,
                                            OptimizationLocators.spent_based_on_cost_dropdown_item_value)
    optimization_page.select_specific_date_range_for_optimisation("all,")
    optimization_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                            OptimizationLocators.optimise_by_exchange_dropdown_item_value)
    optimization_page.click_on_element(OptimizationLocators.search_button_locator)

    print("[START] Validate search field with Conversions value")
    conversions = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "13"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, conversions[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    conversion_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "13"),
        locator_initialization=True)
    assert conversions[0] in conversion_list
    print("[END] Validate search field with Conversions value")

    print("[START] Validate search field with CR value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    crs = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "14"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, crs[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    cr_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "14"),
        locator_initialization=True)
    assert crs[0] in cr_list
    print("[END] Validate search field with CR value")

    print("[START] Validate search field with Tech Fee value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    tech_fees = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "15"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, tech_fees[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    tech_fee_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "15"),
        locator_initialization=True)
    assert tech_fees[0] in tech_fee_list
    print("[END] Validate search field with Tech Fee value")

    print("[START] Validate search field with CPM value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    cpms = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "16"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, cpms[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    cpm_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "16"),
        locator_initialization=True)
    assert cpms[0] in cpm_list
    print("[END] Validate search field with CPM value")

    print("[START] Validate search field with CPC value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    cpcs = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "17"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, cpcs[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    cpc_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "17"),
        locator_initialization=True)
    assert cpcs[0] in cpc_list
    print("[END] Validate search field with CPC value")

    print("[START] Validate search field with CPS value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    cpss = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "18"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, cpss[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    cps_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "18"),
        locator_initialization=True)
    assert cpss[0] in cps_list
    print("[END] Validate search field with CPS value")

    print("[START] Validate search field with CPA value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    cpas = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "19"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, cpas[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    cpa_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "19"),
        locator_initialization=True)
    assert cpas[0] in cpa_list
    print("[END] Validate search field with CPA value")

    print("[START] Validate search field with Spent value")
    optimization_page.clear_field(OptimizationLocators.search_field_locator)
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    time.sleep(1)
    spents = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("2", "20"),
        locator_initialization=True)
    optimization_page.set_value_into_element(
        OptimizationLocators.search_field_locator, spents[0])
    optimization_page.wait_for_presence_of_element(
        OptimizationLocators.search_field_locator).send_keys(Keys.ENTER)
    optimization_page.wait_for_spinner_load()
    spent_list = optimization_page.get_text_or_value_from_list(
        OptimizationLocators.optimisation_table_specific_multi_cell_xpath.format("1", "20"),
        locator_initialization=True)
    assert spents[0] in spent_list
    print("[END] Validate search field with Spent value")

    generic_modules.step_info("[END - RTB-8211] Validate search field II")


def test_dashboard_optimization_filter_button_validation(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    navbar = DashboardNavbar(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    campaign_id_list = [
        '*777# DSP campaign - 05 Mar - 08 Apr - apps (ID: 73951)']

    generic_modules.step_info("[START - RTB-8212]  Filter and Clear all btns and pagination")

    print("[START] Validate Filters button")
    navbar.impersonate_user('Webcoupers - GLO')
    side_bar_navigation.navigate_to_page(PageNames.OPTIMISATION)
    optimization_page.click_on_element(OptimizationLocators.filter_btn_locator)
    time.sleep(2)
    assert optimization_page.is_visible(OptimizationLocators.search_button_locator, time_out=1) is False
    optimization_page.click_on_element(OptimizationLocators.filter_btn_locator,
                                       locator_to_be_appeared=OptimizationLocators.search_button_locator)
    assert optimization_page.is_visible(OptimizationLocators.search_button_locator, time_out=1)
    print("[END] Validate Filters button")

    print("[START] Validate filters button's filter selection count")
    optimization_page.select_from_modal_form_using_js_code(OptimizationLocators.campaign_label,
                                                           option_list_to_select=campaign_id_list)
    optimization_page.click_on_element(OptimizationLocators.add_advance_search_options_btn_locator,
                                       locator_to_be_appeared=OptimizationLocators.x_btn_locator)
    time.sleep(1)
    assert optimization_page.get_attribute_value(OptimizationLocators.filter_btn_locator, BasePage.data_count_tag) is \
           "5"
    optimization_page.click_on_element(OptimizationLocators.x_btn_locator)
    time.sleep(1)
    assert optimization_page.get_attribute_value(OptimizationLocators.filter_btn_locator, BasePage.data_count_tag) is \
           "4"
    print("[END] Validate filters button's filter selection count")

    print("[START] Validate Clear all button")
    optimization_page.click_on_element(OptimizationLocators.add_advance_search_options_btn_locator,
                                       locator_to_be_appeared=OptimizationLocators.x_btn_locator)
    optimization_page.click_on_element(OptimizationLocators.clear_all_btn_locator)
    time.sleep(2)
    assert optimization_page.get_attribute_value(OptimizationLocators.filter_btn_locator, BasePage.data_count_tag) is \
           "3"
    assert "Optimise by exchange" == optimization_page.get_text_or_value_from_selected_option(
        OptimizationLocators.optimise_by_label)
    assert "Spent based on revenue" == optimization_page.get_text_or_value_from_selected_option(
        OptimizationLocators.spent_label)
    assert optimization_page.get_current_date_with_specific_format("%d %b, %Y") in optimization_page.get_element_text(
        OptimizationLocators.dates_field_locator,
        input_tag=True)
    assert optimization_page.is_visible(OptimizationLocators.x_btn_locator, time_out=1) is False
    print("[END] Validate Clear all button")

    generic_modules.step_info("[END - RTB-8212]  Filter and Clear all btns and pagination")


def test_dashboard_optimization(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)
    optimization_page = DspDashboardOptimization(config, driver)

    navbar.impersonate_user('Webcoupers - GLO')

    # [START] OPTIMISE BY OPERATING SYSTEM
    campaigns = "124330,119471,124327,101095"
    optimise_by_option = "os"
    spent_based_option = "2"
    date_from = "2015-01-01"
    date_to = optimization_page.get_current_date_with_specific_format("%Y-%m-%d")
    date_group = "0"
    advance_search = ""
    campaign_optimisation_url = config['credential']['url'] + \
                                 "/admin/optimisation?campaign_id={}&optimise_by={}&spent_based={}" \
                                "&date_from={}&date_to={}&date_group={}&advanceSearch={}".format(
                                    campaigns, optimise_by_option, spent_based_option, date_from, date_to, date_group,
                                    advance_search)
    driver.get(campaign_optimisation_url)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_os_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=False,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_os_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=True,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_os_dropdown_item_value,
        "pause",
        bulk_action=True)

    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=False,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_os_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=True,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_os_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                 is_play=False,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_os_dropdown_item_value,
        "play",
        bulk_action=True)
    # [END] OPTIMISE BY OPERATING SYSTEM

    # [START] OPTIMISE BY BROWSER
    optimise_by_option = "browser"
    campaign_optimisation_url = config['credential']['url'] + \
                                "/admin/optimisation?campaign_id={}&optimise_by={}&spent_based={}" \
                                "&date_from={}&date_to={}&date_group={}&advanceSearch={}".format(
                                    campaigns, optimise_by_option, spent_based_option, date_from, date_to, date_group,
                                    advance_search)
    driver.get(campaign_optimisation_url)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_browser_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=False,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_browser_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=True,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_browser_dropdown_item_value,
        "pause",
        bulk_action=True)

    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=False,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_browser_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=True,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_browser_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                 is_play=False,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_browser_dropdown_item_value,
        "play",
        bulk_action=True)
    # [END] OPTIMISE BY BROWSER

    # [START] OPTIMISE BY OPERATOR
    optimise_by_option = "operator"
    campaign_optimisation_url = config['credential']['url'] + \
                                "/admin/optimisation?campaign_id={}&optimise_by={}&spent_based={}" \
                                "&date_from={}&date_to={}&date_group={}&advanceSearch={}".format(
                                    campaigns, optimise_by_option, spent_based_option, date_from, date_to, date_group,
                                    advance_search)
    driver.get(campaign_optimisation_url)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_operator_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=False,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_operator_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=True,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_operator_dropdown_item_value,
        "pause",
        bulk_action=True)

    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=False,
                                                 group_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_operator_dropdown_item_value,
        "play",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=True,
                                                 single_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_operator_dropdown_item_value,
        "pause",
        group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=True,
                                                 group_action=True)
    optimization_page.click_on_play_pause_button("1",
                                                 OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                 is_play=False,
                                                 bulk_action=True)
    base_page.click_on_element(
        OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status(
        "1",
        OptimizationLocators.optimise_by_operator_dropdown_item_value,
        "play",
        bulk_action=True)
    # [END] OPTIMISE BY OPERATOR

    # [START] OPTIMISE BY PACKAGE
    campaigns = "119471,124327,101095"
    optimise_by_option = "package"
    campaign_optimisation_url = config['credential']['url'] + \
                                "/admin/optimisation?campaign_id={}&optimise_by={}&spent_based={}" \
                                "&date_from={}&date_to={}&date_group={}&advanceSearch={}".format(
                                    campaigns, optimise_by_option, spent_based_option, date_from, date_to, date_group,
                                    advance_search)
    driver.get(campaign_optimisation_url)
    if base_page.is_element_present(
            OptimizationLocators.grid_locator,
            base_page.FIVE_SEC_DELAY):
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_package_dropdown_item_value,
            "pause",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=False,
                                                     single_action=True)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_package_dropdown_item_value,
            "play",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True,
                                                     bulk_action=True)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_package_dropdown_item_value,
            "pause",
            bulk_action=True)

        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=False,
                                                     group_action=True)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_package_dropdown_item_value,
            "play",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True,
                                                     single_action=True)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_package_dropdown_item_value,
            "pause",
            group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True,
                                                     group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=False,
                                                     bulk_action=True)
        base_page.wait_for_spinner_load()
        base_page.click_on_element(
            OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status(
            "1",
            OptimizationLocators.optimise_by_package_dropdown_item_value,
            "play",
            bulk_action=True)
    else:
        print("No data to perform optimisation")
    # [END] OPTIMISE BY PACKAGE
