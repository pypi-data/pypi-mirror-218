import inspect
import re
import shutil
import sys
from datetime import datetime
import logging
import os
import traceback
import zipfile
from os.path import join, abspath, isdir, exists, basename, splitext
from pathlib import Path

from google.oauth2.service_account import Credentials

"""
To install libraries:
    pip install -r requirements.txt
"""
import google.cloud.logging
from google.cloud import error_reporting
from google.cloud.logging import Resource
from google.cloud.logging_v2.handlers import CloudLoggingHandler, setup_logging

"""
Check README.md for more information
"""

class Log:
    _LOGS_FOLER = "logs"

    _LOG_FILE_DATE_FORMAT = '%Y-%m-%d'
    _LOGS_DATETIME_FORMAT = '%d-%m-%Y %H:%M:%S.%f'

    _PROJECT_NAME = os.path.basename(sys.path[1])

    class Level:
        INFO = "I"
        ERROR = "E"
        DEBUG = "D"
        WARNING = "W"

        @staticmethod
        def logger(level):
            if level == Log.Level.INFO:
                return logging.INFO
            if level == Log.Level.ERROR:
                return logging.ERROR
            if level == Log.Level.DEBUG:
                return logging.DEBUG
            if level == Log.Level.WARNING:
                return logging.WARNING
            return logging.NOTSET

    def __init__(self, log_name=None):
        self.log_name = log_name

        self._generate_log_name()
        self._create_dirs()
        self._archive()

        self.handler = logging.FileHandler(filename=os.path.join(self.log_dir, "any.log"), encoding='utf-8', mode='a+')
        logging.basicConfig(
            handlers=[
                self.handler
            ],
            format="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%F %T",
            level=logging.NOTSET
        )
        self.logger = logging.getLogger(self.log_name)

        self.cloud_project_id = None

    def verbose(self, text, level):
        if level == self.Level.ERROR:
            text = f"{text}\n{traceback.format_exc()}"
        self.logger.log(self.Level.logger(level), text)
        if text:
            print(text)
        self._save_file(text, level)

    def info(self, text):
        self.verbose(text, self.Level.INFO)

    def warning(self, text):
        self.verbose(text, self.Level.WARNING)

    def debug(self, text):
        self.verbose(text, self.Level.DEBUG)

    def error(self, error):
        self.verbose(error, self.Level.ERROR)

    def setup_cloud_logging(self, project_id, credentials=None):
        self.cloud_project_id = project_id

        _resource = Resource(
            type="cloud_function",
            labels={
                "project_id": self.cloud_project_id,
                "function_name": self._PROJECT_NAME
            },
        )
        if credentials:
            client = google.cloud.logging.Client(
                project=self.cloud_project_id,
                credentials=Credentials.from_service_account_info(credentials)
            )
        else:
            client = google.cloud.logging.Client(project=self.cloud_project_id)
        setup_logging(self.handler)
        setup_logging(CloudLoggingHandler(client, resource=_resource))

    def _generate_log_name(self):
        try:
            if not self.log_name:
                frame = inspect.stack()[1]
                module = inspect.getmodule(frame[0])
                self.log_name = module.__file__
                if not self.log_name:
                    self.log_name = sys.argv[0]
                self.log_name = splitext(basename(self.log_name))[0]
        except Exception as e:
            print(f"Error while generating log name: {e}")

    def _create_dirs(self):
        self.date = datetime.now().strftime(self._LOG_FILE_DATE_FORMAT)

        self.logs_dir = self._LOGS_FOLER
        self.log_dir = abspath(join(self.logs_dir, self.date))
        try:
            os.umask(0)
            os.makedirs(self.log_dir, exist_ok=True)
        except OSError as e:
            print(f"Error while creating {self.log_dir}: {e}")

        self.log_file = join(self.log_dir, f"{self.log_name}.log")

        print(f"{self.log_name} logs can be found in {self.log_dir}")

    def _save_file(self, log, level):
        with open(self.log_file, "a+") as f:
            at = self._log_date()
            f.write(f"{at[:-3]} {level}: {log}\n")

    def _log_date(self):
        return datetime.now().strftime(self._LOG_FILE_DATE_FORMAT)

    def _archive(self):
        today = self._log_date()
        current_year = today[:4]
        log_directories = [
            join(self._LOGS_FOLER, directory)
            for directory in os.listdir(self._LOGS_FOLER)
            if isdir(os.path.join(self._LOGS_FOLER, directory))
            and directory != today
        ]

        zip_path = join(self._LOGS_FOLER, current_year + ".zip")
        zip_mode = "a" if exists(zip_path) else "w"
        with zipfile.ZipFile(zip_path, zip_mode, zipfile.ZIP_DEFLATED) as zip_file:
            for log_directory in log_directories:
                for file in os.listdir(log_directory):
                    if file.endswith(".log"):
                        file_path = join(log_directory, file)
                        zip_file.write(file_path, arcname=join(os.path.basename(log_directory), file))
                shutil.rmtree(log_directory)
