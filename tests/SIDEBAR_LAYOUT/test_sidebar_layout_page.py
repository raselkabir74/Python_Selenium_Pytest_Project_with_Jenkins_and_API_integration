from locators.sidebar_layout_locators.sidebar_layout_locators import SidebarLayoutLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.sidebar_layout.sidebar_layout_page import DashboardSidebarLayout
from utils.page_names_enum import PageNames


def test_smoke_dashboard_sidebar_layout(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    sidebar_layout_page = DashboardSidebarLayout(driver)

    side_bar_page.navigate_to_page(PageNames.SIDEBAR_LAYOUTS)
    assert 'Title' in sidebar_layout_page.get_element_text(SidebarLayoutLocators.title_data_qa)
    sidebar_layout_page.click_on_element(SidebarLayoutLocators.new_layout_btn)
    assert "Title" in sidebar_layout_page.get_element_text(
        SidebarLayoutLocators.title_form_label_data_qa)
    sidebar_layout_page.click_on_element(SidebarLayoutLocators.cancel_btn)
    sidebar_layout_page.click_on_element(SidebarLayoutLocators.list_first_domain_3_dot_locator)
    sidebar_layout_page.click_on_element(SidebarLayoutLocators.list_first_domain_edit_locator)
    assert "Title" in sidebar_layout_page.get_element_text(
        SidebarLayoutLocators.title_form_label_data_qa)
