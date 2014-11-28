"""
    Symbols and id for each sector 
"""
import config
import os
import pickle
import utils01

def get_industry_sector(instruments):
    s = set()
    for instrument in instruments:
        inst = instrument.split('|')
        s.add('%s|%s' % (inst[1], inst[4]))              
    return list(s)

def write_sectors(industry_sectors, instruments, folder):
    for ind in industry_sectors:
        print ind
        ind_s = ind.split('|')
        symbols = list()
        masterIDs = list()
        for instrument in instruments:
            inst = instrument.split('|') 
            if inst[1] == ind_s[0] and inst[4] == ind_s[1]:
                symbols.append(inst[0] + '\n')
                masterIDs.append(inst[3] + '\n')
        filename = utils01.POSIX_filename('%s-sym.csv' % ind)
        fp = open('%s/%s' % (folder, filename), 'w')
        fp.writelines(symbols)
        fp.close()
        filename = utils01.POSIX_filename('%s-id.csv' % ind)
        fp = open('%s/%s' % (folder, filename), 'w')
        fp.writelines(masterIDs)
        fp.close()

os.chdir(config.APP_DIR)
#--load instruments from pickle
instruments = pickle.load(open(config.PICKLE_DIR + '/' + config.INSTRUMENTS,
                               'rb'))
industry_sectors = get_industry_sector(instruments)
write_sectors(industry_sectors, instruments, config.SECTOR_DIR)
