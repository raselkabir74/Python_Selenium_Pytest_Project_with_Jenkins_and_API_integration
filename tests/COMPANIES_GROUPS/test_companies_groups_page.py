from locators.companies_groups.companies_groups_locators import CompaniesGroupsLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.companies_groups.companies_groups_page import DashboardCompaniesGroups
from utils.page_names_enum import PageNames


def test_smoke_dashboard_companies_groups(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    companies_groups_page = DashboardCompaniesGroups(driver)

    side_bar_page.navigate_to_page(PageNames.COMPANIES_GROUPS)
    assert 'Title' in companies_groups_page.get_element_text(CompaniesGroupsLocators.title_th_data_qa)
    companies_groups_page.click_on_element(CompaniesGroupsLocators.new_cg_btn_data_qa)
    assert "Companies group Title" in companies_groups_page.get_element_text(
        CompaniesGroupsLocators.companies_group_title_data_qa)
    companies_groups_page.click_on_element(CompaniesGroupsLocators.cancel_btn)
    companies_groups_page.click_on_element(CompaniesGroupsLocators.list_first_item)
    assert "Companies group Title" in companies_groups_page.get_element_text(
        CompaniesGroupsLocators.companies_group_title_data_qa)




