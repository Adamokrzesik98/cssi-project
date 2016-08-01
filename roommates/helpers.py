import render
from home import Home
from person import Person
from sticky import Sticky
import time
import logging


# redirect current page to address
def redirect(self, address, wait_time):
	data = {'url': address}
	self.response.write('<script> setTimeout(function() {window.location = "' + address + '"},' + str(wait_time) + ');</script>')


#Takes input as a person
#Returns a dictionary of DND status, current stickies, and people checked in
def getDashData(self, person):
		if person:
			home = Home.query().filter(Home.key == person.home_key).fetch()
			dnd_state = False
			home_stickies = []
			checked_in = []
			checked_out = []
			people_in_home = []
			has_dnd_on = []
			for id in home[0].occupants:
				people_in_home.append(Person.query().filter(id == Person.user_id).fetch()[0])

			for p in people_in_home:
				if p.location:
					checked_in.append(person)
				else:
					checked_out.append(person)
				if p.do_not_disturb:
					dnd_state = True
					has_dnd_on.append(p)
			# Check for and delete expired sticky notes
			for sticky_note in Sticky.query().filter(Sticky.home_key == person.home_key).fetch():
				if sticky_note.expiration < time.time():
					sticky_note.key.delete()
				else:
					home_stickies.append(sticky_note)
					
			# for person in people_in_home:
			# 	logging.info(person.name)

			return_data = {'checked_in' : checked_in, 'checked_out' : checked_out, 'dnd' : dnd_state, 'has_dnd_on' : has_dnd_on ,'home_stickies' : home_stickies}
			return return_data