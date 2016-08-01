import render
from home import Home
from person import Person
from sticky import Sticky
import time
import logging

#For email send
from google.appengine.api import mail


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
					

			room_name = home[0].name

			# for person in people_in_home:
			# 	logging.info(person.name)

<<<<<<< Updated upstream
			return_data = {'room_name': room_name, 'checked_in' : checked_in, 'checked_out' : checked_out, 'dnd' : dnd_state, 'has_dnd_on' : has_dnd_on ,'home_stickies' : home_stickies}
			return return_data
=======
			return_data = {'checked_in' : checked_in, 'checked_out' : checked_out, 'dnd' : dnd_state, 'has_dnd_on' : has_dnd_on ,'home_stickies' : home_stickies}
			return return_data

def dndEnabled(self, enabler):
	home = Home.query().filter(Home.key == person.home_key).fetch()
	for id in home[0].occupants:
		people_in_home.append(Person.query().filter(id == Person.user_id).fetch()[0])
	for person in people_in_home:
		if not person.user_id == enabler.user_id:
			email_content = "Dear " + person.name +",\n" + enabler.name + " has turned on do not disturb for your room. Enter with caution. Or better yet, not at all. ;)\nSincerely,\nThe Roomates Developer Team"
			# Import smtplib for the actual sending function
			sendEmail(person.user_id, 'roomatescalendars@gmail.com', 'Do Not Disturb Enabled', email_content)


def sendEmail(self, to, email_sender, email_subject, message_content):
	message = mail.EmailMessage(sender=email_sender,
                            subject=email_subject)
	message.to = to
	message.body = message_content
	message.send()















>>>>>>> Stashed changes
