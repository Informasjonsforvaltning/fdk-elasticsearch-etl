import csv
import requests
import json

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inputfile', help="the path to the input csv-file", required=True)
parser.add_argument('-o', '--outputdirectory', help="the path to the directory of the output files", required=True)
args = parser.parse_args()

print("Reading organizations from: %s"%args.inputfile)
headers={"Accept":"application/json"}

with open(args.inputfile, encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=",")
  # extracting field names through first row
    next(reader, None)
    for row in reader:
        orgNummer = row[0]
        orgName = row[1]
        # PUT THE CORRECT URL IN HERE:
        host = ''
        if len(host) == 0:
            sys.exit('You must provide the url to the server!')
        url = host + "/dcat/publisher/" + orgNummer
        headers = {'Content-Type' : 'application/json'}
        # PUT THE COOKIE NAME:VALUE IN HERE
        cookieName = 'devshell-proxy-session'
        # PUT THE COOKIE VALUE IN HERE:
        cookieValue = ''
        if len(cookieValue) == 0:
            sys.exit('You must provide the cookieValue!')
        cookies={cookieName:cookieValue}
        r = requests.get(url=url, headers=headers)
        print (orgNummer + "/" + orgName + ": Status code " + str(r.status_code))
        with open(args.outputdirectory + orgNummer + '_enhetsregisteret.json', 'w', encoding="utf-8") as outfile:
            json.dump(r.json(), outfile, ensure_ascii=False, indent=4)

    # get total number of rows
    print("Total no. of organizations from enhetsregisteret: %d"%(reader.line_num - 1))
