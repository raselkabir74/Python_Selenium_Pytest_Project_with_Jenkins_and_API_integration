class SitesUtils:

    @staticmethod
    def pull_sites_platforms_data_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, title FROM sites_platforms'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"]}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_sites_types_data_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, title FROM sites_types'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"]}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_sites_data_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT DISTINCT cps.site_id AS id, s.site_name, s.site_domain ' \
                                   'FROM campaign_performance_report_site cps ' \
                                   'INNER JOIN campaigns c ON cps.campaign_id = c.id ' \
                                   'INNER JOIN sites s ON cps.site_id = s.id ' \
                                   'WHERE c.user_id = 7722'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["site_name"],
                                  "domain": db_result["site_domain"]}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None
