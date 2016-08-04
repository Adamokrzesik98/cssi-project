from google.appengine.ext import ndb

class Home(ndb.Model):
	name = ndb.StringProperty(required = True)
	password = ndb.StringProperty(required = True)
	occupants = ndb.StringProperty(repeated = True)  #defined by user_id
	calendar_id = ndb.StringProperty()
#    stickies = #list of stickies with timestamps



