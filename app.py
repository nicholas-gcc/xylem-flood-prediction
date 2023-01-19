import numpy as np
from flask import Flask, render_template, request
import requests
import pickle
from bs4 import BeautifulSoup
import re

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    data_list = []
    datetime_list = []
    data_stringified = []
    source = requests.get('https://waterdata.usgs.gov/nwis/uv?site_no=14206950&legacy=1').text
    soup = BeautifulSoup(source)
    for element in soup.findAll('div', {"class" : "stationContainerHeading"}):
        formatted_description = element.next_sibling.strip('\n\n').encode('ascii', 'ignore').decode('utf-8')
        formatted_datetime = (re.findall(r'((0[1-9]|1[0-2])\-(0[1-9]|1\d|2\d|3[01])\-(19|20)\d{2}\s\s([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s([P][D][T])\s)$', 
        formatted_description))[0][0]
        formatted_data_to_string = re.findall(r'[\d\.\d]+', formatted_description)[0]
        formatted_data = float(re.findall(r'[\d\.\d]+', formatted_description)[0])
        data_list.append(formatted_data)
        datetime_list.append(formatted_datetime)
        data_stringified.append(formatted_data_to_string)

    decision_data_list = [data_list[2], data_list[1], data_list[6]]

    int_characteristics = [float(x) for x in decision_data_list]
    final_characteristics = [np.array(int_characteristics)]
    prediction = model.predict(final_characteristics)

    if str(prediction) == '[1.]':
        prediction = "It is likely to flood today"
    else:
        prediction = "It is unlikely to flood today"

    return render_template('index.html', temp_value=data_stringified[0], discharge_value=data_stringified[1],
    gage_height=data_stringified[2], conductance_value=data_stringified[3], dissolved_oxygen=data_stringified[4], 
    turbidity=data_stringified[6], prediction_text=prediction, temp_date=datetime_list[0],
    discharge_date=datetime_list[1], gage_height_date=datetime_list[2], conductance_value_date=datetime_list[3],
    dissolved_oxygen_date=datetime_list[4], turbidity_date=datetime_list[5])

@app.route('/about_model')
def about_model():
    return render_template('about_model.html', prediction_text = 'Will it flood today?')

@app.route('/about_model/predict', methods=['POST'])
def predict():
    int_characteristics = [float(x) for x in request.form.values()]
    final_characteristics = [np.array(int_characteristics)]
    prediction = model.predict(final_characteristics)
    if str(prediction) == '[1.]':
        return render_template('about_model.html', prediction_text="It is likely to flood today")
    else:
        return render_template('about_model.html', prediction_text="It is unlikely to flood today")

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
