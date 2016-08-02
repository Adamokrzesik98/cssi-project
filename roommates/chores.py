from google.appengine.ext import ndb

class Chore(ndb.Model):
	chore_name = ndb.StringProperty(required = True)
	workers = ndb.StringProperty(repeated = True)
	end_time = ndb.FloatProperty(required=True)
	duration = ndb.FloatProperty(required=True) 