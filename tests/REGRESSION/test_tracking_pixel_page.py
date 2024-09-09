from configurations import generic_modules
from locators.tracking_pixel.tracking_pixel_locator import TrackingPixelLocators
from pages.tracking_pixel.tracking_pixel_form import DspDashboardTrackingPixel

created_campaign_url = []


def test_regression_pixel_page(login_by_user_type):
    config, driver, redis_connection = login_by_user_type
    tracking_pixel_page = DspDashboardTrackingPixel(driver)

    campaign_approve_url = config['credential']['url'] + config['pixel-page'][
        'pixel-page-url']
    driver.get(campaign_approve_url)
    generic_modules.step_info("[START] RTB-8901 VERIFY TRACKING PIXELS FIELDS AREN'T EMPTY")

    tracking_pixel_page.click_on_element(TrackingPixelLocators.tracking_data_qa)
    tracking_pixel_page.click_on_element(TrackingPixelLocators.conversion_data_qa)
    assert 'function(f,e,t,u,n,s,p)' in tracking_pixel_page.get_element_text(TrackingPixelLocators.audience_text_locator)
    assert "esk('track', 'Conversion');" in tracking_pixel_page.get_element_text(TrackingPixelLocators.conversion_text_locator)
    assert "esk('track', 'Conversion');" in tracking_pixel_page.get_element_text(TrackingPixelLocators.example_text_locator)

    generic_modules.step_info("[END] RTB-8901 VERIFY TRACKING PIXELS FIELDS AREN'T EMPTY")

