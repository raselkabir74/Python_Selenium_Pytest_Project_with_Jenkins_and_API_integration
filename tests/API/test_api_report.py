import json

from configurations import generic_modules
from pages.api.report import Report
from utils.report import ReportUtils


def test_campaign_report(setup, open_database_connection, open_audience_database_connection):
    access_token, api_base_url, config = setup
    db_connection = open_database_connection
    db_audience_connection = open_audience_database_connection

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY AD PLACEMENT POSITION")

    expected_parameters = Report.get_expected_params('placement_pos_id')

    with open('assets/api/report/placement_position_report_campaign_data.json') as json_file:
        placement_position_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_ad_placement_position(config, api_base_url=api_base_url,
                                                                   access_token=access_token,
                                                                   report_data=placement_position_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_placement_pos',
            campaign_id=str(data['campaign_id']),
            column_name='placement_pos_id',
            type_id=str(data['placement_pos_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_ad_placement_position(config, api_base_url, access_token,
                                                                         placement_position_report_campaign_data,
                                                                         True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY AD PLACEMENT POSITION")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY AD PLACEMENT TYPE")
    expected_parameters = Report.get_expected_params('placement_instl_id')

    with open('assets/api/report/placement_type_report_campaign_data.json') as json_file:
        placement_type_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_ad_placement_type(config, api_base_url, access_token=access_token,
                                                               report_data=placement_type_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_placement_instl',
            campaign_id=str(data['campaign_id']),
            column_name='placement_instl_id',
            type_id=str(data['placement_instl_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_ad_placement_type(config, api_base_url,
                                                                     access_token=access_token,
                                                                     report_data=placement_type_report_campaign_data,
                                                                     error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"
    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY AD PLACEMENT TYPE")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY AGE GROUPS")
    expected_parameters = Report.get_expected_params('age_group_id')

    with open('assets/api/report/age_group_report_campaign_data.json') as json_file:
        age_group_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_age_group(config, api_base_url, access_token=access_token,
                                                       report_data=age_group_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_age_group',
            campaign_id=str(data['campaign_id']),
            column_name='age_group_id',
            type_id=str(data['age_group_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_age_group(config, api_base_url, access_token=access_token,
                                                             report_data=age_group_report_campaign_data,
                                                             error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY AGE GROUPS")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY BROWSERS")
    expected_parameters = Report.get_expected_params('browser_id')

    with open('assets/api/report/browser_report_campaign_data.json') as json_file:
        browser_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_browser(config, api_base_url, access_token=access_token,
                                                     report_data=browser_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_browser',
            campaign_id=str(data['campaign_id']),
            column_name='browser_id',
            type_id=str(data['browser_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_browser(config, api_base_url, access_token=access_token,
                                                           report_data=browser_report_campaign_data,
                                                           error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY BROWSERS")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY CREATIVES")
    expected_parameters = Report.get_expected_params('creative_id')

    with open('assets/api/report/creative_report_campaign_data.json') as json_file:
        creative_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_creative(config, api_base_url, access_token=access_token,
                                                      report_data=creative_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_creative',
            campaign_id=str(data['campaign_id']),
            column_name='creative_id',
            type_id=str(data['creative_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_creative(config, api_base_url, access_token=access_token,
                                                            report_data=creative_report_campaign_data,
                                                            error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY CREATIVES")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY EXCHANGES")
    expected_parameters = Report.get_expected_params('exchange_id')

    with open('assets/api/report/exchange_report_campaign_data.json') as json_file:
        exchange_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_exchange(config, api_base_url, access_token=access_token,
                                                      report_data=exchange_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_exchange',
            campaign_id=str(data['campaign_id']),
            column_name='exchange_id',
            type_id=str(data['exchange_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_exchange(config, api_base_url, access_token=access_token,
                                                            report_data=exchange_report_campaign_data,
                                                            error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY EXCHANGES")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY GENDERS")
    expected_parameters = Report.get_expected_params('gender_id')

    with open('assets/api/report/gender_report_campaign_data.json') as json_file:
        gender_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_gender(config, api_base_url, access_token=access_token,
                                                    report_data=gender_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_gender',
            campaign_id=str(data['campaign_id']),
            column_name='gender_id',
            type_id=str(data['gender_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_gender(config, api_base_url, access_token=access_token,
                                                          report_data=gender_report_campaign_data,
                                                          error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY GENDERS")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY OPERATING SYSTEMS")

    expected_parameters = Report.get_expected_params('os_id')
    with open('assets/api/report/operating_system_report_campaign_data.json') as json_file:
        operating_system_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_operating_system(config, api_base_url, access_token=access_token,
                                                              report_data=operating_system_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_os',
            campaign_id=str(data['campaign_id']),
            column_name='os_id',
            type_id=str(data['os_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_operating_system(config, api_base_url, access_token=access_token,
                                                                    report_data=operating_system_report_campaign_data,
                                                                    error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY OPERATING SYSTEMS")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY OPERATORS")

    expected_parameters = Report.get_expected_params('operator_id')

    with open('assets/api/report/operator_report_campaign_data.json') as json_file:
        operator_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_operator(config, api_base_url, access_token=access_token,
                                                      report_data=operator_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_operator',
            campaign_id=str(data['campaign_id']),
            column_name='operator_id',
            type_id=str(data['operator_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_operator(config, api_base_url, access_token=access_token,
                                                            report_data=operator_report_campaign_data,
                                                            error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY OPERATORS")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY SITE PLATFORMS")

    expected_parameters = Report.get_expected_params('site_platform_id')

    with open('assets/api/report/site_platform_report_campaign_data.json') as json_file:
        site_platform_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_site_platform(config, api_base_url, access_token=access_token,
                                                           report_data=site_platform_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Server'] == 'nginx'
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_site_platform',
            campaign_id=str(data['campaign_id']),
            column_name='site_platform_id',
            type_id=str(data['site_platform_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_site_platform(config, api_base_url, access_token=access_token,
                                                                 report_data=site_platform_report_campaign_data,
                                                                 error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY SITE PLATFORMS")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY SITE TYPES")

    expected_parameters = Report.get_expected_params('site_type_id')

    with open('assets/api/report/site_type_report_campaign_data.json') as json_file:
        site_type_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_site_type(config, api_base_url, access_token=access_token,
                                                       report_data=site_type_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_site_type',
            campaign_id=str(data['campaign_id']),
            column_name='site_type_id',
            type_id=str(data['site_type_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_site_type(config, api_base_url, access_token=access_token,
                                                             report_data=site_type_report_campaign_data,
                                                             error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY SITE TYPES")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT BY SITES")

    expected_parameters = Report.get_expected_params('site_id')

    with open('assets/api/report/site_report_campaign_data.json') as json_file:
        site_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_site(config, api_base_url, access_token=access_token,
                                                  report_data=site_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_report_data_from_db(
            data_table_name='campaign_performance_report_site',
            campaign_id=str(data['campaign_id']),
            column_name='site_id',
            type_id=str(data['site_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert formatted_expected_cps == formatted_actual_cps
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_site(config, api_base_url, access_token=access_token,
                                                        report_data=site_report_campaign_data,
                                                        error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT BY SITES")

    generic_modules.step_info("[START] GET CAMPAIGN REPORT")

    expected_parameters = Report.get_expected_params('exchanges')

    with open('assets/api/report/campaign_report_campaign_data.json') as json_file:
        campaign_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_campaign(config, api_base_url, access_token=access_token,
                                                      report_data=campaign_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        bids, impressions, clicks, spent_alt_currency, sessions, views = ReportUtils.pull_campaign_report_data_from_db(
            campaign_id=str(data['campaign_id']),
            date=str(data['date']),
            connection=db_connection)

        formatted_actual_session_rate, formatted_actual_cps, formatted_actual_viewability, \
            formatted_expected_session_rate, formatted_expected_cps, formatted_expected_viewability = \
            Report.get_formatted_report_data(data, clicks, sessions, spent_alt_currency, impressions, views)

        assert data['bids'] == bids
        assert data['impressions'] == impressions
        assert data['clicks'] == clicks
        assert data['sessions'] == sessions
        assert formatted_expected_session_rate == formatted_actual_session_rate
        assert abs(formatted_expected_cps - formatted_actual_cps) <= 1
        assert formatted_expected_viewability == formatted_actual_viewability

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_campaign(config, api_base_url, access_token=access_token,
                                                            report_data=campaign_report_campaign_data,
                                                            error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET CAMPAIGN REPORT")

    generic_modules.step_info("[START] GET VIDEO CAMPAIGN REPORT")

    expected_parameters = [
        "campaign_id",
        "campaign_name",
        "date",
        "start",
        "firstQuartile",
        "midpoint",
        "thirdQuartile",
        "complete",
        "vtr",
        "cpv",
        "view",
        "vcr",
        "cvtr",
        "cpcv",
        "mute",
        "unmute",
        "pause",
        "resume"
    ]
    with open('assets/api/report/video_campaign_report_campaign_data.json') as json_file:
        video_campaign_report_campaign_data = json.load(json_file)
    response = Report.get_campaign_report_by_video_campaign(config, api_base_url, access_token=access_token,
                                                            report_data=video_campaign_report_campaign_data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    for data in response.json():
        for param in expected_parameters:
            assert param in data
        start, first_quartile, midpoint, third_quartile, complete, view, cpv, vtr, cpcv, vcr, cvtr = \
            ReportUtils.pull_video_campaign_report_data_from_db(
                campaign_id=str(data['campaign_id']),
                date=str(data['date']),
                connection=db_connection)
        assert "{:.1f}".format(data['start']) == "{:.1f}".format(start)
        assert "{:.1f}".format(data['firstQuartile']) == "{:.1f}".format(first_quartile)
        assert "{:.1f}".format(data['midpoint']) == "{:.1f}".format(midpoint)
        assert "{:.1f}".format(data['thirdQuartile']) == "{:.1f}".format(third_quartile)
        assert "{:.1f}".format(data['complete']) == "{:.1f}".format(complete)
        assert "{:.1f}".format(data['view']) == "{:.1f}".format(view)
        assert "{:.1f}".format(data['cpv']) == "{:.1f}".format(cpv)
        assert "{:.1f}".format(data['vtr']) == "{:.1f}".format(vtr)
        assert "{:.1f}".format(data['cpcv']) == "{:.1f}".format(cpcv)
        assert "{:.1f}".format(data['vcr']) == "{:.1f}".format(vcr)
        assert "{:.1f}".format(data['cvtr']) == "{:.1f}".format(cvtr)

    # ERROR RESPONSE
    error_response = Report.get_campaign_report_by_video_campaign(config, api_base_url, access_token=access_token,
                                                                  report_data=video_campaign_report_campaign_data,
                                                                  error_response_check=True)
    assert error_response.status_code == 400
    assert (error_response.json())['error'] == "Bad request"

    generic_modules.step_info("[END] GET VIDEO CAMPAIGN REPORT")

    if "dsp.eskimi.com" in config['credential']['url']:
        generic_modules.step_info("[START] GET DEVICE IDS CAMPAIGN REPORT")

        with open('assets/api/report/device_ids_report_campaign_data.json') as json_file:
            campaign_report_campaign_data = json.load(json_file)
        response = Report.get_device_ids_campaign_report(config, api_base_url, access_token=access_token,
                                                         report_data=campaign_report_campaign_data)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

        audience_id_list = [{'audience_id': 171586, 'type': "impressions"}, {'audience_id': 171587, 'type': "event"},
                            {'audience_id': 171588, 'type': "clicks"}, {'audience_id': 171589, 'type': "conversions"}]

        final_list_from_db = Report.get_final_list_from_db(audience_id_list, db_audience_connection)

        response_data = response.json()
        for entry in response_data:
            for key, value in entry.items():
                if key != 'dmp_id':
                    entry[key] = int(value)

        for entry in response_data:
            found = False
            for item in final_list_from_db:
                if item['dmp_id'] == entry['dmp_id']:
                    assert item == entry
                    found = True
                    break
            assert found

        # ERROR RESPONSE
        error_response = Report.get_device_ids_campaign_report(config, api_base_url, access_token=access_token,
                                                               report_data=campaign_report_campaign_data,
                                                               error_response_check=True)
        assert error_response.status_code == 400
        assert (error_response.json())['error'] == "Bad request"

        generic_modules.step_info("[END] GET DEVICE IDS CAMPAIGN REPORT")
