import csv
import time


class ReportUtils:
    @staticmethod
    def read_widget_ids():
        time.sleep(5)
        widget_list = []
        file_path = 'assets/report/widget_list.csv'
        with open(file_path) as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                widget_list.append(row[0])
        return widget_list

    @staticmethod
    def pull_widget_id_from_db(connection):
        widgets = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'select widgets from user_settings_campaign_report where user_id = 143'  # user id of Arunas
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
            if db_result:
                for widget_id_db in db_result:
                    for widget_ids in widget_id_db.values():
                        widgets.append(
                            widget_ids)
                for id_wid in range(len(widgets)):
                    widgets = widgets[id_wid]
                return widgets
            else:
                return widgets
        except Exception as e:
            print("Error in DB Connection", e)
            return widgets

    @staticmethod
    def pull_report_data_from_db(data_table_name, campaign_id, column_name, type_id, date, connection):
        bids, impressions, clicks, spent_alt_currency, views, sessions = None, None, None, None, None, None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM {} where campaign_id ' \
                                   '= {} AND `{}` = {} AND date = "{}"'.format(data_table_name, campaign_id,
                                                                               column_name, type_id, date)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    bids = db_result['bids']
                    impressions = db_result['impressions']
                    clicks = db_result['clicks']
                    sessions = db_result['sessions']
                    spent_alt_currency = db_result['spent_alt_currency']
                    views = db_result['views']
                return bids, impressions, clicks, spent_alt_currency, sessions, views
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_campaign_report_data_from_db(campaign_id, date, connection):
        bids, impressions, clicks, spent_alt_currency, views, sessions = None, None, None, None, None, None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM campaign_performance_report_campaign where campaign_id ' \
                                   '= {} AND date = "{}"'.format(campaign_id, date)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    bids = db_result['bids']
                    impressions = db_result['impressions']
                    clicks = db_result['clicks']
                    spent_alt_currency = db_result['spent_alt_currency']
                    views = db_result['views']
                    sessions = db_result['sessions']
                return bids, impressions, clicks, spent_alt_currency, sessions, views
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_video_campaign_report_data_from_db(campaign_id, date, connection):
        start, first_quartile, midpoint, third_quartile, complete, view, cpv, vtr, cpcv, vcr, cvtr = \
            None, None, None, None, None, None, None, None, None, None, None
        try:
            with connection.cursor() as cursor:
                sql_select_query = """
                        SELECT
                            r.`campaign_id`, r.`name`,
                            SUM(r.impressions) 'impressions',
                            SUM(r.spent) 'spent',
                            SUM(rm.`start`) 'start',
                            SUM(rm.`first_quartile`) 'first_quartile',
                            SUM(rm.`midpoint`) 'midpoint',
                            SUM(rm.`third_quartile`) 'third_quartile',
                            SUM(rm.`complete`) 'complete',
                            SUM(rm.`view`) 'view',
                            ROUND(IFNULL(SUM(r.`spent`) / SUM(rm.`view`), 0), 4) `cpv`,
                            ROUND(IFNULL(SUM(rm.`view`) / SUM(r.`impressions`) * 100, 0), 3) `vtr`,
                            ROUND(IFNULL(SUM(r.`spent`) / SUM(rm.`complete`), 0), 4) `cpcv`,
                            ROUND(IFNULL(SUM(rm.`complete`) / SUM(rm.`start`) * 100, 0), 3) `vcr`,
                            ROUND(IFNULL(SUM(rm.`complete`) / SUM(r.`impressions`) * 100, 0), 3) `cvtr`
                        FROM (SELECT
                                r.campaign_id,
                                CONCAT(c.`name`, " (ID: ", c.`id`, ")") 'name',
                                SUM(r.`impressions`) 'impressions',
                                IFNULL(SUM(r.`impressions` * c.`dev_cpm` / 1000 * (r.`spent_alt_currency` / r.`spent_alt`)) + SUM(r.`spent_alt_currency`), 0) spent
                            FROM `campaign_performance_report_exchange` r
                            INNER JOIN campaigns c ON c.`id` = r.`campaign_id`
                            WHERE r.`date` BETWEEN '{}' AND '{}'
                                AND c.`type` = 3
                                AND (c.`id` = {})
                            GROUP BY r.`campaign_id`) r
                        INNER JOIN (SELECT
                                rm.`campaign_id`,SUM(IF(`subtype_id` = 1, `count`, 0)) 'start',
                                SUM(IF(`subtype_id` = 2, `count`, 0)) 'first_quartile',
                                SUM(IF(`subtype_id` = 3, `count`, 0)) 'midpoint',
                                SUM(IF(`subtype_id` = 4, `count`, 0)) 'third_quartile',
                                SUM(IF(`subtype_id` = 11, `count`, 0)) 'complete',
                                SUM(IF(`subtype_id` = 25, `count`, 0)) 'view'
                            FROM `campaigns` c
                            INNER JOIN `campaign_performance_report_metrics` rm ON c.`id` = rm.`campaign_id`
                            WHERE rm.`date` BETWEEN '{}' AND '{}' AND (c.`id` = {})
                            GROUP BY rm.`campaign_id`) rm ON rm.`campaign_id` = r.`campaign_id`
                        GROUP BY r.`campaign_id`;
                    """.format(date, date, campaign_id, date, date, campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    start = db_result['start']
                    first_quartile = db_result['first_quartile']
                    midpoint = db_result['midpoint']
                    third_quartile = db_result['third_quartile']
                    complete = db_result['complete']
                    view = db_result['view']
                    cpv = db_result['cpv']
                    vtr = db_result['vtr']
                    cpcv = db_result['cpcv']
                    vcr = db_result['vcr']
                    cvtr = db_result['cvtr']
                return start, first_quartile, midpoint, third_quartile, complete, view, cpv, vtr, cpcv, vcr, cvtr
            else:
                return None
        except Exception as e:
            print("Error in DB Connection:", e)
            return None

    @staticmethod
    def pull_campaign_audiences_from_db(campaign_id, connection):
        results = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT ac.type, ac.audience_id FROM `audiences_campaigns` ac ' \
                                   'INNER JOIN `audiences` a ON ac.audience_id = a.id ' \
                                   'WHERE ac.campaign_id = {} AND a.member_count > 0 ' \
                                   'ORDER BY FIELD(ac.type, 5,7,4,6);'.format(campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    audience_type = db_result['type']
                    audience_id = db_result['audience_id']
                    results.append((audience_type, audience_id))
                return results
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_device_ids_campaign_report_from_db(audience_id, audience_type, audience_connection):
        try:
            with audience_connection.cursor() as cursor:
                sql_select_query = 'SELECT ai.dmp_id, IF(ai.dmp_id IS NOT NULL, ai.count, 0) ' \
                                   '"{}" FROM audience_{} ai ' \
                                   'WHERE ai.timestamp > 1693515600 AND ai.timestamp < 1764453600 ' \
                                   'ORDER BY ai.dmp_id LIMIT 500000;'.format(audience_type, audience_id)
                cursor.execute(sql_select_query)
                audience_connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                return db_results
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None
