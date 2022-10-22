# This script is used to encode and encrypt the message from the encoded video

'''
Install dependencies:
pip install -r requirements.txt

Usage: 
python encode.py <path_to_video>

Example:
python encode.py srutest.mp4
'''


from stegano import lsb                                                            
import cv2
import math
import os
import shutil
from subprocess import call,STDOUT
import aesutil
import sys
from termcolor import cprint 
from pyfiglet import figlet_format
import rsautil1
import base64
import PIL.Image as PILImage
# Used to split string into parts.
def split_string(s_str,count=15):
    per_c=math.ceil(len(s_str)/count)
    c_cout=0
    out_str=''
    split_list=[]
    for s in s_str:
        out_str+=s
        c_cout+=1
        if c_cout == per_c:
            split_list.append(out_str)
            out_str=''
            c_cout=0
    if c_cout!=0:
        split_list.append(out_str)
    return split_list

# Used to count frames in Video
def countFrames():
    cap = cv2.VideoCapture(f_name)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cprint(f"Total frame in video are : {length-1}",'blue')
    return length

# Extract the frames
def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder="./tmp"
    cprint("[INFO] tmp directory is created",'green')
    vidcap = cv2.VideoCapture(video)
    count = 0
    cprint("[INFO] Extracting frames from video \n Please be patient",'blue')
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, "{:d}.png".format(count)), image)
        count += 1
    cprint("[INFO] All frames are extracted from video",'green')

#Encrypt and encode text into frames
def encode_string(input_string,root="./tmp/"):
    cprint("Select your encryption type /n 1) AES Encrypted {Symetric Encryption} /n 2) RSA Encrypted {Assysmetric Encryption}",'blue')
    Encryption_Style=int(input(""))
    if Encryption_Style == 1:
        res=input_string
        key123=int(input("Choose key type /n 1.HEX /n 2.ASCII : "))
        key = input("Enter the key : ")
        if key123==1:
           input_string = aesutil.encrypt(key=key,source=res) 
        else:
            input_string = aesutil.encrypt(key=key,source=res,keyType='ascii')
        key_path = input("Enter the receiver publickey filename with path to encrypt key : ")
        key_rsa = rsautil1.encrypt(message=key,key_path=key_path)
        key_rsa = key_rsa.decode('utf-8')
        print(f"Asymetric encrypted key to be shared with receiver \n {key_rsa}")
        file_obj = open("./AES-ENC-Key/ReceiverKey.txt", "wb")
        key_rsa = key_rsa.encode()
        file_obj.write(key_rsa)
        file_obj.close()
        print(f"\n AES Encypted message: {input_string}")
        split_string_list=split_string(input_string)
        #print(split_string_list)
        split_string_length = len(split_string_list)
    
        FRAMES = list(map(int, input(f"Enter {split_string_length} FRAME NUMBERS seperated by space : ").split()))
    
        frame_choice = int(input("1) Do you want to store frame numbers in an image /n 2) No! Don't store : "))
        if frame_choice == 1:
            ENCODE_IMAGE = input("Enter image name with extension : ")
            res = str(FRAMES)
            if key123==1:
                FRAMES_ENCODED = aesutil.encrypt(key=key,source=res)
                secret = lsb.hide(ENCODE_IMAGE,str(FRAMES_ENCODED))
                secret.save("image-enc.png")
                cprint("[Info] Frames numbers are hidden inside the image with filename image-enc.png",'red') 
            else:
                FRAMES_ENCODED = aesutil.encrypt(key=key,source=res,keyType='ascii')
                secret = lsb.hide(ENCODE_IMAGE,str(FRAMES_ENCODED))
                secret.save("image-enc.png")
                cprint("[Info] Frames numbers are hidden inside the image with filename image-enc.png",'red')
        else :
            cprint("[Info] Frame numbers are not stored anywhere. Please remember them.",'red')
    else :
        res=input_string
        key_path = input("Enter the publickey filename with path : ")
        input_string = rsautil1.encrypt(message=res,key_path=key_path)
        input_string = input_string.decode('utf-8')
        input_string = str(input_string)
        print(f"Encypted message: \n {input_string}")
        split_string_list=split_string(input_string)
        #print(split_string_list)
        split_string_length = len(split_string_list)
        FRAMES = list(map(int, input(f"Enter {split_string_length} FRAME NUMBERS seperated by space : ").split()))
        frame_choice = int(input("1) Do you want to store frame numbers in an image /n 2) No! Don't store : "))
        if frame_choice == 1:
            ENCODE_IMAGE = input("Enter image name with extension : ")
            res = str(FRAMES)
            FRAMES_ENCODED = rsautil1.encrypt(message=res,key_path=key_path)
            FRAMES_ENCODED = FRAMES_ENCODED.decode('utf-8')
            secret = lsb.hide(ENCODE_IMAGE,str(FRAMES_ENCODED))
            secret.save("image-enc.png")
            cprint("[Info] Frames numbers are hidden inside the image with filename image-enc.png",'red')
            #res = lsb.reveal("image-enc.png") #for debugging
            #res = res.decode('utf-8')
            #res = str(res)
            #print(f"Encrypted frame numbers : {res}") 
        else :
            cprint("[Info] Frame numbers are not stored anywhere. Please remember them.",'red')
    for i in range(0,len(FRAMES)):
        f_name="{}{}.png".format(root,FRAMES[i])
       #print(f_name)
        secret_enc=lsb.hide(f_name,split_string_list[i])
        secret_enc.save(f_name)
        cprint("[INFO] Frame {} holds {}".format(FRAMES[i],split_string_list[i]),'blue')

# delete temporary files
def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        print("[INFO] tmp files are cleaned up")
def main():
    ENCODE_CHOICE = input("type of encodig : \n 1.TEXT \n 2.IMAGE \n 3.TEXT DOCUMENT \n")
    if ENCODE_CHOICE==1:
        TEXT_TO_ENCODE = input("Enter the text to encrypt and encode : ")
        countFrames()
        frame_extraction(f_name)
        encode_string(TEXT_TO_ENCODE)
    # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        cprint("Video is succesfully encoded with encrypted text.",'green')
        clean_tmp()
    else :
        FILE_TO_ENCODE = input("Select text from file:")
        TEXT_TO_ENCODE = []
        with open(FILE_TO_ENCODE) as f:
            for lines in f:
                TEXT_TO_ENCODE.append(lines)
        TEXT_TO_ENCODE = str(TEXT_TO_ENCODE)
        print(TEXT_TO_ENCODE)
        countFrames()
        frame_extraction(f_name)
        encode_string(TEXT_TO_ENCODE)
    # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        cprint("Video is succesfully encoded with encrypted text.",'green')
        clean_tmp()
    

        
    
if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    cprint(figlet_format('Team Byte', font='slant'),'yellow', attrs=['bold'])
    cprint(figlet_format('AES encryted Video Steganography Encoder', font='digital'),'green', attrs=['bold'])
    f_name = sys.argv[1]
    #image_name = sys.argv[2]
    main()