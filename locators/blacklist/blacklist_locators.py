from selenium.webdriver.common.by import By


class Blacklist:
    # [START] data-qa attribute values
    blacklist_column_data_qa = "blacklist-th"
    list_name_data_qa = "list-name-label"
    type_data_qa = "type-label"
    cancel_btn = (By.XPATH, "//button[contains(normalize-space(), 'CANCEL')]")
    blacklist_btn = (By.XPATH,  "//a[contains(normalize-space(), 'New list')]")
    list_first_item_3_dot_locator = (By.XPATH, '//a[@id="action-0"]')
    list_first_item_edit_locator = (By.XPATH, "(//a[contains(normalize-space(), 'Edit')])[1]")
    # [END] data-qa attribute values
