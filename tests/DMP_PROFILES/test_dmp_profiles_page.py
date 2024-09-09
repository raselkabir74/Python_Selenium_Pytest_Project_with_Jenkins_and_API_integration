from locators.dmp_profiles.dmp_profiles_locators import DMPprofiels
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.dmp_profiles.dmp_profiles_page import DashboardDMPprofiles
from utils.page_names_enum import PageNames


def test_smoke_dashboard_DMP_profiles(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    dmp_profiles_page = DashboardDMPprofiles(driver)

    side_bar_page.navigate_to_page(PageNames.DMP_PROFILES)
    assert 'Filter' in dmp_profiles_page.get_element_text(DMPprofiels.filter_data_qa)
    dmp_profiles_page.click_on_element(DMPprofiels.add_request_btn)
    assert 'Order title' in dmp_profiles_page.get_element_text(DMPprofiels.order_title_data_qa)
    dmp_profiles_page.click_on_element(DMPprofiels.cancel_btn)
    dmp_profiles_page.click_on_element(DMPprofiels.list_first_item_3_dot_data_qa)
    dmp_profiles_page.click_on_element(DMPprofiels.list_first_item_edit_locator)
    assert 'Order title' in dmp_profiles_page.get_element_text(DMPprofiels.order_title_data_qa)

