from configurations import generic_modules


class CompareUtils:

    @staticmethod
    def verify_data(pulled_data_gui, provided_data_gui, pulled_data_db="",
                    expected_data_db="", db_verification=False):
        if generic_modules.ordered(
                pulled_data_gui) == generic_modules.ordered(
                provided_data_gui):
            if db_verification:
                if pulled_data_db is None:
                    return "Unable to retrieve data from DB"
                elif generic_modules.ordered(
                        expected_data_db) == generic_modules.ordered(
                        pulled_data_db):
                    return "All data verification is successful"
                else:
                    return "Database verification has been failed", pulled_data_gui, pulled_data_db
            else:
                return "All data verification is successful"
        else:
            return "Gui data verification has been failed", pulled_data_gui, provided_data_gui
