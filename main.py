from pandas import DataFrame
from source.utils import utils
from source.models.report import Report

data_frames: DataFrame = utils.read_input_excel_file()

report = Report()

for index, row in data_frames.iterrows():
    new_entry = report.parse_row_data(row)
    report.add_new_entry(new_entry)
        
report.to_excel_file()