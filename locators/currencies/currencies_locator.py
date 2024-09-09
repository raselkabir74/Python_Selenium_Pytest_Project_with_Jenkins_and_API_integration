from selenium.webdriver.common.by import By


class CurrenciesLocators:
    # [Start] data-qa attribute values
    currency_filter_data_qa = 'currency-select'
    currency_name_data_qa = "currency-name"
    auto_update_rate_filter_data_qa = 'auto-update-rate-select'
    clear_all_btn_data_qa = 'clear-all-btn'
    filter_count_data_qa = 'filter-btn'
    cancel_btn_data_qa = "cancel-btn"
    currency_rate_data_qa = "currency-rate-input"
    markup_amount_data_qa = 'markup-amount-input'
    final_rate_data_qa = "final-rate-input"
    Yemen_Rial_three_dot_data_qa = 'item-action-159'
    Yemen_Rial_three_dot_adjust_data_qa = "item-action-Adjust-159"
    Yemen_Rial_updated_by = 'updated-by-159'
    Yemen_Rial_updated_at = 'updated-at-159'
    created_by_info_data_qa = "created-by-info"
    last_updated_by_info_data_qa = "last-update-by-info"
    created_info_data_qa = "created-info"
    last_updated_info_data_qa = "last-updated-info"
    auto_update_market_exchange_currency_rate_checkbox_data_qa = 'auto-update-market-exchange-currency-rate-check'
    save_btn_data_qa = 'save-btn'
    alert_message_data_qa = 'alert'
    currency_filter_select_data_qa = 'currency-select'
    # [End] data-qa attribute values

    # [Start] locators
    processing_locator = (By.ID, 'accampaign_table_processing')
    auto_update_rate_list_locator = (By.XPATH, "//span[contains(@data-qa, 'dynamic-currency-rate')]")
    rows_info_locator = (By.ID, 'billing_currency_rate_list_table_info')
    currency_name_locator = (By.XPATH, "(//span[contains(@data-qa, 'name')])[1]")
    currency_rate_from_list_locator = (By.XPATH, "(//span[contains(@data-qa, 'currency-rate')])[1]")
    markup_amount_from_list_locator = (By.XPATH, "(//span[contains(@data-qa, 'markup-amount')])[1]")
    final_rate_from_list_locator = (By.XPATH, "(//span[contains(@data-qa, 'final-rate')])[1]")
    three_dot_locator = (By.XPATH, "(//a[contains(@data-qa, 'item-action')])[1]")
    adjust_locator = (By.XPATH, "(//a[contains(@data-qa, 'item-action-Adjust')])[1]")
    submit_btn_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    # [End] locators
