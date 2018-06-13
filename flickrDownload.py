# Copyright 2014-2017 Bert Carremans
# Author: Bert Carremans <bertcarremans.be>
# Edited by: Affan Farid
#
# License: BSD 3 clause


from flickrapi import FlickrAPI  # https://pypi.python.org/pypi/flickrapi
import urllib
import os, sys,time
#import config
from random import randint
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

#google drive auth process

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)


API_KEY = "6ab5883201c84be19c9ceb0a4f5ba959"  #// replace with your key
API_SECRET = "1d2bcde87f98ed92"  #// replace with your secret
IMG_FOLDER = "/mnt/c/Users/ghabb/Desktop/GitHub/WildbookFlickrStats/" 

folder_id = '1eJeXfRx8VxDRLT8ttdEgjC4eWUa258M1' #folder id for "Shared with me/social media bias/data/Grevy's"
resultsID = '1Wdxca3CdSw9TvSIvPJhr-wLM2FxdmgKt' #folder id for ^^/"Grevy's Search Results"

def download_flickr_photo(url, keyword, count):
    results_folder = IMG_FOLDER #+ keyword.replace(" ", "_") + "/"
    if not os.path.exists(results_folder):
        os.makedirs(results_folder)

    filename = str(count) + ".jpg"
    
    try:
        #downloads image
        urllib.urlretrieve(url,  results_folder + filename)
        print 'Downloading image #' + str(count) + ' from url ' + url

        #UPLOAD LINES HERE

        file = drive.CreateFile({'title' : filename, 'parents' : [{'kind' : 'drive#fileLink', 'id' : resultsID}]})
        file.SetContentFile(filename)
        file.Upload()

        
        #deletion line
        os.remove( IMG_FOLDER + filename)

    except Exception as e:
        print str(e) + ' Download failure'




'''
def download_flickr_photos(keywords, size='original', max_nb_img=-1):
    if not (isinstance(keywords, str) or isinstance(keywords, list)):
        raise AttributeError('keywords must be a string or a list of strings')
    
    if not (size in ['thumbnail', 'square', 'medium', 'original']):
        raise AttributeError('size must be "thumbnail", "square", "medium" or "original"')
    
    if not (max_nb_img == -1 or (max_nb_img > 0 and isinstance(max_nb_img, int))):
        raise AttributeError('max_nb_img must be an integer greater than zero or equal to -1')
    
    flickr = FlickrAPI(API_KEY, API_SECRET)
    
    if isinstance(keywords, str):
        keywords_list = []
        keywords_list.append(keywords)
    else:
        keywords_list = keywords
    
    if size == 'thumbnail':
        size_url = 'url_t'
    elif size == 'square':
        size_url = 'url_q'
    elif size == 'medium':
        size_url = 'url_c'
    elif size == 'original':
        size_url = 'url_o'

    for keyword in keywords_list:
        count = 0
            
            #print('Downloading images for', keyword)
            
        results_folder = IMG_FOLDER + keyword.replace(" ", "_") + "/"
        if not os.path.exists(results_folder):
            os.makedirs(results_folder)

        photos = flickr.walk(text=keyword,extras=size_url,license='1,2,4,5',per_page=50)

        urls = []
        for photo in photos:
            t = randint(1, 3)
            time.sleep(t)
            count += 1

            if max_nb_img != -1:
                if count > max_nb_img:
                    print('Reached maximum number of images to download')
                    break

            try:
                url=photo.get(size_url)
                urls.append(url)

                urllib.request.urlretrieve(url,  results_folder + str(count) +".jpg")
                print('Downloading image #' + str(count) + ' from url ' + url)
            except Exception as e:
                print(e, 'Download failure')
        print ("Total images downloaded:", str(count - 1))
'''
#testing function


#download_flickr_photos(keywords="grevy's zebra",max_nb_img = 5)

url1 = "https://farm1.staticflickr.com/893/40731835074_ccfbbefb59_o.jpg"
download_flickr_photo(url1, "test", 100)

