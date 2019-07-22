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

class GenericPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/generic.html')
        self.response.write(index_template.render())

class ElementsPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/elements.html')
        self.response.write(index_template.render())

class UserPage(webapp2.RequestHandler):
    def get(self): #for a get request
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/user.html')
        self.response.write(index_template.render())
    # def get(self): #for a get request
    #     user = users.get_current_user()
    #     self.response.headers['Content-Type'] = 'text/html'
    #     index_template = JINJA_ENV.get_template('templates/user.html')
    #     values ={
    #     'user': user,
    #     'login_url': users.create_login_url('/user'),
    #     'logout_url': users.create_logout_url('/user'),
    #     }
    #     self.response.write(index_template.render(values))
    #
    # def post(self):
class LogInPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/login.html')
        values ={
        'user': user,
        'login_url': users.create_login_url('/login'),
        'logout_url': users.create_logout_url('/login'),
        }
        self.response.write(index_template.render(values))


# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), ('/generic', GenericPage), ('/index', MainPage), ('/elements', ElementsPage),
     ('/users', UserPage), ('/login', LogInPage)], debug=True)
