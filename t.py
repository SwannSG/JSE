# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import csv
import datetime
import numpy as np

# Own imports
import os
import config

def date(string):
    # string = ccyymmdd
    return datetime.datetime(int(string[0:4]),
                             int(string[4:6]),
                             int(string[6:])) 

def date_range(folder):
    # set dates in qsdateutil.GTS_DATES
    # we can make this read from a pre-configured file
    symbols = ['SOL'] 
    dates = dict()
    for symbol in symbols:
        filename = folder + '/' + symbol + '.csv'
        fp = open(filename, 'r')
        reader = csv.reader(fp)
        reader.next()
        for row in reader:
            if not dates.has_key(row[0]):
                dates[row[0]]=True
        fp.close()
    date_keys = dates.keys()
    date_keys.sort()
    dates = list()
    for each in date_keys:
        dates.append(du.dt.datetime.strptime(each, "%Y-%m-%d")) 
    return du.pd.TimeSeries(index=dates, data=dates)


#--Non-intrusive (I hope) adaptations ************************
#--set environment
os.environ['QSDATA'] = '/home/steve/pythonApp/jse/csv/prices'
os.environ['QSSCRATCH'] = '/tmp/QSScratch'
#--overide GTS_DATES with JSE dates
du.GTS_DATES = date_range(os.environ['QSDATA'])
#--allow another function name
du.getJSEdays = du.getNYSEdays
#--***********************************************************

c_dataobj = da.DataAccess('Yahoo')
start_date = date('20141001')
end_date = date('20141020')
timeofday = datetime.timedelta(hours=16)






