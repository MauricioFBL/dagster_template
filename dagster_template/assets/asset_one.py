from dagster import asset, AssetIn, define_asset_job
import pandas as pd
import pygsheets
import requests
import json

@asset(description='Pull inflation data from Bureau of Labor Statistics',
    op_tags={"Who": "Luis"})
def get_dataframe() -> pd.DataFrame:

    headers = {"Content-type": "application/json"}
    data = json.dumps({"seriesid": ["CUUR0000SA0"], "startyear": "2017", "endyear": "2022"})
    p = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", data=data, headers=headers)

    json_data = json.loads(p.text)
    df = pd.DataFrame.from_dict(json_data["Results"]["series"][0]["data"])
    df = df.astype({
        "year": 'int32',
        "period": 'string',
        "periodName": 'string',
        "value":'float'
        })

    if 'footnotes' in df.columns:
        df.drop(columns=['footnotes'], axis=1, inplace=True)
    print(df.head())
    return df

@asset(description='Save Data in google Sheets')
def save_gsheet(context, get_dataframe):
    gc = pygsheets.authorize(service_account_file='dagster-modelos-drive.json')
    sheet_drive = gc.open('Inflacion BLS Dagster')
    wks = sheet_drive[0]
    wks.clear()
    wks.title = "My Data"
    wks.set_dataframe(get_dataframe, (1, 1))
    context.add_output_metadata({"row_count": len(get_dataframe)})

@asset
def save_local_csv(context, get_dataframe):
    get_dataframe.to_csv('prueba_local.csv')
    context.add_output_metadata({"row_count_local": len(get_dataframe)})


all_assets_job = define_asset_job(name= "all_assets_job", selection= "save_local_csv")
asset2_job = define_asset_job(name="asset2_job", selection=["get_dataframe", "save_gsheet"])

