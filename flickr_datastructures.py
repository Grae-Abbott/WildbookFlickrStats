import requests, json, sys, string, time, flickrapi, pytz, webbrowser
from getFlickrList import searchInFlickr
from datetime import datetime, tzinfo

key = "6ab5883201c84be19c9ceb0a4f5ba959"
secret = "1d2bcde87f98ed92"

#pid refers to photo id, nsid is the user id
#stores all ids from the files in one list
def get_ids():
	ids = []
	for i in range(2010,2019):
		filename = "zebra_ids_" + str(i)
		f = open(filename,'r')
		for line in f: #each id in the file is stored on a new line
			ids.append(line[:-1]) #stores the id without the newline character at the end
		f.close()
	return ids

#creates user_dict which maps users to a list of their photos that contain grevy's zebras, also writes dict to file to avoid multiple flickr api queries
def create_userdict(ids):
	user_dict = {}
	flickrObj = flickrapi.FlickrAPI(key,secret, format = "json")
	for pid in ids:
		photo_info = json.loads(flickrObj.photos.getInfo(photo_id = str(pid)).decode(encoding='utf-8'))
		nsid = photo_info['photo']['owner']['nsid']
		if nsid in user_dict:
			user_dict[nsid].append(pid)
		else:
			user_dict[nsid] = [pid]
	#writes the user_dict to a file to avoid quering the flickr api more than once
	file = open('nsid_dictionary', 'w')
	for i in user_dict.keys():
		file.write(i + "\n")
		file.write(str(user_dict[i]))
		file.write("\n")
	file.close

	return user_dict

#returns a list of nsids(user_ids) given that the user_dict file has been created, and their is no local user_dict
def get_nsids():
	file = open('nsid_dictionary', 'r')
	nsids = []
	count = 0
	for line in file:
		count += 1
		#every other line in the file has an nsid
		if count%2 == 1:
			nsids.append(line[:-1])
	file.close
	return nsids

#creates a dictionary mapping users to their photos of grevy's if the user dict file has already been created
def get_userdict():
	file = open('nsid_dictionary', 'r')
	user_dict = {}
	count = 0
	nsid = ''
	for line in file:
		count += 1
		if count%2 == 1:
			nsid = line[:-1]
		else:
			line = line[2:-2]
			user_dict[nsid] = line.split(sep = "', '")
	file.close
	return user_dict


