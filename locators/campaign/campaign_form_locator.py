from selenium.webdriver.common.by import By


class CampaignFormLocators:
    # [Start] locators

    # [START] data-qa attribute values
    publish_button_locator = "publish-campaign-btn"
    draft_button_locator = "draft-campaign-btn"
    cancel_button_locator = "cancel-campaign-btn"
    uncheck_all_button_locator = "uncheck-all-btn"
    campaign_goal_locator_awareness = "campaign-goal-type-id-2"
    campaign_goal_locator_other = "campaign-goal-type-id-1"
    campaign_goal_locator_traffic = "campaign-goal-type-id-3"
    campaign_goal_locator_engagement = "campaign-goal-type-id-4"
    primary_objective_value_set_button_locator = "primary-goal-save-btn"
    primary_objective_optimisation_slider_locator = "pre-optimisation-check"
    secondary_objective_value_set_button_locator = "secondary-goal-submit-btn"
    secondary_objective_remove_button_locator = "secondary-goal-delete-btn"
    # 'Impression capping' locators
    impression_capping_section_locator = "ac-capping"
    default_impression_capping_checkbox = "default-country-impression-capping-check"
    impression_input_field_locator = "impression-capping-impression-input-0"
    impression_click_input_field_locator = "impression-capping-click-input-0"
    impression_time_input_field_locator = "impression-capping-amount-input-0"
    date_field_locator = "date-range-field-input"
    seven_days_date_range_locator = "date-picker-quicklink-7 days,"
    city_section_locator = "campaign-city"
    state_section_locator = "campaign-state"
    country_label = "country-select"
    brand_safety_label = "state-select"
    type_label = "campaign-creative-type-select"
    url_type_label = "click-url-type-select"
    campaign_type_label = "campaign-channel-type-select"
    bid_cpm_label = "bid-currency-input"
    total_budget_radio_btn_data_qa = "budget-type-1-radio"
    daily_budget_radio_btn_data_qa = "budget-type-0-radio"
    estimated_budget_data_qa = "budget-estimated"
    remaining_budget_data_qa = "remaining-budget-amount"
    budget_input_data_qa = "budget-amount-input"
    budget_pacing_even_data_qa = "budget-pacing-even-radio"
    brand_safety_keywords_label = "brand-safety-select"
    contextual_keywords_label = "contextual-targeting-select"
    campaign_purpose_label = "campaign-purpose-select"
    primary_operator_label = "primary-operator-select"
    age_label = "demographic-age-select"
    gender_label = "demographic-gender-select"
    languages_label = "languages-select"
    sec_socio_economic_class_groups_label = "socio-economic-class-select"
    mobile_operators_isp_label = "operators-container"
    device_type_label = "device-type-select"
    device_os_label = "oses"
    device_brands_label = "device-brand-select"
    device_models_label = "device-model-select"
    device_browsers_label = "device-browsers-select"
    device_cost_ranges_label = "device-cost-select"
    multiple_operator_sim_card_label = "multiple-operator-sim-card-select"
    mobile_data_consumption_label = "mobile-data-consumption-select"
    operator_churn_label = "operator-churn-select"
    city_label_locator = "city-select"
    state_label_locator = "state-select"
    audience_include_label_locator = "audience-include-select"
    audience_group_exclude_label_locator = "audience-group-exclude-select"
    audience_exclude_label_locator = "audience-exclude-select"
    device_brands_label_locator = "device-brand-select"
    device_models_label_locator = "device-model-select"
    mobile_operators_label_locator = "operators-container"
    multiple_operator_label_locator = "multiple-operator-sim-card-select"
    mobile_data_consumption_label_locator = "mobile-data-consumption-select"
    operator_churn_label_locator = "operator-churn-select"
    private_marketplace_label_locator = "private-marketplace-select"
    brand_safety_item_select = "siteCategoriesBrandSafetyChild-0-id-100"
    ad_exchanges_section_locator = "ad-exchanges"
    ad_exchanges_uncheck_all_button_locator = "exchange-uncheck-all-btn"
    packages_section_locator = "packages-box"
    packages_uncheck_all_button_locator = "packages-uncheck-all-btn"
    advance_targeting_selection_locator = "advanced-telecom-targeting"
    sim_amount_selection_locator = "sim-amount"
    device_connection_selection_locator = "device-connection"
    network_connection_selection_locator = "network-connection"
    demographic_section_locator = "campaign-demographic-section"
    device_models_section_locator = "device-models"
    ip_ranges_input_field_locator = "ip-ranges-box"
    ad_placement_type_locator = "ad-placement-type"
    above_the_fold_checkbox_label = "ad-placement-positions-check-1"
    below_the_fold_checkbox_label = "ad-placement-positions-check-3"
    footer_sticky_ad_checkbox_label = "ad-placement-positions-check-5"
    full_screen_checkbox_label = "ad-placement-positions-check-7"
    header_sticky_ad_checkbox_label = "ad-placement-positions-check-4"
    other_checkbox_label = "ad-placement-positions-check-0"
    sidebar_sticky_ad_checkbox_label = "ad-placement-positions-check-6"
    one_sim_checkbox_label = "sim-amount-check-1"
    two_sims_checkbox_label = "sim-amount-check-2"
    three_sims_checkbox_label = "sim-amount-check-3"
    four_sims_checkbox_label = "sim-amount-check-4"
    two_g_supporting_devices_checkbox_label = "device-connection-check-8"
    three_g_supporting_devices_checkbox_label = "device-connection-check-9"
    four_g_supporting_devices_checkbox_label = "device-connection-check-7"
    two_g_network_connection_checkbox_label = "network-connection-check-4"
    three_g_network_connection_checkbox_label = "network-connection-check-5"
    four_g_network_connection_checkbox_label = "network-connection-check-6"
    ad_exchanges_adinmo_ingame_checkbox_label = "ad-exchange-check-41"
    ad_exchanges_adverty_ingame_checkbox_label = "ad-exchange-check-42"
    ad_exchanges_anzu_ingame_checkbox_label = "ad-exchange-check-34"
    ad_exchanges_gadsme_ingame_checkbox_label = "ad-exchange-check-40"
    ad_exchanges_traffic_junky_checkbox_label = "ad-exchange-check-55"
    ad_exchanges_traffic_stars_checkbox_label = "ad-exchange-check-48"
    click_url_input_field_locator = "campaign-click-url-input"
    # [END] data-qa attribute values

    campaign_name_locator = (By.XPATH, "//div[@class='step-body']/h3")

    # 'Name & Type' locators
    platform_type_locator = (By.XPATH,
                             "//div[@class='campaign-platform-icons']/div[contains(@class, 'active')]")
    creative_type_dropdown_locator = (
        By.ID, "select2-js-campaign-type-container")
    campaign_type_dropdown_locator = (
        By.ID, "select2-js-channel-type-container")
    campaign_name_input_field_locator = (By.ID, "name")
    add_creative_from_popup_locator = (
        By.XPATH, "//button[contains(text(), 'Add creative')]")
    cancel_creative_from_popup_locator = (
        By.XPATH,
        "//button[@class='btn btn-danger' and text()='Cancel']")
    campaign_name_mandatory_message_locator = (By.ID, 'name-error')

    # 'Campaign goal' locators
    campaign_goal_section_locator = (
        By.XPATH, "//h6[contains(text(), 'Campaign goal')]")
    selected_campaign_goal_locator = (By.ID, "goal-type-value")
    campaign_goal_reset_no_locator = (
        By.XPATH, "//button[@class='btn btn-danger']")
    campaign_goal_reset_yes_locator = (
        By.XPATH, "//button[@class='btn btn-success']")
    campaign_goal_mandatory_message_locator = (
        By.ID, 'goal-type-value-error')

    # 'Primary campaign objective' locators
    primary_objective_symbol_locator = (By.ID, 'primary-goal-symbol')
    primary_objective_mandatory_message_locator = (
        By.ID, 'primary-goal-value-error')

    # 'Secondary campaign objective' locators
    secondary_objective_symbol_locator = (By.ID, 'secondary-goal-symbol')
    secondary_objective_add_additional_locator = (
        By.ID, 'add-secondary-goal')

    # 'Launch date & Budget' locators
    launch_date_and_budget_group_locator = (
        By.XPATH, "//h6[contains(text(), 'Launch date & Budget')]")
    time_and_day_scheduling_locator = (By.ID, 'time-day-scheduling')
    specific_time_and_day_scheduling_locator = (
        By.XPATH, "//td[normalize-space()='Saturday']")
    specific_time_and_day_scheduling_for_tuesday_locator = (
        By.XPATH, "//td[normalize-space()='Tuesday']")
    time_and_day_scheduling_save_button_locator = (
        By.XPATH, "//button[contains(text(), 'SAVE')]")
    start_campaign_after_approval_locator = (
        By.ID, "campaignFormauto_start_1")
    bid_cpm_in_usd_locator = (By.ID, "budget_bid_currency-in-usd")
    bid_cpm_currency_locator = (
        By.XPATH,
        "//label[contains(text(), 'Bid (CPM) ')]/following-sibling::div[1]/i[@class='add-on']")
    estimated_budget_currency_locator = (
        By.XPATH,
        "//i[@class='add-on currency-symbol']")
    bid_cpm_error_message_locator = (By.ID, 'bid_currency-error')
    total_budget_warning_message_locator = (By.XPATH, "//div[@class='errors']//ul//li")

    # 'Location & Audiences' locator
    location_and_audiences_group_locator = (
        By.XPATH, "//h6[contains(text(),'Location & Audiences')]")
    city_selection_locator = (By.XPATH,
                              "//div[@id='js-city-list']/descendant::span[@class='mselect-selection__arrow']")
    state_selection_locator = (By.ID, 'js-state-county-list')
    audience_section_locator = (By.XPATH,
                                "//span[@class='tab2-selection__rendered' and contains(text(), 'Audiences')]")
    audience_include_selection_locator = (
        By.XPATH,
        "//label[contains(text(), 'Audiences include')]/following-sibling::span")
    audience_include_value_locator = (By.XPATH,
                                      "//label[contains(text(), 'Audiences "
                                      "include')]/following-sibling::span/descendant::span[ "
                                      "@class='mselect-selection__rendered selected']")
    audience_include_search_locator = (
        By.XPATH,
        "//h4[contains(text(), 'Audiences include')]/following::input[@type='text']")
    audience_include_warning_message_locator = (
        By.XPATH,
        "//h4[contains(text(), 'Audiences include')]/following::span[contains(text(), 'No result found')]")
    audience_include_cancel_button_locator = (
        By.XPATH,
        "//h4[contains(text(), 'Audiences include')]/following::button[contains(text(), 'CANCEL')]")
    audience_exclude_value_locator = (By.XPATH,
                                      "//label[contains(text(), 'Audiences "
                                      "exclude')]/following-sibling::span/descendant::span[ "
                                      "@class='mselect-selection__rendered selected']")
    audience_exclude_selection_locator = (
        By.XPATH,
        "//label[contains(text(), 'Audiences exclude')]/following-sibling::span")
    audience_exclude_search_locator = (
        By.XPATH,
        "//h4[contains(text(), 'Audiences exclude')]/following::input[@type='text']")
    audience_exclude_warning_message_locator = (
        By.XPATH,
        "//h4[contains(text(), 'Audiences exclude')]/following::span[contains(text(), 'No result found')]")
    audience_exclude_cancel_button_locator = (
        By.XPATH,
        "//h4[contains(text(), 'Audiences exclude')]/following::button[contains(text(), 'CANCEL')]")
    contextual_keywords_locator = (By.XPATH, "(//label[contains(text(), 'Keywords')]/following-sibling::span)[2]")

    # 'Campaign purpose' locators
    campaign_purpose_section_locator = (
        By.XPATH, "//h6[contains(text(), 'Campaign purpose')]")
    campaign_purpose_warning_message_locator = (
        By.XPATH, "//label[contains(text(), 'Select one country')]")

    # 'Platforms, Telco & Devices'
    platforms_telco_devices_group_locator = (
        By.XPATH,
        "//h6[contains(text(), 'Platforms, Telco & Devices')]")
    ad_placement_type_app_locator = (By.ID, "ad-placement-type-1")
    ip_ranges_section_locator = (
        By.XPATH, "//span[contains(text(), 'IP addresses/ranges ')]")
    device_brands_section_locator = (
        By.XPATH, "//*[@data-target='#ac-js-device-brand-container']")
    device_brands_selection_locator = (
        By.XPATH,
        "//div[@id='js-device-brand-container']/descendant::span["
        "@class='mselect-selection__arrow']")
    device_models_selection_locator = (
        By.XPATH,
        "//div[@id='js-device-model-container']/descendant::span["
        "@class='mselect-selection__arrow']")

    # 'Deals & Packages' locators
    deals_packages_section_locator = (
        By.XPATH, "//h6[contains(text(), 'Deals & packages')]")
    package_locator = (By.ID, "package-id-37413")
    packages_include_only_selector = (
        By.XPATH, "//label[@for='campaignFormpackage_type374131_1']")
    ad_placement_positions_section_locator = (
        By.XPATH, "//*[@data-target='#ad-placement-positions-box']")
    private_marketplace_section_locator = (By.XPATH,
                                           "//span[@class='tab2-selection__rendered' and contains(text(), 'Private "
                                           "marketplace')]")
    private_marketplace_selection_locator = (
        By.XPATH, "//div[@id='ac-target-pmp']/descendant::span["
                  "@class='mselect-selection__arrow']")
    private_marketplace_only_checkbox = (By.XPATH, '//input[@data-qa="private-marketplace-only-radio"]')

    # 'Landings & Creatives' locators
    creative_set_selection_locator = (
        By.XPATH, "//span[contains(@title, 'creative sets')]")
    landing_and_creatives_group_locator = (
        By.XPATH, "//h6[contains(text(), 'Landing & Creatives')]")
    landing_and_creatives_navigation_locator = (
        By.XPATH, "//a[normalize-space()='Landing & Creatives']")
    ad_domain_field_locator = (By.ID, "select2-ad_domain-container")
    ad_domain_search_field_locator = (
        By.XPATH, "//input[@class='select2-search__field']")
    unavailable_creative_type_alert_locator = (
        By.XPATH, "//div[@class='bootbox-body']")
    app_input_field_locator = (By.XPATH,
                               "//input[@placeholder='Google Play Store ID (e.g. your.package.id)']")
    app_input_field2_locator = (
        By.XPATH,
        "//input[@placeholder='Adjust App ID (e.g. abcdef)']")
    call_input_field_locator = (
        By.XPATH,
        "//input[@placeholder='International phone number or short code (e.g. +123456789)']")
    ussd_input_field_locator = (
        By.XPATH, "//input[@placeholder='USSD code (e.g. *999*1#)']")
    landing_page_url_locator = (
        By.XPATH,
        "//input[@placeholder='Landing page URL (e.g. https://www.yoursite.com/?click_id={eucid})']")
    click_url_parameters_locator = (
        By.XPATH,
        "//span[contains(text(), 'Click URL parameters')]//parent::span[@tabindex='0']")
    add_utm_parameters_locator = (
        By.XPATH,
        "//input[@type='button' and @value='Add UTM parameters' ]")
    add_parameter_locator = (
        By.XPATH,
        "//input[@type='button' and @value='Add parameter' ]")
    key_locator = (
        By.XPATH, '//input[@type="text" and @placeholder="Key" ]')
    value_locator = (
        By.XPATH, '//input[@type="text" and @placeholder="Value" ]')
    creative_url_toggle = (
        By.XPATH,
        '//i[contains(@class, "js-campaign-creative-url-toggle")]')
    creative_click_url_cp = (
        By.XPATH, '(//i[contains(@class, "fas fa-retweet")])[1]')
    click_url_per_creative_locator = (
        By.XPATH, '(//i[@class="fas fa-chevron-right mr-2"])[1]')
    creative_toggle_icon_locator = (
        By.XPATH,
        '(//i[@class ="fas fa-external-link-square-alt pull-right js-campaign-creative-url-toggle mr-2"])[1]')
    impression_per_creative_locator = (
        By.XPATH, '(//i[@class="fas fa-chevron-right mr-2"])[2]')
    impression_add_more_button_locator = (
        By.XPATH,
        '(//button[@class="btn btn-sm btn-primary add-more" and @type="button"])[1]')
    pixel_input_locator = (
        By.XPATH, '//textarea[@class= "ace_text-input"]')
    pixel_get_input_locator = (
        By.XPATH, '//span[@class="ace_text ace_xml"]')
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    creatives_bids_locator = (
        By.XPATH,
        "//div[@class='creatives-preview-container js-creatives-preview-container']//input[contains(@name, '[bid_currency]')]")

    # 'Form navigation' locators
    button_group_locator = (By.XPATH, "//a[contains(text(), 'Button')]")

    # 'Campaign Form General' locator
    contextual_targeting_app_site_section = (By.XPATH, "//div[@data-target='#contextual-data-target']")
    modal_search_field_locator = (By.XPATH,
                                  "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
    credit_limit_exceeded_modal = (By.XPATH, "//div[@class='modal-dialog']//div[@class='modal-content']")
    # [End] locators

    # [Start] label names
    date_label = "Date"
    contextual_targeting_label = "Contextual targeting"
    selected_creative_sets_selection_label = "Selected creative sets"
    only_radio_button_label = "Only"
    minimum_impressions_per_placement_to_learn_field_label = "Minimum impressions per placement to learn:"
    minimum_spend_per_placement_to_learn_field_label = "Minimum spend per placement to learn:"
    # [End] label names

    # [Start] Attribute values
    brand_safety_checkbox = 'js-siteCategoriesBrandSafety-id-0'
    time_and_day_schedule = "//td[normalize-space()='{}']"
    platform_name = "//div[@class='campaign-platform-icon' and @data-type='{}']"
    campaign_goal = "//div[@id='type-{}']"
    type_field_id = "select2-js-campaign-type-container"
    campaign_field_id = "name"
    bid_cpm_field_id = "bid_currency"
    daily_budget_field_id = "budget_daily_currency"
    total_budget_field_id = "budget_total_currency"
    city_dropdown_id = "js-city-select"
    state_dropdown_id = "js-state-select"
    ad_placement_type_section_id = "ad-placement-type-box"
    sim_amount_section_id = "sim-amount-box"
    device_connection_section_id = "device-connection-box"
    exchanges_section_id = "exchanges"
    brand_safety_section_id = "js-siteCategoriesBrandSafety-id-0"
    contextual_section_id = "js-siteCategoriesContextual-id-0"
    ad_placement_positions_section_id = "ad-placement-positions-box"
    packages_section_id = "packages-box"
    network_connection_section_id = "network-connection-box"
    impression_field_class = "txtfield form-control impressions"
    impression_click_field_class = "txtfield form-control clicks"
    capping_amount_field_class = "txtfield form-control capping-amount"
    auto_optimisation_section_id = "secondary-auto-optimisation"
    click_url_field_id = "js-campaign-click-url"
    ad_domain_field_id = "select2-ad_domain-container"
    campaign_purpose_field_id = "select2-js-campaign-purpose-container"
    primary_operator_field_id = "select2-js-operators-container-6-container"
    campaign_goal_id = "goal-type-value"
    primary_objective_attribute_value = "primary-goal-value"
    secondary_objective_attribute_value = "secondary-goal-value"
    primary_objective_input_attribute = 'primary-goal-input'
    secondary_objective_input_attribute = 'secondary-goal-input'
    goal_attribute = 'data-goal'
    private_marketplace_dropdown_id = 'private_marketplace'
    package_checkbox_locator = "//label[contains(text(), '{}')]//..//input"
    packages_include_only_locator = "//input[@data-qa='js-package-type-id-1-{}']"
    # [End] Attribute values

    # [Start] Options
    placement_type_app = "App"
    placement_type_site = "Site"
    # [End] Options
