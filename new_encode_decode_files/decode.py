
##This File for Text and text Document read
from stegano import lsb
import cv2
import os
import sys
import aesutil
import shutil
import numpy as np
from termcolor import cprint 
from pyfiglet import figlet_format
import rsautil1
from simple_colors import *
import time
from gtts import gTTS
import playsound
import os
from playsound import playsound

def decrypt_file(file,method):
    global to_decrypt
    to_decrypt=file

    global decode_method
    decode_method=method

    global FRAMES

    global Encryption_Style
    global decoded

    os.system('cls' if os.name == 'nt' else 'clear')
    cprint(figlet_format('Group9', font='slant'),'green', attrs=['bold'])
    print(yellow('Video Steganography', ['bold']))
    print(blue('Group Members', ['bold']))
        # Prajwal Atram, Hitashri Patil, Nupur Shinde, Vishal Singh, Sameer Meshram
    print("\n")
    print("06 - Prajwal Atram")
    print("40 - Hitashri Patil")
    print("54 - Nupur Shinde")
    print("63 - Vishal Singh")
    print("76 - Sameer Meshram")

    print("\n\n")
    time.sleep(2)
    cprint(figlet_format('AES & RSA encrytion', font='digital'),'green', attrs=['bold'])
    global ENCODED_VIDEO 
    ENCODED_VIDEO = to_decrypt
    global temp_folder
    temp_folder = "tmp2"
    # frame_choice = int(input("1) Extract and enter frame numbers from image \n2) Enter frame numbers manually : \nEnter choice: "))
    frame_choice=1
    decoded = {}

    if frame_choice == 1:
        ENCODED_IMAGE = "image-enc.png"
        res = lsb.reveal(ENCODED_IMAGE)
        print(f"Encrypted frame numbers : {res}")
        cprint("Select your encryption type \n 1) AES Encrypted {Symetric Encryption} \n 2) RSA Encrypted {Assysmetric Encryption}",'blue')
        Encryption_Style=int(1)
        if Encryption_Style == 1:
            key = "VtCWNhhO8tB96CK2Xso13YtaHndt0j37vp9czIGEQ5QfxwOsQm2xThqPOUFN58inisxiU4iJPykAw0q+6Nrtl3hAXN5oauKq8ukZJGZDvv7J7sLnyhoEWwAi2NJyZLmSq8VkTrTW0t9DfWCszF6vmxQMb/zyWC56/i4CjFj99SHX5M5bKqvzI2ljKTfltdrJVZTabBemcQaVDmv+1G0QmQsfOL/z4wso3vb4L7JUv/Mk6zwiAc9dRDi/KVOYQaS7q+weyBmpbGbn4xPuMfEDpwprCCOAbGLBdDYtGQwUTmy8NBMMN8yyg2t0hFjXHOSUm4HCsv0AEhq+bviaUhtpYf2cCTXH5HFeLB6TDnhCfTqQQ3C1dMqvUmRPNLAyG8LPCNjFKShR8MLsCBs5uPM4EXl+l1YpN5hxjYorXFQHF3yK4VS0O9WJO2WWTHch6sh7DKSq2onlzgWvgP38K020Tx4ZeIiNSslM/NopvT/F7YN2E5X0EYrap6tJq09fcz7HwnbBGkYnRTPzS+uR0/Q95biMJOzZ2sqOu1nqpDTGYr+dlXR5h4aNy1Eu/vkj4ALkq4WFVUvMCtLlcBvtfdaTQwkOpd+6Avy0g7WDQ5kCu/mEfOOrZKeouU5p0vf5cXPyxx4lb/+Dw+6xgU5iMI3CwwJLNb4EW3m0dku56ln6iydHg9NRaM4bDJC0pVJgUyCtTxhCsXZ2UOwHzUJdk+WMg9tcz1UCgx7JBMGZjSpOWLG5X9k0Aa+UKGA17lQ1phJyzs0mdfB5EvFFThNu3qeWSWx3BUjJPIHml1OaABh3GfwO30JiWkHtSBg/47080x9aRg=="
            key_rsa = rsautil1.decrypt(message=key)
            key_rsa = key_rsa.decode('utf-8')
            print(f"Asymetric decrypted key \n {key_rsa}")
            key123=int(2)
            key = '1'
            if key123==1:
                msg = aesutil.decrypt(key=key,source=res)
                msg1 = msg.decode('utf-8')
                cprint(f"Decoded image : \n {msg}",'green')
                FRAMES = list(map(int, input("Enter Above FRAME NUMBERS seperated by space: ").split()))
        
            else:
                msg = aesutil.decrypt(key=key,source=res,keyType='ascii')
                msg1 = msg.decode('utf-8')
                cprint(f"Decoded image: \n {msg1}",'green')
                FRAMES = list(map(int, input("Enter Above FRAME NUMBERS seperated by space: ").split()))
        else :
            cprint("Reading private key from keys \nfolder and trying to decrypt",'red')
            msg1 = rsautil1.decrypt(message=res)
            msg1 = msg1.decode('utf-8')
            cprint(f"Decoded image: \n {msg1}",'green')
            FRAMES = list(map(int, input("Enter Above FRAME NUMBERS seperated by space: ").split()))
    
        
    else :
        

        FRAMES = [i for i in range(1,16)]
        cprint("Select your decryption type \n 1) AES Encrypted {Symetric Encryption} \n 2) RSA Encrypted {Assysmetric Encryption}",'blue')
        Encryption_Style=int(decode_method)
        #print(FRAMES)
    createTmp()
    frames = countFrames()
    decodeVideo(frames)
    return arrangeAndDecrypt()
# pip3 install gTTS pyttsx3
def createTmp():
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

def countFrames():
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length

def decodeVideo(number_of_frames):
    # First get the frame
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    frame_number = -1
    while(frame_number<=number_of_frames):
        frame_number += 1
        frame_file_name = os.path.join(temp_folder,f"{frame_number}.png")
        encoded_frame_file_name = os.path.join(temp_folder,f"{frame_number}-enc.png")
        # print(f"Frame number {frame_number}")
        ret, frame = cap.read()

        if frame_number in FRAMES:
            cv2.imwrite(encoded_frame_file_name,frame)
            clear_message = lsb.reveal(encoded_frame_file_name)
            decoded[frame_number] = clear_message
            cprint(f"Frame {frame_number} DECODED: {clear_message}",'yellow')

def clean_tmp(path="./tmp2"):
    if os.path.exists(path):
        shutil.rmtree(path)
        cprint("[INFO] tmp files are cleaned up",'yellow')

def arrangeAndDecrypt():
    res=""
    if Encryption_Style == 1:

        while(True):
            try:
                for fn in FRAMES:
                    if(decoded[fn]==None):
                        break
                    res = res + decoded[fn]
               
                break
            except:
                FRAMES.pop(-1)
        print(len(FRAMES))
        print(res)
        # A=input("Enter the key to decrypt image : ")
        cprint(f"Final string: {res}",'green')
        key123=int(2)
        key = '1'
        if key123==1:

            msg = aesutil.decrypt(key=key,source=res)
            msg1 = msg.decode('utf-8')
           
            # s=msg
            # li=s.split(" ")
            # result=[]
            # a=[]
            # b=[]
            # print((li))
            # c=0
            # for i in range(154):

            #     for j in range(328):
            #         for k in range(3):
            #             b.append(int(li[c]))
            #             c+=1
            #         a.append(b)
            #         b=[]
            #     result.append(a)
            #     a=[]
            # # ans=[]
            # # for i in result:
            # #     for j in i:
            # #         for k in j:
            # #             ans.append(k)
            # # print((ans))
            # result=np.asarray(result)
            # result=result.astype(np.uint8)
            # # print(result.shape)
            # print(type(result))
            # cv2.imshow('avc',result)
            # cv2.waitKey(0)
            cprint(f"Decoded message: \n {msg}",'green')
            print(1)
            clean_tmp()
        else:
            msg = aesutil.decrypt(key=key,source=res,keyType='ascii')
           
            msg1 = msg.decode('utf-8')

            if(msg1[-1]=='2'):
                s=msg1[:-1]

                print(s)
                s="Your text document Output is \n\n"+s
                return s

            elif(msg1[-1]=='3'):

                s=msg1[:-7]
                r=int(msg1[-7:-4])
                co=int(msg1[-4:-1])
                print(r,co)
                print(type(r))

                li=s.split(" ")
                result=[]
                a=[]
                b=[]
               
                c=0
                print(len(li))
                for i in range(r):
                        
                        for j in range(co):
                            for k in range(3):
                                b.append(int(li[c]))
                                c+=1
                            a.append(b)
                            b=[]
                        result.append(a)
                        a=[]
                print(c)
                result=np.asarray(result)
                # print(result.shape)
                result=result.astype(np.uint8)
                print(result.shape)
                print(type(result))
                cv2.imshow('Hidden Image',result)
                print("Wait until Image Opens!!")

                cv2.waitKey(0)

                return "Image successfully decoded and displayed"


            

            elif(msg1[-1]=='4'):
                s=msg1[:-1]
                print(s)
                myobj = gTTS(text=s, lang='en', slow=False)
                myobj.save("output.mp3")
                print("Audio Successful Decoded from Video")
                # Playing the converted file
                playsound('output.mp3')
                return "Audio successfully decoded and played   "+s
            
            elif(msg1[-1]=='5'):



                pass

            elif(msg1[-1]=='6'):
                r=int(msg1[-7:-4])
                co=int(msg1[-4:-1])
                s=msg1[:-7]


                li=s.split(" ")
                c=0

                while(c<len(li)):

                    result=[]
                    a=[]
                    b=[]

                    for i in range(r):
                                
                                for j in range(co):
                                    for k in range(3):
                                        b.append(int(li[c]))
                                        c+=1
                                    a.append(b)
                                    b=[]
                                result.append(a)
                                a=[]
                    result=np.asarray(result)
                    # print(result.shape)
                    result=result.astype(np.uint8)
                    
                    cv2.resize(result,(500,500))
                    print(result.shape)
                    print(type(result))
                    cv2.imshow('Hidden video',result)
                    # print("Wait until Image Opens!!")

                    cv2.waitKey(2000)
                return "Video successfully decoded and displayed"








            # cprint(f"Decoded message: \n {msg1}",'red')
            # msg1.save("output.mp3")
            print(2)
            # Playing the converted file
            # os.system("output.mp3")
            clean_tmp()
    else :
        for fn in FRAMES:
            res = res + decoded[fn]
        cprint(f"Final string: {res}",'green')
        cprint("Reading private key from keys folder \nand trying to decrypt",'red')
        msg1 = rsautil1.decrypt(message=res)
        msg1 = msg1.decode('utf-8')
        

        
        cprint(f"Decoded text: \n {msg1}",'green')
        clean_tmp()

