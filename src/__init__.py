from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, jsonify
from .utils import allowed_file
import os
from dotenv import load_dotenv
# loading variables from .env file
load_dotenv() 

# Khởi tạo và cài đặt Flask
app = Flask(__name__)

# Cấu hình thư mục upload bên ngoài thư mục static
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            flash("No selected file!", "error")
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for(
                'result', 
                filename=filename, 
                # url=upload_result['url']
            ))
        else:
            flash("File type not allowed!", "error")

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/result')
def result():
    filename = request.args.get('filename')
    return render_template('result.html', filename=filename)