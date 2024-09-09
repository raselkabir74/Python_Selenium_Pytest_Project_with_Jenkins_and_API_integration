from selenium.webdriver.common.by import By


class AdExchanges:
    # [START] data-qa attribute values
    filter_data_qa = "filter-span"
    exchange_name_data_qa = "exchange-name-label"
    exchange_type_data_qa = "exchange-type-label"
    cancel_btn = "cancel-btn"
    ad_exchange_btn = "add-new-exchange-btn"
    list_first_ad_locator = (By.XPATH, "(//a[@class='text-title'])[1]")
    # [END] data-qa attribute values
