from google.appengine.ext import ndb

class Chores(ndb.Model):
	nameOfChore = ndb.StringProperty(required = True)
	assignedTo = ndb.StringProperty(required = True)
	lengthOfTime = ndb.FloatProperty(required=True) 