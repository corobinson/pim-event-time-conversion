class ReportEntry:
    def __init__(self, id:str, 
                 stibo_utc:str, 
                 converted_event_utc:str, 
                 stibo_matches_converted: bool,
                 event_date:str, 
                 event_time:str, 
                 property_tz:str):
        self.id = id
        self.stibo_utc = stibo_utc
        self.converted_event_utc = converted_event_utc
        self.stibo_matches_converted = stibo_matches_converted
        self.event_date = event_date
        self.event_time = event_time
        self.property_tz = property_tz
    
    def as_dict(self):
        return {
            'ID': self.id,
            'Stibo UTC': self.stibo_utc,
            'Converted Event UTC': self.converted_event_utc,
            'Stibo Matches Converted': self.stibo_matches_converted,
            'Event Date': self.event_date,
            'Event Time': self.event_time,
            'Property Timezone': self.property_tz
        }