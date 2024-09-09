from locators.profile_info.profile_info_locators import ProfileInfo
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.profile_page.profile_page import DashboardProfileInfo
from utils.page_names_enum import PageNames


def test_smoke_dashboard_profile_info(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    profile_info_page = DashboardProfileInfo(driver)

    side_bar_page.navigate_to_page(PageNames.PROFILE_INFO)
    assert 'Company title' in profile_info_page.get_element_text(ProfileInfo.company_title_data_qa)

