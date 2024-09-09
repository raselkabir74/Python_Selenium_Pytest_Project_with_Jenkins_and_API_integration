import json

from configurations import generic_modules
from configurations.generic_modules import get_random_string
from locators.package.package_form_locator import PackageFormLocators
from locators.package.package_list_locator import PackageListLocators
from pages.package.packages_form import DashboardPackagesForm
from pages.package.packages_list import DashboardPackagesList
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.packages import PackagesUtils as PackageUtil
from utils.page_names_enum import PageNames
from pages.navbar.navbar import DashboardNavbar


def test_dashboard_add_package_open_auction_only(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    package_form_page = DashboardPackagesForm(driver)
    side_bar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-8314] Validate package creation with different auction types")
    with open('assets/packages/package_data.json') as json_file:
        package_data = json.load(json_file)
    package_data['package_mandatory_data']['name'] = package_data['package_mandatory_data'][
                                                         'name'] + get_random_string()
    package_data['sites'] = PackageUtil.read_site_domain_names()
    package_data['package_mandatory_data']['auction_type'] = "Open Auction only"

    # ADD PACKAGE
    side_bar_page.navigate_to_page(PageNames.PACKAGES)
    package_list_page.navigate_add_package()
    package_form_page.provide_package_data_and_save(package_data)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully! Package size will be calculated shortly." in success_message


def test_dashboard_add_package_pmp_only(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    package_form_page = DashboardPackagesForm(driver)
    side_bar_page = DashboardSidebarPage(driver)

    with open('assets/packages/package_data.json') as json_file:
        package_data = json.load(json_file)
    package_data['package_mandatory_data']['name'] = package_data['package_mandatory_data'][
                                                         'name'] + get_random_string()
    package_data['sites'] = PackageUtil.read_site_domain_names()
    package_data['package_mandatory_data']['auction_type'] = "PMP only"

    # ADD PACKAGE
    side_bar_page.navigate_to_page(PageNames.PACKAGES)
    package_list_page.navigate_add_package()
    package_form_page.provide_package_data_and_save(package_data)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully! Package size will be calculated shortly." in success_message
    generic_modules.step_info("[END - RTB-8314] Validate package creation with different auction types")

    generic_modules.step_info("[START - RTB-8309] Validate redirect functionality")
    package_list_page.set_value_into_element(PackageListLocators.search_box_locator, package_data[
        'package_mandatory_data']['name'])
    package_list_page.click_on_element(PackageListLocators.package_name_locator)
    assert "eskimi.com/admin/packages/form" in driver.current_url

    generic_modules.step_info("[END - RTB-8309] Validate redirect functionality")


def test_dashboard_package_multiple_edit(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    side_bar_page = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    generic_modules.step_info("[START - RTB-8310] Validate edit option warns")
    side_bar_page.navigate_to_page(PageNames.PACKAGES)
    navbar.impersonate_user('Webcoupers - GLO')
    package_list_page.click_on_element(PackageListLocators.edit_link_locator,
                                       locator_to_be_appeared=PackageListLocators.message_modal_ok_btn_locator)
    package_list_page.wait_for_visibility_of_element(PackageListLocators.message_modal_locator)
    assert "You must choose at least one package to do this operation!" == package_list_page.get_element_text(
        PackageListLocators.message_modal_locator)
    package_list_page.click_on_element(PackageListLocators.message_modal_ok_btn_locator,
                                       locator_to_be_appeared=PackageListLocators.add_package_button_locator_data_qa)
    package_list_page.click_on_checkboxes(PackageListLocators.checkbox_locator)
    package_list_page.click_on_element(PackageListLocators.edit_link_locator,
                                       locator_to_be_appeared=PackageListLocators.message_modal_ok_btn_locator)
    package_list_page.wait_for_visibility_of_element(PackageListLocators.message_modal_locator)
    assert "You can't choose more then 1 package while edit" == package_list_page.get_element_text(
        PackageListLocators.message_modal_locator)
    generic_modules.step_info("[END - RTB-8310] Validate edit option warns")


def test_dashboard_package_multiple_delete(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    package_form_page = DashboardPackagesForm(driver)
    side_bar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-8312] Validate delete functionality")

    with open('assets/packages/package_data.json') as json_file:
        package_data = json.load(json_file)
    package_data['package_mandatory_data']['name'] = package_data['package_mandatory_data'][
                                                         'name'] + get_random_string()
    package_data['sites'] = PackageUtil.read_site_domain_names()

    # CREATE MULTIPLE PACKAGES
    side_bar_page.navigate_to_page(PageNames.PACKAGES)
    package_list_page.navigate_add_package()
    package_form_page.provide_package_mandatory_data(package_data)
    package_form_page.click_on_element(PackageFormLocators.save_button_locator_data_qa,
                                       locator_to_be_appeared=PackageListLocators.add_package_button_locator_data_qa)
    first_package_name = package_data['package_mandatory_data']['name']

    package_data['package_mandatory_data']['name'] = package_data['package_mandatory_data'][
                                                         'name'] + get_random_string()
    package_list_page.navigate_add_package()
    package_form_page.provide_package_mandatory_data(package_data)
    package_form_page.click_on_element(PackageFormLocators.save_button_locator_data_qa,
                                       locator_to_be_appeared=PackageListLocators.add_package_button_locator_data_qa)

    # DELETE MULTIPLE PACKAGES
    package_list_page.select_dropdown_value(PackageListLocators.rows_per_page_label, "100")
    package_list_page.click_on_element(PackageListLocators.package_checkbox_xpath.format(first_package_name),
                                       locator_initialization=True)
    package_list_page.click_on_element(PackageListLocators.package_checkbox_xpath.format(
        package_data['package_mandatory_data']['name']), locator_initialization=True)
    package_list_page.click_on_element(PackageListLocators.delete_link_locator,
                                       locator_to_be_appeared=PackageListLocators.alert_confirm_button_locator)
    package_list_page.click_on_element(PackageListLocators.alert_confirm_button_locator,
                                       locator_to_be_appeared=PackageListLocators.add_package_button_locator_data_qa)
    package_list_page.wait_for_spinner_load()
    assert "Successfully deleted 2 Packages" in package_list_page.get_success_message()
    package_list_page.set_value_into_element(PackageListLocators.search_box_locator, first_package_name)
    assert False is package_list_page.is_element_present(PackageListLocators.package_name_locator)
    package_list_page.set_value_into_element(PackageListLocators.search_box_locator,
                                             package_data['package_mandatory_data']['name'])
    assert False is package_list_page.is_element_present(PackageListLocators.package_name_locator)
    generic_modules.step_info("[END - RTB-8312] Validate delete functionality")


def test_dashboard_package_list_data_sorting(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    side_bar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-8311] Validate data and sorting in the packages table")
    side_bar_page.navigate_to_page(PageNames.PACKAGES)

    # LIST COLUMNS VALIDATION
    columns_locators = (PackageListLocators.package_column_locator, PackageListLocators.type_column_locator,
                        PackageListLocators.apps_sites_placements_column_locator,
                        PackageListLocators.impressions_column_locator,
                        PackageListLocators.auction_type_column_locator, PackageListLocators.date_column_locator)

    for locator in columns_locators:
        assert package_list_page.is_element_present(locator)

    # PACKAGE LIST SORTING BY PACKAGE NAME
    package_list_page.click_on_element(PackageListLocators.package_column_locator)
    packages_list = package_list_page.get_text_or_value_from_list(
        PackageListLocators.sorted_packages_list_locator)
    assert package_list_page.is_list_sorted(packages_list)
    package_list_page.click_on_element(PackageListLocators.package_column_locator)
    packages_list_descending = package_list_page.get_text_or_value_from_list(
        PackageListLocators.sorted_packages_list_locator)
    assert package_list_page.is_list_sorted(packages_list_descending, order='descending')

    # PACKAGE LIST SORTING BY TYPE
    package_list_page.click_on_element(PackageListLocators.type_column_locator)
    types_list = package_list_page.get_text_or_value_from_list(PackageListLocators.type_locator)
    assert package_list_page.is_list_sorted(types_list)
    package_list_page.click_on_element(PackageListLocators.type_column_locator)
    types_list_descending = package_list_page.get_text_or_value_from_list(PackageListLocators.type_locator)
    assert package_list_page.is_list_sorted(types_list_descending, order='descending')

    # PACKAGE LIST SORTING BY APPS/SITES/PLACEMENTS
    package_list_page.click_on_element(PackageListLocators.apps_sites_placements_column_locator)
    apps_sites_placements_list = package_list_page.get_text_or_value_from_list(
        PackageListLocators.apps_sites_placements_locator)
    assert package_list_page.is_list_sorted(apps_sites_placements_list, numbers=True)
    package_list_page.click_on_element(PackageListLocators.apps_sites_placements_column_locator)
    apps_sites_placements_list_descending = package_list_page.get_text_or_value_from_list(
        PackageListLocators.apps_sites_placements_locator)
    assert package_list_page.is_list_sorted(apps_sites_placements_list_descending, numbers=True, order='descending')

    # PACKAGE LIST SORTING BY IMPRESSIONS
    package_list_page.click_on_element(PackageListLocators.impressions_column_locator)
    impressions_list = package_list_page.get_text_or_value_from_list(
        PackageListLocators.impressions_locator)
    assert package_list_page.is_list_sorted(impressions_list, numbers=True)
    package_list_page.click_on_element(PackageListLocators.impressions_column_locator)
    impressions_list_descending = package_list_page.get_text_or_value_from_list(
        PackageListLocators.impressions_locator)
    assert package_list_page.is_list_sorted(impressions_list_descending, numbers=True, order='descending')

    # PACKAGE LIST SORTING BY AUCTION TYPE
    package_list_page.click_on_element(PackageListLocators.auction_type_column_locator)
    auction_type_list = package_list_page.get_text_or_value_from_list(
        PackageListLocators.auction_type_locator)
    assert package_list_page.is_list_sorted(auction_type_list)
    package_list_page.click_on_element(PackageListLocators.auction_type_column_locator)
    auction_type_list_descending = package_list_page.get_text_or_value_from_list(
        PackageListLocators.auction_type_locator)
    assert package_list_page.is_list_sorted(auction_type_list_descending, order='descending')

    # PACKAGE LIST SORTING BY DATE
    package_list_page.click_on_element(PackageListLocators.date_column_locator)
    date_list = package_list_page.get_text_or_value_from_list(
        PackageListLocators.date_locator)
    assert package_list_page.is_list_sorted(date_list, dates=True)
    package_list_page.click_on_element(PackageListLocators.date_column_locator)
    date_list_descending = package_list_page.get_text_or_value_from_list(
        PackageListLocators.date_locator)
    assert package_list_page.is_list_sorted(date_list_descending, dates=True, order='descending')

    generic_modules.step_info("[END - RTB-8311] Validate data and sorting in the packages table")
