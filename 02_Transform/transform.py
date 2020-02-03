import csv
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)


def transform(data):
    # Transforming according to rules in README
    array = data["hits"]["hits"]
    print (len(array))
    # TODO Do the actual transformation
    i = 0
    j = 0
    for begrep in array:
        try:
            del begrep["_source"]["validFromIncluding"]
            i = i + 1
        except KeyError:
            pass
        try:
            del begrep["_source"]["validToIncluding"]
            j = j + 1
        except KeyError:
            pass
    print("Deleted validFroms ", i)
    print("Deleted validTos ", j)
    transformed = array
    return transformed

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = args.outputdirectory + orgNummer + "_enhetsregisteret.json.bakcup"
        outputfileName = args.outputdirectory + orgNummer + "_begreper.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # Transform the organization object to publihser format:
            with open(outputfileName, 'w', encoding="utf-8") as outfile:
                json.dump(transform(data), outfile, ensure_ascii=False, indent=4)
