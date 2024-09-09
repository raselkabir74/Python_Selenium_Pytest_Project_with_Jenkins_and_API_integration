import datetime
import re
from datetime import timedelta

from selenium.webdriver.common.by import *
from selenium.webdriver.common.keys import Keys

from locators.io.io_list_locator import IoListLocators
from pages.base_page import BasePage
from utils.io import IoUtils


class DspDashboardIoList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def navigate_to_add_io(self):
        self.click_on_element(IoListLocators.create_io_button_data_qa,
                              time_out=20, locator_to_be_appeared=IoListLocators.title_field_data_qa)

    def search_by_title(self, io_title):
        self.set_value_into_element(
            IoListLocators.search_field_data_qa,
            io_title)
        self.wait_for_presence_of_element(
            IoListLocators.search_field_data_qa).send_keys(
            Keys.ENTER)
        self.wait_for_spinner_load()

    def click_on_three_dot_and_action(self, io_id, action="None"):
        self.click_on_element(IoListLocators.three_dot_data_qa.format(io_id))
        if action.lower() == 'edit io':
            self.click_on_element(IoListLocators.edit_io_data_qa.format(io_id))
        if action.lower() == 'proforma':
            self.click_on_element(IoListLocators.proforma_data_qa.format(io_id))
        if action.lower() == 'invoice':
            self.click_on_element(IoListLocators.invoice_data_qa.format(io_id))
        if action.lower() == 'add proforma':
            self.click_on_element(IoListLocators.add_proforma_data_qa.format(io_id))
        if action.lower() == 'edit execution comment (internal)':
            self.click_on_element(IoListLocators.edit_execution_comment_data_qa.format(io_id))

    def is_specific_filter_field_available(self, filter_field_data_qa):
        locator = (By.XPATH, "//select[@data-qa='" + filter_field_data_qa +
                   "']/..//span[@class='select2-selection__rendered'] | //select[@data-qa='" +
                   filter_field_data_qa + "']/..//span[@class='mselect-selection__rendered']")
        return self.is_element_present(locator)

    def clear_specific_filter_option_from_io_list_page(self, field_data_qa):
        locator = (By.XPATH, "//select[@data-qa='" + field_data_qa +
                   "']/..//span[@class='select2-selection__clear']")
        self.click_on_element(locator)

    def search_by_value(self, value):
        self.set_value_into_element(
            IoListLocators.search_field_data_qa, value)
        self.wait_for_presence_of_element(
            IoListLocators.search_field_data_qa).send_keys(
            Keys.ENTER)
        self.wait_for_spinner_load()

    @staticmethod
    def get_specific_date(campaign_list, connection, smallest=True):
        date_function = IoUtils.pull_campaign_date_from_db

        date_list = []
        for campaign in campaign_list:
            campaign_name = re.sub(r'\s+\(\d+\)', '', campaign)
            campaign_date = date_function(campaign_name,
                                          connection,
                                          date_type='start' if smallest else 'end')
            if campaign_date is not None:
                campaign_date = datetime.datetime.strptime(
                    campaign_date.strftime('%Y-%m-%d'),
                    '%Y-%m-%d')
                date_list.append(campaign_date)

        if date_list:
            if smallest:
                return min(date_list).strftime('%Y-%m-%d')
            else:
                return max(date_list).strftime('%Y-%m-%d')
        else:
            return None

    def get_io_campaign_status(self, io_title, connection,
                               campaign_list=None):
        campaigns_in_io = IoUtils.pull_campaigns_names_from_db(
            io_title,
            connection)
        invoice_status = IoUtils.pull_invoice_status_from_db(io_title,
                                                             connection)
        current_date = self.get_current_date_with_specific_format(
            "%Y-%m-%d")
        campaign_status_list = self.get_campaign_status_list(
            campaign_list,
            connection) if campaign_list else []
        campaign_left_to_spend = self.get_campaign_left_to_spend_amount(
            io_title, connection)
        io_amount = IoUtils.pull_io_amount_from_db(io_title, connection)
        io_date = IoUtils.pull_io_date_from_db(io_title, connection)
        io_date_str = (io_date + timedelta(days=30)).strftime(
            "%Y-%m-%d")

        if campaigns_in_io is not None and invoice_status == 6:
            return "Canceled"
        if campaign_list:
            campaign_end_date_list = self.get_campaign_end_date_list(
                campaign_list, connection)
            for end_date, status in zip(campaign_end_date_list,
                                        campaign_status_list):
                if end_date > current_date and status in [
                    "Inactive hourly targeting", "Active",
                    "Daily cap",
                    "Empty wallet"]:
                    return "Live"
            if campaign_left_to_spend <= 200 and campaign_left_to_spend <= float(
                    0.03) * float(io_amount):
                return "Complete"
            if campaign_left_to_spend > 200 or campaign_left_to_spend > float(
                    0.03) * float(io_amount):
                if any(status in ["Expired", "Rejected",
                                  "Deleted", "Removed",
                                  "Draft"] for status in
                       campaign_status_list):
                    return "Incomplete"
            if any(status in ["Stopped", "Budget limit"] for status
                   in
                   campaign_status_list):
                return "Paused"
            if any(status in ["Pending", "Ready"] for status in
                   campaign_status_list):
                return "Pending"
        if campaigns_in_io is None and current_date > io_date_str:
            return "Rotten"
        return "Not live"

    @staticmethod
    def get_campaign_status_list(campaign_list, connection):
        campaign_status_list = []
        for campaign in campaign_list:
            campaign_name = re.sub(r'\s+\(\d+\)', '', campaign)
            campaign_status = IoUtils.pull_campaign_status_from_db(
                campaign_name, connection)
            campaign_status_list.append(campaign_status)
        return campaign_status_list

    @staticmethod
    def get_campaign_end_date_list(campaign_list, connection):
        campaign_end_date_list = []
        for campaign in campaign_list:
            campaign_name = re.sub(r'\s+\(\d+\)', '', campaign)
            campaign_end_date = IoUtils.pull_campaign_date_from_db(
                campaign_name,
                connection,
                date_type='end')
            if campaign_end_date is not None:
                campaign_end_date_str = campaign_end_date.strftime(
                    "%Y-%m-%d")
                campaign_end_date_list.append(
                    campaign_end_date_str)
        return campaign_end_date_list

    @staticmethod
    def get_campaign_spent_rm_amount(spent_alt, margin, agency_margin):
        spent_rm = spent_alt + (
                spent_alt / (1 - margin) - spent_alt) * agency_margin
        return spent_rm

    @staticmethod
    def get_campaign_left_to_spend_amount(io_title, connection):
        io_amount = IoUtils.pull_io_amount_from_db(io_title, connection)
        campaign_spent = IoUtils.pull_campaign_spent_from_db(io_title,
                                                             connection)
        campaign_left_to_spend = io_amount - campaign_spent
        return campaign_left_to_spend
