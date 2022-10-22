from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import sys
def encrypt(message,key_path):
    # set public key path 
    public_key_path = key_path
    public_key = RSA.importKey(open(public_key_path, 'r').read())
    # creating the RSA object using public key
    rsa_object = PKCS1_OAEP.new(public_key)
    cipher_text = rsa_object.encrypt(message.encode('utf-8'))
    cipher_text = base64.b64encode(cipher_text)
    return cipher_text
def decrypt(message):
    # set private key path 
    private_key_path = './keys/private_key_5000.pem'
    private_key = RSA.importKey(open(private_key_path, 'r').read())
    # creating the RSA object using private key
    rsa_object = PKCS1_OAEP.new(private_key)
    cipher_text = base64.b64decode(message)
    cipher_text = rsa_object.decrypt(cipher_text)
    return cipher_text
    
if __name__ == '__main__':
    op = sys.argv[1]
    if op=="encrypt" or op==1:
        message = sys.argv[2]
        key_path = sys.argv[3]
        cipher = encrypt(message,key_path)
        print(cipher)
        print(len(cipher))
    elif op=="decrypt" or op==2:
        cipher = sys.argv[2]
        msg = decrypt(cipher)
        print(msg)