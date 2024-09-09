import os
import time

from selenium.webdriver.common.by import By

from locators.creative.creative_form_locator import CreativeFormLocators
from locators.creative.creative_list_locator import CreativeListLocators
from pages.base_page import BasePage

creative_information_from_form_page = {}


class DspDashboardCreativeForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_info_into_add_creative_set_form(self, creative_data, creatives_format=True):
        self.set_value_into_specific_input_field(CreativeFormLocators.creative_set_title_data_qa, creative_data[
            'general_information']['title'])
        self.click_on_specific_radio_button(creative_data['general_information'][
                                                'creative_format'])
        if creatives_format:
            self.click_on_specific_radio_button(creative_data['general_information']['format'])
        self.click_on_element(CreativeFormLocators.creative_set_save_button_data_qa)

    def click_on_specific_radio_button(self, button_value,
                                       script_executor_click=False, locator_to_be_appeared=None):
        button_locator = f"//*[@data-qa='{button_value}-radio']"
        if script_executor_click:
            self.click_element_execute_script(button_locator)
        else:
            self.click_on_element(button_locator,
                                  locator_initialization=True,
                                  locator_to_be_appeared=locator_to_be_appeared)

    def provide_info_into_add_creative_rm_banner_form_new(self):
        self.wait_for_presence_of_element(
            CreativeFormLocators.rm_file_upload_data_qa).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/320x480.png'))
        self.click_on_element(CreativeFormLocators.rm_size_data_qa)
        self.click_on_element(CreativeFormLocators.rm_size_dimension_data_qa)
        self.click_on_element(CreativeFormLocators.select_template_data_qa)
        self.click_on_element(CreativeFormLocators.select_Shake_brake_template_checkbox_data_qa)
        self.click_on_element(CreativeFormLocators.template_btn_data_qa)

    def provide_info_into_add_creative_file_banner_form(self,
                                                        creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/600x600.png'))
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=60)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def provide_info_into_add_creative_javascript_tag_banner_form(self,
                                                                  creative_data):
        self.click_on_element(
            CreativeFormLocators.mass_file_upload_data_qa)
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/javascript_tag_banner_300x250.zip'))
        self.wait_for_presence_of_element(
            CreativeFormLocators.percentage_wait_locator)
        self.wait_for_presence_of_element(
            CreativeFormLocators.warning_icon_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.set_value_into_element(
            CreativeFormLocators.js_tag_height_input,
            creative_data['general_information'][
                "height"])
        self.set_value_into_element(
            CreativeFormLocators.js_tag_width_input,
            creative_data['general_information'][
                "width"])

        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        if 'http://rtb.local/admin' in self.driver.current_url:
            self.click_on_element(CreativeListLocators.grid_first_three_dot_icon_locator)

    def get_banner_creative_information_from_form_page(self,
                                                       creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information']['format']
        creative_information_from_form_page['general_information'][
            'preview'] = str(self.is_image_present(
            CreativeFormLocators.image_preview_locator))
        creative_information_from_form_page['general_information'][
            'dimensions'] = str(self.get_element_text(
            CreativeFormLocators.dimensions_locator)).strip()
        return creative_information_from_form_page

    def get_javascript_tag_banner_creative_information_from_form_page(self,
                                                                      creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information']['format']
        creative_information_from_form_page['general_information'][
            'width'] = \
            creative_data['general_information'][
                'width']
        creative_information_from_form_page['general_information'][
            'height'] = \
            creative_data['general_information'][
                'height']
        if 'http://rtb.local/admin' in self.driver.current_url:
            creative_information_from_form_page['general_information']['preview'] = \
                creative_data['general_information']['preview']
        else:
            creative_information_from_form_page['general_information'][
                'preview'] = str(self.is_image_present(
                CreativeFormLocators.image_preview_locator))
        if 'http://rtb.local/admin' in self.driver.current_url:
            creative_information_from_form_page['general_information']['dimensions'] = \
                creative_data['general_information']['dimensions']
        else:
            creative_information_from_form_page['general_information'][
                'dimensions'] = str(self.get_element_text(
                CreativeFormLocators.dimensions_locator_js_tag)).strip()
        return creative_information_from_form_page

    def get_rich_media_banner_creative_information_from_form_page(self, creative_data, creative_id):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = \
            creative_data['general_information'][
                'title']
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information']['format']
        time.sleep(1)
        creative_information_from_form_page['general_information'][
            'dimensions'] = self.get_element_text(
            CreativeFormLocators.size_xpath.format(creative_id), locator_initialization=True)
        creative_information_from_form_page['general_information'][
            'template'] = creative_data['general_information'][
            'template']
        return creative_information_from_form_page

    def provide_info_into_add_creative_native_form(self, creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format(1)).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/128x128.png'))
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("2")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/1200x627.png'))
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("3")). \
            send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/600x600.png'))
        self.set_value_into_specific_input_field(CreativeFormLocators.title_headline_label,
                                                 creative_data['general_information']['title_headline'])
        self.set_value_into_specific_input_field(CreativeFormLocators.description_label,
                                                 creative_data['general_information']['Description'], is_textarea=True)
        self.set_value_into_specific_input_field(CreativeFormLocators.call_to_action_label,
                                                 creative_data['general_information'][
                                                     'call_to_action_text'])
        self.set_value_into_specific_input_field(CreativeFormLocators.advertiser_label,
                                                 creative_data['general_information']['advertiser'])
        self.set_value_into_specific_input_field(CreativeFormLocators.likes_data_qa,
                                                 creative_data['general_information']['likes'])
        self.set_value_into_specific_input_field(CreativeFormLocators.downloads_data_qa,
                                                 creative_data['general_information']['downloads'])
        self.set_value_into_specific_input_field(CreativeFormLocators.price_data_qa,
                                                 creative_data['general_information']['price'])
        self.set_value_into_specific_input_field(CreativeFormLocators.sale_price_data_qa,
                                                 creative_data['general_information']['sale_price'])
        self.set_value_into_specific_input_field(CreativeFormLocators.phone_data_qa,
                                                 creative_data['general_information']['phone'])
        self.set_value_into_specific_input_field(CreativeFormLocators.address_data_qa,
                                                 creative_data['general_information']['address'])
        self.set_value_into_specific_input_field(CreativeFormLocators.star_rating_label,
                                                 creative_data['general_information']['star_rating'])
        self.set_value_into_specific_input_field(CreativeFormLocators.additional_description_data_qa,
                                                 creative_data['general_information'][
                                                     'additional_description'])
        self.set_value_into_specific_input_field(CreativeFormLocators.display_url_data_qa,
                                                 creative_data['general_information']['display_url'])
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=60)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def provide_info_into_add_creative_native_video_form(self,
                                                         creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/video.mp4'))
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("2")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/128x128.png'))
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("3")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/1200x627.png'))
        self.set_value_into_specific_input_field(CreativeFormLocators.title_headline_label,
                                                 creative_data['general_information']['title_headline'])
        self.set_value_into_specific_input_field(CreativeFormLocators.description_label,
                                                 creative_data['general_information']['Description'], is_textarea=True)
        self.set_value_into_specific_input_field(CreativeFormLocators.call_to_action_label,
                                                 creative_data['general_information'][
                                                     'call_to_action_text'])
        self.set_value_into_specific_input_field(CreativeFormLocators.advertiser_label,
                                                 creative_data['general_information']['advertiser'])
        self.set_value_into_specific_input_field(CreativeFormLocators.price_data_qa,
                                                 creative_data['general_information']['price'])
        self.set_value_into_specific_input_field(CreativeFormLocators.star_rating_label,
                                                 creative_data['general_information']['star_rating'])
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=60)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def get_native_creative_information_from_form_page(self,
                                                       creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'title_headline'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.title_headline_label)
        creative_information_from_form_page['general_information'][
            'Description'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.description_label, is_textarea=True)
        creative_information_from_form_page['general_information'][
            'call_to_action_text'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.call_to_action_label)
        creative_information_from_form_page['general_information'][
            'advertiser'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.advertiser_label)
        creative_information_from_form_page['general_information'][
            'likes'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.likes_data_qa)
        creative_information_from_form_page['general_information'][
            'downloads'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.downloads_data_qa)
        creative_information_from_form_page['general_information'][
            'price'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.price_data_qa)
        creative_information_from_form_page['general_information'][
            'sale_price'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.sale_price_data_qa)
        creative_information_from_form_page['general_information'][
            'phone'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.phone_data_qa)
        creative_information_from_form_page['general_information'][
            'address'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.address_data_qa)
        creative_information_from_form_page['general_information'][
            'star_rating'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.star_rating_label)
        creative_information_from_form_page['general_information'][
            'additional_description'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.additional_description_data_qa)
        creative_information_from_form_page['general_information'][
            'display_url'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.display_url_data_qa)

        creative_information_from_form_page['general_information'][
            'icon_preview'] = str(self.is_image_present(
            CreativeFormLocators.icon_image_preview_locator))
        creative_information_from_form_page['general_information'][
            'cover_preview'] = str(self.is_image_present(
            CreativeFormLocators.cover_image_preview_locator))
        creative_information_from_form_page['general_information'][
            'cover_alt_image_preview'] = str(
            self.is_image_present(
                CreativeFormLocators.cover_alt_image_preview_locator))

        creative_information_from_form_page['general_information'][
            'icon_dimension'] = str(self.get_element_text(
            CreativeFormLocators.icon_image_dimension_locator)).strip()
        creative_information_from_form_page['general_information'][
            'cover_dimension'] = str(self.get_element_text(
            CreativeFormLocators.cover_image_dimension_locator)).strip()
        creative_information_from_form_page['general_information'][
            'cover_alt_image_dimension'] = str(
            self.get_element_text(
                CreativeFormLocators.cover_alt_image_dimension_locator)).strip()
        return creative_information_from_form_page

    def get_native_video_creative_information_from_form_page(self,
                                                             creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information']['format']
        creative_information_from_form_page['general_information'][
            'title_headline'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.title_headline_label)
        creative_information_from_form_page['general_information'][
            'Description'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.description_label, is_textarea=True)
        creative_information_from_form_page['general_information'][
            'call_to_action_text'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.call_to_action_label)
        creative_information_from_form_page['general_information'][
            'advertiser'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.advertiser_label)
        creative_information_from_form_page['general_information'][
            'price'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.price_data_qa)
        creative_information_from_form_page['general_information'][
            'star_rating'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.star_rating_label)
        creative_information_from_form_page['general_information'][
            'icon_preview'] = str(self.is_image_present(
            CreativeFormLocators.icon_image_preview_locator))
        creative_information_from_form_page['general_information'][
            'cover_preview'] = str(self.is_image_present(
            CreativeFormLocators.cover_image_preview_locator))
        creative_information_from_form_page['general_information'][
            'icon_dimension'] = str(self.get_element_text(
            CreativeFormLocators.icon_image_dimension_locator)).strip()
        creative_information_from_form_page['general_information'][
            'cover_dimension'] = str(self.get_element_text(
            CreativeFormLocators.cover_image_dimension_locator)).strip()
        return creative_information_from_form_page

    def get_native_creative_information_from_form_page_for_copy(self,
                                                                creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'title_headline'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.title_headline_label)
        creative_information_from_form_page['general_information'][
            'Description'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.description_label, is_textarea=True)
        creative_information_from_form_page['general_information'][
            'call_to_action_text'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.call_to_action_label)
        creative_information_from_form_page['general_information'][
            'advertiser'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.advertiser_label)
        creative_information_from_form_page['general_information'][
            'likes'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.likes_data_qa)
        creative_information_from_form_page['general_information'][
            'downloads'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.downloads_data_qa)
        creative_information_from_form_page['general_information'][
            'price'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.price_data_qa)
        creative_information_from_form_page['general_information'][
            'sale_price'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.sale_price_data_qa)
        creative_information_from_form_page['general_information'][
            'phone'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.phone_data_qa)
        creative_information_from_form_page['general_information'][
            'address'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.address_data_qa)
        creative_information_from_form_page['general_information'][
            'star_rating'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.star_rating_label)
        creative_information_from_form_page['general_information'][
            'additional_description'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.additional_description_data_qa)
        creative_information_from_form_page['general_information'][
            'display_url'] = \
            self.get_value_from_specific_input_field(CreativeFormLocators.display_url_data_qa)

        creative_information_from_form_page['general_information'][
            'icon_preview'] = str(self.is_image_present(
            CreativeFormLocators.icon_image_preview_locator))
        creative_information_from_form_page['general_information'][
            'cover_preview'] = str(self.is_image_present(
            CreativeFormLocators.cover_image_preview_locator))
        creative_information_from_form_page['general_information'][
            'icon_dimension'] = str(self.get_element_text(
            CreativeFormLocators.icon_image_dimension_locator)).strip()
        creative_information_from_form_page['general_information'][
            'cover_dimension'] = str(self.get_element_text(
            CreativeFormLocators.cover_image_dimension_locator)).strip()
        return creative_information_from_form_page

    def provide_info_into_add_creative_engagement_form(self, creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/600x600.png'))
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=60)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def get_engagement_creative_information_from_form_page(self,
                                                           creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'image_preview'] = str(self.is_image_present(
            CreativeFormLocators.image_preview_locator))
        creative_information_from_form_page['general_information'][
            'dimensions'] = str(self.get_element_text(
            CreativeFormLocators.dimensions_locator)).strip()
        return creative_information_from_form_page

    def provide_info_into_add_creative_carousel_form(self, creative_data):
        self.set_value_into_specific_input_field(CreativeFormLocators.see_more_url_data_qa,
                                                 creative_data['general_information']['see_more_url'])
        self.set_value_into_specific_input_field(CreativeFormLocators.message_data_qa,
                                                 creative_data['general_information']['message'], is_textarea=True)
        self.set_value_into_specific_input_field(CreativeFormLocators.headline_label,
                                                 creative_data['general_information']['headline'])
        self.set_value_into_specific_input_field(CreativeFormLocators.description_label,
                                                 creative_data['general_information']['description'])
        self.set_value_into_specific_input_field(CreativeFormLocators.display_url_data_qa,
                                                 creative_data['general_information']['display_url'])
        self.set_value_into_specific_input_field(CreativeFormLocators.click_url_label,
                                                 creative_data['general_information']['click_url'])
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/600x600.png'))
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=60)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def get_carousel_creative_information_from_form_page(self,
                                                         creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'see_more_url'] = self.get_value_from_specific_input_field(CreativeFormLocators.see_more_url_data_qa)
        creative_information_from_form_page['general_information'][
            'message'] = self.get_value_from_specific_input_field(CreativeFormLocators.message_data_qa,
                                                                  is_textarea=True)
        headline = str(self.get_text_from_specific_label(
            CreativeFormLocators.headline_label)).split(" ")
        final_value = headline[1] + " " + headline[2]
        creative_information_from_form_page['general_information'][
            'headline'] = final_value
        description = str(self.get_text_from_specific_label(
            CreativeFormLocators.description_label)).split(" ")
        final_value = description[1] + " " + description[2]
        creative_information_from_form_page['general_information'][
            'description'] = final_value
        display_url = str(self.get_text_from_specific_label(
            CreativeFormLocators.display_url_2_label)).split(" ")
        final_value = display_url[2]
        creative_information_from_form_page['general_information'][
            'display_url'] = final_value
        click_url = str(self.get_text_from_specific_label(
            CreativeFormLocators.click_url_label)).split(" ")
        final_value = click_url[2]
        creative_information_from_form_page['general_information'][
            'click_url'] = final_value
        creative_information_from_form_page['general_information'][
            'image_preview'] = str(self.is_image_present(
            CreativeFormLocators.image_preview_locator))
        dimensions = str(self.get_text_from_specific_label(
            CreativeFormLocators.dimensions_label)).split(" ")
        final_value = dimensions[1]
        creative_information_from_form_page['general_information'][
            'dimensions'] = final_value
        return creative_information_from_form_page

    def get_text_from_specific_label(self, label_name):
        locator = (
            By.XPATH,
            "//b[normalize-space(text())='" + label_name + "']/..")
        text = self.wait_for_presence_of_element(locator).text
        return text

    def provide_info_into_add_creative_ibv_video_form(self, creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/video.mp4'))
        self.set_value_into_specific_input_field(CreativeFormLocators.description_label,
                                                 creative_data['general_information']['description'], is_textarea=True)
        self.set_value_into_specific_input_field(CreativeFormLocators.call_to_action_label,
                                                 creative_data['general_information'][
                                                     'call_to_action_text'])
        self.check_uncheck_specific_checkbox(CreativeFormLocators.playback_checkbox_label,
                                             bool(creative_data['general_information'][
                                                      'playback_checkbox_status']), "1")
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=60)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def get_ibv_video_creative_information_from_form_page(self,
                                                          creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information'][
                'format']
        creative_information_from_form_page['general_information'][
            'description'] = self.get_value_from_specific_input_field(CreativeFormLocators.description_label,
                                                                      is_textarea=True)
        creative_information_from_form_page['general_information'][
            'call_to_action_text'] = self.get_value_from_specific_input_field(
            CreativeFormLocators.call_to_action_label)
        creative_information_from_form_page['general_information'][
            'playback_checkbox_status'] = self.get_checkbox_status(CreativeFormLocators.playback_checkbox_label, "1")
        return creative_information_from_form_page

    def provide_info_into_add_creative_vast_ibv_video_form(self,
                                                           creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/video.mp4'))
        self.set_value_into_specific_input_field(CreativeFormLocators.description_label,
                                                 creative_data['general_information']['description'], is_textarea=True)
        self.set_value_into_specific_input_field(CreativeFormLocators.call_to_action_label,
                                                 creative_data['general_information'][
                                                     'call_to_action_text'])
        self.click_on_specific_button(CreativeFormLocators.save_button_label)

    def get_vast_video_creative_information_from_form_page(self,
                                                           creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information'][
                'format']
        creative_information_from_form_page['general_information'][
            'description'] = self.get_value_from_specific_input_field(CreativeFormLocators.description_label,
                                                                      is_textarea=True)
        creative_information_from_form_page['general_information'][
            'call_to_action_text'] = self.get_value_from_specific_input_field(
            CreativeFormLocators.call_to_action_label)
        creative_information_from_form_page['general_information'][
            'vpaid_checkbox_status'] = self.get_checkbox_status(
            CreativeFormLocators.viewability_tracking_method_checkbox_label, "1")
        creative_information_from_form_page['general_information'][
            'omid_checkbox_status'] = self.get_checkbox_status(
            CreativeFormLocators.viewability_tracking_method_checkbox_label, "2")
        creative_information_from_form_page['general_information'][
            'enable_vast_wrapper_checkbox_status'] = self.get_checkbox_status(
            CreativeFormLocators.third_party_verification_checkbox_label, "2")
        creative_information_from_form_page['general_information'][
            'skip_after_seconds'] = self.get_value_from_specific_input_field(
            CreativeFormLocators.skip_after_seconds_checkbox_label)
        self.click_on_element(
            CreativeFormLocators.cancel_button_data_qa)
        return creative_information_from_form_page

    def provide_info_into_add_creative_vast_video_form(self,
                                                       creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/video.mp4'))
        self.set_value_into_specific_input_field(CreativeFormLocators.description_label,
                                                 creative_data['general_information']['description'], is_textarea=True)
        self.set_value_into_specific_input_field(CreativeFormLocators.call_to_action_label,
                                                 creative_data['general_information'][
                                                     'call_to_action_text'])
        self.check_uncheck_specific_checkbox(CreativeFormLocators.viewability_tracking_method_checkbox_label, bool(
            creative_data['general_information'][
                'vpaid_checkbox_status']), "1")
        self.check_uncheck_specific_checkbox(CreativeFormLocators.viewability_tracking_method_checkbox_label,
                                             bool(creative_data['general_information'][
                                                      'omid_checkbox_status']), "2")
        self.check_uncheck_specific_checkbox(CreativeFormLocators.third_party_verification_checkbox_label,
                                             bool(creative_data['general_information'][
                                                      'enable_vast_wrapper_checkbox_status']), "2")
        self.set_value_into_specific_input_field(CreativeFormLocators.skip_after_seconds_checkbox_label,
                                                 creative_data['general_information'][
                                                     'skip_after_seconds'])
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=30)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def provide_info_into_add_creative_audio_form(self, creative_data):
        self.wait_for_presence_of_element(
            CreativeFormLocators.file_upload_data_qa.format("1")).send_keys(
            os.path.join(os.getcwd(),
                         'assets/creatives/audio.mp3'))
        self.set_value_into_specific_input_field(CreativeFormLocators.skip_after_seconds_checkbox_label,
                                                 creative_data['general_information'][
                                                     'skip_after_seconds'])
        self.click_on_specific_button(CreativeFormLocators.save_button_label)
        self.wait_for_presence_of_element(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            locator_initialization=True, time_out=30)
        creative_id = self.get_attribute_value(
            CreativeListLocators.specific_creative_id_locator.format(creative_data['general_information']['title']),
            attribute_name=self.href_tag, locator_initialization=True)
        creative_id = (creative_id.split("id="))[1]
        return creative_id

    def get_audio_creative_information_from_form_page(self, creative_data):
        self.reset_creative_information()
        creative_information_from_form_page['general_information'][
            'title'] = self.get_text_using_tag_attribute(
            self.input_tag, self.name_attribute,
            CreativeFormLocators.title_name)
        creative_information_from_form_page['general_information'][
            'creative_format'] = \
            creative_data['general_information']['creative_format']
        creative_information_from_form_page['general_information'][
            'format'] = \
            creative_data['general_information'][
                'format']
        creative_information_from_form_page['general_information'][
            'skip_after_seconds'] = self.get_value_from_specific_input_field(
            CreativeFormLocators.skip_after_seconds_checkbox_label)
        self.click_on_element(
            CreativeFormLocators.cancel_button_data_qa)
        return creative_information_from_form_page

    @staticmethod
    def reset_creative_information():
        # RESET CAMPAIGN_APPROVE INFORMATION BEFORE GETTING DATA
        global creative_information_from_form_page
        creative_information_from_form_page = {
            'general_information': {}}
