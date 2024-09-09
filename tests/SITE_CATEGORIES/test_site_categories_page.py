from locators.sites_categoires.site_cetagories_locators import SiteCategoriesLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.site_categories.site_categories_page import DashboardSiteCategories
from utils.page_names_enum import PageNames


def test_smoke_dashboard_sites_categories(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    site_categories_page = DashboardSiteCategories(driver)

    side_bar_page.navigate_to_page(PageNames.SITES_CATEGORIES)
    assert 'Title' in site_categories_page.get_element_text(SiteCategoriesLocators.title_label_data_qa)
    site_categories_page.click_on_element(SiteCategoriesLocators.new_app_sites_btn)
    assert "IAB categories" in site_categories_page.get_element_text(SiteCategoriesLocators.iab_categories_data_qa)
    site_categories_page.click_on_element(SiteCategoriesLocators.cancel_btn)
    site_categories_page.click_on_element(SiteCategoriesLocators.list_first_site_locator)
    assert "Selected IAB categories" in site_categories_page.get_element_text(
        SiteCategoriesLocators.selected_iab_categories_data_qa)

