from selenium.webdriver.common.by import By


class AllCampaignFormLocators:
    # [Start] locators
    processing_locator = (By.ID, 'accampaign_table_processing')
    clear_all_locator = (By.XPATH, '//a[@data-qa="all-campaign-clear-all-btn"]')
    search_filter_locator = (By.ID, 'filter_name')
    all_campaign_list_status_locator = (
        By.XPATH, "//span[contains(@data-qa, 'all-campaigns-status')]")
    all_campaign_list_user_locator = (By.XPATH, "//span[contains(@data-qa, 'all-campaign-user')]")
    all_campaign_list_country_locator = (By.XPATH, "//span[contains(@data-qa, 'all-campaign-country')]")
    all_campaign_list_creative_type_locator = (By.XPATH, "//i[contains(@data-qa, 'all-campaign-creative-type')]")
    all_campaign_list_last_approved_locator = (By.XPATH, "//span[contains(@data-qa, 'all-campaign-last-approved-by')]")
    filter_btn = (By.XPATH, '//a[@data-qa="all-campaign-filter-btn"]')
    filter_area = (By.ID, 'page_filter')
    alert_message_locator = (By.XPATH, "//div[@data-qa='alert']")
    three_dot_modal_locator = (By.XPATH, "//div[@class='dropdown-menu dropdown-menu-right mx-auto show']")
    reject_popup_locator = (By.XPATH, "//div[@class='modal-content']")
    textbox_locator = (By.ID, "reject-reason")
    submit_btn_locator = (By.ID, "reject-btn")
    reject_reason_message_locator = (By.ID, "reject-reason-required-message")
    reject_popup_x_btn_locator = (By.XPATH, "//button[@class='close']")
    reject_popup_close_btn_locator = (By.XPATH, "//button[@class='btn btn-secondary']")
    delete_popup_message_locator = (By.XPATH, "//div[@class='bootbox-body']")
    delete_popup_locator = (By.XPATH, "//div[@class='modal-content']")
    delete_popup_close_btn_locator = (By.XPATH, "//button[@class='bootbox-close-button close']")
    delete_popup_no_btn_locator = (By.XPATH, "//button[@class='btn btn-danger']")
    delete_popup_yes_btn_locator = (By.XPATH, "//button[@class='btn btn-success']")
    remove_popup_locator = (By.XPATH, "//div[@class='modal-content']")
    remove_popup_x_btn_locator = (By.XPATH, "//button[@class='bootbox-close-button close']")
    no_data_for_defined_criteria_locator = (By.XPATH, "//td[normalize-space()='No data for defined criteria.']")
    # [End] locators

    # [Start] Attribute values
    table_row_id_xpath = '//a[@data-qa="all-campaign-id-{}"]'
    table_row_status_xpath = '//span[@data-qa="all-campaigns-status-{}"]'
    table_row_campaign_type_xpath = '//span[@data-qa="all-campaign-campaign-type-{}"]'
    table_row_creatives_type_xpath = '//i[@data-qa="all-campaign-creative-type-{}"]'
    table_row_country_xpath = '//span[@data-qa="all-campaign-country-{}"]'
    table_row_login_as_xpath = '//span[@data-qa="all-campaign-user-{}"]'
    table_row_login_as_btn_xpath = '//a[@data-qa="all-campaign-login-as-btn-{}"]'
    table_row_campaign_name_xpath = '//*[@data-qa="all-campaign-name-{}"]'
    table_row_last_approved_by_xpath = '//span[@data-qa="all-campaign-last-approved-by-{}"]'
    table_row_bid_by_xpath = '//div[@data-qa="all-campaign-bid-{}"]'
    table_row_daily_budget_by_xpath = '//div[@data-qa="all-campaign-daily-budget-{}"]'
    table_row_total_budget_by_xpath = '//div[@data-qa="all-campaign-total-budget-{}"]'
    all_campaigns_table_wrapper_div_id = "accampaign_table_wrapper"
    three_dot_locator = '//a[@data-qa="item-action-{}"]'
    targeting_optimization_locator = '//a[@data-qa="item-action-Targeting optimisation-{}"]'
    view_report_locator = '//a[@data-qa="item-action-View report-{}"]'
    confirm_campaign_locator = '//a[@data-qa="item-action-Confirm campaign-{}"]'
    reject_campaign_locator = '//a[@data-qa="item-action-Reject campaign-{}"]'
    delete_campaign_locator = '//a[@data-qa="item-action-Delete campaign-{}"]'
    remove_completely_campaign_locator = '//a[@data-qa="item-action-Remove completely-{}"]'
    # [End] Attribute values


    # [START] data-qa attribute values
    status_filter_locator = "all-campaign-status-filter-select"
    user_filter_locator = "all-campaign-user-filter-select"
    country_filter_locator = "all-campaign-country-filter-select"
    creative_type_filter_locator = "all-campaign-creative-filter-select"
    last_approved_filter_locator = "all-campaign-last-approved-filter-select"
    # [END] data-qa attribute values

    # [Start] Label names
    rows_per_page_label = "Rows per page "
    campaign_id_label = "ID"
    # [End] Label names

    # [Start] Options
    status_pending_option = "Pending"
    status_live_option = "Live"
    status_deleted_option = "Deleted"
    status_rejected_option = "Rejected"
    status_all_option = "All"
    user_option = "AutomationAdminUser"
    country_option = "Bangladesh"
    creative_type_option = "Banner"
    hundred_option = "100"
    # [End] Options
