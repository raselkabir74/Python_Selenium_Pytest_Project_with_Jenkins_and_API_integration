from selenium.webdriver.common.by import By


class OptimizationLocators:
    # [Start] Locators
    search_button_locator = (By.ID, "search-btn")
    search_field_locator = (By.ID, "filter_name")
    app_site_column_locator = (By.XPATH, "//th[text()='App/site name']")
    grid_locator = (By.ID, "optimization_table")
    add_advance_search_options_btn_locator = (By.XPATH, "//button[@data-qa='advance-search-options-btn']")
    include_exclude_locator = (By.XPATH, "//span[@id='select2-type0-container']")
    export_excel_btn_locator = (By.XPATH, "//a[@data-qa='export-excel-btn']")
    export_csv_btn_locator = (By.XPATH, "//a[@data-qa='export-csv-btn']")
    filter_btn_locator = (By.XPATH, "//a[@data-qa='filter-btn']")
    x_btn_locator = (By.XPATH, "//i[@data-qa='remove-btn-0']")
    clear_all_btn_locator = (By.XPATH, "//a[@data-qa='clear-all-btn']")
    dates_field_locator = (By.XPATH, "//input[@data-qa='dates-input']")
    # [End] Locators

    # [Start] Label names
    campaign_label = "Campaign"
    optimise_by_label = "Optimise by"
    spent_label = "Spent"
    dates_label = "Dates"
    id_label = "ID"
    # [End] Label names

    # [Start] Dropdown items
    optimise_by_exchange_dropdown_item_value = "exchange"
    optimise_by_creative_dropdown_item_value = "creative"
    optimise_by_os_dropdown_item_value = "os"
    optimise_by_browser_dropdown_item_value = "browser"
    optimise_by_operator_dropdown_item_value = "operator"
    optimise_by_app_site_name_dropdown_item_value = "app_site_name"
    optimise_by_package_dropdown_item_value = "package"
    optimise_by_placement_dropdown_item_value = "placement"
    spent_based_on_cost_dropdown_item_value = "1"
    # [End] Dropdown items

    # [Start] Attribute values
    dropdown_optimize_by_css_selector = '[aria-labelledby="select2-optimise-by-container"] [role="presentation"]'
    dropdown_results_id = 'select2-optimise-by-results'
    table_optimization_id = 'optimization_table'
    group_by_date_id = 'date-group'
    include_option_id = 'select2-type0-container'
    source_medium_id = 'select2-source0-container'
    containing_id = 'select2-containing0-container'
    enter_value_here_id = 'value0'
    x_btn_xpath = "//i[@data-qa='remove-btn-0']"
    optimisation_table_wrapper_div_id = "optimization_table_wrapper"
    optimisation_table_specific_cell_xpath = "(//div[@id='optimization_table_wrapper']//tbody//tr[{}]//td[{}])[1]"
    optimisation_table_specific_multi_cell_xpath = "//div[@id='optimization_table_wrapper']//div[" \
                                                   "@class='dataTables_scrollBody']//tbody//tr[{}]//td[{}]/div"
    optimisation_table_specific_column_all_cell_xpath = "(//div[@id='optimization_table_wrapper']//div[" \
                                                        "@class='dataTables_scrollBody']//tbody//tr//td[{}])"
    source_medium_xpath = "//select[@data-qa='source-select-0']"
    containing_xpath = "//select[@data-qa='containing-select-0']"
    exchange_id_xpath = "//td[@data-qa='id-{}']"
    exchange_xpath = "//td[@data-qa='exchange-{}']"
    campaign_id_xpath = "//td[@data-qa='campaign-{}-{}']"
    impressions_xpath = "//td[@data-qa='impressions-{}-{}']"
    bids_xpath = "//td[@data-qa='bids-{}-{}']"
    win_rate_xpath = "//td[@data-qa='win_rate-{}-{}']"
    views_xpath = "//td[@data-qa='views-{}-{}']"
    viewability_xpath = "//td[@data-qa='viewability-{}-{}']"
    clicks_xpath = "//td[@data-qa='clicks-{}-{}']"
    ctr_xpath = "//td[@data-qa='ctr-{}-{}']"
    engaged_sessions_xpath = "//td[@data-qa='sessions-{}-{}']"
    sr_xpath = "//td[@data-qa='sr-{}-{}']"
    conversions_xpath = "//td[@data-qa='conversions-{}-{}']"
    cr_xpath = "//td[@data-qa='cr-{}-{}']"
    tech_fee_xpath = "//td[@data-qa='dev_cpm-{}-{}']"
    cpm_xpath = "//td[@data-qa='cpm-{}-{}']"
    cpc_xpath = "//td[@data-qa='cpc-{}-{}']"
    cps_xpath = "//td[@data-qa='cps-{}-{}']"
    cpa_xpath = "//td[@data-qa='cpa-{}-{}']"
    spent_xpath = "//td[@data-qa='spent-{}-{}']"
    action_btn = '//a[@data-qa="action-{}-{}"]'
    # [End] Attribute values
