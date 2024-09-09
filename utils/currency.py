
class CurrencyUtils:

    @staticmethod
    def pull_currency_rate_data_db(currency_ids, connection):
        currency_rates = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT currency_rate_usd, markup_amount FROM billing_currency_rates WHERE ' \
                                    'currency_id in (' + currency_ids + ') ORDER BY currency_id'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['currency_rate_usd'] = float(
                        db_result['currency_rate_usd'])
                    db_result['markup_amount'] = float(
                        db_result['markup_amount'])
                    currency_rate_markup = (db_result[
                                                'currency_rate_usd'] *
                                            db_result[
                                                'markup_amount']) / 100
                    currency_rate = db_result[
                                        'currency_rate_usd'] + currency_rate_markup
                    currency_rates.append(currency_rate)
                return currency_rates
            else:
                return currency_rates
        except Exception as e:
            print("Error in DB Connection", e)
            return currency_rates

    @staticmethod
    def pull_specific_currency_rate_data_db(currency_id, connection):
        currency_rate = 0
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT currency_rate_usd, markup_amount FROM billing_currency_rates WHERE ' \
                                    'currency_id = ' + str(
                    currency_id) + ''
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['currency_rate_usd'] = float(
                        db_result['currency_rate_usd'])
                    db_result['markup_amount'] = float(
                        db_result['markup_amount'])
                    currency_rate_markup = (db_result[
                                                'currency_rate_usd'] *
                                            db_result[
                                                'markup_amount']) / 100
                    currency_rate = db_result[
                                        'currency_rate_usd'] + currency_rate_markup
                return currency_rate
            else:
                return currency_rate
        except Exception as e:
            print("Error in DB Connection", e)
            return currency_rate
