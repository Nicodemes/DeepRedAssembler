import sys
import json
import rules 
from optparse import OptionParser
# Parsing rules
# segments
parser = OptionParser()
parser.add_option("-i", "--inp","--inpfile","--inputFile",
                  action="store", type="string", dest="inputFile")
parser.add_option("-o", "--out","--outfile","--outputfile",
                  action="store", type="string", dest="outputFile")

(options, args) = parser.parse_args()