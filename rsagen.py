from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import os
def generate_keys(key_size):
    private_keys_path = './keys/private_key_1024.pem'
    isFileprivate = os.path.isfile(private_keys_path)
    public_keys_path = './keys/public_key_1024.pem'
    isFilepublic = os.path.isfile(public_keys_path)
    if isFileprivate & isFilepublic is True:
        print("Public and private keys are  created")
    else :
    # generating a key pair of public and private key for given size   
        key_pair = RSA.generate(key_size)
    
    # storing private key in file name as private_key_{keysize}.pem 
        file_obj = open("./keys/private_key_"+str(key_size)+".pem", "wb")
        file_obj.write(key_pair.exportKey('PEM'))
        file_obj.close()
    
        pubkey = key_pair.publickey()
    
    # storing public key in file name as public_key_{keysize}.pem    
        file_obj = open("./keys/public_key_"+str(key_size)+".pem", "wb")
        file_obj.write(pubkey.exportKey('OpenSSH'))
        file_obj.close()
        print("Public and Private keys are \ncreated and stored inside keys folder.")
if __name__ == '__main__':
    key_size = 5000
    generate_keys(key_size)