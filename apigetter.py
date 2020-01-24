import json
import pandas as pd
from sodapy import Socrata

od_portal = 'data.calgary.ca'
od_key = 'c2es-76ed'

datafile_path = 'test.csv'

# permit_types = [
#     '1106 - Single Family House', '1407 - Two Family Semi-Detached (1 Unit)',
#     '1706 - Rhs Rowhouse', '1606 - Ths Townhouse', '1506 - Apt Apartment',
#     '1408 - Tfy Semi Detached (2 Unit)', '1507 - Apt Triplex',
#     '1508 - Apt Fourplex'
# ]

permit_types = [
    '1106 - Single Family House', '1407 - Two Family Semi-Detached (1 Unit)',
    '1706 - Rhs Rowhouse', '1606 - Ths Townhouse', '1506 - Apt Apartment',
    '1407 - Tfy Semi Detached (1 Unit)'
]

target_cols = {
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

od_limit = 20000
pcm_args = 'Residential'
wcm_args = 'New'


def main():

    # permit_data = get_data()

    permit_data = csv_open(datafile_path)
    permit_data = refresh_data(permit_data)

    jsave(permit_data)


def refresh_data(old_data):
    max_date = old_data['Date'].max()

    old_data = old_data[old_data['Date'] != max_date]

    new_data = get_data(max_date)

    # filtered_df = filtered_df[filtered_df.applieddate.ge(max_date)]

    # filtered_df.append(old_data)

    return old_data


def get_data(from_date):
    client = Socrata(od_portal, None)
    results = client.get(od_key,
                         applieddate >= from_date,
                         limit=od_limit,
                         permitclassmapped=pcm_args,
                         workclassmapped=wcm_args)

    results_df = pd.DataFrame.from_records(results)

    type_filter = results_df['permitclass'].isin(permit_types)

    # filtered_df = results_df[results_df.permitclass.isin(permit_types)]
    results_df = results_df[type_filter]

    results_df['applieddate'] = pd.to_datetime(results_df['applieddate'])

    results_df = results_df.sort_values('applieddate', axis=0, ascending=False)

    renamed_df = rename_rows(results_df)

    return renamed_df


def rename_rows(df):
    df_renamed = df
    for k in df.columns:
        if k not in list(target_cols.keys()):
            df_renamed = df_renamed.drop(k, axis=1)
        else:
            df_renamed = df_renamed.rename(columns={k: target_cols[k]})

    return df_renamed


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def jsave(obj):
    obj.to_csv('test.csv', index=False)


def csv_open(path):
    return pd.read_csv(path)


if __name__ == '__main__':
    main()
