from selenium.webdriver.common.by import By


class FactoringReportLocators:
    # [Start] locators
    company_filter_locator = (By.ID, 'company_filter')
    first_factoring_report_table_row_locator = (By.XPATH, '//*[@id="factoring-table_wrapper"]//tr[1]')
    # [End] locators
