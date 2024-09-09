from selenium.webdriver.common.by import By


class IncomeReportLocators:
    # [Start] locators
    first_income_report_table_row_locator = (By.XPATH, '//*[@id="income_report_table"]//tr[1]')
    # [End] locators

    # [START] data-qa attribute values
    billing_entity_filter_data_qa = 'billing-entity-select'
    bank_receive_statement_country_th_data_qa = 'country-th'
    bank_receive_statement_history_data_qa = 'history-btn'
    history_transaction_date_th_data_qa = 'transaction-date-data-qa'
    three_dots_action_data_qa = (By.XPATH, "//a[contains(@data-qa, 'item-action-')]")
    add_transaction_option_data_qa = (By.XPATH, "//a[contains(@data-qa, 'item-action-dropdown-')]")
    # [END] data-qa attribute values

    # [Start] title labels values
