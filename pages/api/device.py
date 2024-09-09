import json

import requests
from pages.base_page import BasePage


class Device(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_device_brands_custom(config, api_base_url, access_token, brand_page, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_brands'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['device_brands'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers, data=json.dumps(brand_page))
        return response

    @staticmethod
    def get_device_brands(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_brands'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['device_brands'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_device_connections(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_connections'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['device_connections'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_device_oses(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_OSes'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['device_OSes'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_device_types(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_types'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['device_types'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_device_by_brandID(config, api_base_url, access_token, brandID, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['device_model_by_bandID'], str(brandID), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['device_model_by_bandID'], str(brandID))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
