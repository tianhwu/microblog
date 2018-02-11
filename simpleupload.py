from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, DATA
import pandas as pd

app = Flask(__name__)

loc_data = UploadSet('data', DATA)


#app.config['UPLOADED_DEFAULTS_DEST'] = 'static/img'
app.config['UPLOADED_DATA_DEST'] = 'static/img'
configure_uploads(app, loc_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'data' in request.files:
        filename = loc_data.save(request.files['data'])
        df = pd.read_csv('static/img/' + filename)
        return list(df)[1]
        
    return render_template('upload.html')


if __name__ == '__main__':
	app.run(debug=True)