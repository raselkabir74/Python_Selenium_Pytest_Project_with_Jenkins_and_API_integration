from locators.branding.branding_locators import Branding
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.branding.branding_page import DashboardBranding
from utils.page_names_enum import PageNames


def test_smoke_dashboard_branding(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    branding_page = DashboardBranding(driver)

    side_bar_page.navigate_to_page(PageNames.BRANDING)
    assert 'Branding' in branding_page.get_element_text(Branding.branding_data_qa)
    branding_page.click_on_element(Branding.branding_btn_data_qa)
    assert 'Page title' in branding_page.get_element_text(Branding.page_title_data_qa)
    branding_page.click_on_element(Branding.cancel_btn)
    branding_page.click_on_element(Branding.list_first_item_3_dot_locator)
    branding_page.click_on_element(Branding.list_first_item_edit_locator)
    assert 'Name' in branding_page.get_element_text(Branding.name_data_qa)

