from selenium.webdriver.common.by import By


class InvoiceTrackerLocators:
    # [Start] locators
    payment_modal_locator = (By.XPATH, "//div[@class='modal-content']")
    amount_paid_input_locator = (By.ID, 'paid-amount')
    first_payments_log_table_row_locator = (By.XPATH, '//*[@id="payments-table"]//tr[1]')
    # [End] locators

    # [START] data-qa attribute values
    invoice_tracker_logs_data_qa = 'campaing-io-action-dropdown'
    payment_action_data_qa = 'payment-actions-item'
    invoice_tracker_filter_data_qa = 'invoice-number-data-qa'
    country_row_data_qa = (By.XPATH, "//div[contains(@data-qa, 'country-')]")
    three_dots_action_data_qa = (By.XPATH, "//a[contains(@data-qa, 'item-action-')]")
    add_payment_option_data_qa = (By.XPATH, "//a[contains(@data-qa, 'item-action-Add payment-')]")
    overlay_loading_locator = (By.XPATH, '//div[@data-qa="overlay-loading"]')
    # [END] data-qa attribute values
