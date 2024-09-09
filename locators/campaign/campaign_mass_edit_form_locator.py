from selenium.webdriver.common.by import By


class CampaignMassEditFormLocator:
    # [Start] locators
    save_button_locator = (
        By.XPATH, "//button[text()='Save' and @type='submit']")
    edit_campaign_header_locator = (By.XPATH,
                                    "//a[@class='active' and normalize-space()='Edit campaigns']")
    edit_campaign_creative_apply_all_locator = (
        By.XPATH,
        "//a[@class='mr-1 js-creative-change--1 table-anchor']")
    edit_campaign_creative_search_locator = (
        By.XPATH, "//ul[@class='select2-selection__rendered']")
    edit_campaign_creative_ok_button_locator = (
        By.XPATH,
        "//div[@id='js-creative-inputs--1']//button[@type='button'][normalize-space()='OK']")
    creative_dropdown_value = "//li[contains(text(), '{}')]"
    edit_campaign_bid_cpm_apply_all_locator = (
        By.XPATH,
        "//td[contains(@class,'mass-col-16 js-form-item-container')]//input[@id='bid_currency--1-apply']")
    edit_campaign_landings_apply_all_locator = (
        By.XPATH,
        "//textarea[@name='campaign-multi[-1][click_url]-apply']")
    edit_campaign_ad_domain_apply_all_locator = (
        By.XPATH,
        "//span[contains(text(),'Ad domain (e.g. yourproduct.com)')]")
    edit_campaign_apply_all_search_button_locator = (
        By.XPATH,
        "//span[@class='select2-search select2-search--dropdown']/input")
    edit_campaign_country_apply_all_locator = (
        By.XPATH,
        "//th[contains(text(), 'Country')]/following::span[contains(text(),'Please select any')]")
    edit_campaign_creative_single_ok_button_locator = (By.XPATH,
                                                       "//div[@class='modal fade js-creative-modal show']/descendant::div[@class='modal-footer']/child::button[contains(text(), 'OK')]")
    bid_fields_locator = (By.XPATH, "//div[@class='part mb-2']//input[contains(@name, '[bid_currency]') and @value]")
    daily_budget_fields_locator = (By.XPATH, "//p[contains(@data-qa, 'budget-daily-label-')]")
    total_budget_fields_locator = (By.XPATH, "//p[contains(@data-qa, 'budget-total-label-')]")
    creative_type_locator = (By.XPATH, "//td[@class='mass-col-4 js-form-item-container  ']")
    campaign_type_locator = (By.XPATH, "//td[@class='mass-col-131072 js-form-item-container  ']")
    confirm_button_alert_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    selected_creatives_locator = (By.XPATH,
                                  "//ul[@class='select2-selection__rendered']//li[@class='select2-selection__choice']")
    country_locator = (By.XPATH, "//span[@id='select2-js-country-0-container']")
    sec_locator = (By.XPATH, "(//span[@class='mselect-selection__rendered selected'])[1]")
    operators_locator = (By.XPATH, "(//span[@class='mselect-selection__rendered selected'])[2]")
    # [End] locators

    # [Start] Labels
    cpc_cost_per_click_checkbox_label = "CPC (cost per click)"
    ctr_click_through_rate_checkbox_label = "CTR (click-through rate)"
    cpa_cost_per_action_checkbox_label = "CPA (cost per action)"
    vr_viewability_rate_checkbox_label = "VR (viewability rate)"
    er_engagement_rate_checkbox_label = "ER (engagement rate)"
    cpe_cost_per_engagement_checkbox_label = "CPE (cost per engagement)"
    sr_session_rate_checkbox_label = "SR (session rate)"
    cps_cost_per_session_checkbox_label = "CPS (cost per session)"
    minimum_impressions_per_placement_to_learn_field_label = "Minimum impressions per placement to learn:"
    minimum_spend_per_placement_to_learn_field_label = "Minimum spend per placement to learn:"

    # [End] Labels

    # [Start] Column names
    name_column = "Name"
    sec_column = "SEC"
    ad_domain_column = "Ad domain"
    bid_cpm_column = "Bid (CPM)"
    budget_column = "Budget (Total/Daily)"
    landings_column = "Landings"
    operators_column = "Operators"
    optimisations_column = "Optimisations"
    creatives_column = "Creatives"
    # [End] Column names

    # [Start] Attribute values
    campaign_mass_edit_form_id = "js-main-form"
    seven_days_period_locator = '//*[@id="datepicker-calendar-{}"]/div/div[9]/div/div/a[8]'
    seven_days_period_locator_apply_all = '//*[@id="datepicker-calendar--1"]/div/div[9]/div/div/a[4]'
    ad_domain_id = 'select2-js-ad-domain-0-container'
    # [End] Attribute values

    # [Start] data-qa attribute values
    campaign_name_data_qa = 'mass-edit-campaign-name-input-0'
    second_campaign_creative_locator = 'mass-creative-select-0'
    creative_toggle_icon_locator = "creative-toggle-btn-834658"
    impression_per_creative_locator = "impression-tracking-per-creative-label-834658"
    impression_add_more_button_locator = 'add-more-btn-834658'
    total_budget_radio_btn_data_qa = 'total-budget-radio-{}'
    daily_budget_radio_btn_data_qa = 'daily-budget-radio-{}'
    estimated_budget_data_qa = 'estimated-value-label-{}'
    budget_amount_input_data_qa = 'budget-input-{}'
    budget_save_btn_data_qa = "save-btn-{}"
    edit_campaign_budget_btn_apply_all_data_qa = 'edit-budget-btn--1'
    daily_budget_radio_btn_apply_all_data_qa = "daily-budget-radio--1"
    total_budget_radio_btn_apply_all_data_qa = "total-budget-radio--1"
    edit_campaign_budget_apply_all_data_qa = 'budget-input--1'
    budget_save_btn_apply_all_data_qa = 'save-btn--1'
    total_budget_value_data_qa = 'budget-total-label-{}'
    daily_budget_value_data_qa = 'budget-daily-label-{}'
    date_picker_data_qa = 'date-range-field-{}'
    data_picker_apply_all_data_qa = 'date-range-field--1'
    landings_input_data_qa = 'mass-landing-input-0'
    # [End] data-qa attribute values
    pixel_input_locator = (By.XPATH, '//textarea[@class= "ace_text-input"]')

