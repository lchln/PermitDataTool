""" API GETTER FOR PERMIT DATA"""

import sys

from api_tools import constants
from api_tools import socrata_tools


def main(mode_select):
    """main function"""
    soc_tools = socrata_tools.DFTools()

    if mode_select == 'get':
        print('Getting new data from', constants.OD_PORTAL, 'to',
              constants.DATAFILE_PATH, '...')
        permit_data = soc_tools.get_data(None, False)
    elif mode_select == 'refresh':
        print('Refreshing', constants.DATAFILE_PATH, '...')
        permit_data = soc_tools.csv_open(constants.DATAFILE_PATH)
        permit_data = soc_tools.refresh_data(permit_data)
    else:
        print('No option selected, refreshing...')
        permit_data = soc_tools.csv_open(constants.DATAFILE_PATH)
        permit_data = soc_tools.refresh_data(permit_data)

    permit_data = soc_tools.reclass_builders(permit_data)

    # Save Data to CSV
    soc_tools.jsave(permit_data, constants.DATAFILE_PATH)


if __name__ == '__main__':
    main(sys.argv[len(sys.argv) - 1])
