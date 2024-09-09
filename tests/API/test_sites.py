from pages.api.sites import Sites
from utils.sites import SitesUtils


def test_site_platforms(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Sites.get_platforms(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    sites_platforms_data_from_db = SitesUtils.pull_sites_platforms_data_from_db(connection=db_connection)
    assert response.json() == sites_platforms_data_from_db

    # Error check response
    response = Sites.get_platforms(config, api_base_url, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_site_types(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Sites.get_types(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    sites_types_data_from_db = SitesUtils.pull_sites_types_data_from_db(connection=db_connection)
    assert response.json() == sites_types_data_from_db

    # Error check response
    response = Sites.get_types(config, api_base_url, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_sites(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Sites.get_sites(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    sites_data_from_db = SitesUtils.pull_sites_data_from_db(connection=db_connection)
    json_data = Sites.ordered(response.json())
    sites_data_from_db = Sites.ordered(sites_data_from_db)
    assert json_data == sites_data_from_db

    # Error check response
    response = Sites.get_sites(config, api_base_url, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
