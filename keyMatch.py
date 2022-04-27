from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA


def sign_message(msg):
    digest = SHA256.new()
    digest.update(msg.encode('utf-8'))

    # Load private key previouly generated
    with open ("/Users/rohitsharma/Downloads/unPasswordPrivKey.pem", "r") as myfile:
        private_key = RSA.importKey(myfile.read())

    # Sign the message
    signer = PKCS1_v1_5.new(private_key)
    sig = signer.sign(digest)

    # sig is bytes object, so convert to hex string.
    # (could convert using b64encode or any number of ways)
    print("Signature:")
    print(sig.hex())
    return sig.hex()


def verify_message_signature(message, sig):
    digest = SHA256.new()
    digest.update(message.encode('utf-8'))
    sig = bytes.fromhex(sig)  # convert string to bytes object

    # Load public key (not private key) and verify signature
    public_key = RSA.importKey(open("/Users/rohitsharma/Downloads/cert.pem").read())
    verifier = PKCS1_v1_5.new(public_key)
    #throws exception if it fails
    verifier.verify(digest, sig)
    print('Successfully verified message')


message = "hello world!"
sig = sign_message(message)
verify_message_signature(message, sig)