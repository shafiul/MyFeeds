import os
import pycurl
import sys


def progress(total, existing, upload_t, upload_d):
    existing = existing + os.path.getsize(filename)
    try:
        frac = float(existing)/float(total)
    except:
        frac = 0
    sys.stdout.write("\r%s %3i%%" % ("File downloaded - ", frac*100))

url = 'ftp://ftp.mozilla.org/pub/mozilla.org/b2g/nightly/2014-01-07-00-40-01-mozilla-aurora/mozilla-aurora-linux32_gecko-nightly-bm63-build1-build6.txt.gz'
filename = url.split("/")[-1].strip()


def test(debug_type, debug_msg):
    print("debug(%d): %s" % (debug_type, debug_msg))

c = pycurl.Curl()
c.setopt(pycurl.URL, url)
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
c.setopt(pycurl.DEBUGFUNCTION, test)
c.setopt(pycurl.NOPROGRESS, 0)
c.setopt(pycurl.PROGRESSFUNCTION, progress)
try:
    c.perform()
except:
    pass
