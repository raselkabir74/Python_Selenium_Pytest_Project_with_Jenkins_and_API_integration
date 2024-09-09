from selenium.webdriver.common.by import By


class BulkUserAddFormLocators:
    # [START] data-qa attribute values
    send_invitation_button_data_qa = "invitation-btn"
    # [END] data-qa attribute values

    # [Start] locators
    email_input_locator = (By.XPATH,
                           "//label[normalize-space()='E-mail address(es)']/following-sibling::div/div[@class='bootstrap-tagsinput']/input")
    # [End] locators

    # [Start] labels
    agency_client_account_label = 'Agency/Client account'
    # [End] labels
