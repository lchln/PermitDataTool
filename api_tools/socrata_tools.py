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
        renamed_df.dropna(subset=['Builder'], inplace=True)

        return renamed_df

    @staticmethod
    def rename_rows(df_input):
        """ Renames all rows based on key"""
        df_renamed = df_input
        for k in df_input.columns:
            if k not in list(constants.TARGET_COLS.keys()):
                df_renamed = df_renamed.drop(k, axis=1)
            else:
                df_renamed = df_renamed.rename(
                    columns={k: constants.TARGET_COLS[k]})

        return df_renamed

    def reclass_builders(self, df_input):
        df_reclass = self.csv_open(constants.BUILDER_RECLASS_PATH)
        df_input['Builder Reclass'] = df_input['Builder'].map(
            df_reclass.set_index('Builder')['Builder Reclass'].to_dict())

        df_input_nan = df_input[pd.isna(df_input['Builder Reclass'])]
        self.jsave(df_input_nan[['Builder']], constants.TOCLASS_BUILDER_PATH)

        df_input['Builder Reclass'].fillna('Smaller Builder', inplace=True)

        return df_input

    def jprint(self, obj):
        """ Prints JSON"""
        text = json.dumps(obj, sort_keys=True, indent=4)
        print(text)

    def jsave(self, dataframe, file_name):
        """Exports JSON to CSV"""
        dataframe.to_csv(file_name, index=False)

    def csv_open(self, path):
        """Opens Path using pandas"""
        return pd.read_csv(path)
