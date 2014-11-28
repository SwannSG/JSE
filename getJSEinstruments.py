"""
    Download latest instruments from JSE
        Issuers
            Issuer[Instruments ....}
        Instrument is the actual share
"""

import config
import csv
import JSEutils
import logger
import os
import pickle
import sys
import utils01

def get_instruments(d):
    """
        pass json object
        returns list of instruments
    """
    l = list()
    instruments = d['GetAllInstrumentsForIssuerResult']
    for instrument in instruments:
        if instrument['Status'].upper() == 'CURRENT':
            l.append('%s|%s|%s|%s|%s|%s|' % (instrument['AlphaCode'],
                                             instrument['Industry'],
                                             instrument['InstrumentType'],
                                             instrument['MasterID'],
                                             instrument['Sector'],
                                             instrument['ShortName']))
    return l


log = logger.logger(name = sys.argv[0])
os.chdir(config.APP_DIR)
log.info('App started') 

rsp = JSEutils.base_rq()
if not rsp.ok:
    #--report error and quit
    log.error('Response error %s' % rsp.status_code) 
    log.error('Request %s: ' % rsp.url)
    log.error('App ended')
    quit()

#--build request header
headers = JSEutils.request_header()
cookies = JSEutils.cookies(rsp)

print 'Get all issuers'
rsp = JSEutils.get_all_issuers(headers, cookies)
if not rsp.ok:
    #--report error and quit
    log.error('Response error %s' % rsp.status_code) 
    log.error('Request %s: ' % rsp.url)
    log.error('App ended')
    quit()

issuers = JSEutils.issuers(rsp.json())    

print 'Get all instruments for each issuer'
instruments = list()
for issuer in issuers:
    rsp = JSEutils.get_all_instruments_for_issuer(JSEutils.get_masterid(issuer),
                                                  headers,
                                                  cookies)
    if not rsp.ok:
        #--report error but don't quit
        log.error('Response error %s' % rsp.status_code) 
        log.error('Request %s: ' % rsp.url)
    else:        
        instruments.extend(get_instruments(rsp.json()))

try:
    old_instruments = pickle.load(open(config.PICKLE_DIR + '/' + config.INSTRUMENTS, 'rb'))
except:
    log.warn(config.PICKLE_DIR + '/' + config.INSTRUMENTS + ' file not found')
    old_instruments = []
#--compare old and new instruments
if set(old_instruments) <> set(instruments):
    #--archive old version
    print 'old_instruments <> instruments'
    log.info("Previous 'instruments' archived")
    #--rename file
    old = config.PICKLE_DIR + '/' + config.INSTRUMENTS
    new = '%s/%s%s' % (config.PICKLE_DIR,
                       utils01.datetime.datetime.now().strftime("%Y%m%d%H%M%S"),
                       config.INSTRUMENTS)
    os.renames(old, new)
    #--dump updated instruments
    pickle.dump(instruments, open(config.PICKLE_DIR + '/' + config.INSTRUMENTS, 'wb'))
log.info('App ended')
