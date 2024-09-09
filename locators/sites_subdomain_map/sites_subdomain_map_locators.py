from selenium.webdriver.common.by import By


class SiteSubdomainMapLocators:
    # [START] data-qa attribute values
    subdomain_label_data_qa = 'subdomain-th'
    new_site_subdomain_btn = "add-new-site-subdomain-map-btn"
    subdomain_form_label_data_qa = "subdomain-label"
    cancel_btn = "cancel-btn"
    list_first_domain_3_dot_locator = (By.XPATH, '(//td[@class="text-center dropdown actions"]//a)[1]')
    list_first_domain_edit_locator = (By.XPATH, '(//a[@title="Edit"])[1]')
    # [END] data-qa attribute values
