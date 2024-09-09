from selenium.webdriver.common.by import By


class CampaignViewLocator:
    # [Start] Locators
    campaign_view_three_dot_icon = (By.XPATH,
                                    "//*[@class='dropdown-toggle']//i[@class='fas fa-ellipsis-v']")
    campaign_view_edit_icon = (
        By.XPATH, "//*[@class='dropdown show']//a[@title='Edit']")
    campaign_view_delete_icon = (
        By.XPATH, "//*[@class='dropdown show']//a[@title='Delete']")
    campaign_view_duplicate_icon = (By.XPATH,
                                    "//*[@class='dropdown show']//a[@title='Duplicate campaign']")
    campaign_view_approve_icon = (
        By.XPATH, "//*[@class='dropdown show']//a[@title='Approve']")
    confirm_button_alert_locator = (
        By.XPATH, "//button[@data-bb-handler='confirm']")
    campaign_list_navigation = (By.XPATH,
                                "//*[@class='back-to-list']//*[@class='fas fa-chevron-left']")
    campaign_settings_navigation = "(//dfn[@class='sidebar-tooltip']//*[contains(text(),'Campaign settings')])"
    success_message_locator = (By.XPATH,
                               "//div[@class='alert alert-success alert-dismissible fade show']")
    # [End] Locators
