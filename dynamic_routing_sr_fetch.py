#!/bin/python

import requests
import json
import datetime

data = {
	"transferId" : 123,
	"isRetry": False,
	"transferService": "PG",
	"supportedRoutingSwitches": [
		"yesupi",
		"iciciupi",
		"indusupi",
		"hdfcupi"
	],
	"transactionId":123,
	"paymentCode":7001,
	"merchantId":2887,
	"transferDetails": {
		"mode": "UPI",
		"paymentCode": 7001,
		"bankName": ""
	},
	"pg1": "YESUPI",
	"pg2": "iciciupi",
	"paymentCode": 7001,
	"paymentMode": "UPI"
}
url = "https://prod.cashfree.com/pgtransactionhealthsvc/bankhealth/gateway"
headers = {'Content-type': 'application/json'}
r = requests.post(url, json=data, headers=headers)

#print(r.status_code)
output = r.json()
pgList = output["healthStatsForAllSwitches"]

outputStr = str(datetime.datetime.now()) + "|"
for pgMap in pgList:
    for k in pgMap.keys():
        outputStr += k + "@" + str(pgMap[k]) + "|"

print(outputStr)

