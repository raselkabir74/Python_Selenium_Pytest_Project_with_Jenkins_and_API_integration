from selenium.webdriver.common.by import By


class CampaignApproveLocators:
    # [START] data-qa attribute values
    campaign_status_data_qa = "campaign-status-info"
    client_name_data_qa = "partner-info"
    creative_type_data_qa = "creative-type-info"
    campaign_name_data_qa = "campaign-name-info"
    ad_domain_data_qa = "ad-domain-info"
    landing_page_data_qa = "click-url-info"
    campaign_purpose_data_qa = "campaign-purpose-info"
    countries_data_qa = "countries-info"
    brand_safety_data_qa = "brand-safety-apps-sites"
    contextual_targeting_apps_sites_data_qa = "contextual-targeting-apps-sites"
    contextual_targeting_keywords_data_qa = "contextual-targeting-keywords"
    mobile_operators_data_qa = "mobile-operators-isps-info"
    packages_data_qa = "packages-info"
    device_types_data_qa = "device-types-info"
    oses_data_qa = "oses-info"
    device_brands_data_qa = "devices-brands-info"
    device_models_data_qa = "devices-models-info"
    advanced_telecom_targeting_data_qa = "advanced-telecom-targeting-info"
    audiences_data_qa = "audiences-info"
    demographic_data_qa = "demographic-info"
    languages_data_qa = "languages-info"
    sec_data_qa = "groups-info-SEC (socio-economic class)"
    device_cost_ranges_data_qa = "device-cost-ranges-info"
    ad_exhanges_data_qa = "ad-exchanges-info"
    content_types_data_qa = "content-types-info"
    tech_fee_locator = "tech-fee-input"
    impression_performance_metric_locator = "ac-metric-targeting"
    impression_performance_metric_viewability_locator = "viewability-input"
    impression_performance_metric_ctr = "click_through_rate-input"
    impression_performance_metric_vcr = "video_completion_rate-input"
    custom_impression_tracking_locator = "ac-tracking"
    viewability_and_video_support_locator = "ac-viewability"
    video_player_requirement_locator = "ac-video-player-requirements"
    mraid_support_locator = "ac-mraid"
    anti_fraud_setting_locator = "ac-antifraud-settings"
    enhanced_min_reach_locator = "enhanced-reach-metric-min-input"
    enhanced_max_reach_locator = "enhanced-reach-metric-max-input"
    approve_button_locator = "campaign-approve-btn"
    delete_button_locator = "campaign-delete-btn"
    cancel_button_locator = "campaign-cancel-btn"
    reject_button_locator = "campaign-reject-btn"
    remove_completely_button_locator = "campaign-remove-btn"
    approve_edit_button_locator = "campaign-edit"
    approve_report_button_locator = "campaign-report"
    approve_preview_button_locator = "campaign-preview_in_browser"
    approve_three_dot_locator = "campaign-menu-action-btn"
    approve_three_dot_targeting_optimisation_locator = "campaign-optimisation"
    approve_three_dot_report_locator = "campaign-report"
    approve_three_dot_preview_locator = "campaign-preview_in_browser"
    approve_three_dot_duplicate_campaign_locator = "campaign-duplicate"
    approve_three_dot_changelog_locator = "campaign-changelog"
    approve_three_dot_pixels_locator = "campaign-tracking_pixels"
    goal_type_locator = "goal-type-info"
    goal_pre_optimisation_locator = "pre-optimise-historical-info"
    campaign_id = "campaign-id-info"
    ad_exchange_check_all_locator = "exchange-check-all-btn"
    insertion_order_label = "io-order-select"
    advertiser_name_label = "advertiser-name-select"
    email_report_label = "email-options-check"
    Test_QA_margin_label = "exchange-id-7"
    daily_budget_recalculation_label = "daily-budget-recalculation-check"
    reporting_type_input_data_qa = "reporting-type-input"
    table_and_kpi_dropdown_data_qa = "table-and-kpi-column-options-section"
    spent_checkbox_data_qa = "tmp-report-option-check-2048"
    cpm_data_qa = "tmp-report-option-check-256"
    cpc_data_qa = "tmp-report-option-check-512"
    cpe_data_qa = "tmp-report-option-check-67108864"
    dates_data_qa = "dates-info"
    success_message_data_qa = "alert"
    # [END] data-qa attribute values

    # [Start] locators
    private_deals_locator = (
        By.XPATH,
        "//label[contains(text(),'Anzu - ALWAYS ON - EMEA Tier 2 - Display Mobile')]")
    deal_margin_locator = (
        By.XPATH, "//input[contains(@name, 'deals_margin')]")
    add_more_custom_impression_tracking_locator = (
        By.XPATH,
        "//label[@href='#ac-tracking']/following-sibling::div//button")
    custom_impression_tracking_textarea_locator = (
        By.XPATH, "//textarea[@class='ace_text-input']")
    button_alert_ok_locator = (By.XPATH, '//button[@data-bb-handler="ok"]')
    ignore_button_locator = (
        By.XPATH, "//button[contains(text(), 'Ignore')]")
    close_button_locator = (By.XPATH,
                            "//button[@class = 'btn btn-success' and contains(text(), 'Close')]")
    reject_reason_textarea_locator = (By.ID, 'reject-reason')
    reject_close_button_locator = (
        By.XPATH, "//button[contains(text(), 'Close')]")
    reject_submit_button_locator = (By.ID, 'reject-btn')
    advertise_category_locator = (
        By.XPATH, "//select[@id='js-categories']/option")
    approve_three_dot_edit_locator = (
        By.XPATH, "//a[@title='Edit'][normalize-space()='']")
    approve_click_url_locator = (
        By.XPATH,
        "//a[normalize-space()='https://business.eskimi.com']")
    creative_size_pop_up_ignore_locator = (
        By.XPATH, "//button[contains(text(), 'Ignore')]")
    publish_change_button_locator = (By.XPATH, "//button[contains(text(), 'Publish changes')]")
    creatives_bid_locator = (By.XPATH, "//div[@class='creatives-preview-container']//div[contains(text(), 'Bid:')]")
    bid_locator = (By.XPATH, "//div[@data-qa='bid-info']")
    daily_total_budget_locator = (By.XPATH, "//div[@data-qa='budget-info']")
    main_margin_locator = (By.XPATH, "//input[@data-qa='main-margin-input']")
    modal_message_locator = (By.XPATH, "//div[@class='modal-body']//ul/li/b")
    main_margin_changes_modal_confirm_btn_locator = (
        By.XPATH, "//div[@class='modal-footer']//button[@data-bb-handler='success']")
    main_margin_changes_modal_title_locator = (
        By.XPATH, "//div[@class='modal-content']//*[text()='Changing the main margin']")
    error_message_locator = (By.XPATH, "//div[@class='alert alert-danger alert-dismissible fade show']")
    reporting_type_currency_locator = (By.XPATH, "//i[@class='add-on float-right']")
    states_locator = (By.XPATH,
                      "//div[label[@class='text-value' and text()='States']]//div[@class='form-control-text']")
    cities_locator = (By.XPATH,
                      "//div[label[@class='text-value' and text()='Cities']]//div[@class='form-control-text']")
    # [End] locators

    # [Start] label names
    ad_exchange_margin_label = "Eskimi standard margin"
    advertiser_category_label = "Advertisement category"
    budget_pacing_label = "Budget pacing"
    email_report_frequency_label = "Report frequency"
    email_report_hour_label = "Report hour"
    email_report_day_label = "Report day"
    group_by_io_label = "Group by IO"
    email_attachments_label = "Email attachments"
    generate_insight_report_label = "Generate insights report"
    multiple_bid_per_second_label = "Allow multiple bids per user per second"
    margin_type_label = "Margin type"
    # [End] label names

    # [Start] Attribute values
    custom_impression_tracking_dropdown_id = "ac-tracking"
    io_id = "select2-io-container"
    advertiser_name_id = "select2-adv-name-container"
    custom_impression_tracking_dropdown_xpath = "//div[@id='ac-tracking']/..//span[@class='select2-selection__rendered']"
    custom_impression_tracking_text_xpath = "//div[@id='ac-tracking']/..//span[@class='ace_text ace_xml']"
    viewability_and_video_support_div_id = "ac-viewability"
    video_player_requirement_div_id = "ac-video-player-requirements"
    mraid_support_div_id = "ac-mraid"
    anti_fraud_setting_div_id = "ac-antifraud-settings"
    ad_exchange_margin_text_xpath = "//label[normalize-space()='{}']/../following-sibling::div//input[@type='number']"
    # [End] Attribute values
