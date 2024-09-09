from selenium.webdriver.common.by import By


class PackageFormLocators:
    # [Start] labels
    csv_upload_label = "CSV upload"
    auction_type_label = "Auction type"
    # [End] labels

    # [START] data-qa attribute values
    package_field_data_qa = "package-name-input"
    country_data_qa = "country-select"
    exchange_data_qa = "exchange-select"
    environment_data_qa = "environment-select"
    user_data_qa = "users-select"
    auction_type_data_qa = "auction-type-select"
    tags_data_qa = "tags-select"
    save_button_locator_data_qa = "save-btn"
    cancel_button_locator_data_qa = "cancel-btn"
    # [END] data-qa attribute values

    # [Start] Attribute values
    selected_site_list_id = "js-selected-site-list"
    # [End] Attribute values
