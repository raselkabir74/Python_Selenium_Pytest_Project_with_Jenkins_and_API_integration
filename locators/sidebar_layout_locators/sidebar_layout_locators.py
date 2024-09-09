from selenium.webdriver.common.by import By


class SidebarLayoutLocators:
    # [START] data-qa attribute values
    title_data_qa = 'title-th'
    new_layout_btn = "add-new-layout-btn"
    title_form_label_data_qa = "title-label"
    cancel_btn = "cancel-btn"
    list_first_domain_3_dot_locator = (By.XPATH, '(//td[@class="dropdown actions"]//a)[1]')
    list_first_domain_edit_locator = (By.XPATH, '(//a[@title="Edit"])[1]')
    # [END] data-qa attribute values
