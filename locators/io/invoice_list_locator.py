from selenium.webdriver.common.by import By


class InvoiceListLocators:
    # [Start] locators
    first_grid_item_locator = (
        By.XPATH,
        "//table[@id='campaigns-invoice-table']//tbody//tr//a")
    invoice_list_date_locator = (
        By.XPATH, "//td[@class=' invoice-list-date']")
    # [End] locators

    # [Start] label names
    client_account_label = "Client account"
    rows_per_page_label = "Rows per page "
    # [End] label names

    # [Start] Options
    all_option = "All"
    # [End] Options
