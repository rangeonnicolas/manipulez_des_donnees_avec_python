from lxml import etree
import re

DATE_FORMAT_IN_FILE = "%Y%m%d%H%M%S%f"
MAX_REPORTS = 5  # maximum number of reports to read in the XML file
MAX_DISPLAY = 30  # maximum number of element when showing some parts of the XML file

def select_reports(filename, date_boundaries = None):
    
    with open(filename,"r") as f:
        text = f.read()
        
        if date_boundaries is None:
            # We assume here that there is not any nested tags both of type 'CompteRendu'
            parts = re.finditer('<CompteRendu.*?>.*?</CompteRendu>', text) 
        else:
            start, end = date_boundaries 
            # We assume here that there is not any nested tags both of type 'CompteRendu'
            # We also assume the same for the 'DateSeance' tag.
            parts = re.finditer('<CompteRendu.*?>.*?<DateSeance.*?>\s*?(\d{17})\s*?</DateSeance>.*?</CompteRendu>', text)
            
        reports = []
        for i in range(MAX_REPORTS):
            reports += [next(parts)]
            
        selected_reports = []
            
        for report in reports:
            if date_boundaries is not None:
                # parts.group(1) gets the value catched in the first 
                # parenthesis group of the regular expression
                date_as_str = report.group(1) 
                
                try:
                    date = dt.datetime.strptime(date_as_str + "000", DATE_FORMAT_IN_FILE) # we add "000" to fit format %Y%m%d%H%M%S%f
                except ValueError:
                    print("""Be carreful: the date '%s' found in the XML file doesn't fit to 
                    format %s. This report will be ignored."""%(date_as_str, DATE_FORMAT_IN_FILE))
                    continue
                    
                if date > start and date < end:
                    # report.group() gets the whole matched regular expression
                    selected_reports += [report.group()]
                    
            else:
                selected_reports += [report.group()] 
                
        return selected_reports
            
       
def search(data_file, last_n_days = None, end_date = None):
    
    if end_date is None:
        end_date = dt.datetime.now()
    else:
        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
        
    if last_n_days is None:
        start_date = dt.datetime(1900,12,31) # A very old date!
    else:
        last_n_days = int(last_n_days) # last_n_days was still a string, passed by the command line
        start_date = end_date - dt.timedelta(last_n_days)
    
    path_to_file = os.path.join("data", data_file)
    
    selected_reports = select_reports(path_to_file, date_boundaries = [start_date, end_date])
    
    for report_as_str in selected_reports:
        report = etree.XML(report_as_str)
        
        # A report should always have 2 children:
        # - a 'MetaDonnees' tag
        # - a 'Contenu' tag
        # In case it would contain more than these 2 children, we collect these
        # other parts in the list *other_parts (which will normally always be an empty list)
        metadata, content, *other_parts = report ## todo: ici il y a du unpacking, avec une étoile en plus :p
        
        print("-" * 100)
        print("New report :")
        print()
        for i, text in enumerate(content.itertext()):  ## todo: enumerate a été vue?
            if i < MAX_DISPLAY:
                print(text)