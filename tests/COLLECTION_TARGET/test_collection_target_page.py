from locators.collection_target.collection_target_locators import CollectionTargetLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.collection_target.collection_target_page import DashboardCollectionTarget
from utils.page_names_enum import PageNames


def test_smoke_dashboard_collection_targets(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    collection_target_page = DashboardCollectionTarget(driver)

    side_bar_page.navigate_to_page(PageNames.COLLECTION_TARGET)
    assert 'Period' in collection_target_page.get_element_text(CollectionTargetLocators.period_data_qa)
    collection_target_page.click_on_element(CollectionTargetLocators.add_btn_data_qa)
    assert "Target details" in collection_target_page.get_element_text(
        CollectionTargetLocators.target_details_data_qa)

