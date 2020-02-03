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
        data = json.loads('{"query":{"bool":{"must":[{"match":{"publisher.orgPath":"/STAT/972417807/974761076"}}],"must_not":[],"should":[]}},"from":0,"size":10000,"sort":[],"aggs":{}}')
        # PUT THE CORRECT URL IN HERE:
        host = 'https://8888-dot-7801860-dot-devshell.appspot.com/'
        if len(host) == 0:
            sys.exit('You must provide the url to the server!')
        url = host + "ccat_v34/_search"
        headers = {'Content-Type' : 'application/json'}
        # PUT THE COOKIE NAME:VALUE IN HERE
        cookieName = 'devshell-proxy-session'
        cookieValue = 'b9edd3b588b755a9164d7f396d5f5a17d3962d08a6d005c818ae408eccd5dae8'
        if len(cookieValue) == 0:
            sys.exit('You must provide the cookieValue!')
        cookies={cookieName:cookieValue}
        print("Posting to the following url: ", url)
        print("Posting to publisher index the following data:\n", data)
        # Load the publisher by posting the data:
        r = requests.post(url, cookies=cookies, json=data, headers=headers)
        print (orgNummer + ": " + str(r.status_code))
        with open(args.outputdirectory + orgNummer + '_enhetsregisteret.json', 'w', encoding="utf-8") as outfile:
            json.dump(r.json(), outfile, ensure_ascii=False, indent=4)

       # get total number of rows
        print("Total no. of organizations from enhetsregisteret: %d"%(reader.line_num - 1))
