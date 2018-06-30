import os  # put some of the IOUtils stuff here - split into networking and local IO (OS stuff)
import pickle
import logging
from nltk import word_tokenize
from enum import Enum


class Path(Enum):
    FILE = 0
    FOLDER = 1
    ALL = 2


class Storage:
    def __init__(self, base_directory):
        self.base_dir = base_directory
        self.jobs_dir = os.path.join(base_directory, 'jobs')
        self.train_dir = os.path.join(base_directory, 'training')
        self.train_pass_dir = os.path.join(self.train_dir, 'pass')
        self.train_fail_dir = os.path.join(self.train_dir, 'fail')
        self.classify_dir = os.path.join(self.jobs_dir, 'classify')
        self.job_file_name = 'job.txt'
        self.job_object_name = 'job.pickle'

    def store_jobs(self, jobs):
        for job in jobs:
            self.store_job(job)

    def store_job(self, job):
        job_dir = os.path.join(self.jobs_dir, job.metadata.id)
        text_file_path = os.path.join(job_dir, self.job_file_name)
        object_file_path = os.path.join(job_dir, self.job_object_name)
        self.create_directory(job_dir)
        self.store_job_text(text_file_path, job)
        self.store_object(object_file_path, job)

    @staticmethod
    def store_object(file_path, obj):
        try:
            with open(file_path, 'wb') as file:
                pickle.dump(obj, file)
        except Exception as e:
            logging.error('Error while pickling: ' + str(e))

    def retrieve_jobs(self):
        job_folders = self.get_folders_from_path(self.jobs_dir)
        jobs = []
        for folder in job_folders:
            pickle_paths = self.get_pickles_in_folder(folder)
            for pickle_path in pickle_paths:
                job = self.retrieve_object(pickle_path)
                jobs.append(job)
        return jobs

    def get_pickles_in_folder(self, folder):
        files = self.get_files_from_path(folder)
        pickles = self.get_files_with_extension(files, extension='.pickle')
        return pickles

    @staticmethod
    def get_files_with_extension(files_in, extension=''):
        files_out = []
        for file in files_in:
            if file.endswith(extension):
                files_out.append(file)
        return files_out

    @staticmethod
    def retrieve_object(file_path):
        obj = None
        try:
            with open(file_path, 'r') as file:
                obj = pickle.load(file)
        except Exception as e:
                logging.error('Error while retrieving object: ' + str(e))
        return obj

    def store_job_text(self, file_path, job):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                self.dump_job_text(file, job)
        except Exception as e:
            logging.error('Error while storing text: ' + str(e))

    def dump_job_text(self, file, job):
        file.write(job.title + '\n')
        for keyword in job.keywords:
            file.write(keyword + ", ")
            file.write('\n')
        file.write(job.url + '\n')
        file.write(job.location + '\n')
        file.write(job.company + '\n')
        file.write(job.date + '\n')
        file.write('\n\n')
        text = word_tokenize(job.raw)
        self.write_formatted_text(file, text)

    @staticmethod
    def write_formatted_text(file, text, max_words_per_line=25):
        for i, word in enumerate(text):
            file.write(word + ' ')
            if i % max_words_per_line == 0:
                file.write('\n')

    @staticmethod
    def retrieve_text(file_path):
        text = ''
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
        except Exception as e:
            logging.error('Error while retrieving text file: ' + str(e))
        return text

    def clear_jobs(self):
        self.clear_directory(self.jobs_dir)

    def clear_directory(self, directory):
        files = self.get_items_from_path(directory, item_type=Path.ALL)
        for file in files:
            os.unlink(file)

    @staticmethod
    def clear_files(directory):
        if os.path.exists(directory):
            for the_file in os.listdir(directory):
                file_path = os.path.join(directory, the_file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

    @staticmethod
    def create_directory(directory):
        if not os.path.exists(directory):
                os.makedirs(directory)

    def get_files_from_path(self, path):
        return self.get_items_from_path(path, item_type=Path.FILE)

    def get_folders_from_path(self, path):
        return self.get_items_from_path(path, item_type=Path.FOLDER)

    def get_items_from_path(self, path, item_type=Path.ALL):
        items = []
        contents = self.get_contents_of_path(path)
        for path in contents:
            if self.check_file_type(path, path_type=item_type):
                items.append(path)
        return items

    @staticmethod
    def get_contents_of_path(path):
        contents = []
        try:
            for file in os.listdir(path):
                absolute_path = os.path.join(path, file)
                contents.append(absolute_path)
        except Exception as e:
            logging.error(e)
        return contents

    @staticmethod
    def check_file_type(path, path_type=Path.FILE):
        match = False
        if path_type == Path.FILE:
            match = os.path.isfile(path)
        elif path_type == Path.FOLDER:
            match = os.path.isdir(path)
        elif path_type == Path.ALL:
            match = True
        else:
            logging.error('Invalid path type: ' + str(path_type))
        return match

    @staticmethod
    def write_training_data(self, jobs):
        jobs_dir = self.jobs_dir
        for i, job in enumerate(jobs):
            if job.passed:
                pass
            else:
                pass
            file = open(jobs_dir, 'w', encoding='utf-8')
            file.write(job.title + '\n')

            for keyword in job.keywords:
                file.write(keyword + ", ")
            file.write('\n')
            file.write(job.url + '\n')
            file.write(job.location + '\n')
            file.write(job.company + '\n')
            file.write(job.date + '\n')
            file.write('\n\n')
            raw_txt = word_tokenize(job.raw)
            for j, word in enumerate(raw_txt):
                file.write(word + ' ')
                if (j % 25) == 0:
                    file.write('\n')
            file.close()

    @staticmethod
    def get_jobs(directory, f):
        keywords_list = []
        for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                file = open(file_path, 'r', encoding='utf-8')
                keywords_text = file.readlines()[1]
                keywords = word_tokenize(keywords_text)
                f.find_csharp(keywords)
                keywords = list(set(keywords))
                if len(keywords):
                    keywords.remove(',')
                keywords_list.append(keywords)
        return keywords_list

