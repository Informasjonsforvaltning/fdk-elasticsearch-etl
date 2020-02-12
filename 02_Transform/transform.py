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
    newArray = []
    for dataset in array:
        dataset = {"doc" : {"id": dataset["_id"]}}
        newArray.append(dataset)
    transformed = newArray
    return transformed

def filter(data):
    # Ruteplan for sykkel
    array = data["hits"]["hits"]
    print (len(array))
    newArray = []
    total = 0
    tobedeleted = 0
    for dataset in array:
        # print(dataset)
        if dataset["_source"]["uri"][:17] != "https://prod.nora":
            if dataset["_source"]["title"]["nb"] == "Ruteplan for sykkel":
                dataset = {"doc" : {"id": dataset["_id"],"title": dataset["_source"]["title"], "catalog": dataset["_source"]["catalog"]["uri"]}}
                newArray.append(dataset)
                tobedeleted += 1
        total += 1
    transformed = newArray
    print("total: ", total)
    print("tobedeleted: ", tobedeleted)
    return transformed

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = args.outputdirectory + orgNummer + "_datasets.json"
        outputfileName = args.outputdirectory + orgNummer + "_datasets_tobedeleted.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # Transform the organization object to publihser format:
            with open(outputfileName, 'w', encoding="utf-8") as outfile:
                json.dump(filter(data), outfile, ensure_ascii=False, indent=4)
