import requests
from pages.base_page import BasePage


class Country(BasePage):

    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def get_county_list(config, api_base_url, access_token, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['country_list'], "error")
        else:
            api_url = '{}{}{}'.format(api_base_url, config['api']['v1'],
                                      config['api']['country_list'])
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response

    @staticmethod
    def get_states_list(config, api_base_url, access_token, county_code, error_response_check=False):
        if error_response_check:
            api_url = '{}{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                          config['api']['states_list'], str(county_code), "/error")
        else:
            api_url = '{}{}{}{}'.format(api_base_url, config['api']['v1'],
                                        config['api']['states_list'], str(county_code))

        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = requests.get(api_url, headers=headers)
        return response
