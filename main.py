# the import section
import webapp2
import jinja2
import os
import json
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb


# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/index.html')
        self.response.write(index_template.render())

class UserPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/user.html')
        self.response.write(index_template.render())

# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/users', UserPage)
], debug=True)
