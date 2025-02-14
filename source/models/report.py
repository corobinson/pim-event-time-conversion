from typing import List
from pandas import DataFrame, Series
from datetime import datetime as dt
from pytz import utc
from pathlib import Path
from source.models.report_entry import ReportEntry
from source.utils import utils

class Report:
    def __init__(self, columns:List[str]=['ID', 'Stibo UTC', 'Converted Event UTC', 'Stibo Matches Converted', 'Event Date', 'Event Time', 'Property Timezone'], 
                 report_datetime_format:str='%Y-%m-%dT%H:%M:%SZ'):
        self.data:DataFrame = DataFrame(columns=columns)
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
        except OSError:
            print(f'Unable to convert date ({event_date}) or time ({event_time}) value to datetime object.')
            
            return ReportEntry(id, 
                               event_tz, 
                               'Unable to convert', 
                               event_date, 
                               event_time, 
                               property_tz, 
                               stibo_matches_converted=False)

        converted_utc_event_datetime = tz_event_datetime.astimezone(utc)
        origin_utc_event_datetime = utc.localize(dt.strptime(event_tz, self.report_datetime_format))
        
        converted_utc_str = dt.strftime(converted_utc_event_datetime, self.report_datetime_format)
        stibo_utc_matches_converted = converted_utc_event_datetime == origin_utc_event_datetime
       
        return ReportEntry(id, 
                            event_tz, 
                            converted_utc_str, 
                            stibo_utc_matches_converted,
                            event_date, 
                            event_time, 
                            property_tz)
        
    def add_new_entry(self, entry:ReportEntry):
        new_row_index = self.data.size + 1
        self.data.loc[new_row_index] = entry.as_dict()
    
    def to_excel_file(self, file_location:str='/data_files/output/', file_name:str='stibo_utc_validated'):
        project_root = str(Path(__file__).parent.parent.parent)
        now = dt.now()
        now_str = dt.strftime(now, '%Y-%m-%dT%H-%M')
        output_file_dir = file_location + file_name + now_str + '.xlsx'
        report_file_path = Path(project_root + output_file_dir)
        self.data.to_excel(report_file_path)