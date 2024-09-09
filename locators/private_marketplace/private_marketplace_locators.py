from selenium.webdriver.common.by import By


class PrivateMarketplaceLocators:
    # [START] data-qa attribute values
    title_label_data_qa = 'title-column'
    new_pmp_btn = "new-private-deal-btn"
    bid_cpm_label_data_qa = "bid-price-label"
    cancel_btn = "cancel-btn"
    list_first_pmp_locator = (By.XPATH, "(//td[@class='sorting_1']//a)[1]")
    # [END] data-qa attribute values
