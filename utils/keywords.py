import csv


class KeywordsUtils:

    @staticmethod
    def process_keywords_data(brand_safety_data):
        if brand_safety_data['find_url'] == "False":
            brand_safety_data['find_url'] = ""
        if brand_safety_data['find_content'] == "False":
            brand_safety_data['find_content'] = ""
        return brand_safety_data

    @staticmethod
    def get_provided_keyword_list():
        keywords = []
        file_path = 'assets/brand_safety/keywords.csv'
        with open(file_path) as csvfile:
            data = csv.reader(csvfile)
            next(data)
            for row in data:
                keywords.append(row[0])
        return keywords
