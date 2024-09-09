from selenium.webdriver.common.by import By


class CreativeListLocators:
    # [Start] locators
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    creative_search_field_locator = (By.ID, "filter_name")
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    specific_creative_id_locator = "//a[contains(text(), '{}')]"
    creative_id_locator = "//a[contains(text(), '{}') and contains(@data-qa, 'creative-title')]"
    grid_first_three_dot_icon_locator = (By.XPATH, "(//*[contains(@id, 'action-')])[1]")
    creative_sets_titles_list_locator = (By.XPATH, "//a[contains(@data-qa, 'creative-set-title-')]")
    creative_set_title_locator = 'creative-set-title-{}'
    # [End] locators

    # [Start] label names
    edit_label = "Edit"
    delete_label = "Delete"
    title_column = "Title"
    format_column = "Format"
    dimensions_column = "Dimensions"
    status_column = "Status"
    creative_count = "Creative count"
    # [End] label names

    # [Start] Attribute values
    three_dot_of_creative_xpath = "//a[contains(text(), '{}')]//..//..//..//i[@class='fas fa-ellipsis-v']"
    first_row_image_preview_locator = "//div[@id='creatives-table_wrapper']//img[@src]"
    creatives_table_wrapper_div_id = "creatives-table_wrapper"
    creatives_set_table_wrapper_div_id = "creative-sets-table_wrapper"
    # [End] Attribute values

    # [Start] data-qa attribute values
    btn_create_data_qa = "add-creative-set-btn"
    add_creative_btn_data_qa = "add-creative-btn"
    info_message_data_qa = "alert"
    # [End] data-qa attribute values
