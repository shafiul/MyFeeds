# Introduction
MyFeeds is a simple downloader. Multiple files can be downloaded concurrently, with resume support.

File URLs should be provided as RSS feed.

Supports HTTP/FTP for now, can be extended easily.

Cross-platform (Only tested on Linux for the time being)

# Requirements:
* pycurl (Which means your system should have cURL)
* feedparser

# Usage:
run downloader.py with -h or --help for usage details.

# Configuration
Please see settings.py for some configurable options.

# Known Issues
As pycurl module is not supported in python 3.x, this application will not be usable in Python 3.
Future versions of this application will address this issue hopefully.