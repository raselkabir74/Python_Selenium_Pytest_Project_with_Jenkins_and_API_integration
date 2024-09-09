import json
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from configurations import generic_modules
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_approve_form import \
    DspDashboardCampaignsMassApprove
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.navbar.navbar import DashboardNavbar
from utils.campaigns import CampaignUtils as CampaignUtil


def test_regression_campaign_mass_approve_deal_margin_disabled(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    campaign_list_page = DspDashboardCampaignsList(config, driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_mass_approve_page = DspDashboardCampaignsMassApprove(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_view = DspDashboardCampaignView(driver)
    navbar_page = DashboardNavbar(driver)

    # CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI
    with open(
            'assets/campaign/campaign_mass_approve_data.json') as json_file:
        campaign_mass_approve_data = json.load(json_file)
        private_deal_id = 12992
        deal_margin = 50

    # DATA PREPARATION FOR CAMPAIGN PRIVATE MARKETPLACE AND CREATIVE SET
    with open('assets/campaign/campaign_data.json') as json_file:
        provided_campaign_data = json.load(json_file)

    navbar_page.login_as("AutomationAgencyUser")

    # CREATE CAMPAIGN BY API
    campaign_name_list = CampaignUtil.process_campaign_name(
        campaign_list=config['campaign-mass-approve'])
    for campaign_name in campaign_name_list:
        CampaignUtil.create_campaign_by_api(config,
                                            mass_campaign_name=campaign_name)
        pulled_campaign_data_db = CampaignUtil.pull_campaign_id_from_db(
            campaign_name, db_connection)
        created_campaign_url = campaign_settings_page.navigate_to_created_campaign(
            pulled_campaign_data_db, config)
        campaign_page.go_to_url(created_campaign_url[0])

        # ADD PRIVATE MARKETPLACE AND CHANGE CREATIVE SET
        campaign_page.scroll_to_specific_element(
            CampaignFormLocators.private_marketplace_section_locator)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.private_marketplace_section_locator)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.private_marketplace_section_locator)
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.private_marketplace_section_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.private_marketplace_section_locator,
            locator_to_be_appeared=CampaignFormLocators.private_marketplace_selection_locator)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.private_marketplace_selection_locator)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.private_marketplace_selection_locator)
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.private_marketplace_selection_locator)
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.private_marketplace_selection_locator)
        campaign_page.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.private_marketplace_label_locator,
            option_to_select="Private auction - Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile ($3.98)")
        campaign_page.scroll_to_specific_element(
            CampaignFormLocators.creative_set_selection_locator)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.creative_set_selection_locator)
        campaign_page.wait_for_visibility_of_element(
            CampaignFormLocators.creative_set_selection_locator)
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.creative_set_selection_locator)
        campaign_page.select_from_modal_form_using_js_code(
            field_label_or_xpath_or_data_qa=CampaignFormLocators.selected_creative_sets_selection_label,
            option_to_select=provided_campaign_data['landing_and_creatives']['creative'])
        campaign_view.click_on_element(
            CampaignFormLocators.button_group_locator)
        campaign_view.wait_for_presence_of_element(
            CampaignFormLocators.publish_button_locator)
        campaign_view.wait_for_element_to_be_clickable(
            CampaignFormLocators.publish_button_locator)
        try:
            campaign_view.click_on_element(
                CampaignFormLocators.publish_button_locator)
            WebDriverWait(campaign_view.driver, 5).until(
                EC.alert_is_present(),
                'Timed out waiting for alert to appear')
            alert = campaign_view.driver.switch_to.alert
            alert.accept()
        except TimeoutException:
            print("Alert not present")
        campaign_settings_page.move_to_campaign_settings_page()
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    # CAMPAIGN MASS APPROVE
    campaign_mass_approve_data = CampaignUtil.process_campaign_approve_data(
        campaign_mass_approve_data)
    campaign_list_page.search_and_action(config['campaign-mass-approve'][
                                             'campaign-name-prefix-for-mass-approve'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(
            campaign_name=campaign_name,
            check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu(
        "Mass approve campaign", switch_to_new_window=True)
    campaign_mass_approve_page.provide_campaign_mass_approve_data_and_save(
        campaign_name_list,
        campaign_mass_approve_data,
        deal_margin_disabled=True)
    assert "Successfully approved campaigns." in campaign_list_page.get_success_message()
    # VERIFY DATA
    campaign_list_page.select_all_status()
    for campaign_name in campaign_name_list:
        campaign_list_page.search_and_action(campaign_name, "Approve")
        assert "Pending" not in campaign_approve_form.get_campaign_status()
        pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_data \
            (mass_approve=True, deal_margin=False)
        campaign_mass_approve_data['info'] = {}
        pulled_campaign_approve_data['main_settings'][
            'advertisement_category'] = 'IAB19 Technology & Computing'
        print("Pulled data :",
              generic_modules.ordered(pulled_campaign_approve_data))
        print("Given data :",
              generic_modules.ordered(campaign_mass_approve_data))
        assert pulled_campaign_approve_data == campaign_mass_approve_data
        campaign_list_page.reload_campaign_list_page()
    for campaign_name in campaign_name_list:
        pulled_deal_data_db = CampaignUtil.pull_deal_margin_value_from_db(
            campaign_name, db_connection)
        for deal_margin_data in pulled_deal_data_db:
            private_deal_id_from_db = \
                list(deal_margin_data.items())[0][1]
            assert private_deal_id_from_db == private_deal_id
            deal_margin_from_db = \
                list(deal_margin_data.items())[1][1]
            assert deal_margin_from_db == deal_margin
