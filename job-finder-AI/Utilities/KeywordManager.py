import os
from Storage.LocalStorage import LocalStorage
from DataStructures.Keyword import Keyword


class KeywordManager:
    def __init__(self):
        self.keywords_path = os.path.join('Storage', 'config', 'keywords')
        self.keyword_names = LocalStorage.get_keyword_names()
        self.totals = self.load_totals()
        self.keywords = self.load_keywords()

    def load_keywords(self):
        keyword_dict_path = os.path.join(self.keywords_path, 'keyword_dict.json')
        keyword_dict = LocalStorage.get_json_data(keyword_dict_path)
        keywords = []
        total_jobs_passed = self.get_total_jobs_passed()
        total_jobs_failed = self.get_total_jobs_failed()
        for keyword_name in self.keyword_names:
            passed_count = keyword_dict[keyword_name]['passed']
            failed_count = keyword_dict[keyword_name]['failed']
            keyword = Keyword(keyword_name, passed_count, failed_count, total_jobs_passed, total_jobs_failed)
            keywords.append(keyword)
        return keywords

    def load_totals(self):
        totals_path = os.path.join(self.keywords_path, 'totals.json')
        totals = LocalStorage.get_json_data(totals_path)
        return totals

    def get_keywords(self):
        return self.keywords

    def update_data(self, keywords, jobs_passed, jobs_failed):
        self.keywords = keywords
        self.set_total_jobs_passed(jobs_passed)
        self.set_total_jobs_failed(jobs_failed)
        self.save_data()

    def save_data(self):
        keywords_path = os.path.join(self.keywords_path, 'keyword_dict.json')
        keyword_dict = self.encode_keywords_to_dict()
        LocalStorage.store_json_data(keywords_path, keyword_dict)
        totals_path = os.path.join(self.keywords_path, 'totals.json')
        LocalStorage.store_json_data(totals_path, self.totals)

    def encode_keywords_to_dict(self):
        keyword_dict = {}
        for keyword in self.keywords:
            name = keyword.get_name()
            keyword_dict[name] = {}
            keyword_dict[name]['passed'] = keyword.get_pass_count()
            keyword_dict[name]['failed'] = keyword.get_fail_count()
        return keyword_dict

    def clear_data(self):
        self.clear_totals()
        for keyword in self.keywords:
            keyword.clear_data()

    def clear_totals(self):
        self.set_total_jobs_passed(0)
        self.set_total_jobs_failed(0)

    def get_keyword_names(self):
        return self.keyword_names

    def get_total_jobs_passed(self):
        return self.totals['passed']

    def get_total_jobs_failed(self):
        return self.totals['failed']

    def get_total_jobs(self):
        return self.get_total_jobs_passed() + self.get_total_jobs_failed()

    def get_job_pass_probability(self):
        return self.get_total_jobs_passed() / self.get_total_jobs()

    def get_job_fail_probability(self):
        return self.get_total_jobs_failed() / self.get_total_jobs()

    def set_total_jobs_passed(self, total):
        self.totals['passed'] = total

    def set_total_jobs_failed(self, total):
        self.totals['failed'] = total

    def set_keyword_probabilities(self):
        number_jobs_passed = self.get_total_jobs_failed()
        number_jobs_failed = self.get_total_jobs_failed()
        for keyword in self.keywords:
            keyword.set_pass_probability(number_jobs_passed)
            keyword.set_fail_probability(number_jobs_failed)
