import argparse
import xml_analysis as xml_an
import logging as lg

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d","--datafile",help="""XML file containing the scripts 
        of the debates""")
    parser.add_argument("-l","--lastndays",help="""limits the search to the debates
        dating from less than --lastndays days before today, or before the date 
        specified with --enddate""")
    parser.add_argument("-e","--enddate",help="""limits the search to the debates 
        that occured before --enddate. Please give the date with this format : '%Y-%m-%d' .""")
    parser.add_argument("-r","--regexp",help="""Regular expression to search into the xml file""") #todo: attention, je ne sais pas comment spécifier que cet argument doit être obligatoire
    
    return parser.parse_args()

def main():
    args = parse_arguments()    
    xml_an.search(args.datafile, args.lastndays, args.enddate, args.regexp)
    
if __name__ == '__main__':
    try:
        main()
    except:
        lg.critical('You should use a flag.')
    finally:
        print('------------------ End of analysis -----------------')