"""
    utilities specific to instruments.
        instruments :: list
        instrument
            | seperated
            symbol (AlphaCode)
            industry
            instrumentType
            masterID
            sector
            shortName
"""

def getSymbol(instrument):
    return instrument.split('|')[0]

def getIndustry(instrument):
    return instrument.split('|')[1]

def getInstrumentType(instrument):
    return instrument.split('|')[2]

def getMasterID(instrument):
    return instrument.split('|')[3]

def getSector(instrument):
    return instrument.split('|')[4]

def getShortName(instrument):
    return instrument.split('|')[5]

def findMasterID(instruments, symbol):
    indices = [i for i, s in enumerate(instruments) if symbol in s]
    for index in indices:
        if getSymbol(instruments[index]) == symbol:
            return index
    return None
