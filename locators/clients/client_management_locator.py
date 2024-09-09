from selenium.webdriver.common.by import By


class ClientManagementLocator:
    # [Start] Locators
    save_btn_locator = (By.XPATH, "//input[@class='btn btn-primary success btn-block save-btn' and @value='Save']")
    main_margin_changes_modal_title_locator = (
        By.XPATH, "//div[@class='modal-content']//*[text()='Changing the main margin']")
    modal_message_locator = (By.XPATH, "//div[@class='modal-body']//ul/li/b")
    main_margin_changes_modal_confirm_btn_locator = (
        By.XPATH, "//div[@class='modal-footer']//button[@data-bb-handler='confirm']")
    margin_input_locator = (By.XPATH, "//input[@id='margin']")
    error_message_locator = (By.XPATH, "//div[@class='errors']//li")
    # [End] Locators

    # [Start] Attribute values
    client_dropdown_id = 'select2-client_id-container'
    campaign_dropdown_id = 'select2-campaign_id-container'
    # [End] Attribute values

    # [Start] Label names
    select_client_label = 'Select client'
    select_campaign_label = 'Select campaign (optional)'
    # [End] Label names

    # [Start] data-qa attribute values
    success_message_data_qa = 'alert'
    # [End] data-qa attribute values
