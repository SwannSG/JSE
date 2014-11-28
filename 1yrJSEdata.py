"""
    Download 1 year of JSE data
    CSV file per symbol in Yahoo format
        Date,Open,High,Low,Close,Volume,Adj Close
"""
import pickle
import csv
import JSEutils
import utils01
import logger
import sys
import os
import config

def write_one_year_prices(d, folder):
    """
        pass json object d
            write yahoo price format
            do not duplicate dates
    """
    print d[0]['AlphaCode']
    filename = '%s/%s.csv' % (folder, d[0]['AlphaCode'])
    if os.path.exists(filename):
        dates = dict()
        fp = open(filename, 'r')
        reader = csv.reader(fp)
        reader.next()
        for row in reader:
            dates[row[0]]=True
        fp.close()
        #--append to existing file
        fp = open(filename, 'a')
        writer = csv.writer(fp)
    else:
        #--file does not exist
        dates = dict()
        fp = open(filename, 'w')
        writer = csv.writer(fp)
        writer.writerow( ('Date',
                          'Open',
                          'High',
                          'Low',
                          'Close',
                          'Volume',
                          'Adj Close') )
    for day in d:
        date = utils01.jsonToYahooDate(day['Date'][1:-1])
        if not dates.has_key(date):
            #--new date
            writer.writerow((date
                             , '',
                             '',
                             float(day['Price']),
                             '',
                             '') )
    fp.close()

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
#--load instruments from pickle
instruments = pickle.load(open(config.PICKLE_DIR + '/' + config.INSTRUMENTS,
                               'rb'))

"""
industry_sectors = get_industry_sector(instruments)
write_sectors(industry_sectors, instruments, './csv/sector')
"""

for instrument in instruments:
    rsp = JSEutils.get_one_year(instrument.split('|')[3], headers, cookies)
    if not rsp.ok:
        #--report error but don't quit
        log.error('Response error %s' % rsp.status_code) 
        log.error('Request %s: ' % rsp.url)
    else:
        write_one_year_prices(rsp.json(), config.PRICES_DIR)

log.info('App ended') 
