import re

def get_url_images_in_text(text:str):
    '''finds image urls'''
    return re.findall(r'(?:http\:|https\:)?\/\/.*\.(?:png|jpg|jpeg)', text)


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS