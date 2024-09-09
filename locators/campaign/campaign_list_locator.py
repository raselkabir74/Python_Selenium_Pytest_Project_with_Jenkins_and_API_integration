from selenium.webdriver.common.by import By


class CampaignListLocators:
    # [Start] data-qa attribute values
    campaign_id_data_qa = 'edit-campaign-link-{}'
    total_budget_data_qa = 'total-budget-{}'
    total_spend_data_qa = 'total-spent-{}'
    remaining_total_data_qa = 'total-remaining-budget-{}'
    daily_budget_data_qa = 'daily-budget-{}'
    today_spend_data_qa = 'today-spent-{}'
    remaining_today_data_qa = 'today-remaining-budget-{}'
    total_budget_total_line_data_qa = 'total-budget-total'
    daily_budget_total_line_data_qa = 'total-budget-daily'
    total_spend_total_line_data_qa = 'total-spent-total'
    today_spend_total_line_data_qa = 'total-spent-today'
    # [End] data-qa attribute values

    # [Start] locators
    campaign_search_field_locator = (By.ID, "filter_name")
    campaign_search_button_locator = (
        By.XPATH, "//button[contains(text(),'Search')]")
    three_dot_first_campaign_locator = (
        By.XPATH,
        "//table[@id='campaign_list_table']//i[contains(@class,'fa-ellipsis-v')]")
    edit_option_locator = (
        By.XPATH,
        "//*[@id='campaign_list_table_wrapper']//a[@title='Edit']")
    delete_option_locator = (
        By.XPATH,
        "//*[@id='campaign_list_table_wrapper']//a[@title='Delete']")
    duplicate_campaign_option_locator = (
        By.XPATH,
        "//*[@id='campaign_setting_list_table_wrapper']//a[@title='Duplicate campaign']")
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    warning_message_locator = (By.XPATH, "//div[@class='alert alert-warning alert-dismissible fade show']")
    danger_message_locator = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible fade show']")
    btn_create_locator = (By.XPATH,
                          "//a[contains(@class, 'btn-create') and contains(@class ,'bg-blue')]")
    clear_all_locator = (
        By.XPATH, "//a[normalize-space(text())='Clear All']")
    status_dropdown_locator = (
        By.XPATH, "//span[@id='select2-filter_status-container']")
    all_status_option_locator = (
        By.XPATH,
        "//ul[@id='select2-filter_status-results']/li[normalize-space(text())='All']")
    deleted_status_option_locator = (
        By.XPATH,
        "//ul[@id='select2-filter_status-results']/li[normalize-space(text())='Deleted']")
    campaign_list_draft_status = (
        By.XPATH, "//*[contains(text(), 'Draft')][1]")
    e_cpm_xpath = "//tr[@data-qa='{}']//td[14]//span[2]"
    e_cpc_xpath = "//tr[@data-qa='{}']//td[15]//span[2]"
    ok_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='ok']")
    # [End] locators

    # [Start] label names
    edit_label = "Edit"
    delete_label = "Delete"
    approve_label = "Approve"
    campaign_goals_label = "Campaign goals"
    campaign_end_date_label = "End Date"
    rows_per_page_label = "Rows per page "
    # [End] label names

    # [Start] Attribute values
    campaign_settings_navigation = "(//dfn[@class='sidebar-tooltip']//*[contains(text(),'Campaign settings')])"
    status_dropdown_id = "select2-filter_status-container"
    three_dot_of_campaign_xpath = "//*[@class='dropdown actions']//i[@class='fas fa-ellipsis-v']"
    campaign_id_locator = ""
    campaign_table_id = "campaign_list_table_wrapper"
    campaign_multi_actions_menu_id = "multi-actions-menu"
    campaign_list_edit_locator = "//*[@id='campaign_list_table_wrapper']//a[@title='Edit']"
    campaign_list_delete_locator = "//*[@id='campaign_list_table_wrapper']//a[@title='Delete']"
    campaign_list_duplicate_locator = "//a[@title='Duplicate campaign']"
    campaign_list_approve_locator = "//*[@id='campaign_list_table_wrapper']//a[@title='Approve']"
    campaign_name_xpath_locator = "(//a[contains(text(), '{}')])[{}]"
    campaign_status_locator = "//tr[@data-qa='{}']/td[3]/span[contains(@class, 'badge')]"
    campaign_name_locator = "//tr[@data-qa='{}']//div[@class='large-text']"
    campaign_type_locator = "//tr[@data-qa='{}']/td[6]"
    creative_type_locator = "//tr[@data-qa='{}']/td[7]/i[@data-search='1']"
    campaign_country_locator = "//tr[@data-qa='{}']/td[8]/span"
    start_date_locator = "//tr[@data-qa='{}']/td[9]"
    campaigns_list_table_wrapper_div_id = "campaign_list_table_wrapper"
    campaign_status_select_data_qa = "campaign-status-filter-select"
    # [End] Attribute values
