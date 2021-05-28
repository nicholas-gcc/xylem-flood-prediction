# Xylem Global Innovation Challenge<br>
## Challenge statement: Urban Flood Prediction<br>

Tools relating to the Xylem Global Innovation Challenge on Urban Flood Prediction

In this Challenge, we aim to use predictive modelling to help Portland, Oregon residents predict and take pre-emptive action against floods.

## Setup Instructions

### Dependencies Setup
1. Create a Python virtual environment ([venv](https://docs.python.org/3/library/venv.html)) by invoking the command on your Command Prompt Shell as follows `C:\>python -m venv C:\path\to\myenv
`
1. On your shell, run `pip install -r requirements.txt`
1. [OPTIONAL] Download, install and run ngrok [here](https://ngrok.com/download) if you want to make your locally run Flask servers accessible on the Internet.

### Running Floodopedia on localhost
1. On your shell, run `python app.py`
1. Go to localhost:5000 on your web browser and you begin by typing 'Hi' onto the input box. Alternatively, you can specify a different IP or port number on the `app.run(host='new-IP-address', port=<new-port-number>)` method in `app.py` and visit new-IP-address:<your-port-number> instead.
1. Press `Ctrl` + `C` to terminate server
  
### Running Floodopedia on the Internet (Production server)
1. On your shell, run `python app.py`
1. Open the ngrok shell and run `ngrok http 5000` or `ngrok http <your-port-number>`
1. You should see a temporary link on your shell and you can access Floodopedia via the displayed link.
1. Press `Ctrl` + `C` to terminate server
  
## Prediction Model
  
### About the prediction model
- The decision classifiers used are Gage Height, Turbidity and Discharge. 
- As flooding is an extreme and rare event, available USGS Data had weak correlations (<0.20) with flooding. However, Gage Height, Turbidity and Discharge had the strongest correlations with flooding
[!heatmap](/static/heatmap.png)
-                                                                                               


### Modifying the Prediction Model
1. If you wish to populate the dataset with newer data, you can pull raw values from the [USGS Fanno Creek Website](https://waterdata.usgs.gov/nwis/uv?site_no=14206950)
1. Modify flood `flood_prediction_model.py` to your liking and seralize your modified model as a pickle file by running `pickle.dump(<model-variable-name>, open('<your-filename>.pkl','wb'))`
1. In `app.py`, de-serialize `<your-filename>.pkl` by taking pickle.load(open('<your-filename>.pkl', 'rb')) and you can now run the `.predict()` method of your model on a dataset

