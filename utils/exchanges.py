class ExchangeUtils:
    @staticmethod
    def pull_exchange_data_from_db(connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, name FROM exchanges where status = 1 order by id asc'
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
