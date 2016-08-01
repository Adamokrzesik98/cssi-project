import render
from home import Home
from person import Person
from sticky import Sticky
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
			for id in home[0].occupants:
				people_in_home.append(Person.query().filter(id == Person.user_id).fetch()[0])

			for p in people_in_home:
				if p.location:
					checked_in.append(person)
				else:
					checked_out.append(person)
				if p.do_not_disturb:
					dnd_state = True
			for sticky_note in Sticky.query().filter(Sticky.home_key == person.home_key).fetch():
				home_stickies.append(sticky_note)
			

				

			# for person in people_in_home:
			# 	logging.info(person.name)

			return_data = {'checked_in' : checked_in, 'checked_out' : checked_out, 'dnd' : dnd_state, 'home_stickies' : home_stickies}
			return return_data