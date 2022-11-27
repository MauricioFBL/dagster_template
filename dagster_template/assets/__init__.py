from dagster import asset
import pandas as pd
import requests
import json

@asset(description='Pull inflation data from Bureau of Labor Statistics')
def get_dataframe() -> pd.DataFrame:
    
    headers = {"Content-type": "application/json"}
    data = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": "2017", "endyear": "2022"})
    p = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", data=data, headers=headers)

    json_data = json.loads(p.text)
    df = pd.DataFrame.from_dict(json_data["Results"]["series"][0]["data"])
    df = df.astype({"year":'int32',"period": 'string',"periodName": 'string',"value":'float'})

    if 'footnotes' in df.columns:
        df.drop(columns=['footnotes'], axis=1, inplace=True)
    print(df.head())
    return df