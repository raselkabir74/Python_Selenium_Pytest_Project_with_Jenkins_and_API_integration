from selenium.webdriver.common.by import By


class Branding:
    # [START] data-qa attribute values
    branding_data_qa = "branding-h3"
    branding_btn_data_qa = "add-branding-btn"
    page_title_data_qa = "page-title-label"
    name_data_qa = 'name-label'
    cancel_btn = "cancel-btn"
    list_first_item_3_dot_locator = (By.XPATH, '(//a[@class="dropdown-toggle hide-arrow"])[1]')
    list_first_item_edit_locator = (By.XPATH, '(//a[@class="dropdown-item"])[1]')
    # [END] data-qa attribute values
