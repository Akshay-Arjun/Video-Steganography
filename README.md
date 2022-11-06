
# Video-Steganography

AES 256 & RSA encrypted video steganography.

# License :
<a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc/4.0/">Creative Commons Attribution-NonCommercial 4.0 International License</a>.
</br> ``` A creative commons license that bans commercial use.```
# Tested On :
- Kali Linux
- WSL
- Ubuntu 
- Debian 
- Termux


## Features
 
- Encrypt and Encode Text In Video.
- Decode and Decrypt Text From Video.
- Choose AES-256 or RSA Encryption.
- Apply RSA Encryption For AES key.
- Choose Any Frame Number.
- Save Frame Numbers Inside Another Image like Image.png <img style="border-width:0" src="https://raw.githubusercontent.com/Akshay-Arjun/Video-Steganography/main/image.png"/>


## Cracking Keys ?

### AES-256 Breaking :  
- Takes 27,337,893 trillion trillion trillion trillion years to bruteforce key using single computer.
- Takes 13,689 trillion trillion trillion trillion years to bruteforce key using all computers in the world.
### RSA-5000 Breaking :
- 2^1024 / (5.000.000 * 16 * 60 * 60 * 24 * 365) Years to compute the key using brute force, which is about 10^292 years to break RSA-1024.
- We use RSA-5000,I leave it to your imagination on long it takes to break RSA.
## Installation

1 ) Clone project with git

```bash
git clone https://github.com/Akshay-Arjun/Video-Steganography
```
2 ) Go to the directory & install requirements 
```bash
pip install -r requirements.txt
```
3 ) Install FFmpeg </br>
   [Changes depending on the operating system you are using.](https://ffmpeg.org/download.html) </br>
   For Linux & WSL use :
```bash
sudo apt install ffmpeg -y
```
4 ) Create RSA keys.
```bash
python3 rsagen.py
```


## Usage/Examples
1 ) Encryption & Encoding
```bash
python3 encode.py <video-to-encode-with-extension>
```
  Example: 
  ```
  python3 encode.py srutest.mp4
  ```

2 ) Decoding & Decryption
```bash
python3 decode.py <video-to-decode-with-extension>
```
  Example: 
  ```
  python3 decode.py video.mov
  ```

## Contributing

Contributions are always welcome!


## Support

For support, email 4k5h4y4rjun@duck.com.

