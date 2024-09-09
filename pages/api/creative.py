import json

import requests
from pages.base_page import BasePage


class Creative(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def create_creative_set(config, api_base_url, access_token, creative_set_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_set_create'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_set_create'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(creative_set_data))
        return response

    @staticmethod
    def update_creative_set(config, api_base_url, access_token, creative_set_data, creative_set_id,
                            error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['creative_set_update'], str(creative_set_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_set_update'], str(creative_set_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(creative_set_data))
        return response

    @staticmethod
    def get_creative_set_list(config, api_base_url, access_token, creative_set_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_set_list'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_set_list'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers, data=json.dumps(creative_set_data))
        return response

    @staticmethod
    def delete_creative_set(config, api_base_url, access_token, creative_set_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['creative_set_delete'], str(creative_set_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_set_delete'], str(creative_set_id))
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.delete(api_url, headers=headers)
        return response

    @staticmethod
    def create_creative(config, api_base_url, access_token, creative_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_create'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_create'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(creative_data))
        return response

    @staticmethod
    def update_banner_type_creative(config, api_base_url, access_token, creative_id, creative_data,
                                    error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['creative_update'], str(creative_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_update'], str(creative_id))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(creative_data))
        return response

    @staticmethod
    def upload_creative_asset_of_banner_type(config, api_base_url, access_token, creative_data,
                                             error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_banner_upload'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_banner_upload'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(creative_data))
        return response

    @staticmethod
    def upload_creative_asset_of_native_type(config, api_base_url, access_token, creative_data,
                                             error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_native_upload'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_native_upload'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.post(api_url, headers=headers, data=json.dumps(creative_data))
        return response

    @staticmethod
    def get_banner_type_creative_list(config, api_base_url, access_token, creative_data, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_list'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['creative_list'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers, data=json.dumps(creative_data))
        return response

    @staticmethod
    def delete_banner_type_creative(config, api_base_url, access_token, creative_id, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['creative_delete'], str(creative_id), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['creative_delete'], str(creative_id))
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.delete(api_url, headers=headers)
        return response
