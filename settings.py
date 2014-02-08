import downloaders.http_ftp

options = {
    'feed_url': 'https://dl.dropboxusercontent.com/u/6160850/downloads.rss',
    'download_dir': 'downloads'
}

# Registry of downloaders

downloader = {
    'http': downloaders.http_ftp.HttpFtpDownloader,
    'ftp': downloaders.http_ftp.HttpFtpDownloader
}
