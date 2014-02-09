import logging
import logging.config
import os
import os.path
import argparse
import Queue
import settings
import feed_processor
import myworkers
import downloaders.base

logger = logging.getLogger(__name__)


def get_downloader(protocol):
    """
        Returns a downloader based on given protocol parameter
    """

    if protocol not in settings.downloader:
        raise Exception('Protocol {0} not implemented.'.format(protocol))

    return settings.downloader[protocol]


def download_single_file(app, file_url):
    """
        Downloads a single file
        @type app MyFeedApp
        @type file_url str
    """

    #TODO check if filename is valid

    protocol = None

    if file_url.startswith('http'): # Not distinguishing between HTTP & HTTPs at all
        protocol = 'http'
    elif file_url.startswith('ftp'):
        protocol= 'ftp'
    else:
        raise Exception('Protocol could not be determined from URL: {}'.format(
            file_url
        ))

    downloader = get_downloader('http')

    if not issubclass(downloader, downloaders.base.BaseDownloader):
        raise Exception('Invalid downloader provided in the options file. '
                        'Downloader should be a subclass of BaseDownloader')

    return downloader(
        app.download_location
    ).download(file_url)


class MyFeedApp():

    def __init__(self):
        self._download_location = None

    @property
    def download_location(self):
        return self._download_location

    @download_location.setter
    def download_location(self, download_location):
        self._download_location = download_location

    def _handle_path(self):
        if self.download_location is None:
            logger.info('Using default download location.')
            self.download_location = settings.options['download_dir']

        logger.debug('Download location is: {0}'.format(self.download_location))

        if not os.path.isabs(self.download_location):
            self.download_location = os.path.join(
                os.path.abspath(
                    os.path.dirname(os.path.realpath(__file__))
                ),
                self.download_location
            )
            logger.debug('Calculated new abspath: {0}'.format(self.download_location))

        if not os.path.exists(self.download_location):
            logger.warn('Path {0} does not exist! Trying to create'.format(self.download_location))
            os.makedirs(self.download_location)
        else:
            if not os.path.isdir(self.download_location):
                logger.fatal('Path {0} is not a directory.'.format(self.download_location))
                raise Exception('Path not a directory.')

    def start(self):
        """
            Start Application
        """
        logger.info('Starting application...')

        parser = argparse.ArgumentParser()
        parser.add_argument('feed', help='URL of the feed from which each item will be downloaded.')
        parser.add_argument('-o', '--output', help='Output directory where downloads will be saved.')

        args = parser.parse_args()

        if args.output:
            self.download_location = args.output

        try:
            self._handle_path()
        except Exception as e:
            print('Halting. Invalid path provided, check log for details. ({0})'.format(e))
            return

        # Download feed URL

        try:
            logger.info('Using feed URL: {}'.format(args.feed))
            feed_path = download_single_file(self, args.feed)
        except Exception as e:
            logger.fatal('Exception while downloading feed: {0}'.format(e))
            print('Halting, failed to download feed. Check log.')
            return

        feed_links = feed_processor.get_feed_links(feed_path)

        logger.info('Feed downloaded. Links will be fetched: {0}'.format(feed_links))

        # for single_feed in feed_links:
        #     try:
        #         self._download_single_file(str(single_feed))
        #     except Exception as e:
        #         logger.error('Error while downloading feed: {0}'.format(
        #             e
        #         ))

        in_queue = Queue.Queue()
        for single_feed in feed_links:
            in_queue.put((self, str(single_feed)))

        workers = [myworkers.Worker(download_single_file, in_queue)
                   for i in range(settings.options['max_workers'])]

        for worker in workers:
            worker.start()

        in_queue.join()

        logger.info('Download completed. Exiting')


if __name__ == '__main__':

    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

    app_ob = MyFeedApp()
    app_ob.start()

