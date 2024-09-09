import json

import requests
from pages.base_page import BasePage
from utils.report import ReportUtils


class Report(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_campaign_report_by_ad_placement_position(config, api_base_url, access_token, report_data,
                                                     error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['ad_placement_positions_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['ad_placement_positions_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_ad_placement_type(config, api_base_url, access_token, report_data,
                                                 error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['ad_placement_type_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['ad_placement_type_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_age_group(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['age_group_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['age_group_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_browser(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['browser_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['browser_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_creative(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_exchange(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['exchange_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['exchange_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_gender(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['gender_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['gender_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_operating_system(config, api_base_url, access_token, report_data,
                                                error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['operating_system_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['operating_system_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_operator(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['operator_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['operator_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_site_platform(config, api_base_url, access_token, report_data,
                                             error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['site_platform_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['site_platform_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_site_type(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['site_type_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['site_type_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_site(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['site_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['site_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_campaign(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['campaign_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_campaign_report_by_video_campaign(config, api_base_url, access_token, report_data,
                                              error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['video_campaign_report_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['video_campaign_report_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(report_data))
        return response

    @staticmethod
    def get_device_ids_campaign_report(config, api_base_url, access_token, report_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_ids_campaign_report_get'], "/error")
        else:
            api_url = '{}{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                            config['api']['device_ids_campaign_report_get'] + "?campaignId=",
                                            report_data['campaignId'] + "&dateFrom=", report_data['dateFrom'] +
                                            "&dateTo=", report_data['dateTo'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }

        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views):
        if clicks != 0:
            session_rate = (sessions / clicks) * 100
            formatted_actual_session_rate = float(session_rate)
            formatted_actual_session_rate = int(formatted_actual_session_rate)
        else:
            formatted_actual_session_rate = 0
        formatted_expected_session_rate = float(data['sr'])
        formatted_expected_session_rate = int(formatted_expected_session_rate)

        if sessions != 0:
            cps = (spent_alt_currency / sessions)
            formatted_actual_cps = float(cps)
            formatted_actual_cps = int(formatted_actual_cps)
        else:
            formatted_actual_cps = 0
        formatted_expected_cps = float(data['cps'])
        formatted_expected_cps = int(formatted_expected_cps)

        if impressions != 0:
            viewability = (views / impressions) * 100
            formatted_actual_viewability = float(viewability)
            formatted_actual_viewability = int(formatted_actual_viewability)
        else:
            formatted_actual_viewability = 0
        formatted_expected_viewability = float(data['viewability'])
        formatted_expected_viewability = int(formatted_expected_viewability)

        return formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability

    @staticmethod
    def get_expected_params(specific_report_param):
        return [
            "campaign_id",
            "campaign_name",
            specific_report_param,
            "date",
            "bids",
            "impressions",
            "clicks",
            "ctr",
            "conversions",
            "cr",
            "cpm",
            "cpc",
            "cpa",
            "spent",
            "views",
            "viewability",
            "sessions",
            "sr",
            "cps",
            "wr"]

    @staticmethod
    def get_final_list_from_db(audience_id_list, db_audience_connection):
        final_list = []

        for audience_data in audience_id_list:
            audience_id = audience_data['audience_id']
            audience_type = audience_data['type']
            data_dict = ReportUtils.pull_device_ids_campaign_report_from_db(
                audience_id, audience_type, audience_connection=db_audience_connection)

            cumulative_data = {}

            for entry in data_dict:
                dmp_id = entry['dmp_id']
                if dmp_id not in cumulative_data:
                    cumulative_data[dmp_id] = {"impressions": 0, "event": 0, "clicks": 0, "conversions": 0}
                for key, value in entry.items():
                    if key != 'dmp_id':
                        cumulative_data[dmp_id][key] += value

            for k, v in cumulative_data.items():
                found = False
                for item in final_list:
                    if item['dmp_id'] == k:
                        for key, value in v.items():
                            item[key] += value
                        found = True
                        break
                if not found:
                    final_list.append({'dmp_id': k, **v})
        return final_list
