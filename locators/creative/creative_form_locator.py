from selenium.webdriver.common.by import By


class CreativeFormLocators:
    # [Start] locators
    percentage_wait_locator = (By.XPATH,
                               '//div[@class="uppy-ProgressBar-percentage" and text()="100"]')
    warning_icon_locator = (By.XPATH,
                            '//i[@class="fas fa-exclamation-triangle text-warning js-tag-error"]')
    rm_file_upload_locator = (By.ID, "asset-file-upload")
    rm_image_selection_locator = (
        By.XPATH, '(//img[@class="mr-1" and @alt="Image"])[1]')
    dimensions_locator = (By.XPATH, "//span[@class='text-success']/..")
    dimensions_locator_js_tag = (By.XPATH, '//p[@class="clearfix"]')
    icon_image_dimension_locator = (
        By.XPATH, "//p[text()='Icon']/following-sibling::p[2]")
    cover_image_dimension_locator = (
        By.XPATH, "//p[text()='Cover image']/following-sibling::p[2]")
    cover_alt_image_dimension_locator = (
        By.XPATH,
        "//p[text()='Cover alt image']/following-sibling::p[2]")
    rm_tempelate_selection_locator = (By.XPATH,
                                      '//label[@class="rm-image-title" and text()="Shake & brake"]')
    rm_tempelate_selection_locator2 = (
        By.XPATH,
        '//label[@class="rm-image-title" and text()="Dancing 3D"]')
    creative_set_title = (
        By.XPATH, "//a[contains(text(), 'Creative sets')]")
    creative_title = (
        By.XPATH, "(//h3//a[contains(text(), 'Creative')])[2]")
    list_first_iteam_locator = (By.XPATH,
                                "(//a[contains(@data-qa, 'creative-title-') or contains(@data-qa, 'creative-set-title-')])[1]")
    confirm_button_locator = (
        By.XPATH,
        "//button[contains(@class, 'btn btn-success') and contains(@data-bb-handler, 'confirm')]")
    js_tag_width_input = (By.ID, 'width-1')
    js_tag_height_input = (By.ID, 'height-1')
    creative_sets_breadcrumb_locator = (By.XPATH, "//a[contains(text(), 'Creative sets')]")
    multi_rm_creative_add_btn = (By.XPATH, '//span[contains(text(), "Add Creative")]')
    creative_set_message_locator = (By.XPATH, "//span[contains(text(), 'Creative set created successfully')]")
    loading_spinner_locator = (By.XPATH, "//span[contains(text(), 'Loading')]")
    # [End] locators

    # [Start] label names
    save_button_label = "Save"
    star_rating_label = "Star rating"
    advertiser_label = "Advertiser"
    title_headline_label = "Title / headline"
    display_url_2_label = "Display URL"
    description_label = "Description"
    headline_label = "Headline"
    click_url_label = "Click URL"
    dimensions_label = "Dimensions"
    playback_checkbox_label = "Playback"
    viewability_tracking_method_checkbox_label = "Viewability tracking method"
    skip_after_seconds_checkbox_label = "Skip after seconds"
    third_party_verification_checkbox_label = "3rd party verification tool (IAS, DV, MOAT wrapper URL)"
    call_to_action_label = "Call to action text"
    # [End] label names

    # [Start] Attribute values
    title_name = "title"
    image_preview_locator = "//p//img[@src]"
    icon_image_preview_locator = "//p[text()='Icon']/following-sibling::p[1]//img[@src]"
    cover_image_preview_locator = "//p[text()='Cover image']/following-sibling::p[1]//img[@src]"
    cover_alt_image_preview_locator = "//p[text()='Cover alt image']/following-sibling::p[1]//img[@src]"
    source_xpath = "//div[@data-qa='asset-0']"
    target_xpath_1 = "//div[@data-qa='image_frame-2']"
    target_xpath_2nd_rm_1 = "(//div[@data-qa='image_frame-2'])[2]"
    target_xpath = "//div[@data-qa='image_frame-1']"
    target_xpath_2nd_rm = "(//div[@data-qa='image_frame-1'])[2]"
    size_xpath = "//*[@data-qa='size-{}-select']//span"
    # [End] Attribute values

    # [Start] data-qa attributes
    file_upload_data_qa = "upload-file-input-{}"
    cancel_button_data_qa = "add-creative-cancel-btn"
    creative_format_data_qa = "creative-format-select"
    creative_list_three_dot_data_qa = "item-action-{}"
    preserve_button_data_qa = "item-action-Preserve-{}"
    unpreserve_button_data_qa = "item-action-Unpreserve-{}"
    copy_to_another_button_data_qa = "item-action-Copy to another account-{}"
    duplicate_button_data_qa = "item-action-Duplicate-{}"
    frame_count_data_qa = "frame-count-select"
    dimensions_rm_data_qa = "dimension-select"
    mass_file_upload_data_qa = "mass-upload-btn"
    title_data_qa = "js-creativeset-title-input"
    creative_format_select_data_qa = "creative-format-select"
    format_select_data_qa = "js-creative-subtype-select"
    continue_button_data_qa = "add-creative-continue-btn"
    creative_set_save_data_qa = "creative-set-save-btn"
    likes_data_qa = "likes-input"
    downloads_data_qa = "downloads-input"
    price_data_qa = "price-input"
    sale_price_data_qa = "sale-price-input"
    phone_data_qa = "phone-input"
    address_data_qa = "address-input"
    additional_description_data_qa = "additional-description-input"
    display_url_data_qa = "display-url-input"
    see_more_url_data_qa = "see-more-url-input"
    message_data_qa = "message-textarea"
    rm_size_data_qa = "size-1-select"
    rm_2nd_size_data_qa = "size-2-select"
    rm_size_dimension_data_qa = "2-select"
    select_template_data_qa = "creative-1-templates-btn"
    select_2nd_template_data_qa = "creative-2-templates-btn"
    select_Shake_brake_template_checkbox_data_qa = "templates-1-template-12-check"
    select_pixel_page_template_checkbox_data_qa = "templates-2-template-27-check"
    template_btn_data_qa = "template-modal-save-btn"
    rm_file_upload_data_qa = "file-upload-input"
    creative_btn_data_qa = "creative_save-btn"
    creative_set_title_data_qa = "creative_set_name-input"
    creative_set = (By.XPATH, '//a[contains(text(), "Creative sets")]')
    creative_set_save_button_data_qa = "creative_set_save-btn"
    template_preview_data_qa = "creative-template-preview-12-btn"
    desktop_radio_btn_data_qa = "desktop_preview-radio"
    real_size_btn_data_qa = "real_size_preview-radio"
    remove_template_btn_data_qa = "remove-previewed-template-1-12-btn"
    remove_btn_data_qa = "dialog-submit-btn"
    # [End] data-qa attributes
