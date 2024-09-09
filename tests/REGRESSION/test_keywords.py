import json
from configurations import generic_modules
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.brand_safety.brand_safety_list_form import DashboardKeywordListForm
from pages.brand_safety.brand_safety_form import DashboardBrandSafetyForm
from pages.brand_safety.brand_safety_keywords_list import \
    DashboardBrandSafetyKeywordsList
from utils.compare import CompareUtils as CompareUtil
from utils.keywords import KeywordsUtils as KeywordsUtil
from utils.page_names_enum import PageNames


def test_regression_add_edit_keywords(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    keyword_list_page = DashboardKeywordListForm(driver)
    keyword_form_page = DashboardBrandSafetyForm(driver)
    brand_safety_keyword_list_page = DashboardBrandSafetyKeywordsList(
        driver)
    with open('assets/brand_safety/keyword_data.json') as json_file:
        keywords_data = json.load(json_file)
    keywords_data['title'] = keywords_data['title'] + generic_modules.get_random_string()
    keywords_data = KeywordsUtil.process_keywords_data(keywords_data)
    # ADD BRAND SAFETY
    sidebar_navigation.navigate_to_page(PageNames.KEYWORDS)
    keyword_list_page.navigate_to_add_keywords_page()
    keyword_form_page.provide_and_save_keyword_data(keywords_data)
    # VERIFY ADD BRAND SAFETY DATA
    keyword_list_page.search(keywords_data['title'])
    keyword_list_page.navigate_to_edit_keywords(keywords_data['title'])
    pulled_keyword_information = keyword_form_page.get_keywords_information()
    print("pulled data", pulled_keyword_information)
    print("provided data", keywords_data)
    assert pulled_keyword_information == keywords_data
    # EDIT BRAND SAFETY
    with open('assets/brand_safety/keywords_edit_data.json') as json_file:
        edit_keywords_data = json.load(json_file)
    edit_keywords_data['title'] = edit_keywords_data[
                                      'title'] + generic_modules.get_random_string()
    edit_keywords_data = KeywordsUtil.process_keywords_data(
        edit_keywords_data)
    keyword_form_page.provide_and_save_keyword_data(edit_keywords_data)
    keyword_list_page.search(edit_keywords_data['title'])
    keyword_list_page.navigate_to_edit_keywords(
        edit_keywords_data['title'])
    pulled_brand_edit_safety_information = keyword_form_page.get_keywords_information()
    print("pulled data", pulled_brand_edit_safety_information)
    print("provided data", edit_keywords_data)
    assert pulled_brand_edit_safety_information == edit_keywords_data
    keyword_form_page.cancel_form()
    keyword_list_page.search(edit_keywords_data['title'])
    keyword_list_page.navigate_to_keyword_count_page(
        edit_keywords_data['title'])
    # KEYWORDS VERIFICATION, ADD and EDIT
    pulled_keywords_list = brand_safety_keyword_list_page.get_keywords_list()
    provided_keywords_list = KeywordsUtil.get_provided_keyword_list()
    assert "All data verification is successful" == CompareUtil.verify_data(
        pulled_keywords_list,
        provided_keywords_list)
    new_keyword = "Keyword_Add" + generic_modules.get_random_string()
    brand_safety_keyword_list_page.add_keyword(new_keyword)
    success_message = brand_safety_keyword_list_page.get_success_message()
    assert "Successfully added new keywords." in success_message
    brand_safety_keyword_list_page.delete_keyword(new_keyword)
    success_message = brand_safety_keyword_list_page.get_success_message()
    assert "Successfully deleted keywords" in success_message
    brand_safety_keyword_list_page.navigate_back_to_brand_safety_list()
    # DELETE BRAND SAFETY
    keyword_list_page.search(edit_keywords_data['title'])
    keyword_list_page.delete_keywords(edit_keywords_data['title'])
    assert "Successfully deleted keywords" in keyword_list_page.get_success_message()
