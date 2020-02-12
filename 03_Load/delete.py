import csv
import json
import requests
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

print("Reading datasets from: %s"%args.inputfile)

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = args.outputdirectory + orgNummer + "_datasets_transformed.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # PUT THE CORRECT URL IN HERE:
            host = 'https://9200-dot-9383651-dot-devshell.appspot.com/'
            if len(host) == 0:
                sys.exit('You must provide the url to the server!')
            headers = {'Content-Type': 'application/json'}
            # PUT THE COOKIE NAME:VALUE IN HERE
            cookieName = 'devshell-proxy-session'
            cookieValue = '710e58c90b795dd2f52eba6a3f3d503e369274c9bcdf710a00f291938cf4d833'
            if len(cookieValue) == 0:
                sys.exit('You must provide the cookieValue!')
            cookies={cookieName:cookieValue}
            print("Deleting the following data from dataset index:\n", data)
            # Load the publisher by posting the data:
            for dataset in data:
                url = host + "/dcat_v3/dataset/" + dataset["doc"]["id"]
                print("Deleting from the following url: ", url)
                r = requests.delete(url, cookies=cookies, json=dataset, headers=headers)
                print ("Deleted " + dataset["doc"]["id"] + ": " + str(r.status_code))
