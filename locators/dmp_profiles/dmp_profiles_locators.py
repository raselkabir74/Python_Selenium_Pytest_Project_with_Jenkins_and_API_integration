from selenium.webdriver.common.by import By


class DMPprofiels:
    # [START] data-qa attribute values
    filter_data_qa = "filter-span"
    list_name_data_qa = "list-name-label"
    order_title_data_qa = "title-label"
    cancel_btn = "cancel-btn"
    add_request_btn = "add-request-btn"
    list_first_item_3_dot_data_qa = (By.XPATH, '(//td[@class="dropdown actions"]//a)[1]')
    list_first_item_edit_locator = (By.XPATH, '(//a[@title="Edit"])[1]')
    # [END] data-qa attribute values
