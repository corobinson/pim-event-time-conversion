from typing import List
from pandas import DataFrame, Series, ExcelWriter
from datetime import datetime as dt
from pytz import utc
from pathlib import Path
from source.models.report_entry import ReportEntry
from source.utils import utils

import traceback

class Report:
    def __init__(self, valid_sheet_columns:List[str]=['ID', 'Stibo UTC', 'Converted Event UTC', 'Stibo Matches Converted', 'Event Date', 'Event Time', 'Property Timezone'], 
                 valid_data_sheet_name='Validated Data',
                 invalid_sheet_columns:List[str]=['ID', 'Stibo UTC', 'Converted Event UTC', 'Stibo Matches Converted', 'Event Date', 'Event Time', 'Property Timezone'],
                 invalid_data_sheet_name='Unable to Process',
                 report_datetime_format:str='%Y-%m-%dT%H:%MZ'):
        self.valid_data:DataFrame = DataFrame(columns=valid_sheet_columns)
        self.valid_data_sheet_name = valid_data_sheet_name
        self.invalid_data:DataFrame = DataFrame(columns=invalid_sheet_columns)
        self.invalid_data_sheet_name = invalid_data_sheet_name
        self.report_datetime_format:str = report_datetime_format
        
    def parse_row_data(self, row_data: Series) -> ReportEntry:
        
        id = row_data['<ID>']
        event_date = row_data['Event Date']
        event_time = row_data['Event Time']
        event_tz = row_data['EventTz']
        property_tz = row_data['Timezone']
        converted_timezone = utils.translate_timezone(property_tz)
        
        try:
            event_datetime = dt.strptime(event_date + " " + event_time, "%Y-%m-%d %H:%M:%S")
            tz_event_datetime = converted_timezone.localize(event_datetime)
            origin_utc_event_datetime = utc.localize(dt.strptime(event_tz, self.report_datetime_format))
            
        except Exception as e:
            print('***********************************')
            print(f'Unable to convert date, time, or timezone value to datetime object for Event ID: {id}.')
            print('***********************************')
            traceback.print_exc()
            return ReportEntry(id=id, 
                               stibo_utc=event_tz, 
                               converted_event_utc='Unable to convert', 
                               event_date=event_date, 
                               event_time=event_time, 
                               property_tz=property_tz, 
                               stibo_matches_converted=False,
                               is_data_valid=False)

        converted_utc_event_datetime = tz_event_datetime.astimezone(utc)        
        converted_utc_str = dt.strftime(converted_utc_event_datetime, self.report_datetime_format)
        stibo_utc_matches_converted = converted_utc_event_datetime == origin_utc_event_datetime
       
        return ReportEntry(id=id, 
                            stibo_utc=event_tz, 
                            converted_event_utc=converted_utc_str, 
                            stibo_matches_converted=stibo_utc_matches_converted,
                            event_date=event_date, 
                            event_time=event_time, 
                            property_tz=property_tz,
                            is_data_valid=True)
        
    def add_new_entry(self, entry:ReportEntry):
        if entry.is_data_valid:
            new_row_index = self.valid_data.size + 1
            self.valid_data.loc[new_row_index] = entry.as_dict()
        else:
            new_row_index = self.invalid_data.size + 1
            self.invalid_data.loc[new_row_index] = entry.as_dict()
    
    def to_excel_file(self, file_location:str='/data_files/output/', file_name:str='stibo_utc_validated'):
        project_root = str(Path(__file__).parent.parent.parent)
        now = dt.now()
        now_str = dt.strftime(now, '%Y-%m-%dT%H-%M')
        output_file_dir = file_location + file_name + now_str + '.xlsx'
        report_file_path = Path(project_root + output_file_dir)
        with ExcelWriter(report_file_path, mode='w', engine='openpyxl') as writer:
            self.valid_data.to_excel(writer, sheet_name=self.valid_data_sheet_name, index=False)
        with ExcelWriter(report_file_path, mode='a', engine='openpyxl') as writer:
            self.invalid_data.to_excel(writer, sheet_name=self.invalid_data_sheet_name, index=False)