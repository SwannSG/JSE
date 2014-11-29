#!/usr/bin/python
"""
    DailyJSE data
    Get daily prices and append to Yahoo formated files
    CSV file per symbol in Yahoo format
        Date,Open,High,Low,Close,Volume,Adj Close
    Directory structure
        ./csv
            /industry
                *-id.csv
                *-sym.csv
            /prices
                <symbol>.csv
            /sector
                *-id.csv
                *-sym.csv
        ./pickle
            instruments.pkl            
"""

import config
import csv
import JSEutils
import logger
import os
import pickle
import sys
import utils01

def add_daily_price(instrument, d1, d2, folder):
    print instrument.split('|')[0]
    date = utils01.jsonToYahooDate(d1['AsAtDateTime'][1:-1])
    filename = '%s/%s.csv' % (folder, instrument.split('|')[0])
    #--check if file actually exists
    if os.path.exists(filename):
        #--file exists
        fp = open(filename, 'r')
    else:
        #--create file
        fp = open(filename, 'w')
        writer = csv.writer(fp)
        writer.writerow( ('Date',
                          'Open',
                          'High',
                          'Low',
                          'Close',
                          'Volume',
                          'Adj Close') )
        fp.close()
        fp = open(filename, 'r')
    if date in fp.read():
        #--date already in file, do nothing
        fp.close()
        return False
    fp = open(filename, 'a')
    writer = csv.writer(fp)
    writer.writerow((date,
                    '',
                    float(d2['DailyHigh']),
                    float(d2['DailyLow']),
                    float(d1['ClosingPrice']),
                    float(d1['Volume']),
                    ''))
    fp.close()
    return True



os.chdir(config.APP_DIR)
log = logger.logger(name = sys.argv[0])
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
#--loads all equities from local store
instruments = pickle.load(open(config.PICKLE_DIR + '/' + config.INSTRUMENTS, 'rb'))
for instrument in instruments:
    rsp = JSEutils.get_pricing_information(instrument.split('|')[3], headers, cookies)
    if not rsp.ok:
        #--report error but don't quit
        log.error('Response error %s' % rsp.status_code) 
        log.error('Request %s: ' % rsp.url)
    else:
        d1 = rsp.json()
        rsp = JSEutils.get_daily_highs_and_lows(instrument.split('|')[3], headers, cookies)
        if not rsp.ok:
            #--report error but don't quit
            log.error('Response error %s' % rsp.status_code) 
            log.error('Request %s: ' % rsp.url)
            #!!!do some error handling
        else:
            d2 = rsp.json()
            add_daily_price(instrument,
                            d1['GetPricingInformationResult'],
                            d2['GetDailyHighsAndLowsResult'],
                            config.PRICES_DIR)

log.info('App ended')

