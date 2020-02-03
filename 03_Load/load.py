import csv
import json
import requests
import sys

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        inputfileName = args.outputdirectory + orgNummer + "_begreper.json"
        with open(inputfileName) as json_file:
            data = json.load(json_file)
            # PUT THE CORRECT URL IN HERE:
            host = 'https://8888-dot-7801860-dot-devshell.appspot.com'
            if len(host) == 0:
                sys.exit('You must provide the url to the server!')
            headers = {'Content-Type' : 'application/json'}
            # PUT THE COOKIE NAME:VALUE IN HERE
            cookieName = 'devshell-proxy-session'
            cookieValue = 'b9edd3b588b755a9164d7f396d5f5a17d3962d08a6d005c818ae408eccd5dae8'
            if len(cookieValue) == 0:
                sys.exit('You must provide the cookieValue!')
            cookies={cookieName:cookieValue}
            print("Posting to publisher index the following data:\n", data)
            # Load the publisher by posting the data:
            for begrep in data:
                url = host + "/ccat_v34/concept/" + begrep["doc"]["id"] + "/_update"
                print("Posting to the following url: ", url)
                r = requests.post(url, cookies=cookies, json=begrep, headers=headers)
                print ("Updated " + begrep["doc"]["id"] + ": " + str(r.status_code))
