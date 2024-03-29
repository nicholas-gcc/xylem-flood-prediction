import numpy as np
import requests
import pickle
import re
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

# Constants
USGS_URL = 'https://waterdata.usgs.gov/nwis/uv?site_no=14206950&legacy=1'
DATETIME_REGEX = r'((0[1-9]|1[0-2])\-(0[1-9]|1\d|2\d|3[01])\-(19|20)\d{2}\s\s([0-1]?[0-9]|2[0-3]):[0-5][0-9]\s([P][D][T])\s)$'
DATA_REGEX = r'[\d\.\d]+'

# Flask App
app = Flask(__name__, static_folder='static')

# Load Model
model = pickle.load(open('model.pkl', 'rb'))

def fetch_data(url):
    """
    Fetches data from the given URL and returns it in the form of lists.
    :param url: The URL to fetch data from.
    :return: A tuple of data_list, datetime_list, data_stringified.
    """
    source = requests.get(url).text
    soup = BeautifulSoup(source)

    data_list = []
    datetime_list = []
    data_stringified = []

    for element in soup.findAll('div', {"class" : "stationContainerHeading"}):
        formatted_description = element.next_sibling.strip('\n\n').encode('ascii', 'ignore').decode('utf-8')
        formatted_datetime = (re.findall(DATETIME_REGEX, formatted_description))[0][0]
        formatted_data_to_string = re.findall(DATA_REGEX, formatted_description)[0]
        formatted_data = float(formatted_data_to_string)

        data_list.append(formatted_data)
        datetime_list.append(formatted_datetime)
        data_stringified.append(formatted_data_to_string)

    return data_list, datetime_list, data_stringified

def get_prediction(characteristics):
    """
    Returns a prediction based on the given characteristics.
    :param characteristics: The characteristics to base the prediction on.
    :return: A prediction string.
    """
    final_characteristics = [np.array([float(x) for x in characteristics])]
    prediction = model.predict(final_characteristics)

    if str(prediction) == '[1.]':
        return "It is likely to flood today"
    else:
        return "It is unlikely to flood today"

@app.route('/')
def home():
    try:
        data_list, datetime_list, data_stringified = fetch_data(USGS_URL)
    except Exception as e:
        return render_template('error.html', message=str(e))  # Create an error.html template for displaying errors

    prediction = get_prediction([data_list[2], data_list[1], data_list[6]])

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
    prediction = get_prediction(request.form.values())
    return render_template('about_model.html', prediction_text=prediction)

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
    app.run(host='0.0.0.0', debug=True, port=5001)
