class CreativesUtils:

    @staticmethod
    def pull_creative_preserve_status_from_db(creative_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT is_reserved FROM `rtb-dsp`.creatives ' \
                                   f'WHERE title = "{creative_title}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['is_reserved']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_creative_id_from_db(creative_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM `rtb-dsp`.creatives ' \
                                   f'WHERE title = "{creative_title}";'
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
    def pull_creative_set_id_from_db(creative_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id FROM `rtb-dsp`.creative_sets ' \
                                   f'WHERE title = "{creative_title}";'
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
    def pull_creative_set_data_from_db(creative_set_id, connection):
        title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, status, \
            created_at, updated_at = None, None, None, None, None, None, None, None, None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM `creative_sets` WHERE id = {}'.format(creative_set_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    title = db_result['title']
                    user_id = db_result['user_id']
                    creative_type_id = db_result['creative_type_id']
                    creative_count = db_result['creative_count']
                    duplicate_count = db_result['duplicate_count']
                    is_reserved = db_result['is_reserved']
                    status = db_result['status']
                    created_at = db_result['created_at']
                    updated_at = db_result['updated_at']
                return title, user_id, creative_type_id, creative_count, duplicate_count, is_reserved, \
                    status, created_at, updated_at
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_creative_data_from_db(creative_id, connection):
        title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, created_at, \
            updated_at = None, None, None, None, None, None, None, None, None, None, None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM `creatives` WHERE id = {}'.format(creative_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    title = db_result['title']
                    user_id = db_result['user_id']
                    creative_set_id = db_result['creative_set_id']
                    type_id = db_result['type_id']
                    subtype_id = db_result['subtype_id']
                    is_reserved = db_result['is_reserved']
                    status = db_result['status']
                    width = db_result['width']
                    height = db_result['height']
                    created_at = db_result['created_at']
                    updated_at = db_result['updated_at']
                return title, user_id, creative_set_id, type_id, subtype_id, is_reserved, status, width, height, \
                    created_at, updated_at
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None

    @staticmethod
    def pull_creative_data_from_creative_assets_db_table(creative_id, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT * FROM `creative_assets` WHERE creative_id = {}'.format(creative_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                return db_results
            else:
                return None
        except Exception as e:
            print("Error in DB Connection", e)
            return None
