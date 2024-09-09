from selenium.webdriver.common.by import By


class CompaniesGroupsLocators:
    # [START] data-qa attribute values
    title_th_data_qa = "title-th"
    companies_group_title_data_qa = "companies-group-title-label"
    new_cg_btn_data_qa = "add-new-companies-groups-btn"
    cancel_btn = "cancel-btn"
    list_first_item = (By.XPATH, "(//a[@class='text-title'])[1]")
    # [END] data-qa attribute values
