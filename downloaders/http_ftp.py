import os
import os.path
import logging
import pycurl
import downloaders.base


logger = logging.getLogger(__name__)


class HttpFtpDownloader(downloaders.base.BaseDownloader):

    def __init__(self, store_location):
        downloaders.base.BaseDownloader.__init__(self, store_location)

    def download(self, url):

        filename = os.path.join(
            self._store_location,
            url.split("/")[-1].strip()
        )

        c = pycurl.Curl()
        c.setopt(pycurl.URL, url)

        if url.startswith('https'):
            c.setopt(pycurl.SSL_VERIFYPEER, 0)
            c.setopt(pycurl.SSL_VERIFYHOST, 0)

        c.setopt(pycurl.FOLLOWLOCATION, 1)
        c.setopt(pycurl.MAXREDIRS, 5)

        # Setup writing
        if os.path.exists(filename):
            f = open(filename, "ab")
            c.setopt(pycurl.RESUME_FROM, os.path.getsize(filename))
        else:
            f = open(filename, "wb")

        c.setopt(pycurl.WRITEDATA, f)

        #c.setopt(pycurl.VERBOSE, 1)
        c.setopt(pycurl.NOPROGRESS, 0)
        try:
            logger.info('Starting downloading {0} to {1}'.format(
                url, filename
            ))
            c.perform()
        except:
            pass

        return filename