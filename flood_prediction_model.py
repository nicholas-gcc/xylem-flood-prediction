import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import pickle
sb.set()

fcd = pd.read_csv('resources/FannoCreekDurham.1.csv')
fcd_1=pd.DataFrame.dropna(fcd)
fcd_2 = fcd_1.iloc[1:]
fcd_2.columns=['Agency_cd','Site_No','Datetime','Timezone','Gage Height','Discharge','Temperature','Turbidity','Flooding']

fc5 = pd.read_csv('resources/FannoCreek56th.csv')
fc5_1=pd.DataFrame.dropna(fc5)
fc5_2 = fc5_1.iloc[1:]
fc5_2.columns=['Agency_cd','Site_No','Datetime','Timezone','Gage Height','Discharge']

fcd_3= pd.DataFrame(fcd_2[['Gage Height','Discharge','Temperature','Turbidity','Flooding']])
fcd_4=fcd_3.apply(pd.to_numeric,errors='coerce')

fc5_3= pd.DataFrame(fc5_2[['Gage Height','Discharge']])
fc5_4=fc5_3.apply(pd.to_numeric,errors='coerce')

frames = [fcd_4,fc5_4]
combined = pd.concat(frames,axis=0)
combined_1=pd.DataFrame.dropna(combined)

predictors = ['Gage Height','Discharge','Turbidity']
y = pd.DataFrame(combined_1["Flooding"])
X = pd.DataFrame(combined_1[predictors])

# Split the Dataset into Train and Test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

# Check the sample sizes
print("Train Set :", y_train.shape, X_train.shape)
print("Test Set  :", y_test.shape, X_test.shape)

rforest = RandomForestClassifier(n_estimators = 100, max_depth = 4)  # create the object
rforest.fit(X_train, y_train.values.ravel())                         # train the model

# Saving model to current directory
# Pickle serializes objects so they can be saved to a file, and loaded in a program again later on.
pickle.dump(rforest, open('model.pkl','wb'))

#Loading model to compare the results
model = pickle.load(open('model.pkl','rb'))
print(model.predict([[6.00, 500.0, 69.1]]))


