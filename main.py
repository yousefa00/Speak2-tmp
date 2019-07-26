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
from collections import OrderedDict

# This initializes the jinja2 Environment.
# This will be the same in every app that uses the jinja2 templating library.
JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def root_parent():
    return ndb.Key('Parent', 'default_parent')

# def getAPIKey():
#     form_data = urllib.urlencode({
#         "delegates": [],
#         "scope": [
#         "https://www.googleapis.com/auth/cloud-platform"
#         ],
#         "lifetime": "300s"
#     })
#     result = urlfetch.fetch(
#         url='https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/speak2@appspot.gserviceaccount.com:generateAccessToken',
#         payload=form_data,
#         method=urlfetch.POST)
#     print result.content

def translateSentence(textToTranslate, sourceLang, targetLang):
    try:

        inverted_languages = {'Estonian': 'et', 'Telugu': 'te', 'Limburgan; Limburger; Limburgish': 'li', 'Uighur; Uyghur': 'ug', 'Pushto; Pashto': 'ps', 'Cornish': 'kw','Bulgarian': 'bg', 'Norwegian': 'no', 'Yoruba': 'yo', 'Bambara': 'bm', 'French': 'fr', 'Fijian': 'fj', 'Bengali': 'bn', 'Tsonga': 'ts', 'Tamil': 'ta', 'Ossetian; Ossetic': 'os', 'Samoan': 'sm', 'Nepali': 'ne', 'Finnish': 'fi', 'Manx': 'gv', 'Sundanese': 'su', 'Albanian': 'sq', 'Ojibwa': 'oj', 'Tagalog': 'tl', 'Serbian': 'sr', 'Malayalam': 'ml', 'Haitian; Haitian Creole': 'ht', 'Aragonese': 'an', 'Italian': 'it', 'Walloon': 'wa', 'Hebrew': 'he', 'Chamorro': 'ch', 'Bislama': 'bi', 'Kongo': 'kg', 'Micmac': 'Mi', 'Galician': 'gl', 'German': 'de', 'Slovak': 'sk', 'Yiddish': 'yi', 'Tonga (Tonga Islands)': 'to', 'Polish': 'pl', 'Xhosa': 'xh', 'Marshallese': 'mh', 'Kuanyama; Kwanyama': 'kj', 'Marathi': 'mr','Slovenian': 'sl', 'Ewe': 'ee', 'Fulah': 'ff', 'Azerbaijani': 'az', 'Faroese': 'fo', 'Nauru': 'na', 'Cree': 'cr', 'Danish': 'da', 'Indonesian': 'id', 'Latin': 'la', 'Zulu': 'zu', 'Georgian': 'ka', 'Tigrinya': 'ti', 'Ganda': 'lg', 'Komi': 'kv', 'Tajik': 'tg', 'Thai': 'th', 'Afrikaans': 'af', 'Tibetan': 'bo', 'Turkmen': 'tk', 'Ndebele, North; North Ndebele': 'nd', 'Central Khmer': 'km', 'Avaric': 'av', 'Guarani': 'gn', 'Uzbek': 'uz', 'Divehi': 'dv', 'Punjabi': 'pa', 'Herero': 'hz', 'Gaelic': 'gd', 'Burmese': 'my', 'Maori': 'mi', 'Latvian': 'lv', 'English': 'en', 'Interlingue; Occidental': 'ie', 'Lingala': 'ln', 'Chinese': 'zh', 'Greek': 'el', 'Inuktitut': 'iu', 'Tatar': 'tt', 'Pali': 'pi', 'Bosnian': 'bs', 'Arabic': 'ar', 'Venda': 've', 'Breton': 'br', 'Kikuyu; Gikuyu': 'ki', 'Swahili': 'sw', 'Swedish': 'sv', 'Interlingua (International Auxiliary Language Association)': 'ia', 'Icelandic': 'is', 'Turkish': 'tr', 'Kalaallisut; Greenlandic': 'kl', 'Twi': 'tw', 'Inupiaq': 'ik', 'Malay': 'ms', 'Luxembourgish; Letzeburgesch': 'lb', 'Gujarati': 'gu', 'Hindi': 'hi', 'Ndebele, South; South Ndebele': 'nr', 'Sindhi': 'sd', 'Korean': 'ko', 'Malagasy': 'mg', 'Chuvash': 'cv', 'Zhuang; Chuang': 'za', 'Occitan (post 1500)': 'oc', 'Hungarian': 'hu', 'Wolof': 'wo', 'Igbo': 'ig', 'Lithuanian': 'lt', 'Kirghiz; Kyrgyz': 'ky', 'Sinhala; Sinhalese': 'si', 'Russian': 'ru', 'Croatian': 'hr', 'Kazakh': 'kk', 'Armenian': 'hy', 'Kashmiri': 'ks', 'Hiri Motu': 'ho', 'Amharic': 'am', 'Romansh': 'rm', 'Javanese': 'jv', 'Oriya': 'or', 'Afar': 'aa', 'Hausa': 'ha', 'Irish': 'ga', 'Navajo; Navaho': 'nv', 'Czech': 'cs', 'Belarusian': 'be', 'Kannada': 'kn', 'Macedonian': 'mk', 'Persian': 'fa', 'Mongolian': 'mn', 'Dzongkha': 'dz', 'Basque': 'eu', 'Aymara': 'ay', 'Romanian; Moldavian; Moldovan': 'ro', 'Dutch; Flemish': 'nl', 'Northern Sami': 'se', 'Vietnamese': 'vi', 'Shona': 'sn', 'Sardinian': 'sc', 'Western Frisian': 'fy', 'Corsican': 'co', 'Swati': 'ss', 'Chechen': 'ce', 'Somali': 'so', 'Sanskrit': 'sa', 'Akan': 'ak', 'Lao': 'lo', 'Ukrainian': 'uk', 'Welsh': 'cy', 'Tahitian': 'ty', 'Maltese': 'mt', 'Sichuan Yi; Nuosu': 'ii', 'Assamese': 'as', 'Kurdish': 'ku', 'Urdu': 'ur', 'Kanuri': 'kr', 'Bashkir': 'ba', 'Luba-Katanga': 'lu', 'Spanish': 'es', 'Tswana': 'tn', 'Ido': 'io', 'Sango': 'sg', 'Oromo': 'om', 'Rundi': 'rn', 'Portuguese': 'pt', 'Abkhazian': 'ab', 'Ndonga': 'ng', 'Japanese': 'ja', 'Kinyarwanda': 'rw', 'Avestan': 'ae', 'Sotho': 'st', 'Quechua': 'qu', 'Esperanto': 'eo'}

        form_data = urllib.urlencode({
            'q': textToTranslate.encode('utf-8'),
            'source': inverted_languages[sourceLang],
            'target': inverted_languages[targetLang],
            'format': 'text'
        })



        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        result = urlfetch.fetch(
            url='https://translation.googleapis.com/language/translate/v2?key=' + api_key.gcpkey,
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
    'translated': msg.translated,
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
    languages_spoken = ndb.StringProperty() #repeated=True
    languages_to_learn = ndb.StringProperty()#repeated=True
    friends = ndb.StringProperty(repeated=True)
    timeSent = ndb.StringProperty()

class Message(ndb.Model):
    # A database entry representing a message
    sentFrom = ndb.StringProperty()
    sentTo = ndb.StringProperty()
    msg = ndb.StringProperty()
    timeSent = ndb.StringProperty()
    translated = ndb.StringProperty()

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
            my_user = User.query(User.id == user.user_id()).fetch()[0]
            other_user = User.query(User.id == str(self.request.get("id"))).fetch()[0]
            new_msg = Message(parent=root_parent())
            new_msg.sentFrom = user.user_id()
            new_msg.sentTo = str(self.request.get("id"))
            new_msg.msg = self.request.get("chatText")
            new_msg.translated = json.loads(translateSentence(self.request.get("chatText"), my_user.languages_spoken, other_user.languages_spoken))["data"]["translations"][0]["translatedText"]
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
        myself = User.query(User.id == user.user_id()).fetch()[0]
        myfriends = []
        if len(myself.friends) >0:
            for x in myself.friends:
                myfriends.append(User.query(User.id == x).fetch()[0])
        values ={
        'user': user,
        'logout_url': users.create_logout_url('/'),
        'myfriends' : myfriends
        }
        self.response.write(index_template.render(values))

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
        # languageactual = OrderedDict()
        languages= {
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
        'cr': 'Cree',
        'cy': 'Welsh',
        'da': 'Danish',
        'de': 'German',
        'dz': 'Dzongkha',
        'eo': 'Esperanto',
        'et': 'Estonian',
        'ee': 'Ewe',
        'en': 'English',
        'fo': 'Faroese',
        'fa': 'Persian',
        'fj': 'Fijian',
        'fi':'Finnish',
        'fr': 'French',
        'ff': 'Fulah',
        'Ga': 'Georgian',
        'de': 'German',
        'gd': 'Gaelic',
        'ga': 'Irish',
        'gl': 'Galician',
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
        'ig': 'Igbo',
        'is': 'Icelandic',
        'io': 'Ido',
        'ii': 'Sichuan Yi',
        'iu': 'Inuktitut',
        'id': 'Indonesian',
        'ik': 'Inupiaq',
        'is': 'Icelandic',
        'it': 'Italian',
        'jv': 'Javanese',
        'ja': 'Japanese',
        'kl': 'Kalaallisut',
        'kn': 'Kannada',
        'ks': 'Kashmiri',
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
        'lb': 'Luxembourgish',
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
        'nv': 'Navajo',
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
        printuser = User.query(User.id == user.user_id(),ancestor=root_parent()).fetch()
        if len(printuser) == 0:
            printuser = None
        else:
            printuser = printuser[0]

        values = {
        'user': user,
        'logout_url': users.create_logout_url('/'),
        'printuser' : printuser,
        'languages' : languages
        }
        self.response.write(index_template.render(values))

    def post(self):
        user = users.get_current_user()
        values = {
        'user': user,
        'logout_url': users.create_logout_url('/'),
        }
        iammyself = User.query(User.id == user.user_id()).fetch()
        if len(iammyself) > 0:
            iammyself[0].full_name = self.request.get('name')
            iammyself[0].languages_spoken = self.request.get('spoken')
            iammyself[0].languages_to_learn = self.request.get('learn')
            iammyself[0].timeSent = str(datetime.datetime.now())
            iammyself[0].put()
        else:
            newUser = User(parent=root_parent())
            newUser.full_name = self.request.get('name')
            newUser.id = user.user_id()
            newUser.languages_spoken = self.request.get('spoken')
            newUser.languages_to_learn = self.request.get('learn')
            newUser.timeSent = str(datetime.datetime.now())
            newUser.put()

        self.redirect('/settings')

    # def post(self):
    #     user = users.get_current_user()
    #     values = {
    #     'user': user,
    #     'logout_url': users.create_logout_url('/'),
    #     }
    #     newUser = User(parent=root_parent())
    #     newUser.full_name = self.request.get('name')
    #     newUser.id = user.user_id()
    #     newUser.languages_spoken = self.request.get('spoken')
    #     newUser.languages_to_learn = self.request.get('learn')
    #     newUser.timeSent = str(datetime.datetime.now())
    #     newUser.put()
    #
    #     self.redirect('/settings')

class SearchPage(webapp2.RequestHandler):
    def get(self): #for a get request
        user = users.get_current_user()
        self.response.headers['Content-Type'] = 'text/html'
        queryName = self.request.get('val')
        listofusers = User.query(ndb.OR(queryName == User.full_name, queryName == User.languages_spoken)).fetch()
        actuallistofusers = []
        currentuser = User.query(User.id == user.user_id()).fetch()[0]
        for x in listofusers:
            if x.id != user.user_id() and x.languages_to_learn == currentuser.languages_spoken:
                if x.id not in currentuser.friends:
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

        me = User.query(User.id == user.user_id()).fetch()[0]
        listoffriends = []
        if len(me.friends) >0:
            for x in me.friends:
                listoffriends.append(User.query(User.id == x).fetch()[0])
        values ={
        'user': user,
        'logout_url': users.create_logout_url('/'),
        'listoffriends' :listoffriends
        }
        self.response.write(index_template.render(values))

class AjaxGetMessages(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        myId = user.user_id()
        otherUser = self.request.get('id')
        data = {
            'messages': allToDict(Message.query(ndb.OR(ndb.AND(Message.sentFrom == user.user_id(), Message.sentTo == otherUser),
                   ndb.AND(Message.sentTo == user.user_id(), Message.sentFrom == otherUser)), ancestor=root_parent()).order(Message.timeSent, Message.msg).fetch()),
            'myId': myId
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
