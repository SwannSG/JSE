import datetime

def jsonToPyDate(js_date):
    """
        Convert javascript date to python date
        js_date: 'Date(1415138400000+0200)', should return 5 Nov 2014
            timeoffset +0200 = 02 hrs, 00 minites
        JavaScript dates are calculated in milliseconds
        from 01 January, 1970 00:00:00 Universal Time (UTC).
        One day contains 86,400,000 millisecond.
    """ 
    return datetime.datetime(1970, 1, 1,
                      int(js_date[19:21]),
                      int(js_date[21:23])) + \
                      datetime.timedelta(float(js_date[5:18])/86400000) 


def YahooDate(dt):
    """
        Convert python datetime obj to string 'CCYY-MM-DD'    
            This is the Yahoo format
    """
    return dt.strftime('%Y-%m-%d')


def jsonToYahooDate(js_date):
  return YahooDate(jsonToPyDate(js_date))


def POSIX_filename(filename):
    """
        generates a POSIX compliant filename
    """
    #--POSIX compliant chars
    s = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-'
    fn = ''
    for char in filename:
        if s.find(char) > -1:
            #--char found
            fn = '%s%s' % (fn, char)
    return fn





#f = '/home/steve/pythonApp/jse/pickle/instruments.pkl'
#print md5sum(f)
#dt = jsonToPyDate('Date(1415138400000+0200)')
#print dt
#print YahooDate(dt)
#print jsonToYahooDate('Date(1415138400000+0200)')

