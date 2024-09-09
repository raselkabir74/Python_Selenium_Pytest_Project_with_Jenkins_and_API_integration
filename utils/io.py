import json
from collections import defaultdict

from collections import Counter

from configurations import generic_modules


class IoUtils:

    @staticmethod
    def pull_open_ios_from_db(connection):
        open_ios = []
        io_amounts = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = ' SELECT io.* FROM io io LEFT JOIN invoice_ios ii ON ii.io_id = io.id LEFT JOIN ' \
                                   'invoices i ON i.id = ii.invoice_id LEFT JOIN io_proforma ip ON ip.io_id = io.id' \
                                   ' WHERE i.invoice_number IS NULL AND ip.invoice_status NOT IN (1,4) AND ' \
                                   'io.company_id = 9718 AND (io.status != 1 OR io.status IS NULL) AND ' \
                                   'io.invoice_status NOT IN (4,1,6) AND io.io_number IS NOT NULL AND ip.paid = ' \
                                   '0 GROUP BY io.id'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['io_number'] = float(
                        db_result['io_number'])
                    db_result['total'] = db_result['total']
                    open_ios.append(db_result['io_number'])
                    io_amounts.append(db_result['total'])
                return open_ios, io_amounts
            else:
                return open_ios, io_amounts
        except Exception as e:
            print("Error in DB Connection", e)
            return open_ios, io_amounts

    @staticmethod
    def pull_finance_balances_from_db(connection):
        balances = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT i.id, DATE_ADD(i.date, INTERVAL i.payment_term DAY) due_date, ' \
                                   'i.currency_rate, ipa.balance/i.currency_rate as balance FROM io `io` ' \
                                   'INNER JOIN invoice_ios ii ' \
                                   'ON ii.io_id = io.id INNER JOIN invoices i ON i.id = ii.invoice_id INNER ' \
                                   'JOIN users_admin ua ON `i`.client_id = ua.id LEFT JOIN invoice_campaigns ic ' \
                                   'ON `i`.id = ic.invoice_id LEFT JOIN io_proforma ip ON ip.io_id = io.id LEFT ' \
                                   'JOIN companies cou ON i.company_id = cou.id LEFT JOIN campaigns c ON ' \
                                   'ic.campaign_id = c.id LEFT JOIN currencies cu ON i.currency_id = cu.id ' \
                                   'LEFT JOIN company_profiles cp ON `i`.company_profile = cp.id LEFT JOIN ' \
                                   'company_profiles cp2 ON i.company_profile = cp2.id LEFT JOIN ' \
                                   'invoice_payment_log ipls ON ipls.id = i.id AND ipls.type = "invoice" LEFT ' \
                                   'JOIN invoice_proforma_aggregator ipa ON ipa.item_id = i.id AND ipa.type = ' \
                                   '"invoice" WHERE (io.status != 1 OR io.status IS NULL) AND (i.status != 1 OR ' \
                                   'i.status IS NULL) AND cou.id = 9718 AND i.invoice_number IS NOT NULL GROUP ' \
                                   'BY i.id UNION ALL SELECT ip.id, DATE_ADD(ip.date, INTERVAL ' \
                                   'ip.payment_term DAY) due_date, ip.currency_rate, ipa.balance FROM io ' \
                                   '`io` INNER JOIN io_proforma ip ON `io`.id = ip.io_id INNER JOIN ' \
                                   'users_admin ua ON `ip`.client_id = ua.id LEFT JOIN invoice_ios ii ' \
                                   'ON ii.io_id = io.id LEFT JOIN invoices i ON i.id = ii.invoice_id LEFT ' \
                                   'JOIN io_proforma_campaigns ic ON `ip`.id = ic.proforma_id LEFT JOIN ' \
                                   'companies cou ON ip.company_id = cou.id LEFT JOIN campaigns c ON ' \
                                   'ic.campaign_id = c.id LEFT JOIN currencies cu ON ip.currency_id = ' \
                                   'cu.id LEFT JOIN company_profiles cp ON `ip`.company_profile = ' \
                                   'cp.id LEFT JOIN company_profiles cp2 ON ip.company_profile = cp2.id ' \
                                   'LEFT JOIN invoice_payment_log ipls ON ipls.id = ip.id AND ipls.type = ' \
                                   '"proforma" LEFT JOIN invoice_proforma_aggregator ipa ON ipa.item_id = ' \
                                   'ip.id AND ipa.type = "proforma" WHERE ip.invoice_status IN (1,4) AND ' \
                                   '(i.status != 1 OR i.status IS NULL) AND (ip.status != 1 OR ' \
                                   'ip.status IS NULL) AND cou.id = 9718 AND i.invoice_number IS ' \
                                   'NULL GROUP BY ip.id ORDER BY `id` DESC'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['balance'] = float(
                        db_result['balance'])
                    balances.append(db_result['balance'])
                return balances
            else:
                return balances
        except Exception as e:
            print("Error in DB Connection", e)
            return balances

    @staticmethod
    def pull_campaign_id_which_has_large_spent_amount_from_db(connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT cpr.campaign_id FROM campaign_performance_report_campaign cpr LEFT JOIN ' \
                                   'campaigns c ON c.id = cpr.campaign_id WHERE c.user_id = 1187 and c.status = 7 ' \
                                   'GROUP BY c.id HAVING SUM(cpr.spent) > 100 LIMIT 1'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['campaign_id']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_spent_and_spent_alt_for_specific_campaign_from_db(campaign_id,
                                                               currency_rate,
                                                               connection):
        spent = None
        spent_alt = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT ROUND(SUM(cpr.spent * {}), 2) \'c\', ' \
                                   'ROUND(SUM(cpr.spent_alt_currency), 2) \'r\' FROM ' \
                                   r'campaign_performance_report_campaign cpr ' \
                                   r'WHERE cpr.campaign_id >= 100 AND cpr.campaign_id IN ({})'.format(
                    currency_rate,
                    campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['c'] = float(db_result['c'])
                    db_result['r'] = float(db_result['r'])
                    spent = db_result['c']
                    spent_alt = db_result['r']
                return spent, spent_alt
            else:
                return spent, spent_alt
        except Exception as e:
            print("Error in DB Connection", e)
            return spent, spent_alt

    @staticmethod
    def pull_spent_and_spent_alt_data_for_specific_campaign_from_db(
            campaign_id, currency_rate, connection):
        spent = None
        spent_alt = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT ROUND(SUM(cpr.spent * {}), 2) \'c\', ' \
                                   'ROUND(SUM(cpr.spent_alt), 2) \'r\' FROM ' \
                                   r'campaign_performance_report_campaign cpr ' \
                                   r'WHERE cpr.campaign_id >= 100 AND cpr.campaign_id IN ({})'.format(
                    currency_rate,
                    campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['c'] = float(db_result['c'])
                    db_result['r'] = float(db_result['r'])
                    spent = db_result['c']
                    spent_alt = db_result['r']
                return spent, spent_alt
            else:
                return spent, spent_alt
        except Exception as e:
            print("Error in DB Connection", e)
            return spent, spent_alt

    @staticmethod
    def pull_margin_main_for_specific_campaign_from_db(campaign_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT margin_main FROM campaigns WHERE id = \'{}\''.format(
                    campaign_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = float(db_results[0]['margin_main'])
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_agency_margin_for_specific_user_id_from_db(user_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT agency_margin FROM users_admin where id = \'{}\''.format(
                    user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = float(
                    db_results[0]['agency_margin'])
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_feedback_email_status_from_db(io_number, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT feedback_email FROM io WHERE `io_number`= {}'.format(
                    int(io_number))
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['feedback_email']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def get_signed_status_from_db(io_number, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT signed FROM io WHERE `io_number`= {}'.format(
                    int(io_number))
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchone()
            if db_results:
                db_result = db_results['signed']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_account_manager_from_db(io_data, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT ua2.name FROM `rtb-dsp`.users_admin ua JOIN' \
                                   '`rtb-dsp`.users_admin ua2 ON ua.account_manager = ua2.id' \
                                   f' WHERE ua.name = "{io_data}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['name']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_date_from_db(campaign_name, connection,
                                   date_type='start'):
        if date_type not in ['start', 'end']:
            raise ValueError(
                "Invalid date_type. Use 'start' or 'end'.")
        db_result = None
        try:
            with connection.cursor() as cursor:
                date_column = 'targeting_date_from' if date_type == 'start' else 'targeting_date_to'
                sql_select_query = f'SELECT {date_column} FROM `rtb-dsp`.campaigns ' \
                                   f'WHERE name = "{campaign_name}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0][date_column]
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_status_from_db(campaign_name, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT campaign_statuses.title FROM `rtb-dsp`.campaign_statuses ' \
                                   'INNER JOIN `rtb-dsp`.campaigns ON campaigns.status = campaign_statuses.id ' \
                                   f'WHERE campaigns.name = "{campaign_name}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['title']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaigns_names_from_db(io_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT io_aggregator.io_campaigns_name FROM `rtb-dsp`.io ' \
                                   'JOIN `rtb-dsp`.io_aggregator ON io.id = io_aggregator.io_id ' \
                                   f'WHERE title = "{io_title}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['io_campaigns_name']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_invoice_status_from_db(io_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = f'SELECT invoice_status FROM `rtb-dsp`.io WHERE title = "{io_title}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['invoice_status']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_io_amount_from_db(io_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT io_aggregator.io_amount_usd FROM `rtb-dsp`.io ' \
                                   'JOIN `rtb-dsp`.io_aggregator ON io.id = io_aggregator.io_id ' \
                                   f'WHERE title = "{io_title}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['io_amount_usd']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_spent_from_db(io_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT io_aggregator.io_campaigns_spent_rmt_usd FROM `rtb-dsp`.io ' \
                                   'JOIN `rtb-dsp`.io_aggregator ON io.id = io_aggregator.io_id ' \
                                   f'WHERE title = "{io_title}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0][
                    'io_campaigns_spent_rmt_usd']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_io_date_from_db(io_title, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = f'SELECT date FROM `rtb-dsp`.io WHERE title = "{io_title}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['date']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_campaign_with_specific_status_from_db(connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT id, name FROM `rtb-dsp`.campaigns ' \
                                   'WHERE status = "12" and user_id = "1187" ' \
                                   'AND targeting_date_to > CURDATE() LIMIT 1;'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_io_campaign_status_from_db(io_number, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT io_campaign_status_title FROM `rtb-dsp`.io_aggregator ' \
                                   f'WHERE io_id = (SELECT id FROM `rtb-dsp`.io WHERE io_number = {io_number});'
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                db_result = db_results[0]['io_campaign_status_title']
                return db_result
            else:
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_email_reports_settings_from_db(io_number, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT iser.view_by, iser.attachments, iser.frequency, iser.hour, ' \
                                   'iser.weekday, iser.status  FROM `rtb-dsp`.io_settings_email_reports iser ' \
                                   f'JOIN `rtb-dsp`.io i ON iser.io_id = i.id WHERE i.io_number = {io_number};'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_io_which_have_expected_amount_of_spent(io_campaign_status_title, last_month_first_date,
                                                    last_month_last_date, connection, compare_sign='>',
                                                    company_list_to_exclude=None):
        attempts = 0
        ids_with_multiple_country = ''
        if compare_sign != '>':
            compare = " BETWEEN 1 AND 40"
        else:
            compare = " > 50"
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                with connection.cursor() as cursor:
                    sql_select_query = """
                        SELECT io.id, io.country_row, c.country, ia.io_campaign_status_title, ia.client_company_name,
                        IFNULL(
                            SUM(
                                IF(c.margin_main > 0 AND u.agency_margin > 0,
                                    r.spent_alt_currency + (r.spent_alt_currency / (1 - c.margin_main / 100) - r.spent_alt_currency) * u.agency_margin / 100,
                                    r.spent_alt_currency)
                            ), 0) AS campaign_spent,
                        IFNULL(
                            SUM(
                                IF(c.margin_main > 0 AND u.agency_margin > 0,
                                    r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                    r.spent_alt)
                            ), 0) AS campaign_spent_usd,
                        (IFNULL(
                            SUM(
                                IF(c.margin_main > 0 AND u.agency_margin > 0,
                                    r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                    r.spent_alt)
                            ), 0)) * io.currency_rate AS campaign_spent_io_currency,
                        SUM(r.impressions) AS impressions
                        FROM io
                        LEFT JOIN io_campaigns AS ioc ON ioc.io_id = io.id
                        LEFT JOIN campaign_performance_report_campaign AS r ON r.campaign_id = ioc.campaign_id
                        LEFT JOIN campaigns AS c ON c.id = ioc.campaign_id
                        LEFT JOIN users_admin AS u ON u.id = c.user_id
                        LEFT JOIN io_aggregator AS ia ON ia.io_id = io.id
                        WHERE ia.io_campaign_status_title IS NOT NULL AND ia.io_campaign_status_title = '{}'
                        AND r.date BETWEEN '{}' AND '{}'
                        AND io.date >= '2023-01-01'
                        AND io.status = 0
                        AND io.paid_status != 1
                        AND ia.io_left >= 50
                        GROUP BY io.id
                        HAVING campaign_spent_usd {}
                        """.format(io_campaign_status_title, last_month_first_date, last_month_last_date, compare)
                    cursor.execute(sql_select_query)
                    db_result = cursor.fetchall()

                    if company_list_to_exclude is not None:
                        db_results = [entry for entry in db_result if
                                      entry['client_company_name'] not in company_list_to_exclude]
                    else:
                        db_results = db_result

                    id_country_dict = {}
                    for item in db_results:
                        dic_id = item['id']
                        country_row = json.loads(item['country_row'])
                        if dic_id not in id_country_dict:
                            id_country_dict[dic_id] = set()
                        for country_code in country_row:
                            id_country_dict[dic_id].add(country_code)

                    ids_with_multiple_countries = [dic_id for dic_id, countries in id_country_dict.items() if
                                                   len(countries) > 1]
                    if ids_with_multiple_countries:
                        ids_with_multiple_country = str(ids_with_multiple_countries[0])

                    if not ids_with_multiple_country:
                        for row in db_results:
                            countries = [country.strip('" ') for country in row['country_row'].strip('[]').split(',')]
                            country_counts = Counter(countries)
                            if any(count > 1 for count in country_counts.values()):
                                ids_with_multiple_country = str(row['id'])
                                break

                    if ids_with_multiple_country:
                        return ids_with_multiple_country
                    elif attempts == generic_modules.MYSQL_MAX_RETRY - 1:
                        return db_results[0]['id']

                    attempts += 1
            except Exception as e:
                print("Error in DB Connection:", e)
                attempts += 1

        return ids_with_multiple_country

    @staticmethod
    def pull_io_from_specific_user_which_have_expected_amount_of_spent(io_campaign_status_title,
                                                                       client_name, last_month_first_date,
                                                                       last_month_last_date, connection,
                                                                       compare_sign='>'):
        attempts = 0
        ids_with_multiple_country = ''
        if compare_sign != '>':
            compare = " BETWEEN 1 AND 50"
        else:
            compare = " > 50"
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                with connection.cursor() as cursor:
                    sql_select_query = """
                        SELECT io.id, io.country_row, c.country, ia.io_campaign_status_title,
                        IFNULL(
                            SUM(
                                IF(c.margin_main > 0 AND u.agency_margin > 0,
                                    r.spent_alt_currency + (r.spent_alt_currency / (1 - c.margin_main / 100) - r.spent_alt_currency) * u.agency_margin / 100,
                                    r.spent_alt_currency)
                            ), 0) AS campaign_spent,
                        IFNULL(
                            SUM(
                                IF(c.margin_main > 0 AND u.agency_margin > 0,
                                    r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                    r.spent_alt)
                            ), 0) AS campaign_spent_usd,
                        (IFNULL(
                            SUM(
                                IF(c.margin_main > 0 AND u.agency_margin > 0,
                                    r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                    r.spent_alt)
                            ), 0)) * io.currency_rate AS campaign_spent_io_currency,
                        SUM(r.impressions) AS impressions
                        FROM io
                        LEFT JOIN io_campaigns AS ioc ON ioc.io_id = io.id
                        LEFT JOIN campaign_performance_report_campaign AS r ON r.campaign_id = ioc.campaign_id
                        LEFT JOIN campaigns AS c ON c.id = ioc.campaign_id
                        LEFT JOIN users_admin AS u ON u.id = c.user_id
                        LEFT JOIN io_aggregator AS ia ON ia.io_id = io.id
                        WHERE ia.`client_name` = '{}' AND ia.io_campaign_status_title IS NOT NULL
                        AND ia.io_campaign_status_title = '{}'
                        AND r.date BETWEEN '{}' AND '{}'
                        AND io.date >= '2023-01-01'
                        AND io.status = 0
                        AND io.paid_status != 1
                        AND ia.io_left >= 50
                        GROUP BY io.id
                        HAVING campaign_spent_usd {}
                        """.format(client_name, io_campaign_status_title, last_month_first_date, last_month_last_date,
                                   compare)
                    cursor.execute(sql_select_query)
                    db_result = cursor.fetchall()

                    id_country_dict = {}
                    for item in db_result:
                        dic_id = item['id']
                        country_row = json.loads(item['country_row'])
                        if dic_id not in id_country_dict:
                            id_country_dict[dic_id] = set()
                        for country_code in country_row:
                            id_country_dict[dic_id].add(country_code)

                    ids_with_multiple_countries = [dic_id for dic_id, countries in id_country_dict.items() if
                                                   len(countries) > 1]
                    if ids_with_multiple_countries:
                        ids_with_multiple_country = str(ids_with_multiple_countries[0])

                    if not ids_with_multiple_country:
                        for row in db_result:
                            countries = [country.strip('" ') for country in row['country_row'].strip('[]').split(',')]
                            country_counts = Counter(countries)
                            if any(count > 1 for count in country_counts.values()):
                                ids_with_multiple_country = str(row['id'])
                                break

                    if ids_with_multiple_country:
                        return ids_with_multiple_country
                    elif attempts == generic_modules.MYSQL_MAX_RETRY - 1:
                        return db_result[0]['id']

                    attempts += 1
            except Exception as e:
                print("Error in DB Connection:", e)
                attempts += 1

        return ids_with_multiple_country

    @staticmethod
    def pull_country_wise_actual_io_campaign_spent(io_number, connection):
        attempts = 0
        data_dict = {}
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                with connection.cursor() as cursor:
                    sql_select_query = """
                                SELECT io.id, c.country, IFNULL( SUM(IF(c.`margin_main` > 0 AND u.`agency_margin` > 0,
                                r.`spent_alt_currency` + (r.`spent_alt_currency` / (1 - c.`margin_main` / 100) - r.`spent_alt_currency`) * u.`agency_margin` / 100,
                                r.`spent_alt_currency`)), 0) as campaign_spent, IFNULL( SUM(IF(c.`margin_main` > 0 AND u.`agency_margin` > 0, r.`spent_alt` +
                                (r.`spent_alt` / (1 - c.`margin_main` / 100) - r.`spent_alt`) * u.`agency_margin` / 100, r.`spent_alt`)), 0) as campaign_spent_usd,
                                (IFNULL( SUM(IF(c.`margin_main` > 0 AND u.`agency_margin` > 0, r.`spent_alt` + (r.`spent_alt` / (1 - c.`margin_main` / 100) -
                                r.`spent_alt`) * u.`agency_margin` / 100, r.`spent_alt`)), 0)) * io.currency_rate as campaign_spent_io_currency,
                                SUM(r.impressions) as impressions from `io` as `io` left join `io_campaigns` as `ioc` on `ioc`.`io_id` = `io`.`id`
                                left join `campaign_performance_report_campaign` as `r` on `r`.`campaign_id` = `ioc`.`campaign_id` left join
                                `campaigns` as `c` on `c`.`id` = `ioc`.`campaign_id` left join `users_admin` as `u` on `u`.`id` = `c`.`user_id`
                                where `io`.`id` in ({}) group by `io`.`id`, `c`.`country`;
                                """.format(io_number)
                    cursor.execute(sql_select_query)
                    db_results = cursor.fetchall()
                if db_results:
                    for db_result in db_results:
                        db_result = dict(db_result)
                        campaign_spent = db_result['campaign_spent']
                        data_dict[db_result['country']] = campaign_spent
                    return data_dict
                else:
                    attempts += 1
            except Exception as e:
                print("Error in DB Connection:", e)
                attempts += 1

        return data_dict

    @staticmethod
    def pull_io_invoice(io_id, connection, is_list=False):
        invoice_list = []
        try:
            with connection.cursor() as cursor:
                if is_list:
                    sql_select_query = "SELECT invoice_id FROM invoice_ios WHERE io_id IN ({})".format(', '.join(str(
                        io) for io in io_id))
                else:
                    sql_select_query = "SELECT invoice_id from invoice_ios where io_id IN ({})".format(io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    invoice_list.append(db_result['invoice_id'])
                return invoice_list
            else:
                return invoice_list
        except Exception as e:
            print("Error in DB Connection:", e)
            return invoice_list

    @staticmethod
    def pull_total_invoice_amount(invoice_id, connection):
        total = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT total FROM invoice_ios WHERE invoice_id = {}".format(invoice_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()

            # Assuming db_results is a list containing a single dictionary
            for db_result in db_results:
                total_string = db_result['total']
                total_list = eval(total_string)
                total = sum(float(val) for val in total_list)
                return total
        except Exception as e:
            print("Error in DB Connection:", e)
            return total

    @staticmethod
    def pull_io_company_name_and_id(io_id, connection):
        client_company_name = ''
        client_company_id = ''
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT client_company_name, client_company_id FROM io_aggregator WHERE " \
                                   "io_id = {}".format(io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    client_company_id = db_result['client_company_id']
                    client_company_name = db_result['client_company_name']
                return str(client_company_id), client_company_name
            else:
                return client_company_id, client_company_name
        except Exception as e:
            print("Error in DB Connection:", e)
            return client_company_id, client_company_name

    @staticmethod
    def pull_io_currency(io_id, connection):
        io_currency = ""
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT io_currency FROM io_aggregator WHERE io_id = {}".format(io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                io_currency = db_result[0]['io_currency']
            return str(io_currency)
        except Exception as e:
            print("Error in DB Connection:", e)
            return str(io_currency)

    @staticmethod
    def pull_user_id(user_name, connection):
        user_id = ""
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT ua.id FROM users_admin ua WHERE ua.name = '{}'".format(user_name)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                user_id = db_result[0]['id']
            return user_id
        except Exception as e:
            print("Error in DB Connection:", e)
            return user_id

    @staticmethod
    def pull_users_spent_alt_and_spent_alt_currency(last_month_first_date, last_month_last_date, user_id, connection,
                                                    spent_alt=False):
        spent_amount = ""
        if spent_alt:
            spent_alt_str = 'spent_alt'
        else:
            spent_alt_str = 'spent_alt_currency'
        try:
            with connection.cursor() as cursor:
                sql_select_query = """SELECT c.user_id,
                   IFNULL(SUM(IF(c.`margin_main` > 0 AND u.`agency_margin` > 0, r.`{}` +
                   (r.`{}` / (1 - c.`margin_main` / 100) - r.`{}`) *
                   u.`agency_margin` / 100, r.`{}`)), 0) AS spent FROM
                   campaign_performance_report_campaign r
                   LEFT JOIN campaigns c ON c.id = r.campaign_id LEFT JOIN users_admin u ON u.id = c.user_id
                   WHERE  r.date BETWEEN '{}' AND '{}' AND c.id > 10000 AND u.id={}
                   GROUP  BY c.user_id""".format(spent_alt_str, spent_alt_str, spent_alt_str, spent_alt_str,
                                                 last_month_first_date, last_month_last_date, user_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                spent_amount = db_result[0]['spent']
            return spent_amount
        except Exception as e:
            print("Error in DB Connection:", e)
            return spent_amount

    @staticmethod
    def pull_io_ids_which_were_created_last_month_last_date(company_id, last_month_last_date, connection):
        ios = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT id FROM io WHERE date IN ('{}') AND company_id = {}".format(
                    last_month_last_date, company_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    ios.append(db_result['id'])
                return ios
            else:
                return ios
        except Exception as e:
            print("Error in DB Connection:", e)
            return ios

    @staticmethod
    def pull_io_client_name(io_id, connection):
        client_name = ''
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT client_name FROM io_aggregator WHERE io_id = {}".format(io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            if db_results:
                for db_result in db_results:
                    db_result = dict(db_result)
                    client_name = db_result['client_name']
                return client_name
            else:
                return client_name
        except Exception as e:
            print("Error in DB Connection:", e)
            return client_name

    @staticmethod
    def pull_io_id(io_number, connection, io_title=""):
        db_result = None
        try:
            with connection.cursor() as cursor:
                if io_title == "":
                    sql_select_query = 'SELECT id FROM io WHERE io_number = {}'.format(io_number)
                else:
                    sql_select_query = "SELECT id FROM io WHERE title = '{}'".format(io_title)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                db_result = db_result['id']
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_io_number(io_id, connection):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT io_number FROM io WHERE id = {}'.format(io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                db_result = db_result['io_number']
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
            return db_result

    @staticmethod
    def pull_io_campaigns(io_id, connection):
        campaign_ids = []
        try:
            with connection.cursor() as cursor:
                sql_select_query = 'SELECT campaign_id FROM io_campaigns WHERE io_id = {}'.format(io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_results = cursor.fetchall()
            for campaign_id in db_results:
                campaign_ids.append(campaign_id['campaign_id'])
            return campaign_ids
        except Exception as e:
            print("Error in DB Connection", e)
            return campaign_ids

    @staticmethod
    def pull_spent_amount_from_io_campaigns(campaign_ids, connection, spent_alt=False):
        spent = None
        if spent_alt:
            spent_alt_str = 'spent_alt'
        else:
            spent_alt_str = 'spent_alt_currency'
        try:
            with connection.cursor() as cursor:
                sql_select_query = """SELECT c.user_id,
                            IFNULL(SUM(IF(c.`margin_main` > 0 AND u.`agency_margin` > 0, r.`{}` +
                            (r.`{}` / (1 - c.`margin_main` / 100) - r.`{}`) *
                            u.`agency_margin` / 100, r.`{}`)), 0) AS spent
                            FROM campaign_performance_report_campaign r LEFT JOIN campaigns c ON c.id =
                            r.campaign_id LEFT JOIN users_admin u ON u.id = c.user_id  WHERE c.id > 10000 AND c.id in
                            ({}) GROUP  BY c.user_id""".format(spent_alt_str, spent_alt_str, spent_alt_str,
                                                               spent_alt_str, campaign_ids)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                spent = db_result['spent']
            return spent
        except Exception as e:
            print("Error in DB Connection", e)
            return spent

    @staticmethod
    def pull_last_month_spent_for_specific_io(io_id, last_month_first_date, last_month_last_date, connection,
                                              io_revenue_margin=False):
        last_month_spent = None
        if io_revenue_margin:
            io_revenue_margin_str = 'io_revenue_margin'
        else:
            io_revenue_margin_str = 'io_revenue_margin_currency'
        try:
            with connection.cursor() as cursor:
                sql_select_query = """SELECT {} as io_revenue_margin FROM io_aggregator_monthly WHERE date =
                '{}' AND '{}' AND io_id = {};""".format(io_revenue_margin_str, last_month_first_date,
                                                        last_month_last_date, io_id)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            if db_result:
                last_month_spent = db_result['io_revenue_margin']
            return last_month_spent
        except Exception as e:
            print("Error in DB Connection", e)
            return last_month_spent

    @staticmethod
    def pull_ios_from_one_company_multi_users_which_have_expected_amount_of_spent(io_campaign_status_title,
                                                                                  last_month_first_date,
                                                                                  last_month_last_date, connection,
                                                                                  compare_sign='>'):
        attempts = 0
        results = {}
        if compare_sign != '>':
            compare = " BETWEEN 1 AND 50"
        else:
            compare = " > 50"
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                with connection.cursor() as cursor:
                    sql_select_query = """
                            SELECT io.id, io.country_row, c.country, ia.io_campaign_status_title, ia.client_name,
                            ia.client_company_name,
                            IFNULL(
                                SUM(
                                    IF(c.margin_main > 0 AND u.agency_margin > 0,
                                        r.spent_alt_currency + (r.spent_alt_currency / (1 - c.margin_main / 100) - r.spent_alt_currency) * u.agency_margin / 100,
                                        r.spent_alt_currency)
                                ), 0) AS campaign_spent,
                            IFNULL(
                                SUM(
                                    IF(c.margin_main > 0 AND u.agency_margin > 0,
                                        r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                        r.spent_alt)
                                ), 0) AS campaign_spent_usd,
                            (IFNULL(
                                SUM(
                                    IF(c.margin_main > 0 AND u.agency_margin > 0,
                                        r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                        r.spent_alt)
                                ), 0)) * io.currency_rate AS campaign_spent_io_currency,
                            SUM(r.impressions) AS impressions
                            FROM io
                            LEFT JOIN io_campaigns AS ioc ON ioc.io_id = io.id
                            LEFT JOIN campaign_performance_report_campaign AS r ON r.campaign_id = ioc.campaign_id
                            LEFT JOIN campaigns AS c ON c.id = ioc.campaign_id
                            LEFT JOIN users_admin AS u ON u.id = c.user_id
                            LEFT JOIN io_aggregator AS ia ON ia.io_id = io.id
                            WHERE ia.io_campaign_status_title IS NOT NULL AND ia.io_campaign_status_title = '{}'
                            AND r.date BETWEEN '{}' AND '{}'
                            AND io.date >= '2023-01-01'
                            AND io.status = 0
                            AND io.paid_status != 1
                            AND ia.io_left >= 50
                            GROUP BY io.id
                            HAVING campaign_spent_usd {}
                            """.format(io_campaign_status_title, last_month_first_date, last_month_last_date, compare)
                    cursor.execute(sql_select_query)
                    db_results = cursor.fetchall()

                    # Step 1: Group by client_company_name
                    company_to_names = defaultdict(lambda: defaultdict(list))
                    for io in db_results:
                        company_to_names[io['client_company_name']][io['client_name']].append(
                            io['id'])

                    # Step 2: Filter those with more than one unique client_name
                    for company_name, names in company_to_names.items():
                        if len(names) > 1:  # More than one unique client_name
                            for client_name, ids in names.items():
                                results[client_name] = ids
                    return results
            except Exception as e:
                print("Error in DB Connection:", e)
                attempts += 1

        return results

    @staticmethod
    def pull_ios_from_one_user_which_have_expected_amount_of_spent(io_client_name, last_month_last_date,
                                                                   connection, compare_sign='>'):
        attempts = 0
        io_ids = []
        campaign_spent_list = []
        io_number_list = []
        if compare_sign != '>':
            compare = " BETWEEN 1 AND 50"
        else:
            compare = " > 50"
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                with connection.cursor() as cursor:
                    sql_select_query = """
                           SELECT io.id, io.io_number, io.country_row, c.country, ia.io_campaign_status_title,
                           ia.client_name,
                           ia.client_company_name,
                           IFNULL(
                               SUM(
                                   IF(c.margin_main > 0 AND u.agency_margin > 0,
                                      r.spent_alt_currency + (r.spent_alt_currency / (1 - c.margin_main / 100) - r.spent_alt_currency) * u.agency_margin / 100,
                                      r.spent_alt_currency)
                               ), 0) AS campaign_spent,
                           IFNULL(
                               SUM(
                                   IF(c.margin_main > 0 AND u.agency_margin > 0,
                                      r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                      r.spent_alt)
                               ), 0) AS campaign_spent_usd,
                           (IFNULL(
                               SUM(
                                   IF(c.margin_main > 0 AND u.agency_margin > 0,
                                      r.spent_alt + (r.spent_alt / (1 - c.margin_main / 100) - r.spent_alt) * u.agency_margin / 100,
                                      r.spent_alt)
                               ), 0)) * io.currency_rate AS campaign_spent_io_currency,
                           SUM(r.impressions) AS impressions
                    FROM io
                    LEFT JOIN io_campaigns AS ioc ON ioc.io_id = io.id
                    LEFT JOIN campaign_performance_report_campaign AS r ON r.campaign_id = ioc.campaign_id
                    LEFT JOIN campaigns AS c ON c.id = ioc.campaign_id
                    LEFT JOIN users_admin AS u ON u.id = c.user_id
                    LEFT JOIN io_aggregator AS ia ON ia.io_id = io.id
                    WHERE ia.io_campaign_status_title IS NOT NULL
                          AND ia.client_name = '{}'
                          AND r.date <= '{}'
                          AND io.date >= '2023-01-01'
                          AND ia.io_campaigns_min_start_date <= '{}'
                          AND io.status = 0
                          AND io.paid_status != 1
                          AND ia.io_left_usd >= 50
                    GROUP BY io.id
                    HAVING campaign_spent_usd {};
                            """.format(io_client_name, last_month_last_date, last_month_last_date, compare)
                    cursor.execute(sql_select_query)
                    db_results = cursor.fetchall()

                    for record in db_results:
                        io_ids.append(record['id'])
                        campaign_spent_list.append(record['campaign_spent'])
                        io_number_list.append(record['io_number'])

                    return io_ids, campaign_spent_list, io_number_list
            except Exception as e:
                print("Error in DB Connection:", e)
                attempts += 1

        return io_ids, campaign_spent_list, io_number_list
