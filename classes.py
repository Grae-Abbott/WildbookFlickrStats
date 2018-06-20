import flickrapi, time, json
from datetime import datetime, tzinfo

key = "6ab5883201c84be19c9ceb0a4f5ba959"
secret = "1d2bcde87f98ed92"
flickrObj = flickrapi.FlickrAPI(key,secret, format = "json")

class Album:
    def __init__(self, set_id, url = "", user_id = "", name = "", size = -1, species_count = {}, species_ratio = -1.0, species_ofInterest = "", photo_list = [], time_range_posted = -1.0, time_range_taken = -1.0):
        self.sid = set_id #set id
        self.url = url
        self.user_id = user_id
        self.name = name
        self.size = size
        self.species_ratio = species_ratio
        self.soi = species_ofInterest #species of interest
        self.photo_list = photo_list
        self.time_range_posted = time_range_posted
        self.time_range_taken = time_range_taken

    def print_album(self, file):
        file.write("Album/Set id: " + str(self.sid) + '\n')
        file.write("Url: " + str(self.url) + '\n')
        file.write("User id: " + str(self.user_id) + '\n')
        file.write("Name: " + str(self.name) + '\n')
        file.write("Number of images: " + str(self.size) + '\n')
        file.write("Ratio of images of zebras to total: " + str( round(self.species_ratio,5)  ) + '\n')
        file.write("Species of interest: " + str(self.soi) + '\n')
        file.write("Image ids: " + str(self.photo_list) + '\n')
        file.write("Time range of images in album being posted: " + str(    round(self.time_range_posted/60/60/24 ,5)   ) + " days" + '\n')
        file.write("Time range of images in album being taken: " + str( round(self.time_range_taken/60/60/24, 5)   ) + " days" + '\n')
        file.write("===" + '\n')

class Photo:
    def __init__(self, pos = -1, url = "", geotagged = False, photographer = "", tags = "", photo_description = "", locationX = -1, locationY = -1, timeTaken = -1, timePosted = -1, photoIfZoo = False, photoId = "", albumId = ""  ):
        self.id = photoId
        photo_info = json.loads(flickrObj.photos.getInfo(photo_id = self.id).decode(encoding='utf-8'))
        all_contexts = json.loads(flickrObj.photos.getAllContexts(photo_id = self.id).decode(encoding='utf-8'))
        self.locationX = locationX
        self.locationY = locationY
        self.location = (locationX, locationY)
        self.timeTaken = timeTaken if not(timeTaken == -1) else datetime.strptime(photo_info['photo']['dates']['taken'], '%Y-%m-%d %H:%M:%S').strftime("%s") #unix timestamp
        self.timePosted = timePosted if not(timePosted == -1) else photo_info['photo']['dates']['posted'] #unix timestamp
        self.timeDifference = timeTaken - timePosted
        self.photographer = photographer if not(photographer == "") else photo_info['photo']['owner']['nsid'] #nsid
        self.photoIfZoo = False
        self.albumId = albumId if not(albumId == "") else ("" if not('set' in all_contexts) else all_contexts['set'][0]['id'])
        self.pos = pos if not(pos == -1) else self.get_pos() #position in album (1 indexed)
        self.url = url
        self.photo_description = photo_description
        self.geotagged = geotagged
        self.tags = tags

        self.checkIfZoo()

    def checkIfZoo(self):
        #set coordinates
        xmin = -20.868596
        xmax = 54.187409
        ymax = 35.478236
        ymin = -35.587096
        if( self.locationY <=  ymax and self.locationY >=  ymin):
            if( self.locationX <=  xmax and self.locationX >=  xmin):
                self.photoIfZoo = True
        return

    #gets pos of image in album
    def get_pos(self):
        if self.albumId == "":
            return -1
            else:
                album = json.loads(flickrObj.photosets.getPhotos(photoset_id = self.albumId, user_id = self.id).decode(encoding='utf-8'))
                if not 'photoset' in album:
                    return -1
                else:
                    album = album['photoset']['photo']
                id_list = [] #list of all pids in album in order they appear on flickr
                for i in album:
                    id_list.append(i['id'])
                return id_list.index(self.id)+1

    def print_photo(self, file):
        file.write("Photo id: " + str(self.id) + '\n')
        file.write("Url: " + str(self.url) + '\n')
        file.write("Location: " + str(self.location) + '\n')
        file.write("Time difference: " + str( round(self.timeDifference/60/60/24 ,5) ) + " days" + '\n')
        file.write("Photographer: " + str(self.photographer) + '\n')
        file.write("Taken in zoo: " + str(self.photoIfZoo) + '\n')
        file.write("Album ID: " + str(self.albumId) + '\n')
        file.write("Positiion in the album: " + str(self.pos) + '\n')
        file.write("Photo description: " + str(`self.photo_description) + '\n')
        file.write("Geotagged: " + str(self.geotagged) + '\n')
        file.write("Tags: " + str(self.tags) + '\n')
        file.write("===" + '\n')



class Photographer:
    def __init__(self, user_id, name = "", userIfPro=False, geotagged= False, hometown="", timeTaken = -1, timePosted = -1, numposted=-1, numalbum=-1, firstyear=-1, numlocations=-1):
        self.user_id = user_id
        self.name = name
        user_info=people=json.loads(flickrObj.people.getInfo(user_id=self.user_id).decode(encoding='utf-8'))
        self.timeTaken = timeTaken if not(timeTaken == -1) else datetime.strptime(photo_info['photo']['dates']['taken'], '%Y-%m-%d %H:%M %S').strftime("%s") #unix timestamp
        self.timePosted = timePosted if not(timePosted == -1) else photo_info['photo']['dates']['posted'] #unix timestamp
        self.timeDelay = timeTaken - timePosted
        self.hometown=hometown
        self.geotagged = geotagged
        self.userIfPro=False
        self.numposted=numposted #count=people['person']['photos']['count']['_content']
        self.numalbum=numalbum
        self.firstyear=firstyear #first=people['person']['photos']['firstdate']['_content']
        self.numlocations=numlocations
        #frequency??

        self.checkIfPro(user_id)
    
    #i dont know if this is right or necessary?
    def checkIfPro(self, user_id):
        people=json.loads(flickrObj.people.getInfo(user_id=self.user_id).decode(encoding='utf-8'))['person']['ispro']
        if(people==1):
            return True
        else:
            return False

    def print_photographer(self, file):
        file.write("User id: " + str(self.user_id) + '\n')
        file.write("Name: " + str(self.name) + '\n')
        file.write("Avg Delay: " + str( round(self.timeDelay/60/60/24 ,5) ) + " days" + '\n')
        file.write("Hometown: " + str(self.hometown)+'\n')
        file.write("Avg Geotagged: " + str(self.geotagged) + '\n')
        file.write("Is Pro: " + str(self.userIfPro) + '\n')
        file.write("# Pics Posted: " + str(self.numposted) + '\n')
        file.write("# Albums Posted: " + str(self.numalbum) + '\n')
        file.write("Day First Active: " + str(datetime.strptime(self.firstyear, '%Y-%m-%d %H:%M:%S').strftime("%s")) + '\n')
        file.write("Number of Locations: " + str(self.numlocations) + '\n')
        file.write("===" + '\n')




    
