import requests
import json
import csv
from watson_developer_cloud import ToneAnalyzerV3


tone_analyzer = ToneAnalyzerV3(
   username='36c3b85b-65be-4293-a21e-f9df7e95790f',
   password='mUxPfIHcJFSK',
   version='2017-03-29 ')

# API at https://www.ibm.com/watson/developercloud/tone-analyzer/api/v3/?python#post-tone
# for user/password, go to Tone Analyzer-y1, then Service Credentials, View Credentials
# location: 0 for emotion
#               0 anger
#               1 disgust
#               2 fear
#               3 joy
#               4 sadness
#           1 for language
#               0 analytical
#               1 confident
#               2 tentative
#           2 for social
#               0 Openness
#               1 Conscientiousness
#               2 Extraversion
#               3 Agreeableness
#               4 Emotional Range

# 15K tweet collection (cataloged) at https://github.com/t-davidson/hate-speech-and-offensive-language
#   based on this article: https://arxiv.org/abs/1703.04009
# this has a few guidelines about how to clean tweets: http://www.cs.cmu.edu/~lingwang/papers/sp250-xiang.pdf
# list of swear words: http://www.noswearing.com/dictionary

# this takes in textstring and returns a json object
def sentiments(textstring):
    org = tone_analyzer.tone(text=textstring)
    temp = json.dumps(org, indent=2)
    return json.loads(temp)
    
#this takes in a sentiment json and returns the score of a specific
# tone category and tone
def sent_query(jsonobject, toneCat, tone):
    return jsonobject['document_tone']['tone_categories'][toneCat]['tones'][tone]['score']

# reads user input, based on a prompt
def testing():
    data = input("Enter some text to be analyzed for tone analysis:")
    return data

def printall(textstring):
    jsonobject = sentiments(textstring)
    print("Emotions:")
    for i in range(5):
        cat = ["Anger", "Disgust", "Fear", "Joy", "Sadness"]
        print(cat[i] + ": " + str(sent_query(jsonobject, 0, i)), end="\t")
    print()
    print("Language:")
    for i in range(3):
        cat = ["Analytical", "Confident", "Tentative"]
        print(cat[i] + ": " + str(sent_query(jsonobject, 1, i)), end="\t")
    print()
    print("Big 5:")
    for i in range(5):
        cat = ["Open.", "Conscient.", "Extravers.", "Agreeableness", "Emotion Rng"]
        print(cat[i] + ": " + str(sent_query(jsonobject, 2, i)), end="\t")
    print()

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


#trial = sentiments("hi, how are you today?")
#print (sent_query(trial, 2, 3))
#printall("today is a cold day")

# this is the current main (as of 11:50am)
userdata = testing()
printall(userdata)
print(featurelist(userdata))


# this section reads the tweetdb file, and writes a simplified version to output 
# after adding in all the features from sentiment analysis
inputfile = open("tweetsdb-3000b.csv", "r")
outputfile = open("editedtweets.csv", "w")
reader = csv.reader(inputfile)
writer = csv.writer(outputfile)
for row in reader:
    if row[5] == "The tweet is not offensive": val = "okay"
    elif row[5] == "The tweet uses offensive language but not hate speech": val = "off"
    else:
        val = "hate"
    temp = featurelist(row[19])
    newtemp = []
    for i in temp:
        newtemp.append(str(i))
    rowfixed = "\t".join([val, row[6], row[19]] + newtemp)
    outputfile.write(rowfixed)
    outputfile.write("\n")

inputfile.close()
outputfile.close()