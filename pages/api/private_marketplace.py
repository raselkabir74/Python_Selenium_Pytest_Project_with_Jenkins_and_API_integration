import requests
from pages.base_page import BasePage


class PrivateMarketplace(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_list_of_private_marketplaces(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['private_marketplace'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['private_marketplace'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
