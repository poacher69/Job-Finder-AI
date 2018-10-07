import argparse
from JobManager import JobManager
from Storage.LocalStorage import LocalStorage
from Storage.JobDatabase import JobDatabase
from Crawlers import EngineerJobsCrawler
from DataStructures.Listers import EngineerJobsLister
from Utilities import TextFormatter
from Utilities.Stats import Stats


class CLI:
    def __init__(self):
        parser = argparse.ArgumentParser(description='Command line interface for job searcher AI.')
        parser.add_argument('-clear_cache', help='Clear local job cache.', action='store_true')
        parser.add_argument('-clear_database', help='Clear database.', action='store_true')
        parser.add_argument('-crawl', help='Crawl job postings and save them locally.', action='store_true')
        parser.add_argument('-train', help='Train the AI by classifying jobs as passed/failed.', action='store_true')
        parser.add_argument('-classify', help='Show results of classification applied to cache.', action='store_true')
        parser.add_argument('-time', help='Specify how many days to crawl')
        parser.add_argument('-store', help='Store jobs in database.', action='store_true')
        args = parser.parse_args()
        self.args_to_values = vars(args)
        self.storage = LocalStorage()
        self.stats = Stats()
        self.args_to_functions = {'clear_cache': self.clear_cache, 'clear_database': self.clear_database,
                                  'crawl': self.crawl, 'train': self.train, 'classify': self.classify,
                                  'store': self.store}
        self.execute()

    def execute(self):
        for argument in self.args_to_functions:
            argument_provided = self.args_to_values[argument]
            if argument_provided:
                run_function = self.args_to_functions[argument]
                run_function()

    def store(self):
        jobs = self.storage.get_jobs_from_cache()
        db = JobDatabase()
        db.add_jobs(jobs)
        num_jobs = db.get_last_id()
        print('Total number of jobs in database ' + str(num_jobs))

    def classify(self):
        print('Classifying jobs...')
        jobs = self.storage.get_jobs_from_cache()
        for job in jobs:
            score = self.stats.classify(job)
            job.set_score(score)
            if score > 1.0:
                self.print_classify_info(job)

    def crawl(self):
        print('Crawling job postings...')
        time = int(self.args_to_values['time']) if self.args_to_values['time'] else 1
        print('Number of days to crawl: ' + str(time))
        crawler = EngineerJobsCrawler.EngineerJobsCrawler(time)
        lister = EngineerJobsLister.EngineerJobsLister()
        manager = JobManager(crawler, lister)
        jobs = manager.get_jobs()
        print('Saving ' + str(len(jobs)) + ' jobs...')
        self.storage.store_jobs(jobs)

    def train(self):
        print('Starting training session...')
        print('Enter exit to quit.')
        jobs = self.storage.get_jobs_from_database()
        num_jobs = len(jobs)
        current_job = 0
        exit_condition = False
        print('Number of jobs ' + str(num_jobs))
        while not exit_condition:
            job = jobs[current_job]
            self.print_training_info(job)
            user_exit = self.process_job_passed(job)
            exit_condition = user_exit or current_job == num_jobs - 1
            current_job += 1
        self.storage.store_jobs(jobs)

    @staticmethod
    def print_training_info(job):
        job_description = TextFormatter.format_job_description(job.get_plaintext())
        job_title = TextFormatter.format_job_title(job.get_title())
        job_keywords = TextFormatter.format_job_keywords(job.get_keyword_names())
        TextFormatter.multi_print(job_title, job_description, job_keywords)

    @staticmethod
    def print_classify_info(job):
        job_title = TextFormatter.format_job_title(job.get_title())
        job_keywords = TextFormatter.format_job_keywords(job.get_keyword_names())
        job_score = TextFormatter.format_job_score(job.get_score())
        TextFormatter.multi_print(job_title, job_keywords, job_score)

    @staticmethod
    def process_job_passed(job):
        user_exit = False
        job_passed = input('Job passed? y/n ')
        if job_passed == 'y':
            job.set_passed(True)
        elif job_passed == 'n':
            job.set_passed(False)
        else:
            print('Exiting...')
            user_exit = True
        return user_exit

    def clear_cache(self):
        print('Clearing local cache...')
        self.storage.clear_cache()

    def clear_database(self):
        print('Clearing database...')
        self.storage.clear_database()



