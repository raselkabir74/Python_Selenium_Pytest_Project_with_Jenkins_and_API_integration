import json

from pages.api.ad_placement_types_page import AdPlacementType


def test_ad_placement_position(setup):
    access_token, api_base_url, config = setup

    with open('assets/api/ad_placement/ad_placement_types.json') as json_file:
        ad_placement_types = json.load(json_file)

    response = AdPlacementType.get_ad_placement_types(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    assert response.json() == ad_placement_types

    # ERROR RESPONSE
    response = AdPlacementType.get_ad_placement_types(config, api_base_url, access_token=access_token,
                                                      error_response_check=True)
    assert response.status_code == 400
