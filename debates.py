import argparse
import analysis as an
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
    
    return parser.parse_args()

def main():
    args = parse_arguments()    
    an.launch_analysis(args.datafile, args.lastndays, args.enddate) ##todo: faire du packing/unpacking pour tous ces arguments?
    
if __name__ == '__main__':
    try:
        main()
    except:
        lg.critical('You should use a flag.')
    finally:
        print('------------------ End of analysis -----------------')