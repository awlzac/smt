# handle access to google fusion table.
#
# the table and its realtime updates can be seen at:
# https://www.google.com/fusiontables/DataSource?docid=13sbd2KKAzniR-0rPdP0EMBBPuErYtq0eMErN-UZX
#

from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build
import threading

# these could be supplied in a better way depending on purpose; mindset
# for this test project is that all auth info for fusion tables in the 
# app should come from a consolidated place: this file
tablekey = '13sbd2KKAzniR-0rPdP0EMBBPuErYtq0eMErN-UZX'
apikey = 'AIzaSyDSIhZ7Qe-xH6sW4-U2NexW8fbcGZr9e88'

fusionso = None
lock = threading.Lock()
def query_fusion(sql):
    '''
    access a service object, that we can use for querying fusion.  oauth is 
    a bit of a headache, and access to fusion is slow, and not reentrant,
    but this allows it to happen.  private key file used; obviously 
    in a real app this wouldn't be checked into a public source repo.
    
    in a real app, we might look into ways to thread for performance gain.  
    or better yet, we wouldn't use fusion tables :)
    '''
    global fusionso
    if not fusionso:
        scopes=['https://www.googleapis.com/auth/fusiontables']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
                'smt-messick-166ba8bc6c9d.json', scopes=scopes)
        http_auth = credentials.authorize(Http())
        fusionso = build('fusiontables', 'v2', http=http_auth)
    with lock:
        fusionso.query().sql(sql=sql).execute()

    
def add_to_fusion(addr):
    '''
    add inpassed address as a row in fusion table.
    '''
    query_fusion('INSERT INTO '+tablekey+' (address_desc, lat, lng) VALUES (\'' \
            + addr.desc+'\','+str(addr.lat)+','+str(addr.lng)+')')
       

def trunc_fusion():
    '''
    clear fusion table.
    '''
    query_fusion('DELETE FROM '+tablekey)

