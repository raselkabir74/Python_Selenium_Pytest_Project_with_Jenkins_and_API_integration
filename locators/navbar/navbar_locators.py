from selenium.webdriver.common.by import By


class NavbarLocators:    
    # [START] data-qa attribute values
    search_box_locator = "impersonate-search-input"
    three_dot_locator = "nav-settings-menu-three-dot-icon"
    logout_locator = "log-out-item"
    login_as_locator = "log-in-as-item"
    logout_as_locator = "log-in-as-item"
    # [START] data-qa attribute values

    # [Start] locators
    account_dropdown_locator = (By.ID, "navAccountsDropdown")
    account_name = '//a[normalize-space()="{}"]'
    username_locator = (By.ID, 'username')
    password_locator = (By.ID, 'password')
    # [End] locators
