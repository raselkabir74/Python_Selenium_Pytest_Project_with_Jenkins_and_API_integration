from locators.billing.billing_locators import Billing
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.billing.billing_page import DashboardBilling
from utils.page_names_enum import PageNames


def test_smoke_dashboard_billing(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    billing_page = DashboardBilling(driver)

    side_bar_page.navigate_to_page(PageNames.SETTINGS_BILLING)
    assert 'Total amount due' in billing_page.get_element_text(Billing.total_amount_due_title_data_qa)

