import json

from pages.api.operator import Operators
from utils.operators import OperatorUtils


def test_operator(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    with open('assets/api/operator/operator.json') as json_file:
        operator_data = json.load(json_file)

    country = operator_data['country']
    response = Operators.get_operator(config, api_base_url, access_token=access_token, country=country)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    exchange_data_from_db = OperatorUtils.pull_operator_data_from_db(country, connection=db_connection)

    assert response.json() == exchange_data_from_db

    # Error check response
    response = Operators.get_operator(config, api_base_url, access_token=access_token, country=country,
                                      error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
