# the import section
import webapp2
import jinja2
import os
import json
import datetime
import logging
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

def toDict(msg):
    return {
    'sentFrom': msg.sentFrom,
    'sentTo': msg.sentTo,
    'msg': msg.msg,
    'timeSent': msg.timeSent
    }

def allToDict(messages):
    out = []
    for msg in messages:
        out.append(toDict(msg))
    return out

class User(ndb.Model):
    # A database entry representing a message
    full_name = ndb.StringProperty()
    id = ndb.StringProperty()
    languages_spoken = ndb.StringProperty()#repeated=True
    languages_to_learn = ndb.StringProperty()#repeated=True
    friends = ndb.StringProperty()#repeated=True
    timeSent = ndb.StringProperty()
    language_proficiency = ndb.StringProperty()


class Message(ndb.Model):
    # A database entry representing a message
    sentFrom = ndb.StringProperty()
    sentTo = ndb.StringProperty()
    msg = ndb.StringProperty()
    timeSent = ndb.StringProperty()

# the handler section
class MainPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/index.html')
        values ={
        'user': user,
        'login_url': users.create_login_url('/adduser'),
        'logout_url': users.create_logout_url('/'),
        }
        if user:
            print "blah blah blah" + str(user.user_id())
        User.query(ancestor=root_parent()).fetch(),
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
            if user:
                self.response.headers['Content-Type'] = 'text/html'
                index_template = JINJA_ENV.get_template('templates/chatroom.html')

                self.response.write(index_template.render())
            else:
                self.redirect('/')

        def post(self):
            user = users.get_current_user()
            logging.debug(user.user_id())
            new_msg = Message(parent=root_parent())
            new_msg.sentFrom = user.user_id()
            new_msg.sentTo = str(self.request.get("id"))
            new_msg.msg = self.request.get("chatText")
            new_msg.timeSent = str(datetime.datetime.now())
            new_msg.put()
            # redirect to '/' so that the get() version of this handler will run
            # and show the list of dogs.
            self.redirect('/chatroom?id=' + self.request.get("id"))


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
class AddUser(webapp2.RequestHandler):
    def post(self):
        user = users.get_current_user()

        other_new_user = User(parent=root_parent())
        other_new_user.full_name = ""
        other_new_user.id = user.user_id()
        other_new_user.languages_spoken = ""
        other_new_user.languages_to_learn = ""
        other_new_user.language_proficiency = ""
        other_new_user.timeSent = str(datetime.datetime.now())
        other_new_user.put()

        self.redirect('/settings')

class LogInPage(webapp2.RequestHandler):
    def get(self): #for a get request

        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/login.html')

class SettingsPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/settings.html')
        listofusers = User.query(User.id == user.user_id()).fetch()

        test = ""

        if len(listofusers) > 0:
            values = {
            'user': user,
            'logout_url': users.create_logout_url('/'),
            'printuser' : listofusers[0]
            }
        else:
            values = {
            'user': user,
            'logout_url': users.create_logout_url('/'),
            'printuser' : test
            }
        self.response.write(index_template.render(values))

    def post(self):
        user = users.get_current_user()
        values = {
        'user': user,
        'logout_url': users.create_logout_url('/'),
        }
        newUser = User(parent=root_parent())
        newUser.full_name = self.request.get('name')
        newUser.id = user.user_id()
        newUser.languages_spoken = self.request.get('spoken')
        newUser.languages_to_learn = self.request.get('learn')
        newUser.timeSent = str(datetime.datetime.now())
        newUser.language_proficiency = self.request.get('proguy')
        newUser.put()

        self.redirect('/settings')

class SearchPage(webapp2.RequestHandler):
    def get(self): #for a get request

        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/search.html')
        self.response.write(index_template.render())

class IntermediatePage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/intermediate.html')
        values ={
        'user': user,
        'logout_url': users.create_logout_url('/'),
        }
        self.response.write(index_template.render(values))

class AjaxGetMessages(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # Part of broken query:
        # ndb.OR(ndb.AND(Message.sentFrom == user.user_id(), Message.sentTo == otherUser),
        #        ndb.AND(Message.sentTo == user.user_id(), Message.sentFrom == otherUser)))
        data = {
            'messages': allToDict(Message.query(ancestor=root_parent()).order(Message.timeSent, Message.msg).fetch())
        }
        self.response.headers['Content-Type'] = 'application/json'
        print(data)
        self.response.write(json.dumps(data))


# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), ('/generic', GenericPage), ('/index', MainPage), ('/elements', ElementsPage),
     ('/users', UserPage), ('/chatroom', ChatPage), ('/settings', SettingsPage), ('/search', SearchPage),
     ('/ajax/AjaxGetMessages', AjaxGetMessages),("/chats", IntermediatePage), ('/adduser', AddUser)
     ], debug=True)
