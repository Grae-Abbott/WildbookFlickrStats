import flickrapi, time
from datetime import datetime, tzinfo

key = "6ab5883201c84be19c9ceb0a4f5ba959"
secret = "1d2bcde87f98ed92"
flickrObj = flickrapi.FlickrAPI(key,secret, format = "json")

class Album:
    def __init__(self, set_id, url = "", user_id = "", name = "", size = -1, species_count = {}, species_ratio = -1.0, species_ofInterest = "", photo_list = [], time_range_posted = -1.0, time_range_taken = -1.0):
        self.sid = set_id #photo id
        self.url = url
        self.user_id = user_id
        self.name = name
        self.size = size
        self.species_ratio = species_ratio
        self.soi = species_ofInterest #species of interest
        self.photo_list = photo_list
        self.time_range_posted = time_range_posted
        self.time_range_taken = time_range_taken

class Photo:
    def __init__(self, pos = -1,url = "", geotagged = False, photographer = "", tags = "", name = "", locationX = -1, locationY = -1, timeTaken = -1, timePosted = -1, zoo = False, id = "", albumId = ""  ):
        self.id = photoId
        photo_info = json.loads(flickrObj.photos.getInfo(photo_id = self.id).decode(encoding='utf-8'))
        all_contents = json.loads(flickrObj.photos.getAllContexts(photo_id = self.id).decode(encoding='utf-8'))
        self.locationX = locationX
        self.locationY = locationY
        self.location = (locationX, locationY)
        self.timeTaken = timeTaken if not(timeTaken == -1) else datetime.strptime(photo_info['photo']['dates']['taken'], '%Y-%m-%d %H:%M:%S').strftime("%s") #unix timestamp
        self.timePosted = timePosted if not(timePosted == -1) else photo_info['photo']['dates']['posted'] #unix timestamp
        self.timeDifference = timeTaken - timePosted
        self.photographer = photographer if not(photographer == "") else photo_info['photo']['owner']['nsid'] #nsid
        self.zoo = False
        self.albumId = albumId if not(albumId == "") else ("" if not('set' in all_contexts) else all_contexts['set']['id'])
        self.pos = pos if not(pos == -1) else get_pos() #position in album (1 indexed)
        self.url = url
        self.name = name
        self.geotagged = geotagged
        self.tags = tags

        checkIfZoo()


    def checkIfZoo():
        #set coordinates
        xmax = 0
        xmin = 0
        ymax = 0
        ymin = 0
        if( photoLocationY <=  ymax and photoLocationY >=  ymin):
            if( photoLocationX <=  xmax and photoLocationX >=  xmin):
                return True

    #gets pos of image in album
    def get_pos():
        if self.albumId == "":
            return -1
        else:
            album = json.loads(flickrObj.photosets.getPhotos(photoset_id = self.albumId, user_id = self.id).decode(encoding='utf-8'))['photoset']['photo']
            return album.index(self.id)+1





    
