from locators.predictive.predictive_locators import PredictiveLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.predictive.predictive_page import DashboardPredictive
from utils.page_names_enum import PageNames


def test_smoke_dashboard_predictive(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    predictive_page = DashboardPredictive(driver)

    side_bar_page.navigate_to_page(PageNames.PREDICTIVE)
    assert 'Predictive campaigns' in predictive_page.get_element_text(PredictiveLocators.title_label_data_qa)
