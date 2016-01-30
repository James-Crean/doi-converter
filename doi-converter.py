import requests
import json
import sys
import getopt
import codecs

class DOIConverter(object):

#additional headers can be found at http://www.crosscite.org/cn/

    def __init__(self, accept='text/x-bibliography; style=apa; locale=en-US', timout=3):
        self.headers = {'accept': accept}
        self.timeout = timout
        """
        If query is ran by itself without setting a different header
        then the client will use the default header set here.
        """

    def query(self, doi):
        if doi[:5].lower() == 'doi: ': #grabs first 5 characters lowercases, and compares
            url = doi.split()[1] #removes "doi:" and whitespace leaving only the doi
        elif doi.startswith("http://dx.doi.org/"):
            url = doi
        else:
            url = "http://dx.doi.org/" + doi
        r = requests.get(url, headers =self.headers)
        if r.status_code == 200:
            return r.content
        elif r.status_code == 204:
            return doi + " -- The request was OK but there was no metadata available.available."
        elif r.status_code == 404:
            return doi + " -- The DOI requested doesn't exist."
        elif r.status_code == 406: #note, this is recoverable. will add later
            return doi + " -- Can't serve any requested content type."
        else:
            return doi + " -- Unknown status code returned (" + r.response_code + ")."

    def doi2apa(self, doi):
        self.headers['accept'] = "text/x-bibliography; style=apa; locale=en-US"
        return self.query(doi)
    def doi2json(self, doi):
        self.headers['accept'] = 'application/vnd.citationstyles.csl+json'
        return self.query(doi).json()

def main(argv):
    inputfile = ""
    outputfile = ""
    converter = DOIConverter()
    #
    #Begin checking command line options
    #
    if len(argv) < 1:
        print ("Usage: doi-converter.py -i <inputfile> -o <outputfile> -h")
        sys.exit()
    try:
        opts, args = getopt.getopt(argv, "hi:o:",["help"])
    except getopt.GetoptError:
        print ("Usage: doi-converter.py -h -d -i <inputfile> -o <outputfile>")
        print ("For help use -h and to enable debug messages use -d")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ("Usage: doi-converter.py -h -d -i <inputfile> -o <outputfile>")
            print ("For help use -h and to enable debug messages use -d")
            sys.exit()
        elif opt == "-i":
            inputfile = arg
        elif opt == "-o":
            outputfile = arg
    if inputfile == "" or outputfile == "":
        print("Error: Both input and output files must be specified.")
        print("Inputfile=" + inputfile + " Outputfile=" + outputfile)
        sys.exit(2)

    #
    #End of command line checking
    #Begin opening files and reading DOIs
    #

    inputfile = open(inputfile, 'r')
    outputfile = codecs.open(outputfile, 'wb', "utf-8")

    #Warning: There should be a check for the output file being read only
    #However, I do not currently know how to check that in python

    for line in inputfile:
        response = converter.doi2apa(line)
        outputfile.write(response.decode('utf-8'))
    inputfile.close()
    outputfile.close()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:]) #no need to include the script name in args


