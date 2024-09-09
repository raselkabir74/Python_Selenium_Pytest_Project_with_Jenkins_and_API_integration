import json

import requests
from pages.base_page import BasePage


class Campaign(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def create_campaign_banner(config, api_base_url, access_token, campaign_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_create_banner'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['campaign_create_banner'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(campaign_data))
        return response

    @staticmethod
    def create_campaign_native(config, api_base_url, access_token, campaign_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_create_native'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['campaign_create_native'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(campaign_data))
        return response

    @staticmethod
    def delete_campaign(config, api_base_url, access_token, campaign_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['campaign_delete'], str(campaign_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_delete'], str(campaign_id))
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.delete(api_url, headers=headers)
        return response

    @staticmethod
    def get_campaign_list(config, api_base_url, access_token, campaign_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_list_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['campaign_list_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers, data=json.dumps(campaign_data))
        return response

    @staticmethod
    def get_campaign_status(config, api_base_url, access_token, campaign_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['campaign_status_get'], str(campaign_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_status_get'], str(campaign_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def start_campaign(config, api_base_url, access_token, campaign_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['campaign_start'], str(campaign_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_start'], str(campaign_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers)
        return response

    @staticmethod
    def stop_campaign(config, api_base_url, access_token, campaign_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['campaign_stop'], str(campaign_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_stop'], str(campaign_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers)
        return response

    @staticmethod
    def update_campaign_banner(config, api_base_url, access_token, campaign_data, campaign_id,
                               error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['campaign_update_banner'], str(campaign_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_update_banner'], str(campaign_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(campaign_data))
        return response

    @staticmethod
    def update_campaign_native(config, api_base_url, access_token, campaign_data, campaign_id,
                               error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['campaign_update_native'], str(campaign_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['campaign_update_native'], str(campaign_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(campaign_data))
        return response
