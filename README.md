# CS338.O21
## Project Introduction: Leaf Doctor
Leaf Doctor is a user-friendly web application designed to empower you as a plant parent. This lightweight tool leverages the power of artificial intelligence to help you diagnose and treat leaf diseases in your precious greenery.

## User flow:
1. Snap a photo: Simply use your smartphone or computer to capture an image of your ailing plant's leaf.
2. Upload and diagnose: Upload the picture to Leaf Doctor. Our intelligent system will analyze the image and provide you with a diagnosis.
3. Get informed: Leaf Doctor will identify the specific disease affecting your plant, explain its potential impact, and offer solutions to help your plant recover.

## Team Information 
### Instructor: Ms.C Đỗ Văn Tiến

### Team:
|No.|Member|Student ID|
|:-:|:--|:-:|
|1|[Bui Huynh Kim Uyen](https://github.com/uyenbhku)|21521659|
|2|[Nguyen Nguyen Giap](https://github.com/Paignn)|21522025|
|3|[Nguyen Bui Thanh Mai](https://github.com/mainbt)|21522320|
|4|[Le Thi Nhu Y](https://github.com/lethinhuy203)|21522818|
|5|[Ho Dinh Duy](https://github.com/Hodnduy)|21520769|


# Tech-stacks: 
- Server: Flask 
- CDN: Cloudinary
- Database: SQLite3


# Installations
## Prerequisites
- Python 3.1x

## Run in localhost
- Prepare:
```
# Create virtual environment and activate it
python -m venv venv
source venv/Scripts/activate
# install required packages
pip install -r requirements.txt
```
- Init new database: 
```flask --app src init-db```
- Run: 
```flask --app src run```
- Access: http://127.0.0.1:5000/
