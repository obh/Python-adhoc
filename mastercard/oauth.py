import oauth1.authenticationutils as authenticationutils
from client_encryption.field_level_encryption import encrypt_payload
from client_encryption.field_level_encryption_config import FieldLevelEncryptionConfig
from client_encryption.json_path_utils import get_node, pop_node, update_node, cleanup_node
from oauth1.oauth import OAuth
from Crypto.PublicKey import RSA
from OpenSSL.crypto import load_certificate, load_pkcs12, dump_privatekey, FILETYPE_PEM, FILETYPE_ASN1, Error
from client_encryption.encryption_exception import CertificateError, PrivateKeyError, HashAlgorithmError
import requests
import request_logger

signing_key_path = "/Users/rohitsharma/api_keys/mastercard_token/Tokenization-sandbox.p12"
consumer_key = 'iHkJXQw5p0_R2Oj9vLbXkFckjPXKUyFZFkOB9Gpmfff085f1!fe3aa659ba74490aaa160dde352244660000000000000000'

signing_key = authenticationutils.load_signing_key(signing_key_path, 'keystorepassword')

# uri = 'https://sandbox.api.mastercard.com/service'
# payload = 'Hello world!'
# authHeader = OAuth.get_authorization_header(uri, 'POST', payload, '<insert consumer key>', signing_key)

def getFieldLevelEncryptionConfig():
  return {
      "paths": {
        "$": {
          "toEncrypt": {
              "fundingAccountInfo.encryptedPayload.encryptedData": "fundingAccountInfo.encryptedPayload"
          },
          "toDecrypt": {
              "encryptedPayload": "encryptedPayload.encryptedData"
          }
        }
      },
      "ivFieldName": "iv",
      "encryptedKeyFieldName": "encryptedKey",
      "encryptedValueFieldName": "encryptedData",
      "dataEncoding": "hex",
      "encryptionCertificate": "/Users/rohitsharma/api_keys/mastercard_token/public-key-encrypt.crt",
      "decryptionKey": "/Users/rohitsharma/api_keys/mastercard_token/private-key-decrypt.pem",
      "oaepPaddingDigestAlgorithm": "SHA-512",
      "encryptionKeyFingerprintFieldName": "publicKeyFingerprint",
      "encryptionCertificateFingerprint": "80810fc13a8319fcf0e2ec322c82a4c304b782cc3ce671176343cfe8160c2279",
      "oaepPaddingDigestAlgorithmFieldName": "oaepHashingAlgorithm",
    }


def getPayload():
    return {
      "responseHost": "site1.your-server.com",
      "requestId": "123456",
      "tokenType": "CLOUD",
      "tokenRequestorId": "98765432101",
      "taskId": "123456",
      "fundingAccountInfo": {
        "encryptedPayload": {
          "encryptedData": {
            "cardAccountData": {
              "accountNumber": "5123456789012345",
              "expiryMonth": "09",
              "expiryYear": "25",
              "securityCode": "123"
            },
            "accountHolderData": {
              "accountHolderName": "John Doe",
              "accountHolderAddress": {
                "line1": "100 1st Street",
                "line2": "Apt. 4B",
                "city": "St. Louis",
                "countrySubdivision": "MO",
                "postalCode": "61000",
                "country": "USA"
              }
            },
            "source": "ACCOUNT_ON_FILE"
          }
        }
      },
      "consumerLanguage": "en",
      "tokenizationAuthenticationValue": "RHVtbXkgYmFzZSA2NCBkYXRhIC0gdGhpcyBpcyBub3QgYSByZWFsIFRBViBleGFtcGxl",
      "decisioningData": {
        "recommendation": "APPROVED",
        "recommendationAlgorithmVersion": "01",
        "deviceScore": "1",
        "accountScore": "1",
        "recommendationReasons": [
          "LONG_ACCOUNT_TENURE"
        ],
        "deviceCurrentLocation": "38.63,-90.25",
        "deviceIpAddress": "127.0.0.1",
        "mobileNumberSuffix": "3456"
      }
    }

uri = 'https://sandbox.api.mastercard.com/mdes/digitization/static/1/0/tokenize'

config = FieldLevelEncryptionConfig(getFieldLevelEncryptionConfig())
payload = getPayload()

encrypted_request_payload = encrypt_payload(payload, config)
print(config.paths["$"].to_encrypt.items())
print("Encrypted payload --> ", encrypted_request_payload)
# from https://developer.mastercard.com/mdes-digital-enablement/documentation/tutorials/create-a-new-project/#6-download-client-encryption-key-sandbox
encrypted_request_payload["fundingAccountInfo"]["encryptedPayload"]["publicKeyFingerprint"] = '243E6992EA467F1CBB9973FACFCC3BF17B5CD007'

authHeader = OAuth.get_authorization_header(uri, 'POST', encrypted_request_payload, consumer_key, signing_key)

headerdict = {'Authorization' : authHeader}
request_logger.debug_requests_on()
resp = requests.post(uri, headers=headerdict, json=encrypted_request_payload)
#resp = requests.get(uri, headers=headerdict)

print(resp.headers)
print(resp.text)



