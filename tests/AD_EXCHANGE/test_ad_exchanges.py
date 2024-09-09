from locators.ad_exchanges.ad_exchanges_locators import AdExchanges
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.ad_exchanges.ad_exchanges_page import DashboardAdExchanges
from utils.page_names_enum import PageNames


def test_smoke_dashboard_ad_exchanges(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    ad_exchanges_page = DashboardAdExchanges(driver)

    side_bar_page.navigate_to_page(PageNames.AD_EXCHANGES)
    assert 'Filter' in ad_exchanges_page.get_element_text(AdExchanges.filter_data_qa)
    ad_exchanges_page.click_on_element(AdExchanges.ad_exchange_btn)
    assert 'Exchange name' in ad_exchanges_page.get_element_text(AdExchanges.exchange_name_data_qa)
    ad_exchanges_page.click_on_element(AdExchanges.cancel_btn)
    ad_exchanges_page.click_on_element(AdExchanges.list_first_ad_locator)
    assert "Exchange type" in ad_exchanges_page.get_element_text(AdExchanges.exchange_type_data_qa)


