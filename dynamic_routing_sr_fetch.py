#!/bin/python

import requests
import json
import datetime

def getSR(url):
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
    headers = {'Content-type': 'application/json'}
    r = requests.post(url, json=data, headers=headers)
    
    #print(r.status_code)
    output = r.json()
    pgList = output["healthStatsForAllSwitches"]
    
    outputStr = str(datetime.datetime.now()) + "|"
    for pgMap in pgList:
        for k in pgMap.keys():
            outputStr += k + "@" + str(pgMap[k]) + "|"
    
    return outputStr


url1 = "https://prod.cashfree.com/pgtransactionhealthsvc-test/bankhealth/gateway"
url2 = "https://prod.cashfree.com/pgtransactionhealthsvc-test/v2/bankhealth/gateway"


out1 = getSR(url1)
print("old|", out1)
out2 = getSR(url2)
print("new|", out2)

