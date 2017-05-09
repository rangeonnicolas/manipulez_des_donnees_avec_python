## todo: enlever du code précédent les constantes MAX_REPORTS et MAX_DISPLAY, qui ne sont plus utilisées ici

MAX_RESULTS = 10  # Maximum number of search results to display

def select_reports(filename, regexp = "", date_boundaries = None):
    
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
                
    for report in parts:
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
                yield report.group()        
        else:
            yield report.group()
            
       
def search(data_file, last_n_days = None, end_date = None, regexp = None):
    
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
    
    selected_reports = select_reports(path_to_file, regexp, date_boundaries = [start_date, end_date])
    
    if regexp is not None:
        cpt = 0
        for report_as_str in selected_reports:
            report = etree.XML(report_as_str)
            
            cpt = search_regexp_in_report(report, regexp, cpt)
            if cpt >= MAX_RESULTS:
                break
            
def search_regexp_in_report(report, regexp, cpt):

    # A report should always have 2 children:
    # - a 'MetaDonnees' tag
    # - a 'Contenu' tag
    # In case it would contain more than these 2 children, we collect these
    # other parts in the list *other_parts (which will normally always be an empty list)
    metadata, content, *other_parts = report ## todo: ici il y a du unpacking, avec une étoile en plus :p

    # iteration over all the descendants of content:
    # children, grand-children, great grandchildren, etc.
    for elem in content.iter():
        if elem.tag == "paragraphe":                
            speakers, text, *other_parts = elem
                    
            for t in text.itertext():
                search_regexp = re.finditer(regexp, t)
                try:
                    found = next(search_regexp)
                    cpt += 1
                except StopIteration:
                    continue

                print_speakers(speakers)
                print_text(found, t)
                                
                if cpt >= MAX_RESULTS:
                    return cpt
    return cpt


def print_speakers(speakers):

    print("-" *100)
    speakers_names = [spkr.find("NOM").text for spkr in speakers if spkr.find("NOM") is not None]
    spkr_str = "Speaker(s) : " + ', '.join(speakers_names)
    print(spkr_str)
    print()
    
def print_text(found, t):
                
    fnd = found.group()
    location = t.index(fnd)
    from_loc = max(0,location-200)
    to_loc = min(location+len(fnd)+200 , len(t))
    print(t[from_loc : to_loc])
            
