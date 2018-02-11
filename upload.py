from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, DATA
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    df = pd.read_csv(request.files.get('data'))
    #return(df[[1,1]])

if __name__ == '__main__':
	app.run(debug=True)