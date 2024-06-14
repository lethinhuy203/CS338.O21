from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session
from flask_cors import CORS
from flask_restful import Api 
import cloudinary 
from cloudinary.uploader import upload as cloudinary_upload
from .utils import allowed_file
import os
from dotenv import load_dotenv
from .image_processing import predict_sample, predict_ensemble_sample
from src.db import get_db
from . import db


# loading variables from .env file
load_dotenv() 

def create_app():
    # Khởi tạo và cài đặt Flask
    app = Flask(__name__)

    # init database 
    app.config['DATABASE'] = os.getenv('DB_ENDPOINT')
    db.init_app(app)
    
    # Cho phép tất cả API được vượt tường
    api = Api(app) 
    CORS(app)

    # Cấu hình Cloudinary 
    cloudinary.config.update = ({
        'cloud_name': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'api_key': os.getenv('CLOUDINARY_API_KEY'),
        'api_secret': os.getenv('CLOUDINARY_API_SECRET')
    })

    # Cấu hình thư mục upload bên ngoài thư mục static
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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


    @app.route('/result')
    def result():
        filename = session.get('filename')
        url = session.get("url")
        pred_results = predict_ensemble_sample(url, fetch=True, threshold=0.7)
        disease_id, confidence_score, props = pred_results
        #TODO: retrieve info from database
        db = get_db()

        if disease_id != 'Unknown':
            plant_disease_info = db.execute(
                'SELECT * FROM PlantDisease WHERE disease_id = ?', (disease_id,)
            ).fetchone()
        
            if plant_disease_info is None:
                app.logger.info('Healthy leaf')
            else:
                print(plant_disease_info['plant_name'])
                print(plant_disease_info['disease_name'])
                print(plant_disease_info['affect'])
                print(plant_disease_info['solution'])

        return render_template('result.html', filename=disease_id, url=url)

    return app