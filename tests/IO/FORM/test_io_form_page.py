import copy
import json
import os
import time

import pytest
import pytz
from selenium.webdriver import Keys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

from configurations import generic_modules
from locators.billing_entities.billing_entities_form_locators import \
    BillingEntitiesFormLocators
from locators.company.company_form_locators import CompanyFormLocators
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.invoice_list_locator import InvoiceListLocators
from locators.io.io_form_locator import IoFormLocators
from locators.io.io_list_locator import IoListLocators
from locators.io.proforma_form_locator import ProformaFormLocators
from locators.user.userform_locators import UserFormLocators
from pages.io.invoice_form import DspDashboardInvoiceForm
from pages.io.invoice_list import DspDashboardInvoiceList
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.io.proforma_form import DspDashboardProformaForm
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.user.user_form import DashboardUserFormPage
from utils.campaigns import CampaignUtils
from utils.compare import CompareUtils as CompareUtil
from utils.currency import CurrencyUtils
from utils.io import IoUtils
from utils.page_names_enum import PageNames

date_format = "%d %b, %Y"
all_data_verification_message = "All data verification is successful"
debug_mode = "JENKINS_URL" not in os.environ


def test_finance_io_form_page(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_list = DspDashboardInvoiceList(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    # PROVIDED IO DATA IN GUI
    global date_format, all_data_verification_message
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    # GETTING AND STORING INFO
    with open('assets/io/profile_finance_status_data.json') as json_file:
        profile_finance_status_data = json.load(json_file)
    pulled_profile_finance_status_data_from_gui = copy.deepcopy(
        profile_finance_status_data)

    company_profile_url = config['credential']['url'] + \
                          profile_finance_status_data[
                              'profile_finance_data'][
                              'company_profile_url']
    driver.get(company_profile_url)
    profile_finance_status_data['profile_finance_data'][
        'discount'] = io_form_page.get_element_text(
        CompanyFormLocators.company_discount_locator,
        input_tag=True) + "%"
    profile_finance_status_data['profile_finance_data'][
        'bonus'] = io_form_page.get_element_text(
        CompanyFormLocators.company_bonus_locator,
        input_tag=True) + "%"
    profile_finance_status_data['profile_finance_data'][
        'tax'] = io_form_page.get_element_text(
        CompanyFormLocators.company_tax_locator,
        input_tag=True) + "%(i.e. WHT)"
    profile_finance_status_data['profile_finance_data'][
        'last_payment'] = io_form_page.get_current_date_with_specific_format(
        date_format)
    final_credit_limit = io_form_page.get_element_text(
        CompanyFormLocators.final_credit_limit_locator, input_tag=True)
    final_credit_limit = float(final_credit_limit.replace(",", ""))
    io_list_page.wait_for_spinner_load()
    final_credit_limit = " / $" + "{:.2f}".format(final_credit_limit)

    generic_modules.step_info(
        "[START - RTB-6610] Validate whether the user is not able to create IO without filling up the mandatory fields")
    driver.get(io_creation_url)
    io_form_page.click_on_element(IoFormLocators.date_field_data_qa)
    io_form_page.wait_for_presence_of_element(
        IoFormLocators.date_field_data_qa).send_keys(
        Keys.COMMAND + 'a')
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.wait_for_presence_of_element(
        IoFormLocators.date_field_data_qa).send_keys(Keys.DELETE)
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.set_value_into_specific_input_field(IoFormLocators.io_date_data_qa, " ", tab_out=True)
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.define_missing_fields_warning_message_locator)
    assert True is io_form_page.is_element_present(
        IoFormLocators.define_missing_fields_warning_message_locator)
    io_form_page.click_on_specific_button(IoFormLocators.close_label)
    generic_modules.step_info(
        "[END - RTB-6610] Validate whether the user is not able to create IO without filling up the mandatory fields")

    generic_modules.step_info(
        "[START - RTB-6611] Validate whether the user is able to generate IO just by filling up the mandatory fields \n"
        "[START - RTB-6609] Validate Profile finance status are available in the io form page \n"
        "[START - RTB-6824] Validate whether proper Profile finance status information is showing in the IO form page")
    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.set_value_into_specific_input_field(IoFormLocators.io_date_data_qa,
                                                     io_form_page.get_current_date_with_specific_format(
                                                         "%d %b, %Y"), tab_out=True)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoFormLocators.campaign_select_data_qa,
        option_to_select=io_data['io_object']['campaign'])
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format(1),
                                              io_data['io_object'][
                                                  'media_budget'])
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # CREATING INVOICE ADDING PAYMENT
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    io_form_page.click_on_specific_button(InvoiceFormLocators.add_payment_button,
                                          locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
    io_form_page.wait_for_visibility_of_element(
        InvoiceFormLocators.paid_amount_field_locator)
    io_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "1")
    io_form_page.click_on_specific_button(InvoiceFormLocators.save_button,
                                          locator_to_be_appeared=InvoiceFormLocators.success_message_locator)

    # GETTING INVOICE LAST DATE FROM INVOICE LIST PAGE
    sidebar_navigation.navigate_to_page(PageNames.INVOICE)
    invoice_list.select_dropdown_value(InvoiceListLocators.client_account_label, io_data['client_profile']['client'])
    invoice_list.wait_for_spinner_load()
    invoice_list.select_dropdown_value(InvoiceListLocators.rows_per_page_label, InvoiceListLocators.all_option)
    profile_finance_status_data['profile_finance_data'][
        'last_invoice'] = invoice_list.get_last_invoice_date_from_list(
        InvoiceListLocators.invoice_list_date_locator)

    # GETTING OPEN IOS, CREDIT LIMIT LEVEL, FINANCE BALANCE & OPEN IOS AMOUNT
    driver.get(io_url)
    bd_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        13, db_connection)
    open_ios, io_amounts = IoUtils.pull_open_ios_from_db(db_connection)
    finance_balances = IoUtils.pull_finance_balances_from_db(db_connection)
    open_io_string = ""
    if len(open_ios) > 0:
        for open_io in open_ios:
            open_io_string += (str(open_io).split("."))[0]
            if open_ios[len(open_ios) - 1] != open_io:
                open_io_string += ", "
    profile_finance_status_data['profile_finance_data'][
        'open_ios'] = open_io_string

    io_amount_list = []
    if len(io_amounts) > 0:
        for io_amount in io_amounts:
            io_amount_string = (str(io_amount)).replace(
                "[", "").replace('"', "").replace("]", "")
            io_amount_values = io_amount_string.split(',')
            if len(io_amount_values) > 1:
                for value in io_amount_values:
                    io_amount_list.append(float(value))
            else:
                io_amount_list.append(str(io_amount_values[0]))
    open_io_amount = sum(map(float, io_amount_list))

    total_finance_balances = sum(map(float, finance_balances))
    credit_limit_level = open_io_amount + total_finance_balances
    profile_finance_status_data['profile_finance_data'][
        'open_ios_amount'] = "$" + io_form_page.round_up_half_float(open_io_amount)
    profile_finance_status_data['profile_finance_data'][
        'finance_balance'] = "$" + io_form_page.round_up_half_float(total_finance_balances)
    profile_finance_status_data['profile_finance_data'][
        'credit_limit_level'] = "$" + io_form_page.round_up_half_float(credit_limit_level) + final_credit_limit
    profile_finance_status_data['profile_finance_data']['currency_rate'] = \
        profile_finance_status_data['profile_finance_data'][
            'currency_rate'] + io_form_page.round_up_half_float(bd_currency_rate)

    # DATA VERIFICATION
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'credit_limit_level'] = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.credit_limit_info_data_qa).replace(",", "")
    # pulled_profile_finance_status_data_from_gui['profile_finance_data'][
    #     'overdue'] = io_form_page.get_specific_finance_profile_status(
    #     IoFormLocators.overdue_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'finance_balance'] = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.finance_balance_info_data_qa).replace(",", "")
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'open_ios_amount'] = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.open_ios_amount_info_data_qa).replace(",", "")
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'open_ios'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.open_ios_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'last_invoice'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.last_invoice_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'last_payment'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.last_payment_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'discount'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.discount_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'rebate'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.rebate_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'bonus'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.bonus_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'tax'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.tax_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'currency_rate'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.currency_rate_label)
    assert generic_modules.ordered(
        pulled_profile_finance_status_data_from_gui) == generic_modules.ordered(
        profile_finance_status_data)

    pulled_io_data_gui = copy.deepcopy(io_data)
    pulled_io_data_gui['io_main_information'][
        'io_title'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.io_title_input_data_qa)
    # pulled_io_data_gui['client_profile'][
    #     'client'] = io_form_page.get_text_using_tag_attribute(
    #     io_form_page.span_tag, io_form_page.id_attribute,
    #     IoFormLocators.select2_client_container_id)
    pulled_io_data_gui['client_profile'][
        'client'] = io_form_page.get_selected_options_using_js_code(IoFormLocators.client_select_data_qa)
    pulled_io_data_gui['client_profile'][
        'email'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.email_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'contact'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.contact_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'responsible_adOps'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.responsible_adops_input_data_qa)
    assert generic_modules.ordered(
        pulled_io_data_gui) == generic_modules.ordered(io_data)
    generic_modules.step_info(
        "[END - RTB-6611] Validate whether the user is able to generate IO just by filling up the mandatory fields \n"
        "[END - RTB-6609] Validate Profile finance status are available in the io form page \n"
        "[END - RTB-6824] Validate whether proper Profile finance status information is showing in the IO form page")


def test_finance_io_form_page_two(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']

    generic_modules.step_info(
        "[START - RTB-6649] Validate whether the Responsible AdOps, Client company, Company profile, Payment term "
        "(days) and Currency rate fields are readonly")
    navbar.login_as("AutomationAgencyUser")
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.responsible_adops_input_data_qa)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.client_company_select_data_qa)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.company_profile_select_data_qa)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.currency_rate_label, is_input_field=True)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.payment_term_days_input_data_qa,
                                                           is_input_field=True)

    navbar.logout_as()
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.responsible_adops_input_data_qa)
    assert True is io_form_page.is_specific_field_enabled(IoFormLocators.client_company_select_data_qa)
    assert True is io_form_page.is_specific_field_enabled(IoFormLocators.company_profile_select_data_qa)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.currency_rate_label, is_input_field=True)
    assert True is io_form_page.is_specific_field_enabled(IoFormLocators.payment_term_days_input_data_qa,
                                                          is_input_field=True)
    generic_modules.step_info(
        "[END - RTB-6649] Validate whether the Responsible AdOps, Client company, Company profile, Payment term "
        "(days) and Currency rate fields are readonly")

    generic_modules.step_info(
        "[START - RTB-6655] Validate whether some fields are being auto-filled based on the selection of the Client")

    pulled_io_data_gui = copy.deepcopy(io_data)
    pulled_io_data_gui['client_profile'][
        'client'] = io_form_page.get_selected_options_using_js_code(IoFormLocators.client_select_data_qa)
    pulled_io_data_gui['client_profile'][
        'email'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.email_input_data_qa).lower()
    pulled_io_data_gui['client_profile'][
        'contact'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.contact_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'responsible_adOps'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.responsible_adops_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'client_company'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.client_company_select_data_qa)
    pulled_io_data_gui['billing_entity'][
        'company_profile'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.company_profile_select_data_qa)
    pulled_io_data_gui['billing_entity'][
        'sales_manager'] = io_form_page.get_selected_options_using_js_code(IoFormLocators.sales_manager_select_data_qa)
    pulled_io_data_gui['billing_information'][
        'currency'] = io_form_page.get_selected_options_using_js_code(IoFormLocators.currency_select_data_qa)
    currency_rate = io_form_page.get_value_from_specific_input_field(IoFormLocators.currency_rate_label)
    split_currency_rate = currency_rate.split(".")
    pulled_io_data_gui['billing_information']['currency_rate'] = \
        split_currency_rate[0]
    print(generic_modules.ordered(pulled_io_data_gui))
    print(generic_modules.ordered(io_data))
    assert all_data_verification_message == CompareUtil.verify_data(
        pulled_io_data_gui, io_data)
    generic_modules.step_info(
        "[END - RTB-6655] Validate whether some fields are being auto-filled based on the selection of the Client")

    generic_modules.step_info(
        "[START - RTB-6656] Validate whether the FinAdmin users are able to add multiple client company under "
        "Client Company dropdown and some fields are being auto updated based on the company selection")
    generic_modules.step_info(
        "[START - RTB-6658] Validate whether the finAdmin type users are able to change Company Profile. "
        "And Currency is also changing based on the selection of company profile")

    ngn_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        102, db_connection)
    test_data = {'client_company': 'Webcoupers',
                 'company_profile': 'Eskimi NG-NG',
                 'currency': 'Nigeria Naira (NGN)',
                 'currency_rate': int(ngn_currency_rate)}
    io_form_page.select_dropdown_value(IoFormLocators.client_company_select_data_qa, test_data['client_company'])
    io_form_page.wait_alert_is_present()
    alert_text = io_form_page.get_alert_text()
    io_form_page.accept_alert()
    pulled_test_data = copy.deepcopy(test_data)
    pulled_test_data[
        'client_company'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.client_company_select_data_qa)
    pulled_test_data[
        'company_profile'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.company_profile_select_data_qa)
    pulled_test_data[
        'currency'] = io_form_page.get_selected_options_using_js_code(IoFormLocators.currency_select_data_qa)
    io_form_page.wait_for_spinner_load()
    if 'http://rtb.local/admin' in driver.current_url:
        pulled_test_data['currency_rate'] = round(float(
            io_form_page.get_value_from_specific_input_field(IoFormLocators.currency_rate_label, inner_html=True)))
        pulled_test_data['currency_rate'] = int(pulled_test_data['currency_rate'])
    else:
        pulled_test_data['currency_rate'] = int(
            io_form_page.get_value_from_specific_input_field(IoFormLocators.currency_rate_label, inner_html=True))
    print(pulled_test_data)
    print(test_data)
    assert pulled_test_data == test_data
    generic_modules.step_info(
        "[END - RTB-6656] Validate whether the FinAdmin users are able to add multiple client company under "
        "Client Company dropdown and some fields are being auto updated based on the company selection")
    generic_modules.step_info(
        "[END - RTB-6658] Validate whether the finAdmin type users are able to change Company Profile. "
        "And Currency is also changing based on the selection of company profile")

    generic_modules.step_info(
        "[START - RTB-6657] Validate whether the FinAdmin users are getting proper warning message while trying "
        "to change the client company with different company profile and currency")
    assert "Company profile usual currency and selected currency doesn't match" == alert_text
    generic_modules.step_info(
        "[END - RTB-6657] Validate whether the FinAdmin users are getting proper warning message while trying "
        "to change the client company with different company profile and currency")


def test_finance_io_form_page_three(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6659] Validate whether the users are able to select multiple campaigns from the Campaign field")
    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    campaign_list = [
        'MassEditAndDuplicateAutomationBannerCampaign01 (111248)',
        'MassEditAndDuplicateAutomationBannerCampaign02 (111250)']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_multiple_item_from_modal(campaign_list, IoFormLocators.campaign_select_data_qa)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    time.sleep(5)
    campaigns_from_gui = io_form_page.get_selected_options_using_js_code(IoFormLocators.campaign_select_data_qa)
    assert campaigns_from_gui == campaign_list
    if io_form_page.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        io_form_page.click_on_specific_button(IoFormLocators.delete_label)
        io_form_page.wait_alert_is_present()
        alert = driver.switch_to.alert
        alert.accept()

    navbar.login_as("AutomationAgencyUser")
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_multiple_item_from_modal(campaign_list, IoFormLocators.campaign_select_data_qa)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    time.sleep(5)
    campaigns_from_gui_2 = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.campaign_select_data_qa)
    # Commenting out because it fails sometimes, registered a bug https://eskimidev.atlassian.net/browse/RTB-9161
    # assert campaigns_from_gui_2 == campaign_list
    navbar.logout_as()
    generic_modules.step_info(
        "[END - RTB-6659] Validate whether the users are able to select multiple campaigns from the Campaign field")

    generic_modules.step_info(
        "[START - RTB-6660] Validate whether the media budget table is populating with proper information")
    test_data = {'media_budget': '12.00', 'channel': 'DSP',
                 'country': 'Bangladesh', 'from_date': '', 'due_date': '',
                 'campaign_type': 'CPM', 'impressions': '111',
                 'media_rate': "{:.2f}".format((12 / 111) * 1000)}
    current_date = io_form_page.get_current_date_with_specific_format(
        "%Y-%m-%d")
    future_date = io_form_page.get_specific_date_with_specific_format(
        "%Y-%m-%d", days_to_add=6)
    test_data['from_date'] = current_date
    test_data['due_date'] = future_date
    io_form_page.click_on_element(
        IoFormLocators.media_budget_arrow_icon_data_qa.format("1"))
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              test_data['media_budget'])
    io_form_page.click_on_element(IoFormLocators.channel_dropdown_locator)
    io_form_page.set_value_into_element(
        IoFormLocators.channel_text_field_locator,
        test_data['channel'] + Keys.ENTER)
    io_form_page.select_dropdown_value(IoFormLocators.country_select_data_qa, test_data['country'])
    io_form_page.click_on_element(IoFormLocators.period_field_data_qa,
                                  locator_to_be_appeared=IoFormLocators.seven_days_option_locator)
    io_form_page.click_on_element(IoFormLocators.seven_days_option_locator)
    io_form_page.wait_for_spinner_load()
    io_form_page.select_dropdown_value(IoFormLocators.campaign_type_select_data_qa, test_data['campaign_type'])
    io_form_page.set_value_into_specific_input_field(IoFormLocators.goal_input_data_qa.format("1"), test_data[
        'impressions'],
                                                     tab_out=True)
    test_data_from_gui = copy.deepcopy(test_data)
    test_data_from_gui[
        'channel'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                            IoFormLocators.channel_info_data_qa, 1)
    test_data_from_gui[
        'country'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                            IoFormLocators.country_row_info_data_qa, 1)
    test_data_from_gui[
        'from_date'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                              IoFormLocators.date_from_row_info_data_qa,
                                                                              1)
    test_data_from_gui[
        'due_date'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                             IoFormLocators.date_to_row_info_data_qa, 1)
    test_data_from_gui[
        'campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                  IoFormLocators.campaign_type_info_data_qa,
                                                                                  1)
    test_data_from_gui[
        'impressions'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                IoFormLocators.goal_info_data_qa, 1)
    test_data_from_gui[
        'media_rate'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                               IoFormLocators.cpm_rate_info_data_qa, 1)
    test_data_from_gui[
        'media_budget'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                 IoFormLocators.total_currency_info_data_qa,
                                                                                 1)
    assert test_data_from_gui == test_data

    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    driver.get(io_url)
    test_data_from_gui_1 = copy.deepcopy(test_data)
    test_data_from_gui_1[
        'channel'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                            IoFormLocators.channel_info_data_qa, 1)
    test_data_from_gui_1[
        'country'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                            IoFormLocators.country_row_info_data_qa, 1)
    test_data_from_gui_1[
        'from_date'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                              IoFormLocators.date_from_row_info_data_qa,
                                                                              1)
    test_data_from_gui_1[
        'due_date'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                             IoFormLocators.date_to_row_info_data_qa, 1)
    test_data_from_gui_1[
        'campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                  IoFormLocators.campaign_type_info_data_qa,
                                                                                  1)
    test_data_from_gui_1[
        'impressions'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                IoFormLocators.goal_info_data_qa, 1)
    test_data_from_gui_1[
        'media_rate'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                               IoFormLocators.cpm_rate_info_data_qa, 1)
    test_data_from_gui_1[
        'media_budget'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial1_id,
                                                                                 IoFormLocators.total_currency_info_data_qa,
                                                                                 1)
    assert test_data_from_gui_1 == test_data
    generic_modules.step_info(
        "[END - RTB-6660] Validate whether the media budget table is populating with proper information")

    generic_modules.step_info(
        "[START - RTB-6711] Validate whether the users are able to add multiple media budget")
    test_data_2 = {'media_budget': '100.00', 'channel': 'DSP display',
                   'country': 'Afghanistan',
                   'from_date': current_date, 'due_date': future_date,
                   'campaign_type': 'CPC', 'clicks': '111',
                   'media_rate': "{:.2f}".format((100 / 111))}
    io_form_page.click_on_element(
        IoFormLocators.media_budget_plus_button_data_qa,
        locator_to_be_appeared=IoFormLocators.media_budget_arrow_data_qa)
    io_form_page.click_on_element(
        IoFormLocators.media_budget_arrow_icon_data_qa.format("2"))
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("2"),
                                              test_data_2['media_budget'])
    io_form_page.click_on_element(IoFormLocators.channel_dropdown_locator)
    io_form_page.set_value_into_element(
        IoFormLocators.channel_text_field_locator,
        test_data_2['channel'] + Keys.ENTER)
    io_form_page.select_dropdown_value(IoFormLocators.second_country_select_data_qa, test_data_2['country'])
    io_form_page.wait_for_spinner_load()
    io_form_page.select_dropdown_value(IoFormLocators.second_campaign_type_select_data_qa, test_data_2['campaign_type'])
    io_form_page.set_value_into_specific_input_field(IoFormLocators.goal_input_data_qa.format("2"), test_data_2[
        'clicks'],
                                                     tab_out=True)
    test_data_from_gui_3 = copy.deepcopy(test_data_2)
    test_data_from_gui_3[
        'channel'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                            IoFormLocators.channel_info_data_qa, 1)
    test_data_from_gui_3[
        'country'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                            IoFormLocators.country_row_info_data_qa, 1)
    test_data_from_gui_3['from_date'] = current_date
    test_data_from_gui_3['due_date'] = future_date
    test_data_from_gui_3[
        'campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                                  IoFormLocators.campaign_type_info_data_qa,
                                                                                  1)
    test_data_from_gui_3[
        'clicks'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                           IoFormLocators.goal_info_data_qa, 1)
    test_data_from_gui_3[
        'media_rate'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                               IoFormLocators.cpm_rate_info_data_qa, 1)
    test_data_from_gui_3[
        'media_budget'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                                 IoFormLocators.total_currency_info_data_qa,
                                                                                 1)
    assert test_data_from_gui_3 == test_data_2

    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    test_data_from_gui_4 = copy.deepcopy(test_data_2)
    test_data_from_gui_4[
        'channel'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                            IoFormLocators.channel_info_data_qa, 1)
    test_data_from_gui_4[
        'country'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                            IoFormLocators.country_row_info_data_qa, 1)
    test_data_from_gui_4['from_date'] = current_date
    test_data_from_gui_4['due_date'] = future_date
    test_data_from_gui_4[
        'campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                                  IoFormLocators.campaign_type_info_data_qa,
                                                                                  1)
    test_data_from_gui_4[
        'clicks'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                           IoFormLocators.goal_info_data_qa, 1)
    test_data_from_gui_4[
        'media_rate'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                               IoFormLocators.cpm_rate_info_data_qa, 1)
    test_data_from_gui_4[
        'media_budget'] = io_form_page.get_text_from_specific_media_budget_table(IoFormLocators.tr_serial2_id,
                                                                                 IoFormLocators.total_currency_info_data_qa,
                                                                                 1)
    assert test_data_from_gui_4 == test_data_2
    generic_modules.step_info(
        "[END - RTB-6711] Validate whether the users are able to add multiple media budget")

    generic_modules.step_info(
        "[START - RTB-6713] Validate whether the Total media budget amount is showing proper data based on the added media budget")
    assert "112.00" == io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag, io_form_page.data_qa_attribute,
        IoFormLocators.total_media_budget_info_data_qa)
    generic_modules.step_info(
        "[END - RTB-6713] Validate whether the Total media budget amount is showing proper data based on the added media budget")

    generic_modules.step_info(
        "[START - RTB-6712] Validate whether the users are able to remove media budget")
    io_form_page.click_on_element(IoFormLocators.media_budget_remove_icon_data_qa.format("2"))
    assert False is io_form_page.is_element_present(
        IoFormLocators.second_media_budget_table_locator, time_out=1)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    driver.get(io_url)
    assert False is io_form_page.is_element_present(
        IoFormLocators.second_media_budget_table_locator, time_out=1)
    generic_modules.step_info(
        "[END - RTB-6712] Validate whether the users are able to remove media budget")


@pytest.mark.dependency()
def test_finance_io_form_page_four(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    user_form_page = DashboardUserFormPage(driver)
    navbar = DashboardNavbar(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page']['io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.provide_io_total_media_budget_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_url = driver.current_url

    if debug_mode:
        generic_modules.step_info(
            "[START - RTB-6714] Validate whether the FinAdmin users are able to edit IO-campaign execution comment (internal)")

        automation_admin_user_settings_url = config['credential']['url'] + \
                                             config['user-settings-pages'][
                                                 'automation-admin-user']

        try:
            # CHANGING THE USER SETTINGS
            driver.get(automation_admin_user_settings_url)
            io_form_page.click_on_element(
                UserFormLocators.billing_settings_locator)
            io_form_page.wait_for_spinner_load()
            io_form_page.click_on_element(
                UserFormLocators.finance_options_section_expand_icon_locator)
            user_form_page.check_uncheck_checkbox(
                UserFormLocators.billing_all_io_proforma_invoice_checkbox_data_qa,
                False)
            user_form_page.check_uncheck_checkbox(
                UserFormLocators.billing_invoice_create_and_view_its_clients_checkbox_data_qa,
                True)
            user_form_page.check_uncheck_checkbox(
                UserFormLocators.billing_io_view_its_clients_only_checkbox_data_qa,
                True)
            user_form_page.check_uncheck_checkbox(
                UserFormLocators.add_execution_comment_to_io_invoice_proforma_checkbox_data_qa,
                False)
            io_form_page.click_on_element(
                UserFormLocators.save_button_locator)

            # CHECKING IO EXECUTION COMMENT FIELD
            driver.get(io_url)
            io_execution_comment = io_form_page.get_selected_options_using_js_code(
                IoFormLocators.io_execution_comment_select_data_qa)
            assert io_execution_comment == io_data['total_media_budget'][
                'io_execution_comment']
            generic_modules.step_info(
                "[END - RTB-6714] Validate whether the FinAdmin users are able to edit IO-campaign execution comment (internal)")
        finally:
            driver.get(automation_admin_user_settings_url)
            io_form_page.click_on_element(
                UserFormLocators.billing_settings_locator)
            io_form_page.wait_for_spinner_load()
            io_form_page.click_on_element(
                UserFormLocators.finance_options_section_expand_icon_locator)
            user_form_page.click_on_element(UserFormLocators.check_all_billing_button_data_qa)
            io_form_page.click_on_element(
                UserFormLocators.save_button_locator)

    generic_modules.step_info(
        "[START - RTB-6716] Validate whether the Non FinAdmin users are not being able to edit IO-campaign execution comment (internal)")
    automation_agency_user_settings_url = config['credential']['url'] + \
                                          config['user-settings-pages'][
                                              'automation-agency-user']

    try:
        # CHANGING THE USER SETTINGS
        driver.get(automation_agency_user_settings_url)
        io_form_page.click_on_element(
            UserFormLocators.billing_settings_locator)
        io_form_page.wait_for_spinner_load()
        io_form_page.click_on_element(
            UserFormLocators.finance_options_section_expand_icon_locator)
        user_form_page.check_uncheck_checkbox(
            UserFormLocators.billing_all_io_proforma_invoice_checkbox_data_qa,
            False)
        user_form_page.check_uncheck_checkbox(
            UserFormLocators.billing_clients_management_margins_checkbox_data_qa,
            False)
        user_form_page.check_uncheck_checkbox(
            UserFormLocators.billing_invoice_create_and_view_its_clients_checkbox_data_qa,
            False)
        user_form_page.check_uncheck_checkbox(
            UserFormLocators.billing_io_view_its_clients_only_checkbox_data_qa,
            True)
        user_form_page.check_uncheck_checkbox(
            UserFormLocators.add_execution_comment_to_io_invoice_proforma_checkbox_data_qa,
            False)
        io_form_page.click_on_element(
            UserFormLocators.save_button_locator)

        # CHECKING IO EXECUTION COMMENT FIELD
        navbar.login_as("AutomationAgencyUser")
        sidebar_navigation.navigate_to_page(PageNames.IO)
        io_form_page.wait_for_spinner_load()
        io_list_page.wait_for_visibility_of_element(
            IoListLocators.first_grid_item_locator)
        io_list_page.search_by_title(
            io_data['io_main_information']['io_title'])
        io_form_page.wait_for_spinner_load()
        assert False is io_form_page.is_element_present(
            IoListLocators.io_number_link_xpath.format(
                io_data['io_main_information']['io_title']), 1,
            locator_initialization=True)
        io_list_page.click_on_three_dot_and_action(io_id)
        assert False is io_form_page.is_element_present(
            IoListLocators.edit_execution_comment_data_qa.format(io_id))
        navbar.logout_as()
        generic_modules.step_info(
            "[END - RTB-6716] Validate whether the Non FinAdmin users are not being able to edit IO-campaign execution comment (internal)")
    finally:
        driver.get(automation_agency_user_settings_url)
        io_form_page.click_on_element(
            UserFormLocators.billing_settings_locator)
        io_form_page.wait_for_spinner_load()
        io_form_page.click_on_element(
            UserFormLocators.finance_options_section_expand_icon_locator)
        user_form_page.click_on_element(UserFormLocators.check_all_billing_button_data_qa)
        io_form_page.click_on_element(
            UserFormLocators.save_button_locator)


@pytest.mark.dependency(depends=['test_finance_io_form_page_four'])
def test_finance_io_form_page_five(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    navbar = DashboardNavbar(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)
    invoice_list_page = DspDashboardInvoiceList(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    generic_modules.step_info(
        "[START - RTB-6717] Validate whether the Non FinAdmin users are able to edit IO-campaign execution comment "
        "(internal) if he have the edit permission on IO and Add execution comment to IO/Invoice/Proforma checkbox "
        "remains unchecked")

    # CHECKING IO EXECUTION COMMENT FIELD
    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    navbar.login_as("AutomationAgencyUser")
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              '2')
    io_form_page.provide_io_total_media_budget_info(io_data)
    io_form_page.select_specific_radio_button(
        io_data['billing_information']['invoice_payment_type'])
    io_form_page.select_dropdown_value(IoFormLocators.invoice_status_select_data_qa, "Ready for assistant")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_execution_comment = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.io_execution_comment_select_data_qa)
    assert io_execution_comment == io_data['total_media_budget'][
        'io_execution_comment']
    navbar.logout_as()
    generic_modules.step_info(
        "[END - RTB-6717] Validate whether the Non FinAdmin users are able to edit IO-campaign execution comment "
        "(internal) if he have the edit permission on IO and Add execution comment to IO/Invoice/Proforma checkbox "
        "remains unchecked")

    generic_modules.step_info(
        "[START - RTB-6718] Validate whether the Comment field is generating after selecting "
        "Other: Comment option from the IO-campaign execution comment (internal) dropdown")
    driver.get(io_url)
    io_form_page.select_dropdown_value(IoFormLocators.io_execution_comment_select_data_qa, "Other: Comment")
    io_form_page.set_value_into_element(
        IoFormLocators.comment_text_field_data_qa, "Test Notes")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    assert "Test Notes" == io_form_page.get_element_text(
        IoFormLocators.comment_text_field_data_qa)
    generic_modules.step_info(
        "[END - RTB-6718] Validate whether the Comment field is generating after selecting "
        "Other: Comment option from the IO-campaign execution comment (internal) dropdown")

    generic_modules.step_info(
        "[START - RTB-6779] Validate the users are able to select Full radio button from "
        "Invoice/payment type and this type of IO will have only one Invoice")
    generic_modules.step_info(
        "[START - RTB-6885] Validate Invoice Status as Ready to assistant")

    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    driver.get(io_url)
    assert False is io_form_page.is_element_present(
        IoFormLocators.create_invoice_button_data_qa, 1)
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.click_on_element(IoListLocators.three_dot_data_qa.format(io_id))
    io_list_page.wait_for_spinner_load()
    assert False is io_form_page.is_element_present(IoListLocators.invoice_data_qa.format(io_id))
    assert False is io_form_page.is_element_present(IoListLocators.add_invoice_data_qa.format(io_id))

    sidebar_navigation.navigate_to_page(PageNames.INVOICE)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    invoice_list_page.wait_for_visibility_of_element(
        InvoiceListLocators.first_grid_item_locator)
    io_list_page.wait_for_spinner_load()
    io_list_page.click_on_three_dot_and_action(io_id)
    assert False is io_form_page.is_element_present(IoListLocators.add_invoice_data_qa.format(io_id))

    generic_modules.step_info(
        "[END - RTB-6779] Validate the users are able to select Full radio button from "
        "Invoice/payment type and this type of IO will have only one Invoice")
    generic_modules.step_info(
        "[END - RTB-6885] Validate Invoice Status as Ready to assistant")


def test_finance_io_form_page_six(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6780] Validate the users are able to select Partly radio button from "
        "Invoice/payment type and this type of IO will have more than one Invoice")
    generic_modules.step_info(
        "[START - RTB-6885] Validate Invoice Status as Ready to assistant")

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              '2')
    io_form_page.provide_io_total_media_budget_info(io_data)
    io_form_page.select_specific_radio_button("Partly")
    io_form_page.select_dropdown_value(IoFormLocators.invoice_status_select_data_qa, "Ready for assistant")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_url = driver.current_url
    driver.get(io_url)
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button()
    driver.get(io_url)
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()
    driver.get(io_url)
    assert True is io_form_page.is_element_present(
        IoFormLocators.create_invoice_button_data_qa)
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.click_on_three_dot_and_action(io_id)
    assert True is io_form_page.is_element_present(
        IoListLocators.add_invoice_data_qa.format(io_id))
    sidebar_navigation.navigate_to_page(PageNames.INVOICE)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.click_on_three_dot_and_action(io_id)
    assert True is io_form_page.is_element_present(IoListLocators.add_invoice_data_qa.format(io_id))
    generic_modules.step_info(
        "[END - RTB-6780] Validate the users are able to select Partly radio button from "
        "Invoice/payment type and this type of IO will have more than one Invoice")
    generic_modules.step_info(
        "[END - RTB-6885] Validate Invoice Status as Ready to assistant")


def test_finance_io_form_page_seven(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)

    generic_modules.step_info(
        "[START - RTB-6782] Validate Payment details section is generated with proper data")
    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    # GETTING AND STORING INFO
    payment_test_data = {'discount': '', 'vat': '', 'payment_term': ''}

    company_profile_url = config['credential']['url'] + \
                          config['company-pages']['webcoupers-url']
    billing_entity_url = config['credential']['url'] + \
                         config['billing-entity-pages']['eskimi-ng-ng-url']
    user_url = config['credential']['url'] + config['user-settings-pages'][
        'webcoupers-glo-user']

    driver.get(company_profile_url)
    payment_test_data['payment_term'] = io_form_page.get_element_text(
        CompanyFormLocators.company_payment_term_locator,
        input_tag=True)
    driver.get(billing_entity_url)
    payment_test_data['vat'] = io_form_page.get_element_text(
        BillingEntitiesFormLocators.vat_locator, input_tag=True)
    driver.get(user_url)
    io_form_page.click_on_element(
        UserFormLocators.currency_and_margins_section_locator)
    payment_test_data['discount'] = io_form_page.get_element_text(
        UserFormLocators.discount_field_data_qa, input_tag=True)

    generic_modules.step_info(
        "[START - RTB-6822] Validate whether the Campaign Cost & Actual spend calculations are showing correct")
    generic_modules.step_info(
        "[START - RTB-6823] Validate whether proper IO balance information is showing in the IO form page")

    ngn_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        102, db_connection)
    campaign_id = IoUtils.pull_campaign_id_which_has_large_spent_amount_from_db(db_connection)
    campaign_name = CampaignUtils.pull_campaign_name_from_db(campaign_id, db_connection)
    campaign_name_id = f"{campaign_name} ({campaign_id})"
    spent, spent_alt_currency = IoUtils.pull_spent_and_spent_alt_for_specific_campaign_from_db(
        campaign_id,
        ngn_currency_rate,
        db_connection)
    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.select_dropdown_value(IoFormLocators.client_select_data_qa, "Webcoupers - GLO")
    io_form_page.wait_for_spinner_load()
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoFormLocators.campaign_select_data_qa, option_to_select=campaign_name_id)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              "1000")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    io_form_page.wait_for_spinner_load()
    io_form_page.click_on_specific_form_nav_option(
        IoFormLocators.total_media_budget_label)
    if 'http://rtb.local/admin' not in driver.current_url:
        assert int(float(spent)) == int(
            float(io_form_page.get_value_from_specific_input_field(IoFormLocators.campaign_cost_label)))
        assert int(float(spent_alt_currency)) == int(
            float(io_form_page.get_value_from_specific_input_field(IoFormLocators.actual_spend_label)))

    io_form_page.click_on_specific_form_nav_option(
        IoFormLocators.billing_information_label)
    io_form_page.click_on_element(
        IoFormLocators.payment_details_section_data_qa, locator_to_be_appeared=IoFormLocators.vat_field_data_qa)
    if 'http://rtb.local/admin' not in driver.current_url:
        assert float(payment_test_data['vat']) == float(
            io_form_page.get_value_from_specific_input_field(IoFormLocators.vat_field_data_qa))
        assert float(payment_test_data['discount']) == float(
            io_form_page.get_text_using_tag_attribute(
                io_form_page.input_tag, io_form_page.data_qa_attribute,
                IoFormLocators.discount_field_data_qa))
        assert float(payment_test_data['payment_term']) == float(
            io_form_page.get_value_from_specific_input_field(IoFormLocators.payment_term_days_input_data_qa))

    assert "Complete" == io_form_page.get_specific_finance_profile_status(IoFormLocators.campaign_status_info_data_qa)
    assert "1,000.00" == io_form_page.get_specific_finance_profile_status(IoFormLocators.total_io_amount_info_data_qa)
    assert str(Decimal(1000 / ngn_currency_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) == \
           (io_form_page.get_specific_finance_profile_status(IoFormLocators.total_io_amount_usd_info_data_qa))
    assert "0.00" == io_form_page.get_specific_finance_profile_status(IoFormLocators.total_amount_invoiced_info_data_qa)
    assert "1,000.00" == io_form_page.get_specific_finance_profile_status(
        IoFormLocators.left_amount_to_invoice_info_data_qa)
    if 'http://rtb.local/admin' not in driver.current_url:
        assert "{:,.2f}".format(
            spent_alt_currency) in io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_spent_amount_info_data_qa)
        assert "0.00" == io_form_page.get_specific_finance_profile_status(IoFormLocators.spent_last_month_info_data_qa)
        assert '' == io_form_page.get_specific_finance_profile_status(IoFormLocators.invoices_info_data_qa)

    generic_modules.step_info(
        "[END - RTB-6822] Validate whether the Campaign Cost & Actual spend calculations are showing correct")
    generic_modules.step_info(
        "[END - RTB-6782] Validate Payment details section is generated with proper data")
    generic_modules.step_info(
        "[END - RTB-6823] Validate whether proper IO balance information is showing in the IO form page")


def test_finance_io_form_page_eight(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6825] Validate whether proper IO balance information is showing in the IO form page for "
        "the multi invoices under one IO")

    ngn_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        102, db_connection)
    campaign_id = IoUtils.pull_campaign_id_which_has_large_spent_amount_from_db(db_connection)
    campaign_name = CampaignUtils.pull_campaign_name_from_db(campaign_id, db_connection)
    campaign_name_id = f"{campaign_name} ({campaign_id})"
    spent, spent_alt_currency = IoUtils.pull_spent_and_spent_alt_for_specific_campaign_from_db(
        campaign_id,
        ngn_currency_rate,
        db_connection)
    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.select_dropdown_value(IoFormLocators.client_select_data_qa, "Webcoupers - GLO")
    io_form_page.wait_for_spinner_load()
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoFormLocators.campaign_select_data_qa, option_to_select=campaign_name_id)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              "1000")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    io_form_page.wait_for_spinner_load()
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.class_attribute,
                                              InvoiceFormLocators.form_control_media_budget_class,
                                              "500")
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_form_page.wait_for_spinner_load()
    first_invoice_number = "ENG " + io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.class_attribute,
        InvoiceFormLocators.first_invoice_number_class)

    driver.get(io_url)
    io_form_page.wait_for_spinner_load()
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.class_attribute,
                                              InvoiceFormLocators.form_control_media_budget_class,
                                              "500")
    # Commented out success notification verification, b/c https://eskimidev.atlassian.net/browse/RTB-9027
    # invoice_form_page.click_on_save_and_generate_invoice_button(
    #     locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button()
    io_form_page.wait_for_spinner_load()
    second_invoice_number = "ENG " + io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.class_attribute,
        InvoiceFormLocators.first_invoice_number_class)
    invoices = first_invoice_number + ", " + second_invoice_number

    io_form_page.click_on_specific_button(InvoiceFormLocators.add_payment_button,
                                          locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
    io_form_page.wait_for_visibility_of_element(
        InvoiceFormLocators.paid_amount_field_locator)
    io_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "1")
    io_form_page.click_on_specific_button(InvoiceFormLocators.save_button)

    assert "Complete" == io_form_page.get_specific_finance_profile_status(IoFormLocators.campaign_status_info_data_qa)
    assert "1,000.00" == io_form_page.get_specific_finance_profile_status(IoFormLocators.total_io_amount_info_data_qa)
    assert str(Decimal(1000 / ngn_currency_rate).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)) == \
           io_form_page.get_specific_finance_profile_status(IoFormLocators.total_io_amount_usd_info_data_qa)
    assert "1,000.00" == io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_amount_invoiced_info_data_qa)
    assert "0.00" == io_form_page.get_specific_finance_profile_status(
        IoFormLocators.left_amount_to_invoice_info_data_qa)
    if 'http://rtb.local/admin' not in driver.current_url:
        assert "{:,.2f}".format(
            spent_alt_currency) in io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_spent_amount_info_data_qa)
        assert "0.00" == io_form_page.get_specific_finance_profile_status(IoFormLocators.spent_last_month_info_data_qa)
        assert invoices == io_form_page.get_specific_finance_profile_status(IoFormLocators.invoices_info_data_qa)

    generic_modules.step_info(
        "[END - RTB-6825] Validate whether proper IO balance information is showing in the IO form page for "
        "the multi invoices under one IO")


def test_finance_io_form_page_nine(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_list = DspDashboardInvoiceList(driver)

    # PROVIDED IO DATA IN GUI
    global date_format, all_data_verification_message
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    # GETTING AND STORING INFO
    with open('assets/io/profile_finance_status_data.json') as json_file:
        profile_finance_status_data = json.load(json_file)
    pulled_profile_finance_status_data_from_gui = copy.deepcopy(
        profile_finance_status_data)

    company_profile_url = config['credential']['url'] + \
                          profile_finance_status_data[
                              'profile_finance_data'][
                              'company_profile_url']
    driver.get(company_profile_url)
    profile_finance_status_data['profile_finance_data'][
        'discount'] = io_form_page.get_element_text(
        CompanyFormLocators.company_discount_locator,
        input_tag=True) + "%"
    profile_finance_status_data['profile_finance_data'][
        'bonus'] = io_form_page.get_element_text(
        CompanyFormLocators.company_bonus_locator,
        input_tag=True) + "%"
    profile_finance_status_data['profile_finance_data'][
        'tax'] = io_form_page.get_element_text(
        CompanyFormLocators.company_tax_locator,
        input_tag=True) + "%(i.e. WHT)"
    profile_finance_status_data['profile_finance_data'][
        'last_payment'] = io_form_page.get_current_date_with_specific_format(
        date_format)
    final_credit_limit = io_form_page.get_element_text(
        CompanyFormLocators.final_credit_limit_locator, input_tag=True)
    final_credit_limit = float(final_credit_limit.replace(",", ""))
    io_form_page.wait_for_spinner_load()
    final_credit_limit = " / $" + "{:,.2f}".format(final_credit_limit)

    # GETTING INVOICE LAST DATE FROM INVOICE LIST PAGE
    sidebar_navigation.navigate_to_page(PageNames.INVOICE)
    invoice_list.select_dropdown_value(InvoiceListLocators.client_account_label, io_data['client_profile']['client'])
    invoice_list.wait_for_spinner_load()
    invoice_list.select_dropdown_value(InvoiceListLocators.rows_per_page_label, InvoiceListLocators.all_option)
    profile_finance_status_data['profile_finance_data'][
        'last_invoice'] = invoice_list.get_last_invoice_date_from_list(
        InvoiceListLocators.invoice_list_date_locator)

    generic_modules.step_info(
        "[START - RTB-6881] Validate whether proper Profile finance status information is showing in the IO form "
        "page for multi invoices under one IO")

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_from_modal_form_using_js_code(
        field_label_or_xpath_or_data_qa=IoFormLocators.campaign_select_data_qa,
        option_to_select=io_data['io_object']['campaign'])
    io_form_page.wait_for_spinner_load()
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              "100")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url

    # CREATING INVOICES AND ADDING PAYMENTS
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.class_attribute,
                                              InvoiceFormLocators.form_control_media_budget_class,
                                              "50")
    io_form_page.select_dropdown_value(InvoiceFormLocators.io_execution_comment_label, "I: Not enough traffic")
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    io_form_page.click_on_specific_button(InvoiceFormLocators.add_payment_button,
                                          locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
    io_form_page.wait_for_visibility_of_element(
        InvoiceFormLocators.paid_amount_field_locator)
    io_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "50")
    io_form_page.click_on_specific_button(InvoiceFormLocators.save_button,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    driver.get(io_url)

    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.class_attribute,
                                              InvoiceFormLocators.form_control_media_budget_class,
                                              "50")
    io_form_page.select_dropdown_value(InvoiceFormLocators.io_execution_comment_label, "I: Not enough traffic")
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    io_form_page.click_on_specific_button(InvoiceFormLocators.add_payment_button,
                                          locator_to_be_appeared=InvoiceFormLocators.amount_paid_locator)
    io_form_page.wait_for_visibility_of_element(
        InvoiceFormLocators.paid_amount_field_locator)
    io_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "50")
    io_form_page.click_on_specific_button(InvoiceFormLocators.save_button,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    driver.get(io_url)

    # GETTING OPEN IOS, CREDIT LIMIT LEVEL, FINANCE BALANCE & OPEN IOS AMOUNT
    bd_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(
        13, db_connection)
    open_ios, io_amounts = IoUtils.pull_open_ios_from_db(db_connection)
    finance_balances = IoUtils.pull_finance_balances_from_db(db_connection)
    open_io_string = ""
    if len(open_ios) > 0:
        for open_io in open_ios:
            open_io_string += (str(open_io).split("."))[0]
            if open_ios[len(open_ios) - 1] != open_io:
                open_io_string += ", "
    profile_finance_status_data['profile_finance_data'][
        'open_ios'] = open_io_string

    io_amount_list = []
    if len(io_amounts) > 0:
        for io_amount in io_amounts:
            io_amount_string = (str(io_amount)).replace(
                "[", "").replace('"', "").replace("]", "")
            io_amount_values = io_amount_string.split(',')
            if len(io_amount_values) > 1:
                for value in io_amount_values:
                    io_amount_list.append(float(value))
            else:
                io_amount_list.append(str(io_amount_values[0]))
    open_io_amount = sum(map(float, io_amount_list))

    total_finance_balances = sum(map(float, finance_balances))
    credit_limit_level = open_io_amount + total_finance_balances
    profile_finance_status_data['profile_finance_data'][
        'open_ios_amount'] = "$" + "{:,.2f}".format(open_io_amount)
    profile_finance_status_data['profile_finance_data'][
        'finance_balance'] = "$" + "{:,.2f}".format(
        total_finance_balances)
    profile_finance_status_data['profile_finance_data'][
        'credit_limit_level'] = "$" + "{:,.2f}".format(
        credit_limit_level) + final_credit_limit
    profile_finance_status_data['profile_finance_data']['currency_rate'] = \
        profile_finance_status_data['profile_finance_data'][
            'currency_rate'] + "{:,.2f}".format(bd_currency_rate)

    # DATA VERIFICATION
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'credit_limit_level'] = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.credit_limit_info_data_qa)
    # pulled_profile_finance_status_data_from_gui['profile_finance_data'][
    #     'overdue'] = io_form_page.get_specific_finance_profile_status(
    #     IoFormLocators.overdue_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'finance_balance'] = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.finance_balance_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'open_ios_amount'] = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.open_ios_amount_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'open_ios'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.open_ios_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'last_invoice'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.last_invoice_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'last_payment'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.last_payment_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'discount'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.discount_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'rebate'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.rebate_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'bonus'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.bonus_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'tax'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.tax_info_data_qa)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'currency_rate'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.currency_rate_label)
    if 'http://rtb.local/admin' in driver.current_url:
        del pulled_profile_finance_status_data_from_gui['profile_finance_data']['last_invoice']
        del profile_finance_status_data['profile_finance_data']['last_invoice']
    print(generic_modules.ordered(
        pulled_profile_finance_status_data_from_gui))
    print(generic_modules.ordered(profile_finance_status_data))
    assert generic_modules.ordered(
        pulled_profile_finance_status_data_from_gui) == generic_modules.ordered(
        profile_finance_status_data)

    pulled_io_data_gui = copy.deepcopy(io_data)
    pulled_io_data_gui['io_main_information'][
        'io_title'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.io_title_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'client'] = io_form_page.get_selected_options_using_js_code(IoFormLocators.client_select_data_qa)
    pulled_io_data_gui['client_profile'][
        'email'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.email_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'contact'] = io_form_page.get_value_from_specific_input_field(IoFormLocators.contact_input_data_qa)
    pulled_io_data_gui['client_profile'][
        'responsible_adOps'] = io_form_page.get_selected_options_using_js_code(
        IoFormLocators.responsible_adops_input_data_qa)
    print(generic_modules.ordered(pulled_io_data_gui))
    print(generic_modules.ordered(io_data))
    assert generic_modules.ordered(
        pulled_io_data_gui) == generic_modules.ordered(io_data)
    generic_modules.step_info(
        "[END - RTB-6881] Validate whether proper Profile finance status information is showing in the IO form "
        "page for multi invoices under one IO")


def test_finance_io_form_page_ten(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6882] Validate whether the Created/updated by & created/updated date information "
        "are showing properly")
    generic_modules.step_info(
        "[START - RTB-6883] Validate whether the IO-campaign execution comment (internal) change history log "
        "is showing properly")

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']

    timezone = pytz.timezone("Europe/Vilnius")
    current_time = datetime.now(timezone)
    gmt_offset = current_time.strftime("%z")
    gmt_offset = gmt_offset.replace('0', '')

    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_dropdown_value(IoFormLocators.io_execution_comment_select_data_qa, "I: Low performance")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    io_form_page.wait_for_spinner_load()

    created_by_info = io_form_page.get_element_text(
        IoFormLocators.created_by_info_data_qa)
    created_by = created_by_info.split(":")
    assert "AutomationAdminUser" == created_by[1].strip()

    last_updated_by_info = io_form_page.get_element_text(
        IoFormLocators.last_updated_by_info_data_qa)
    last_updated_by = last_updated_by_info.split(":")
    assert "AutomationAdminUser" == last_updated_by[1].strip()

    created_info = io_form_page.get_element_text(
        IoFormLocators.created_info_data_qa)
    created = created_info.split(" ")
    current_date = io_form_page.get_current_date_with_specific_format(
        "%Y-%m-%d")
    assert current_date == created[1].strip()
    assert "(GMT+3)" == created[3].strip()

    last_updated_info = io_form_page.get_element_text(
        IoFormLocators.last_updated_info_data_qa)
    last_updated = last_updated_info.split(" ")
    assert current_date == last_updated[2].strip()
    assert "(GMT+3)" == last_updated[4].strip()

    io_execution_update_info = io_form_page.get_element_text(
        IoFormLocators.io_execution_update_info_data_qa)
    io_execution_update = io_execution_update_info.split(" ")
    assert "AutomationAdminUser," == io_execution_update[2]
    assert current_date == io_execution_update[3]
    assert f"(GMT{gmt_offset})" == io_execution_update[5]

    navbar.login_as("AutomationAgencyUser")
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_dropdown_value(IoFormLocators.io_execution_comment_select_data_qa, "I: Low performance")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    io_form_page.wait_for_spinner_load()

    created_by_info = io_form_page.get_element_text(
        IoFormLocators.created_by_info_data_qa)
    created_by = created_by_info.split(":")
    assert "AutomationAdminUser" == created_by[1].strip()

    last_updated_by_info = io_form_page.get_element_text(
        IoFormLocators.last_updated_by_info_data_qa)
    last_updated_by = last_updated_by_info.split(":")
    assert "AutomationAdminUser" == last_updated_by[1].strip()

    created_info = io_form_page.get_element_text(
        IoFormLocators.created_info_data_qa)
    created = created_info.split(" ")
    current_date = io_form_page.get_current_date_with_specific_format(
        "%Y-%m-%d")
    assert current_date == created[1].strip()
    assert "(GMT+3)" == created[3].strip()

    last_updated_info = io_form_page.get_element_text(
        IoFormLocators.last_updated_info_data_qa)
    last_updated = last_updated_info.split(" ")
    assert current_date == last_updated[2].strip()
    assert "(GMT+3)" == last_updated[4].strip()

    io_execution_update_info = io_form_page.get_element_text(
        IoFormLocators.io_execution_update_info_data_qa)
    io_execution_update = io_execution_update_info.split(" ")
    assert "AutomationAdminUser," == io_execution_update[2]
    assert current_date == io_execution_update[3]
    assert f"(GMT{gmt_offset})" == io_execution_update[5]

    generic_modules.step_info(
        "[END - RTB-6882] Validate whether the Created/updated by & created/updated date information "
        "are showing properly")
    generic_modules.step_info(
        "[END - RTB-6883] Validate whether the IO-campaign execution comment (internal) change history log "
        "is showing properly")


def test_finance_io_form_page_eleven(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    generic_modules.step_info(
        "[START - RTB-6884] Validate Invoice Status as Invoice Issued")
    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_dropdown_value(IoFormLocators.invoice_status_select_data_qa, "Invoice issued")
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_url = driver.current_url
    driver.get(io_url)
    assert False is io_form_page.is_element_present(
        IoFormLocators.create_invoice_button_data_qa, 1)
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_form_page.wait_for_spinner_load()
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.click_on_three_dot_and_action(io_id)
    assert False is io_form_page.is_element_present(
        IoListLocators.invoice_data_qa.format(io_id))
    assert False is io_form_page.is_element_present(
        IoListLocators.add_invoice_data_qa.format(io_id))
    assert True is io_form_page.is_element_present(
        IoListLocators.invoice_issued_data_qa.format(io_id))

    generic_modules.step_info(
        "[END - RTB-6884] Validate Invoice Status as Invoice Issued")


def test_finance_io_form_page_twelve(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6886] Validate Invoice Status as ProForma")
    generic_modules.step_info(
        "[START - RTB-6887] Validate Send feedback after IO closed checkbox")
    generic_modules.step_info(
        "[START - RTB-6947] Validate Signed IO checkbox")

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag,
                                              io_form_page.data_qa_attribute,
                                              IoFormLocators.media_budget_input_data_qa.format("1"),
                                              '2')
    io_form_page.provide_io_total_media_budget_info(io_data)
    io_form_page.select_specific_radio_button("Partly")
    io_form_page.select_dropdown_value(IoFormLocators.invoice_status_select_data_qa, "ProForma")
    io_form_page.check_uncheck_specific_checkbox(IoFormLocators.signed_io_check_data_qa, True)
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_url = driver.current_url
    driver.get(io_url)
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_input_data_qa)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    driver.get(io_url)
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_btn_data_qa,
                                          locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
    if invoice_form_page.is_element_present(InvoiceFormLocators.manual_invoicing_reason_locator, time_out=2):
        invoice_form_page.select_dropdown_value(InvoiceFormLocators.manual_invoicing_reason_label,
                                                'Client requested invoice early')
    invoice_form_page.click_on_save_and_generate_invoice_button(
        locator_to_be_appeared=InvoiceFormLocators.success_message_locator)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()
    driver.get(io_url)
    io_number = io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag,
        io_form_page.data_qa_attribute,
        IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    assert True is io_form_page.is_element_present(
        IoFormLocators.create_invoice_button_data_qa)
    sidebar_navigation.navigate_to_page(PageNames.IO)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.click_on_three_dot_and_action(io_id)
    assert True is io_form_page.is_element_present(
        IoListLocators.add_invoice_data_qa.format(io_id))

    sidebar_navigation.navigate_to_page(PageNames.INVOICE)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_spinner_load()
    io_list_page.click_on_three_dot_and_action(io_id)
    assert True is io_form_page.is_element_present(
        IoListLocators.add_invoice_data_qa.format(io_id))

    feedback_email_status = IoUtils.get_feedback_email_status_from_db(
        io_number.strip(), db_connection)
    assert feedback_email_status == 1

    signed_status = IoUtils.get_signed_status_from_db(io_number.strip(), db_connection)
    assert signed_status == 1

    generic_modules.step_info(
        "[END - RTB-6885] Validate Invoice Status as ProForma")
    generic_modules.step_info(
        "[END - RTB-6887] Validate Send feedback after IO closed checkbox")
    generic_modules.step_info(
        "[END - RTB-6947] Validate Signed IO checkbox")


def test_finance_io_form_page_thirteen(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    proforma_form_page = DspDashboardProformaForm(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)
    io_data['billing_information']['invoice_payment_type'] = "Partly"
    io_data['billing_information'][
        'send_feedback_after_io_closed_checkbox_status'] = ''
    io_data['billing_information']['invoice_status'] = '-'
    io_data['total_media_budget'][
        'io_execution_comment'] = "I: Not enough traffic"

    with open('assets/io/proforma_edit_data.json') as json_file:
        proforma_data = json.load(json_file)
    proforma_data['proforma_main_information']['proforma_title'] = \
        io_data['io_main_information']['io_title']
    io_list_url = config['credential']['url'] + config['io-list-page']['io-list-url']

    generic_modules.step_info(
        "[START - RTB-6948] Validate whether the Save and Sync with Proforma is working properly")

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_element(
        IoFormLocators.channel_dropdown_item_locator)
    io_form_page.select_dropdown_value(IoFormLocators.country_select_data_qa, io_data['io_object']['country'])
    io_form_page.select_specific_radio_button(
        io_data['billing_information']['invoice_payment_type'])
    io_form_page.select_dropdown_value(IoFormLocators.invoice_status_select_data_qa, io_data['billing_information'][
        'invoice_status'])
    io_form_page.click_on_save_and_generate_io_button(
        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_number = io_form_page.get_text_using_tag_attribute(io_form_page.div_tag, io_form_page.data_qa_attribute,
                                                          IoFormLocators.insertion_order_info_data_qa)
    io_id = IoUtils.pull_io_id(io_number, db_connection)
    io_url = driver.current_url

    # PROFORMA CREATION
    driver.get(io_list_url)
    io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa,
                                       IoListLocators.test_automation_company_data)
    io_form_page.wait_for_spinner_load()
    io_list_page.wait_for_visibility_of_element(
        IoListLocators.first_grid_item_locator)
    io_list_page.click_on_three_dot_and_action(io_id, action='add proforma')
    io_list_page.click_on_element(
        ProformaFormLocators.confirmation_yes_button_locator,
        locator_to_be_appeared=ProformaFormLocators.save_and_generate_proforma_button_data_qa)
    proforma_form_page.click_on_save_and_generate_proforma_button(
        locator_to_be_appeared=ProformaFormLocators.success_message_locator)
    io_list_page.wait_for_visibility_of_element(
        ProformaFormLocators.success_message_locator)

    proforma_form_page.provide_proforma_data_and_save(proforma_data,
                                                      edit_proforma=True)
    io_list_page.click_on_element(
        ProformaFormLocators.save_and_sync_with_io_button_locator,
        locator_to_be_appeared=ProformaFormLocators.success_message_locator)
    io_list_page.wait_for_visibility_of_element(
        ProformaFormLocators.success_message_locator)
    assert "Proforma saved and synced with IO" in proforma_form_page.get_success_message()

    driver.get(io_url)
    pulled_io_data_gui = io_form_page.get_io_information_from_gui(io_data)
    print(generic_modules.ordered(pulled_io_data_gui))
    print(generic_modules.ordered(io_data))
    assert io_data == pulled_io_data_gui

    generic_modules.step_info(
        "[END - RTB-6948] Validate whether the Save and Sync with Proforma is working properly")
