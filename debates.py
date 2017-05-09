def parse_arguments():
    
    if not NOTEBOOK:
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
    
    else: ## todo: A enlever. Ici on triche car ArgumentParser est innutilisable dans un notebook
        class foo:
            pass
        o = foo()
        o.__dict__ = {
            'datafile' : "SyceronBrut.xml",
            'lastndays' : 15,
            'enddate' : "2017-02-01",
            'regexp' : "concitoyen"
        }
        return o
    
if __name__ == '__main__':
    args = parse_arguments()    
    search(args.datafile, args.lastndays, args.enddate, args.regexp)