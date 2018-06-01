import requests, json, sys, string, time, flickrapi, pytz, webbrowser
from getFlickrList import searchInFlickr
from datetime import datetime, tzinfo
from classes import Album, Photo

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

#creates a list of albums that
def get_albums():
    flickrObj = flickrapi.FlickrAPI(key,secret, format = "json")
    photolist = get_ids()
    albumlist = {}
    for pid in photolist:
        all_contexts = json.loads(flickrObj.photos.getAllContexts(photo_id = pid).decode(encoding='utf-8'))
        sets = all_contexts["set"]
        for i in sets:
            set_id = i["id"]           
            if not(set_id in albumlist):
                user = json.loads(flickrObj.photos.getInfo(photo_id = pid).decode(encoding='utf-8'))['photo']['owner']['nsid']
                photosets = json.loads(flickrObj.photosets.getPhotos(photoset_id = set_id, user_id = user).decode(encoding='utf-8'))
                newalbum = Album(set_id)
                first_posted = json.loads(flickrObj.photos.getInfo(photo_id = photosets['photoset']['photo'][0]['id']).decode(encoding='utf-8'))['photo']['dates']['posted']
                first_taken = json.loads(flickrObj.photos.getInfo(photo_id = photosets['photoset']['photo'][0]['id']).decode(encoding='utf-8'))['photo']['dates']['taken']
                mint = int(datetime.strptime(first_taken,'%Y-%m-%d %H:%M:%S').strftime("%s"))
                maxt = int(datetime.strptime(first_taken,'%Y-%m-%d %H:%M:%S').strftime("%s"))
                minp = int(first_posted)
                maxp = int(first_posted)
                for j in photosets['photoset']['photo']:
                	taken = json.loads(flickrObj.photos.getInfo(photo_id = j['id']).decode(encoding='utf-8'))['photo']['dates']['taken']
                	taken = int(datetime.strptime(taken, '%Y-%m-%d %H:%M:%S').strftime("%s"))
                	posted = int(json.loads(flickrObj.photos.getInfo(photo_id = j['id']).decode(encoding='utf-8'))['photo']['dates']['posted'])
                	if taken < mint:
                		mint = taken
                	if taken > maxt:
                		maxt = taken
                	if posted < minp:
                		minp = posted
                	if posted > maxp:
                		maxp = posted
                	newalbum.photo_list.append(j['id'])
                newalbum.time_range_posted = int(maxp) - int(minp)
                newalbum.time_range_taken = int(maxt) - int(mint)
                albumlist[newalbum.sid] = newalbum
    return albumlist



