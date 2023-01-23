from dagster import repository
from assets.asset_one import *

@repository(name='data_gsheets')
def repo_one():
    return [
        get_dataframe, 
        save_gsheet, 
        save_local_csv, 
        all_assets_job, 
        asset2_job
    ]