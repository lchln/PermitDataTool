"""Constants!"""
DATAFILE_PATH = 'calgary_permit_data.csv'

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
    'locationaddresses': 'Address'
}

PCG_ARGS = ['Single Family', 'Two Family']
PCM_ARG = 'Residential'
WCM_ARG = 'New'
PT_ARG = 'Single Construction Permit'
ORDER_ARG = 'applieddate DESC'
