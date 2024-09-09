from locators.campaign.campaign_view_locator import CampaignViewLocator
from pages.base_page import BasePage


class DspDashboardCampaignView(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def get_success_message(self):
        return self.get_element_text(
            CampaignViewLocator.success_message_locator)

    def perform_action(self, action):
        if action.lower() == 'edit':
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_edit_icon)
            self.wait_for_visibility_of_element(
                CampaignViewLocator.campaign_view_edit_icon)
            self.wait_for_element_to_be_clickable(
                CampaignViewLocator.campaign_view_edit_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_edit_icon)
        elif action.lower() == 'delete':
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_delete_icon)
            self.wait_for_element_to_be_clickable(
                CampaignViewLocator.campaign_view_delete_icon)
            self.wait_for_visibility_of_element(
                CampaignViewLocator.campaign_view_delete_icon)
            self.wait_for_element_to_be_clickable(
                CampaignViewLocator.campaign_view_delete_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_delete_icon)
            self.click_on_element(
                CampaignViewLocator.confirm_button_alert_locator)
        elif action.lower() == 'duplicate':
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_duplicate_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_duplicate_icon)
        elif action.lower() == 'approve':
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_three_dot_icon)
            self.wait_for_presence_of_element(
                CampaignViewLocator.campaign_view_approve_icon)
            self.click_on_element(
                CampaignViewLocator.campaign_view_approve_icon)
