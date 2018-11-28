import datetime

class RedFlagModel():

  def __init__(self, createdOn, createdBy, incidenttype, location, status, images, videos, comment):
    self.createdOn = datetime.datetime.utcnow()
    self.createdBy = createdBy
    self.incidenttype = incidenttype
    self.location = location
    self.status = status
    self.images = images
    self.videos = videos
    self.comment = comment