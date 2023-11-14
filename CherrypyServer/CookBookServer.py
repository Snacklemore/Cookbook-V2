import hashlib
import os, os.path
import cherrypy
#import CherrypyMako
from mako.template import Template
from mako.lookup import TemplateLookup
import psycopg2
import datetime
from ws4py.messaging import TextMessage
from datetime import datetime,date,time,timezone
import bcrypt
import glob
import json
import shutil
from db import connpsql
userDB = "users.db"

#CherrypyMako.setup()
#(root(01)/public | root(01)/templates)
root_dir = os.path.abspath( os.getcwd())
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

from db import adminAuth
#Register API
@cherrypy.expose
class appDatabaseRegister(object):
    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        pass

    def POST(self,passphrase):
       cherrypy.log(passphrase)
       
       if (passphrase == "123"):
        cherrypy.log("true")
        cookie = cherrypy.response.cookie
        cherrypy.session[SESSION_KEY] = cherrypy.request.login = "user"
        return "success"
       if ( passphrase == adminAuth):
        cherrypy.log("true")
        cookie = cherrypy.response.cookie
        cherrypy.session[SESSION_KEY] = cherrypy.request.login = "admin"
        return "success"
       else:
        return "-1"
    def PUT(self):
        return
    def DELETE(self,id):
        print("delete triggerd")
        return
    
#Login API
@cherrypy.expose
class appDatabaseLogin(object):
    @cherrypy.tools.accept(media='text/plain')
    @require()
    def GET(self):
        pass

    def POST(self,username,password):
       pass
    def PUT(self):
        return
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
            
            

            cur1.execute("SELECT name,id FROM pdf_storage ORDER BY name ASC;")
            pdf_names = cur1.fetchall()
            print(pdf_names)
            json_pdf_names = json.dumps(pdf_names)
            cur1.close()
            return json_pdf_names
           
        
       
    
    
    
    
    @require()
    def POST(self,ufile):
        
        pass
       
        
    def PUT(self):
        return
    def DELETE(self,id):
        print("pdf delete trigger")
        cur1 = connpsql.cursor()
        cur1.execute("DELETE FROM pdf_storage WHERE id = %s;", (int(id),))
        connpsql.commit()
        

        return


localDirec = os.path.abspath(os.path.dirname(__file__))

#lookup = TemplateLookup(directories=['/templates'])
class Root(object):
    @cherrypy.expose
    @require()
    def index(self):
        user = cherrypy.request.login
        print(user)
        raise cherrypy.HTTPRedirect("/content")
        
       
    #Require a passphrase, if correct cookie gets authorized
    @cherrypy.expose
    def passphrase(self):
        lookup = TemplateLookup(directories=['E:\\Cookbook V2\\CherrypyServer\\templates'])
        print(lookup.directories)
        template = lookup.get_template('index.mako')


        return template.render()
        
    

    #content delivery from here (eg. the pdf)
    @cherrypy.expose
    @require()
    def content(self):
        #determine user type 
        if (cherrypy.request.login == "admin"):
            lookup = TemplateLookup(directories=['E:\\Cookbook V2\\CherrypyServer\\templates'])

            template = lookup.get_template('content-admin.mako')


            return template.render()
            #deliver admin content page
            pass
        if (cherrypy.request.login == "user"):
            #deliver user content page
            lookup = TemplateLookup(directories=['E:\\Cookbook V2\\CherrypyServer\\templates'])

            template = lookup.get_template('content.mako')


            return template.render()
           
    @cherrypy.expose
    @require()
    def uploadPDF(self,ufile):
        if (cherrypy.request.login == "admin"):
            print("admin post trigger")
            # Either save the file to the directory where server.py is
            # or save the file to a given path:
            # upload_path = '/path/to/project/data/'
            upload_path = os.path.dirname(__file__)

            # Save the file to a predefined filename
            # or use the filename sent by the client:
            upload_filename = ufile.filename
           # upload_filename = 'saved.pdf'

            upload_file = os.path.normpath(
                os.path.join(upload_path, upload_filename))
            size = 0
            with open(upload_file, 'wb') as out:
                while True:
                    data = ufile.file.read(8192)
                    if not data:
                        break
                    out.write(data)
                    size += len(data)
            
            out = '''
                File received.
                Filename: {}
                Length: {}
                Mime-type: {}
                ''' .format(ufile.filename, size, ufile.content_type, data)
            print(out)

            f = open(upload_file,"rb")
            pdf_data = f.read()
            cur = connpsql.cursor()
            vals = [(psycopg2.Binary(pdf_data),ufile.filename)]
            cur.executemany("INSERT INTO pdf_storage (pdf_data,name) VALUES (%s,%s)", vals)
            f.close()
            #absolute path
            move_file(upload_file,"e:\\Cookbook V2\\CherrypyServer\\pdf")
            return out

#move file helper
def move_file(source_path, destination_path):
    try:
        # Check if the source file exists
        if not os.path.exists(source_path):
            print(f"Error: Source file '{source_path}' does not exist.")
            return

        # Check if the destination folder exists, create it if not
        destination_folder = os.path.dirname(destination_path)
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Copy the file
        shutil.copy(source_path, destination_path)
        print(f"File '{source_path}' copied to '{destination_path}' successfully.")

        # Delete the source file
        os.remove(source_path)
        print(f"Source file '{source_path}' deleted.")

    except Exception as e:
        print(f"Error: {e}")

    




        
if __name__ == '__main__':
    
    
   
    

    
    
    
    
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
        
        
}
    
    
    
    webapp = Root()
    webapp.register = appDatabaseRegister()
    webapp.login = appDatabaseLogin()
    webapp.pdf = appDatabasePdf()
   
    
    cherrypy.quickstart(webapp, '/', config=_cp_config)