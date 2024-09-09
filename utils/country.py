class CountryUtils:

    @staticmethod
    def pull_country_name(country_code, connection):
        name = ""
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT name FROM countries WHERE code = '" + country_code + "'"
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()

            for db_result in db_results:
                db_result = dict(db_result)
                name = db_result['name']
            return name
        except Exception as e:
            print("Error in DB Connection", e)
            return name
