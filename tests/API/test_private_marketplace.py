from pages.api.private_marketplace import PrivateMarketplace
from utils.private_marketplace import PrivateMarketplaceUtils


def test_get_list_of_private_marketplaces(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = PrivateMarketplace.get_list_of_private_marketplaces(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    private_marketplace_list_from_db = PrivateMarketplaceUtils.pull_private_marketplace_data_from_db(
        connection=db_connection)
    json_data = PrivateMarketplace.ordered(response.json())
    private_marketplace_list_from_db = PrivateMarketplace.ordered(private_marketplace_list_from_db)
    assert json_data == private_marketplace_list_from_db

    # ERROR RESPONSE
    response = PrivateMarketplace.get_list_of_private_marketplaces(config, api_base_url, access_token=access_token,
                                                                   error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
