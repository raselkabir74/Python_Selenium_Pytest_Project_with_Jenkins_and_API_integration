import requests
from pages.base_page import BasePage


class Sites(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_platforms(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['platforms_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['platforms_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_types(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['types_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['types_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_sites(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['sites_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['sites_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
