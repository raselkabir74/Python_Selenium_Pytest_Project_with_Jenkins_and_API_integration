import json

import requests
from pages.base_page import BasePage


class Audience(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def create_audience_by_dmp_ids(config, api_base_url, access_token, audience_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['dmp_audience'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['dmp_audience'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(audience_data))
        return response

    @staticmethod
    def update_dmp_audience(config, api_base_url, access_token, audience_data, audience_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['dmp_audience_update'], str(audience_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['dmp_audience_update'], str(audience_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(audience_data))
        return response

    @staticmethod
    def create_behavioural_audience(config, api_base_url, access_token, audience_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['behavioural_audience'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['behavioural_audience'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(audience_data))
        return response

    @staticmethod
    def update_behavioural_audience(config, api_base_url, access_token, audience_data, audience_id,
                                    error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['behavioural_audience_update'], str(audience_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['behavioural_audience_update'], str(audience_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(audience_data))
        return response

    @staticmethod
    def delete_behavioural_audience(config, api_base_url, access_token, audience_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['behavioural_audience_delete'], str(audience_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['behavioural_audience_delete'], str(audience_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.delete(api_url, headers=headers)
        return response

    @staticmethod
    def delete_dmp_audience(config, api_base_url, access_token, audience_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['dmp_audience_delete'], str(audience_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['dmp_audience_delete'], str(audience_id))
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.delete(api_url, headers=headers)
        return response

    @staticmethod
    def get_audience_interest(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['audience_interest'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['audience_interest'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
