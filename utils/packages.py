import csv


class PackagesUtils:
    @staticmethod
    def read_site_domain_names(operation='add'):
        site_domain_name = []
        if operation == 'edit':
            file_path = 'assets/packages/edit_package_sites_domain.csv'
        else:
            file_path = 'assets/packages/package_sites_domain.csv'
        with open(file_path) as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                site_domain_name.append(row[0])
        return site_domain_name

    @staticmethod
    def pull_package_id_from_db(package_name, connection):
        try:
            with connection.cursor() as cursor:
                sql_select_query = f'SELECT id FROM packages WHERE name = "{package_name}";'
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchall()
                return db_result
        except Exception as e:
            print("Error in DB Connection", e)
