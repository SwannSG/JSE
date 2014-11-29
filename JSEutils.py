"""
    JSE REST API calls
"""

import requests as rq
import pickle
import csv
import utils01

def base_rq():
    #--current companies
    return rq.request('GET',
                      'https://www.jse.co.za/current-companies/companies-and-financial-instruments')

def request_header():
    return {'Content-Type': 'application/json',
            'Host': 'www.jse.co.za',
            'Origin': 'https://www.jse.co.za',
            'Referer': 'https://www.jse.co.za/current-companies/companies-and-financial-instruments'}
    
def cookies(rsp):
    return {'SearchSession': rsp.cookies.get('SearchSession'),
            'TS3ca655': rsp.cookies.get('TS3ca655'),
            '_ga': rsp.cookies.get('_ga'),
            'WSS_FullScreenMode': rsp.cookies.get('WSS_FullScreenMode')}
    
def get_all_issuers(headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/CustomerRoleService.svc/GetAllIssuers',
                      headers=headers,
                      cookies=cookies,
                      data='{"filterLongName":"","filterType":"Equity Issuer"}')

def get_company_profile_information(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SharesService.svc/GetCompanyProfileInformation',
                      headers=headers,
                      cookies=cookies,
                      data='{"instrumentMasterId":"%s"}' % masterID)
    
def get_pricing_information(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SharesService.svc/GetPricingInformation',
                      headers=headers,
                      cookies=cookies,
                      data='{"instrumentMasterId":"%s"}' % masterID)
    
def get_daily_highs_and_lows(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SharesService.svc/GetDailyHighsAndLows',
                      headers=headers,
                      cookies=cookies,
                      data='{"instrumentMasterId":"%s"}' % masterID)

def get_dividend_information(masterID, headers, cookies):
    print '{"instrumentMasterId":"%s"}' % masterID
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/McGregorService.svc/GetDividendInformation',
                      headers=headers,
                      cookies=cookies,
                      data='{"instrumentMasterId":"%s"}' % masterID)

def get_sector_peers(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SharesService.svc/GetSectorPeers',
                      headers=headers,
                      cookies=cookies,
                      data='{"instrumentMasterId":"%s"}' % masterID)

def get_one_year(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SharesService.svc/GetOneYear',
                      headers=headers,
                      cookies=cookies,
                      data='{"masterId":"%s"}' % masterID)

def get_announcements_by_instrument_masterid(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SENSService.svc/GetSensAnnouncementsByInstrumentMasterId',
                      headers=headers,
                      cookies=cookies,
                      data='{"instrumentMasterId":"%s"}' % masterID)

def get_issuer(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/CustomerRoleService.svc/GetIssuer',
                      headers=headers,
                      cookies=cookies,
                      data='{"issuerMasterId":"%s"}' % masterID)
    
def get_issuer_nature_of_business(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/CustomerRoleService.svc/GetIssuerNatureOfBusiness',
                      headers=headers,
                      cookies=cookies,
                      data='{"issuerMasterId":"%s"}' % masterID)

def get_issuer_associated_roles(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/CustomerRoleService.svc/GetIssuerAssociatedRoles',
                      headers=headers,
                      cookies=cookies,
                      data='{"issuerMasterId":"%s"}' % masterID)

def get_all_instruments_for_issuer(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SharesService.svc/GetAllInstrumentsForIssuer',
                      headers=headers,
                      cookies=cookies,
                      data='{"issuerMasterId":"%s"}' % masterID)

def get_all_announcements_by_issuer_masterid(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/SENSService.svc/GetSensAnnouncementsByIssuerMasterId',
                      headers=headers,
                      cookies=cookies,
                      data='{"issuerMasterId":"%s"}' % masterID)

def get_webstir_document_years_by_issuer_masterid(masterID, headers, cookies):
    return rq.request(method='POST',
                      url='https://www.jse.co.za/_vti_bin/JSE/WebstirService.svc/GetWebstirDocumentYearsByIssuerMasterId',
                      headers=headers,
                      cookies=cookies,
                      data='{"issuerMasterId":"%s"}' % masterID)

def get_masterid(s):
    return s.split('|')[2]

def issuers(d):
    """
        pass json object
        returns list of issuers    
    """
    issuers = list()
    for issuer in d:
        if issuer['Status'] == 'Current':
            issuers.append('%s|%s|%s|%s' % (issuer['AlphaCode'],
                                            issuer['CustomerAlphaCode'],
                                            issuer['MasterID'],
                                            issuer['LongName']))
    return issuers


def write_instruments(instruments, fp):
    writer = csv.writer(fp)
    writer.writerow(('AlphaCode', 'Industry', 'InstrumentType',
                    'MasterID', 'Sector', 'ShortName'))
    for instrument in instruments:
        writer.writerow(instrument.split('|'))
    fp.close()


