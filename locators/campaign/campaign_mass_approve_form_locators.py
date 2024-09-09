from selenium.webdriver.common.by import By


class CampaignMassApproveFormLocators:
    # [Start] locators
    mass_approve_header_locator = (
        By.XPATH,
        "//a[@class='active' and normalize-space()='Mass approve']")
    approve_button_locator = (
        By.XPATH, "//button[@class='btn btn-success btn-block']")
    ignor_button_locator = (By.XPATH, "//button[@class='btn btn-danger']")
    specific_adv_category_locator = (
        By.XPATH, "//select[@name='[]']//option[@value='IAB19']")
    specific_app_site_category_locator = (
        By.XPATH, "//select[@name='[]']//option[@value='31']")
    mass_daily_budget_recalculation_locator = (
        By.XPATH, "//input[@data-key='128']")
    exchange_prompt_ok_button_locator = (
        By.XPATH, "//button[@class='btn btn-primary']")
    adv_category_dropdown_values_locator = (
        By.ID, "js-categories-280C28CD-94A0-428C-AE73-7A3777FFF818")
    main_margin_modal_message_locator = (By.XPATH, "//div[@class='bootbox-body']//ul//li[1]")
    main_margin_changes_modal_title_locator = (
        By.XPATH, "//div[@class='modal-content']//*[text()='Changing the main margin']")
    main_margin_changes_modal_confirm_btn_locator = (
        By.XPATH, "//div[@class='modal-footer']//button[@data-bb-handler='cancel']")
    error_message_locator = (By.XPATH, "//span[@class='error-message']")
    # [End] locators

    # [Start] Column names
    insertion_order_column = "Insertion"
    insertion_order_column_mandatory = "Insertion *"
    advertisement_category_column = "Advertisement category"
    app_site_category_column = "App/Site category"
    advertiser_name_column = "Advertiser name"
    budget_pacing_column = "Budget pacing"
    daily_budget_recalculation_column = "Daily budget recalculation"
    strict_creative_size_placement_column = "Strict creative size placement"
    multiple_bids_per_user_second_column = "Multiple bids/user/second"
    ad_exchange_column = "Ad exchanges"
    private_deals_column = "Private deals"
    # [End] Column names

    # [Start] label name
    margin_type_label = "Margin type"
    ad_exchange_name_label = "Eskimi standard margin"
    # [End] label name

    # [Start] Attribute values
    campaign_mass_approve_form_id = "js-main-form"
    advertisement_category_modal_xpath = "//select[@name='campaigns[{}][excluded_cat][]']"
    app_site_category_modal_xpath = "//select[@name='campaigns[{}][sites_categories][]']"
    ad_exchange_text_field_xpath = "(//input[@data-name='{}'])[{}]/..//..//following-sibling::div//input"
    deal_margin_text_field_xpath = "(//input[contains(@name,'[deals_margin]')])[{" \
                                   "}]/..//..//following-sibling::div//input "
    advertiser_name_xpath = "(//tr[@data-campaign-id='{}']//span[contains(@id,'select2-campaigns')])[3]"
    ad_exchanges_xpath = "//tr[@data-campaign-id='{}']//div[contains(text(),'Exchanges')]"
    main_margin_input_xpath = "//tr[@data-campaign-id='{}']//div[contains(text(),'Exchanges')]/..//input[" \
                              "contains(@name, '[margin_main]')]"
    ad_exchanges_ok_btn_xpath = "//tr[@data-campaign-id='{}']//div[contains(text(),'Exchanges')]/..//button[" \
                                "@class='btn btn-primary js-modal-data-save']"
    error_message_for_specific_campaign_xpath = "//tr[@data-campaign-id='{}']//span[@class='error-message']"
    # [End] Attribute values
