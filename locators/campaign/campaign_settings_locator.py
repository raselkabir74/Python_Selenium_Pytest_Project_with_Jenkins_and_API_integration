from selenium.webdriver.common.by import By


class CampaignSettingsLocator:
    # [Start] data-qa attribute values
    user_filter_data_qa = "campaign-user-filter-select"
    total_budget_data_qa = "total-budget-{}"
    total_spend_data_qa = "total-spent-{}"
    remaining_total_data_qa = "total-remaining-budget-{}"
    daily_budget_data_qa = "daily-budget-{}"
    today_spend_data_qa = "today-spent-{}"
    remaining_today_data_qa = "today-remaining-budget-{}"
    # [End] data-qa attribute values

    #  [Start] locators
    campaign_search_field_locator = (By.ID, "filter_name")
    loader_locator = (By.ID, 'loader-container')
    search_box_locator = (By.ID, 'filter_name')
    campaign_name_edit_field_locator = (By.ID, 'name')
    bid_cpm_edit_field_locator = (By.ID, 'bid_currency')
    click_url_edit_field_locator = (By.ID, 'click_url')
    ad_domain_locator = (By.ID, 'select2-ad_domain-container')
    tick_or_cross_sign_click_url_locator = (By.XPATH,
                                            "//input[@id='click_url']//following-sibling::span//i[contains(@class, 'fa-check') or contains(@class ,'fa-times')]")
    ad_domain_search_field_locator = (
        By.XPATH, "//input[@class='select2-search__field']")
    apply_to_all_creative_label_locator = (
        By.XPATH, "//label[@for='apply_to_all_creative']")
    campaign_search_button_locator = (
        By.XPATH, "//button[contains(text(),'Search')]")
    campaign_settings_locator = (
        By.XPATH, "//a[contains(text(),'Campaign settings')]")
    btn_create_locator = (By.XPATH,
                          "//a[contains(@class, 'btn-create') and contains(@class ,'bg-blue')]")
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    status_dropdown_locator = (By.ID, 'select2-filter_status-container')
    all_status_option_locator = (
        By.XPATH,
        "//ul[@id='select2-filter_status-results']/li[normalize-space(text())='All']")
    campaign_settings_navigation = "(//dfn[@class='sidebar-tooltip']//*[contains(text(),'Campaign settings')])"
    campaign_stopped_status_locator = (
        By.XPATH, "//span[contains(text(), 'Sto.')]")
    campaign_status_locator = (By.XPATH, "//td[@data-dt-column='4']//span")
    campaign_inactive_status_locator = (By.XPATH, "//div[@class='campaign-status-hour-inactive']")
    user_selector = (By.XPATH,
                     "//label[contains(text(), 'User')]/../descendant::span[@role='presentation']")
    # PREVIEW PAGE LOCATOR
    preview_in_browser_locator = (
        By.XPATH, "//a[@data-role='preview_in_browser']")
    preview_ad_div_locator = (By.ID, 'adsArea')
    native_preview_ad_div_locator = (By.ID, 'ad-container-cover')
    video_preview_ad_div_locator = (By.XPATH, "(//div[contains(@id, 'vast-video')])[1]")
    preview_toggle_locator = (By.XPATH, "//div[@data-qa='device_toggle-btn']")
    creative_three_dot = (
        By.XPATH, "//a[@class='dropdown-toggle hide-arrow']")
    preview_copy_icon = (By.XPATH, "//div[@data-qa='copy-btn']")
    preview_previous_version = (
        By.XPATH,
        "//p[contains(text(), 'Switch to previous version')]")
    preview_previous_title = (By.XPATH, "//div[@id='container']//b")
    preview_platform_url_locator = (
        By.XPATH,
        '(//p[text()="Programmatic Blog"])[2]')
    preview_ad_gallery_url_locator = (
        By.XPATH, '(//p[text()="Ad Gallery"])[2]')
    preview_manual_url_locator = (
        By.XPATH, '(//p[text()="Eskimi Manual"])[2]')
    preview_book_demo_url_locator = (
        By.XPATH, '(//p[text()="Book a Demo"])[2]')
    data_checkbox_all = 'data-table-check'
    iframe_locator = (By.XPATH, "//iframe[@id]")
    # [End] locators

    # [Start] labels
    campaign_name_title = "Edit campaign name"
    bid_cpm_title = "Edit bid cpm"
    landing_page_title = "Edit landing page"
    creative_set_title = "Edit creative sets"
    creative_set_label = "Selected creative sets"
    # [End] labels

    # [Start] Attributes
    modal_save_button_xpath = "//div[@class='modal-footer']//button[@data-bb-handler='save' and @type='button' and contains(text(),'SAVE')]"
    status_dropdown_id = "select2-filter_status-container"
    campaign_name_xpath_locator = "(//a[contains(text(), '{}')])[{}]"
    three_dot_of_campaign_xpath = "//*[@class='dropdown actions']//i[@class='fas fa-ellipsis-v']"
    campaign_list_duplicate_locator = "//a[@data-qa='item-action-Duplicate campaign-{}']"
    bid_cpm_id = "bid_currency_{}"
    # [End] Attributes
