class PrivateMarketplaceUtils:

    @staticmethod
    def pull_private_marketplace_data_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = ('SELECT pm.id, pm.title FROM private_marketplace pm INNER JOIN '
                                    'private_marketplace_user pmu ON pmu.private_marketplace_id = pm.id WHERE ('
                                    'pmu.user_id = 0 OR pmu.user_id = 7722) AND pm.status = 1')
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
