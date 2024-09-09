import json
import os
import time

import pytest
from _decimal import Decimal

from selenium.webdriver import Keys

from configurations import generic_modules
from locators.io.io_list_locator import IoListLocators
from pages.io.io_list import DspDashboardIoList
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.io.io_form import DspDashboardIoForm
from locators.io.io_form_locator import IoFormLocators
from utils.currency import CurrencyUtils
from utils.io import IoUtils
from pages.io.invoice_form import DspDashboardInvoiceForm
from locators.io.invoice_form_locator import InvoiceFormLocators
from pages.io.proforma_form import DspDashboardProformaForm
from locators.io.proforma_form_locator import ProformaFormLocators
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.navbar.navbar import DashboardNavbar
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from utils.page_names_enum import PageNames
from utils.user import UserUtils as UserUtil


debug_mode = "JENKINS_URL" not in os.environ


def test_finance_io_list_page(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    generic_modules.step_info(
        "[START - RTB-6987] Validate filter options are available in the IO list page")

    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page_filter_field_data_qa = (
        IoListLocators.client_account_data_qa,
        IoListLocators.client_company_data_qa,
        IoListLocators.company_group_data_qa,
        IoListLocators.eskimi_billing_entity_data_qa,
        IoListLocators.sent_data_qa,
        IoListLocators.paid_data_qa,
        IoListLocators.expired_data_qa, IoListLocators.bill_status_data_qa,
        IoListLocators.io_period_data_qa,
        IoListLocators.invoice_period_data_qa,
        IoListLocators.credit_invoice_data_qa,
        IoListLocators.io_signed_data_qa,
        IoListLocators.responsible_adops_data_qa,
        IoListLocators.sales_person_data_qa,
        IoListLocators.sales_team_data_qa,
        IoListLocators.account_manager_data_qa,
        IoListLocators.io_campaign_status_data_qa,
        IoListLocators.io_deadline_data_qa,
        IoListLocators.io_execution_comment_data_qa,
        IoListLocators.io_warning_message_data_qa)

    for field_data_qa in io_list_page_filter_field_data_qa:
        assert io_list_page.is_specific_filter_field_available(
            field_data_qa)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    generic_modules.step_info(
        "[END - RTB-6987] Validate filter options are available in the IO list page")

    generic_modules.step_info(
        "[START - RTB-6988] Validate filter options are working properly in the IO list page individually")

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_data_and_save(io_data)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag,
                                                          io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # VALIDATE CLIENT ACCOUNT FILTER
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.select_dropdown_value(IoListLocators.client_account_data_qa, io_data['client_profile']['client'])
    io_list_page.wait_for_spinner_load()
    io_list_page.set_value_into_element(
        IoListLocators.search_field_data_qa,
        io_data['io_main_information'][
            'io_title'])
    io_list_page.wait_for_presence_of_element(
        IoListLocators.search_field_data_qa).send_keys(Keys.ENTER)
    io_list_page.wait_for_spinner_load()
    assert io_data['client_profile'][
               'client'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.client_label)

    # VALIDATE CLIENT COMPANY
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, io_data['client_profile'][
        'client_company'])
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)

    # VALIDATE CLIENT COMPANY
    io_list_page.clear_specific_filter_option_from_io_list_page(
        IoListLocators.client_company_data_qa)
    io_list_page.wait_for_spinner_load()
    io_list_page.select_dropdown_value(IoListLocators.company_group_data_qa, "ACI")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE ESKIMI BILLING ENTITY
    io_list_page.clear_specific_filter_option_from_io_list_page(
        IoListLocators.company_group_data_qa)
    io_list_page.wait_for_spinner_load()
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.eskimi_billing_entity_data_qa,
        option_to_select=io_data['billing_entity']['company_profile'])
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.eskimi_billing_entity_data_qa, option_to_select="Eskimi NG-NG")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE SENT
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.eskimi_billing_entity_data_qa, check_all=False)
    io_list_page.wait_for_spinner_load()
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.sent_data_qa, check_all=True)
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE PAID
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.sent_data_qa, check_all=False)
    io_list_page.wait_for_spinner_load()
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.paid_data_qa, check_all=True)
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)

    # VALIDATE EXPIRED
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.paid_data_qa, check_all=False)
    io_list_page.wait_for_spinner_load()
    io_list_page.select_dropdown_value(IoListLocators.expired_data_qa, "Yes")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)
    io_list_page.select_dropdown_value(IoListLocators.expired_data_qa, "No")
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)

    # VALIDATE BILL STATUS
    io_list_page.clear_specific_filter_option_from_io_list_page(
        IoListLocators.expired_data_qa)
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.bill_status_data_qa, check_all=True)
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)

    # VALIDATE IO PERIOD
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.bill_status_data_qa, check_all=False)
    io_list_page.wait_for_spinner_load()
    current_month_year = io_list_page.get_current_date_with_specific_format(
        "%Y-%m")
    io_form_page.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=IoListLocators.io_period_data_qa,
                                                      option_to_select=current_month_year)
    io_list_page.wait_for_spinner_load()
    assert current_month_year in io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.io_date_label)

    previous_month_year = io_form_page.get_last_invoice_date("%Y-%m")
    io_form_page.select_from_modal_form_using_js_code(field_label_or_xpath_or_data_qa=IoListLocators.io_period_data_qa,
                                                      option_to_select=previous_month_year)
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE INVOICE PERIOD
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.io_period_data_qa, check_all=False)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.invoice_period_data_qa, option_to_select=current_month_year)
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE CREDIT INVOICE
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.invoice_period_data_qa, check_all=False)
    io_list_page.select_dropdown_value(IoListLocators.credit_invoice_data_qa, "No")
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    io_list_page.select_dropdown_value(IoListLocators.credit_invoice_data_qa, "Yes")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE IO SIGNED
    io_list_page.clear_specific_filter_option_from_io_list_page(
        IoListLocators.credit_invoice_data_qa)
    io_list_page.select_dropdown_value(IoListLocators.io_signed_data_qa, "No")
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    io_list_page.select_dropdown_value(IoListLocators.io_signed_data_qa, "Yes")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE RESPONSIBLE ADOPS
    io_list_page.clear_specific_filter_option_from_io_list_page(
        IoListLocators.io_signed_data_qa)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.responsible_adops_data_qa,
        option_to_select=io_data['client_profile']['client'])
    io_list_page.wait_for_spinner_load()
    assert io_data['client_profile'][
               'client'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.responsible_adops_label)

    # VALIDATE SALES PERSON
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.responsible_adops_data_qa, check_all=False)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.sales_person_data_qa,
        option_to_select=io_data['billing_entity']['sales_manager'])
    io_list_page.wait_for_spinner_load()
    assert io_data['billing_entity'][
               'sales_manager'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.sales_manager_label)

    # VALIDATE SALES TEAM
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.sales_person_data_qa, check_all=False)
    io_list_page.wait_for_spinner_load()
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.sales_team_data_qa, check_all=True)
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.sales_team_data_qa, check_all=False)
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)

    # VALIDATE ACCOUNT MANAGER
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.account_manager_data_qa, option_to_select="Eskimi - Alavi AM")
    io_list_page.wait_for_spinner_load()
    assert "Eskimi - Alavi AM" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.account_manager_label)

    # VALIDATE IO CAMPAIGN STATUS
    option_to_select = IoUtils.pull_io_campaign_status_from_db(io_number, db_connection)
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.account_manager_data_qa, check_all=False)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.io_campaign_status_data_qa, option_to_select=option_to_select)
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    assert option_to_select == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_status_label)

    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.io_campaign_status_data_qa, option_to_select="Closed (manually)")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE IO DEADLINE
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.io_campaign_status_data_qa, check_all=False)
    io_list_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.io_deadline_data_qa,
        option_to_select="Yes")
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    io_list_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.io_deadline_data_qa,
        option_to_select="No")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE IO EXECUTION COMMENT
    io_list_page.clear_specific_filter_option_from_io_list_page(
        IoListLocators.io_deadline_data_qa)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.io_execution_comment_data_qa,
        option_to_select=io_data['total_media_budget']['io_execution_comment'])
    io_list_page.wait_for_spinner_load()
    assert io_data['total_media_budget'][
               'io_execution_comment'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.io_execution_comment_label)
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)

    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoListLocators.io_execution_comment_data_qa,
        option_to_select="I: Not enough traffic")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    # VALIDATE IO WARNING MESSAGE
    io_list_page.check_uncheck_all_from_from_modal(IoListLocators.io_execution_comment_data_qa, check_all=False)
    io_list_page.select_from_modal_form_using_js_code(IoListLocators.io_warning_message_data_qa,
                                                      "Same campaigns under multi IOs")
    io_list_page.wait_for_spinner_load()
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    assert "Same campaigns under multi IOs" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.io_warning_label)
    io_list_page.select_dropdown_value(IoListLocators.io_warning_message_data_qa, "Overspend")
    io_list_page.wait_for_spinner_load()
    assert io_list_page.is_visible(
        IoListLocators.no_data_for_defined_criteria_locator)

    generic_modules.step_info(
        "[END - RTB-6988] Validate filter options are working properly in the IO list page individually")


def test_finance_io_list_page_columns_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    generic_modules.step_info(
        "[START - RTB-7075] Validate specific columns is showing proper value")

    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_data_and_save(io_data)
    io_number = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_date = io_form_page.get_selected_and_formatted_date(
        IoFormLocators.selected_date_locator)
    total_io_amount_in_usd = "$" + io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_io_amount_usd_info_data_qa)
    future_date = io_form_page.get_specific_date_with_specific_format(
        "%Y-%m-%d", days_to_add=6)
    yesterday_date = io_form_page.get_specific_date_with_specific_format(
        "%Y-%m-%d", days_to_subtract=1)

    io_form_page.click_on_element(
        IoFormLocators.media_budget_arrow_icon_data_qa.format("1"))
    io_form_page.click_on_element(IoFormLocators.period_field_data_qa)
    io_form_page.click_on_element(IoFormLocators.seven_days_option_locator)
    io_form_page.click_on_element(
        IoFormLocators.media_budget_plus_button_data_qa,
        locator_to_be_appeared=IoFormLocators.second_period_field_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.second_period_field_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.second_yesterday_option_locator)
    assert future_date == io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                 IoFormLocators.date_to_row_info_data_qa,
                                                                                 1)
    assert yesterday_date == io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                                    IoFormLocators.date_to_row_info_data_qa,
                                                                                    1)
    io_campaign_execution_comment = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.io_execution_comment_select_data_qa)
    io_form_page.check_uncheck_specific_checkbox(IoFormLocators.signed_io_check_data_qa, True)
    signed_io_checkbox_status = io_form_page.get_checkbox_status(IoFormLocators.signed_io_check_data_qa, value="1")

    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.create_invoice_button_data_qa,
        locator_to_be_appeared=InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
    # Commented out success notification verification, b/c https://eskimidev.atlassian.net/browse/RTB-9027
    # invoice_form_page.click_on_save_and_generate_invoice_button(
    #     locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button()
    invoice_number = "ENG " + io_form_page.get_text_using_tag_attribute(
        invoice_form_page.div_tag,
        invoice_form_page.class_attribute,
        InvoiceFormLocators.first_invoice_number_class)
    invoice_url = driver.current_url
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    assert io_number in io_list_page.get_element_text(
        IoListLocators.first_grid_item_locator)
    assert io_data['client_profile'][
               'client'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.client_label)
    assert io_data['billing_entity'][
               'sales_manager'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.sales_manager_label)
    assert io_data['billing_entity'][
               'sales_manager'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.sales_team_label)
    assert io_data['client_profile'][
               'responsible_adOps'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.responsible_adops_label)
    account_manager = IoUtils.pull_account_manager_from_db(
        io_data['client_profile']['client'], db_connection)
    assert account_manager == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.account_manager_label)
    # This assertion failed, registered a bug  https://eskimidev.atlassian.net/browse/RTB-9159
    # assert io_data['io_object'][
    #            'campaign'] == io_list_page.get_value_from_specific_grid_column(
    #     IoListLocators.campaigns_io_table_wrapper_div_id,
    #     IoListLocators.campaigns_label)
    assert io_date == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.io_date_label)
    assert future_date == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.deadline_label)
    formatted_amount = '₦{:,.2f}'.format(
        float(io_data['total_media_budget'][
                  'total_media_budget_amount']))
    assert formatted_amount == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.amount_label)
    assert total_io_amount_in_usd == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.amount_in_usd_label)
    assert io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.country_label) in io_data['billing_entity'][
               'company_profile']
    assert invoice_number == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.invoice_number_label)
    proforma_number = "PRO " + io_number
    assert proforma_number == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.proforma_label)
    assert "No" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.invoice_sent_label)
    driver.get(invoice_url)
    # Commented out success notification verification, b/c https://eskimidev.atlassian.net/browse/RTB-9027
    # io_list_page.click_on_element(
    #     InvoiceFormLocators.send_invoice_button_locator,
    #     locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    io_list_page.click_on_element(
        InvoiceFormLocators.send_invoice_button_locator)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    io_list_page.wait_for_spinner_load()
    assert "Pending" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.invoice_sent_label)
    assert io_campaign_execution_comment == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.io_execution_comment_label)
    assert signed_io_checkbox_status == io_list_page.get_checkbox_status_for_specific_checkbox(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    generic_modules.step_info(
        "[END - RTB-7075] Validate specific columns is showing proper value")


def test_finance_io_list_page_adjusted_io_amount_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    generic_modules.step_info(
        "[START - RTB-7087] Validate Adjusted IO amount column is showing proper data")

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data['client_profile']['client'] = "AutomationAgencyClientUser"
    io_data['io_object']['media_budget'] = "100"

    # CALCULATION
    bd_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        13, db_connection)
    margin = UserUtil.get_user_margin(7718, db_connection)
    agency_margin = UserUtil.get_user_agency_margin(7718, db_connection)
    io_amount = int(io_data['io_object']['media_budget'])
    io_amount_usd = io_amount / bd_currency_rate
    adjusted_io_amount = round(io_amount * (1 - margin / 100) + (
            io_amount * (1 - margin / 100) * agency_margin / 100),
                               2)
    adjusted_io_amount_usd = round(
        Decimal(io_amount_usd) * (1 - margin / 100) + (
                Decimal(io_amount_usd) * (
                1 - margin / 100) * agency_margin / 100),
        2)

    # IO CREATION
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_dropdown_value(IoFormLocators.company_profile_select_data_qa, "Eskimi BD")
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              io_data['io_object'][
                                                  'media_budget'])
    io_form_page.wait_for_spinner_load()
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    io_list_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.wait_for_spinner_load()
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, io_data['client_profile'][
        'client_company'])
    io_list_page.wait_for_spinner_load()
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    adjusted_io_amount_from_grid = io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.adjusted_io_amount_label)
    adjusted_io_amount_usd_from_grid = io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.adjusted_io_amount_usd_label)
    adjusted_io_amount_from_grid = \
        (adjusted_io_amount_from_grid.split('BDT'))[
            1]
    adjusted_io_amount_usd_from_grid = \
        (adjusted_io_amount_usd_from_grid.split('$'))[1]
    assert float(adjusted_io_amount) == float(adjusted_io_amount_from_grid)
    assert float(adjusted_io_amount_usd) == float(
        adjusted_io_amount_usd_from_grid)
    generic_modules.step_info(
        "[END - RTB-7087] Validate Adjusted IO amount column is showing proper data")


def test_finance_io_list_page_execution_comment_option_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    generic_modules.step_info(
        "[START - RTB-7123] Validate 'Edit execution comment (internal)' option from the three dot icon")

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_form_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.click_on_three_dot_and_action(io_id, action='edit execution comment (internal)')
    assert True is io_list_page.is_element_present(
        IoListLocators.execution_comment_form_locator)
    assert True is io_list_page.is_element_present(
        IoListLocators.update_execution_comment_button_locator)
    assert True is io_list_page.is_element_present(
        IoListLocators.cancel_button_locator)
    assert "1" == io_list_page.get_text_or_value_from_selected_option(
        IoListLocators.io_campaign_execution_comment_label, value=True)
    io_list_page.select_dropdown_value(IoListLocators.io_campaign_execution_comment_label,
                                       IoListLocators.other_comment_option)
    assert True is io_list_page.is_element_present(
        IoListLocators.comment_textarea_data_qa)
    io_list_page.select_dropdown_value(IoListLocators.io_campaign_execution_comment_label,
                                       IoListLocators.interim_invoice_option)
    assert False is io_list_page.is_element_displayed(
        IoListLocators.comment_textarea_data_qa)
    io_list_page.click_on_element(IoListLocators.cancel_button_locator)
    time.sleep(1)
    assert False is io_list_page.is_element_present(
        IoListLocators.execution_comment_form_locator)
    generic_modules.step_info(
        "[END - RTB-7123] Validate 'Edit execution comment (internal)' option from the three dot icon")

    generic_modules.step_info(
        "[START - RTB-7124] Validate 'Update execution comment' functionality")

    io_list_page.click_on_three_dot_and_action(io_id, action='edit execution comment (internal)')
    io_list_page.select_dropdown_value(IoListLocators.io_campaign_execution_comment_label,
                                       IoListLocators.interim_invoice_option)
    io_list_page.click_on_element(
        IoListLocators.update_execution_comment_button_locator)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert "Interim invoice" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.io_execution_comment_label)
    generic_modules.step_info(
        "[END - RTB-7124] Validate 'Update execution comment' functionality")


def test_finance_io_list_page_search_field_validation(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    generic_modules.step_info("[START - RTB-7107] Validate search field")

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    io_list_url = config['credential']['url'] + config['io-list-page']['io-list-url']

    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.create_invoice_button_data_qa,
        locator_to_be_appeared=InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    invoice_number = "ELT " + io_form_page.get_text_using_tag_attribute(
        invoice_form_page.div_tag,
        invoice_form_page.class_attribute,
        InvoiceFormLocators.first_invoice_number_class)
    driver.get(io_list_url)
    io_list_page.search_by_value(io_number)
    assert io_number in io_list_page.get_element_text(
        IoListLocators.first_grid_item_locator)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert io_data['io_main_information'][
               'io_title'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.title_label)
    io_list_page.search_by_value(io_data['client_profile']['client'])
    assert io_data['client_profile'][
               'client'] == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.client_label)
    io_list_page.search_by_value(invoice_number)
    assert invoice_number == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.invoice_number_label)
    proforma_number = "PRO " + io_number
    io_list_page.search_by_value(proforma_number)
    assert proforma_number == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.proforma_label)
    generic_modules.step_info("[END - RTB-7107] Validate search field")


def test_finance_io_list_page_campaign_dates_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    generic_modules.step_info(
        "[START - RTB-7094] Validate Campaign start date column is showing proper data")

    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    campaign_list = ['Glo jollificat8 (10832)', 'Glo Overload (10833)',
                     'Glo TGIF (10840)', 'GLO Sharp (10924)']

    # IO CREATION
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_multiple_item_from_modal(campaign_list, IoFormLocators.campaign_select_data_qa)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    # CAMPAIGN START DATE VALIDATION
    io_form_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    campaign_start_date = io_list_page.get_specific_date(campaign_list,
                                                         db_connection)
    assert campaign_start_date == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_start_date_label)
    generic_modules.step_info(
        "[END - RTB-7094] Validate Campaign start date column is showing proper data")

    generic_modules.step_info(
        "[START - RTB-7095] Validate Campaign end date column is showing proper data")

    # CAMPAIGN END DATE VALIDATION
    campaign_end_date = io_list_page.get_specific_date(campaign_list,
                                                       db_connection,
                                                       smallest=False)
    assert campaign_end_date == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_end_date_label)
    generic_modules.step_info(
        "[END - RTB-7095] Validate Campaign end date column is showing proper data")


def test_finance_io_list_page_paid_status_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    proforma_form = DspDashboardProformaForm(driver)

    generic_modules.step_info("[START - RTB-7093] Validate paid status")

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data['io_object']['media_budget'] = "100"
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    io_list_url = config['credential']['url'] + config['io-list-page']['io-list-url']

    # IO AND INVOICE CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.provide_io_object_info_using_js(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    proforma_number = "PRO " + io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.create_invoice_button_data_qa,
        locator_to_be_appeared=InvoiceFormLocators.save_and_generate_invoice_button_data_qa)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    invoice_number = "ELT " + io_form_page.get_text_using_tag_attribute(
        invoice_form_page.div_tag,
        invoice_form_page.class_attribute,
        InvoiceFormLocators.first_invoice_number_class)
    driver.get(io_list_url)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert f"No: {proforma_number}\nNo: {invoice_number}" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.paid_status_label)

    # PROFORMA AND INVOICE PARTLY PAYMENT ADDITION
    io_list_page.click_on_three_dot_and_action(io_id, action='proforma')
    proforma_form.click_on_element(
        ProformaFormLocators.add_payment_locator, locator_to_be_appeared=ProformaFormLocators.amount_paid_locator)
    proforma_form.set_value_into_specific_input_field(ProformaFormLocators.amount_paid_label, "60")
    time.sleep(2)
    proforma_form.click_on_element(
        ProformaFormLocators.save_add_payment_button_locator,
        locator_to_be_appeared=ProformaFormLocators.success_message_locator)
    proforma_form.click_on_element(
        ProformaFormLocators.invoices_xpath.format(invoice_number),
        locator_initialization=True,
        locator_to_be_appeared=InvoiceFormLocators.add_payment_locator)
    invoice_form_page.click_on_element(
        InvoiceFormLocators.add_payment_locator, locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
    invoice_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "60")
    time.sleep(2)
    invoice_form_page.click_on_element(
        InvoiceFormLocators.save_add_payment_button_locator,
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    driver.get(io_list_url)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert f"Partly: {proforma_number}\nPartly: {invoice_number}" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.paid_status_label)

    # PROFORMA AND INVOICE FULLY PAYMENT ADDITION
    io_list_page.click_on_three_dot_and_action(io_id, action='proforma')
    proforma_form.click_on_element(
        ProformaFormLocators.add_payment_locator, locator_to_be_appeared=ProformaFormLocators.amount_paid_locator)
    proforma_form.set_value_into_specific_input_field(ProformaFormLocators.amount_paid_label, "48.90")
    time.sleep(2)
    proforma_form.click_on_element(
        ProformaFormLocators.save_add_payment_button_locator,
        locator_to_be_appeared=ProformaFormLocators.success_message_locator)
    proforma_form.click_on_element(
        ProformaFormLocators.invoices_xpath.format(invoice_number),
        locator_initialization=True, locator_to_be_appeared=InvoiceFormLocators.add_payment_locator)
    invoice_form_page.click_on_element(
        InvoiceFormLocators.add_payment_locator, locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
    invoice_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "48.90")
    time.sleep(2)
    invoice_form_page.click_on_element(
        InvoiceFormLocators.save_add_payment_button_locator,
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    driver.get(io_list_url)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert f"Yes: {proforma_number}\nYes: {invoice_number}" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.paid_status_label)

    generic_modules.step_info("[END - RTB-7093] Validate paid status")


def test_finance_io_list_page_spent_column_verification(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data["io_object"][
        "campaign"] = "AJ Dig Deep campaign 16-25April (22885)"
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    io_list_url = config['credential']['url'] + config['io-list-page']['io-list-url']

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.provide_io_object_info_using_js(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    driver.get(io_list_url)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])

    ngn_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        102, db_connection)
    spent, spent_alt = IoUtils.pull_spent_and_spent_alt_data_for_specific_campaign_from_db(
        "22885", ngn_currency_rate, db_connection)
    margin_main = IoUtils.pull_margin_main_for_specific_campaign_from_db(
        "22885", db_connection)
    agency_margin = IoUtils.pull_agency_margin_for_specific_user_id_from_db(
        "1187", db_connection)
    spent_rm = DspDashboardIoList.get_campaign_spent_rm_amount(spent_alt,
                                                               margin_main,
                                                               agency_margin)
    spent_rm = "$" + "{:,.2f}".format(spent_rm)
    assert spent_rm == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.spent_amount_label)


def test_finance_io_list_page_campaign_status_validation(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    navbar = DashboardNavbar(driver)

    if 'http://rtb.local/admin' in driver.current_url:
        pytest.skip()
    generic_modules.step_info(
        "[START - RTB-7096] Validate Campaign status column is showing proper data")

    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data['io_object']['media_budget'] = "1500000"

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = \
        campaign_data['name_and_type'][
            'campaign_name'] + generic_modules.get_random_string(5)
    campaign_data['location_and_audiences']['audience_include'] = \
        "Behavioral (user interests) - Games - Tech (21,332,293 users)"
    campaign_data['location_and_audiences']['audience_exclude'] = \
        "Behavioral (user interests) - Business - Tech - Finance (22,893,227 users)"
    campaign_data['landing_and_creatives']['creative'] = "Samsung S23"
    current_day = io_form_page.get_current_date_with_specific_format(
        "%d %b, %Y")
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # CAMPAIGN CREATION
    campaign_settings_page.navigate_to_add_campaign_group()
    navbar.impersonate_user('Webcoupers - GLO')
    campaign_page.provide_mandatory_campaign_data_and_save(campaign_data,
                                                           "Save")

    # IO CREATION WITH STATUS "NOT LIVE"
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_form_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert "Not live" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_status_label)

    # IO EDITING WITH STATUS "ROTTEN"
    io_list_page.click_on_three_dot_and_action(io_id, action="edit io")
    time.sleep(1)
    io_form_page.set_value_into_element(IoFormLocators.io_date_data_qa,
                                        "01 Aug, 2023")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_form_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert "Rotten" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_status_label)

    # IO EDITING WITH STATUS "LIVE"
    campaign_live_dict = IoUtils.pull_campaign_with_specific_status_from_db(
        db_connection)
    if campaign_live_dict is not None:
        campaign_live1 = ' '.join((campaign_live_dict['name']).split()) + ' (' + str(campaign_live_dict['id']) + ')'
        io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
        campaign_live_list = [campaign_live1]
        io_form_page.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=IoFormLocators.campaign_select_data_qa,
            option_list_to_select=campaign_live_list)
        io_form_page.click_on_save_and_generate_io_button(
            locator_to_be_appeared=IoFormLocators.success_message_data_qa)
        io_form_page.click_on_element(
            IoFormLocators.back_to_list_locator, locator_to_be_appeared=IoListLocators.search_field_data_qa)
        io_list_page.search_by_title(
            io_data['io_main_information']['io_title'])
        assert "Live" == io_list_page.get_value_from_specific_grid_column(
            IoListLocators.campaigns_io_table_wrapper_div_id,
            IoListLocators.campaign_status_label)

    # IO EDITING WITH STATUS "PENDING"
    campaign_pending = [campaign_data['name_and_type']['campaign_name']]
    io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
    io_form_page.select_multiple_item_from_modal(campaign_pending, IoFormLocators.campaign_select_data_qa)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              io_data['io_object'][
                                                  'media_budget'])
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_form_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    assert "Pending" == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_status_label)

    if debug_mode:
        # IO CAMPAIGN STATUS PRIORITY VALIDATION
        if campaign_live_dict is not None:
            campaign_live = f"{campaign_live_dict['name']} ({campaign_live_dict['id']})"
            campaign_list = [campaign_live,
                             campaign_data['name_and_type'][
                                 'campaign_name']]
            io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
            io_form_page.check_uncheck_all_from_from_modal(IoFormLocators.campaign_select_data_qa, check_all=False)
            io_form_page.select_multiple_item_from_modal(campaign_list, IoFormLocators.campaign_select_data_qa)
            io_form_page.click_on_save_and_generate_io_button(
                locator_to_be_appeared=IoFormLocators.success_message_data_qa)
            io_form_page.click_on_element(
                IoFormLocators.back_to_list_locator, locator_to_be_appeared=IoListLocators.search_field_data_qa)
            io_list_page.search_by_title(
                io_data['io_main_information']['io_title'])
            io_campaign_status = io_list_page.get_io_campaign_status(
                io_data['io_main_information']['io_title'],
                db_connection, campaign_list)
            assert "Live" == io_campaign_status

            io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
            first_campaign = campaign_list[0]
            io_form_page.click_on_element(
                IoFormLocators.campaign_locator)
            time.sleep(2)
            io_form_page.check_uncheck_specific_checkbox(first_campaign, do_check=False, without_text=False)
            io_form_page.click_on_element(
                IoFormLocators.select_button_locator)
            del campaign_list[0]
            io_form_page.click_on_save_and_generate_io_button(
                locator_to_be_appeared=IoFormLocators.success_message_data_qa)
            io_form_page.click_on_element(
                IoFormLocators.back_to_list_locator, locator_to_be_appeared=IoListLocators.search_field_data_qa)
            io_list_page.search_by_title(
                io_data['io_main_information']['io_title'])
        else:
            campaign_list = [campaign_data['name_and_type'][
                                 'campaign_name']]
        io_campaign_status = io_list_page.get_io_campaign_status(
            io_data['io_main_information']['io_title'],
            db_connection, campaign_list)
        assert "Pending" == io_campaign_status

        io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
        del campaign_list[0]
        time.sleep(2)
        io_form_page.check_uncheck_all_from_from_modal(IoFormLocators.campaign_select_data_qa, check_all=False)
        io_form_page.click_on_save_and_generate_io_button(
            locator_to_be_appeared=IoFormLocators.success_message_data_qa)
        io_form_page.click_on_element(
            IoFormLocators.back_to_list_locator, locator_to_be_appeared=IoListLocators.search_field_data_qa)
        io_list_page.search_by_title(
            io_data['io_main_information']['io_title'])
        io_campaign_status = io_list_page.get_io_campaign_status(
            io_data['io_main_information']['io_title'],
            db_connection, campaign_list)
        assert "Rotten" == io_campaign_status

        io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
        time.sleep(1)
        io_form_page.set_value_into_element(
            IoFormLocators.io_date_data_qa,
            current_day)
        io_form_page.click_on_save_and_generate_io_button(
            locator_to_be_appeared=IoFormLocators.success_message_data_qa)
        io_form_page.click_on_element(
            IoFormLocators.back_to_list_locator, locator_to_be_appeared=IoListLocators.search_field_data_qa)
        io_list_page.search_by_title(
            io_data['io_main_information']['io_title'])
        io_campaign_status = io_list_page.get_io_campaign_status(
            io_data['io_main_information']['io_title'],
            db_connection, campaign_list)
        assert "Not live" == io_campaign_status

    generic_modules.step_info(
        "[START - RTB-7096] Validate Campaign status column is showing proper data")


def test_finance_io_list_page_left_to_spent_verification(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    generic_modules.step_info(
        "[START - RTB-7098] Validate Left to spent column is showing proper data")

    with open('assets/io/io_webcoupers_glo_client_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data["io_object"]["campaign"] = "Glo Overload (10833)"
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    io_list_url = config['credential']['url'] + config['io-list-page']['io-list-url']

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.provide_io_object_info_using_js(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    driver.get(io_list_url)
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])

    left_spent = io_list_page.get_campaign_left_to_spend_amount(
        io_data['io_main_information']['io_title'],
        db_connection)
    left_spent = "$" + "{:,.2f}".format(left_spent)
    print(left_spent)
    assert left_spent == io_list_page.get_value_from_specific_grid_column(
        IoListLocators.campaigns_io_table_wrapper_div_id,
        IoListLocators.campaign_left_to_spent)

    generic_modules.step_info(
        "[END - RTB-7098] Validate Left to spent column is showing proper data")


def test_finance_io_list_page_signed_io_column_verification(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_list_page = DspDashboardIoList(driver)
    io_form_page = DspDashboardIoForm(driver)

    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # IO CREATION
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)

    # SEARCH FOR THE CREATED IO AND CHECK THE SIGNED IO CHECKBOX
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    io_list_page.scroll_to_specific_element(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    io_list_page.click_on_element(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    assert 'True' == io_list_page.get_checkbox_status_for_specific_checkbox(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))

    # ASSERT THAT SIGNED IO CHECKBOX IS CHECKED FROM THE IO FORM PAGE
    io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
    assert 'True' == io_form_page.get_checkbox_status(IoFormLocators.signed_io_check_data_qa)

    # RETURN TO IO LIST PAGE
    io_form_page.click_on_element(IoFormLocators.back_to_list_locator,
                                  locator_to_be_appeared=IoListLocators.search_field_data_qa)

    # SEARCH FOR THE CREATED IO AND UN-CHECK THE SIGNED IO CHECKBOX
    io_list_page.search_by_title(
        io_data['io_main_information']['io_title'])
    io_list_page.scroll_to_specific_element(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    io_list_page.click_on_element(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))
    assert '' == io_list_page.get_checkbox_status_for_specific_checkbox(
        IoListLocators.signed_io_checkbox_data_qa.format(io_id))

    # ASSERT THAT SIGNED IO CHECKBOX IS UN-CHECKED FROM THE IO FORM PAGE
    io_list_page.click_on_three_dot_and_action(io_id, action='edit io')
    assert '' == io_form_page.get_checkbox_status(IoFormLocators.signed_io_check_data_qa)
