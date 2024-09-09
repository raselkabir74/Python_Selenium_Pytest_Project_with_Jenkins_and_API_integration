from locators.private_marketplace.private_marketplace_locators import PrivateMarketplaceLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.private_marketplace.private_marketplace_page import DashboardPrivateMarketplace
from utils.page_names_enum import PageNames


def test_smoke_dashboard_private_marketplace(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    private_marketplace_page = DashboardPrivateMarketplace(driver)

    side_bar_page.navigate_to_page(PageNames.PRIVATE_MARKETPLACE)
    assert 'Title' in private_marketplace_page.get_element_text(PrivateMarketplaceLocators.title_label_data_qa)
    private_marketplace_page.click_on_element(PrivateMarketplaceLocators.new_pmp_btn)
    assert "Bid price (CPM) info" in private_marketplace_page.get_element_text(
        PrivateMarketplaceLocators.bid_cpm_label_data_qa)
    private_marketplace_page.click_on_element(PrivateMarketplaceLocators.cancel_btn)
    private_marketplace_page.click_on_element(PrivateMarketplaceLocators.list_first_pmp_locator)
    assert "Bid price (CPM) info" in private_marketplace_page.get_element_text(
        PrivateMarketplaceLocators.bid_cpm_label_data_qa)

