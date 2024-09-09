from pages.api.gender import Gender
from utils.genders import GenderUtils


def test_genders(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    response = Gender.get_genders(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200

    gender_list_from_db = GenderUtils.pull_genders_list_from_db(connection=db_connection)
    json_data = Gender.ordered((response.json()))
    gender_list_from_db = Gender.ordered(gender_list_from_db)
    assert json_data == gender_list_from_db

    # ERROR RESPONSE
    response = Gender.get_genders(config, api_base_url, access_token=access_token, error_response_check=True)
    assert response.status_code == 400
    assert (response.json())['error'] == "Bad request"
