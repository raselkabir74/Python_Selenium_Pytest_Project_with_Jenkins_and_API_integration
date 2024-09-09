from pages.base_page import BasePage
from locators.brand_safety.brand_safety_form_locators import \
    BrandSafetyFormLocators
import os

keyword_information = {}


class DashboardBrandSafetyForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_and_save_keyword_data(self, brand_safety):
        self.set_value_into_element(
            BrandSafetyFormLocators.title_field_locator,
            brand_safety['title'])
        self.check_uncheck_specific_checkbox(BrandSafetyFormLocators.context_checkboxes_label,
                                             do_check=bool(brand_safety['find_url']), value="1")
        self.check_uncheck_specific_checkbox(BrandSafetyFormLocators.context_checkboxes_label,
                                             do_check=bool(brand_safety['find_content']), value="2")
        self.set_value_into_element(
            BrandSafetyFormLocators.keywords_upload_locator,
            os.path.join(os.getcwd(),
                         "assets/brand_safety/keywords.csv"))
        self.select_dropdown_value(BrandSafetyFormLocators.default_data_qa, brand_safety['default'])
        self.click_on_element(
            BrandSafetyFormLocators.save_button_locator)

    def get_keywords_information(self):
        global keyword_information
        keyword_information['title'] = self.get_element_text(
            BrandSafetyFormLocators.title_field_locator,
            input_tag=True)
        keyword_information['find_url'] = self.get_checkbox_status(BrandSafetyFormLocators.context_checkboxes_label,
                                                                   value="1")
        keyword_information['find_content'] = self.get_checkbox_status(BrandSafetyFormLocators.context_checkboxes_label,
                                                                       value="2")
        keyword_information[
            'default'] = self.get_text_or_value_from_selected_option(
            BrandSafetyFormLocators.default_data_qa)
        keyword_information[
            'status'] = self.get_text_or_value_from_selected_option(
            BrandSafetyFormLocators.status_data_qa)
        return keyword_information

    def cancel_form(self):
        self.click_on_element(
            BrandSafetyFormLocators.cancel_link_locator)
