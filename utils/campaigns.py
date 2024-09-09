import json
import os
from configurations import generic_modules
import datetime
import requests


class CampaignUtils:

    @staticmethod
    def pull_campaign_data_db(campaign_name, connection, user_id="7722", status=0):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT user_id, platform_id, ad_domain, click_url, country, bid_currency, ' \
                                   'budget_daily_currency, budget_total_currency, targeting, ' \
                                   'capping FROM campaigns where name = \'{}\' and user_id = \'{}\' ' \
                                   'and status = \'{}\''.format(campaign_name, user_id, status)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                db_result = dict(db_result)
                db_result['bid_currency'] = float(
                    db_result['bid_currency'])
                db_result['budget_daily_currency'] = float(
                    db_result['budget_daily_currency'])
                db_result['budget_total_currency'] = float(
                    db_result['budget_total_currency'])
                db_result['targeting'] = json.loads(
                    db_result['targeting'])
                del db_result['targeting']['date_from']
                del db_result['targeting']['date_to']
                del db_result['targeting'][
                    'excluded_operators']
                db_result['capping'] = json.loads(
                    db_result['capping'])
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_id_from_db(campaign_name, connection, user_id="7722"):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns where name like \'%{}%\' and user_id = \'{}\''.format(
                    campaign_name, user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_goal_data_from_db(connection, country_id, goal_type):
        """
        Pull impression data for goal type
        """
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'select impressions from country_settings_optimisations where ' \
                                   'country_id =\'{}\' and type =\'{}\''.format(
                    country_id, goal_type)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_deal_margin_value_from_db(campaign_name, connection):
        db_result_margin = None
        try:
            with connection.cursor() as cursor:
                sql_select_id_query = 'SELECT id FROM campaigns where name = \'{}\''.format(
                    campaign_name)
                cursor.execute(sql_select_id_query)
                connection.commit()
                db_result_id = cursor.fetchone()
                if db_result_id:
                    for id in db_result_id.values():
                        sql_select_query = 'SELECT private_deal_id, deal_margin FROM campaign_settings_private_deals ' \
                                           'where campaign_id = \'{}\''.format(id)
                        cursor.execute(
                            sql_select_query)
                        connection.commit()
                        db_result_margin = cursor.fetchall()
                        return db_result_margin
                else:
                    return db_result_margin
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result_margin

    @staticmethod
    def pull_campaign_name_from_db(campaign_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT name FROM campaigns WHERE id = {}'.format(
                    campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['name']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def create_campaign_by_api(config, user_type="admin",
                               mass_campaign_name=""):
        access_token, base_url, config = generic_modules.get_api_access_token(
            config['api']['oauth'],
            config['credential'])
        api_url = '{}{}{}'.format(base_url,
                                  config['api']['v1'],
                                  config['api']['banner-create'])
        with open(
                'assets/campaign/campaign_data_api.json') as campaign_data:
            campaign_data = json.load(campaign_data)
        campaign_data['budget']['total'] = 60
        campaign_data['dates']['from'] = str(
            datetime.date.today() + + datetime.timedelta(days=2))
        campaign_data['dates']['to'] = str(
            datetime.date.today() + datetime.timedelta(days=7))
        if mass_campaign_name != "":
            campaign_data['name'] = mass_campaign_name
        else:
            campaign_data['name'] = campaign_data[
                                        'name'] + generic_modules.get_random_string(
                5)
        campaign_data['userId'] = int(config['credential']['user-id'])
        campaign_data['creativeSetIds'] = [
            int(config['banner-creative-set-by-user-type'][
                    user_type])]
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = json.loads(
            requests.request('POST', api_url,
                             data=json.dumps(campaign_data),
                             headers=headers).text)
        campaign_data['campaignId'] = response['id']
        return campaign_data

    @staticmethod
    def delete_campaign_by_api(config, campaign_id):
        access_token, base_url, config = generic_modules.get_api_access_token(
            config['api']['oauth'],
            config['credential'])
        api_url = '{}{}{}'.format(base_url,
                                  config['api']['v1'],
                                  (config['api']['delete']).format(campaign_id))
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = json.loads(
            requests.request('DELETE', api_url,
                             headers=headers).text)
        status = response['success']
        return status

    @staticmethod
    def create_campaign_by_api_with_current_date(config, user_type="admin",
                                                 mass_campaign_name=""):
        access_token, base_url, config = generic_modules.get_api_access_token(
            config['api']['oauth'],
            config['credential'], user_type)
        api_url = '{}{}{}'.format(base_url,
                                  config['api']['v1'],
                                  config['api']['banner-create'])
        with open(
                'assets/campaign/campaign_data_api.json') as campaign_data:
            campaign_data = json.load(campaign_data)
        campaign_data['dates']['from'] = str(
            datetime.date.today() + datetime.timedelta(days=0))
        campaign_data['dates']['to'] = str(
            datetime.date.today() + datetime.timedelta(days=7))
        if mass_campaign_name != "":
            campaign_data['name'] = mass_campaign_name
        else:
            campaign_data['name'] = campaign_data[
                                        'name'] + generic_modules.get_random_string(
                5)
        if user_type == "admin":
            campaign_data['userId'] = int(config['credential']['user-id'])
            campaign_data['creativeSetIds'] = [
                int(config['banner-creative-set-by-user-type'][
                        user_type])]
        elif user_type == "agency-client":
            campaign_data['userId'] = int(config['credential']['agency-client-user-id'])
            campaign_data['creativeSetIds'] = [
                int(config['banner-creative-set-by-user-type'][
                        user_type])]
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = json.loads(
            requests.request('POST', api_url,
                             data=json.dumps(campaign_data),
                             headers=headers).text)
        campaign_data['campaignId'] = response['id']
        return campaign_data

    @staticmethod
    def process_campaign_approve_data(campaign_approve_data,
                                      single_approve=False):
        if single_approve:
            if campaign_approve_data['reporting_and_budget'][
                'email_report'][
                'is_checked'] == "False":
                campaign_approve_data['reporting_and_budget'][
                    'email_report'][
                    'is_checked'] = ""

            if campaign_approve_data['reporting_and_budget'][
                'group_by_io'][
                'is_checked'] == "False":
                campaign_approve_data['reporting_and_budget'][
                    'group_by_io'][
                    'is_checked'] = ""

            if \
                    campaign_approve_data['reporting_and_budget'][
                        'email_attachment'][
                        'xls']['is_checked'] == "False":
                campaign_approve_data['reporting_and_budget'][
                    'email_attachment']['xls'][
                    'is_checked'] = ""

            if \
                    campaign_approve_data['reporting_and_budget'][
                        'email_attachment'][
                        'pdf']['is_checked'] == "False":
                campaign_approve_data['reporting_and_budget'][
                    'email_attachment']['pdf'][
                    'is_checked'] = ""

        if campaign_approve_data['optimization_and_tracking'][
            'multiple_bids_per_second'] == "False":
            campaign_approve_data['optimization_and_tracking'][
                'multiple_bids_per_second'] = ""

        if campaign_approve_data['ad_exchange'][
            'eskimi_margin'] == "False":
            campaign_approve_data['ad_exchange'][
                'eskimi_margin'] = ""

        return campaign_approve_data

    @staticmethod
    def process_campaign_name(campaign_list, operation="mass approve"):
        if operation == "mass approve":
            campaign_name_list = [
                campaign_list[
                    'campaign-name-for-mass-approve-1'] + generic_modules.get_random_string(
                    5),
                campaign_list[
                    'campaign-name-for-mass-approve-2'] + generic_modules.get_random_string(
                    5),
                campaign_list[
                    'campaign-name-for-mass-approve-3'] + generic_modules.get_random_string(
                    5)
                ]
            return campaign_name_list
        elif operation == "mass duplicate and edit":
            campaign_name_list = [
                campaign_list[
                    'campaign-name-for-mass-edit-and-duplicate-1'] + generic_modules.get_random_string(
                    5),
                campaign_list[
                    'campaign-name-for-mass-edit-and-duplicate-2'] + generic_modules.get_random_string(
                    5),
                campaign_list[
                    'campaign-name-for-mass-edit-and-duplicate-3'] + generic_modules.get_random_string(
                    5)
                ]
            return campaign_name_list
        elif operation == "mass edit":
            campaign_name_list = [
                campaign_list[
                    'campaign-name-for-mass-edit-1'] + generic_modules.get_random_string(
                    5),
                campaign_list[
                    'campaign-name-for-mass-edit-1'] + generic_modules.get_random_string(
                    5)
                ]
            return campaign_name_list
        elif operation == "before mass duplicate operation":
            campaign_name_list = [
                campaign_list[
                    'campaign-name-before-mass-edit-and-duplicate-1'],
                campaign_list[
                    'campaign-name-before-mass-edit-and-duplicate-2'],
                campaign_list[
                    'campaign-name-before-mass-edit-and-duplicate-3']
                ]
            return campaign_name_list

    @staticmethod
    def pull_campaign_spent_based_on_cost_from_db(campaign_id, creative_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT FORMAT(SUM(spent), 2) AS total_spent ' \
                                   'FROM campaign_performance_report_creative ' \
                                   f'WHERE campaign_id = "{campaign_id}" AND creative_id = "{creative_id}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['total_spent']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_exchange_id_from_db(exchange_name, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = f'SELECT id from exchanges WHERE name = "{exchange_name}"'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['id']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_exchange_name_from_db(exchange_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = f'SELECT name from exchanges WHERE id = {exchange_id}'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['name']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_impressions_from_db(campaign_id, exchange_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT SUM(cpre.impressions) from campaign_performance_report_exchange cpre ' \
                                   f'WHERE cpre.campaign_id = {campaign_id} AND cpre.exchange_id = {exchange_id}'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['SUM(cpre.impressions)']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_bids_from_db(campaign_id, exchange_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT SUM(cpre.bids) from campaign_performance_report_exchange cpre ' \
                                   f'WHERE cpre.campaign_id = {campaign_id} AND cpre.exchange_id = {exchange_id}'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['SUM(cpre.bids)']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_views_from_db(campaign_id, exchange_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT SUM(cpre.views) from campaign_performance_report_exchange cpre ' \
                                   f'WHERE cpre.campaign_id = {campaign_id} AND cpre.exchange_id = {exchange_id}'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['SUM(cpre.views)']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_clicks_from_db(campaign_id, exchange_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT SUM(cpre.clicks) from campaign_performance_report_exchange cpre ' \
                                   f'WHERE cpre.campaign_id = {campaign_id} AND cpre.exchange_id = {exchange_id}'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['SUM(cpre.clicks)']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_spent_based_on_revenue_from_db(campaign_id, exchange_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT SUM(cpre.spent_alt) from campaign_performance_report_exchange cpre ' \
                                   f'WHERE cpre.campaign_id = {campaign_id} AND cpre.exchange_id = {exchange_id}'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['SUM(cpre.spent_alt)']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_data_from_db_without_status(campaign_name, connection, user_id="7722"):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT user_id, platform_id, ad_domain, click_url, country, bid_currency, ' \
                                   'budget_daily_currency, budget_total_currency, targeting, ' \
                                   'capping, margin_main FROM campaigns where name = \'{}\' and user_id = \'{}\''. \
                    format(campaign_name, user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                db_result = dict(db_result)
                db_result['bid_currency'] = float(
                    db_result['bid_currency'])
                db_result['budget_daily_currency'] = float(
                    db_result['budget_daily_currency'])
                db_result['budget_total_currency'] = float(
                    db_result['budget_total_currency'])
                db_result['targeting'] = json.loads(
                    db_result['targeting'])
                del db_result['targeting']['date_from']
                del db_result['targeting']['date_to']
                del db_result['targeting'][
                    'excluded_operators']
                db_result['capping'] = json.loads(
                    db_result['capping'])
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_specific_campaign_id_from_db(connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE status = 1 AND margin_main > 0 ' \
                                   'AND targeting_date_from < CURDATE() AND targeting_date_to >= DATE_ADD(CURDATE(), ' \
                                   'INTERVAL 5 DAY) AND type > 1 ORDER BY RAND() LIMIT 1;'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_main_margin_from_db(campaign_id, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT margin_main FROM campaigns WHERE id = "{}"'.format(campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['margin_main']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_user_id_from_db(campaign_id, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT user_id FROM campaigns WHERE id = "{}"'.format(campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['user_id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_clicks_impressions_from_db(campaign_id, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT FORMAT(SUM(cpre.spent_alt), 2) AS total_spent, SUM(cpre.clicks) AS ' \
                                   'total_clicks, SUM(cpre.impressions) AS total_impressions FROM ' \
                                   'campaign_performance_report_exchange cpre WHERE cpre.campaign_id = {}'. \
                    format(campaign_id)
                cursor.execute(sql_select_query)
                db_results = cursor.fetchone()
            if db_results:
                total_spent = db_results['total_spent']
                total_clicks = db_results['total_clicks']
                total_impressions = db_results['total_impressions']
                return total_spent, total_clicks, total_impressions
            else:
                return None, None, None
        except Exception as e:
            print("Error in DB Connection:", e)
            return None, None, None

    @staticmethod
    def pull_campaign_engagement_from_db(campaign_id, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT SUM(count) AS total_engagement FROM ' \
                                   'campaign_performance_report_metrics_creative WHERE subtype_id = 4757 AND ' \
                                   'campaign_id = {};'.format(campaign_id)
                cursor.execute(sql_select_query)
                db_results = cursor.fetchone()
            if db_results:
                total_engagement = db_results['total_engagement']
                return total_engagement
            else:
                return 0
        except Exception as e:
            print("Error in DB Connection:", e)
            return None

    @staticmethod
    def pull_campaign_daily_budget_from_db(campaign_id, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT budget_daily_currency FROM campaigns WHERE id = "{}"'.format(campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return float(db_result['budget_daily_currency'])
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_id_with_fixed_cpm_from_db(connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT c.id FROM campaigns c JOIN campaign_settings_reporting csr ON c.id = ' \
                                   'csr.campaign_id JOIN (SELECT campaign_id, MAX(date) AS latest_date FROM ' \
                                   'campaign_settings_reporting GROUP BY campaign_id) latest_csr ON csr.campaign_id ' \
                                   '= latest_csr.campaign_id AND csr.date = latest_csr.latest_date WHERE c.status = 1 ' \
                                   'AND c.margin_main > 0 AND c.targeting_date_from < CURDATE() ' \
                                   'AND csr.report_type = 3 ORDER BY RAND() LIMIT 1;'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_fixed_cpm_from_db(connection, campaign_id):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT price_currency FROM campaign_settings_reporting WHERE ' \
                                   'campaign_id ="{}"'.format(campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['price_currency']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_live_campaign_without_main_margin_id_from_db(connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE status = 1 AND margin_main = 0 ' \
                                   'AND targeting_date_from < CURDATE() AND targeting_date_to >= DATE_ADD(CURDATE(), ' \
                                   'INTERVAL 5 DAY) ORDER BY RAND() LIMIT 1;'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_end_date_from_db(connection, campaign_id):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT targeting_date_to FROM campaigns ' \
                                   'WHERE id = {}'.format(campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                date_to = db_result['targeting_date_to']
                return date_to
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_few_live_campaign_ids_for_the_same_user_from_db(connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE user_id = (SELECT user_id FROM (SELECT user_id ' \
                                   'FROM campaigns WHERE status = 1 AND margin_main > 0 AND targeting_date_from ' \
                                   '< CURDATE() AND targeting_date_to >= DATE_ADD(CURDATE(), INTERVAL 5 DAY) ' \
                                   'AND type > 1 GROUP BY user_id HAVING COUNT(id) >= 2 ORDER BY RAND() LIMIT 1) ' \
                                   'AS eligible_users) AND status = 1 AND margin_main > 0 AND targeting_date_from ' \
                                   '< CURDATE() AND targeting_date_to >= DATE_ADD(CURDATE(), INTERVAL 5 DAY) ' \
                                   'AND type > 1 ORDER BY RAND() LIMIT 2;'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                if db_result:
                    return [row['id'] for row in db_result]
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def check_main_margin_changes_today(connection, campaign_id):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM data_change_log_diff WHERE item_id = "{}" AND created_at_date = ' \
                                   'CURDATE() AND JSON_CONTAINS_PATH(item, "one", "$.margin_main");'.format(campaign_id)
                cursor.execute(sql_select_query)
                db_result = cursor.fetchall()
                if db_result:
                    return True
                else:
                    return False
        except Exception as e:
            print("Error in DB Connection:", e)
            return False

    @staticmethod
    def pull_campaign_type_from_db(campaign_name, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT type FROM campaigns where name like \'%{}%\' and user_id = 7722 ' \
                                   'and status = 0'.format(campaign_name)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
            if db_result:
                return db_result
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_status_from_db(campaign_name, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT status FROM campaigns where name like \'%{}%\' and user_id = 7722'. \
                    format(campaign_name)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
            if db_result:
                return db_result
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_bid_from_db(campaign_name, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT bid_currency FROM campaigns where name like \'%{}%\' and ' \
                                   'user_id = 7722 and status = 0'.format(campaign_name)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
            if db_result:
                return db_result
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_id_from_db_for_api(campaign_name, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT id FROM campaigns where name = '{}' and user_id = 7722 and " \
                                   "status = 0".format(campaign_name)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
            if db_result:
                return db_result
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_with_specific_status_id_from_db(connection, status='1'):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE status = {} ORDER BY RAND() LIMIT 1;'.format(status)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_expired_live_campaign_id_from_db(connection, status):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE status = {} AND targeting_date_to = CURDATE() - ' \
                                   'INTERVAL 1 DAY ORDER BY RAND() LIMIT 1;'.format(status)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_ready_live_campaign_id_from_db(connection, status):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE status = {} AND targeting_date_from = CURDATE() ' \
                                   'ORDER BY RAND() LIMIT 1;'.format(status)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_inactive_live_campaign_id_from_db(connection, status):
        current_day = datetime.datetime.now().isoweekday()
        current_hour = datetime.datetime.now().hour
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, targeting FROM campaigns WHERE status = {} ' \
                                   'ORDER BY RAND();'.format(status)
                cursor.execute(sql_select_query)
                campaigns = cursor.fetchall()
                for campaign in campaigns:
                    targeting = json.loads(campaign['targeting'])
                    if str(current_day) in targeting['hours'] and current_hour in targeting['hours'][str(current_day)]:
                        return campaign['id']
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_live_campaign_with_end_day_today_tomorrow_id_from_db(connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM campaigns WHERE status = 1 AND targeting_date_to = CURDATE() ORDER' \
                                   ' BY RAND() LIMIT 1;'
                cursor.execute(sql_select_query)
                db_result = cursor.fetchone()
                if not db_result:
                    sql_select_query = 'SELECT id FROM campaigns WHERE status = 1 AND targeting_date_to = ' \
                                       'CURDATE() + INTERVAL 1 DAY ORDER BY RAND() LIMIT 1;'
                    cursor.execute(sql_select_query)
                    db_result = cursor.fetchone()
                connection.commit()
                if db_result:
                    return db_result['id']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_user_name_from_db(connection, user_id):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT name FROM users_admin WHERE id = {}'.format(user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                if db_result:
                    return db_result['name']
                else:
                    return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None
