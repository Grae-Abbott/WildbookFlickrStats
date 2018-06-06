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
    def __init__(self, pos = -1,url = "", geotagged = False, photographer = "", tags = "", name = "", locationX = -1, locationY = -1, timeTaken = -1, timePosted = -1, zoo = False, id = "", albumID = ""  ):
        
        self.pos = pos #position in album
        self.locationX = locationX
        self.locationY = locationY
        self.location = (locationX, locationY)
        self.timeTaken = timeTaken
        self.timePosted = timePosted
        self.timeDifference = timeTaken - timePosted
        self.zoo = False
        self.id = photoId
        self.albumId = albumID
        self.url = url
        self.name = name
        self.geotagged = geotagged
        self.tags = tags
        self.photographer = photographer #nsid

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





    
