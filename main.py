# the import section
import webapp2
import jinja2
import os
import json
import datetime
import logging
import urllib
import ssl
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import ndb
import api_key

# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():
    return ndb.Key('Parent', 'default_parent')

def translateSentence():
    try:
        form_data = urllib.urlencode({
            'q': 'The Great Pyramid of Giza (also known as the Pyramid of Khufu or the Pyramid of Cheops) is the oldest and largest of the three pyramids in the Giza pyramid complex.',
            'source': 'en',
            'target': 'es',
            'format': 'text'
        })

        languages = {
        'aa': 'Afar',
        'ab': 'Abkhazian',
        'af': 'Afrikaans',
        'ak': 'Akan',
        'sq': 'Albanian',
        'am': 'Amharic',
        'ar': 'Arabic',
        'an': 'Aragonese',
        'hy': 'Armenian',
        'as': 'Assamese',
        'av': 'Avaric',
        'ae': 'Avestan',
        'ay':'Aymara',
        'az': 'Azerbaijani',
        'ba': 'Bashkir',
        'bm': 'Bambara',
        'eu': 'Basque',
        'be': 'Belarusian',
        'bn': 'Bengali',
        'bi': 'Bislama',
        'bo':'Tibetan',
        'bs': 'Bosnian',
        'br': 'Breton',
        'bg': 'Bulgarian',
        'my': 'Burmese',
        'cs':'Czech',
        'ch': 'Chamorro',
        'ce': 'Chechen',
        'zh': 'Chinese',
        'cv': 'Chuvash',
        'kw': 'Cornish',
        'co': 'Corsican',
        'cr': 'Cree',
        'cy': 'Welsh',
        'cs': 'Czech',
        'da': 'Danish',
        'de': 'German',
        'dv': 'Divehi',
        'dz': 'Dzongkha',
        'el': 'Greek',
        'en': 'English',
        'eo': 'Esperanto',
        'et': 'Estonian',
        'eu': 'Basque',
        'ee': 'Ewe',
        'fo': 'Faroese',
        'fa': 'Persian',
        'fj': 'Fijian',
        'fi':'Finnish',
        'fr': 'French',
        'fr': 'French',
        'fy': 'Western Frisian',
        'ff': 'Fulah',
        'Ga': 'Georgian',
        'de': 'German',
        'gd': 'Gaelic',
        'ga': 'Irish',
        'gl': 'Galician',
        'gv': 'Manx',
        'gn': 'Guarani',
        'gu': 'Gujarati',
        'ht': 'Haitian; Haitian Creole',
        'ha': 'Hausa',
        'he': 'Hebrew',
        'hz': 'Herero',
        'hi': 'Hindi',
        'ho': 'Hiri Motu',
        'hr': 'Croatian',
        'hu': 'Hungarian',
        'hy': 'Armenian',
        'ig': 'Igbo',
        'is': 'Icelandic',
        'io': 'Ido',
        'ii': 'Sichuan Yi; Nuosu',
        'iu': 'Inuktitut',
        'ie': 'Interlingue; Occidental',
        'ia': 'Interlingua (International Auxiliary Language Association)',
        'id': 'Indonesian',
        'ik': 'Inupiaq',
        'is': 'Icelandic',
        'it': 'Italian',
        'jv': 'Javanese',
        'ja': 'Japanese',
        'kl': 'Kalaallisut; Greenlandic',
        'kn': 'Kannada',
        'ks': 'Kashmiri',
        'ka': 'Georgian',
        'kr': 'Kanuri',
        'kk': 'Kazakh',
        'km': 'Central Khmer',
        'ki': 'Kikuyu; Gikuyu',
        'rw': 'Kinyarwanda',
        'ky': 'Kirghiz; Kyrgyz',
        'kv': 'Komi',
        'kg': 'Kongo',
        'ko': 'Korean',
        'kj': 'Kuanyama; Kwanyama',
        'ku': 'Kurdish',
        'lo': 'Lao',
        'la': 'Latin',
        'lv': 'Latvian',
        'li': 'Limburgan; Limburger; Limburgish',
        'ln': 'Lingala',
        'lt': 'Lithuanian',
        'lb': 'Luxembourgish; Letzeburgesch',
        'lu': 'Luba-Katanga',
        'lg': 'Ganda',
        'mk': 'Macedonian',
        'mh': 'Marshallese',
        'ml': 'Malayalam',
        'mi': 'Maori',
        'mr': 'Marathi',
        'ms': 'Malay',
        'Mi': 'Micmac',
        'mk': 'Macedonian',
        'mg': 'Malagasy',
        'mt': 'Maltese',
        'mn': 'Mongolian',
        'mi': 'Maori',
        'ms': 'Malay',
        'my': 'Burmese',
        'na': 'Nauru',
        'nv': 'Navajo; Navaho',
        'nr': 'Ndebele, South; South Ndebele',
        'nd': 'Ndebele, North; North Ndebele',
        'ng': 'Ndonga',
        'ne': 'Nepali',
        'nl': 'Dutch; Flemish',
        'no': 'Norwegian',
        'oc': 'Occitan (post 1500)',
        'oj': 'Ojibwa',
        'or': 'Oriya',
        'om': 'Oromo',
        'os': 'Ossetian; Ossetic',
        'pa': 'Punjabi',
        'fa': 'Persian',
        'pi': 'Pali',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ps': 'Pushto; Pashto',
        'qu': 'Quechua',
        'rm': 'Romansh',
        'ro': 'Romanian; Moldavian; Moldovan',
        'rn': 'Rundi',
        'ru': 'Russian',
        'sg': 'Sango',
        'sa': 'Sanskrit',
        'si': 'Sinhala; Sinhalese',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'se': 'Northern Sami',
        'sm': 'Samoan',
        'sn': 'Shona',
        'sd': 'Sindhi',
        'so': 'Somali',
        'st': 'Sotho',
        'es': 'Spanish',
        'sq': 'Albanian',
        'sc': 'Sardinian',
        'sr': 'Serbian',
        'ss': 'Swati',
        'su': 'Sundanese',
        'sw': 'Swahili',
        'sv': 'Swedish',
        'ty': 'Tahitian',
        'ta': 'Tamil',
        'tt': 'Tatar',
        'te': 'Telugu',
        'tg': 'Tajik',
        'tl': 'Tagalog',
        'th': 'Thai',
        'bo': 'Tibetan',
        'ti': 'Tigrinya',
        'to': 'Tonga (Tonga Islands)',
        'tn': 'Tswana',
        'ts': 'Tsonga',
        'tk': 'Turkmen',
        'tr': 'Turkish',
        'tw': 'Twi',
        'ug': 'Uighur; Uyghur',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'uz': 'Uzbek',
        've': 'Venda',
        'vi': 'Vietnamese',
        'cy': 'Welsh',
        'wa': 'Walloon',
        'wo': 'Wolof',
        'xh': 'Xhosa',
        'yi': 'Yiddish',
        'yo': 'Yoruba',
        'za': 'Zhuang; Chuang',
        'zh': 'Chinese',
        'zu': 'Zulu'
        }



        headers = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Bearer ' + api_key.gcpkey
        }
        result = urlfetch.fetch(
            url='https://translation.googleapis.com/language/translate/v2',
            payload=form_data,
            method=urlfetch.POST,
            headers=headers)
        return result.content
    except urlfetch.Error:
        logging.exception('Caught exception fetching url')

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
    friends = ndb.StringProperty(repeated=True)
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
        'login_url': users.create_login_url('/firstLoginCheck'),
        'logout_url': users.create_logout_url('/'),
        }
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

# class LogInPage(webapp2.RequestHandler):
#     def get(self): #for a get request
#
#         self.response.headers['Content-Type'] = 'text/html'
#         index_template = JINJA_ENV.get_template('templates/login.html')

class FirstLoginCheck(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            listofusers = User.query(User.id == user.user_id()).fetch()
        if len(listofusers) > 0:
            self.redirect('/users')
            return
        else:
            self.redirect('/settings')

class SettingsPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        index_template = JINJA_ENV.get_template('templates/settings.html')
        languages = {
        'aa': 'Afar',
        'ab': 'Abkhazian',
        'af': 'Afrikaans',
        'ak': 'Akan',
        'sq': 'Albanian',
        'am': 'Amharic',
        'ar': 'Arabic',
        'an': 'Aragonese',
        'hy': 'Armenian',
        'as': 'Assamese',
        'av': 'Avaric',
        'ae': 'Avestan',
        'ay':'Aymara',
        'az': 'Azerbaijani',
        'ba': 'Bashkir',
        'bm': 'Bambara',
        'eu': 'Basque',
        'be': 'Belarusian',
        'bn': 'Bengali',
        'bh': 'Bihari',
        'bi': 'Bislama',
        'bo':'Tibetan',
        'bs': 'Bosnian',
        'br': 'Breton',
        'bg': 'Bulgarian',
        'my': 'Burmese',
        'ca': 'Catalan',
        'cs':'Czech',
        'ch': 'Chamorro',
        'ce': 'Chechen',
        'zh': 'Chinese',
        'cu': 'Slavic',
        'cv': 'Chuvash',
        'kw': 'Cornish',
        'co': 'Corsican',
        'cr': 'Cree',
        'cy': 'Welsh',
        'cs': 'Czech',
        'da': 'Danish',
        'de': 'German',
        'dz': 'Dzongkha',
        'eo': 'Esperanto',
        'et': 'Estonian',
        'eu': 'Basque',
        'ee': 'Ewe',
        'en': 'English',
        'fo': 'Faroese',
        'fa': 'Persian',
        'fj': 'Fijian',
        'fi':'Finnish',
        'fr': 'French',
        'fr': 'French',
        'fy': 'Western Frisian',
        'ff': 'Fulah',
        'Ga': 'Georgian',
        'de': 'German',
        'gd': 'Gaelic',
        'ga': 'Irish',
        'gl': 'Galician',
        'gv': 'Manx',
        'gn': 'Guarani',
        'gu': 'Gujarati',
        'ht': 'Haitian',
        'ha': 'Hausa',
        'he': 'Hebrew',
        'hz': 'Herero',
        'hi': 'Hindi',
        'ho': 'Hiri Motu',
        'hr': 'Croatian',
        'hu': 'Hungarian',
        'hy': 'Armenian',
        'ig': 'Igbo',
        'is': 'Icelandic',
        'io': 'Ido',
        'ii': 'Sichuan Yi',
        'iu': 'Inuktitut',
        'ie': 'Interlingue; Occidental',
        'id': 'Indonesian',
        'ik': 'Inupiaq',
        'is': 'Icelandic',
        'it': 'Italian',
        'jv': 'Javanese',
        'ja': 'Japanese',
        'kl': 'Kalaallisut',
        'kn': 'Kannada',
        'ks': 'Kashmiri',
        'ka': 'Georgian',
        'kr': 'Kanuri',
        'kk': 'Kazakh',
        'km': 'Central Khmer',
        'ki': 'Kikuyu',
        'rw': 'Kinyarwanda',
        'ky': 'Kirghiz',
        'kv': 'Komi',
        'kg': 'Kongo',
        'ko': 'Korean',
        'kj': 'Kuanyama',
        'ku': 'Kurdish',
        'lo': 'Lao',
        'la': 'Latin',
        'lv': 'Latvian',
        'li': 'Limburgan',
        'ln': 'Lingala',
        'lt': 'Lithuanian',
        'lb': 'Luxembourgish; Letzeburgesch',
        'lu': 'Luba-Katanga',
        'lg': 'Ganda',
        'mk': 'Macedonian',
        'mh': 'Marshallese',
        'ml': 'Malayalam',
        'mi': 'Maori',
        'mr': 'Marathi',
        'ms': 'Malay',
        'Mi': 'Micmac',
        'mk': 'Macedonian',
        'mg': 'Malagasy',
        'mt': 'Maltese',
        'mn': 'Mongolian',
        'mi': 'Maori',
        'ms': 'Malay',
        'my': 'Burmese',
        'na': 'Nauru',
        'nv': 'Navajo; Navaho',
        'nr': 'Ndebele',
        'ng': 'Ndonga',
        'ne': 'Nepali',
        'no': 'Norwegian',
        'oc': 'Occitan (post 1500)',
        'oj': 'Ojibwa',
        'or': 'Oriya',
        'om': 'Oromo',
        'os': 'Ossetian',
        'pa': 'Punjabi',
        'fa': 'Persian',
        'pi': 'Pali',
        'pl': 'Polish',
        'pt': 'Portuguese',
        'ps': 'Pushto; Pashto',
        'qu': 'Quechua',
        'rm': 'Romansh',
        'ro': 'Romanian',
        'rn': 'Rundi',
        'ru': 'Russian',
        'sg': 'Sango',
        'sa': 'Sanskrit',
        'si': 'Sinhala; Sinhalese',
        'sk': 'Slovak',
        'sl': 'Slovenian',
        'se': 'Northern Sami',
        'sm': 'Samoan',
        'sn': 'Shona',
        'sd': 'Sindhi',
        'so': 'Somali',
        'st': 'Sotho',
        'es': 'Spanish',
        'sq': 'Albanian',
        'sc': 'Sardinian',
        'sr': 'Serbian',
        'ss': 'Swati',
        'su': 'Sundanese',
        'sw': 'Swahili',
        'sv': 'Swedish',
        'ty': 'Tahitian',
        'ta': 'Tamil',
        'tt': 'Tatar',
        'te': 'Telugu',
        'tg': 'Tajik',
        'tl': 'Tagalog',
        'th': 'Thai',
        'bo': 'Tibetan',
        'ti': 'Tigrinya',
        'to': 'Tonga',
        'tn': 'Tswana',
        'ts': 'Tsonga',
        'tk': 'Turkmen',
        'tr': 'Turkish',
        'tw': 'Twi',
        'ug': 'Uighur; Uyghur',
        'uk': 'Ukrainian',
        'ur': 'Urdu',
        'uz': 'Uzbek',
        've': 'Venda',
        'vi': 'Vietnamese',
        'cy': 'Welsh',
        'wa': 'Walloon',
        'wo': 'Wolof',
        'xh': 'Xhosa',
        'yi': 'Yiddish',
        'yo': 'Yoruba',
        'za': 'Zhuang; Chuang',
        'zh': 'Chinese',
        'zu': 'Zulu'
        }
        values = {
        'user': user,
        'logout_url': users.create_logout_url('/'),
        'printuser' : '',
        'languages' : languages
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
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        queryName = self.request.get('val')
        listofusers = User.query(ndb.OR(queryName == User.full_name, queryName == User.languages_spoken)).fetch()
        actuallistofusers = []
        currentuser = User.query(User.id == user.user_id()).fetch()
        for x in listofusers:
            if x.id != user.user_id() and x.languages_to_learn == currentuser[0].languages_spoken:
                actuallistofusers.append(x)
        values = {
        'listofusers' : actuallistofusers
        }
        index_template = JINJA_ENV.get_template('templates/search.html')
        self.response.write(index_template.render(values))


class AddFriends(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        id = self.request.get('id')
        my_user = User.query(User.id == user.user_id()).fetch()[0]
        if id not in my_user.friends:
            my_user.friends.append(id)
            my_user.put()
            other_user = User.query(User.id == id).fetch()[0]
            other_user.friends.append(user.user_id())
            other_user.put()
        self.redirect('/chats')

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
        otherUser = self.request.get('id')
        # Part of broken query:
        # ndb.OR(ndb.AND(Message.sentFrom == user.user_id(), Message.sentTo == otherUser),
        #        ndb.AND(Message.sentTo == user.user_id(), Message.sentFrom == otherUser)))
        data = {
            'messages': allToDict(
                Message.query(
                    ndb.OR(
                        ndb.AND(
                            Message.sentFrom == user.user_id(),
                            Message.sentTo == otherUser),
                        ndb.AND(
                            Message.sentTo == user.user_id(),
                            Message.sentFrom == otherUser)
                    ),ancestor=root_parent()).order(Message.timeSent, Message.msg).fetch())
        }
        self.response.headers['Content-Type'] = 'application/json'
        print(data)
        self.response.write(json.dumps(data))


# the app configuration section
app = webapp2.WSGIApplication([
    ('/', MainPage), ('/generic', GenericPage), ('/index', MainPage), ('/elements', ElementsPage),
     ('/users', UserPage), ('/chatroom', ChatPage), ('/settings', SettingsPage), ('/search', SearchPage),
     ('/ajax/AjaxGetMessages', AjaxGetMessages),("/chats", IntermediatePage), ('/add', AddFriends), ('/firstLoginCheck', FirstLoginCheck)
     ], debug=True)
