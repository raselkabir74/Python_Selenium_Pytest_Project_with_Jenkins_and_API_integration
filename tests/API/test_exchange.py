from pages.api.exchange import Exchanges
from utils.exchanges import ExchangeUtils


def test_exchanges_list(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Exchanges.get_exchange_list(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    exchange_data_from_db = ExchangeUtils.pull_exchange_data_from_db(connection=db_connection)
    assert response.json() == exchange_data_from_db

    # Error check response
    response = Exchanges.get_exchange_list(config, api_base_url, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
