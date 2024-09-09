import json
import time

from configurations import generic_modules
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from locators.package.package_form_locator import PackageFormLocators
from locators.package.package_list_locator import PackageListLocators
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_list_locator import CampaignListLocators
from locators.all_campaigns.all_campaign_locators import AllCampaignFormLocators
from pages.budget.add_payment import DspDashboardAddPayment
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.package.packages_form import DashboardPackagesForm
from pages.package.packages_list import DashboardPackagesList
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.compare import CompareUtils as CompareUtil
from utils.packages import PackagesUtils as PackageUtil
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.redis import RedisUtils
from utils.page_names_enum import PageNames


def test_regression_add_and_edit_package(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    package_form_page = DashboardPackagesForm(driver)
    side_bar_page = DashboardSidebarPage(driver)

    with open('assets/packages/package_data.json') as json_file:
        package_data = json.load(json_file)
    package_data['package_mandatory_data']['name'] = package_data['package_mandatory_data'][
                                                         'name'] + generic_modules.get_random_string()
    package_data['sites'] = PackageUtil.read_site_domain_names()
    package_data['package_remaining_data'] = {}

    with open('assets/packages/edit_package_data.json') as json_file:
        edit_package_data = json.load(json_file)
    edit_package_data['package_mandatory_data']['name'] = edit_package_data['package_mandatory_data'][
                                                              'name'] + generic_modules.get_random_string()
    edit_package_data['sites'] = PackageUtil.read_site_domain_names(
        operation='edit')
    edit_package_data['package_remaining_data'] = {}

    generic_modules.step_info("[START - RTB-8313] Validate package creation")

    # ADD PACKAGE
    side_bar_page.navigate_to_page(PageNames.PACKAGES)
    package_list_page.navigate_add_package()
    package_form_page.provide_package_mandatory_data(package_data)
    package_form_page.click_on_element(PackageFormLocators.save_button_locator_data_qa)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully! Package size will be calculated shortly." in success_message

    # VERIFY ADD PACKAGE DATA
    package_list_page.edit_package(package_data['package_mandatory_data']['name'])
    pulled_gui_data = package_form_page.get_package_mandatory_data()
    package_form_page.click_on_element(
        PackageFormLocators.cancel_button_locator_data_qa)
    print("pulled_campaign_data_gui",
          generic_modules.ordered(pulled_gui_data))
    print("campaign_data           ",
          generic_modules.ordered(package_data))
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_gui_data, package_data)

    generic_modules.step_info("[END - RTB-8313] Validate package creation")

    generic_modules.step_info("[START - RTB-8315] Validate package edit")

    # EDIT PACKAGE DATA
    package_list_page.edit_package(package_data['package_mandatory_data']['name'])
    package_form_page.provide_package_mandatory_data(edit_package_data)
    package_form_page.click_on_element(PackageFormLocators.save_button_locator_data_qa)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully!" in success_message

    # VERIFY EDIT PACKAGE DATE WITH TABLE DATA
    package_list_page.set_value_into_element(PackageListLocators.search_box_locator,
                                             edit_package_data['package_mandatory_data']['name'])
    assert edit_package_data['package_mandatory_data']['name'] == package_list_page.get_element_text(
        PackageListLocators.package_name_locator)
    assert "Apps/sites" == package_list_page.get_element_text(PackageListLocators.type_locator)
    assert edit_package_data['package_mandatory_data']['auction_type'] == package_list_page.get_element_text(
        PackageListLocators.auction_type_locator)
    current_date = package_list_page.get_current_date_with_specific_format(
        "%d %b, %Y")
    assert current_date == package_list_page.get_element_text(PackageListLocators.date_locator)

    # VERIFY EDIT PACKAGE DATA
    package_list_page.edit_package(edit_package_data['package_mandatory_data']['name'])
    pulled_gui_data = package_form_page.get_package_mandatory_data(operation='edit')
    package_form_page.click_on_element(
        PackageFormLocators.cancel_button_locator_data_qa)
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_gui_data, edit_package_data)

    generic_modules.step_info("[END - RTB-8315] Validate package edit")

    # PACKAGE CLEAN UP
    package_list_page.delete_package(edit_package_data['package_mandatory_data']['name'])
    success_message = package_list_page.get_success_message()
    assert "Successfully deleted 1 Packages" in success_message


def test_regression_add_and_edit_package_two(login_by_user_type, open_database_connection):
    config, driver, redis_connection = login_by_user_type
    db_connection = open_database_connection
    package_list_page = DashboardPackagesList(driver)
    package_form_page = DashboardPackagesForm(driver)
    side_bar_page = DashboardSidebarPage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    payment_page = DspDashboardAddPayment(config, driver)
    redis_page = RedisUtils(config, driver)

    with open('assets/packages/package_data.json') as json_file:
        package_data = json.load(json_file)
    package_data['package_mandatory_data']['name'] = package_data['package_mandatory_data'][
                                                         'name'] + generic_modules.get_random_string()
    package_data['sites'] = PackageUtil.read_site_domain_names()

    with open('assets/packages/edit_package_data.json') as json_file:
        edit_package_data = json.load(json_file)
    edit_package_data['package_mandatory_data']['name'] = edit_package_data['package_mandatory_data'][
                                                              'name'] + generic_modules.get_random_string()
    edit_package_data['sites'] = PackageUtil.read_site_domain_names(
        operation='edit')

    with open('assets/campaign/redis_data/redis_data_for_campaign_with_package_creation.json') as json_file:
        redis_data_for_campaign_with_package_creation = json.load(json_file)
    with open('assets/campaign/redis_data/redis_data_for_campaign_with_edited_package.json') as json_file:
        redis_data_for_campaign_with_edited_package = json.load(json_file)

    campaign_id = None
    campaign_data = None
    package_id = None

    generic_modules.step_info("[START - RTB-8313] Validate package creation")

    # ADD PACKAGE
    side_bar_page.navigate_to_page(PageNames.PACKAGES)
    package_list_page.navigate_add_package()
    package_form_page.provide_package_data_and_save(package_data)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully! Package size will be calculated shortly." in success_message

    # VERIFY ADD PACKAGE DATA
    package_list_page.edit_package(package_data['package_mandatory_data']['name'])
    pulled_gui_data = package_form_page.get_package_data()
    pulled_gui_data['package_remaining_data']['tags'] = "Top sites"
    print("pulled_campaign_data_gui",
          generic_modules.ordered(pulled_gui_data))
    print("campaign_data           ",
          generic_modules.ordered(package_data))
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_gui_data, package_data)

    generic_modules.step_info("[END - RTB-8313] Validate package creation")

    generic_modules.step_info(
        "[START - RTB-8374] Expand test_regression_add_and_edit_package test to include data verification in redis")

    # CREATE CAMPAIGN BY API AND APPROVE
    if "qa-testing" in config['credential']['url']:
        campaign_data = CampaignUtil.create_campaign_by_api_with_current_date(config)
        payment_page.add_budget_into_specific_client(config['credential']['username'], 10)
        campaign_id = CampaignUtil.pull_campaign_id_from_db(campaign_data['name'], db_connection)
        package_id = PackageUtil.pull_package_id_from_db(package_data['package_mandatory_data']['name'], db_connection)
        campaign_edit_url = config['credential']['url'] + config['campaign-edit-page']['campaign-edit-url'].format(
            str(campaign_id[0]['id']))
        driver.get(campaign_edit_url)
        campaign_page.click_on_element(CampaignFormLocators.packages_section_locator,
                                       locator_to_be_appeared=CampaignFormLocators.packages_uncheck_all_button_locator)
        campaign_page.click_on_element(CampaignFormLocators.packages_uncheck_all_button_locator)
        campaign_page.click_on_element(CampaignFormLocators.package_checkbox_locator.format(
            package_data['package_mandatory_data']['name']), locator_initialization=True)
        campaign_page.click_on_element(CampaignFormLocators.packages_include_only_locator.format(package_id[0]['id']),
                                       locator_initialization=True)
        campaign_page.scroll_to_specific_element(
            CampaignFormLocators.publish_button_locator)
        time.sleep(campaign_page.ONE_SEC_DELAY)
        campaign_page.wait_for_presence_of_element(
            CampaignFormLocators.publish_button_locator)
        campaign_page.wait_for_element_to_be_clickable(
            CampaignFormLocators.publish_button_locator)
        campaign_page.click_on_element(
            CampaignFormLocators.publish_button_locator, locator_to_be_appeared=CampaignListLocators.btn_create_locator)
        campaign_approve_url = config['credential']['url'] + config['campaign-approve-page'][
            'campaign-approve-url'].format(str(campaign_id[0]['id']))
        driver.get(campaign_approve_url)
        campaign_approve_form.click_on_element(CampaignApproveLocators.ad_exchange_check_all_locator)
        campaign_approve_form.click_approve_button()
        campaign_approve_form.click_on_element(
            CampaignApproveLocators.creative_size_pop_up_ignore_locator,
            locator_to_be_appeared=AllCampaignFormLocators.search_filter_locator)

        redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == redis_data['id']
        assert campaign_data['name'] == redis_data['name']
        assert package_id[0]['id'] == redis_data['targeting']['domains']['packages'][0]['packageId']
        redis_data['id'] = ""
        redis_data['name'] = ""
        redis_data['targeting']['domains']['packages'][0]['packageId'] = ""
        redis_data['contentCategories'] = []
        redis_data['user']['targetDmpIds'] = []
        redis_data['targeting']['endEpochSecond'] = ""
        redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_campaign_with_package_creation == redis_data

    generic_modules.step_info("[START - RTB-8315] Validate package edit")

    # EDIT PACKAGE DATA
    package_list_url = config['credential']['url'] + config['package-list-page']['package-list-url']
    driver.get(package_list_url)
    package_list_page.edit_package(package_data['package_mandatory_data']['name'])
    package_form_page.provide_package_data_and_save(edit_package_data)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully!" in success_message

    # VERIFY EDIT PACKAGE DATE WITH TABLE DATA
    package_list_page.set_value_into_element(PackageListLocators.search_box_locator,
                                             edit_package_data['package_mandatory_data']['name'])
    assert edit_package_data['package_mandatory_data']['name'] == package_list_page.get_element_text(
        PackageListLocators.package_name_locator)
    assert "Apps/sites" == package_list_page.get_element_text(PackageListLocators.type_locator)
    assert edit_package_data['package_mandatory_data']['auction_type'] == package_list_page.get_element_text(
        PackageListLocators.auction_type_locator)
    current_date = package_list_page.get_current_date_with_specific_format(
        "%d %b, %Y")
    assert current_date == package_list_page.get_element_text(PackageListLocators.date_locator)

    # VERIFY EDIT PACKAGE DATA
    package_list_page.edit_package(edit_package_data['package_mandatory_data']['name'])
    pulled_gui_data = package_form_page.get_package_data(operation='edit')
    pulled_gui_data['package_remaining_data']['tags'] = "Top sites"
    print("pulled_campaign_data_gui",
          generic_modules.ordered(pulled_gui_data))
    print("campaign_data           ",
          generic_modules.ordered(edit_package_data))
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_gui_data, edit_package_data)

    if "qa-testing" in config['credential']['url']:
        new_redis_data = redis_page.establish_connection_and_get_campaign_rule(redis_connection, campaign_id[0]['id'])
        assert campaign_id[0]['id'] == new_redis_data['id']
        assert campaign_data['name'] == new_redis_data['name']
        assert package_id[0]['id'] == new_redis_data['targeting']['domains']['packages'][0]['packageId']
        new_redis_data['id'] = ""
        new_redis_data['name'] = ""
        new_redis_data['targeting']['domains']['packages'][0]['packageId'] = ""
        new_redis_data['contentCategories'] = []
        new_redis_data['user']['targetDmpIds'] = []
        new_redis_data['targeting']['endEpochSecond'] = ""
        new_redis_data['targeting']['startEpochSecond'] = ""

        assert redis_data_for_campaign_with_edited_package == new_redis_data

    generic_modules.step_info("[END - RTB-8315] Validate package edit")
    generic_modules.step_info(
        "[END - RTB-8374] Expand test_regression_add_and_edit_package test to include data verification in redis")
