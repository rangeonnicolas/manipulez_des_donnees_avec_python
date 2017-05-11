import argparse
import analysis as an
import logging as lg

def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-d","--datafile",help="""CSV file containing pieces of 
        information about the members of parliament""")
    parser.add_argument("-p","--byparty", action='store_false', help="""displays 
        a graph for each political party""")
    
    return parser.parse_args()

def main():
    args = parse_arguments()    
    an.launch_analysis(args.datafile, args.byparty) ##todo: faire du packing/unpacking pour tous ces arguments?
    
if __name__ == '__main__':
    try:
        main()
    except:
        lg.critical('You should use a flag.')
    finally:
        print('------------------ End of analysis -----------------')