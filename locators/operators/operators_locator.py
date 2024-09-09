from selenium.webdriver.common.by import By


class Operators:
    # [START] data-qa attribute values
    filter_data_qa = "filter-span"
    list_name_data_qa = "list-name-label"
    title_data_qa = "title-label"
    full_title_data_qa = "full-title-label"
    cancel_btn = "cancel-btn"
    add_operator_btn = "add-new-operator-btn"
    list_first_item_3_dot_locator = (By.XPATH, '(//td[@class="dropdown actions"]//a)[1]')
    list_first_item_edit_locator = (By.XPATH, '(//a[@title="Edit"])[1]')
    # [END] data-qa attribute values
