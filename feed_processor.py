import feedparser


def get_feed_links(path_of_feed):
    """
        Parses the feed from path_of_feed parameter and returns list of
        feeds to be fetched.
    """

    feed = feedparser.parse(path_of_feed)

    return [item['link'] for item in feed['items']]