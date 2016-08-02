from oauth2client import client

def get_credentials():
	flow = client.flow_from_clientsecrets(
	    'client_secret_tester.json',
	    scope='https://www.googleapis.com/auth/calendar.readonly',
	    redirect_uri='http://www.example.com/oauth2callback')