import downloaders.http_ftp

options = {
    'download_dir': 'downloads',
    'max_workers': 2
}

# Registry of downloaders

downloader = {
    'http': downloaders.http_ftp.HttpFtpDownloader,
    'ftp': downloaders.http_ftp.HttpFtpDownloader
}
