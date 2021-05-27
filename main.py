import numpy as np
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', prediction_text = 'Will it flood today?')

#To use the predict button in our web-app
@app.route('/predict', methods=['GET','POST'])
def predict():
    int_characteristics = [float(x) for x in request.form.values()]
    final_characteristics = [np.array(int_characteristics)]
    prediction = model.predict(final_characteristics)
    if str(prediction) == '[1.]':
        return render_template('index.html', prediction_text="It is likely to flood today")
    else:
        return render_template('index.html', prediction_text="It is unlikely to flood today")

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