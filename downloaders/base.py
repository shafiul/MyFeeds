import logging


class BaseDownloader():

    logger = logging.getLogger(__name__)

    def __init__(self, store_location):
        self._store_location = store_location

    def download(self, file_location):
        pass

