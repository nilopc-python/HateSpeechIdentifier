import numpy as np
import pandas as pd
import requests
import json
import csv
from watson_developer_cloud import ToneAnalyzerV3


tone_analyzer = ToneAnalyzerV3(
   username='36c3b85b-65be-4293-a21e-f9df7e95790f',
   password='mUxPfIHcJFSK',
   version='2017-03-29 ')

def getPara():
    print("enter a sentence")
    userInput = input()
    return featurelist(userInput)

# this takes in textstring and returns a json object
def sentiments(textstring):
    org = tone_analyzer.tone(text=textstring)
    temp = json.dumps(org, indent=2)
    return json.loads(temp)
    
#this takes in a sentiment json and returns the score of a specific
# tone category and tone
def sent_query(jsonobject, toneCat, tone):
    return jsonobject['document_tone']['tone_categories'][toneCat]['tones'][tone]['score']

# returns a list of all the features for a textstring
def featurelist(textstring):
    jsonobject = sentiments(textstring)
    ans = []
    for i in range(5):
        ans.append(sent_query(jsonobject, 0, i))
    for i in range(3):
        ans.append(sent_query(jsonobject, 1, i))
    for i in range(5):
        ans.append(sent_query(jsonobject, 2, i))
    return ans


testtwitter = pd.read_csv("8400clean.csv") # _ã¢Û__ can crash system
#estimtaed = pd.read_csv("toEstimate")

# testing measures
#print(testtwitter.head())
#print(testtwitter.shape)
#print(testtwitter.describe())
#print(testtwitter.info())

#print(testtwitter[["grade"]]) # this call works

#import matplotlib.pyplot as plt
#import seaborn as sns
#sns.set(font_scale=1)

# convert the categorical variable to a number
from sklearn.preprocessing import LabelEncoder,OneHotEncoder
labelEnc=LabelEncoder()

testtwitter['emtype']=labelEnc.fit_transform(testtwitter['emtype'])
print(testtwitter.head()) # this works


#classifies a list of parameters using Random Forest
from sklearn.ensemble import RandomForestRegressor
from sklearn import preprocessing

#Feature set
type_df = testtwitter[["emtype", "Anger", "Disgust", "Fear", \
    			"Joy", "Sadness", "Analytical", "Confident", \
    			"Tentative", "Open.", "Conscient.", "Extravers.", \
    			"Agreeableness", "Emotion Rng"]]

train = type_df.loc[(testtwitter.emtype.notnull())]
#test = type_df.loc[ (df.emtype.isnull()) ]
    
#train = scaler.transform(train)    

#print(train.values)
# All values are stored in a target array
y = train.values[:, 0]	# all the values of the first variable, emtype

# All the other values are stored in the feature array
X = train.values[:, 1::]

# Create and fit a model
rtr = RandomForestRegressor(n_estimators=2000, n_jobs=-1)
rtr.fit(X, y)

while True:
    #reg trial
    #temp = [[0.471789,0.636699,0.056785,0.000009,0.061664,0,0,0.874805,0.718028,0.038296,0.863941,0.304049,0.454404]]

    temp = [getPara()]
    predictedValue = rtr.predict(temp)
    print("The predicted value is: %s" % predictedValue)


