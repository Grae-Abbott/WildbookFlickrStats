class Album:
    def __init__(self, set_id, size = -1, species_count = {}, species_ratio = -1, species_ofInterest = "", photo_list = [], time_range = -1.0):
        self.sid = set_id #photo id
        self.size = size
        self.species_ratio = species_ratio
        self.soi = species_ofInterest #species of interest
        self.photo_list = photo_list
        self.time_range = time_range

class Photo:
    def __init__(self, photoPos = -1, photoLocationX = -1, photoLocationY = -1, photoTimeTaken = -1, photoTimePosted = -1, photoIfZoo = False, photoId = "defaultpid", AlbumID = "defaultaid"  ):
        
        self.photoPos = photoPos
        self.photoLocationX = photoLocationX
        self.photoLocationY = photoLocationY
        self.photoLocation = (photoLocationX, photoLocationY)
        self.photoTimeTaken = photoTimeTaken
        self.photoTimePosted = photoTimePosted
        self.photoTimeDifference = photoTimeTaken - photoTimePosted
        self.photoIfZoo = False
        self.photoId = photoId
        self.AlbumID = AlbumID

        checkIfZoo()


    def checkIfZoo():
        #set coordinates
        xmax = 0
        xmin = 0
        ymax = 0
        ymin = 0
        if( photoLocationY <=  ymax && photoLocationY >=  ymin):
            if( photoLocationX <=  xmax && photoLocationX >=  xmin):
                return True





    
