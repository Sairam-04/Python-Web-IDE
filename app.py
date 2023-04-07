from flask import Flask, render_template, request
from os import system
import subprocess
import random
# from flask_ngrok import run_with_ngrok
  
app = Flask(__name__)
# run_with_ngrok(app)

@app.route('/')
def index():

    return render_template("index.html",output='')


@app.route('/run',methods=['POST'])
def run_script():
    code = request.form['code']
    with open("runner.py","w") as rnr: 
        rnr.write(code)
    run_code()
    with open("output_file.txt","r") as opfile:
        op = opfile.readlines()
    
    op = [remove_esc(line) for line in op]
    print(op)
    return render_template("index.html", output = op, script = code)


def run_code():
    command = f'python runner.py'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    with open("output_file.txt","w") as opf:
        opf.write(output.decode('utf-8'))
        opf.write(error.decode('utf-8'))
    return

def remove_esc(s):
    escapes = ''.join([chr(char) for char in range(1,10)])
    translator = str.maketrans('','',escapes)
    s = s.translate(translator)
    return s

if __name__ == "__main__":
    app.run()