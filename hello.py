from flask import Flask
from flask import request
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask import render_template
import pandas as pd


app = Flask(__name__)


@app.route('/')
def index():
    return "welcome to the index" 

@app.route('/hayabusa')
def hello_world():
    return str(2+4)


photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
configure_uploads(app, photos)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')

@app.route('/uploadcsv', methods=['POST'])
def uploadcsv():
    return render_template('upload.html')
    
if __name__ == '__main__':
	app.run(debug=True)


