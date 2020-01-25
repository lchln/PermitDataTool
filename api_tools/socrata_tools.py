""" API GETTER FOR PERMIT DATA"""

import json
import pandas as pd
from sodapy import Socrata

from api_tools import constants


class DFTools:
    """DOG STRING"""
    def refresh_data(self, old_data):
        """ Loads old data from file, gets new data from date onwards"""
        max_date = old_data['Date'].max()
        print('Last New Permit in dataset: ', max_date)

        count_before = old_data.shape[0]
        old_data = old_data[old_data['Date'] < max_date]
        count_after = old_data.shape[0]

        new_data = self.get_data(max_date, True)

        print(abs(count_before - count_after - new_data.shape[0]),
              'new permits')

        new_data = new_data.append(old_data)

        return new_data

    def get_data(self, from_date, refresh):
        """ gets data from from_date onwards"""
        client = Socrata(constants.OD_PORTAL,
                         None,
                         username=constants.OD_API_KEY,
                         password=constants.OD_API_SKEY)
        if from_date is None:
            from_date = '1900-01-01T00:00:00'

        if refresh:
            od_limit = constants.OD_LIMIT_REFRESH
        else:
            od_limit = constants.OD_LIMIT_GET

        results = client.get(constants.OD_KEY,
                             select=', '.join(constants.TARGET_COLS.keys()),
                             permitclassmapped=constants.PCM_ARG,
                             workclassmapped=constants.WCM_ARG,
                             permittype=constants.PT_ARG,
                             order=constants.ORDER_ARG,
                             limit=od_limit)
        results_df = pd.DataFrame.from_records(results)

        # Remove the 'wrong kind' or permits.
        type_filter = results_df['permitclassgroup'].isin(constants.PCG_ARGS)
        results_df = results_df[type_filter]

        results_df['applieddate'] = pd.to_datetime(results_df['applieddate'])
        date_filter = results_df['applieddate'].ge(from_date)
        results_df = results_df[date_filter]

        results_df = results_df.sort_values('applieddate',
                                            axis=0,
                                            ascending=False)

        renamed_df = self.rename_rows(results_df)
        renamed_df = renamed_df.dropna(subset=['Builder'])

        return renamed_df

    @staticmethod
    def rename_rows(input_df):
        """ Renames all rows based on key"""
        renamed_df = input_df
        for k in input_df.columns:
            if k not in list(constants.TARGET_COLS.keys()):
                renamed_df = renamed_df.drop(k, axis=1)
            else:
                renamed_df = renamed_df.rename(
                    columns={k: constants.TARGET_COLS[k]})

        return renamed_df

    def clean_addresses(self, input_df):
        """ 3 new columns: house no., street"""
        split_address_l = input_df['Address'].str.split(' ', n=1)
        house_no = []
        street = []
        for l in split_address_l:
            try:
                house_no.append(l[0])
                street.append(l[1])
            except:
                house_no.append('NaN')
                street.append('NaN')
        input_df['House Number'] = house_no
        input_df['Street'] = street
        print(input_df)

    def reclass_builders(self, input_df):
        reclass_df = self.csv_open(constants.BUILDER_RECLASS_PATH)
        input_df['Builder Reclass'] = input_df['Builder'].map(
            reclass_df.set_index('Builder')['Builder Reclass'].to_dict())

        input_df_nan = input_df[pd.isna(input_df['Builder Reclass'])]
        print(
            input_df_nan.shape[0], 'Builders are currently unclassified..' +
            ' setting them to Smaller Builder')
        self.jsave(input_df_nan[['Builder']], constants.TOCLASS_BUILDER_PATH)

        input_df['Builder Reclass'] = input_df['Builder Reclass'].fillna(
            'Smaller Builder')

        return input_df

    def jprint(self, obj):
        """ Prints JSON"""
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def jsave(self, dataframe, file_name):
        """Exports JSON to CSV"""
        dataframe.to_csv(file_name, header=True, index=False)

    def csv_open(self, path):
        """Opens Path using pandas"""
        return pd.read_csv(path)
