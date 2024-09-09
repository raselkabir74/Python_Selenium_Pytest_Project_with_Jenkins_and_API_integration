import requests
from pages.base_page import BasePage


class Operators(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_operator(config, api_base_url, access_token, country, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['operators_get'], country, "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['operators_get'], country)

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
