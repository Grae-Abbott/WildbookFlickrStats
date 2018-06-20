import requests, json, sys, string, time, flickrapi, pytz, webbrowser
from getFlickrList import searchInFlickr
from datetime import datetime, tzinfo
import flickr_datastructures as dts
import classes

albums = dts.get_albums()
print(albums)
f = open('albums', 'w')
x = albums['72157625579178878']
x.print_album(f)
#ids = dts.get_ids()
#print(len(ids))
'''
for i in albums:
	i.print_album(f)
print("Total results: " + str(len(albums)) + " albums")'''
''