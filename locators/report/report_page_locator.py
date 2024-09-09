from selenium.webdriver.common.by import By


class ReportPageLocators:
    # [Start] locators
    report_title_locator = (
        By.XPATH, "//div[@class='col-12 col-md-4 titles']/h3")
    specific_date_locator = "//td[contains(@class, 'd_{}')]/a"
    loader_icon_locator = (
        By.XPATH, "//a[@href='#tab-0']//i[@class='loader-icon']")
    widget_list_locator = (
        By.XPATH, "//*[@id='tab-0']//div[@class='widgets w-row']/div")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-info alert-dismissible fade show']")
    export_link_locator = (
        By.XPATH, "//span[normalize-space(text())='Export']")
    excel_export_link_locator = (
        By.XPATH, "//span[normalize-space(text())='Excel']")
    pdf_export_link_locator = (
        By.XPATH, "//span[normalize-space(text())='PDF']")
    pdf_chart_export_link_locator = (
        By.XPATH, "//span[normalize-space(text())='PDF with charts']")
    close_alert_button_locator = (
        By.XPATH, "//button[@data-dismiss='alert']")
    cross_icon_locator = (By.XPATH, "//span[normalize-space()='×']")
    # [Start] locators

    # [Start] data-qa attribute values
    datepicker_apply_btn_data_qa = "datepicker-apply-btn"
    update_report_button_data_qa = "update-report-btn"
    date_range_link_data_qa = "date-range-field-input"
    all_date_data_qa = "date-picker-quicklink-all,"
    last_month_data_qa = "date-picker-quicklink-last month,"
    report_view_select_data_qa = "view-select"
    campaign_select_data_qa = "campaign-select"
    spent_select_data_qa = "spent-select"
    impression_value_data_qa = "metric-Impressions"
    reach_value_data_qa = "metric-Reach"
    ctr_value_data_qa = "performance-metric-CTR"
    cpc_amount_data_qa = "performance-metric-CPC"
    cpe_amount_data_qa = "performance-metric-CPE"
    cpm_amount_data_qa = "performance-metric-CPM"
    spent_amount_data_qa = "performance-metric-Spent"
    # [End] data-qa attribute values

    # [Start] Attributes
    widget_list_xpath = "//*[@id='tab-0']//div[@class='widgets w-row']/div[{}]"
    # [End] Attributes

    # [Start] options name
    admin_view = "Admin view"
    client_view = "Client view"
    spent_based_on_cost = "Spent based on cost"
    spent_based_on_revenue = "Spent based on revenue"
    spent_based_on_revenue_with_margin = "Spent based on revenue with margin"
    spent_based_on_revenue_with_agency_share = "Spent based on revenue with agency share"
    #end options name
