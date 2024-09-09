from selenium.webdriver.common.by import By


class AudienceFormLocators:
    # [Start] locators
    save_button_locator = (
        By.XPATH, "//button[@data-qa='audience-save-btn']")
    cancel_button_locator = (
        By.XPATH, "//button[@data-qa='audience-cancel-btn']")
    add_button_locator = (By.XPATH, "//button[@data-qa='audience-list-add-btn']")
    selected_first_item_locator = (By.XPATH,
                                   "//select[@data-qa='audience-list-selected']//option")
    csv_file_upload_locator = (By.XPATH, "//input[@data-qa='audience-file-upload-btn']")
    remove_if_url_contains_field_locator = (By.XPATH,
                                            "//label[normalize-space()='Remove if URL contains:']/..//input")
    nav_button_locator = (By.XPATH,
                          "//li[@data-qa='form-nav-step-Buttons']//a")
    autos_vehicles_checkbox_locator = (By.XPATH,
                                       "//span[text()='Autos & Vehicles']/preceding-sibling::input[@type='checkbox']")
    back_to_list_locator = (By.XPATH, "//div[@class='back-to-list']//i[@class='fas fa-chevron-left']")
    # [End] locators

    # [Start] Label names
    audience_list_field_name = "Audience list"
    # [End] Label names

    # [Start] Attribute values
    name_field_data_qa = "audience-name-input"
    description_field_data_qa = "audience-description-input"
    type_field_data_qa = "audience-type-select"
    country_field_data_qa = "country-select"
    country_form_field_data_qa = "country-select"
    users_field_data_qa = "audience-user-select"
    date_field_data_qa = "date-range-input"
    rule_field_data_qa = "audience-rule-select"
    method_field_data_qa = "audience-geolocation-select"
    user_validity_field_data_qa = "audience-user-validity-input"
    exchange_field_data_qa = "exchange-select"
    type_form_field_data_qa = "type-select"
    generate_insights_report_field_data_qa = "generate-insight-form-select"
    audience_field_name_data_qa = "audience-name-input"
    description_data_qa = "audience-description-input"
    type_container_id = "select2-js-type-container"
    country_container_id = "select2-js-country-container"
    verticals_id = "verticals"
    form_control_class = "form-control"
    user_validity_minutes_id = "user_validity_minutes"
    select2_validity_type_container_id = "select2-validity_type-container"
    select2_generate_insight_form_container_id = "select2-generate_insight_form-container"
    amount_locations_id = "amount-locations"
    select2_selection_choice_class = "select2-selection__choice"
    # [End] Attribute values
