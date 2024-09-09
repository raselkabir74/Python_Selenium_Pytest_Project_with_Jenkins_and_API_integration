import json
import time

from configurations import generic_modules
from locators.company.company_form_locators import CompanyFormLocators
from locators.io.io_form_locator import IoFormLocators
from pages.company.company_form import DashboardCompanyForm
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList


def test_regression_prerequisite_and_delete_io(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    company_form_page = DashboardCompanyForm(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = \
        io_data['io_main_information'][
            'io_title'] + generic_modules.get_random_string(5)

    io_creation_url = config['credential']['url'] + \
                      config['io-creation-page'][
                          'io-creation-url']

    generic_modules.step_info("[START] Prerequisite for extending base credit limit")
    webcoupers_company_profile_url = config['credential']['url'] + \
                                     config['company-pages']['webcoupers-url']
    test_automation_company_profile_url = config['credential']['url'] + \
                                          config['company-pages']['test-automation-company-url']
    company_list = []
    company_list.extend([webcoupers_company_profile_url, test_automation_company_profile_url])

    for company in company_list:
        driver.get(company)

        remove_button_elements = company_form_page.wait_for_presence_of_all_elements_located(
            CompanyFormLocators.auto_billing_remove_button_locator)
        for remove_button_element in remove_button_elements:
            remove_button_element.click()
            time.sleep(2)
            if company_form_page.is_element_present(CompanyFormLocators.ok_button_locator, time_out=2):
                company_form_page.click_on_element(CompanyFormLocators.ok_button_locator)

        if io_list_page.get_text_using_tag_attribute(io_list_page.input_tag,
                                                     io_list_page.id_attribute,
                                                     CompanyFormLocators.credit_limit_id) != "999999":
            io_list_page.set_text_using_tag_attribute(
                attribute_name=io_list_page.id_attribute,
                attribute_value=CompanyFormLocators.credit_limit_id,
                input_value="999999")
            if company is not test_automation_company_profile_url:
                io_list_page.set_text_using_tag_attribute(
                    attribute_name=io_list_page.id_attribute,
                    attribute_value=CompanyFormLocators.manually_reviewed_credit_limit_percentage_id,
                    input_value="100")
                company_form_page.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                                       option_to_select='Webcoupers')
                company_form_page.select_from_modal_form_using_js_code(
                    CompanyFormLocators.select_client_main_account_for_io_invoice_label, option_to_select='Webcoupers')
            else:
                company_form_page.select_from_modal_form_using_js_code(CompanyFormLocators.auto_billing_users_label,
                                                                       option_to_select='AutomationAdminUser')
                company_form_page.select_from_modal_form_using_js_code(
                    CompanyFormLocators.select_client_main_account_for_io_invoice_label,
                    option_to_select='AutomationAdminUser')
        company_form_page.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_month_interim_invoices_label,
            do_check=True)
        company_form_page.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.end_of_io_budgets_spend_campaign_status_complete_label, do_check=False)
        company_form_page.check_uncheck_company_checkbox_radiobutton(
            CompanyFormLocators.group_all_client_account_self_service_label, do_check=True)
        io_list_page.click_on_element(
            CompanyFormLocators.save_button_locator,
            locator_to_be_appeared=CompanyFormLocators.success_message_locator, time_out=60)
    generic_modules.step_info("[END] Prerequisite for extending base credit limit")

    generic_modules.step_info(
        "[START - RTB-6952]  Validate whether the Delete button is working properly")
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_save_and_generate_io_button(locator_to_be_appeared=IoFormLocators.success_message_data_qa)
    io_list_page.click_on_specific_button(IoFormLocators.delete_label)
    io_form_page.wait_alert_is_present()
    alert = io_list_page.driver.switch_to.alert
    alert.accept()
    assert "IO has been deleted!" in io_form_page.get_success_message()
    generic_modules.step_info(
        "[END - RTB-6952]  Validate whether the Delete button is working properly")
