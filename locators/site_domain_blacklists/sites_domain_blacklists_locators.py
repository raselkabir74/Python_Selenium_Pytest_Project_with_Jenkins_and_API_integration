from selenium.webdriver.common.by import By


class SiteDomainBlacklistsLocators:
    # [START] data-qa attribute values
    title_label_data_qa = 'domain-th'
    new_domain_btn = "add-new-domain-btn"
    domain_data_qa = "domain-label"
    cancel_btn = "cancel-btn"
    list_first_domain_3_dot_locator = (By.XPATH, '(//td[@class="dropdown actions"]//a)[1]')
    list_first_domain_edit_locator = (By.XPATH, '(//a[@title="Edit"])[1]')
    # [END] data-qa attribute values
