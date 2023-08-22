from flask import Flask,render_template,request,flash
from encode import *
from decode import *

app=Flask(__name__)

app.config['SECRET_KEY'] = '12345'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decrypt')
def decrypt():
    return render_template('decrypt.html')

@app.route('/encrypt')
def Analysis():
    # innn name get from analysisForm.html
    name="Vishal Mankotia"
    n="Govindani"
    print(name)
    return render_template('./encrypt.html',name=name,n=n)
 
@app.route('/aboutus')
def About():
    return render_template('aboutUs.html')

@app.route('/encode', methods=['POST','GET'])
def encode():
    result = request.form.to_dict()
    output = result['cover']
    to_hide = result['to_hide']
    file_type = result['file_type']
    encode_method1=result['encode_method']

    final(output,to_hide,file_type,encode_method1)
    print(output,to_hide,file_type)
    
    a=1

    return render_template('decrypt.html',set=a)

@app.route('/decode', methods=['POST','GET'])
def decode():
    result=request.form.to_dict()
    to_decode=result["to_decode"]
    decode_method=result["decode_method"]
    print(to_decode,decode_method)

    message=decrypt_file(to_decode,decode_method)


    return render_template('done.html',message=message)



app.run(debug=True)