import json

from pages.api.device import Device
from utils.device import DeviceUtils


def test_device_brand(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Device.get_device_brands(config, api_base_url, access_token=access_token)
    device_brand_list = DeviceUtils.pull_device_page_list_item_from_db(connection=db_connection)
    device_brand_list = Device.ordered(device_brand_list)
    json_data = Device.ordered(response.json()['data'])
    assert json_data == device_brand_list
    assert response.json()["current_page"] == 1

    # ERROR RESPONSE
    response = Device.get_device_brands(config, api_base_url, access_token=access_token,
                                        error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_brands_custom(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    with open('assets/api/device/device_page_data.json') as json_file:
        device_brand_page = json.load(json_file)

    response = Device.get_device_brands_custom(config, api_base_url, access_token=access_token,
                                               brand_page=device_brand_page)
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    assert response.json()["current_page"] == 3
    assert response.json()["per_page"] == 1
    assert response.json()['from'] == 3
    device_total_count_from_db = DeviceUtils.pull_total_device_count_from_db(connection=db_connection)
    assert response.json()["total"] == device_total_count_from_db

    # ERROR RESPONSE
    response = Device.get_device_brands_custom(config, api_base_url, access_token=access_token,
                                               error_response_check=True, brand_page=device_brand_page)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_connections(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Device.get_device_connections(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    device_connection_list_from_db = DeviceUtils.pull_device_connections_from_db(connection=db_connection)
    json_data = Device.ordered(response.json())
    device_connection_list_from_db = Device.ordered(device_connection_list_from_db)
    assert json_data == device_connection_list_from_db

    # ERROR RESPONSE
    response = Device.get_device_connections(config, api_base_url, access_token=access_token,
                                             error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_oses(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Device.get_device_oses(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    device_oses_list_from_db = DeviceUtils.pull_device_oses_from_db(connection=db_connection)
    json_data = Device.ordered(response.json())
    device_oses_list_from_db = Device.ordered(device_oses_list_from_db)
    assert json_data == device_oses_list_from_db

    # ERROR RESPONSE
    response = Device.get_device_oses(config, api_base_url, access_token=access_token,
                                      error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_types(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Device.get_device_types(config, api_base_url, access_token=access_token)
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    device_types_list_from_db = DeviceUtils.pull_device_types_from_db(connection=db_connection)
    json_data = Device.ordered(response.json())
    device_types_list_from_db = Device.ordered(device_types_list_from_db)
    assert json_data == device_types_list_from_db

    # ERROR RESPONSE
    response = Device.get_device_types(config, api_base_url, access_token=access_token,
                                       error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"


def test_device_model(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection
    """
    brandID = 5, 5 = apple mobile brand ID
    """
    response = Device.get_device_by_brandID(config, api_base_url, brandID=5, access_token=access_token)
    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    device_model_list_from_db = DeviceUtils.pull_device_model_from_db(connection=db_connection)
    device_brand_list = Device.ordered(device_model_list_from_db)
    json_data = Device.ordered(response.json()['data'])
    assert json_data == device_brand_list
    assert response.json()["current_page"] == 1
    assert response.json()["per_page"] == 15
    assert response.json()['from'] == 1

    # ERROR RESPONSE
    response = Device.get_device_by_brandID(config, api_base_url, brandID=5, access_token=access_token,
                                            error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
