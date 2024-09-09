import json

from pages.api.country import Country


def test_country_list(setup):
    access_token, api_base_url, config = setup

    with open('assets/api/country/country_list.json') as json_file:
        country_list = json.load(json_file)

    response = Country.get_county_list(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    assert response.json() == country_list

    # ERROR RESPONSE
    response = Country.get_county_list(config, api_base_url, access_token=access_token,
                                       error_response_check=True)
    assert response.status_code == 400


def test_state_list(setup):
    access_token, api_base_url, config = setup

    with open('assets/api/country/states_list.json') as json_file:
        country_list = json.load(json_file)

    response = Country.get_states_list(config, api_base_url, county_code='bd', access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    assert response.json() == country_list
    # ERROR RESPONSE
    response = Country.get_states_list(config, api_base_url, county_code='bd', access_token=access_token,
                                       error_response_check=True)
    assert response.status_code == 400
