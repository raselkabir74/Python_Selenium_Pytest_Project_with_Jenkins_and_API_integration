import json

from configurations import generic_modules
from locators.index.index_locator import IndexLocator
from locators.navbar.navbar_locators import NavbarLocators
from locators.user.userform_locators import UserFormLocators
from pages.index.index import DspDashboardIndex
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.user.user_form import DashboardUserFormPage
from pages.user.user_list_form import DashboardUserListForm
from utils.user import UserUtils as UserUtil
from utils.page_names_enum import PageNames


def test_dashboard_add_user_with_all_users_for_child_acc(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    user_list_page = DashboardUserListForm(driver)
    user_page = DashboardUserFormPage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)
    index_page = DspDashboardIndex(config, driver)

    generic_modules.step_info("[START - RTB-8756] Verify added child account for new user")

    with open('assets/user/user_data.json') as json_file:
        user_data = json.load(json_file)
    user_data['main_and_billing_info']['username'] = \
        user_data['main_and_billing_info'][
            'username'] + generic_modules.get_random_string()
    generated_password = generic_modules.get_random_string(10)

    # ADD USER
    side_bar_navigation.navigate_to_page(PageNames.USERS)
    user_list_page.navigate_to_add_user_page()
    user_page.provide_user_mandatory_information(user_data, generated_password)
    user_page.check_uncheck_checkbox(UserFormLocators.all_users_label, do_check=True)
    user_page.click_save_user_btn()
    pulled_selected_child_acc_option = UserUtil.get_user_parent_af_all_users_status(
        user_data['main_and_billing_info']['username'], db_connection)
    all_users_option = 1
    assert all_users_option == pulled_selected_child_acc_option

    # IMPERSONATE USER
    navbar.logout_user()
    index_page.login_user(user_data['main_and_billing_info']['username'],
                          generated_password)
    index_page.check_uncheck_specific_checkbox(IndexLocator.terms_and_conditions_checkbox_label, do_check=True)
    index_page.click_on_element(IndexLocator.submit_btn_locator)
    navbar.impersonate_user('AutomationAdminUser')
    assert 'AutomationAdminUser' == navbar.get_element_text(NavbarLocators.account_dropdown_locator)

    generic_modules.step_info("[END - RTB-8756] Verify added child account for new user")


def test_dashboard_add_user_with_one_user_for_child_acc(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    user_list_page = DashboardUserListForm(driver)
    user_page = DashboardUserFormPage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)
    index_page = DspDashboardIndex(config, driver)

    generic_modules.step_info("[START - RTB-8756] Verify added child account for new user")

    with open('assets/user/user_data.json') as json_file:
        user_data = json.load(json_file)
    user_data['main_and_billing_info']['username'] = \
        user_data['main_and_billing_info'][
            'username'] + generic_modules.get_random_string()
    generated_password = generic_modules.get_random_string(10)

    # ADD USER
    side_bar_navigation.navigate_to_page(PageNames.USERS)
    user_list_page.navigate_to_add_user_page()
    user_page.provide_user_mandatory_information(user_data, generated_password)
    user_page.select_child_acc('AutomationAdminUser', '7722')
    user_page.click_save_user_btn()
    pulled_selected_child_acc_option = UserUtil.get_user_parent_af_all_users_status(
        user_data['main_and_billing_info']['username'], db_connection)
    selected_users_option = 0
    assert selected_users_option == pulled_selected_child_acc_option

    # IMPERSONATE USER
    navbar.logout_user()
    index_page.login_user(user_data['main_and_billing_info']['username'],
                          generated_password)
    index_page.check_uncheck_specific_checkbox(IndexLocator.terms_and_conditions_checkbox_label, do_check=True)
    index_page.click_on_element(IndexLocator.submit_btn_locator)
    navbar.impersonate_user('AutomationAdminUser')
    assert 'AutomationAdminUser' == navbar.get_element_text(NavbarLocators.account_dropdown_locator)

    generic_modules.step_info("[END - RTB-8756] Verify added child account for new user")
