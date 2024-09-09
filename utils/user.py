from configurations import generic_modules


class UserUtils:
    @staticmethod
    def get_bulk_user_url(user_email, connection):
        url = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT hash FROM bulk_user_create_invitation WHERE email = '{}';".format(
                    user_email)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            url = generic_modules.BASE_URL + "/SignUp/createAccountFromInvite?verify_code=" + str(
                db_result['hash'])
            return url
        except Exception as e:
            print("Error in DB Connection", e)
            return url

    @staticmethod
    def get_user_margin(user_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT margin FROM users_admin WHERE id = '{}'".format(
                    user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['margin']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_user_agency_margin(user_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT agency_margin FROM users_admin WHERE id = '{}'".format(
                    user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['agency_margin']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_user_discount_from_db(connection, user_id):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT discount_agency FROM `rtb-dsp`.user_settings_discounts ' \
                                    f'WHERE user_id = "{user_id}" AND period_to >= CURDATE();'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['discount_agency']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_user_vat_from_db(connection, company_profile):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = f'SELECT vat FROM `rtb-dsp`.company_profiles WHERE title = "{company_profile}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['vat']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_payment_term_from_db(client, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT c.payment_term FROM `rtb-dsp`.users_admin ua ' \
                                    'JOIN `rtb-dsp`.companies c ON ua.company_id = c.id ' \
                                    f'WHERE ua.name = "{client}" AND c.id = "9718";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['payment_term']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_user_parent_af_all_users_status(user_name, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT parent_of_all_users FROM users_admin WHERE login = '{}'".format(
                    user_name)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['parent_of_all_users']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result
