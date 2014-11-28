"""
    Symbols and id for each industry 
"""
import config
import os
import pickle

def get_industry(instruments):
    s = set()
    for instrument in instruments:
        inst = instrument.split('|')
        s.add('%s' % (inst[1]))              
    return list(s)

def write_industry(industry, instruments, folder):
    for ind in industry:
        print ind
        symbols = list()
        masterIDs = list()
        for instrument in instruments:
            inst = instrument.split('|') 
            if inst[1] == ind:
                symbols.append(inst[0] + '\n')
                masterIDs.append(inst[3] + '\n')
        fp = open('%s/%s-sym.csv' % (folder, ind), 'w')
        fp.writelines(symbols)
        fp.close()
        fp = open('%s/%s-id.csv' % (folder, ind), 'w')
        fp.writelines(masterIDs)
        fp.close()

os.chdir(config.APP_DIR)
#--load instruments from pickle
instruments = pickle.load(open(config.PICKLE_DIR + '/' + config.INSTRUMENTS,
                               'rb'))
industry = get_industry(instruments)
write_industry(industry, instruments, config.INDUSTRY_DIR)
