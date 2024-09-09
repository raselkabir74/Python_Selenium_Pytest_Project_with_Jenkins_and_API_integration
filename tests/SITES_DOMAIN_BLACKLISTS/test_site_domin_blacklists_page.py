from locators.site_domain_blacklists.sites_domain_blacklists_locators import SiteDomainBlacklistsLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.sites_domain_blacklists.site_domain_blacklists_page import DashboardSiteDomainBlacklists
from utils.page_names_enum import PageNames


def test_smoke_dashboard_sites_domain_blacklists(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    sites_domain_blacklists_page = DashboardSiteDomainBlacklists(driver)

    side_bar_page.navigate_to_page(PageNames.SITES_DOMAIN_BLACKLIST)
    assert 'Domain' in sites_domain_blacklists_page.get_element_text(SiteDomainBlacklistsLocators.title_label_data_qa)
    sites_domain_blacklists_page.click_on_element(SiteDomainBlacklistsLocators.new_domain_btn)
    assert "Domain" in sites_domain_blacklists_page.get_element_text(
        SiteDomainBlacklistsLocators.domain_data_qa)
    sites_domain_blacklists_page.click_on_element(SiteDomainBlacklistsLocators.cancel_btn)
    sites_domain_blacklists_page.click_on_element(SiteDomainBlacklistsLocators.list_first_domain_3_dot_locator)
    sites_domain_blacklists_page.click_on_element(SiteDomainBlacklistsLocators.list_first_domain_edit_locator)
    assert "Domain" in sites_domain_blacklists_page.get_element_text(
        SiteDomainBlacklistsLocators.domain_data_qa)

