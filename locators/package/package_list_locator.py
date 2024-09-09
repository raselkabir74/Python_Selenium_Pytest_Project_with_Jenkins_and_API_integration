from selenium.webdriver.common.by import By


class PackageListLocators:
    # [START] data-qa attribute values
    add_package_button_locator_data_qa = "new-package-btn"
    search_box_locator = "filter-input"
    delete_link_locator = "delete-btn"
    edit_link_locator = "edit-btn"
    # [End] data-qa attribute values
    # [Start] locators
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    message_modal_locator = (By.XPATH, "//div[@class='bootbox-body']")
    message_modal_ok_btn_locator = (By.XPATH, "//button[@class='btn btn-primary']")
    alert_confirm_button_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    checkbox_locator = "//input[@data-qa='data-table-check']"
    package_column_locator = (By.XPATH, "//span[@class='sortable sortable_after' and contains(text(),'Package')]")
    sorted_packages_list_locator = (By.XPATH, "//td[@class='text-left sorting_1']//a[contains(@data-qa, 'package')]")
    package_name_locator = (By.XPATH, "//td[@class=' text-left']//a[contains(@data-qa, 'package')]")
    type_column_locator = (By.XPATH, "//span[@class='sortable sortable_after' and contains(text(),'Type')]")
    type_locator = (By.XPATH, "//span[contains(@data-qa, 'data-type')]")
    apps_sites_placements_column_locator = (
        By.XPATH, "//span[@class='sortable sortable_after' and contains(text(),'Apps/Sites/Placements')]")
    apps_sites_placements_locator = (By.XPATH, "//span[contains(@data-qa, 'apps-sites-palcements')]")
    impressions_column_locator = (
        By.XPATH, "//span[@class='sortable sortable_after' and contains(text(),'Impressions (1d)')]")
    impressions_locator = (By.XPATH, "//span[contains(@data-qa, 'impressions')]")
    auction_type_column_locator = (
        By.XPATH, "//span[@class='sortable sortable_after' and contains(text(),'Auction type')]")
    auction_type_locator = (By.XPATH, "//span[contains(@data-qa, 'auction-type')]")
    date_column_locator = (By.XPATH, "//span[@class='sortable sortable_after' and contains(text(),'Date')]")
    date_locator = (By.XPATH, "//span[contains(@data-qa, 'date')]")
    # [Start] locators

    # [Start] attribute values
    package_checkbox_xpath = "//table[@id='package_list_table']//a[@title='{}']/..//../td//input[@type='checkbox']"
    # [End] attribute values

    # [Start] labels
    rows_per_page_label = "Rows per page "
    # [End] labels
