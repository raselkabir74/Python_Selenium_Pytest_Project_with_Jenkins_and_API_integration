class SitesCategoriesUtils:

    @staticmethod
    def pull_sites_categories_id_from_db(connection, site_category_name):
        db_result = None
        try:
            with connection.cursor() as cursor:
                sql_select_query = "SELECT id FROM sites_categories WHERE title = '{}'".format(site_category_name)
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
