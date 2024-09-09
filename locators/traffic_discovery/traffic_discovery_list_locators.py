from selenium.webdriver.common.by import By


class TrafficDiscoveryLocators:
    # [Start] locators
    traffic_discovery_table_locator = (
        By.ID, 'traffic_discovery_table_wrapper')
    chart_line_graph_locator = (By.ID, 'chart-line-graph')
    traffic_discovery_search_button_locator = (
        By.XPATH, "//a[contains(text(),'Search')]")
    traffic_discovery_table_country_locator = (
        By.XPATH, "//td[contains(@data-label, 'Country')]")
    traffic_discovery_table_packages_names_locator = (
        By.XPATH, "//td[contains(@data-label, 'Package')]")
    traffic_discovery_table_app_sites_names_locator = (
        By.XPATH, "//td[contains(@data-label, 'App/Site name')]")
    traffic_discovery_table_columns_locator = (By.XPATH, "//thead/tr[1]/th")
    # [End] locators

    # [Start] label names locator
    select_and_group_by_country_label_locator = 'Countries'
    select_and_group_by_package_label_locator = 'Packages'
    select_and_group_by_app_sites_label_locator = 'App/Site Name'
    rows_per_page_label = 'Rows per page'
    # [End] label names locator

    # [Start] Options
    country = "Lithuania"
    package_option = "Kids and Family-Oriented Games (Open Auction and PMP)"
    package_category = "Kids and Family-Oriented Games"
    site_name = "Pixel Art - Color by Number (com.europosit.pixelcoloring)"
    app_id = "632064380"
    # [End] Options
