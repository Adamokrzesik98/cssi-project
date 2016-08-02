#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Models
from person import Person
from home import Home
from sticky import Sticky
from chores import Chore
from bills import Bills


# Personal Libraries
import helpers
import login
import render
import logging
#import my_calendar



# Outside libraries
from google.appengine.api import users
import jinja2
import os
import time
#import json        DELETE IF NOT USED
#import urllib
#import urllib2
import webapp2



# Initialize Jinja Environment
env = jinja2.Environment(loader= jinja2.FileSystemLoader('templates'))



# Main Handler that either shows the login page, the create an account page, or the dashboard
class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            # Check if user has an account set up
            person = login.is_roommate_account_initialized(user)
            if person:
                # Render Dashboard
                helpers.redirect(self, '/dashboard', 0)
            # Otherwise, prompt user to create account
            else:
                #redirect to create account page
                helpers.redirect(self, '/create_account', 0)
        # If there is no user, prompt client to login
        else:
            login.render_login_page(self)



class DashboardHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                render_data = helpers.getDashData(self, person)
                render.render_page_with_data(self, 'dashboard.html', "Developer" +"'s Dashboard", render_data)
            else:
               helpers.redirect(self, '/', 0) 
        else:
            helpers.redirect(self, '/', 0)



class CreateStickyHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                render.render_page(self, 'createSticky.html', "Create a Sticky")
            else:
                helpers.redirect(self, '/', 0)
        else:
            helpers.redirect(self, '/', 0)
        
    def post(self):
        user = users.get_current_user()
        if user:
            # Retrieve data from form
            title = self.request.get('title')
            content = self.request.get('content')
            days = int(self.request.get('days'))
            hours = int(self.request.get('hours'))
            # Convert 'on' or 'off' from checkbox to True or False 
            important_original = self.request.get('important')
            if important_original == 'on':
                important = True
            else:
                important = False
            # Retrieve person and home objects
            person = login.is_roommate_account_initialized(user)
            home = Home.query().filter(Home.key == person.home_key).fetch()
            # Calculate expiration time
            cur_time = time.time()
            expir_time = cur_time + days*24*60*60 + hours*60*60
            # Create and put new sticky
            new_sticky = Sticky(title= title, content= content, important= important, author= person.user_id, home_key= person.home_key, expiration= expir_time)
            new_sticky.put()
            render.render_page(self, 'stickyCreated.html', "Sticky Created")
            helpers.redirect(self, '/dashboard', 1000)

class AssignBillHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                home = Home.query(Home.key == person.home_key).fetch()[0]
                possible_payers = []
                for user_id in home.occupants:
                    p = Person.query().filter(Person.user_id == user_id).fetch()[0]
                    possible_payers.append(p)
                data = {'payers': possible_payers}
                render.render_page_with_data(self, 'bills.html', 'Assign a Bill', data)
            else:
                helpers.redirect(self, '/', 0)
        else:
            helpers.redirect(self, '/', 0)
    def post(self):
        user = users.get_current_user()
        person = login.is_roommate_account_initialized(user)
        home = Home.query(Home.key == person.home_key).fetch()[0]
        bill_name = self.request.get('bill_name')
        payer_id = self.request.get('payer')
        payer_name = Person.query().filter(Person.user_id == payer_id).fetch()[0].name
        bill = Bills(bill_name=bill_name, payer_id=payer_id, payer_name = payer_name)
        bill.put()
        render.render_page(self, 'billsCreated.html', 'Bill Created')
        helpers.redirect(self, '/dashboard', 1000)




class CreateChoreHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                home = Home.query(Home.key == person.home_key).fetch()[0]
                rotation_list = []
                for user_id in home.occupants:
                    p = Person.query().filter(Person.user_id == user_id).fetch()[0]
                    rotation_list.append(p)
                data = {'rotation_list': rotation_list}
                render.render_page_with_data(self, 'chores.html', 'Create a Chore', data)
            else:
                helpers.redirect(self, '/', 0)
        else:
            helpers.redirect(self, '/', 0)

    def post(self):
        user = users.get_current_user()
        person = login.is_roommate_account_initialized(user)
        home = Home.query(Home.key == person.home_key).fetch()[0]
        home_key = home.key
        chore_name = self.request.get('chore_name')
        duration = int(self.request.get('days'))
        cur_time = time.time()
        duration = duration*24*60*60
        end_time = cur_time + duration
        workers = []
        workers_names = []
        for p in home.occupants:
            if self.request.get(p) == 'on':
                workers.append(p)
                per = Person.query().filter(Person.user_id == p).fetch()[0].name
                workers_names.append(per)
        chore = Chore(home_key= home_key, workers_names = workers_names, chore_name= chore_name, duration=duration, end_time=end_time, workers=workers)
        chore.put()
        render.render_page(self, 'choreCreated.html', 'Chore Created')
        helpers.redirect(self, '/dashboard', 1000)


class DoNotDisturbHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                if(person.do_not_disturb):
                    person.do_not_disturb = False
                    data = {'dnd_state' : 'Do not disturb is off.'}
                    person.put()
                else:
                    person.do_not_disturb = True
                    data = {'dnd_state' : 'DO NOT DISTURB!'}
                    person.put()
                render.render_page_with_data(self, 'doNotDisturb.html', "Do Not Disturb Toggle", data)
                helpers.redirect(self, '/dashboard', 1000)
            else:
                helpers.redirect(self, '/', 0)
        else:
            helpers.redirect(self, '/', 0)



class CheckInOutHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                if(person.location):
                    person.location = False
                    person.put()
                else:
                    person.location = True
                    person.put()
                if(person.location):
                    data = {'check_in_state' : 'Checked In!'}
                else:
                    data = {'check_in_state' : 'Checked Out!'}
                render.render_page_with_data(self, 'checkInState.html', "Check In or Out", data)
                helpers.redirect(self, '/dashboard', 1000)
            else:
             helpers.redirect(self, '/',0)   
        else:
            helpers.redirect(self, '/',0)




class DeleteStickyHandler(webapp2.RequestHandler):
    def post(self): 
        None
#        sticky_expir = float(self.request.get('sticky_expir').replace("u'","").replace("'",""))
#        sticky = Sticky.query().filter(Sticky.expiration==sticky_expir).fetch()[0]
#        sticky.key.delete()
#        helpers.redirect(self, '/dashboard', 1000)



class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            person = login.is_roommate_account_initialized(user)
            if not person:
                login.initialize_roommate_account(self)
            else:
             helpers.redirect(self, '/dashboard',0)   
        else:
            helpers.redirect(self, '/',0)

    def post(self):
        #retrieve data from form
        name = self.request.get('name')
        phone_number = int(self.request.get('phone_number1') + self.request.get('phone_number2') + self.request.get('phone_number3'))
        #create new person object
        user = users.get_current_user()
        person = Person(name= name, phone_number = phone_number, user_id = user.user_id(), email_address = user.email())
        person.put()
        #redirect to join or create a home page
        helpers.redirect(self, '/create_home', 500)



class CreateHomeHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                # Display create a Home page
                render.render_page_without_header(self, 'createHome.html', 'Create a Home')
            else:
               helpers.redirect(self, '/',0)
        # If there is no user, prompt client to login
        else:
            helpers.redirect(self, '/',0)

    def post(self):
        #retrieve data from form
        home_name = self.request.get('name')
        password = self.request.get('password')
        #create new person object
        user = users.get_current_user()
        person = login.is_roommate_account_initialized(user)
        new_home = Home(name= home_name, password = password, occupants = [user.user_id()])
        person.home_key = new_home.put()
        person.put()
        #redirect to create a calendar
        helpers.redirect(self, '/dashboard',1000)



class JoinHomeHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                # Display create a Home page
                render.render_page_without_header(self, 'joinHome.html', 'Join a Home')
            else:
               helpers.redirect(self, '/',0)
        # If there is no user, prompt client to login
        else:
            helpers.redirect(self, '/',0)

    def post(self):
        user = users.get_current_user()
        person = login.is_roommate_account_initialized(user)
        #retrieve data from form
        home_name = self.request.get('name')
        password = self.request.get('password')
        # Query for home object
        potential_home = Home.query().filter(Home.name == home_name, Home.password == password).fetch()
        if potential_home:
            potential_home[0].occupants.append(user.user_id())
            home_key = potential_home[0].put()
            person.home_key = home_key
            person.put()
            data = {'home_name': home_name}
            render.render_page_with_data(self, 'successfullyJoinedHome.html', 'Successfully Joined Home', data)
            helpers.redirect(self, '/dashboard', 1000)
        else:
            # REPORT to client to try again. wrong name or password
            data = {'error': 'You have entered an incorrect home name or password'}
            render.render_page_without_header_with_data(self, 'joinHome.html', 'Error: Wrong Name or Password', data)


        ## TODO: redirect to create a calendar
        




class CreateCalendarHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                # Display Calendar
                None
#                cals = my_calendar.get_calender_list()
#                data = {"cals": cals}
#                render.render_page_with_data(self, 'createCalendar.html', 'Create a Schedule', data)
            else:
               helpers.redirect(self, '/',0)
        # If there is no user, prompt client to login
        else:
            helpers.redirect(self, '/',0)



class TemplateHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()

        # Check if there is a user signed in
        if user:

            person = login.is_roommate_account_initialized(user)
            if person:
                None

        # If there is no user, prompt client to login
        else:
            helpers.redirect(self, '/',0)




class DeveloperHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)

        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))

class SettingsHandler(webapp2.RequestHandler):
    def get(self):
        render.render_page(self, 'settings.html', 'Settings')

class LeaveRoomHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            #Add mini-form to ask if stickies should be deleted, replace True with var name
            helpers.removeFromRoom(self, user, True) #Add confirmation for leaving room
            helpers.redirect(self, '/create_home', 0)
        else:
            helpers.redirect(self, '/', 0)
        

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/do_not_disturb', DoNotDisturbHandler),
    ('/check_in_out', CheckInOutHandler),
    ('/create_sticky', CreateStickyHandler),
    ('/dashboard', DashboardHandler),
    ('/delete_sticky', DeleteStickyHandler),
    ('/create_account', CreateAccountHandler),
    ('/create_home', CreateHomeHandler),
    ('/join_home', JoinHomeHandler),
    ('/create_calendar', CreateCalendarHandler),
    ('/developer', DeveloperHandler),
    ('/settings', SettingsHandler),
    ('/create_a_chore', CreateChoreHandler),
    ('/leaveRoom', LeaveRoomHandler),
    ('/assign_bills',AssignBillHandler)
], debug=True)
