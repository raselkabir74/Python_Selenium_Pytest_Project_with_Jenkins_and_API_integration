from locators.sites_subdomain_map.sites_subdomain_map_locators import SiteSubdomainMapLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.sites_subdomain_map.sites_subdomain_map_page import DashboardSiteSubdomainMap
from utils.page_names_enum import PageNames


def test_smoke_dashboard_sites_subdomain_map(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    sites_subdomain_map_page = DashboardSiteSubdomainMap(driver)

    side_bar_page.navigate_to_page(PageNames.SITES_SUBDOMAIN_MAP)
    assert 'Subdomain' in sites_subdomain_map_page.get_element_text(SiteSubdomainMapLocators.subdomain_label_data_qa)
    sites_subdomain_map_page.click_on_element(SiteSubdomainMapLocators.new_site_subdomain_btn)
    assert "Subdomain" in sites_subdomain_map_page.get_element_text(
        SiteSubdomainMapLocators.subdomain_form_label_data_qa)
    sites_subdomain_map_page.click_on_element(SiteSubdomainMapLocators.cancel_btn)
    sites_subdomain_map_page.click_on_element(SiteSubdomainMapLocators.list_first_domain_3_dot_locator)
    sites_subdomain_map_page.click_on_element(SiteSubdomainMapLocators.list_first_domain_edit_locator)
    assert "Subdomain" in sites_subdomain_map_page.get_element_text(
        SiteSubdomainMapLocators.subdomain_form_label_data_qa)
