class DeviceUtils:

    @staticmethod
    def pull_device_connections_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, title FROM device_connections WHERE enabled = "1"'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_device_page_list_item_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT id , title FROM device_brands WHERE enabled = '1' " \
                                   "ORDER BY id ASC LIMIT 15"
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_total_device_count_from_db(connection):
        total_count = 0
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT COUNT(id) as Total FROM device_brands WHERE enabled = '1'"
                cursor.execute(sql_select_query)
                db_result = cursor.fetchone()
                connection.commit()
            if db_result:
                total_count = db_result["Total"]
            return total_count
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_device_oses_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, title FROM oses WHERE enabled = "1"'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_device_types_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, title FROM device_types WHERE enabled = "1"'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_device_model_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT id, title FROM device_models WHERE device_brand_id = '5' and " \
                                   "enabled = '1' ORDER BY title ASC LIMIT 15"
                cursor.execute(sql_select_query)
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", " ")}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection:", e)
            return None
