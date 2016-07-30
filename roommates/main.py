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

# Personal Libraries
import helpers
import login
import render

# Outside libraries
from google.appengine.api import users
import jinja2
import os
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
                ######### Create Function that takes person as input to render dashboard ##########
                render.render_page(self, 'dashboard.html', person.name +"'s Dashboard")

            # Otherwise, prompt user to create account
            else:
                #redirect to create account page
                helpers.redirect(self, '/create_account')
         
        # If there is no user, prompt client to login 
        else:
            login.render_login_page(self)


class CreateAccountHandler(webapp2.RequestHandler):
    def get(self):
        login.initialize_roommate_account(self)

    def post(self):
        #retrieve data from form
        name = self.request.get('name')
        phone_number = int(self.request.get('phone_number1') + self.request.get('phone_number2') + self.request.get('phone_number3'))

        #create new person object
        user = users.get_current_user()
        person = Person(name= name, phone_number = phone_number, user_id = user.user_id())
        person.put()

        #redirect to join or create a home page
        helpers.redirect(self, '/create_home')


class CreateHomeHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                # Display create a Home page
                render.render_page(self, 'createHome.html', 'Create a Home')
            else:
               helpers.redirect(self, '/') 
        # If there is no user, prompt client to login 
        else:
            helpers.redirect(self, '/')

    def post(self):
        #retrieve data from form
        home_name = self.request.get('name')
        password = self.request.get('password')

        #create new person object
        user = users.get_current_user()
        new_home = Home(name= home_name, password = password, occupants = [user.user_id()])
        new_home.put()

        #redirect to join or create a home page
        helpers.redirect(self, '/calendar')

class JoinHomeHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                # Display create a Home page
                render.render_page(self, 'joinHome.html', 'Join a Home')
            else:
               helpers.redirect(self, '/') 
        # If there is no user, prompt client to login 
        else:
            helpers.redirect(self, '/')

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

            ## TODO: Render a successfully joined page
        else:
            ## TODO: REPORT to client to try again. wrong name or password
            None
        

        #redirect to join or create a home page
#        helpers.redirect(self, '/calendar')

class CalendarHandler(webapp2.RequestHandler):
    def get(self):
        # Get current google account that is signed in
        user = users.get_current_user()
        # Check if there is a user signed in
        if user:
            person = login.is_roommate_account_initialized(user)
            if person:
                # Display create a Home page
                render.render(self, 'createHome.html', 'Create a Home')
            else:
               helpers.redirect(self, '/') 
        # If there is no user, prompt client to login 
        else:
            helpers.redirect(self, '/')



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
            helpers.redirect(self, '/')

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

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/create_account', CreateAccountHandler),
    ('/create_home', CreateHomeHandler),
    ('/join_home', JoinHomeHandler),
    ('/developer', DeveloperHandler)
], debug=True)



#            logout_url = users.create_logout_url('/')
#            logout = env.get_template('logout.html')
#            data = {'url': logout_url}
