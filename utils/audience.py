class AudienceUtils:

    @staticmethod
    def pull_audience_data_from_db(audience_id, connection):
        name, user_id, user_validity_minutes, au_type, status, description, date_from, \
            date_to, rule, country, verticals, member_count, api_version, created_date, created_at, updated_at = \
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM `audiences` WHERE id = {}'.format(audience_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    name = db_result['name']
                    user_id = db_result['user_id']
                    user_validity_minutes = db_result['user_validity_minutes']
                    au_type = db_result['type']
                    status = db_result['status']
                    description = db_result['description']
                    date_from = db_result['date_from']
                    date_to = db_result['date_to']
                    rule = db_result['rule']
                    country = db_result['country']
                    verticals = db_result['verticals']
                    member_count = db_result['member_count']
                    api_version = db_result['api_version']
                    created_date = db_result['created_date']
                    updated_at = db_result['updated_at']
                    created_at = db_result['created_at']
                return name, user_id, user_validity_minutes, au_type, status, description, date_from, \
                    date_to, rule, country, verticals, member_count, api_version, created_date, created_at, \
                    updated_at
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None
