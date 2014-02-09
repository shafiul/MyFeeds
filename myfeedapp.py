import logging
import logging.config
import os
import os.path
import argparse
import settings
import feed_processor
import downloaders.base

logger = logging.getLogger(__name__)


class MyFeedApp():

    def __init__(self):
        self._download_location = None

    def _handle_path(self):
        if self._download_location is None:
            logger.info('Using default download location.')
            self._download_location = settings.options['download_dir']

        logger.debug('Download location is: {0}'.format(self._download_location))

        if not os.path.isabs(self._download_location):
            self._download_location = os.path.join(
                os.path.abspath(
                    os.path.dirname(os.path.realpath(__file__))
                ),
                self._download_location
            )
            logger.debug('Calculated new abspath: {0}'.format(self._download_location))

        if not os.path.exists(self._download_location):
            logger.warn('Path {0} does not exist! Trying to create', format(self._download_location))
            os.makedirs(self._download_location)
        else:
            if not os.path.isdir(self._download_location):
                logger.fatal('Path {0} is not a directory.'.format(self._download_location))
                raise Exception('Path not a directory.')

    def _download_single_file(self, filename):
        """
            Downloads a single file
        """

        #TODO check if filename is valid

        downloader = _get_downloader('http')

        if not issubclass(downloader, downloaders.base.BaseDownloader):
            raise Exception('Invalid downloader provided in the options file. '
                            'Downloader should be a subclass of BaseDownloader')

        return downloader(
            self._download_location
        ).download(filename)

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
            self._download_location = args.output

        try:
            self._handle_path()
        except Exception as e:
            print('Halting. Invalid path provided, check log for details. ({0})'.format(e))
            return

        try:
            logger.info('Using feed URL: {}'.format(args.feed))
            feed_path = self._download_single_file(args.feed)
        except Exception as e:
            logger.fatal('Exception while downloading feed: {0}'.format(e))
            print('Halting, failed to download feed. Check log.')
            return

        feed_links = feed_processor.get_feed_links(feed_path)

        logger.info('Feed downloaded. Links will be fetched: {0}'.format(feed_links))

        for single_feed in feed_links:
            try:
                self._download_single_file(str(single_feed))
            except Exception as e:
                logger.error('Error while downloading feed: {0}'.format(
                    e
                ))

        logger.info('Done! Happy day.')


def _get_downloader(protocol=None):
    """
        Returns a downloader based on given protocol parameter
    """

    if protocol is None:
        raise Exception('Protocol can not be none. Future version will support auto detection.')

    if protocol not in settings.downloader:
        raise Exception('Protocol {0} not implemented.'.format(protocol))

    return settings.downloader[protocol]


if __name__ == '__main__':

    logging.config.fileConfig('logging.ini', disable_existing_loggers=False)

    app_ob = MyFeedApp()
    app_ob.start()

