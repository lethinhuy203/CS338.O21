from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session
from flask_cors import CORS
from flask_restful import Api 
import cloudinary 
from cloudinary.uploader import upload as cloudinary_upload
from .utils import allowed_file
import os
from dotenv import load_dotenv
from .image_processing import predict_sample, predict_ensemble_sample
# loading variables from .env file
load_dotenv() 

# Khởi tạo và cài đặt Flask
app = Flask(__name__)

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
api = Api(app) 
# Cho phép tất cả API được vượt tường
CORS(app)

# Cấu hình Cloudinary 
cloudinary.config.update = ({
    'cloud_name':os.getenv('CLOUDINARY_CLOUD_NAME'),
    'api_key': os.getenv('CLOUDINARY_API_KEY'),
    'api_secret': os.getenv('CLOUDINARY_API_SECRET')
})


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
            app.logger.info('%s file_to_upload', file)
            upload_result = cloudinary_upload(
                file, 
                resource_type='image',
                folder=UPLOAD_FOLDER
            )
            filename = file.filename
            url = upload_result['url']
            session['url'] = url
            session['filename'] = filename
            return redirect(url_for('result'))
        else:
            flash("File type not allowed!", "error")

    return render_template('upload.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/result')
def result():
    filename = session.get('filename')
    url = session.get("url")
    pred_results = predict_ensemble_sample(url, fetch=True, threshold=0.7)
    #TODO: retrieve info from database
    
    return render_template('result.html', filename=pred_results[0], url=url)


def create_app():
    global app
    return app