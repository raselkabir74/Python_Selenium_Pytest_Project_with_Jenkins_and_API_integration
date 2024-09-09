from locators.blacklist.blacklist_locators import Blacklist
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.blacklist.blacklist_page import DashboardBlacklist
from utils.page_names_enum import PageNames


def test_smoke_dashboard_blacklist(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    blacklist_page = DashboardBlacklist(driver)

    side_bar_page.navigate_to_page(PageNames.BLACKLISTS)
    assert 'Blacklist' in blacklist_page.get_element_text(Blacklist.blacklist_column_data_qa)
    blacklist_page.click_on_element(Blacklist.blacklist_btn)
    assert 'List name' in blacklist_page.get_element_text(Blacklist.list_name_data_qa)
    blacklist_page.click_on_element(Blacklist.cancel_btn)
    blacklist_page.click_on_element(Blacklist.list_first_item_3_dot_locator)
    blacklist_page.click_on_element(Blacklist.list_first_item_edit_locator)
    assert 'Type' in blacklist_page.get_element_text(Blacklist.type_data_qa)

