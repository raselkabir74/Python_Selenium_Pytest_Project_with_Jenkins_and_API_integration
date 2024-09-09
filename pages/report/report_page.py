import time
import math

from decimal import Decimal, ROUND_HALF_UP
from locators.report.report_page_locator import ReportPageLocators
from pages.base_page import BasePage
from selenium.common import TimeoutException
from utils.campaigns import CampaignUtils


class DashboardReportPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def generate_report(self):
        self.select_from_modal("VAST campaign test (ID: 72703)", ReportPageLocators.campaign_select_data_qa)
        self.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, "Admin view")
        self.click_on_element(
            ReportPageLocators.date_range_link_data_qa,
            locator_to_be_appeared=ReportPageLocators.all_date_data_qa)
        self.click_on_element(ReportPageLocators.all_date_data_qa)
        self.click_on_element(
            ReportPageLocators.update_report_button_data_qa,
            locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        self.wait_for_element_to_be_invisible(
            ReportPageLocators.loader_icon_locator)

    def download_report(self, report_type='Excel'):
        self.click_on_element(ReportPageLocators.export_link_locator)
        if report_type == 'Excel':
            self.click_on_element(
                ReportPageLocators.excel_export_link_locator)
        elif report_type == 'PDF':
            self.click_on_element(
                ReportPageLocators.pdf_export_link_locator)
        elif report_type == 'PDF with chart':
            self.click_on_element(
                ReportPageLocators.pdf_chart_export_link_locator)
        success_message = self.get_element_text(
            ReportPageLocators.success_message_locator)
        time.sleep(self.ONE_SEC_DELAY)
        self.wait_for_presence_of_element(
            ReportPageLocators.cross_icon_locator)
        self.wait_for_visibility_of_element(
            ReportPageLocators.cross_icon_locator)
        self.wait_for_element_to_be_clickable(
            ReportPageLocators.cross_icon_locator)
        self.click_on_element(ReportPageLocators.cross_icon_locator)
        try:
            self.wait_for_element_to_be_invisible(
                ReportPageLocators.success_message_locator)
        except TimeoutException:
            self.click_on_element(
                ReportPageLocators.close_alert_button_locator)
        return success_message

    def generate_specific_report(self, campaign_name, campaign_id, view_mode, spent_option):
        self.select_from_modal_form_using_js_code(ReportPageLocators.campaign_select_data_qa,
                                                  option_to_select=campaign_name + " (ID: " + str(campaign_id) + ")")
        self.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, view_mode)
        self.select_dropdown_value(ReportPageLocators.spent_select_data_qa, spent_option)
        self.click_on_element(
            ReportPageLocators.date_range_link_data_qa,
            locator_to_be_appeared=ReportPageLocators.all_date_data_qa)
        self.click_on_element(ReportPageLocators.all_date_data_qa)
        self.click_on_element(ReportPageLocators.datepicker_apply_btn_data_qa)
        self.click_on_element(
            ReportPageLocators.update_report_button_data_qa,
            locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        self.wait_for_element_to_be_invisible(
            ReportPageLocators.loader_icon_locator)

    def get_report_budget_related_metrics_data(self, view_mode=""):
        if view_mode == "Client view":
            impressions = self.get_element_text(ReportPageLocators.impression_value_data_qa)
            reach = self.get_element_text(ReportPageLocators.reach_value_data_qa)

            impressions = int(impressions.replace(',', ''))
            reach = int(reach.replace(',', ''))

            campaign_report_data = {
                "impressions": impressions,
                "reach": reach         
            }
            return campaign_report_data
        elif view_mode == "Admin view":
            impressions = self.get_element_text(ReportPageLocators.impression_value_data_qa)
            reach = self.get_element_text(ReportPageLocators.reach_value_data_qa)
            ctr = self.get_element_text(ReportPageLocators.ctr_value_data_qa)
            spent_amount = self.get_element_text(ReportPageLocators.spent_amount_data_qa)
            cpc_amount = self.get_element_text(ReportPageLocators.cpc_amount_data_qa)
            cpe_amount = self.get_element_text(ReportPageLocators.cpe_amount_data_qa)
            cpm_amount = self.get_element_text(ReportPageLocators.cpm_amount_data_qa)

            impressions = int(impressions.replace(',', ''))
            reach = int(reach.replace(',', ''))
            ctr = float(ctr.replace('%', '').replace(',', ''))
            spent_amount = float(spent_amount.replace('$', '').replace(',', ''))
            cpc_amount = float(cpc_amount.replace('$', '').replace(',', ''))
            cpe_amount = float(cpe_amount.replace('$', '').replace(',', ''))
            cpm_amount = float(cpm_amount.replace('$', '').replace(',', ''))

            campaign_report_data = {
                "impressions": impressions,
                "reach": reach,
                "ctr": ctr,       
                "spent_amount": spent_amount,
                "cpc_amount": cpc_amount,
                "cpe_amount": cpe_amount,
                "cpm_amount": cpm_amount         
            }
            return campaign_report_data
        else:
            spent_amount = self.get_element_text(ReportPageLocators.spent_amount_data_qa)
            cpc_amount = self.get_element_text(ReportPageLocators.cpc_amount_data_qa)
            cpm_amount = self.get_element_text(ReportPageLocators.cpm_amount_data_qa)
            cpe_amount = self.get_element_text(ReportPageLocators.cpe_amount_data_qa)

            spent_amount = float(spent_amount.replace('$', '').replace(',', ''))
            cpc_amount = float(cpc_amount.replace('$', '').replace(',', ''))
            cpm_amount = float(cpm_amount.replace('$', '').replace(',', ''))
            cpe_amount = float(cpe_amount.replace('$', '').replace(',', ''))

            campaign_report_data = {
                "spent_amount": int(spent_amount),
                "cpc_amount": int(cpc_amount),
                "cpe_amount": cpe_amount,
                "cpm_amount": int(cpm_amount)
            }
            return campaign_report_data

    def generate_different_reports_and_get_data(self, campaign_name, campaign_id):
        self.generate_specific_report(campaign_name, campaign_id, "Admin view", "Spent based on cost")
        report_data_admin_view_based_on_cost = self.get_report_budget_related_metrics_data()
        self.select_dropdown_value(ReportPageLocators.spent_select_data_qa, "Spent based on revenue")
        self.click_on_element(ReportPageLocators.update_report_button_data_qa,
                              locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        report_data_admin_view_based_on_revenue = \
            self.get_report_budget_related_metrics_data()
        self.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, "Client view")
        self.click_on_element(ReportPageLocators.update_report_button_data_qa,
                              locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        report_data_client_view_based_on_revenue = \
            self.get_report_budget_related_metrics_data()
        self.select_dropdown_value(ReportPageLocators.spent_select_data_qa, "Spent based on cost")
        self.click_on_element(ReportPageLocators.update_report_button_data_qa,
                              locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        report_data_client_view_based_on_cost = self.get_report_budget_related_metrics_data()
        return report_data_admin_view_based_on_cost, report_data_admin_view_based_on_revenue, \
            report_data_client_view_based_on_revenue, report_data_client_view_based_on_cost

    @staticmethod
    def verify_dicts(dict1, dict2):
        for key in dict1.keys():
            assert key in dict2, f"Key '{key}' missing in second dictionary"
            assert dict1[key] == dict2[key], f"Values for key '{key}' differ between dictionaries"

        for key in dict2.keys():
            assert key in dict1, f"Key '{key}' missing in first dictionary"

    @staticmethod
    def get_calculated_metrics(campaign_id, db_connection, updated_main_margin):
        try:
            data_from_db = CampaignUtils.pull_campaign_clicks_impressions_from_db(campaign_id, db_connection)
            spent_from_db = float(data_from_db[0].replace(',', ''))
            clicks_from_db = int(data_from_db[1])
            impressions_from_db = int(data_from_db[2])
            engagement_from_db = CampaignUtils.pull_campaign_engagement_from_db(campaign_id, db_connection)

            spent_with_new_margin = spent_from_db / (1 - updated_main_margin)
            spent_with_new_margin = math.floor(spent_with_new_margin * 100) / 100
            cpc = round(spent_with_new_margin / clicks_from_db, 2)
            cpe = "0.000" if engagement_from_db is None else spent_with_new_margin / int(engagement_from_db)
            cpm = (spent_with_new_margin / (impressions_from_db / 1000))
            cpm = Decimal(cpm).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

            calculated_metrics_dict = {
                "spent_amount": int(spent_with_new_margin),
                "cpc_amount": int(cpc),
                "cpm_amount": int(cpm),
                "cpe_amount": float(cpe)
            }
            return calculated_metrics_dict
        except Exception as e:
            print(f"Error occurred while calculating metrics: {e}")
            return None

    def update_view_mode(self, view_mode=""):
        self.select_dropdown_value(ReportPageLocators.report_view_select_data_qa, view_mode)
        self.click_on_element(
            ReportPageLocators.update_report_button_data_qa,
            locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        self.wait_for_element_to_be_invisible(
            ReportPageLocators.loader_icon_locator)

    def update_spent_option(self, spent_option=""):
        self.select_dropdown_value(ReportPageLocators.spent_select_data_qa, spent_option)
        self.click_on_element(
            ReportPageLocators.update_report_button_data_qa,
            locator_to_be_appeared=ReportPageLocators.loader_icon_locator)
        self.wait_for_element_to_be_invisible(
            ReportPageLocators.loader_icon_locator)
