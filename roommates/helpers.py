import render
import login
from home import Home
from person import Person
from sticky import Sticky
from chores import Chore
from bills import Bills
from google.appengine.api import users
from google.appengine.api import app_identity
from google.appengine.api import mail
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
                    checked_in.append(p)
                else:
                    checked_out.append(p)
                if p.do_not_disturb:
                    has_dnd_on.append(p)
            # Check for and delete expired sticky notes
            for sticky_note in Sticky.query().filter(Sticky.home_key == person.home_key).fetch():
                if sticky_note.expiration < time.time():
                    sticky_note.key.delete()
                else:
                    home_stickies.append(sticky_note)
            # fetch chores
            chores = Chore.query().filter(Chore.home_key==home[0].key).fetch()
            # update chores
            for chore in chores:
                if chore.end_time < time.time():
                    chore.end_time = chore.end_time + chore.duration
                    chore.index = (chore.index + 1)%len(chore.workers)
                    chore.completed = False
                    chore.put()
            # fetch bills
            bills = Bills.query().filter(Bills.home_key==home[0].key).fetch()


            # fetch room name
            room_name = home[0].name

            # for person in people_in_home:
            #   logging.info(person.name)

            return_data = {'room_name': room_name, 'bills': bills, 'chores': chores, 'checked_in' : checked_in, 'checked_out' : checked_out, 'has_dnd_on' : has_dnd_on ,'home_stickies' : home_stickies, 'person': person}
            return return_data


#Currently Unused
def dndEnabled(self, enabler):
	home = Home.query().filter(Home.key == enabler.home_key).fetch()
	for id in home[0].occupants:
		people_in_home.append(Person.query().filter(id == Person.user_id).fetch()[0])
	for person in people_in_home:
		if not person.user_id == enabler.user_id:
			email_content = "Dear " + person.name +",\n" + enabler.name + " has turned on do not disturb for your room. Enter with caution. Or better yet, not at all. ;)\nSincerely,\nThe Roomates Developer Team"
			# Import smtplib for the actual sending function
			sendEmail(person.user_id, enabler.email, 'Do Not Disturb Enabled', email_content)


def send_dnd_mail(sender_address, name, receipient_address):
    # [START send_message]
    message = mail.EmailMessage(
        sender=sender_address,
        subject= "ALERT: " + name + " has turned on Do Not Disturb")

    message.to = receipient_address
    message.body = "ALERT: " + name + " has turned on Do Not Disturb.  From, your friends at Roommates"
    message.send()
    # [END send_message]

def removeFromRoom(self, user):
	person = login.is_roommate_account_initialized(user)
	
	if person:
		home = Home.query().filter(Home.key == person.home_key).fetch()[0]
		logging.info("Person: ")
		logging.info(person)
		logging.info("Home Occupants: ")
		logging.info(home.occupants)
	else:
		logging.info("no person")
	
	#Removes person from record of Home
	if person.user_id in home.occupants:
		home.occupants.remove(person.user_id)
		logging.info("Home occupants: ")
		logging.info(home.occupants)
		chores = Chore.query().filter(Chore.home_key == home.key)
		bills = Bills.query().filter(Bills.home_key == home.key)
		if len(home.occupants) == 0:
			
			for c in chores:
				c.key.delete()
			
			for b in bills:
				b.key.delete()
			home.key.delete()
		else: #Creo que esto funcione
			for c in chores:
				c.workers.remove(person.user_id)
			for b in bills:
				if b.payer_id == person.user_id:
					b.key.delete()
			home.put()
		#Find stickies associated with person
		stickies = Sticky.query().filter(Sticky.author == person.user_id)
		for note in stickies:
			note.key.delete()
		#Updates person and home entries
		person.key.delete()









def sendSMS(to, message):
    # replace with your credentials from: https://www.twilio.com/user/account
    account_sid = "SK205e8dc6c1bcdc8d8f1f1cffd7bc79e9"
    auth_token = "BPEfbiNoBLcGJqmix1G2xGrkAFT175ei"
    client = TwilioRestClient(account_sid, auth_token)
    # replace "to" and "from_" with real numbers
    rv = client.messages.create(to="+1" + to,
                                from_="+16304493710",
                                body=message)
    self.response.write(str(rv))



