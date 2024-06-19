from flask import Flask, flash, render_template, request, redirect, url_for, send_from_directory, session
from flask_cors import CORS
from flask_restful import Api 
import cloudinary 
from cloudinary.uploader import upload as cloudinary_upload
from .utils import allowed_file, retrieve_info, log_prediction
import os
from dotenv import load_dotenv
from .image_processing import predict_efficientnet, predict_ensemble, predict_dino, predict_yolo
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
            file = request.files.get('file', None)
            model_selected = request.form.get('selected-model-data', 'ensemble')
    
            if 'currentImageUrl' in request.form:
                # Nếu currentImageUrl có trong form, sử dụng URL này cho dự đoán
                url = request.form['currentImageUrl']
                filename = url.split('/')[-1]
                session['url'] = url
                session['filename'] = filename
                session['model-selected'] = model_selected
                return redirect(url_for('result'))
        
            if file and allowed_file(file.filename):
                app.logger.info('%s file_to_upload', file)
                if model_selected:
                    session['model-selected'] = model_selected

                # Upload file mới
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
                flash("File type not allowed or no file uploaded!", "error")
                return redirect(request.url)

        return render_template('upload.html')



    @app.route('/result',  methods=['GET'])
    def result():
        filename = session.get('filename')
        url = session.get("url")
        model_name = session.get('model-selected')
        confidence_score = None

        match model_name:
            case 'ensemble': 
                pred_results = predict_ensemble(url, fetch=True, threshold=0.7)
                disease_id, confidence_score, props = pred_results
                model_name = 'Ensemble MobileNetV2'
            case 'dino': 
                disease_id = predict_dino(url)
                model_name = 'DINOv2 + SVM'
            case 'yolo': 
                disease_id = predict_yolo(url)
                model_name ='YOLOv8'
            case 'efficientNet': 
                pred_results = predict_efficientnet(url)
                disease_id, confidence_score, props = pred_results
                model_name = 'EfficientNet'

        # save prediction log for future use
        log_prediction(url, disease_id, model_name)

        condition = retrieve_info(disease_id)
        if condition['status'] != 0 and confidence_score:
            condition['Confidence score'] = confidence_score

        return render_template('result.html', filename=filename, url=url, condition=condition, model_name=model_name)


    return app