class AgeGroupUtils:

    @staticmethod
    def pull_age_group_list_from_db(connection):
        formatted_data = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, title FROM age_groups'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    entry_dict = {"id": db_result["id"], "name": db_result["title"].replace(" ", "")}
                    formatted_data.append(entry_dict)
                return formatted_data
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None
