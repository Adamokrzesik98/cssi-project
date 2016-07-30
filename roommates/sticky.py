from google.appengine.ext import ndb

class Sticky(ndb.Model):
    title = ndb.StringProperty(required = True)
    content = ndb.StringProperty(required = True)  
    author = ndb.StringProperty(required = True)  #defined by user_id
    time_created = ndb.DateTimeProperty(required=True, auto_now=True)
#   duration = 