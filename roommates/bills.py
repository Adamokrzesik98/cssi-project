from google.appengine.ext import ndb

class Bills(ndb.Model):
	bill_name = ndb.StringProperty(required = True)
	payer_id = ndb.StringProperty(required = True)
	payer_name = ndb.StringProperty(required = True)
