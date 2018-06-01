import string, sys, flickrapi, json, time
from datetime import datetime
from getFlickrList import searchInFlickr,searchInFlickrUid

key = "6ab5883201c84be19c9ceb0a4f5ba959"
secret = "1d2bcde87f98ed92"

ids = []
for i in range(2010,2019):
	filename = "zebra_ids_" + str(i)
	f = open(filename,'r')
	for line in f: #each id in the file is stored on a new line
		ids.append(line[:-1]) #stores the id without the newline character at the end
	f.close()
total = len(ids)
print(total)
#calculates the avg time between the picture being taken and posted
total_dif = 0.0
flickrObj = flickrapi.FlickrAPI(key,secret, format = "json")
i = 0
for pid in ids:
	photo_info = json.loads(flickrObj.photos.getInfo(photo_id = str(pid)).decode(encoding='utf-8'))
	posted = photo_info['photo']['dates']['posted']
	taken = datetime.strptime(photo_info['photo']['dates']['taken'], '%Y-%m-%d %H:%M:%S').strftime("%s")
	difference = int(posted) - int(taken)
	difference = float(difference)/(60*60*24)
	total_dif += difference
	print(i)
	i += 1
avg_dif = total_dif/len(ids)
print(avg_dif)
#creates a list of all the unique user ids(nsids)
file = open('nsid_dictionary', 'r')
nsids = []
count = 0
for line in file:
	count += 1
	if count%2 == 1:
		nsids.append(line[:-1])
file.close

#calculates amount of "pro" users 

pro_count = 0
for uid in nsids:
	ppl_info = json.loads(flickrObj.people.getInfo(user_id = str(uid)).decode(encoding='utf-8'))
	pro_count += ppl_info['person']['ispro']
pro_avg = float(pro_count)/len(nsids)
print(pro_avg)
print(pro_count)

flickrObj = flickrapi.FlickrAPI(key,secret, format = "json")
final_total = 0
for nsid in nsids:
	urls,ids,total = searchInFlickrUid(flickrObj, nsid = nsid, tags = ["grevy's zebra"], text = "grevy's zebra")
	final_total += int(total)
	print(final_total)
print(final_total)