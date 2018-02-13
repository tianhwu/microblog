from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, DATA

#loads data manipulation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta


#loads mapping
import folium
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from folium.plugins import HeatMapWithTime


app = Flask(__name__)

loc_data = UploadSet('data', DATA)


#app.config['UPLOADED_DEFAULTS_DEST'] = 'static/img'
app.config['UPLOADED_DATA_DEST'] = 'static/data'
configure_uploads(app, loc_data)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'data' in request.files:
        filename = loc_data.save(request.files['data'])
        df = pd.read_csv(app.config['UPLOADED_DATA_DEST'] + "/" + filename)
        os.remove(os.path.join(app.config['UPLOADED_DATA_DEST']+ "/" + filename))

        #ensures our lat and long are numeric datatypes
        num_cols = ['latitude','longitude']
        df[num_cols] = df[num_cols].apply(pd.to_numeric)

        #ensures our date column is a datetime object
        dt_cols = ['date']
        df[dt_cols] = df[dt_cols].apply(pd.to_datetime)

        #Calculates a timedelta based and creates a new integer column. Casting sucks in python
        df = df.assign(days_delta=df.date - df.date.min(axis=0))
        df[['days_int']] = (df[['days_delta']]/np.timedelta64(1, 'D')).astype(np.int64)

        #Generates a heatmap centered on New York
        heatmap = folium.Map(location=[40, 12],zoom_start = 2.5) 
        heat_data = [[[row['latitude'],row['longitude']] 
                        for index, row in df[df['days_int'] == i].iterrows()] 
                        for i in range(df.days_int.min(axis=0),df.days_int.max(axis=0))]
        
        #plots a HeatMapWithTime graph
        hm = plugins.HeatMapWithTime(heat_data,auto_play=True,max_opacity=0.7)
        hm.add_to(heatmap)

        heatmap.save('static/map.html')
        return str(df.days_int.max(axis=0))
        
    return render_template('upload.html')

@app.route('/map')
def createsMap():
    return """
    <h1>Please run the upload script before this</h1>

    <iframe src="/static/map.html" width="1200" height="600" frameborder="0" allowfullscreen></iframe>
    """
if __name__ == '__main__':
	app.run(debug=True)
