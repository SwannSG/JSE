import pickle
import csv
import utils01
import JSEutils

rsp = JSEutils.base_rq()
if not rsp.ok:
    #--report error and quit
    print 'Response error %s' % rsp.status_code 
    print 'Request %s: ' % rsp.url
    #!!!do some error handling and stop program

#--build request header
headers = JSEutils.request_header()
cookies = JSEutils.cookies(rsp)

instruments = pickle.load(open('./pickle/instruments.pkl', 'rb'))
dividends = list()
for instrument in instruments:
    print instrument[0]
    rsp = JSEutils.get_dividend_information(instrument.split('|')[3], headers, cookies)
    if not rsp.ok:
        #--report error but don't quit
        print 'Response error %s' % rsp.status_code 
        print 'Request %s: ' % rsp.url
        #!!!do some error handling
    else:
        dividends.append(rsp.json())

