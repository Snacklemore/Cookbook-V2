import hashlib
import os, os.path
import cherrypy
import CherrypyMako
import datetime
import smtplib
import sqlite3
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from datetime import datetime,date,time,timezone
import bcrypt
import json
import psycopg2
from db import connpsql
userDB = "users.db"

CherrypyMako.setup()
#app needs to start in 01CrowChit\01
#(root(01)/public | root(01)/templates)
root_dir = os.path.abspath( os.getcwd())
#ASSERT EVERY DYNAMIC DATABASE REQUEST!!!!!
SESSION_KEY = '_cp_username'

#implemented https://github.com/cherrypy/tools/blob/master/AuthenticationAndAccessRestrictions
########################################################################################################
########################################################################################################



def check_auth(*args,**kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                # A condition is just a callable that returns true or false
                if not condition():
                    raise cherrypy.HTTPRedirect("/passphrase")
                else: 
                    raise cherrypy.HTTPRedirect("/content")
        else:
            raise cherrypy.HTTPRedirect("/passphrase")
    
cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)
def is_logged_in(*args,**kwargs):
    return

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""
    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f
    return decorate




# Conditions are callables that return True
# if the user fulfills the conditions they define, False otherwise
#
# They can access the current username as cherrypy.request.login
#
# Define those at will however suits the application.

def member_of(groupname):
    def check():
        # replace with actual check if <username> is in <groupname>
        return cherrypy.request.login == 'joe' and groupname == 'admin'
    return check

def name_is(reqd_username):
    return lambda: reqd_username == cherrypy.request.login
    
########################################################################################################  
########################################################################################################        


#Register API
@cherrypy.expose
class appDatabaseRegister(object):
#fetch user data
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        hash = "hash"
        with sqlite3.connect(userDB) as c:
            r = c.execute("""  SELECT 
                        username 
                            FROM 
                        users  
                            WHERE hpassword = ?
            """,[hash]) 
            result = r.fetchone()[0]
        cherrypy.log(result)
        #ASSERT EVERY DYNAMIC DATABASE REQUEST!!!!!
           
        return result


       #Restrict username duplicates!!!
    def POST(self,passphrase):
       cherrypy.log(passphrase)
       
       if (passphrase == "123"):
        cherrypy.log("true")
        cookie = cherrypy.response.cookie
        cherrypy.session[SESSION_KEY] = cherrypy.request.login = cookie
       
        return "success"
       else:
        return "-1"
#(possibly update user data)
    def PUT(self):
        return
#delete user data
    def DELETE(self):
        return
    
#Login API
@cherrypy.expose
class appDatabaseLogin(object):
#fetch user data
    @cherrypy.tools.accept(media='text/plain')
    #GET request to loginDB is the session logout
    @require()
    def GET(self):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY,None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            
           
        return 
#add new userdata

    def POST(self,username,password):
       cherrypy.log(username)
       cherrypy.log(password)
       rusername = username
       #Authenticate 
       ## Fetch hash from username and email
       with sqlite3.connect(userDB) as c:
            r = c.execute(""" SELECT passwordhash FROM users WHERE username=?""",[rusername])
         
       
       try:
            passwordhash = r.fetchall()[0]
            print(passwordhash[0])
       except IndexError as e:
            nouser = "noUserFoundError"
            print(nouser)
            return "denied"
       
       if (bcrypt.checkpw(password.encode('utf-8'),passwordhash[0])):
            cherrypy.log("true")
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username;
            cherrypy.log("User logged in ?",username)
            
            return "success"
            

            
       
      
       
       return "denied"
#(possibly update user data)
    def PUT(self):
        return
#delete user data
    def DELETE(self):
        return
    
    

#Pdf Delivery point
@cherrypy.expose
class appDatabasePdf(object):

    


    @cherrypy.tools.accept(media='text/plain')
    @require()
    def GET(self,type,id):
        if (type == "all"):
            cur1 = connpsql.cursor()
            

            if (int(id) != -1):
                cur1.execute("SELECT pdf_data FROM pdf_storage WHERE id = %s", (int(id),))
                connpsql.commit()

                pdf_data = cur1.fetchone()[0]
                cur1.close
                return pdf_data


            pdf_names =[]
            
            

            cur1.execute("SELECT name,id FROM pdf_storage ORDER BY name ASC")
            pdf_names = cur1.fetchall()
            print(pdf_names)
            json_pdf_names = json.dumps(pdf_names)
            cur1.close()
            return json_pdf_names
            #cur = connpsql.cursor()
            #cur.execute("SELECT pdf_data FROM pdf_storage WHERE id = %s", (1,))
            #pdf_data = cur.fetchone()[0]
            #return pdf_data
        
       
    
    
    
    
    @require()
    def POST(self,username):
        print("username sent::")
        print(username)
        error = "-1"
        #find username in db, return username if found
        with sqlite3.connect(userDB) as c:
            r = c.execute(""" SELECT username FROM users WHERE username=?;""", [username])
        try:
            response = r.fetchone()[0]
        except TypeError as e:
            response = error
        
        #if no username found return -1 or similar error message
       
        return response
    def PUT(self):
        return
    def DELETE(self):
        return


        
 
class Root(object):
    #pull login into seperate uri, redirect directly to chat, and redirect if no login!
    @cherrypy.expose
    @cherrypy.tools.mako(filename='content.mako')
    @require()
    def index(self):
        user = cherrypy.request.login
        print(user)
       
        return """"""
       
    #Require a passphrase, if correct cookie gets authorized
    @cherrypy.expose
    @cherrypy.tools.mako(filename='index.mako')
    def passphrase(self):
        return """"""
    

    #content delivery from here (eg. the pdf)
    @cherrypy.expose
    @cherrypy.tools.mako(filename='content.mako')
    @require()
    def content(self):
        return """"""
    
    
    def mail(self):
       
        return ""
    @cherrypy.expose
    def verify(self,hash,email):
    #ASSERT EMAIL
    #ASSERT HASH
        #fetch database entry via email
        #compare activation hashes
        #activate account if matching
        cherrypy.log(hash)
        cherrypy.log(email)
        return
        


#user applies 
def create_table(conn,str):
    
    c = conn.cursor()
    c.execute(str)
    

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except:
        print("Variable  is not defined")
        
    return conn

def send_email(user, pwd, recipient, subject, body):
    FROM = user
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject
    TEXT = body

       # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
  """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(user, pwd)
            server.sendmail(FROM, TO, message)
            server.close()
            print('successfully sent the mail')
    except:
            print("failed to send mail")
        
        
        
    return
        
if __name__ == '__main__':
    dbconn = create_connection("users.db")
    
   
    

    
    
    
    
    localDir = os.path.abspath(os.path.dirname(__file__))
    print(localDir)
    CA = os.path.join(localDir,'cert1.pem')
    KEY= os.path.join(localDir,'privkey1.pem')
   
    _cp_config={
    'global':{
        'server.socket_host'  : '192.168.178.26',
        'server.socket_port'  : 8080,
        'environment':'production',
        'tools.mako.directories' : [os.path.join(localDir,'templates')],
        'log.screen' : True,
        'log.access_file' : 'logs.txt',
        #'server.ssl_module' : 'pyopenssl',
        #'server.ssl_certificate': CA,
        #'server.ssl_private_key': KEY,
        'tools.sessions.on': True,
        'tools.auth.on': True,
        
        
    },
    
    '/': {'tools.staticdir.root': os.path.abspath(os.getcwd()),
          'tools.response_headers.on': True,
        },
    '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': os.path.join(localDir,'public')
        },
        '/login': {'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
                     'tools.response_headers.on': True,
                      'tools.response_headers.headers': [('Content-Type', 'text/plain')]
                    },
        '/register': {'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
                      'tools.response_headers.on': True,
                      'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        '/pdf': {'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
                      'tools.response_headers.on': True,
                      'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        '/start': {'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
                      'tools.response_headers.on': True,
                      'tools.response_headers.headers': [('Content-Type', 'text/plain')]
        },
        
}
    
    
    
    webapp = Root()
    webapp.register = appDatabaseRegister()
    webapp.login = appDatabaseLogin()
    webapp.pdf = appDatabasePdf()
   
    
    cherrypy.quickstart(webapp, '/', config=_cp_config)