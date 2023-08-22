


from tkinter import filedialog
from tkinter import *
from stegano import lsb
import speech_recognition as sr         
import cv2
import math
import os
import shutil
from time import *
from subprocess import call,STDOUT
import aesutil
import sys
from termcolor import cprint 
from pyfiglet import figlet_format
import rsautil1
import base64
import PIL.Image as PILImage
from simple_colors import *
import time
from tkinter.filedialog import askopenfile
from gtts import gTTS
import random


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
    cprint("Select your encryption type \n 1) AES Encrypted {Symetric Encryption} \n 2) RSA Encrypted {Assysmetric Encryption}\n",'blue')
    Encryption_Style=int(encode_method)
    if Encryption_Style == 1:
        res=input_string
        key123=int(2)
        key = "1"
        if key123==1:
           input_string = aesutil.encrypt(key=key,source=res) 
        else:
            input_string = aesutil.encrypt(key=key,source=res,keyType='ascii')
        key_path = "./keys/public_key_5000.pem"
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

        li=[]
        while(len(li)!=split_string_length):

            num=random.randint(10,99)

            if(num not in li):

                li.append(num)
        print(li)
        # FRAMES = [random.randint(10,100) for i in range (1,split_string_length+1)]
        FRAMES = li
    
        # frame_choice = int(input("1) Do you want to store frame numbers in an image \n 2) No! Don't store : "))
        frame_choice = 1
        if frame_choice == 1:
            ENCODE_IMAGE = "test.jpg"
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
        key_path = "./keys/public_key_5000.pem"
        input_string = rsautil1.encrypt(message=res,key_path=key_path)
        input_string = input_string.decode('utf-8')
        input_string = str(input_string)
        print(f"Encypted message: \n {input_string}")
        split_string_list=split_string(input_string)
        #print(split_string_list)
        split_string_length = len(split_string_list)
        FRAMES = [i for i in range(1,16)]
        # frame_choice = int(input("1) Do you want to store frame numbers in an image \n2) No! Don't store : "))
        frame_choice = 2
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
    ENCODE_CHOICE = int(file_type1)
    print("inside main")

    # ENCODE_CHOICE = int(input("Choose text or text from text document to hide inside image. \n Enter number either 1|2|3|4|5 : \n1.TEXT \n2.TEXT DOCUMENT  \nEnter Your Choice : "))
    # print("Enter Your Choice : ")

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
    if ENCODE_CHOICE==2:
        print("Please Select a Txt file as an Input")
        # FILE_TO_ENCODE  =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Text files","*.txt"),("all files","*.*")))
        FILE_TO_ENCODE= to_hide1

        # FILE_TO_ENCODE = input("Select text from file:")
        TEXT_TO_ENCODE = []
        with open(FILE_TO_ENCODE) as f:
            for lines in f:
                TEXT_TO_ENCODE.append(lines)
        TEXT_TO_ENCODE = str(TEXT_TO_ENCODE)
        print(TEXT_TO_ENCODE)
        TEXT_TO_ENCODE+="2"
        countFrames()
        frame_extraction(f_name)
        encode_string(TEXT_TO_ENCODE)
    # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        print(yellow('Video is succesfully encoded with encrypted text Document', ['bold']))
        # cprint("Video is succesfully encoded with encrypted text.",'yellow')
        clean_tmp()

    if ENCODE_CHOICE==3:
        # root=Tk()
        FILE_TO_ENCODE= to_hide1
        # FILE_TO_ENCODE  =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Image files","*.*"),("all files","*.*")))


        img=cv2.imread(FILE_TO_ENCODE)
        # img=cv2.resize(img,(1000,1000))
        li=[]

        # cv2.imshow("img",img)
        # root.destroy()
        # root.mainloop()
        # .deiconify()
        # print("Hello")
        # cv2.waitKey(0)
        # print("Hello2")
        # root.mainloop()
        for i in img:
            for j in i:
                for k in j:
                    li.append(k)

      
        s=" ".join(str(x) for x in li)
        a,b,c=img.shape
        s+=str(a)+str(b)+"3"
        # print(s)
        countFrames()
        frame_extraction(f_name)
        encode_string(s)
        # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        print(yellow('Video is succesfully encoded with Image.', ['bold']))
        # cprint("Video is succesfully encoded with encrypted text.",'yellow')
        clean_tmp()

    if ENCODE_CHOICE==4:
        r=sr.Recognizer()
        # print("1")
        print(yellow('Audio Name Speech.wav is reading...', ['bold']))
        with sr.AudioFile(to_hide1) as source:

            audio_text = r.listen(source)
            print(audio_text)
            # print("1")
            try:
                text = r.recognize_google(audio_text)
                # print('Converting audio transcripts into text ...')
                print(text)
            except:
                print('Sorry.. run again...')

        text+="4"
        countFrames()
        frame_extraction(f_name)
        encode_string(text)
        # print("Hurreg")
    # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        cprint("Video is succesfully encoded with encrypted audio.",'green')
        clean_tmp()




    if ENCODE_CHOICE==5:
        print(yellow('Be Patient for processing ', ['bold']))
        # print("Be Patient for processing")
        # vishal =Tk()
        FILE_TO_ENCODE= f1

        # FILE_TO_ENCODE = input("Select text from file:")
        TEXT_TO_ENCODE = []
        with open(FILE_TO_ENCODE) as f:
            for lines in f:
                TEXT_TO_ENCODE.append(lines)
        TEXT_TO_ENCODE = str(TEXT_TO_ENCODE)
        print(TEXT_TO_ENCODE)

        text1=TEXT_TO_ENCODE

        
        # time.sleep(2)
        # print(yellow('The text Entered is ', ['bold'],text1))
        path = f2


        

        r=sr.Recognizer()
        # # print("1")
        # print(yellow('Audio Name Speech.wav is reading...', ['bold']))
        with sr.AudioFile(path) as source:

            audio_text = r.listen(source)
            # print("1")
            try:
                text2 = r.recognize_google(audio_text)
                # print('Converting audio transcripts into text ...')
                 
                print(text2)
            except:
                print('Sorry.. run again...')
        print("\n")
        # time.sleep(2)
        path= f3
        


        img=cv2.imread(path)
        img=cv2.resize(img,(168,200))
        li=[]
        # a,b,c=img.shape
        
        for i in img:
            for j in i:
                for k in j:
                    li.append(k)

      
        text3=" ".join(str(x) for x in li)

        print("\n\n")
        # time.sleep(2)
        path= f4


        cap = cv2.VideoCapture(path)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        li=[]
        count=0

        while(cap.isOpened()):

            ret, frame = cap.read()
            if ret == True:
                frame = cv2.resize(frame, (100, 100))
                # cv2.imshow('frame',frame)
                # count+=1
                # if(count%2==0):

                    # fp+=1
                # for i in frame:

                    # for j in i:
                        # for k in j:
                            # li.append(k)

                count+=1
                if(count%48==0):
                    # 4 lakh


                    # fp+=1
                    for i in frame:

                        for j in i:
                            for k in j:
                                li.append(k)
                            
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        text4=" ".join(str(x) for x in li)
        # input()
        print(text1)
        sleep(1)
        print(text2)
        sleep(1)
        print(text3)
        sleep(1)
        print(text4)
        print("\n\n")
        time.sleep(2)
        s=text1+"***"+text2+"***"+text3+"***"+text4
# 1 89 32 2 5 6 7 8 9 10 11 12 13 14 18
# 89 32 2 5 6 7 8 9 10 11 12 13 14 18 1
#./keys/public_key_5000.pem
        # Prajwal Hitashri Nupur Vishal Sameer are the  Members of group 9
        # r=sr.Recognizer()
        # # print("1")
        # print(yellow('Audio Name Speech.wav is reading...', ['bold']))
        # with sr.AudioFile('speech.wav') as source:

        #     audio_text = r.listen(source)
        #     # print("1")
        #     try:
        #         text = r.recognize_google(audio_text)
        #         # print('Converting audio transcripts into text ...')
        #         print(text)
        #     except:
        #         print('Sorry.. run again...')


        countFrames()
        frame_extraction(f_name)
        encode_string(s)
        # print("Hurreg")
    # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        cprint("Video is succesfully encoded with Multiple formats data .",'green')
        clean_tmp()



        
        # FILE_TO_ENCODE= input("\n Enter image name with extension : ")
        # FILE_TO_ENCODE  =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Image files","*.*"),("all files","*.*")))

        # # print("Succ")
        # # Language in which you want to convert
        # language = 'en'
        # myobj = gTTS(text=FILE_TO_ENCODE, lang=language, slow=False)
        # print("Succ1")
        # # img=cv2.imread(FILE_TO_ENCODE)
        # # Saving the converted audio in a mp3 file named
        # # welcome 
        # myobj.save("welcome1.mp3")
        # print("Succ2")
  
        #    Playing the converted file
        # os.system("welcome.mp3")
        # r = sr.Recognizer()
        # with sr.AudioFile('spech.wav') as source:


        #     audio_text = r.listen(source)
        # #    recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        #     try:


        # using google speech recognition
                # text = r.recognize_google(audio_text)
                # print('Converting audio transcripts into text ...')
                # print(text)
    # if ENCODE_CHOICE==6:
    #     print("Be Patient for processing")

        # text1 = input("1.enter text to hide\n")
        # print("Select file to hide audio")
        # file = askopenfile(parent=vishal, mode='r+', title = "ADD DATA",filetype=[("audio file",".wav"),("ALL FILES", ".*")])

        # r=sr.Recognizer()
        # # print("1")
        # print(yellow('Audio Name Speech.wav is reading...', ['bold']))
        # with sr.AudioFile(file.name) as source:

        #     audio_text = r.listen(source)
        #     # print("1")
        #     try:
        #         text2 = r.recognize_google(audio_text)
        #         # print('Converting audio transcripts into text ...')
        #         print(text2)

        # countFrames()
        # frame_extraction(f_name)
        # encode_string(s)
        # print("Hurreg")
    if ENCODE_CHOICE==6:
        print("Be Patient for processing")

        cap = cv2.VideoCapture(to_hide1)
        length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        li=[]
        count=0

        while(cap.isOpened()):

            ret, frame = cap.read()
            if ret == True:
                frame = cv2.resize(frame, (150, 150))
                # cv2.imshow('frame',frame)
                # count+=1
                # if(count%2==0):

                    # fp+=1
                # for i in frame:

                    # for j in i:
                        # for k in j:
                            # li.append(k)

                count+=1
                if(count%48==0):
                    # 4 lakh


                    # fp+=1
                    for i in frame:

                        for j in i:
                            for k in j:
                                li.append(k)
                    a,b,c=frame.shape
                            
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
            else:
                break
        s=" ".join(str(x) for x in li)
        s+=str(a)+str(b)+"6"

        # r=sr.Recognizer()
        # # print("1")
        # print(yellow('Audio Name Speech.wav is reading...', ['bold']))
        # with sr.AudioFile('speech.wav') as source:

        #     audio_text = r.listen(source)
        #     # print("1")
        #     try:
        #         text = r.recognize_google(audio_text)
        #         # print('Converting audio transcripts into text ...')
        #         print(text)
        #     except:
        #         print('Sorry.. run again...')


        countFrames()
        frame_extraction(f_name)
        encode_string(s)
        # print("Hurreg")
    # Mix images into video and add audio.
        call(["ffmpeg", "-i",f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/%d.png" , "-vcodec", "png", "tmp/video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)  
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        cprint("Video is succesfully encoded with encrypted Video.",'green')
        clean_tmp()




def multi(cover,to_hide1,to_hide2,to_hide3,to_hide4,file_type,encode_method1):
    print("name is ",cover)
    print("to_hide is ",to_hide1)
    print("to_hide is ",to_hide2)
    print("to_hide is ",to_hide3)
    print("to_hide is ",to_hide4)
    print("file_type is ",file_type)
    global f_name
    f_name = cover
    global f1
    f1 = to_hide1
    global f2
    f2 = to_hide2
    global f3
    f3 = to_hide3
    global f4
    f4 = to_hide4
    global file_type1
    file_type1 = file_type
    global encode_method
    encode_method = encode_method1

    print("encode_method is ",end="")
    if(encode_method=='1'):
        print("AES")
    else:
        print("RSA")
    main()
    


        
    
def final(name,to_hide,file_type,encode_method1):
    # os.system('cls' if os.name == 'nt' else 'clea/r')
    print("name is ",name)
    print("to_hide is ",to_hide)
    print("file_type is ",file_type)

    global name1
    name1 = name
    global to_hide1
    to_hide1 = to_hide
    global file_type1
    file_type1 = file_type
    global encode_method
    encode_method = encode_method1
    print("name is ",name1)
    print("to_hide is ",to_hide1)
    print("file_type is ",file_type1)
    print("encode_method is ",end="")
    if(encode_method=='1'):
        print("AES")
    else:
        print("RSA")
    print(type(file_type1))

    cprint(figlet_format('Group6', font='slant'),'yellow', attrs=['bold'])
    # time.sleep(3)
    # print("\n")

    
    # print(green('Guide: Prof. (Dr.) Premanand P. Ghadekar', ['bold']))
    # print("Guide: Prof. (Dr.) Premanand P. Ghadekar")
    # time.sleep(2)

    print("\n")
    # print(blue('Group Members', ['bold']))
    # Prajwal Atram, Hitashri Patil, Nupur Shinde, Vishal Singh, Sameer Meshram
    # print("\n")
    # print("06 - Prajwal Atram")
    # print("40 - Hitashri Patil")
    # print("54 - Nupur Shinde")
    # print("63 - Vishal Singh")
    # print("76 - Sameer Meshram")
    
    # print("\n\n")
    time.sleep(2)
    print(yellow('Video Steganography', ['bold']))
    print("\n\n")
    cprint(figlet_format('AES & RSA encrytion', font='digital'),'green', attrs=['bold'])
    global f_name
    f_name = name
    #image_name = sys.argv[2]
    main()
