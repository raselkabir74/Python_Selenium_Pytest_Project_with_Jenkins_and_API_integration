import json

from pages.api.ad_placement_positions_page import AdPlacementPosition


def test_ad_placement_position(setup):
    access_token, api_base_url, config = setup

    with open('assets/api/ad_placement/ad_placement_positions.json') as json_file:
        ad_placement_positions_data = json.load(json_file)

    response = AdPlacementPosition.get_ad_placement_positions(config, api_base_url, access_token=access_token)

    assert response.headers['Content-Type'] == 'application/json'
    assert response.status_code == 200
    assert response.json() == ad_placement_positions_data

    # ERROR RESPONSE
    response = AdPlacementPosition.get_ad_placement_positions(config, api_base_url, access_token=access_token,
                                                              error_response_check=True)
    assert response.status_code == 400
