# the import section
import webapp2
import jinja2
import os
import json
import datetime
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb


# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():
    return ndb.Key('Parent', 'default_parent')

class Message(ndb.Model):
    # A database entry representing a message
    sentFrom = ndb.StringProperty()
    sentTo = ndb.StringProperty()
    msg = ndb.StringProperty(repeated=True)
    timeSent = ndb.StringProperty()

# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/index.html')
        values ={
        'user': user,
        'login_url': users.create_login_url('/users'),
        'logout_url': users.create_logout_url('/'),
        }
        self.response.write(index_template.render(values))

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

class ChatPage(webapp2.RequestHandler):
        def get(self):
            user = users.get_current_user()
            self.response.headers['Content-Type'] = 'text/html'
            index_template = JINJA_ENV.get_template('templates/chatroom.html')
            otherUser = self.request.get("id")
            data = {
                'messages': Message.query(ndb.OR(ndb.AND(user.user_id() == Message.sentFrom, otherUser == Message.sentTo), ndb.AND(user.user_id() == Message.sentTo, otherUser == Message.sentFrom)).order(Message.timeSent, Message.msg))
            }
            self.response.write(index_template.render(data))

        def post(self):
            user = users.get_current_user()
            new_msg = Message(parent=root_parent())
            new_msg.sentFrom = user.user_id()
            new_msg.sendTo = self.request.get("id")
            new_msg.msg = self.request.get("chatText")
            new_msg.timeSent = str(datetime.datetime.now())
            new_msg.put()
            # redirect to '/' so that the get() version of this handler will run
            # and show the list of dogs.
            self.redirect('/chatroom.html')


class UserPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/user.html')
        values ={
        'user': user,
        'logout_url': users.create_logout_url('/'),
        }
        self.response.write(index_template.render(values))
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

        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/login.html')

class SettingsPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/settings.html')
        values ={
        'user': user,
        'logout_url': users.create_logout_url('/'),
        }
        self.response.write(index_template.render(values))

class SearchPage(webapp2.RequestHandler):
    def get(self): #for a get request

        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/search.html')
        self.response.write(index_template.render())


# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), ('/generic', GenericPage), ('/index', MainPage), ('/elements', ElementsPage),
     ('/users', UserPage), ('/chatroom', ChatPage), ('/settings', SettingsPage), ('/search', SearchPage)
     ], debug=True)
