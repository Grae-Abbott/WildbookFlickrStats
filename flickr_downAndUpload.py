from flickrapi import FlickrAPI  # https://pypi.python.org/pypi/flickrapi
import urllib
import os
#import config
from random import randint
import time
import flickr_datastructures as dts 
import flickrDownload

urls = dts.get_urls()

count = 1
for i in urls:
	flickrDownload.download_flickr_photo(i, count)
	count += 1