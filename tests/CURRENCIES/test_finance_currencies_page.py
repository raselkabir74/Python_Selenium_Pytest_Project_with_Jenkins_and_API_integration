from configurations import generic_modules
from locators.currencies.currencies_locator import CurrenciesLocators
from pages.currencies.currencies import DspDashboardCurrencies
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.page_names_enum import PageNames


def test_finance_currencies_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    currencies_page = DspDashboardCurrencies(driver)
    side_bar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-8378] Validate filters and Clear all btn functionality")

    # FILTERS VALIDATION
    side_bar_page.navigate_to_page(PageNames.CURRENCIES)
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    rows_info = currencies_page.get_element_text(CurrenciesLocators.rows_info_locator)
    assert currencies_page.is_element_present(CurrenciesLocators.currency_filter_data_qa)
    assert currencies_page.is_element_present(CurrenciesLocators.auto_update_rate_filter_data_qa)

    currencies_page.select_dropdown_value(CurrenciesLocators.currency_filter_data_qa, "Euro Member Countries (EUR)")
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    assert "Euro Member Countries (EUR)" == currencies_page.get_element_text(
        CurrenciesLocators.currency_name_locator)
    currencies_page.click_on_element(CurrenciesLocators.clear_all_btn_data_qa)
    currencies_page.select_dropdown_value(CurrenciesLocators.auto_update_rate_filter_data_qa, "Yes")
    assert "Yes" == currencies_page.get_text_or_value_from_list(CurrenciesLocators.auto_update_rate_list_locator,
                                                                selected_option="Yes")
    # CLEAR ALL BUTTON VALIDATION
    currencies_page.click_on_element(CurrenciesLocators.clear_all_btn_data_qa)
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    assert "0" == currencies_page.get_attribute_value(CurrenciesLocators.filter_count_data_qa,
                                                      attribute_name="data-count")
    assert "Select currency" == currencies_page.get_selected_options_using_js_code(
        CurrenciesLocators.currency_filter_data_qa)
    assert "Select auto update rate" == currencies_page.get_selected_options_using_js_code(
        CurrenciesLocators.auto_update_rate_filter_data_qa)
    assert rows_info == currencies_page.get_element_text(CurrenciesLocators.rows_info_locator)

    generic_modules.step_info("[END - RTB-8378] Validate filters and Clear all btn functionality")


def test_finance_currencies_page_two(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    currencies_page = DspDashboardCurrencies(driver)
    side_bar_page = DashboardSidebarPage(driver)

    generic_modules.step_info("[START - RTB-8649] Validate Adjust and Cancel functionality and Currency rate and the "
                              "Final rate fields")

    side_bar_page.navigate_to_page(PageNames.CURRENCIES)
    # Validate Adjust option from the three dot icon
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    currencies_page.select_dropdown_value(CurrenciesLocators.currency_filter_select_data_qa,
                                          'Yemen Rial (YER)', select_by_value=False)
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    updated_by = currencies_page.get_element_text(CurrenciesLocators.Yemen_Rial_updated_by)
    updated_at = currencies_page.get_element_text(CurrenciesLocators.Yemen_Rial_updated_at)
    auto_update_status = currencies_page.get_element_text(CurrenciesLocators.auto_update_rate_list_locator)
    currencies_page.click_on_element(CurrenciesLocators.Yemen_Rial_three_dot_data_qa)
    currencies_page.click_on_element(CurrenciesLocators.Yemen_Rial_three_dot_adjust_data_qa)
    assert "Yemen Rial (﷼)" in currencies_page.get_element_text(CurrenciesLocators.currency_name_data_qa)
    # Validate whether the Currency rate and the Final rate fields are readonly
    readonly_value_for_final_rate_data_qa = currencies_page.find_element(
        CurrenciesLocators.final_rate_data_qa).get_attribute("readonly")
    readonly_value_for_currency_rate_data_qa = currencies_page.find_element(
        CurrenciesLocators.currency_rate_data_qa).get_attribute("readonly")
    readonly_value_for_markup_amount_data_qa = currencies_page.find_element(
        CurrenciesLocators.markup_amount_data_qa).get_attribute("readonly")
    assert readonly_value_for_currency_rate_data_qa == "true", "The Currency rate element is not readonly"
    if auto_update_status == "Yes":
        assert readonly_value_for_final_rate_data_qa == "true", "The Final rate element is not readonly"
    else:
        assert readonly_value_for_markup_amount_data_qa == "true", "The Markup amount element is not readonly"

    generic_modules.step_info("[START - RTB-8650] Verify correct data displayed and currency rate edit functionality")
    created_by_info = currencies_page.get_element_text(CurrenciesLocators.created_by_info_data_qa)
    created_by = created_by_info.split(":")
    assert "N/A" == created_by[1].strip()
    last_updated_by_info = currencies_page.get_element_text(CurrenciesLocators.last_updated_by_info_data_qa)
    last_updated_by = last_updated_by_info.split(":")
    assert updated_by == last_updated_by[1].strip()
    created_info = currencies_page.get_element_text(CurrenciesLocators.created_info_data_qa)
    created = created_info.split(" ")
    assert "2022-09-29" == created[1].strip()
    assert "(GMT+3)" == created[3].strip()
    last_updated_info = currencies_page.get_element_text(CurrenciesLocators.last_updated_info_data_qa)
    last_updated = last_updated_info.split(" ")
    assert updated_at == last_updated[2].strip() + " " + last_updated[3].strip()
    assert "(GMT+3)" == last_updated[4].strip()
    generic_modules.step_info("[END - RTB-8650] Verify correct data displayed and currency rate edit functionality")

    # Validate whether the Cancel button is working properly
    currencies_page.click_on_element(CurrenciesLocators.cancel_btn_data_qa)
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    assert currencies_page.is_visible(CurrenciesLocators.clear_all_btn_data_qa)

    generic_modules.step_info("[END - RTB-8649] Validate Adjust and Cancel functionality and Currency rate and the "
                              "Final rate fields")


def test_finance_currencies_page_three(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    currencies_page = DspDashboardCurrencies(driver)
    side_bar_page = DashboardSidebarPage(driver)
    currencies_list_page_url = (config['credential']['url']
                    + config['currencies-page']['currencies-list-page-url'])

    generic_modules.step_info("[START - RTB-8650] Verify correct data displayed and currency rate edit functionality")

    side_bar_page.navigate_to_page(PageNames.CURRENCIES)
    currencies_page.select_dropdown_value(CurrenciesLocators.auto_update_rate_filter_data_qa, "Yes")
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    currency_name = currencies_page.get_element_text(CurrenciesLocators.currency_name_locator)
    currencies_page.click_on_adjust()

    # FINAL RATE VERIFICATION
    currency_rate = float(currencies_page.get_attribute_value(CurrenciesLocators.currency_rate_data_qa, "value"))
    markup_amount = float(currencies_page.get_attribute_value(CurrenciesLocators.markup_amount_data_qa, "value"))
    final_rate = float(currencies_page.get_attribute_value(CurrenciesLocators.final_rate_data_qa, "value"))
    changed_markup_decimal = markup_amount / 100
    calculated_final_rate = currency_rate + (currency_rate * changed_markup_decimal)
    assert final_rate == calculated_final_rate

    # CHANGED MARKUP AMOUNT AND UPDATED FINAL RATE VERIFICATION
    changed_markup_amount = markup_amount + 1
    currencies_page.set_value_into_specific_input_field(CurrenciesLocators.markup_amount_data_qa, changed_markup_amount)
    changed_markup_decimal = float(changed_markup_amount) / 100
    calculated_updated_final_rate = currency_rate + (currency_rate * changed_markup_decimal)
    currencies_page.click_on_element(CurrenciesLocators.save_btn_data_qa)
    currencies_page.click_on_element(CurrenciesLocators.submit_btn_locator)
    # Temporary redirect to currencies list page and assertion disabling, b/c https://eskimidev.atlassian.net/browse/RTB-8873
    # assert "currency rate changes saved successfully" in currencies_page.get_element_text(
    #     CurrenciesLocators.alert_message_data_qa)

    driver.get(currencies_list_page_url)
    currencies_page.select_dropdown_value(CurrenciesLocators.currency_filter_data_qa, currency_name)
    currencies_page.wait_for_spinner_load(spinner_locator=CurrenciesLocators.processing_locator)
    assert currency_rate == float(currencies_page.get_element_text(CurrenciesLocators.currency_rate_from_list_locator))
    assert changed_markup_amount == float(currencies_page.get_element_text(
        CurrenciesLocators.markup_amount_from_list_locator))
    assert "Yes" == currencies_page.get_element_text(CurrenciesLocators.auto_update_rate_list_locator)
    assert round(calculated_updated_final_rate, 2) == round(float(currencies_page.get_element_text(
        CurrenciesLocators.final_rate_from_list_locator)), 2)
    currencies_page.click_on_adjust()
    assert changed_markup_amount == int(currencies_page.get_attribute_value(
        CurrenciesLocators.markup_amount_data_qa, "value"))
    updated_final_rate = currencies_page.get_attribute_value(CurrenciesLocators.final_rate_data_qa, "value")
    assert calculated_updated_final_rate == float(updated_final_rate)

    # CHANGED FINAL RATE AND UPDATED MARKUP AMOUNT VERIFICATION
    currencies_page.check_uncheck_specific_checkbox(
        CurrenciesLocators.auto_update_market_exchange_currency_rate_checkbox_data_qa, do_check=False)
    changed_final_rate = float(updated_final_rate) + 2
    rounded_final_rate = round(changed_final_rate)
    currencies_page.set_value_into_specific_input_field(CurrenciesLocators.final_rate_data_qa, rounded_final_rate)
    calculated_updated_markup_amount = ((rounded_final_rate - currency_rate) / currency_rate) * 100
    currencies_page.click_on_element(CurrenciesLocators.save_btn_data_qa)
    currencies_page.click_on_element(CurrenciesLocators.submit_btn_locator)
    # Temporary redirect to currencies list page and assertion disabling, b/c https://eskimidev.atlassian.net/browse/RTB-8873
    # assert "currency rate changes saved successfully" in currencies_page.get_element_text(
    #     CurrenciesLocators.alert_message_data_qa)
    driver.get(currencies_list_page_url)
    currencies_page.select_dropdown_value(CurrenciesLocators.currency_filter_data_qa, currency_name)
    assert currency_rate == float(currencies_page.get_element_text(CurrenciesLocators.currency_rate_from_list_locator))
    assert round(calculated_updated_markup_amount, 5) == round(float(currencies_page.get_element_text(
        CurrenciesLocators.markup_amount_from_list_locator)), 5)
    assert "No" == currencies_page.get_element_text(CurrenciesLocators.auto_update_rate_list_locator)
    assert rounded_final_rate == round(float(currencies_page.get_element_text(
        CurrenciesLocators.final_rate_from_list_locator)))
    currencies_page.click_on_adjust()
    assert rounded_final_rate == round(float(currencies_page.get_attribute_value(
        CurrenciesLocators.final_rate_data_qa, "value")))
    updated_markup_amount = float(currencies_page.get_attribute_value(
        CurrenciesLocators.markup_amount_data_qa, "value"))
    assert round(calculated_updated_markup_amount, 5) == round(updated_markup_amount, 5)

    generic_modules.step_info("[END - RTB-8650] Verify correct data displayed and currency rate edit functionality")
