from locators.campaign_emails.campaign_emails_locators import CampaignsEmails
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.campaign_emails.campaign_emails_page import DashboardCampaignsEmails
from utils.page_names_enum import PageNames


def test_smoke_dashboard_campaigns_emails(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    campaigns_emails_page = DashboardCampaignsEmails(driver)

    side_bar_page.navigate_to_page(PageNames.CAMPAIGNS_EMAILS)
    assert 'Campaign/IO ID' in campaigns_emails_page.get_element_text(CampaignsEmails.campaign_io_data_qa)

