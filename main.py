import numpy as np
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html', prediction_text = 'Will it flood today?')

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    int_characteristics = [float(x) for x in request.form.values()]
    final_characteristics = [np.array(int_characteristics)]
    prediction = model.predict(final_characteristics)
    print(prediction)
    output = prediction[0]
    if output == 1.0:
        return render_template('index.html', prediction_text="It is likely to flood today")
    else:
        return render_template('index.html', prediction_text="It is unlikely to flood today")

if __name__ == "__main__":
    app.run(debug=True)