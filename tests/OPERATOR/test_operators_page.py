from locators.operators.operators_locator import Operators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.operators.operator_page import DashboardOperator
from utils.page_names_enum import PageNames


def test_smoke_dashboard_operators(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    operators_page = DashboardOperator(driver)

    side_bar_page.navigate_to_page(PageNames.OPERATORS)
    assert 'Filter' in operators_page.get_element_text(Operators.filter_data_qa)
    operators_page.click_on_element(Operators.add_operator_btn)
    assert 'Title' in operators_page.get_element_text(Operators.title_data_qa)
    operators_page.click_on_element(Operators.cancel_btn)
    operators_page.click_on_element(Operators.list_first_item_3_dot_locator)
    operators_page.click_on_element(Operators.list_first_item_edit_locator)
    assert 'Full title' in operators_page.get_element_text(Operators.full_title_data_qa)
