from selenium.webdriver.common.by import By


class PaymentSettingLocators:
    # [START] data-qa attribute values
    settings_title_data_qa = "title-th"
    country_setting_form_title_data_qa = "title-label"
    country_setting_form_county_data_qa = "country-label"
    payment_option_label_data_qa = "payment-option-list-label"
    option_title_data_qa ="title-th"
    payment_option_title_data_qa = "title-label"
    payment_option_display_title_data_qa = "display-title-label"
    country_setting_btn = (By.XPATH, "//a[contains(normalize-space(), 'Add country settings')]")
    user_setting_btn = (By.XPATH, "//a[contains(normalize-space(), 'Add user settings')]")
    payment_option_btn = (By.XPATH, "//a[contains(normalize-space(), 'Add payment option')]")
    cancel_btn = (By.XPATH, "//a[contains(normalize-space(), 'CANCEL')]")
    list_first_settings_item_locator = (By.XPATH, "(//td//a)[1]")
    user_settings_option_locator = (By.XPATH, "//a[contains(normalize-space(), 'User settings')]")
    options_locator = (By.XPATH, "//a[contains(normalize-space(), 'Options')]")
    user_settings_id_locator = (By.XPATH, '//th[contains(text(), "ID")]')
    payment_option_list_first_title_locator = (By.XPATH, '(//td[@class="sorting_1"]//a)[1]')
    # [END] data-qa attribute values
