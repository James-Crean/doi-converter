#! /usr/bin/env python2
import requests
import json
import sys
import getopt

class RefClient(object):
    def __init__(self, accept='application/vnd.citationstyles.csl+json', timout=3):
        self.headers = {'accept': accept}
        self.timeout = timout
        """
        If query is ran by itself without setting a different header
        then the client will use the default header set here.
        """

    def query(self, doi):
        if doi.startswith("http://dx.doi.org/"):
            url = doi

        else:
            url = "http://dx.doi.org/" + doi

        r = requests.get(url, headers =self.headers)

        if DEBUG:
            print("Printing request output:")
            print(r)
            print("--------------------------------")
        return r

    def doi2json(self, doi):
        self.headers['accept'] = 'application/vnd.citationstyles.csl+json'
        return self.query(doi).json()

def main(argv):
    inputfile = ""
    outputfile = ""
    """
    Begin checking command line options
    """
    try:
        opts, args = getopt.getopt(argv, "hi:o:d",["help"])
    except getopt.GetoptError:
        print ("Usage: doi-converter.py -i <inputfile> -o <outputfile> -h -d")
        print ("For help use -h and to enable debug messages use -d")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("Usage: doi-converter.py -i <inputfile> -o <outputfile> -h -d")
            print ("For help use -h and to enable debug messages use -d")
            sys.exit()
        elif opt in ("-i"):
            inputfile = arg
        elif opt in ("-o"):
            outputfile = arg
    if inputfile == "" or outputfile ""
        print("Error: Both input and output files must be specified."
        sys.exit(2)



