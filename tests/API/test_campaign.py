import json
import time

from pages.api.campaign import Campaign
from utils.campaigns import CampaignUtils
from datetime import date, timedelta


def test_create_get_delete_banner_type_campaign(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name'] = campaign_data['name'] + Campaign.get_random_string(5)
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d', days_to_add=10)

    # CREATE BANNER CAMPAIGN
    response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                               campaign_data=campaign_data)

    campaign_id_from_db = CampaignUtils.pull_campaign_id_from_db_for_api(campaign_data['name'],
                                                                         connection=db_connection)
    created_campaign_id = response.json().get('id')

    try:
        # ASSERT CAMPAIGN TYPE
        assert created_campaign_id == campaign_id_from_db[0].get('id')
        campaign_type_from_db = CampaignUtils.pull_campaign_type_from_db(campaign_data['name'],
                                                                         connection=db_connection)
        assert 1 == campaign_type_from_db[0].get('type')

        # ASSERT RESPONSE HEADERS
        assert response.headers['Content-Type'] == 'application/json'

        # GET CAMPAIGN STATUS

        response = Campaign.get_campaign_status(config, api_base_url, access_token=access_token,
                                                campaign_id=(response.json())['id'])

        assert response.json().get('status') == 'pending'
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

        with open('assets/api/campaign/campaign_list_get.json') as json_file:
            get_campaign_list_data = json.load(json_file)

        get_response = Campaign.get_campaign_list(config, api_base_url, access_token=access_token,
                                                  campaign_data=get_campaign_list_data)

        for i, item in enumerate(get_response.json()['data']):
            if item['id'] == created_campaign_id:
                index = i
                assert get_response.json()['data'][index]['id'] == created_campaign_id
                break

        assert get_response.status_code == 200
        assert get_response.json()['from'] == 1
        assert get_response.json()['per_page'] == 15
        assert get_response.json()['to'] == 15
        assert get_response.headers['Content-Type'] == 'application/json'

        get_campaign_list_data['page'] = 2
        get_response = Campaign.get_campaign_list(config, api_base_url, access_token=access_token,
                                                  campaign_data=get_campaign_list_data)
        assert get_response.json()['current_page'] == get_campaign_list_data['page']
        assert get_response.json()['from'] == 16
        assert get_response.json()['per_page'] == 15

        # UPDATE CAMPAIGN
        with open('assets/api/campaign/campaign_update.json') as json_file:
            update_campaign_banner_data = json.load(json_file)

        update_campaign_response = Campaign.update_campaign_banner(config, api_base_url, access_token=access_token,
                                                                   campaign_data=update_campaign_banner_data,
                                                                   campaign_id=created_campaign_id)
        campaign_bid_from_db = CampaignUtils.pull_campaign_bid_from_db(campaign_data['name'], connection=db_connection)

        assert campaign_bid_from_db[0].get('bid_currency') == update_campaign_banner_data['bid']
        assert update_campaign_response.status_code == 200
        assert (update_campaign_response.json())['success'] is True

        # START CAMPAIGN
        start_campaign_response = Campaign.start_campaign(config, api_base_url, access_token=access_token,
                                                          campaign_id=created_campaign_id)
        campaign_status_from_db = CampaignUtils.pull_campaign_status_from_db(campaign_data['name'],
                                                                             connection=db_connection)
        time.sleep(5)
        assert 12 == campaign_status_from_db[0].get('status') or 11 == campaign_status_from_db[0].get('status')
        assert start_campaign_response.status_code == 200
        assert (start_campaign_response.json())['success'] is True

        # STOP CAMPAIGN
        stop_campaign_response = Campaign.stop_campaign(config, api_base_url, access_token=access_token,
                                                        campaign_id=created_campaign_id)
        campaign_status_from_db = CampaignUtils.pull_campaign_status_from_db(campaign_data['name'],
                                                                             connection=db_connection)
        assert 4 == campaign_status_from_db[0].get('status')
        assert stop_campaign_response.status_code == 200
        assert (stop_campaign_response.json())['success'] is True

    finally:
        # DELETE CAMPAIGN
        delete_response = Campaign.delete_campaign(config, api_base_url, access_token=access_token,
                                                   campaign_id=created_campaign_id)
        campaign_status_from_db = CampaignUtils.pull_campaign_status_from_db(campaign_data['name'],
                                                                             connection=db_connection)
        assert 13 == campaign_status_from_db[0].get('status')
        assert delete_response.status_code == 200
        assert (delete_response.json())['success'] is True


def test_create_get_delete_native_type_campaign(setup, open_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection

    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)

    campaign_data['name'] = campaign_data['name'] + Campaign.get_random_string(5)
    campaign_data['creativeSetIds'] = [96570]
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d', days_to_add=10)

    # CREATE NATIVE CAMPAIGN
    response = Campaign.create_campaign_native(config, api_base_url, access_token=access_token,
                                               campaign_data=campaign_data)

    campaign_id_from_db = CampaignUtils.pull_campaign_id_from_db_for_api(campaign_data['name'],
                                                                         connection=db_connection)
    created_campaign_id = response.json().get('id')

    try:
        # ASSERT CAMPAIGN ID
        assert created_campaign_id == campaign_id_from_db[0].get('id')
        # ASSERT CAMPAIGN TYPE
        campaign_type_from_db = CampaignUtils.pull_campaign_type_from_db(campaign_data['name'],
                                                                         connection=db_connection)
        assert 2 == campaign_type_from_db[0].get('type')

        # ASSERT RESPONSE HEADERS
        assert response.headers['Content-Type'] == 'application/json'

        # GET CAMPAIGN STATUS
        response = Campaign.get_campaign_status(config, api_base_url, access_token=access_token,
                                                campaign_id=(response.json())['id'])

        assert response.json().get('status') == 'pending'
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

        with open('assets/api/campaign/campaign_list_get.json') as json_file:
            get_campaign_list_data = json.load(json_file)

        get_response = Campaign.get_campaign_list(config, api_base_url, access_token=access_token,
                                                  campaign_data=get_campaign_list_data)
        print(get_response.json())

        for i, item in enumerate(get_response.json()['data']):
            if item['id'] == created_campaign_id:
                index = i
                assert get_response.json()['data'][index]['id'] == created_campaign_id
                break

        assert get_response.status_code == 200
        assert get_response.json()['from'] == 1
        assert get_response.json()['per_page'] == 15
        assert get_response.json()['to'] == 15
        assert get_response.headers['Content-Type'] == 'application/json'

        get_campaign_list_data['page'] = 2
        get_response = Campaign.get_campaign_list(config, api_base_url, access_token=access_token,
                                                  campaign_data=get_campaign_list_data)
        assert get_response.json()['current_page'] == get_campaign_list_data['page']
        assert get_response.json()['from'] == 16
        assert get_response.json()['per_page'] == 15

        # UPDATE CAMPAIGN
        with open('assets/api/campaign/campaign_update.json') as json_file:
            update_campaign_native_data = json.load(json_file)

        update_campaign_response = Campaign.update_campaign_native(config, api_base_url, access_token=access_token,
                                                                   campaign_data=update_campaign_native_data,
                                                                   campaign_id=created_campaign_id)
        campaign_bid_from_db = CampaignUtils.pull_campaign_bid_from_db(campaign_data['name'], connection=db_connection)

        assert campaign_bid_from_db[0].get('bid_currency') == update_campaign_native_data['bid']
        assert update_campaign_response.status_code == 200
        assert (update_campaign_response.json())['success'] is True

        # START CAMPAIGN
        start_campaign_response = Campaign.start_campaign(config, api_base_url, access_token=access_token,
                                                          campaign_id=created_campaign_id)
        campaign_status_from_db = CampaignUtils.pull_campaign_status_from_db(campaign_data['name'],
                                                                             connection=db_connection)
        time.sleep(5)
        assert 12 == campaign_status_from_db[0].get('status') or 11 == campaign_status_from_db[0].get('status')
        assert start_campaign_response.status_code == 200
        assert (start_campaign_response.json())['success'] is True

        # STOP CAMPAIGN
        stop_campaign_response = Campaign.stop_campaign(config, api_base_url, access_token=access_token,
                                                        campaign_id=created_campaign_id)
        campaign_status_from_db = CampaignUtils.pull_campaign_status_from_db(campaign_data['name'],
                                                                             connection=db_connection)
        assert 4 == campaign_status_from_db[0].get('status')
        assert stop_campaign_response.status_code == 200
        assert (stop_campaign_response.json())['success'] is True

    finally:
        # DELETE CAMPAIGN
        delete_response = Campaign.delete_campaign(config, api_base_url, access_token=access_token,
                                                   campaign_id=created_campaign_id)
        campaign_status_from_db = CampaignUtils.pull_campaign_status_from_db(campaign_data['name'],
                                                                             connection=db_connection)
        assert 13 == campaign_status_from_db[0].get('status')
        assert delete_response.status_code == 200
        assert (delete_response.json())['success'] is True


def test_banner_campaign_validations(setup):
    access_token, api_base_url, config = setup

    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)

    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    # Empty User ID
    campaign_data['userId'] = ''
    userid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                            campaign_data=campaign_data)

    assert 'The given data was invalid.  The user id field is required.. Invalid creatives set ID.' == \
           userid_empty_response.json().get('error')

    # User with no permission for campaign creation
    campaign_data['userId'] = 22911
    userid_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                              campaign_data=campaign_data)

    assert 'The given data was invalid.  Invalid creatives set ID.' == \
           userid_invalid_response.json().get('error')

    # Empty Name field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    name_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                          campaign_data=campaign_data)
    assert 'The given data was invalid.  The name field is required..' in \
           name_empty_response.json().get('error')

    # Name minimum length
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name'] = 'zz'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    name_min_length_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The name must be at least 3 characters..' == \
           name_min_length_response.json().get('error')

    # Empty AdDomain field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['adDomain'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    ad_domain_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The ad domain field is required..' == \
           ad_domain_empty_response.json().get('error')

    # Empty AdDomain field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['adDomain'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    ad_domain_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The ad domain field is required..' == \
           ad_domain_empty_response.json().get('error')

    # Empty clickUrl field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['clickUrl'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    click_url_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The click url field is required..' == \
           click_url_empty_response.json().get('error')

    # Invalid clickUrl field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['clickUrl'] = 'https:business.eskimi.com'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    invalid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                             campaign_data=campaign_data)
    assert 'The given data was invalid.  The click url format is invalid..' == \
           invalid_empty_response.json().get('error')

    # Empty country field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['country'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    country_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                             campaign_data=campaign_data)
    assert 'The given data was invalid.  The country field is required..' == \
           country_empty_response.json().get('error')

    # Invalid country code
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['country'] = 'bdz'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    country_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  Invalid country code.' == \
           country_invalid_response.json().get('error')

    # Empty bid field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['bid'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    bid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The bid field is required..' == \
           bid_empty_response.json().get('error')

    # Minimum bid value
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['bid'] = -1
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    bid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The bid must be at least 0.01..' == \
           bid_empty_response.json().get('error')

    # Maximum bid value
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['bid'] = 111
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    bid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The bid may not be greater than 10..' == \
           bid_empty_response.json().get('error')

    # Empty daily budget
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['budget']['daily'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    daily_budget_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The budget.daily field is required..' == \
           daily_budget_empty_response.json().get('error')

    # Empty total budget
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['budget']['total'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    total_budget_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The budget.total field is required..' == \
           total_budget_empty_response.json().get('error')
    # Empty creative set
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['creativeSetIds'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    creative_set_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The creative set ids field is required..' == \
           creative_set_empty_response.json().get('error')

    # Invalid creative set
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['creativeSetIds'] = '123456'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    creative_set_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                    campaign_data=campaign_data)
    assert 'The given data was invalid.  Invalid creatives set ID.' == \
           creative_set_invalid_response.json().get('error')

    # Empty date.from
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = ''
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    dates_from_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from field is required..' == \
           dates_from_empty_response.json().get('error')

    # Empty date.to
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                              campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to field is required..' == \
           dates_to_empty_response.json().get('error')

    # Invalid date.from
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = 'aaaa-03-29'
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    dates_from_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from is not a valid date.. The dates.from does not match the ' \
           'format Y-m-d.. The dates.from must be a date after or equal to today.. The dates.to must be a date after ' \
           'or equal to dates.from.. Invalid dates for targeting hours.' == \
           dates_from_invalid_response.json().get('error')

    # Invalid date.to
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = 'aaaa-03-29'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to is not a valid date.. The dates.to does not match the ' \
           'format Y-m-d.. The dates.to must be a date after or equal to dates.from.. Invalid dates for' \
           ' targeting hours.' == \
           dates_to_invalid_response.json().get('error')

    # Invalid date.from format
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = '2024-29-03'
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)
    dates_from_invalid_format_response = Campaign.create_campaign_banner(config, api_base_url,
                                                                         access_token=access_token,
                                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from is not a valid date.. The dates.from does not match the ' \
           'format Y-m-d.. The dates.to must be a date after or equal to dates.from.. Invalid dates for targeting' \
           ' hours.' == \
           dates_from_invalid_format_response.json().get('error')

    # Invalid date.to format
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = '2024-29-03'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_invalid_format_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                       campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to is not a valid date.. The dates.to does not match the format' \
           ' Y-m-d.. Invalid dates for targeting hours.' == dates_to_invalid_format_response.json().get('error')

    # date.from minimum validation
    today = date.today()
    yesterday = today - timedelta(days=1)
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = str(yesterday)
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)
    dates_from_min_validation_response = Campaign.create_campaign_banner(config, api_base_url,
                                                                         access_token=access_token,
                                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from must be a date after or equal to today..' == \
           dates_from_min_validation_response.json().get('error')

    # date.from minimum validation
    today = date.today()
    yesterday = today - timedelta(days=1)
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = str(yesterday)
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_min_validation_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                       campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to must be a date after or equal to dates.from..' == \
           dates_to_min_validation_response.json().get('error')

    # invalid hours
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['hours']['1'] = [24]
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    hours_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                             campaign_data=campaign_data)
    assert 'The given data was invalid.  Invalid targeting hours value.' == \
           hours_invalid_response.json().get('error')


def test_native_campaign_validations(setup):
    access_token, api_base_url, config = setup

    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    # Empty User ID
    campaign_data['userId'] = ''
    userid_empty_response = Campaign.create_campaign_native(config, api_base_url, access_token=access_token,
                                                            campaign_data=campaign_data)

    assert 'The given data was invalid.  The user id field is required.. Invalid creatives set ID.' == \
           userid_empty_response.json().get('error')

    # User with no permission for campaign creation
    campaign_data['userId'] = 22911
    userid_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                              campaign_data=campaign_data)

    assert 'The given data was invalid.  Invalid creatives set ID.' == \
           userid_invalid_response.json().get('error')

    # Empty Name field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    name_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                          campaign_data=campaign_data)
    assert 'The given data was invalid.  The name field is required..' == \
           name_empty_response.json().get('error')

    # Name minimum length
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name'] = 'zz'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    name_min_length_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The name must be at least 3 characters..' == \
           name_min_length_response.json().get('error')

    # Empty AdDomain field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['adDomain'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    ad_domain_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The ad domain field is required..' == \
           ad_domain_empty_response.json().get('error')

    # Empty clickUrl field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['clickUrl'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    click_url_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  The click url field is required..' == \
           click_url_empty_response.json().get('error')

    # Invalid clickUrl field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['clickUrl'] = 'https:business.eskimi.com'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    invalid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                             campaign_data=campaign_data)
    assert 'The given data was invalid.  The click url format is invalid..' == \
           invalid_empty_response.json().get('error')

    # Empty country field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['country'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    country_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                             campaign_data=campaign_data)
    assert 'The given data was invalid.  The country field is required..' == \
           country_empty_response.json().get('error')

    # Invalid country code
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['country'] = 'bdz'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    country_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                               campaign_data=campaign_data)
    assert 'The given data was invalid.  Invalid country code.' == \
           country_invalid_response.json().get('error')

    # Empty bid field
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['bid'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    bid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The bid field is required..' == \
           bid_empty_response.json().get('error')

    # Minimum bid value
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['bid'] = -1
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    bid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The bid must be at least 0.01..' == \
           bid_empty_response.json().get('error')

    # Maximum bid value
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['bid'] = 111
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    bid_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The bid may not be greater than 10..' == \
           bid_empty_response.json().get('error')

    # Empty daily budget
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['budget']['daily'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    daily_budget_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The budget.daily field is required..' == \
           daily_budget_empty_response.json().get('error')

    # Empty total budget
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['budget']['total'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    total_budget_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The budget.total field is required..' == \
           total_budget_empty_response.json().get('error')

    # Empty creative set
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['creativeSetIds'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    creative_set_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The creative set ids field is required..' == \
           creative_set_empty_response.json().get('error')

    # Invalid creative set
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['creativeSetIds'] = '123456'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    creative_set_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                    campaign_data=campaign_data)
    assert 'The given data was invalid.  Invalid creatives set ID.' == \
           creative_set_invalid_response.json().get('error')

    # Empty date.from
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = ''
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    dates_from_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from field is required..' == \
           dates_from_empty_response.json().get('error')

    # Empty date.to
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = ''
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_empty_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                              campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to field is required..' == \
           dates_to_empty_response.json().get('error')

    # Invalid date.from
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = 'aaaa-03-29'
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    dates_from_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                  campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from is not a valid date.. The dates.from does not match the ' \
           'format Y-m-d.. The dates.from must be a date after or equal to today.. The dates.to must be a date after ' \
           'or equal to dates.from.. Invalid dates for targeting hours.' == \
           dates_from_invalid_response.json().get('error')

    # Invalid date.to
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = 'aaaa-03-29'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to is not a valid date.. The dates.to does not match the ' \
           'format Y-m-d.. The dates.to must be a date after or equal to dates.from.. Invalid dates for' \
           ' targeting hours.' == \
           dates_to_invalid_response.json().get('error')

    # Invalid date.from format
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = '2024-29-03'
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    dates_from_invalid_format_response = Campaign.create_campaign_banner(config, api_base_url,
                                                                         access_token=access_token,
                                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from is not a valid date.. The dates.from does not match the ' \
           'format Y-m-d.. The dates.to must be a date after or equal to dates.from.. Invalid dates for targeting' \
           ' hours.' == \
           dates_from_invalid_format_response.json().get('error')

    # Invalid date.to format
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = '2024-29-03'
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_invalid_format_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                       campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to is not a valid date.. The dates.to does not match the format' \
           ' Y-m-d.. Invalid dates for targeting hours.' == dates_to_invalid_format_response.json().get('error')

    # date.from minimum validation
    today = date.today()
    yesterday = today - timedelta(days=1)
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['from'] = str(yesterday)
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    dates_from_min_validation_response = Campaign.create_campaign_banner(config, api_base_url,
                                                                         access_token=access_token,
                                                                         campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.from must be a date after or equal to today..' == \
           dates_from_min_validation_response.json().get('error')

    # date.from minimum validation
    today = date.today()
    yesterday = today - timedelta(days=1)
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['dates']['to'] = str(yesterday)
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')

    dates_to_min_validation_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                                       campaign_data=campaign_data)
    assert 'The given data was invalid.  The dates.to must be a date after or equal to dates.from..' == \
           dates_to_min_validation_response.json().get('error')

    # invalid hours
    with open('assets/api/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['hours']['1'] = [24]
    campaign_data['dates']['from'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d')
    campaign_data['dates']['to'] = Campaign.get_specific_date_with_specific_format_for_api('%Y-%m-%d',
                                                                                           days_to_add=30)

    hours_invalid_response = Campaign.create_campaign_banner(config, api_base_url, access_token=access_token,
                                                             campaign_data=campaign_data)
    assert 'The given data was invalid.  Invalid targeting hours value.' == \
           hours_invalid_response.json().get('error')
