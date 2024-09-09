import json
import os
import time
from itertools import islice

import pytest

from configurations import generic_modules
from locators.company.company_form_locators import CompanyFormLocators
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.io_form_locator import IoFormLocators
from locators.io.io_list_locator import IoListLocators
from pages.company.company_form import DashboardCompanyForm
from pages.io.invoice_form import DspDashboardInvoiceForm
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.country import CountryUtils
from utils.page_names_enum import PageNames
from utils.io import IoUtils
from decimal import Decimal

debug_mode = "JENKINS_URL" not in os.environ
complete = ''
incomplete = ''
live = ''
complete_less_than_50 = ''
incomplete_less_than_50 = ''
live_less_than_50 = ''


@pytest.mark.dependency()
def test_regression_prerequisite_test_case_to_collect_data(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)

    global complete, incomplete, live, complete_less_than_50, incomplete_less_than_50, live_less_than_50

    client_company_name_list = []
    if sidebar_navigation.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")

    with open('assets/auto_billing/auto_billing_data.json') as json_file:
        auto_billing_data = json.load(json_file)

    last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
    last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')
    io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Complete', last_month_first_date,
                                                                last_month_last_date, db_connection)
    auto_billing_data['different_status']['complete'] = str(io_id)
    complete = str(io_id)

    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    client_company_name_list.append(client_company_name)
    io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Incomplete', last_month_first_date,
                                                                last_month_last_date, db_connection,
                                                                company_list_to_exclude=client_company_name_list)
    auto_billing_data['different_status']['incomplete'] = str(io_id)
    incomplete = str(io_id)

    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    client_company_name_list.append(client_company_name)
    io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Live', last_month_first_date,
                                                                last_month_last_date, db_connection,
                                                                company_list_to_exclude=client_company_name_list)
    auto_billing_data['different_status']['live'] = str(io_id)
    live = str(io_id)

    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    client_company_name_list.append(client_company_name)
    io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Complete', last_month_first_date,
                                                                last_month_last_date, db_connection,
                                                                compare_sign='<',
                                                                company_list_to_exclude=client_company_name_list)
    auto_billing_data['different_status']['complete_less_than_50'] = str(io_id)
    complete_less_than_50 = str(io_id)

    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    client_company_name_list.append(client_company_name)
    io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Incomplete', last_month_first_date,
                                                                last_month_last_date, db_connection,
                                                                compare_sign='<',
                                                                company_list_to_exclude=client_company_name_list)
    auto_billing_data['different_status']['incomplete_less_than_50'] = str(io_id)
    incomplete_less_than_50 = str(io_id)

    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    client_company_name_list.append(client_company_name)
    io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Live', last_month_first_date,
                                                                last_month_last_date, db_connection,
                                                                compare_sign='<',
                                                                company_list_to_exclude=client_company_name_list)
    auto_billing_data['different_status']['live_less_than_50'] = str(io_id)
    live_less_than_50 = str(io_id)

    with open('assets/temp/auto_billing_data.json', 'w') as json_file:
        json.dump(auto_billing_data, json_file)


@pytest.mark.dependency(depends=['test_regression_prerequisite_test_case_to_collect_data'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_3(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    io_form = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    company_form = DashboardCompanyForm(driver)

    user_list = []
    io_list = []

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-8783] Validate monthly auto billing for interim invoice &  Group all client accounts under one "
            "invoice (always a new IO+invoice(dedicated for self-service)) without last month invoice")
        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')
        io_ids = IoUtils.pull_ios_from_one_company_multi_users_which_have_expected_amount_of_spent('Complete',
                                                                                                   last_month_first_date,
                                                                                                   last_month_last_date,
                                                                                                   db_connection,
                                                                                                   compare_sign='>')
        if io_ids is not {}:
            first_two = dict(islice(io_ids.items(), 2))
            for key, value in first_two.items():
                user_list.append(key)
                io_list.append(value)
            io_list = [item for sublist in io_list for item in sublist]

            generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
            client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_list[0], db_connection)
            company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
                client_company_id)
            driver.get(company_form_url)

            remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
                CompanyFormLocators.auto_billing_remove_button_locator)
            for remove_button_element in remove_button_elements:
                remove_button_element.click()
                time.sleep(1)
                if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                    company_form.click_on_element(CompanyFormLocators.ok_button_locator)

            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.group_all_client_account_self_service_label, do_check=True)
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.credit_limit_id,
                input_value="999999")
            dis_status = company_form.get_attribute_value(
                CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                attribute_name='disabled', locator_initialization=True)
            if not dis_status:
                company_form.set_text_using_tag_attribute(
                    attribute_name=company_form.id_attribute,
                    attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                    input_value="100")
            company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                              option_list_to_select=user_list)
            company_form.select_from_modal_form_using_js_code(
                CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=user_list[0])
            company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                          locator_to_be_appeared=CompanyFormLocators.success_message_locator,
                                          time_out=60)
            generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

            generic_modules.step_info("[START] MODIFYING EXISTING IOS & INVOICES")
            for io in io_list:
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                           db_connection)
            ios = IoUtils.pull_io_ids_which_were_created_last_month_last_date(client_company_id, last_month_last_date,
                                                                              db_connection)
            io_form.navigate_to_specific_io_and_update_date(config, ios)
            for io in ios:
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                           db_connection)
            generic_modules.step_info("[END] MODIFYING EXISTING IOS & INVOICES")

            generic_modules.step_info("[START] GETTING USER WISE SPENT AMOUNT FOR ALL CAMPAIGNS AND RUNNING CRON JOB")
            previous_io_invoices = {}
            for io in io_list:
                if io not in previous_io_invoices:
                    previous_io_invoices[io] = set()
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                for invoice_id in invoice_ids:
                    previous_io_invoices[io].add(invoice_id)

            user_wise_spent_amount = {}
            spent_amount_float = ""
            for user in user_list:
                io_currency = IoUtils.pull_io_currency(io_list[user_list.index(user)], connection=db_connection)
                user_id = IoUtils.pull_user_id(user, connection=db_connection)
                if io_currency != 'USD':
                    spent_amount = IoUtils.pull_users_spent_alt_and_spent_alt_currency(last_month_first_date,
                                                                                       last_month_last_date, user_id,
                                                                                       db_connection)
                    if spent_amount != '':
                        spent_amount_float = round(float(spent_amount), 2)
                else:
                    spent_amount = IoUtils.pull_users_spent_alt_and_spent_alt_currency(last_month_first_date,
                                                                                       last_month_last_date, user_id,
                                                                                       db_connection, spent_alt=True)
                    if spent_amount != '':
                        spent_amount_float = round(float(spent_amount), 2)

                if user not in user_wise_spent_amount:
                    user_wise_spent_amount[user] = set()
                user_wise_spent_amount[user].add(spent_amount_float)

            generic_modules.step_info(
                "[START - RTB-8784] Validate daily auto billing for interim invoice & Group all client accounts under "
                "one invoice (always a new IO+invoice(dedicated for self-service)) without last month invoice")
            sidebar_navigation.navigate_to_page(PageNames.IO)
            io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
            io_list_page.wait_for_spinner_load()
            io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
            expected_row_count = io_list_page.get_element_text(IoListLocators.total_row_count_locator)
            expected_row_count = (expected_row_count.split('of'))[1]
            base_url = (config['credential']['url'].split('//'))[1]
            cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
                'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                               'daily-auto-billing-cron-job']
            try:
                driver.get(cron_job_url)
            except Exception as e:
                print(e)
                pass
            driver.get(config['credential']['url'])
            sidebar_navigation.navigate_to_page(PageNames.IO)
            io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
            io_list_page.wait_for_spinner_load()
            io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
            actual_row_count = io_list_page.get_element_text(IoListLocators.total_row_count_locator)
            actual_row_count = (actual_row_count.split('of'))[1]
            assert expected_row_count == actual_row_count
            generic_modules.step_info(
                "[END - RTB-8784] Validate daily auto billing for interim invoice & Group all client accounts under "
                "one invoice (always a new IO+invoice(dedicated for self-service)) without last month invoice")

            cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
                'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                               'monthly-auto-billing-cron-job']
            try:
                driver.get(cron_job_url)
            except Exception as e:
                print(e)
                pass
            time.sleep(60)

            generic_modules.step_info(
                "[START - RTB-8785] Validate monthly auto billing for interim invoice & Group all client accounts under "
                "one invoice (always a new IO+invoice(dedicated for self-service)) with last month invoice")
            driver.get(config['credential']['url'])
            sidebar_navigation.navigate_to_page(PageNames.IO)
            io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
            io_list_page.wait_for_spinner_load()
            io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
            expected_row_count = io_list_page.get_element_text(IoListLocators.total_row_count_locator)
            expected_row_count = (expected_row_count.split('of'))[1]
            cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
                'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                               'monthly-auto-billing-cron-job']
            try:
                driver.get(cron_job_url)
            except Exception as e:
                print(e)
                pass
            driver.get(config['credential']['url'])
            sidebar_navigation.navigate_to_page(PageNames.IO)
            io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
            io_list_page.wait_for_spinner_load()
            io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
            actual_row_count = io_list_page.get_element_text(IoListLocators.total_row_count_locator)
            actual_row_count = (actual_row_count.split('of'))[1]
            assert expected_row_count == actual_row_count
            generic_modules.step_info(
                "[END - RTB-8785] Validate monthly auto billing for interim invoice & Group all client accounts under "
                "one invoice (always a new IO+invoice(dedicated for self-service)) with last month invoice")

            latest_io_invoices = {}
            for io in io_list:
                if io not in latest_io_invoices:
                    latest_io_invoices[io] = set()
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                for invoice_id in invoice_ids:
                    latest_io_invoices[io].add(invoice_id)
            assert latest_io_invoices == previous_io_invoices

            generic_modules.step_info("[END] GETTING USER WISE SPENT AMOUNT FOR ALL CAMPAIGNS AND RUNNING CRON JOB")

            generic_modules.step_info("[START] DATA VALIDATION")
            time.sleep(2)
            io_url = io_list_page.get_attribute_value(IoListLocators.first_grid_item_locator, "href")
            driver.get(io_url)
            if io_form.is_alert_popup_available(io_form.ONE_SEC_DELAY):
                io_form.accept_alert()
            media_budget_elements = io_form.wait_for_presence_of_all_elements_located(
                IoFormLocators.media_budgets_input_locator)
            assert len(media_budget_elements) == len(user_wise_spent_amount)
            for user in user_list:
                media_budget = io_form.get_element_text(IoFormLocators.user_wise_media_budget_xpath.format(user),
                                                        locator_initialization=True, input_tag=True)
                media_budget = float(media_budget)
                media_budget = round(media_budget, 2)
                media_budget_2 = user_wise_spent_amount.get(user)
                media_budget_2 = float(next(iter(media_budget_2))) if isinstance(media_budget_2,
                                                                                 set) else media_budget_2
                assert media_budget == media_budget_2

            io_form.click_on_element(IoFormLocators.invoice_locator,
                                     locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
            if io_form.is_alert_popup_available(io_form.ONE_SEC_DELAY):
                io_form.accept_alert()
            media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
                InvoiceFormLocators.media_budgets_info_locator)
            assert len(media_budget_elements) == len(user_wise_spent_amount)
            for user in user_list:
                media_budget = invoice_form.get_element_text(
                    InvoiceFormLocators.user_wise_media_budget_xpath.format(user),
                    locator_initialization=True, input_tag=True)
                media_budget = float(media_budget)
                media_budget = round(media_budget, 2)
                media_budget_2 = user_wise_spent_amount.get(user)
                media_budget_2 = float(next(iter(media_budget_2))) if isinstance(media_budget_2,
                                                                                 set) else media_budget_2
                assert media_budget == media_budget_2
            generic_modules.step_info("[END] DATA VALIDATION")

            if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
                invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
                time.sleep(io_list_page.TWO_SEC_DELAY)
                alert = driver.switch_to.alert
                alert.accept()
                assert "Invoice has been deleted!" in invoice_form.get_success_message()

        generic_modules.step_info(
            "[END - RTB-8783] Validate monthly auto billing for interim invoice &  Group all client accounts under one "
            "invoice (always a new IO+invoice(dedicated for self-service)) without last month invoice")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process(login_by_user_type,
                                                                                         open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-9073] Validate multi auto billing process 1")
        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')

        io_ids = IoUtils.pull_ios_from_one_company_multi_users_which_have_expected_amount_of_spent('Complete',
                                                                                                   last_month_first_date,
                                                                                                   last_month_last_date,
                                                                                                   db_connection,
                                                                                                   compare_sign='>')
        user_list = []
        io_list = []
        first_two = {}
        if io_ids is not {}:
            first_two = dict(islice(io_ids.items(), 2))
            for key, value in first_two.items():
                user_list.append(key)
                io_list.append(value)

        io_id = IoUtils.pull_io_from_specific_user_which_have_expected_amount_of_spent('Complete', user_list[0],
                                                                                       last_month_first_date,
                                                                                       last_month_last_date,
                                                                                       db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)
        io_ids, campaign_spent_list, io_number_list = IoUtils.pull_ios_from_one_user_which_have_expected_amount_of_spent(
            io_client_name,
            last_month_last_date,
            db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.group_all_client_ios_under_one_invoice_label, do_check=True)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)

        # [START] FOR SECOND AUTO BILLING PROCESS
        company_form.click_on_element(CompanyFormLocators.auto_invoicing_add_btn,
                                      locator_to_be_appeared=CompanyFormLocators.group_all_client_radio_button_locator)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True, index='2')
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False, index='2')
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.group_all_client_account_self_service_label, do_check=True, index='2')

        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=user_list[1], index='2')
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=user_list[1],
            index='2')
        # [END] FOR SECOND AUTO BILLING PROCESS

        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        for io in io_ids:
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
        invoice_ids_for_assertion = IoUtils.pull_io_invoice(io_id, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] MODIFYING EXISTING IOS & INVOICES FOR SECOND BILLING PROCESS")
        io_list = first_two.get(user_list[1])
        for io in io_list:
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
        ios = IoUtils.pull_io_ids_which_were_created_last_month_last_date(client_company_id, last_month_last_date,
                                                                          db_connection)
        io_form_page.navigate_to_specific_io_and_update_date(config, ios)

        for io in ios:
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING IOS & INVOICES FOR SECOND BILLING PROCESS")

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
        io_wise_media_budget = {}
        io_wise_media_budget_2 = {}
        for io in io_ids:
            io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io)
            driver.get(io_form_url)
            if io_form_page.is_alert_popup_available(io_form_page.ONE_SEC_DELAY):
                io_form_page.accept_alert()
            io_form_page.click_on_save_and_generate_io_button(
                locator_to_be_appeared=IoFormLocators.success_message_data_qa)

            if io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.campaign_status_info_data_qa) == 'Complete':
                total_io_amount_str = io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.total_io_amount_info_data_qa)
                total_io_amount_str = total_io_amount_str.replace(",", "")
                total_io_amount = float(total_io_amount_str)

                total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.total_spent_amount_info_data_qa)
                total_spent_amount_str = total_spent_amount_str.split('(')[0]
                total_spent_amount_1 = total_spent_amount_str.replace(",", "")
                total_spent_amount_1 = float(total_spent_amount_1)

                total_io_amount = total_spent_amount_1 if total_spent_amount_1 < total_io_amount else total_io_amount

                rounded_campaign_spent = round(float(campaign_spent_list[io_ids.index(io)]), 0)
                total_spent_amount = rounded_campaign_spent if total_io_amount > rounded_campaign_spent else total_io_amount
            else:
                total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.spent_last_month_info_data_qa)
                total_spent_amount_str = total_spent_amount_str.split('(')[0]
                total_spent_amount = total_spent_amount_str.replace(",", "")
                total_spent_amount = float(total_spent_amount)
                total_io_amount = float(total_spent_amount)

            if io not in io_wise_media_budget:
                io_wise_media_budget[io_number_list[io_ids.index(io)]] = set()
                io_wise_media_budget_2[io_number_list[io_ids.index(io)]] = set()
            io_wise_media_budget[io_number_list[io_ids.index(io)]].add(total_spent_amount)
            io_wise_media_budget_2[io_number_list[io_ids.index(io)]].add(total_io_amount)

        generic_modules.step_info(
            "[START] GETTING USER WISE SPENT AMOUNT FOR ALL CAMPAIGNS AND RUNNING CRON JOB FOR SECOND BILLING PROCESS")
        previous_io_invoices = {}
        for io in io_list:
            if io not in previous_io_invoices:
                previous_io_invoices[io] = set()
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            for invoice_id in invoice_ids:
                previous_io_invoices[io].add(invoice_id)

        user_wise_spent_amount = {}
        io_currency = IoUtils.pull_io_currency(user_list[1], connection=db_connection)
        user_id = IoUtils.pull_user_id(user_list[1], connection=db_connection)
        if io_currency != 'USD':
            spent_amount = IoUtils.pull_users_spent_alt_and_spent_alt_currency(last_month_first_date,
                                                                               last_month_last_date, user_id,
                                                                               db_connection)
            spent_amount_float = round(float(spent_amount), 2)
        else:
            spent_amount = IoUtils.pull_users_spent_alt_and_spent_alt_currency(last_month_first_date,
                                                                               last_month_last_date, user_id,
                                                                               db_connection, spent_alt=True)
            spent_amount_float = round(float(spent_amount), 2)

        if user_list[1] not in user_wise_spent_amount:
            user_wise_spent_amount[user_list[1]] = set()
        user_wise_spent_amount[user_list[1]].add(spent_amount_float)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job']
        try:
            driver.get(cron_job_url)
        except Exception as e:
            print(e)
            pass

        time.sleep(60)

        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert len(invoice_ids_for_assertion) + 1 == len(invoice_id_updated_list)

        latest_io_invoices = {}
        for io in io_list:
            if io not in latest_io_invoices:
                latest_io_invoices[io] = set()
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            for invoice_id in invoice_ids:
                latest_io_invoices[io].add(invoice_id)
        assert latest_io_invoices == previous_io_invoices

        driver.get(config['credential']['url'])
        sidebar_navigation.navigate_to_page(PageNames.IO)
        io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
        io_list_page.wait_for_spinner_load()
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)

        generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
        generic_modules.step_info(
            "[END] GETTING USER WISE SPENT AMOUNT FOR ALL CAMPAIGNS AND RUNNING CRON JOB FOR SECOND BILLING PROCESS")

        generic_modules.step_info("[START] DATA VALIDATION FOR SECOND BILLING PROCESS")
        time.sleep(2)
        io_url = io_list_page.get_attribute_value(IoListLocators.first_grid_item_locator, "href")
        driver.get(io_url)
        if io_form_page.is_alert_popup_available(io_form_page.ONE_SEC_DELAY):
            io_form_page.accept_alert()
        media_budget_elements = io_form_page.wait_for_presence_of_all_elements_located(
            IoFormLocators.media_budgets_input_locator)
        assert len(media_budget_elements) == len(user_wise_spent_amount)
        media_budget = io_form_page.get_element_text(IoFormLocators.user_wise_media_budget_xpath.format(user_list[1]),
                                                     locator_initialization=True, input_tag=True)
        media_budget = float(media_budget)
        media_budget = round(media_budget, 2)
        media_budget_2 = user_wise_spent_amount.get(user_list[1])
        media_budget_2 = float(next(iter(media_budget_2))) if isinstance(media_budget_2, set) else media_budget_2
        assert media_budget == media_budget_2

        io_form_page.click_on_element(IoFormLocators.invoice_locator,
                                      locator_to_be_appeared=InvoiceFormLocators.invoice_title_field_locator)
        if io_form_page.is_alert_popup_available(io_form_page.ONE_SEC_DELAY):
            io_form_page.accept_alert()
        media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
            InvoiceFormLocators.media_budgets_info_locator)
        assert len(media_budget_elements) == len(user_wise_spent_amount)
        media_budget = invoice_form.get_element_text(
            InvoiceFormLocators.user_wise_media_budget_xpath.format(user_list[1]),
            locator_initialization=True, input_tag=True)
        media_budget = float(media_budget)
        media_budget = round(media_budget, 2)
        media_budget_2 = user_wise_spent_amount.get(user_list[1])
        media_budget_2 = float(next(iter(media_budget_2))) if isinstance(media_budget_2, set) else media_budget_2
        assert media_budget == media_budget_2

        if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
            invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
            time.sleep(io_form_page.TWO_SEC_DELAY)
            alert = driver.switch_to.alert
            alert.accept()
            assert "Invoice has been deleted!" in invoice_form.get_success_message()
        generic_modules.step_info("[END] DATA VALIDATION FOR SECOND BILLING PROCESS")

        generic_modules.step_info("[START] DATA VALIDATION FOR FIRST BILLING PROCESS")
        set_1 = set(invoice_ids_for_assertion)
        set_2 = set(invoice_id_updated_list)
        created_invoice_id = (set_1 ^ set_2).pop()
        invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
            created_invoice_id)
        driver.get(invoice_form_url)
        if invoice_form.is_alert_popup_available(invoice_form.TWO_SEC_DELAY):
            invoice_form.accept_alert()
        for (io_number, io_media_budget), (io_number_2, io_media_budget_2) in zip(io_wise_media_budget.items(),
                                                                                  io_wise_media_budget_2.items()):
            media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.media_budget_amount_xpath.format(str(
                io_number)), locator_initialization=True)
            media_budget_str = media_budget_str.replace('(', '')
            media_budget_str = media_budget_str.replace(')', '')
            media_budget_str = media_budget_str.replace(',', '')
            media_budget = round(float(media_budget_str), 0)
            io_media_budget_float = float(next(iter(io_media_budget))) if isinstance(io_media_budget,
                                                                                     set) else io_media_budget
            io_media_budget_float_2 = float(next(iter(io_media_budget_2))) if isinstance(io_media_budget_2,
                                                                                         set) else io_media_budget_2
            io_media_budget_float = round(io_media_budget_float, 0)
            min_value = media_budget - io_media_budget_float
            min_value_2 = media_budget - io_media_budget_float_2
            if abs(min_value) <= 1 or abs(min_value_2) <= 1:
                assert True
            else:
                assert False

        if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
            invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
            time.sleep(io_form_page.TWO_SEC_DELAY)
            alert = driver.switch_to.alert
            alert.accept()
            assert "Invoice has been deleted!" in invoice_form.get_success_message()
        generic_modules.step_info("[END] DATA VALIDATION FOR FIRST BILLING PROCESS")

        generic_modules.step_info(
            "[END - RTB-9073] Validate multi auto billing process 1")


@pytest.mark.dependency(
    depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process'])
def test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process(login_by_user_type,
                                                                                                   open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_list_page = DspDashboardIoList(driver)

    total_spent_amount_2 = 0
    country_wise_expected_total_media_budget = {}
    country_wise_db_total_media_budget = {}

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-9074 & RTB-9075] Validate multi auto billing process 2 & 3")
        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')

        io_ids = IoUtils.pull_ios_from_one_company_multi_users_which_have_expected_amount_of_spent('Complete',
                                                                                                   last_month_first_date,
                                                                                                   last_month_last_date,
                                                                                                   db_connection,
                                                                                                   compare_sign='>')
        user_list = []
        io_list = []
        if io_ids is not {}:
            first_two = dict(islice(io_ids.items(), 2))
            for key, value in first_two.items():
                user_list.append(key)
                io_list.append(value)

        io_id_1 = IoUtils.pull_io_from_specific_user_which_have_expected_amount_of_spent('Complete', user_list[0],
                                                                                         last_month_first_date,
                                                                                         last_month_last_date,
                                                                                         db_connection)
        invoice_ids_1 = IoUtils.pull_io_invoice(io_id_1, db_connection)
        io_client_name_1 = IoUtils.pull_io_client_name(io_id_1, db_connection)

        io_id_2 = IoUtils.pull_io_from_specific_user_which_have_expected_amount_of_spent('Complete', user_list[1],
                                                                                         last_month_first_date,
                                                                                         last_month_last_date,
                                                                                         db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id_1, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name_1)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name_1)

        # [START] FOR SECOND AUTO BILLING PROCESS
        company_form.click_on_element(CompanyFormLocators.auto_invoicing_add_btn,
                                      locator_to_be_appeared=CompanyFormLocators.group_all_client_radio_button_locator)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False, index='2')
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True, index='2')
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True, index='2')

        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=user_list[1], index='2')
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=user_list[1],
            index='2')
        # [END] FOR SECOND AUTO BILLING PROCESS

        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids_1, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id_1)
        driver.get(io_form_url)
        time.sleep(invoice_form.ONE_SEC_DELAY)
        if invoice_form.is_alert_popup_available(1):
            invoice_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

        total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_spent_amount_info_data_qa)
        total_spent_amount_str = total_spent_amount_str.split('(')[0]
        total_spent_amount = total_spent_amount_str.replace(",", "")
        total_spent_amount = float(total_spent_amount)

        total_io_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_io_amount_info_data_qa)
        total_io_amount_str = total_io_amount_str.replace(",", "")
        total_io_amount = float(total_io_amount_str)

        invoice_amount = total_spent_amount if total_spent_amount < total_io_amount else total_io_amount

        invoice_ids_1 = IoUtils.pull_io_invoice(io_id_1, db_connection)
        invoice_ids_2 = IoUtils.pull_io_invoice(io_id_2, db_connection)
        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io']
        try:
            driver.get(cron_job_url)
        except Exception as e:
            print(e)
            pass
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id_1, db_connection)
        assert len(invoice_ids_1) + 1 == len(invoice_id_updated_list)

        invoice_id_updated_list_2 = IoUtils.pull_io_invoice(io_id_2, db_connection)
        assert invoice_ids_2 == invoice_id_updated_list_2
        generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

        generic_modules.step_info("[START] DATA VERIFICATION")
        set_1 = set(invoice_ids_1)
        set_2 = set(invoice_id_updated_list)
        created_invoice_id = (set_1 ^ set_2).pop()
        invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
            created_invoice_id)
        driver.get(invoice_form_url)
        time.sleep(invoice_form.ONE_SEC_DELAY)
        if invoice_form.is_alert_popup_available(1):
            invoice_form.accept_alert()
        media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
            InvoiceFormLocators.media_budgets_info_locator)
        assert len(media_budget_elements) == 1
        actual_invoice_amount_str = invoice_form.get_element_text(InvoiceFormLocators.media_budgets_locator.format('1'),
                                                                  locator_initialization=True, input_tag=True)
        actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
        actual_invoice_amount = float(actual_invoice_amount_str)

        total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
        total_media_budget_str = total_media_budget_str.replace(",", "")
        total_media_budget = float(total_media_budget_str)
        assert actual_invoice_amount == total_media_budget == invoice_amount
        generic_modules.step_info("[END] DATA VERIFICATION")

        if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
            invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
            time.sleep(io_list_page.TWO_SEC_DELAY)
            alert = driver.switch_to.alert
            alert.accept()
            assert "Invoice has been deleted!" in invoice_form.get_success_message()

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                                  "AUTO BILLING CRON JOB FOR SECOND BILLING PROCESS")
        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id_2)
        driver.get(io_form_url)
        time.sleep(invoice_form.ONE_SEC_DELAY)
        if invoice_form.is_alert_popup_available(1):
            invoice_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

        country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
        expected_country_list = list(set(country_list))
        expected_country_list = sorted(expected_country_list)

        country_wise_ui_total_media_budget = io_form_page.get_country_wise_total_media_budget()
        country_wise_ui_total_media_budget = dict(sorted(country_wise_ui_total_media_budget.items()))

        country_code_wise_db_total_media_budget = IoUtils.pull_country_wise_actual_io_campaign_spent(io_id_2,
                                                                                                     db_connection)

        # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
        total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_spent_amount_info_data_qa)
        total_spent_amount_str = total_spent_amount_str.split('(')[0]
        total_spent_amount = total_spent_amount_str.replace(",", "")
        total_spent_amount = float(total_spent_amount)
        invoice_amount = total_spent_amount
        # else:
        for key, value in country_code_wise_db_total_media_budget.items():
            country_name = CountryUtils.pull_country_name(key, db_connection)
            if country_name not in country_wise_db_total_media_budget:
                country_wise_db_total_media_budget[country_name] = []
            country_wise_db_total_media_budget[country_name] = value
        country_wise_db_total_media_budget = dict(sorted(country_wise_db_total_media_budget.items()))

        for key, value in country_wise_ui_total_media_budget.items():
            if key in country_wise_db_total_media_budget:
                if value < float(country_wise_db_total_media_budget[key]):
                    country_wise_expected_total_media_budget[key] = round(float(value), 2)
                else:
                    float_value = float(country_wise_db_total_media_budget[key])
                    country_wise_expected_total_media_budget[key] = round(float_value, 2)

        for value in country_wise_expected_total_media_budget.values():
            if isinstance(value, Decimal):
                total_spent_amount_2 += float(value)
            else:
                total_spent_amount_2 += value

        total_io_amount_str_2 = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_io_amount_info_data_qa)
        total_io_amount_str_2 = total_io_amount_str_2.replace(",", "")
        total_io_amount_2 = float(total_io_amount_str_2)

        invoice_amount_2 = total_spent_amount_2 if total_spent_amount_2 < total_io_amount_2 else total_io_amount_2

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES FOR SECOND BILLING PROCESS")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids_2, db_connection)
        invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids_2, expected_country_list)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES FOR SECOND BILLING PROCESS")

        invoice_ids_1 = IoUtils.pull_io_invoice(io_id_1, db_connection)
        invoice_ids_2 = IoUtils.pull_io_invoice(io_id_2, db_connection)
        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'daily-auto-billing-cron-job-for-specific-io']
        try:
            driver.get(cron_job_url)
        except Exception as e:
            print(e)
            pass
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id_2, db_connection)
        assert len(invoice_ids_2) + 1 == len(invoice_id_updated_list)

        invoice_id_updated_list_1 = IoUtils.pull_io_invoice(io_id_1, db_connection)
        assert invoice_ids_1 == invoice_id_updated_list_1
        generic_modules.step_info("[END] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                                  "AUTO BILLING CRON JOB FOR SECOND BILLING PROCESS")

        generic_modules.step_info("[START] DATA VERIFICATION FOR SECOND BILLING PROCESS")
        set_1 = set(invoice_ids_2)
        set_2 = set(invoice_id_updated_list)
        created_invoice_id = (set_1 ^ set_2).pop()
        invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
            created_invoice_id)
        driver.get(invoice_form_url)
        time.sleep(invoice_form.ONE_SEC_DELAY)
        if invoice_form.is_alert_popup_available(1):
            invoice_form.accept_alert()
        # media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
        #     InvoiceFormLocators.media_budgets_info_locator)
        # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
        #     assert len(media_budget_elements) == 1
        # else:
        #     assert len(media_budget_elements) == len(expected_country_list)

        total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
        total_media_budget_str = total_media_budget_str.replace(",", "")
        total_media_budget = float(total_media_budget_str)
        invoice_amount = round(invoice_amount, 2)
        invoice_amount_2 = round(invoice_amount_2, 2)
        assert total_media_budget == invoice_amount or total_media_budget == invoice_amount_2 or total_media_budget == total_io_amount

        # if len(expected_country_list) == len(country_code_wise_db_total_media_budget):
        #     invoice_country_list = invoice_form.get_specific_media_table_column_data_from_invoice(
        #         IoFormLocators.country_row_info_data_qa)
        #     actual_country_list = list(set(invoice_country_list))
        #     actual_country_list = sorted(actual_country_list)
        #
        #     actual_country_wise_total_media_budget = invoice_form.get_country_wise_total_media_budget_from_invoice()
        #     actual_country_wise_total_media_budget = dict(sorted(actual_country_wise_total_media_budget.items()))
        #
        #     assert actual_country_list == expected_country_list
        #     assert actual_country_wise_total_media_budget == country_wise_expected_total_media_budget

        generic_modules.step_info("[END] DATA VERIFICATION FOR SECOND BILLING PROCESS")

        if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
            invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
            time.sleep(io_list_page.TWO_SEC_DELAY)
            alert = driver.switch_to.alert
            alert.accept()
            assert "Invoice has been deleted!" in invoice_form.get_success_message()

        generic_modules.step_info(
            "[END - RTB-9074 & RTB-9075] Validate multi auto billing process 2 & 3")


@pytest.mark.dependency(
    depends=['test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    io_form = DspDashboardIoForm(driver)
    company_form = DashboardCompanyForm(driver)

    user_list = []
    io_list = []
    previous_io_invoices = {}
    actual_io_invoices = {}

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-9068] Validate monthly auto billing for interim invoice & Grouping by account and IO without "
            "last month invoice and last month spent > 50 (For complete/incomplete status)")

        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')
        io_ids = IoUtils.pull_ios_from_one_company_multi_users_which_have_expected_amount_of_spent('Complete',
                                                                                                   last_month_first_date,
                                                                                                   last_month_last_date,
                                                                                                   db_connection,
                                                                                                   compare_sign='>')
        if io_ids is not {}:
            first_two = dict(islice(io_ids.items(), 2))
            for key, value in first_two.items():
                user_list.append(key)
                io_list.append(value)
            io_list = [item for sublist in io_list for item in sublist]

            generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
            client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_list[0], db_connection)
            company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
                client_company_id)
            driver.get(company_form_url)

            remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
                CompanyFormLocators.auto_billing_remove_button_locator)
            for remove_button_element in remove_button_elements:
                remove_button_element.click()
                time.sleep(1)
                if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                    company_form.click_on_element(CompanyFormLocators.ok_button_locator)

            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.grouping_by_account_and_io_label,
                do_check=True)
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.credit_limit_id,
                input_value="999999")
            dis_status = company_form.get_attribute_value(
                CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                attribute_name='disabled', locator_initialization=True)
            if not dis_status:
                company_form.set_text_using_tag_attribute(
                    attribute_name=company_form.id_attribute,
                    attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                    input_value="100")
            company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                              option_list_to_select=user_list)
            company_form.select_from_modal_form_using_js_code(
                CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=user_list[0])
            company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                          locator_to_be_appeared=CompanyFormLocators.success_message_locator,
                                          time_out=60)
            generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

            generic_modules.step_info("[START] MODIFYING EXISTING IOS & INVOICES")
            for io in io_list:
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                           db_connection)

                io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io)
                driver.get(io_form_url)
                time.sleep(invoice_form.ONE_SEC_DELAY)
                if invoice_form.is_alert_popup_available(1):
                    invoice_form.accept_alert()
                if "0.00" != io_form.get_specific_finance_profile_status(
                        IoFormLocators.total_amount_invoiced_info_data_qa):
                    io_form.click_on_save_and_generate_io_button(
                        locator_to_be_appeared=IoFormLocators.success_message_data_qa)
            generic_modules.step_info("[END] MODIFYING EXISTING IOS & INVOICES")

            generic_modules.step_info(
                "[START - RTB-9069] Validate daily auto billing for interim invoice & Grouping by account and IO without "
                "last month invoice and last month spent > 50 (For complete/incomplete status)")

            generic_modules.step_info("[START] RUNNING DAILY CRON JOB AND DATA VALIDATION")
            for io in io_list:
                if io not in previous_io_invoices:
                    previous_io_invoices[io] = set()
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                for invoice_id in invoice_ids:
                    previous_io_invoices[io].add(invoice_id)

            base_url = (config['credential']['url'].split('//'))[1]
            cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
                'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                               'daily-auto-billing-cron-job']
            try:
                driver.get(cron_job_url)
            except Exception as e:
                print(e)
                pass

            for io in io_list:
                if io not in actual_io_invoices:
                    actual_io_invoices[io] = set()
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                for invoice_id in invoice_ids:
                    actual_io_invoices[io].add(invoice_id)

            assert previous_io_invoices == actual_io_invoices
            generic_modules.step_info("[END] RUNNING DAILY CRON JOB AND DATA VALIDATION")

            generic_modules.step_info(
                "[END - RTB-9069] Validate daily auto billing for interim invoice & Grouping by account and IO without "
                "last month invoice and last month spent > 50 (For complete/incomplete status)")

            generic_modules.step_info("[START] RUNNING MONTHLY CRON JOB AND DATA VALIDATION")
            base_url = (config['credential']['url'].split('//'))[1]
            cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
                'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                               'monthly-auto-billing-cron-job']
            try:
                driver.get(cron_job_url)
            except Exception as e:
                print(e)
                pass

            # [START] GETTING ACTUAL IO INVOICES
            for io in io_list:
                if io not in actual_io_invoices:
                    actual_io_invoices[io] = set()
                invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
                for invoice_id in invoice_ids:
                    actual_io_invoices[io].add(invoice_id)

            for key in actual_io_invoices:
                if key not in previous_io_invoices or len(actual_io_invoices[key]) != len(
                        previous_io_invoices[key]) + 1:
                    assert False
                else:
                    assert True
            # [END] GETTING ACTUAL IO INVOICES

            # [START] CREATING A DICT WITH LATEST INVOICES
            all_ios = set(previous_io_invoices.keys()) | set(actual_io_invoices.keys())
            latest_invoices = {}
            for key in all_ios:
                id1 = max(previous_io_invoices.get(key, []), default=None)
                id2 = max(actual_io_invoices.get(key, []), default=None)
                if id1 is None:
                    latest_id = id2
                else:
                    latest_id = max(id1, id2)
                if latest_id is not None:
                    latest_invoices[key] = {latest_id}
            # [END] CREATING A DICT WITH LATEST INVOICES

            for user in first_two:
                ios = first_two.get(user)
                invoice_id = latest_invoices.get(ios[0])
                invoice_id = str(invoice_id).replace('{', '').replace('}', '')
                invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
                    invoice_id)
                driver.get(invoice_form_url)
                if io_form.is_alert_popup_available(io_form.ONE_SEC_DELAY):
                    io_form.accept_alert()
                for io in ios:
                    io_number = IoUtils.pull_io_number(io, db_connection)
                    io_campaigns = IoUtils.pull_io_campaigns(io, db_connection)
                    io_campaigns = ', '.join(str(item) for item in io_campaigns)

                    io_currency = IoUtils.pull_io_currency(io, connection=db_connection)
                    if io_currency != 'USD':
                        last_month_spent = IoUtils.pull_last_month_spent_for_specific_io(io, last_month_first_date,
                                                                                         last_month_last_date,
                                                                                         db_connection)
                        io_media_budget_amount = IoUtils.pull_spent_amount_from_io_campaigns(io_campaigns,
                                                                                             db_connection)
                    else:
                        last_month_spent = IoUtils.pull_last_month_spent_for_specific_io(io, last_month_first_date,
                                                                                         last_month_last_date,
                                                                                         db_connection,
                                                                                         io_revenue_margin=True)
                        io_media_budget_amount = IoUtils.pull_spent_amount_from_io_campaigns(io_campaigns,
                                                                                             db_connection,
                                                                                             spent_alt=True)
                    io_media_budget_amount = round(float(io_media_budget_amount), 0)
                    last_month_spent = round(float(last_month_spent), 0)

                    # invoice_amount = io_media_budget_amount if io_media_budget_amount < last_month_spent else last_month_spent

                    media_budget_str = invoice_form.get_element_text(
                        InvoiceFormLocators.media_budget_amount_xpath.format(str(
                            io_number)), locator_initialization=True)
                    media_budget_str = media_budget_str.replace('(', '').replace(')', '').replace(',', '')
                    media_budget = round(float(media_budget_str), 0)
                    assert io_media_budget_amount == media_budget or last_month_spent == media_budget

                generic_modules.step_info("[END] RUNNING MONTHLY CRON JOB AND DATA VALIDATION")

        generic_modules.step_info(
            "[END - RTB-9068] Validate monthly auto billing for interim invoice & Grouping by account and IO without "
            "last month invoice and last month spent > 50 (For complete/incomplete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5'])
def test_regression_finance_backend_cron_jobs_for_daily_cron_3(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)
    company_form = DashboardCompanyForm(driver)

    user_list = []
    io_list = []

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-8867] Validate daily auto billing for interim invoice & Group all client accounts under one "
            "invoice (always a new IO+invoice(dedicated for self-service)) with last month invoice")
        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')
        io_ids = IoUtils.pull_ios_from_one_company_multi_users_which_have_expected_amount_of_spent('Complete',
                                                                                                   last_month_first_date,
                                                                                                   last_month_last_date,
                                                                                                   db_connection,
                                                                                                   compare_sign='>')
        if io_ids is not {}:
            first_two = dict(islice(io_ids.items(), 2))
            for key, value in first_two.items():
                user_list.append(key)
                io_list.append(value)
            io_list = [item for sublist in io_list for item in sublist]

            generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
            client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_list[0], db_connection)
            company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
                client_company_id)
            driver.get(company_form_url)

            remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
                CompanyFormLocators.auto_billing_remove_button_locator)
            for remove_button_element in remove_button_elements:
                remove_button_element.click()
                time.sleep(1)
                if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                    company_form.click_on_element(CompanyFormLocators.ok_button_locator)

            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
            company_form.check_uncheck_company_checkbox_radiobutton(
                CompanyFormLocators.group_all_client_account_self_service_label, do_check=True)
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.credit_limit_id,
                input_value="999999")
            dis_status = company_form.get_attribute_value(
                CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                attribute_name='disabled', locator_initialization=True)
            if not dis_status:
                company_form.set_text_using_tag_attribute(
                    attribute_name=company_form.id_attribute,
                    attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                    input_value="100")
            company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                              option_list_to_select=user_list)
            company_form.select_from_modal_form_using_js_code(
                CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=user_list[0])
            company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                          locator_to_be_appeared=CompanyFormLocators.success_message_locator,
                                          time_out=60)
            generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

            driver.get(config['credential']['url'])
            sidebar_navigation.navigate_to_page(PageNames.IO)
            io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
            io_list_page.wait_for_spinner_load()
            io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
            expected_row_count = io_list_page.get_element_text(IoListLocators.total_row_count_locator)
            expected_row_count = (expected_row_count.split('of'))[1]
            base_url = (config['credential']['url'].split('//'))[1]
            cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
                'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                               'daily-auto-billing-cron-job']
            try:
                driver.get(cron_job_url)
            except Exception as e:
                print(e)
                pass
            driver.get(config['credential']['url'])
            sidebar_navigation.navigate_to_page(PageNames.IO)
            io_list_page.select_dropdown_value(IoListLocators.client_company_data_qa, client_company_name)
            io_list_page.wait_for_spinner_load()
            io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
            actual_row_count = io_list_page.get_element_text(IoListLocators.total_row_count_locator)
            actual_row_count = (actual_row_count.split('of'))[1]
            assert expected_row_count == actual_row_count
            generic_modules.step_info(
                "[END - RTB-8867] Validate daily auto billing for interim invoice & Group all client accounts under one "
                "invoice (always a new IO+invoice(dedicated for self-service)) with last month invoice")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_daily_cron_3'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_4(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    company_form = DashboardCompanyForm(driver)

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-8868 & RTB-9070] Validate monthly auto billing for interim invoice & Group all client io's under "
            "one "
            "invoice without last month invoice and last month spent > 50 (For complete/incomplete status)")
        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')

        io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Complete',
                                                                    last_month_first_date,
                                                                    last_month_last_date,
                                                                    db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)
        io_ids, campaign_spent_list, io_number_list = IoUtils.pull_ios_from_one_user_which_have_expected_amount_of_spent(
            io_client_name,
            last_month_last_date,
            db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.group_all_client_ios_under_one_invoice_label, do_check=True)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        for io in io_ids:
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
        invoice_ids_for_assertion = IoUtils.pull_io_invoice(io_id, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
        io_wise_media_budget = {}
        io_wise_media_budget_2 = {}
        for io in io_ids:
            io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io)
            driver.get(io_form_url)
            if io_form_page.is_alert_popup_available(io_form_page.ONE_SEC_DELAY):
                io_form_page.accept_alert()
            io_form_page.click_on_save_and_generate_io_button(
                locator_to_be_appeared=IoFormLocators.success_message_data_qa)

            if io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.campaign_status_info_data_qa) == 'Complete':
                total_io_amount_str = io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.total_io_amount_info_data_qa)
                total_io_amount_str = total_io_amount_str.replace(",", "")
                total_io_amount = float(total_io_amount_str)

                total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.total_spent_amount_info_data_qa)
                total_spent_amount_str = total_spent_amount_str.split('(')[0]
                total_spent_amount_1 = total_spent_amount_str.replace(",", "")
                total_spent_amount_1 = float(total_spent_amount_1)

                total_io_amount = total_spent_amount_1 if total_spent_amount_1 < total_io_amount else total_io_amount

                rounded_campaign_spent = round(float(campaign_spent_list[io_ids.index(io)]), 0)
                total_spent_amount = rounded_campaign_spent if total_io_amount > rounded_campaign_spent else total_io_amount
            else:
                total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
                    IoFormLocators.spent_last_month_info_data_qa)
                total_spent_amount_str = total_spent_amount_str.split('(')[0]
                total_spent_amount = total_spent_amount_str.replace(",", "")
                total_spent_amount = float(total_spent_amount)
                total_io_amount = float(total_spent_amount)

            if io not in io_wise_media_budget:
                io_wise_media_budget[io_number_list[io_ids.index(io)]] = set()
                io_wise_media_budget_2[io_number_list[io_ids.index(io)]] = set()
            io_wise_media_budget[io_number_list[io_ids.index(io)]].add(total_spent_amount)
            io_wise_media_budget_2[io_number_list[io_ids.index(io)]].add(total_io_amount)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job']
        try:
            driver.get(cron_job_url)
        except Exception as e:
            print(e)
            pass
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert len(invoice_ids_for_assertion) + 1 == len(invoice_id_updated_list)
        generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

        generic_modules.step_info("[START] DATA VERIFICATION")
        set_1 = set(invoice_ids_for_assertion)
        set_2 = set(invoice_id_updated_list)
        created_invoice_id = (set_1 ^ set_2).pop()
        invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
            created_invoice_id)
        driver.get(invoice_form_url)
        if invoice_form.is_alert_popup_available(invoice_form.TWO_SEC_DELAY):
            invoice_form.accept_alert()

        for (io_number, io_media_budget), (io_number_2, io_media_budget_2) in zip(io_wise_media_budget.items(),
                                                                                  io_wise_media_budget_2.items()):
            media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.media_budget_amount_xpath.format(str(
                io_number)), locator_initialization=True)
            media_budget_str = media_budget_str.replace('(', '')
            media_budget_str = media_budget_str.replace(')', '')
            media_budget_str = media_budget_str.replace(',', '')
            media_budget = round(float(media_budget_str), 0)
            io_media_budget_float = float(next(iter(io_media_budget))) if isinstance(io_media_budget,
                                                                                     set) else io_media_budget
            io_media_budget_float_2 = float(next(iter(io_media_budget_2))) if isinstance(io_media_budget_2,
                                                                                         set) else io_media_budget_2
            io_media_budget_float = round(io_media_budget_float, 0)
            min_value = media_budget - io_media_budget_float
            min_value_2 = media_budget - io_media_budget_float_2
            if abs(min_value) <= 1 or abs(min_value_2) <= 1:
                assert True
            else:
                assert False

        if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
            invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
            time.sleep(io_form_page.TWO_SEC_DELAY)
            alert = driver.switch_to.alert
            alert.accept()
            assert "Invoice has been deleted!" in invoice_form.get_success_message()
        generic_modules.step_info("[END] DATA VERIFICATION")

        generic_modules.step_info(
            "[END - RTB-8868 & RTB-9070] Validate monthly auto billing for interim invoice & Group all client io's under "
            "one "
            "invoice without last month invoice and last month spent > 50 (For complete/incomplete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_4'])
def test_regression_finance_backend_cron_jobs_for_daily_cron_4(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if debug_mode:
        if sidebar_navigation.is_first_date_or_last_date_of_the_month():
            pytest.skip("Test skipped because it's the first or last date of the month")
        if "qa-testing" in config['credential']['url']:
            pytest.skip("Skipping test because it's running in qa-testing!!!!!")
        generic_modules.step_info(
            "[START - RTB-8869 & RTB-9071] Validate daily auto billing for interim invoice & Group all client io's under one "
            "invoice without last month invoice and last month spent > 50 (For complete/incomplete status)")
        last_month_first_date = sidebar_navigation.get_first_day_of_previous_month('%Y-%m-%d')
        last_month_last_date = sidebar_navigation.get_last_day_of_previous_month('%Y-%m-%d')
        io_id = IoUtils.pull_io_which_have_expected_amount_of_spent('Complete',
                                                                    last_month_first_date,
                                                                    last_month_last_date,
                                                                    db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)
        io_ids, campaign_spent_list, io_number_list = IoUtils.pull_ios_from_one_user_which_have_expected_amount_of_spent(
            io_client_name,
            last_month_last_date,
            db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.group_all_client_ios_under_one_invoice_label, do_check=True)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        for io in io_ids:
            invoice_ids = IoUtils.pull_io_invoice(io, db_connection)
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
        invoice_ids_for_assertion = IoUtils.pull_io_invoice(io_id, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'daily-auto-billing-cron-job']
        try:
            driver.get(cron_job_url)
        except Exception as e:
            print(e)
            pass
        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
        driver.get(io_form_url)
        time.sleep(invoice_form.ONE_SEC_DELAY)
        if invoice_form.is_alert_popup_available(1):
            invoice_form.accept_alert()
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert len(invoice_ids_for_assertion) == len(invoice_id_updated_list)
        generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

        generic_modules.step_info(
            "[END - RTB-8869 & RTB-9070] Validate daily auto billing for interim invoice & Group all client io's under one "
            "invoice without last month invoice and last month spent > 50 (For complete/incomplete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_complete_status(login_by_user_type,
                                                                               open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8515] Validate monthly auto billing for interim invoice & One line DSP services"
        " without last month invoice and last month spent > 50 (For complete status)")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_spent_amount_info_data_qa)
    total_spent_amount_str = total_spent_amount_str.split('(')[0]
    total_spent_amount = total_spent_amount_str.replace(",", "")
    total_spent_amount = float(total_spent_amount)

    total_io_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_io_amount_info_data_qa)
    total_io_amount_str = total_io_amount_str.replace(",", "")
    total_io_amount = float(total_io_amount_str)

    invoice_amount = total_spent_amount if total_spent_amount < total_io_amount else total_io_amount

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[START - RTB-8516] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "with last month invoice and last month spent > 50 (For complete status)")
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info(
        "[END - RTB-8516] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "with last month invoice and last month spent > 50 (For complete status)")

    generic_modules.step_info("[START] DATA VERIFICATION FOR RTB-8515")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
        InvoiceFormLocators.media_budgets_info_locator)
    assert len(media_budget_elements) == 1
    actual_invoice_amount_str = invoice_form.get_element_text(InvoiceFormLocators.media_budgets_locator.format('1'),
                                                              locator_initialization=True, input_tag=True)
    actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
    actual_invoice_amount = float(actual_invoice_amount_str)

    total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
    total_media_budget_str = total_media_budget_str.replace(",", "")
    total_media_budget = float(total_media_budget_str)
    assert actual_invoice_amount == total_media_budget == invoice_amount
    generic_modules.step_info("[END] DATA VERIFICATION FOR RTB-8515")

    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8515] Validate monthly auto billing for interim invoice & One line DSP services"
        " without last month invoice and last month spent > 50 (For complete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_complete_status'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_complete_status_2(login_by_user_type,
                                                                                 open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    total_spent_amount_2 = 0
    country_wise_expected_total_media_budget = {}
    country_wise_db_total_media_budget = {}

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8707] Validate monthly auto billing for interim invoice & By media budget and country "
        "without last month invoice and last month spent > 50 (For complete status))")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                              "AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
    expected_country_list = list(set(country_list))
    expected_country_list = sorted(expected_country_list)
    invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids, expected_country_list)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    country_wise_ui_total_media_budget = io_form_page.get_country_wise_total_media_budget()
    country_wise_ui_total_media_budget = dict(sorted(country_wise_ui_total_media_budget.items()))

    country_code_wise_db_total_media_budget = IoUtils.pull_country_wise_actual_io_campaign_spent(io_id, db_connection)

    # TODO: Need to talk with dev to identify the issue
    # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
    total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_spent_amount_info_data_qa)
    total_spent_amount_str = total_spent_amount_str.split('(')[0]
    total_spent_amount = total_spent_amount_str.replace(",", "")
    total_spent_amount = float(total_spent_amount)
    invoice_amount = total_spent_amount
    # else:
    # [START] GETTING COUNTRY WISE MEDIA BUDGET
    for key, value in country_code_wise_db_total_media_budget.items():
        country_name = CountryUtils.pull_country_name(key, db_connection)
        if country_name not in country_wise_db_total_media_budget:
            country_wise_db_total_media_budget[country_name] = []
        country_wise_db_total_media_budget[country_name] = value
    country_wise_db_total_media_budget = dict(sorted(country_wise_db_total_media_budget.items()))

    for key, value in country_wise_ui_total_media_budget.items():
        if key in country_wise_db_total_media_budget:
            if value < float(country_wise_db_total_media_budget[key]):
                country_wise_expected_total_media_budget[key] = round(float(value), 2)
            else:
                float_value = float(country_wise_db_total_media_budget[key])
                country_wise_expected_total_media_budget[key] = round(float_value, 2)

    for value in country_wise_expected_total_media_budget.values():
        if isinstance(value, Decimal):
            total_spent_amount_2 += float(value)
        else:
            total_spent_amount_2 += value

    total_io_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_io_amount_info_data_qa)
    total_io_amount_str = total_io_amount_str.replace(",", "")
    total_io_amount = float(total_io_amount_str)

    invoice_amount_2 = total_spent_amount_2 if total_spent_amount_2 < total_io_amount else total_io_amount
    # [END] GETTING COUNTRY WISE MEDIA BUDGET

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                              "AUTO BILLING CRON JOB")

    generic_modules.step_info("[START] DATA VERIFICATION")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    # media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
    #     InvoiceFormLocators.media_budgets_info_locator)
    # TODO: Need to talk with dev to identify the issue
    # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
    #     assert len(media_budget_elements) == 1
    # else:
    #     assert len(media_budget_elements) == len(expected_country_list)

    total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
    total_media_budget_str = total_media_budget_str.replace(",", "")
    total_media_budget = float(total_media_budget_str)
    invoice_amount = round(invoice_amount, 2)
    invoice_amount_2 = round(invoice_amount_2, 2)
    assert total_media_budget == invoice_amount or total_media_budget == invoice_amount_2 or total_media_budget == total_io_amount

    # TODO: Need to talk with dev to identify the issue
    # if len(expected_country_list) == len(country_code_wise_db_total_media_budget):
    #     invoice_country_list = invoice_form.get_specific_media_table_column_data_from_invoice(
    #         IoFormLocators.country_row_info_data_qa)
    #     actual_country_list = list(set(invoice_country_list))
    #     actual_country_list = sorted(actual_country_list)
    #
    #     actual_country_wise_total_media_budget = invoice_form.get_country_wise_total_media_budget_from_invoice()
    #     actual_country_wise_total_media_budget = dict(sorted(actual_country_wise_total_media_budget.items()))
    #
    #     assert actual_country_list == expected_country_list
    #     assert actual_country_wise_total_media_budget == country_wise_expected_total_media_budget

    generic_modules.step_info("[END] DATA VERIFICATION")

    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8707] Validate monthly auto billing for interim invoice & By media budget and country "
        "without last month invoice and last month spent > 50 (For complete status))")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_complete_status_2'])
def test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status(login_by_user_type,
                                                                             open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8513] Validate daily auto billing for interim invoice & One line "
        "'DSP services' without last month invoice and last month spent > 50 (For complete status)")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8513] Validate daily auto billing for interim invoice & One line "
        "'DSP services' without last month invoice and last month spent > 50 (For complete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status'])
def test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status_2(login_by_user_type,
                                                                               open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8776] Validate daily auto billing for interim invoice & By media budget and country without "
        "last month invoice and last month spent > 50 (For complete status))")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING DAILY "
                              "AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
    expected_country_list = list(set(country_list))
    expected_country_list = sorted(expected_country_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT & COUNTRY WISE TOTAL MEDIA BUDGET")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids, expected_country_list)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list

    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info("[END RTB-8776] Validate daily auto billing for interim invoice & By media budget and "
                              "country without last month invoice and last month spent > 50 (For complete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status_2'])
def test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status_2_1(login_by_user_type,
                                                                                 open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8870] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For complete status)")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                               db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info(
        "[START - RTB-8871] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For complete status)")

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list_for_monthly = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) == len(invoice_id_updated_list_for_monthly)

    generic_modules.step_info(
        "[END - RTB-8871] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For complete status)")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING DAILY AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_spent_amount_info_data_qa)
    total_spent_amount_str = total_spent_amount_str.split('(')[0]
    total_spent_amount = total_spent_amount_str.replace(",", "")
    total_spent_amount = float(total_spent_amount)

    total_io_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_io_amount_info_data_qa)
    total_io_amount_str = total_io_amount_str.replace(",", "")
    total_io_amount = float(total_io_amount_str)

    invoice_amount = total_spent_amount if total_spent_amount < total_io_amount else total_io_amount

    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list_for_daily = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list_for_daily)

    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list_for_daily)
    created_invoice_id_for_daily = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id_for_daily)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
        InvoiceFormLocators.media_budgets_info_locator)
    assert len(media_budget_elements) == 1
    actual_invoice_amount_str = invoice_form.get_element_text(InvoiceFormLocators.media_budgets_locator.format('1'),
                                                              locator_initialization=True, input_tag=True)
    actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
    actual_invoice_amount = float(actual_invoice_amount_str)

    total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
    total_media_budget_str = total_media_budget_str.replace(",", "")
    total_media_budget = float(total_media_budget_str)
    assert actual_invoice_amount == total_media_budget == invoice_amount
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[START - RTB-8949] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' with last month invoice and last month spent > 50 (For complete status)")

    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list_for_daily_1 = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_id_updated_list_for_daily == invoice_id_updated_list_for_daily_1

    generic_modules.step_info(
        "[END - RTB-8949] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' with last month invoice and last month spent > 50 (For complete status)")

    generic_modules.step_info(
        "[START - RTB-8950] Validate monthly auto billing for End of IO budgets spend (campaign status = complete)"
        " & One line 'DSP services' with last month invoice and last month spent > 50 (For complete status)")

    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list_for_monthly = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_id_updated_list_for_daily == invoice_id_updated_list_for_monthly
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()

    generic_modules.step_info(
        "[END - RTB-8950] Validate monthly auto billing for End of IO budgets spend (campaign status = complete)"
        " & One line 'DSP services' with last month invoice and last month spent > 50 (For complete status)")

    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8870] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For complete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status_2_1'])
def test_regression_finance_backend_cron_jobs_for_monthly_cron_complete_status_2_2(login_by_user_type,
                                                                                   open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8953] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For complete status)")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING DAILY "
                              "AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
    expected_country_list = list(set(country_list))
    expected_country_list = sorted(expected_country_list)

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids, expected_country_list)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8953] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For complete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_complete_status_2_2'])
def test_regression_finance_backend_cron_jobs_for_daily_cron_complete_status_2_2(login_by_user_type,
                                                                                 open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    total_spent_amount_2 = 0
    country_wise_expected_total_media_budget = {}
    country_wise_db_total_media_budget = {}

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8872] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For complete status)")

    global complete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete']
    io_id = complete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                              "AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
    expected_country_list = list(set(country_list))
    expected_country_list = sorted(expected_country_list)

    country_wise_ui_total_media_budget = io_form_page.get_country_wise_total_media_budget()
    country_wise_ui_total_media_budget = dict(sorted(country_wise_ui_total_media_budget.items()))

    country_code_wise_db_total_media_budget = IoUtils.pull_country_wise_actual_io_campaign_spent(io_id, db_connection)

    # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
    total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_spent_amount_info_data_qa)
    total_spent_amount_str = total_spent_amount_str.split('(')[0]
    total_spent_amount = total_spent_amount_str.replace(",", "")
    total_spent_amount = float(total_spent_amount)
    invoice_amount = total_spent_amount
    # else:
    for key, value in country_code_wise_db_total_media_budget.items():
        country_name = CountryUtils.pull_country_name(key, db_connection)
        if country_name not in country_wise_db_total_media_budget:
            country_wise_db_total_media_budget[country_name] = []
        country_wise_db_total_media_budget[country_name] = value
    country_wise_db_total_media_budget = dict(sorted(country_wise_db_total_media_budget.items()))

    for key, value in country_wise_ui_total_media_budget.items():
        if key in country_wise_db_total_media_budget:
            if value < float(country_wise_db_total_media_budget[key]):
                country_wise_expected_total_media_budget[key] = round(float(value), 2)
            else:
                float_value = float(country_wise_db_total_media_budget[key])
                country_wise_expected_total_media_budget[key] = round(float_value, 2)

    for value in country_wise_expected_total_media_budget.values():
        if isinstance(value, Decimal):
            total_spent_amount_2 += float(value)
        else:
            total_spent_amount_2 += value

    total_io_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_io_amount_info_data_qa)
    total_io_amount_str = total_io_amount_str.replace(",", "")
    total_io_amount = float(total_io_amount_str)

    invoice_amount_2 = total_spent_amount_2 if total_spent_amount_2 < total_io_amount else total_io_amount

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids, expected_country_list)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                              "AUTO BILLING CRON JOB")

    generic_modules.step_info("[START] DATA VERIFICATION")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    # media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
    #     InvoiceFormLocators.media_budgets_info_locator)
    # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
    #     assert len(media_budget_elements) == 1
    # else:
    #     assert len(media_budget_elements) == len(expected_country_list)

    total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
    total_media_budget_str = total_media_budget_str.replace(",", "")
    total_media_budget = float(total_media_budget_str)
    invoice_amount = round(invoice_amount, 2)
    invoice_amount_2 = round(invoice_amount_2, 2)
    assert total_media_budget == invoice_amount or total_media_budget == invoice_amount_2 or total_media_budget == total_io_amount

    # if len(expected_country_list) == len(country_code_wise_db_total_media_budget):
    #     invoice_country_list = invoice_form.get_specific_media_table_column_data_from_invoice(
    #         IoFormLocators.country_row_info_data_qa)
    #     actual_country_list = list(set(invoice_country_list))
    #     actual_country_list = sorted(actual_country_list)
    #
    #     actual_country_wise_total_media_budget = invoice_form.get_country_wise_total_media_budget_from_invoice()
    #     actual_country_wise_total_media_budget = dict(sorted(actual_country_wise_total_media_budget.items()))
    #
    #     assert actual_country_list == expected_country_list
    #     assert actual_country_wise_total_media_budget == country_wise_expected_total_media_budget

    generic_modules.step_info("[END] DATA VERIFICATION")

    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8872] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For complete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_finance_backend_cron_jobs_for_monthly_cron_live_status_grater_than_fifty(login_by_user_type,
                                                                                  open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8602] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent > 50 (For live status)")
    global live
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live']
    io_id = live

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    if invoice_ids:
        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    last_month_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.spent_last_month_info_data_qa)
    last_month_spent_amount_str = last_month_spent_amount_str.split('(')[0]
    last_month_spent_amount = last_month_spent_amount_str.replace(",", "")
    last_month_spent_amount = float(last_month_spent_amount)

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[START - RTB-8704] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "with last month invoice and last month spent > 50 (For live status)")
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info(
        "[END - RTB-8704] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "with last month invoice and last month spent > 50 (For live status)")

    generic_modules.step_info("[START] DATA VERIFICATION")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
        InvoiceFormLocators.media_budgets_info_locator)
    assert len(media_budget_elements) == 1
    actual_invoice_amount_str = invoice_form.get_element_text(InvoiceFormLocators.media_budgets_locator.format('1'),
                                                              locator_initialization=True, input_tag=True)
    actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
    actual_invoice_amount = float(actual_invoice_amount_str)

    assert actual_invoice_amount == last_month_spent_amount
    generic_modules.step_info("[END] DATA VERIFICATION")

    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8602] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent > 50 (For live status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_monthly_cron_live_status_grater_than_fifty'])
def test_finance_backend_cron_jobs_for_daily_cron_live_status_grater_than_fifty(login_by_user_type,
                                                                                open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8601] Validate daily auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent > 50 (For live status)")

    global live
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live']
    io_id = live

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    if invoice_ids:
        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8601] Validate daily auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent > 50 (For live status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_daily_cron_live_status_grater_than_fifty'])
def test_finance_backend_cron_jobs_for_daily_cron_live_status_grater_than_fifty_2(login_by_user_type,
                                                                                  open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8782] Validate daily auto billing for interim invoice & By media budget and country without "
        "last month invoice and last month spent > 50 (For live status)")

    global live
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live']
    io_id = live

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    if invoice_ids:
        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8782] Validate daily auto billing for interim invoice & By media budget and country without "
        "last month invoice and last month spent > 50 (For live status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_daily_cron_live_status_grater_than_fifty_2'])
def test_finance_backend_cron_jobs_for_monthly_cron_live_status_grater_than_fifty_2(login_by_user_type,
                                                                                    open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8780] Validate monthly auto billing for interim invoice & By media budget and country without "
        "last month invoice and last month spent > 50 (For live status))")

    global live
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live']
    io_id = live

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                              "AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(company_form.ONE_SEC_DELAY)
    if company_form.is_alert_popup_available(1):
        company_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
    expected_country_list = list(set(country_list))
    expected_country_list = sorted(expected_country_list)

    # country_code_wise_db_total_media_budget = IoUtils.pull_country_wise_actual_io_campaign_spent(io_id, db_connection)

    total_io_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.total_io_amount_info_data_qa)
    total_io_amount_str = total_io_amount_str.replace(",", "")
    total_io_amount = float(total_io_amount_str)

    spent_last_month_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.spent_last_month_info_data_qa)
    spent_last_month_str = spent_last_month_str.replace(",", "")
    spent_last_month = float(spent_last_month_str)

    invoice_amount = spent_last_month if spent_last_month < total_io_amount else total_io_amount

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids, expected_country_list)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING MONTHLY "
                              "AUTO BILLING CRON JOB")

    generic_modules.step_info("[START] DATA VERIFICATION")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    # media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
    #     InvoiceFormLocators.media_budgets_info_locator)
    # if len(expected_country_list) != len(country_code_wise_db_total_media_budget):
    #     assert len(media_budget_elements) == 1
    # else:
    #     assert len(media_budget_elements) == len(expected_country_list)

    total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
    total_media_budget_str = total_media_budget_str.replace(",", "")
    total_media_budget = float(total_media_budget_str)
    invoice_amount = round(invoice_amount, 0)
    total_media_budget = round(total_media_budget, 0)
    assert total_media_budget == invoice_amount or total_media_budget == total_io_amount

    # if len(expected_country_list) == len(country_code_wise_db_total_media_budget):
    #     invoice_country_list = invoice_form.get_specific_media_table_column_data_from_invoice(
    #         IoFormLocators.country_row_info_data_qa)
    #     actual_country_list = list(set(invoice_country_list))
    #     actual_country_list = sorted(actual_country_list)
    #
    #     assert actual_country_list == expected_country_list

    generic_modules.step_info("[END] DATA VERIFICATION")

    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info("[END - RTB-8780] Validate monthly auto billing for interim invoice & By media budget "
                              "and country without last month invoice and last month spent > 50 (For live status))")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_monthly_cron_live_status_grater_than_fifty_2'])
def test_finance_backend_cron_jobs_for_monthly_cron_live_status_grater_than_fifty_2_2(login_by_user_type,
                                                                                      open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-9039] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For live status))")

    global live
    # with open('assets/temp/auto_billing_data.json') as json_file:
    # auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live']
    io_id = live

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    if invoice_ids:
        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[START - RTB-9039] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For live status))")

@pytest.mark.skip("Skipping test because of assertion failures, registered RTB-9521")
@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_finance_backend_cron_jobs_for_daily_cron_complete_status_less_than_fifty(login_by_user_type,
                                                                                  open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    invoice_form = DspDashboardInvoiceForm(driver)
    io_form_page = DspDashboardIoForm(driver)

    io_client_name, cron_job_url, invoice_ids, client_company_id = '', '', '', ''

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8517] Validate daily auto billing for interim invoice & One line 'DSP services'"
        " without last month invoice and last month spent < 50 (For complete status)")

    global complete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete_less_than_50']
    io_id = complete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")
    generic_modules.step_info(
        "[END - RTB-8517] Validate daily auto billing for interim invoice & One line 'DSP services'"
        " without last month invoice and last month spent < 50 (For complete status)")

    generic_modules.step_info(
        "[START - RTB-8947] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent < 50 (For complete status)")
    if io_id:
        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING DAILY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
        driver.get(io_form_url)
        time.sleep(company_form.ONE_SEC_DELAY)
        if company_form.is_alert_popup_available(1):
            company_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

        total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_spent_amount_info_data_qa)
        total_spent_amount_str = total_spent_amount_str.split('(')[0]
        total_spent_amount = total_spent_amount_str.replace(",", "")
        total_spent_amount = float(total_spent_amount)

        total_io_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_io_amount_info_data_qa)
        total_io_amount_str = total_io_amount_str.replace(",", "")
        total_io_amount = float(total_io_amount_str)

        invoice_amount = total_spent_amount if total_spent_amount < total_io_amount else total_io_amount

        if invoice_amount > 50:
            driver.get(cron_job_url)
            invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
            assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
            generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING DAILY AUTO BILLING CRON JOB")

            generic_modules.step_info("[START] DATA VERIFICATION")
            set_1 = set(invoice_ids)
            set_2 = set(invoice_id_updated_list)
            created_invoice_id = (set_1 ^ set_2).pop()
            invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
                created_invoice_id)
            driver.get(invoice_form_url)
            time.sleep(invoice_form.ONE_SEC_DELAY)
            if invoice_form.is_alert_popup_available(1):
                invoice_form.accept_alert()
            media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
                InvoiceFormLocators.media_budgets_info_locator)
            assert len(media_budget_elements) == 1
            actual_invoice_amount_str = invoice_form.get_element_text(
                InvoiceFormLocators.media_budgets_locator.format('1'),
                locator_initialization=True, input_tag=True)
            actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
            actual_invoice_amount = float(actual_invoice_amount_str)

            total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
            total_media_budget_str = total_media_budget_str.replace(",", "")
            total_media_budget = float(total_media_budget_str)
            assert actual_invoice_amount == total_media_budget == invoice_amount
            generic_modules.step_info("[END] DATA VERIFICATION")

            if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
                invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
                if invoice_form.is_alert_popup_available(2):
                    invoice_form.accept_alert()
                assert "Invoice has been deleted!" in invoice_form.get_success_message()
    generic_modules.step_info(
        "[END - RTB-8947] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent < 50 (For complete status)")


@pytest.mark.skip("Skipping test because of assertion failures, registered RTB-9521")
@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_daily_cron_complete_status_less_than_fifty'])
def test_finance_backend_cron_jobs_for_monthly_cron_complete_status_less_than_fifty(login_by_user_type,
                                                                                    open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    invoice_form = DspDashboardInvoiceForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8518] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent < 50 (For complete status)")

    global complete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete_less_than_50']
    io_id = complete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                   db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
        driver.get(io_form_url)
        time.sleep(company_form.ONE_SEC_DELAY)
        if company_form.is_alert_popup_available(1):
            company_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

        total_spent_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_spent_amount_info_data_qa)
        total_spent_amount_str = total_spent_amount_str.split('(')[0]
        total_spent_amount = total_spent_amount_str.replace(",", "")
        total_spent_amount = float(total_spent_amount)

        total_io_amount_str = io_form_page.get_specific_finance_profile_status(
            IoFormLocators.total_io_amount_info_data_qa)
        total_io_amount_str = total_io_amount_str.replace(",", "")
        total_io_amount = float(total_io_amount_str)

        invoice_amount = total_spent_amount if total_spent_amount < total_io_amount else total_io_amount

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        if invoice_amount > 50:
            driver.get(cron_job_url)
            invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
            assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
            generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

            generic_modules.step_info("[START] DATA VERIFICATION")
            set_1 = set(invoice_ids)
            set_2 = set(invoice_id_updated_list)
            created_invoice_id = (set_1 ^ set_2).pop()
            invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
                created_invoice_id)
            driver.get(invoice_form_url)
            time.sleep(invoice_form.ONE_SEC_DELAY)
            if invoice_form.is_alert_popup_available(1):
                invoice_form.accept_alert()
            media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
                InvoiceFormLocators.media_budgets_info_locator)
            assert len(media_budget_elements) == 1
            actual_invoice_amount_str = invoice_form.get_element_text(
                InvoiceFormLocators.media_budgets_locator.format('1'),
                locator_initialization=True, input_tag=True)
            actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
            actual_invoice_amount = float(actual_invoice_amount_str)

            total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
            total_media_budget_str = total_media_budget_str.replace(",", "")
            total_media_budget = float(total_media_budget_str)
            assert actual_invoice_amount == total_media_budget == invoice_amount
            generic_modules.step_info("[END] DATA VERIFICATION")

        generic_modules.step_info(
            "[END - RTB-8518] Validate monthly auto billing for interim invoice & One line 'DSP services' "
            "without last month invoice and last month spent < 50 (For complete status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_monthly_cron_complete_status_less_than_fifty'])
def test_finance_backend_cron_jobs_for_monthly_cron_complete_status_less_than_fifty_2(login_by_user_type,
                                                                                      open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8708] Validate monthly auto billing for interim invoice &  By media budget and country "
        "without last month invoice and last month spent < 50 (For complete status)")

    global complete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete_less_than_50']
    io_id = complete_less_than_50

    if io_id:
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
        driver.get(io_form_url)
        time.sleep(company_form.ONE_SEC_DELAY)
        if company_form.is_alert_popup_available(1):
            company_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        if invoice_id_updated_list:
            assert len(invoice_ids) == len(invoice_id_updated_list)
        else:
            assert invoice_id_updated_list == []
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

        generic_modules.step_info(
            "[END - RTB-8708] Validate monthly auto billing for interim invoice &  By media budget and country "
            "without last month invoice and last month spent < 50 (For complete status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_monthly_cron_complete_status_less_than_fifty_2'])
def test_finance_backend_cron_jobs_for_monthly_cron_complete_status_less_than_fifty_2_2(login_by_user_type,
                                                                                        open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8954] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent < 50 (For complete status)")

    global complete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['complete_less_than_50']
    io_id = complete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] GETTING INVOICE AMOUNT, COUNTRY WISE TOTAL MEDIA BUDGET AND RUNNING DAILY "
                                  "AUTO BILLING CRON JOB")
        io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
        driver.get(io_form_url)
        time.sleep(invoice_form.ONE_SEC_DELAY)
        if invoice_form.is_alert_popup_available(1):
            invoice_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

        country_list = io_form_page.get_specific_media_table_column_data(IoFormLocators.country_row_info_data_qa)
        expected_country_list = list(set(country_list))
        expected_country_list = sorted(expected_country_list)

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        invoice_form.navigate_to_specific_invoice_and_add_country(config, invoice_ids, expected_country_list)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        base_url = (config['credential']['url'].split('//'))[1]
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

        generic_modules.step_info(
            "[END - RTB-8954] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
            "By media budget and country without last month invoice and last month spent < 50 (For complete status)")

        generic_modules.step_info(
            "[START - RTB-8948] Validate monthly auto billing for End of IO budgets spend (campaign status = complete)"
            " & One line 'DSP services' without last month invoice and last month spent < 50 (For complete status)")

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        driver.get(company_form_url)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING IO AND INVOICES")
        invoice_ids_for_monthly = IoUtils.pull_io_invoice(io_id, db_connection)
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids_for_monthly,
                                                                                   db_connection)
        driver.get(io_form_url)
        time.sleep(company_form.ONE_SEC_DELAY)
        if company_form.is_alert_popup_available(1):
            company_form.accept_alert()
        io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)
        generic_modules.step_info("[END] MODIFYING EXISTING IO AND INVOICES")

        invoice_ids_for_monthly = IoUtils.pull_io_invoice(io_id, db_connection)
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list_for_monthly = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids_for_monthly == invoice_id_updated_list_for_monthly

        generic_modules.step_info(
            "[END - RTB-8948] Validate monthly auto billing for End of IO budgets spend (campaign status = complete)"
            " & One line 'DSP services' without last month invoice and last month spent < 50 (For complete status)")


# TODO: After bug fix, I need to enable this again
@pytest.mark.skip("Due to bug RTB-9214")
@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_grater_than_fifty(login_by_user_type,
                                                                                        open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8597] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent > 50 (For incomplete status)")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    last_month_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.spent_last_month_info_data_qa)
    last_month_spent_amount_str = last_month_spent_amount_str.split('(')[0]
    last_month_spent_amount = last_month_spent_amount_str.replace(",", "")
    last_month_spent_amount = float(last_month_spent_amount)

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info("[START] DATA VERIFICATION")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
        InvoiceFormLocators.media_budgets_info_locator)
    assert len(media_budget_elements) == 1
    actual_invoice_amount_str = invoice_form.get_element_text(InvoiceFormLocators.media_budgets_locator.format('1'),
                                                              locator_initialization=True, input_tag=True)
    actual_invoice_amount_str = actual_invoice_amount_str.replace(",", "")
    actual_invoice_amount = float(actual_invoice_amount_str)

    assert actual_invoice_amount == last_month_spent_amount
    generic_modules.step_info("[END] DATA VERIFICATION")

    generic_modules.step_info(
        "[START - RTB-8598] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "with last month invoice and last month spent > 50 (For incomplete status)")
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info(
        "[END - RTB-8598] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "with last month invoice and last month spent > 50 (For incomplete status)")

    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8597] Validate monthly auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent > 50 (For incomplete status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_grater_than_fifty'])
def test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty(login_by_user_type,
                                                                                      open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8519] Validate daily auto billing for interim invoice & One line 'DSP services'"
        " without last month invoice and last month spent > 50 (For incomplete status)")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8519] Validate daily auto billing for interim invoice & One line 'DSP services'"
        " without last month invoice and last month spent > 50 (For incomplete status)")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty'])
def test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty_2(login_by_user_type,
                                                                                        open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8779] Validate daily auto billing for interim invoice & By media budget and country without last"
        " month invoice and last month spent > 50 (For incomplete status)")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8779] Validate daily auto billing for interim invoice & By media budget and country without last "
        "month invoice and last month spent > 50 (For incomplete status))")


@pytest.mark.dependency(depends=['test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty_2'])
def test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_grater_than_fifty_2(login_by_user_type,
                                                                                          open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)

    if io_form_page.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8777] Validate monthly auto billing for interim invoice &  By media budget and country without "
        "last month invoice and last month spent > 50 (For incomplete status))")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")
    io_form_url = config['credential']['url'] + config['io-form-page']['io-form-url'].format(io_id)
    driver.get(io_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)

    last_month_spent_amount_str = io_form_page.get_specific_finance_profile_status(
        IoFormLocators.spent_last_month_info_data_qa)
    last_month_spent_amount_str = last_month_spent_amount_str.split('(')[0]
    last_month_spent_amount = last_month_spent_amount_str.replace(",", "")
    last_month_spent_amount = float(last_month_spent_amount)

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert len(invoice_ids) + 1 == len(invoice_id_updated_list)
    generic_modules.step_info("[END] GETTING INVOICE AMOUNT AND RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info("[START] DATA VERIFICATION")
    set_1 = set(invoice_ids)
    set_2 = set(invoice_id_updated_list)
    created_invoice_id = (set_1 ^ set_2).pop()
    invoice_form_url = config['credential']['url'] + config['invoice-form-page']['invoice-form-url'].format(
        created_invoice_id)
    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()

    # TODO: Need to fix this
    # media_budget_elements = invoice_form.wait_for_presence_of_all_elements_located(
    #     InvoiceFormLocators.media_budgets_info_locator)

    # assert len(media_budget_elements) == 1

    total_media_budget_str = invoice_form.get_element_text(InvoiceFormLocators.total_media_budget_info_data_qa)
    total_media_budget_str = total_media_budget_str.replace(",", "")
    actual_invoice_amount = float(total_media_budget_str)

    min_value = actual_invoice_amount - last_month_spent_amount

    if abs(min_value) <= 5:
        assert True
    else:
        assert False
    generic_modules.step_info("[END] DATA VERIFICATION")

    driver.get(invoice_form_url)
    time.sleep(invoice_form.ONE_SEC_DELAY)
    if invoice_form.is_alert_popup_available(1):
        invoice_form.accept_alert()
    if invoice_form.is_element_present(InvoiceFormLocators.delete_button_locator, time_out=2):
        invoice_form.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form.get_success_message()

    generic_modules.step_info(
        "[END - RTB-8777] Validate monthly auto billing for interim invoice &  By media budget and country without "
        "last month invoice and last month spent > 50 (For incomplete status))")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_grater_than_fifty_2'])
def test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty_2_1(login_by_user_type,
                                                                                          open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8951] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For incomplete status)")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8951] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For incomplete status)")

    generic_modules.step_info(
        "[START - RTB-8952] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For incomplete status)")

    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list

    generic_modules.step_info(
        "[END - RTB-8952] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "One line 'DSP services' without last month invoice and last month spent > 50 (For incomplete status)")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty_2_1'])
def test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_grater_than_fifty_2_2(login_by_user_type,
                                                                                            open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-9038] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) "
        "& By media budget and country without last month invoice and last month spent > 50 (For incomplete status))")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-9038] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) "
        "& By media budget and country without last month invoice and last month spent > 50 (For incomplete status))")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_grater_than_fifty_2_2'])
def test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_grater_than_fifty_2_2(login_by_user_type,
                                                                                          open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-9038] Validate daily auto billing for End of IO budgets spend (campaign status = complete) "
        "& By media budget and country without last month invoice and last month spent > 50 (For incomplete status)")

    global incomplete
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete']
    io_id = incomplete

    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
    io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

    generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
    client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
    company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
        client_company_id)
    driver.get(company_form_url)

    remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
        CompanyFormLocators.auto_billing_remove_button_locator)
    for remove_button_element in remove_button_elements:
        remove_button_element.click()
        time.sleep(1)
        if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
            company_form.click_on_element(CompanyFormLocators.ok_button_locator)

    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
    company_form.check_uncheck_company_checkbox_radiobutton(
        CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.set_text_using_tag_attribute(
        attribute_name=company_form.id_attribute,
        attribute_value=CompanyFormLocators.credit_limit_id,
        input_value="999999")
    dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                  attribute_name='disabled', locator_initialization=True)
    if not dis_status:
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
            input_value="100")
    company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                      option_to_select=io_client_name)
    company_form.select_from_modal_form_using_js_code(
        CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
    company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                  locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

    generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
    invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
    generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

    generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
    invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

    base_url = (config['credential']['url'].split('//'))[1]
    cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
        'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                       'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
    driver.get(cron_job_url)
    invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
    assert invoice_ids == invoice_id_updated_list
    generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-9038] Validate daily auto billing for End of IO budgets spend (campaign status = complete) "
        "& By media budget and country without last month invoice and last month spent > 50 (For incomplete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_less_than_fifty(login_by_user_type,
                                                                                      open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8600] Validate monthly auto billing for interim invoice & One line 'DSP services' without last "
        "month invoice and last month spent < 50 (For incomplete status)")

    global incomplete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete_less_than_50']
    io_id = incomplete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8600] Validate monthly auto billing for interim invoice & One line 'DSP services' without last "
        "month invoice and last month spent < 50 (For incomplete status)")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_less_than_fifty'])
def test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_less_than_fifty(login_by_user_type,
                                                                                    open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8599] Validate daily auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent < 50 (For incomplete status)")

    global incomplete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete_less_than_50']
    io_id = incomplete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        if invoice_ids:
            generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
            generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8599] Validate daily auto billing for interim invoice & One line 'DSP services' "
        "without last month invoice and last month spent < 50 (For incomplete status)")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_daily_cron_incomplete_status_less_than_fifty'])
def test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_less_than_fifty_2(login_by_user_type,
                                                                                        open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8778]  Validate monthly auto billing for interim invoice &  By media budget and country without "
        "last month invoice and last month spent < 50 (For incomplete status))")

    global incomplete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete_less_than_50']
    io_id = incomplete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8778]  Validate monthly auto billing for interim invoice &  By media budget and country without "
        "last month invoice and last month spent < 50 (For incomplete status))")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_less_than_fifty_2'])
def test_finance_backend_cron_jobs_for_monthly_cron_incomplete_status_less_than_fifty_2_2(login_by_user_type,
                                                                                          open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-9038] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent < 50 (For incomplete status)")

    global incomplete_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['incomplete_less_than_50']
    io_id = incomplete_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-9038] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent < 50 (For incomplete status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_finance_backend_cron_jobs_for_daily_cron_live_status_less_than_fifty(login_by_user_type,
                                                                              open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    invoice_form = DspDashboardInvoiceForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8705] Validate daily auto billing for interim invoice & One line 'DSP services'"
        " without last month invoice and last month spent < 50 (For Live status)")

    global live_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live_less_than_50']
    io_id = live_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        if invoice_ids:
            generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
            generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8705] Validate daily auto billing for interim invoice & One line 'DSP services'"
        " without last month invoice and last month spent < 50 (For Live status)")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_daily_cron_live_status_less_than_fifty'])
def test_finance_backend_cron_jobs_for_monthly_cron_live_status_less_than_fifty(login_by_user_type,
                                                                                open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    invoice_form = DspDashboardInvoiceForm(driver)
    company_form = DashboardCompanyForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8706] Validate monthly auto billing for interim invoice & One line 'DSP services' without last "
        "month invoice and last month spent < 50 (For Live status)")

    global live_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live_less_than_50']
    io_id = live_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.one_line_dsp_services_default_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
        invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids, db_connection)
        generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING DAILY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING DAILY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8706] Validate monthly auto billing for interim invoice & One line 'DSP services' without last "
        "month invoice and last month spent < 50 (For Live status)")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_monthly_cron_live_status_less_than_fifty'])
def test_finance_backend_cron_jobs_for_monthly_cron_live_status_less_than_fifty_2(login_by_user_type,
                                                                                  open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    invoice_form = DspDashboardInvoiceForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-8781] Validate monthly auto billing for interim invoice & By media budget and country without"
        " last month invoice and last month spent < 50 (For live status)")

    global live_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live_less_than_50']
    io_id = live_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        if invoice_ids:
            generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
            generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-8781] Validate monthly auto billing for interim invoice & By media budget and country without last "
        "month invoice and last month spent < 50 (For live status)")


@pytest.mark.dependency(
    depends=['test_finance_backend_cron_jobs_for_monthly_cron_live_status_less_than_fifty_2'])
def test_finance_backend_cron_jobs_for_monthly_cron_live_status_less_than_fifty_2_2(login_by_user_type,
                                                                                    open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    invoice_form = DspDashboardInvoiceForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-9039] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent < 50 (For live status)")

    global live_less_than_50
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live_less_than_50']
    io_id = live_less_than_50

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        if invoice_ids:
            generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
            generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'monthly-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-9039] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent < 50 (For live status)")


@pytest.mark.dependency(depends=['test_regression_finance_backend_cron_jobs_for_monthly_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_and_daily_cron_for_multi_billing_process',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_1_5',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_3',
                                 'test_regression_finance_backend_cron_jobs_for_monthly_cron_4',
                                 'test_regression_finance_backend_cron_jobs_for_daily_cron_4',
                                 'test_regression_prerequisite_test_case_to_collect_data'])
def test_finance_backend_cron_jobs_for_daily_cron_live_status_grater_than_fifty_2_2(login_by_user_type,
                                                                                    open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    company_form = DashboardCompanyForm(driver)
    invoice_form = DspDashboardInvoiceForm(driver)

    if invoice_form.is_first_date_or_last_date_of_the_month():
        pytest.skip("Test skipped because it's the first or last date of the month")
    if "qa-testing" in config['credential']['url']:
        pytest.skip("Skipping test because it's running in qa-testing!!!!!")
    generic_modules.step_info(
        "[START - RTB-9039] Validate daily auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For live status)")

    global live
    # with open('assets/temp/auto_billing_data.json') as json_file:
    #     auto_billing_data = json.load(json_file)

    # io_id = auto_billing_data['different_status']['live']
    io_id = live

    if io_id:
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)
        io_client_name = IoUtils.pull_io_client_name(io_id, db_connection)

        generic_modules.step_info("[START] UPDATING COMPANY PROFILE")
        client_company_id, client_company_name = IoUtils.pull_io_company_name_and_id(io_id, db_connection)
        company_form_url = config['credential']['url'] + config['company-pages']['company-form-url'].format(
            client_company_id)
        driver.get(company_form_url)

        remove_button_elements = company_form.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(1)
            if company_form.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form.click_on_element(CompanyFormLocators.ok_button_locator)

        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label, do_check=False)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=True)
        company_form.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.by_media_budget_and_country_label, do_check=True)
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.set_text_using_tag_attribute(
            attribute_name=company_form.id_attribute,
            attribute_value=CompanyFormLocators.credit_limit_id,
            input_value="999999")
        dis_status = company_form.get_attribute_value(CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                                                      attribute_name='disabled', locator_initialization=True)
        if not dis_status:
            company_form.set_text_using_tag_attribute(
                attribute_name=company_form.id_attribute,
                attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                input_value="100")
        company_form.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                          option_to_select=io_client_name)
        company_form.select_from_modal_form_using_js_code(
            CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select=io_client_name)
        company_form.click_on_element(CompanyFormLocators.save_button_locator,
                                      locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
        generic_modules.step_info("[END] UPDATING COMPANY PROFILE")

        if invoice_ids:
            generic_modules.step_info("[START] MODIFYING EXISTING INVOICES")
            invoice_form.navigate_to_specific_invoice_and_update_date_and_media_budget(config, invoice_ids,
                                                                                       db_connection)
            generic_modules.step_info("[END] MODIFYING EXISTING INVOICES")

        generic_modules.step_info("[START] RUNNING MONTHLY AUTO BILLING CRON JOB")
        invoice_ids = IoUtils.pull_io_invoice(io_id, db_connection)

        base_url = (config['credential']['url'].split('//'))[1]
        cron_job_url = "https://" + config['debugger_credentials']['debugging-username'] + ":" + config[
            'debugger_credentials']['debugging-password'] + "@" + base_url + config['cron-jobs'][
                           'daily-auto-billing-cron-job-for-specific-io'].format(io_id)
        driver.get(cron_job_url)
        invoice_id_updated_list = IoUtils.pull_io_invoice(io_id, db_connection)
        assert invoice_ids == invoice_id_updated_list
        generic_modules.step_info("[END] RUNNING MONTHLY AUTO BILLING CRON JOB")

    generic_modules.step_info(
        "[END - RTB-9039] Validate monthly auto billing for End of IO budgets spend (campaign status = complete) & "
        "By media budget and country without last month invoice and last month spent > 50 (For live status)")
