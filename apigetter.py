import json
import pandas as pd
from sodapy import Socrata

# od_api = 'https://data.calgary.ca/resource/c2es-76ed.json?WorkClassMapped=New$limit=2000'
od_portal = 'data.calgary.ca'
od_key = 'c2es-76ed'

permit_types = [
    '1106 - Single Family House', '1407 - Two Family Semi-Detached (1 Unit)',
    '1706 - Rhs Rowhouse', '1606 - Ths Townhouse', '1506 - Apt Apartment',
    '1408 - Tfy Semi Detached (2 Unit)'
    '1507 - Apt Triplex', '1508 - Apt Fourplex'
]

od_limit = 2000
pcm_args = 'Residential'
wcm_args = 'New'


def main():
    client = Socrata(od_portal, None)
    results = client.get(od_key,
                         limit=od_limit,
                         permitclassmapped=pcm_args,
                         workclassmapped=wcm_args)

    results_df = pd.DataFrame.from_records(results)

    filtered_df = results_df[results_df.permitclass.isin(permit_types)]

    jsave(filtered_df)


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def jsave(obj):
    obj.to_csv('test.csv', index=False)



if __name__ == '__main__':
    main()
