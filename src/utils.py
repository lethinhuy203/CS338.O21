import re
import tensorflow as tf
from .db import get_db


def get_url_images_in_text(text:str):
    '''finds image urls'''
    return re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg)', text)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def log_prediction(image_url, disease_id):
    db = get_db()
    sql = ''' INSERT INTO PredictionLog(image_url, disease_id)
              VALUES(?,?) '''
    try:
        cur = db.cursor()
        cur.execute(sql, (image_url, disease_id))
        db.commit()
    except:
        print('Already logged')

    print('Logged result to db successfully')


def retrieve_info(disease_id):
    condition = dict()
    if disease_id == 'Unknown':
        condition['status'] = 0
        return condition

    db = get_db()
    plant_disease_info = db.execute(
        'SELECT * FROM PlantDisease WHERE disease_id = ?', (disease_id,)
    ).fetchone()
    
    if plant_disease_info is None:
        condition['status'] = 1 # healthy
        condition['Tên lá'] = disease_id.split('_')[0]
        condition['Chẩn đoán'] = 'Lá khỏe mạnh'
        return condition
    else:
        condition = {
            'status': 2, #unhealthy
            "Tên lá": plant_disease_info['plant_name'],
            "Chẩn đoán": plant_disease_info['disease_name'],
            "Biểu hiện": plant_disease_info['affect'],
            "Giải pháp": plant_disease_info['solution'],
        }
        return condition


class FixedDropout(tf.keras.layers.Dropout):
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            return self.noise_shape

        symbolic_shape = tf.keras.backend.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape
                        for axis, shape in enumerate(self.noise_shape)]
        return tuple(noise_shape)