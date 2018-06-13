from flickrapi import FlickrAPI  # https://pypi.python.org/pypi/flickrapi
import urllib
import os
#import config
from random import randint
import time
import flickrDownload

def get_urls():
    urls = []
    f = open('all_urls','r')
    for line in f: #each id in the file is stored on a new line
        urls.append(line[:-1]) #stores the id without the newline character at the end
    f.close()
    return urls

urls = get_urls()

count = 1
for i in urls:
	flickrDownload.download_flickr_photo(i, count)
	count += 1