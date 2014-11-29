import pickle
import csv
import utils01
import utils02
import JSEutils
import config
import os

os.chdir(config.APP_DIR)
rsp = JSEutils.base_rq()
if not rsp.ok:
    #--report error and quit
    print 'Response error %s' % rsp.status_code 
    print 'Request %s: ' % rsp.url
    #!!!do some error handling and stop program

#--build request header
headers = JSEutils.request_header()
cookies = JSEutils.cookies(rsp)
instruments = pickle.load(open(config.PICKLE_DIR + '/' + config.INSTRUMENTS,
                              'rb'))

index = utils02.findMasterID(instruments, 'SOL')
print instruments[index]
master_id = utils02.getMasterID(instruments[index])

"""
dividends = list()
for instrument in instruments:
    symbol = instrument.split('|')[0]
    print symbol
    master_id = instrument.split('|')[3]
    rsp = JSEutils.get_dividend_information(master_id, headers, cookies)
    if not rsp.ok:
        #--report error but don't quit
        print 'Response error %s' % rsp.status_code 
        print 'Request %s: ' % rsp.url
        #!!!do some error handling
    else:
        dividends.append(rsp.json())

"""
