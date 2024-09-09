from selenium.webdriver.common.by import By


class SiteCategoriesLocators:
    # [START] data-qa attribute values
    title_label_data_qa = 'title-th'
    successful_message_data_qa = 'alert'
    new_app_sites_btn = (By.XPATH, "//a[contains(normalize-space(), 'New app/site category')]")
    iab_categories_data_qa = "IAB-categories-label"
    selected_iab_categories_data_qa = "selected-iab-categories-label"
    cancel_btn = (By.XPATH, "//a[contains(normalize-space(), 'CANCEL')]")
    list_first_site_locator = (By.XPATH, "(//td[@class='sorting_1']//a)[1]")
    # [END] data-qa attribute values

    # [Start] locators
    category_search_field_locator = (By.ID, "filter_name")
    three_dot_of_category_locator = "action-{}"
    category_edit_locator = "//*[@class='dropdown actions align-icon show']//a[@title='Edit']"
    category_delete_locator = "//*[@class='dropdown actions align-icon show']//a[@title='Delete']"
    confirm_delete_btn_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    app_sites_count_locator = (By.XPATH, "//td[@class='ad-pad text-center'][1]")
    title_input_locator = (By.XPATH, "//input[@name='title']")
    save_btn_locator = (By.XPATH, "//button[@type='submit']")
    # [End] locators

    # [Start] labels
    csv_upload_label = "CSV upload"
    # [End] labels
