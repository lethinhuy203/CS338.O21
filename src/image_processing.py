import tensorflow as tf
from PIL import Image
import numpy as np
import os, gdown
from .utils import get_url_images_in_text
from dotenv import load_dotenv

load_dotenv() 

MODEL_PATH = os.getenv('MODEL_PATH')
CLASS_NAMES = ['Apple___Apple_scab',
 'Apple___Black_rot',
 'Apple___Cedar_apple_rust',
 'Apple___healthy',
 'Blueberry___healthy',
 'Cherry_(including_sour)___Powdery_mildew',
 'Cherry_(including_sour)___healthy',
 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
 'Corn_(maize)___Common_rust_',
 'Corn_(maize)___Northern_Leaf_Blight',
 'Corn_(maize)___healthy',
 'Grape___Black_rot',
 'Grape___Esca_(Black_Measles)',
 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 'Grape___healthy',
 'Orange___Haunglongbing_(Citrus_greening)',
 'Peach___Bacterial_spot',
 'Peach___healthy',
 'Pepper,_bell___Bacterial_spot',
 'Pepper,_bell___healthy',
 'Potato___Early_blight',
 'Potato___Late_blight',
 'Potato___healthy',
 'Raspberry___healthy',
 'Soybean___healthy',
 'Squash___Powdery_mildew',
 'Strawberry___Leaf_scorch',
 'Strawberry___healthy',
 'Tomato___Bacterial_spot',
 'Tomato___Early_blight',
 'Tomato___Late_blight',
 'Tomato___Leaf_Mold',
 'Tomato___Septoria_leaf_spot',
 'Tomato___Spider_mites Two-spotted_spider_mite',
 'Tomato___Target_Spot',
 'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
 'Tomato___Tomato_mosaic_virus',
 'Tomato___healthy']


def download_model(drive_url, model_name):
    """Downloads a model from Google Drive if not already present."""
    model_path = os.path.join(MODEL_PATH, f"{model_name}.h5")
    if not os.path.exists(model_path):
        print(f"Downloading model: {model_name}")
        gdown.download(
            drive_url, 
            os.path.join(MODEL_PATH, f'{model_name}.h5'), 
            quiet=False,
            fuzzy=True # extract drive id from drive URL 
        ) 


try:
    if MODEL_PATH not in os.listdir('.'):
        os.makedirs(MODEL_PATH)
except OSError as e: # name the Exception `e`
        print( "Failed with:", e.strerror) # look what it says
        print( "Error code:", e.code )


def load_model_tf(model_name:str):
    """
    Download trained model and load tensorflow model
    Params:
    `drive_url`: an URL generated by Google Drive when clicked 'Copy link' in share. Please configure view accessibility to "Anyone with the link"
    `model_name`: name of the model
    """
    model = tf.keras.models.load_model(os.path.join(MODEL_PATH, f'{model_name}.h5'))
    return model


def read_and_prep(image_path:str, fetch:bool):
    """
    Read an image from a path or an url 
    Params:
    `image_path`: path or url to the image
    `fetch`: if True, the server will download the file
    """
    if fetch:
        print(image_path)
        image_url = get_url_images_in_text(image_path)[0]
        if image_url:
            try:
                img_path = gdown.download(image_url, quiet=False,)
                print(img_path)
            except:
                return None
        else:
            print(image_path)
            print('Only support PNG and JPEG image or unencrypted file url')
            return None

    img = tf.keras.preprocessing.image.load_img(img_path)
    img = tf.keras.preprocessing.image.smart_resize(
        img,
        size=(224, 224),
        interpolation='nearest'
    )
    try:
        os.remove(img_path) # Remove the cached file
    except OSError as e: # name the Exception `e`
        print( "Failed with:", e.strerror) # look what it says
        print( "Error code:", e.code )
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0) / 255.
    return img


def predict(model, img):
    # Predict the class probabilities with img normalized to [0, 1]
    probs = model.predict(img)[0]
    # Get the predicted class index and name
    pred_class_prob = np.argmax(probs)
    pred_class_name = CLASS_NAMES[pred_class_prob]
    # Print the predicted class name and probability
    print(f'Probability: {probs[pred_class_prob]}')
    print(f'Predicted class: {pred_class_name}')

    return pred_class_name, pred_class_prob, probs


def predict_sample(image_path, fetch=False, threshold=0.5, model=None):
    """
    Load, preprocess and predict an image
    """
    global CLASS_NAMES, model1
    if model is None:
        model = model1

    img = read_and_prep(image_path, fetch)
    if img is None:
        print("We're restricted to read the file on our server, please download the file and upload")
        return

    # Predict the class probabilities with img normalized to [0, 1]
    pred_class_name, pred_class_prob, probs = predict(model, img)

    # Find final label
    if probs[pred_class_prob] < threshold:
        pred_class_name = 'Unknown'

    del img
    return pred_class_name, probs[pred_class_prob], probs


def predict_ensemble_sample(image_path, fetch=False, threshold=0.5):
    """
    Load, preprocess and predict an image
    """
    global CLASS_NAMES, model1, model2
    img = read_and_prep(image_path, fetch)
    if img is None:
        print("We're restricted to read the file on our server, please download the file and upload")
        return

    # Predict the class probabilities with img normalized to [0, 1]
    # first model
    print('Model 1')
    _, pred_class_prob1, probs1 = predict(model1, img)

    print('Model 2')
    # second model
    _, pred_class_prob2, probs2 = predict(model2, img)

    # ensemble
    # Get the predicted class index and name
    probs = (probs1 + probs2)/2
    pred_class_prob = np.argmax(probs)
    pred_class_name = CLASS_NAMES[pred_class_prob]
    # Find final label
    if pred_class_prob1 != pred_class_prob2 \
        or probs[pred_class_prob] < threshold:
        pred_class_name = 'Unknown'

    del img

    return pred_class_name, probs[pred_class_prob], probs



model_links = {
    'mobileNetV2_ver1': 'https://drive.google.com/file/d/18xhVHvV54WqlmincjGwwczifbtHJmHZZ/view?usp=drive_link',
    'mobileNetV2_ver2': 'https://drive.google.com/file/d/1ulDbs-PJNsMVNXEfiV2ejOFd-6h89Mnq/view?usp=drive_link',
    'efficientNet': 'https://drive.google.com/file/d/1Hrp0TyvSDcdDfQrS9YXUD6ibt-hq72DY/view?usp=drive_link',
}

for model_name in model_links:
    download_model(model_links[model_name], model_name)


model1 = load_model_tf(
    model_name='mobileNetV2_ver1'
)

model2 = load_model_tf(
    model_name='mobileNetV2_ver2'
)