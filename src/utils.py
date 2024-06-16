import re
import tensorflow as tf


def get_url_images_in_text(text:str):
    '''finds image urls'''
    return re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg)', text)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

class FixedDropout(tf.keras.layers.Dropout):
    def _get_noise_shape(self, inputs):
        if self.noise_shape is None:
            return self.noise_shape

        symbolic_shape = tf.keras.backend.shape(inputs)
        noise_shape = [symbolic_shape[axis] if shape is None else shape
                        for axis, shape in enumerate(self.noise_shape)]
        return tuple(noise_shape)