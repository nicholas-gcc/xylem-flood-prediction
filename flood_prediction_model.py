import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pickle

def load_and_process_data(path: str, columns: list, dropna: bool = True, numeric: bool = True):
    """Load a CSV file as a DataFrame and process it."""
    df = pd.read_csv(path)
    
    if dropna:
        df = df.dropna()
        
    df = df.iloc[1:]
    
    df.columns = columns

    if numeric:
        df = df.apply(pd.to_numeric, errors='coerce')

    return df

def split_dataset(X, y, test_size=0.25):
    """Split the Dataset into Train and Test."""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size)

    # Check the sample sizes
    print("Train Set :", y_train.shape, X_train.shape)
    print("Test Set  :", y_test.shape, X_test.shape)

    return X_train, X_test, y_train, y_test

def train_model(X_train, y_train, n_estimators=100, max_depth=4):
    """Train the model using Random Forest Classifier."""
    rforest = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)  
    rforest.fit(X_train, y_train.values.ravel())

    # Save the model
    pickle.dump(rforest, open('model.pkl','wb'))

    return rforest

sb.set()

fcd_columns = ['Agency_cd','Site_No','Datetime','Timezone','Gage Height','Discharge','Temperature','Turbidity','Flooding']
fcd = load_and_process_data('resources/FannoCreekDurham.1.csv', fcd_columns)

fc5_columns = ['Agency_cd','Site_No','Datetime','Timezone','Gage Height','Discharge']
fc5 = load_and_process_data('resources/FannoCreek56th.csv', fc5_columns)

# Combine the dataframes
frames = [fcd, fc5]
combined = pd.concat(frames,axis=0).dropna()

predictors = ['Gage Height','Discharge','Turbidity']
y = pd.DataFrame(combined["Flooding"])
X = pd.DataFrame(combined[predictors])

X_train, X_test, y_train, y_test = split_dataset(X, y)

# Train the model
rforest = train_model(X_train, y_train)

# Load the model to compare the results
model = pickle.load(open('model.pkl','rb'))
