"""Constants!"""
DATA_FOLDER_PATH = 'data/'
DATAFILE_PATH = DATA_FOLDER_PATH + 'calgary_permit_data.csv'
BUILDER_RECLASS_PATH = DATA_FOLDER_PATH + 'builder_reclass.csv'
TOCLASS_BUILDER_PATH = DATA_FOLDER_PATH + 'To Reclass/toclass_builders.csv'

OD_PORTAL = 'data.calgary.ca'
OD_KEY = 'c2es-76ed'
OD_LIMIT_GET = 420000
OD_LIMIT_REFRESH = 1000
OD_API_KEY = '95sjwlpm6fc7foon0dl8gvjy1'
OD_API_SKEY = 'h1na7abklklkvps3fucpv96sntnzdljswoatcesta0ht4lo5g'

TARGET_COLS = {
    'permitnum': 'Permit ID',
    'applieddate': 'Date',
    'permitclass': 'Class',
    'permitclassgroup': 'Class Group',
    'contractorname': 'Builder',
    'housingunits': 'Units',
    'estprojectcost': 'Est. Project Cost',
    'totalsqft': 'Footage',
    'communityname': 'Community',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'originaladdress': 'Address'
}

PCG_ARGS = ['Single Family', 'Two Family']
PCM_ARG = 'Residential'
WCM_ARG = 'New'
PT_ARG = 'Single Construction Permit'
ORDER_ARG = 'applieddate DESC'


COMPASS_LIST = [
    'N',
    'NE',
    'E',
    'SE',
    'S',
    'SW',
    'W',
    'NW'
]
