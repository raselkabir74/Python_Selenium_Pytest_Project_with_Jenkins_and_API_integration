from pages.base_page import BasePage


class DspDashboardTrackingPixel(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
