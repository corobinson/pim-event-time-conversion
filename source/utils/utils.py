from pathlib import Path
import pandas as pd
from pandas import DataFrame
from datetime import datetime, tzinfo
import pytz

def read_input_excel_file() -> DataFrame:
    project_root = Path(__file__).parent.parent.parent
    input_file_path = project_root.joinpath('data_files', 'input')
    for file in input_file_path.iterdir():
        if file.is_file():
            return pd.read_excel(file)

def translate_timezone(time_zone_string: str) -> tzinfo:
    if(time_zone_string == "Pacific Time"):
        return pytz.timezone('America/Los_Angeles')
    elif(time_zone_string == "Central Time"):
        return pytz.timezone('America/Chicago')
    elif(time_zone_string == "Eastern Time"):
        return pytz.timezone('America/New_York')
    elif(time_zone_string == 'Alaska Time'):
        return pytz.timezone('US/Alaska')
    elif(time_zone_string == 'Hawaii-Aleutian Time'):
        return pytz.timezone('US/Hawaii')
    elif(time_zone_string == 'Mountain Time'):
        return pytz.timezone('US/Mountain')
    else:
        print(f'Timezone String {time_zone_string} is not mapped. Returning None.')
        return None # To throw an error when the value is used so I know I need to map a new TZ