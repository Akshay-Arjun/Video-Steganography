
# Video-Steganography

AES 256 & RSA encrypted video steganography.



## Features
 
- Encrypt and Encode Text In Video.
- Decode and Decrypt Text From Video.
- Choose AES-256 or RSA Encryption.
- Apply RSA Encryption For AES key.
- Choose Any Frame Number.
- Save Frame Numbers Inside Another Image.


## Craking Keys ?

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
2 ) Install requirements 
```bash
pip install -r requirements.txt
```
3 ) Install FFmpeg
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

