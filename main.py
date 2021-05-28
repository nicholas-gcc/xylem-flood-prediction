import numpy as np
from flask import Flask, render_template, request
import requests
import pickle
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
import re

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    data_list = []
    description_list = []
    source = requests.get('https://waterdata.usgs.gov/nwis/uv?site_no=14206950').text
    soup = BeautifulSoup(source)
    for element in soup.findAll('div', {"class" : "stationContainerHeading"}):
        formatted_description = element.next_sibling.strip('\n\n').encode('ascii', 'ignore').decode('utf-8')
        formatted_data = float(re.findall(r'[\d\.\d]+', formatted_description)[0])
        data_list.append(formatted_data)
        description_list.append(formatted_description)

    decision_data_list = [data_list[2], data_list[1], data_list[6]]

    int_characteristics = [float(x) for x in decision_data_list]
    final_characteristics = [np.array(int_characteristics)]
    prediction = model.predict(final_characteristics)

    if str(prediction) == '[1.]':
        prediction = "It is likely to flood today"
    else:
        prediction = "It is unlikely to flood today"

    return render_template('index.html', temp_value=description_list[0], discharge_value=description_list[1],
    gage_height=description_list[2], conductance_value=description_list[3], dissolved_oxygen=description_list[4], 
    turbidity=description_list[6], prediction_text=prediction)


@app.route('/flood_causes', methods=['GET'])
def flood_causes():
    return render_template('flood_causes.html')

@app.route('/flood_protection', methods=['GET'])
def flood_protection():
    return render_template('flood_protection.html')

@app.route('/flood_risks', methods=['GET'])
def flood_risks():
    return render_template('flood_risks.html')

if __name__ == "__main__":
    app.run(debug=True)