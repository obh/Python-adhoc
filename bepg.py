request = {
    "header": {
        "version": "2.0.0.0",
        "callerid": "300081",
        "token": "497c6f48-e29b-4ae5-b6d8-a36588d0de71",
        "userid": "kotakcash"
    },
    "body": {
        "card_bin": "607304987"
    }
}
request = {
	"header": {
		"version": "2.0.0.0",
		"callerid": "300081",
		"token": "497c6f48-e29b-4ae5-b6d8-a36588d0de71",
		"userid": "kotakcash"
	},
	"body": {
		"card_no": "6073049876543212",
		"card_exp_date": "122028",
		"card_cvv": "123",
		"card_holder": "rohit",
        "card_holder_status" : "NW",
		"merchantName": "Cashfree",
		"amount": "100.25",
		"currency_code": "356",
		"shopper_ip_address": "15.206.45.168",
		"requestID": 6123456097631,
		"language_code": "EN"
	}
}
request = {
        "messageId": "6c82ce70-133c-4862-885e-ccaf650cf08b",
        "conversationId": "a8103a75-22ae-4e92-9a7c-ac81883ec2c2",
        "tokenRequestorId": "77799966617",
        "tokenRequestorGtwyId": "77799966617",
        "panSource": "ONFILE",
        "consumerId": "consumer001",
        "pathRecommendation": "APPROVED",
        "presentationMode": ["ECOM"],
        "merchantId": "777999666170000",
        "merchantName": "Cashfree",
        "userData": {
            "panData": {
                "pan": "5305620400000002",
                "panExpDate": "2812"
                }
            }
        }

import json
import base64
_s = json.dumps(request)
msg = base64.urlsafe_b64encode( bytes(_s, 'utf-8') )
print(msg)
from Crypto.PublicKey import RSA
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Hash import SHA256
import binascii

f = open('/Users/rohitsharma/Downloads/bepg/privkey_rsa.pem', 'rb')
f = open('/Users/rohitsharma/Downloads/siddhesh_privkey_rsa.pem', 'rb')
key = RSA.importKey(f.read())

hash = SHA256.new(msg)
signer = PKCS115_SigScheme(key)
signature = signer.sign(hash)
print(signature)
print("Signature:", binascii.hexlify(signature))

