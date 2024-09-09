import requests
from pages.base_page import BasePage


class Exchanges(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_exchange_list(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['exchanges_get'], "/error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['exchanges_get'])

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
