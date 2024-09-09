import json

import pytest

from configurations.generic_modules import get_random_string
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.company.company_list_form import DashboardCompanyListForm
from pages.company.company_form import DashboardCompanyForm
from utils.compare import CompareUtils as CompareUtil
from utils.page_names_enum import PageNames


# TODO: Will fix later
@pytest.mark.skip()
def test_regression_add_edit_company(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    company_list_page = DashboardCompanyListForm(driver)
    company_form_page = DashboardCompanyForm(driver)
    with open('assets/company/company_data.json') as json_file:
        company_data = json.load(json_file)
    company_data['name'] = company_data['name'] + get_random_string()
    # ADD COMPANY
    sidebar_navigation.navigate_to_page(PageNames.CLIENTS_COMPANIES)
    company_list_page.navigate_to_add_company_page()
    company_form_page.provide_and_save_company_information(company_data)
    assert "Company saved successfully!" in company_list_page.get_success_message()
    # DATA VERIFICATION
    company_list_page.search_user_and_action(company_data['name'],
                                             action='edit')
    pulled_gui_data = company_form_page.get_company_information()
    print("Pulled gui data :", pulled_gui_data)
    print("Given gui data :", company_data)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_gui_data, company_data)
    # COMPANY EDIT
    with open('assets/company/company_edit_data.json') as json_file:
        edit_company_data = json.load(json_file)
    edit_company_data['name'] = edit_company_data[
                                    'name'] + get_random_string()
    company_list_page.search_user_and_action(company_data['name'],
                                             action='edit')
    company_form_page.provide_and_save_company_information(
        edit_company_data,
        mode='edit')
    assert "Company saved successfully!" in company_list_page.get_success_message()
    # DATA VERIFICATION OF COMPANY EDIT
    company_list_page.search_user_and_action(edit_company_data['name'],
                                             action='edit')
    pulled_gui_edit_data = company_form_page.get_company_information()
    print("Pulled gui data :", pulled_gui_edit_data)
    print("Given gui data :", edit_company_data)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_gui_edit_data, edit_company_data)
    # DATA CLEAN UP
    company_list_page.search_user_and_action(edit_company_data['name'],
                                             action='delete')
    company_list_page.search_user_and_action(edit_company_data['name'])
    assert "No matching records found" in company_list_page.get_no_record_found_message()
