from selenium.webdriver.common.by import By


class ProformaListLocators:
    # [Start] locators
    search_field_locator = (By.XPATH, "//input[@data-qa='search-filter-input']")
    three_dot_of_io_xpath = "//a[@data-qa='item-action-{}']/..//i[@class='fas fa-ellipsis-v']"
    first_grid_item_locator = (
        By.XPATH,
        "//a[contains(@data-qa, 'client-')]")
    # [End] locators

    # [Start] label names
    edit_io_label_data_qa = "item-action-Edit"
    # [End] label names

    # [Start] Attribute values
    dropdown_menu_mx_auto_dropdown_menu_left_class = "dropdown-menu mx-auto dropdown-menu-left"
    # [End] Attribute values
