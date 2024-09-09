from locators.payment_settings.payment_settings_locator import PaymentSettingLocators
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.payment_settings.payment_settings_page import DashboardPaymentSettings
from utils.page_names_enum import PageNames


def test_smoke_dashboard_payment_settings(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    side_bar_page = DashboardSidebarPage(driver)
    payment_settings_page = DashboardPaymentSettings(driver)

    side_bar_page.navigate_to_page(PageNames.PAYMENT_SETTINGS)
    assert 'Title' in payment_settings_page.get_element_text(PaymentSettingLocators.settings_title_data_qa)
    payment_settings_page.click_on_element(PaymentSettingLocators.country_setting_btn)
    assert "Title" in payment_settings_page.get_element_text(
        PaymentSettingLocators.country_setting_form_title_data_qa)
    payment_settings_page.click_on_element(PaymentSettingLocators.cancel_btn)
    payment_settings_page.click_on_element(PaymentSettingLocators.list_first_settings_item_locator)
    assert "Country" in payment_settings_page.get_element_text(
        PaymentSettingLocators.country_setting_form_county_data_qa)
    payment_settings_page.click_on_element(PaymentSettingLocators.cancel_btn)
    payment_settings_page.click_on_element(PaymentSettingLocators.user_settings_option_locator)
    assert "ID" in payment_settings_page.get_element_text(PaymentSettingLocators.user_settings_id_locator)
    payment_settings_page.click_on_element(PaymentSettingLocators.user_setting_btn)
    assert "Payment option list" in payment_settings_page.get_element_text(PaymentSettingLocators.payment_option_label_data_qa)
    payment_settings_page.click_on_element(PaymentSettingLocators.cancel_btn)
    payment_settings_page.click_on_element(PaymentSettingLocators.options_locator)
    assert "Title" in payment_settings_page.get_element_text(PaymentSettingLocators.option_title_data_qa)
    payment_settings_page.click_on_element(PaymentSettingLocators.payment_option_btn)
    assert "Title" in payment_settings_page.get_element_text(PaymentSettingLocators.payment_option_title_data_qa)
    payment_settings_page.click_on_element(PaymentSettingLocators.cancel_btn)
    payment_settings_page.click_on_element(PaymentSettingLocators.payment_option_list_first_title_locator)
    assert "Display title" in payment_settings_page.get_element_text(PaymentSettingLocators.payment_option_display_title_data_qa)




