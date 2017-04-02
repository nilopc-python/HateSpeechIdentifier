# HateSpeechIdentifier
Part of a larger project; this takes a sentence (or tweet) and classifies it using IBM's Watson's Sentiment Analysis and Machine Learning. It returns a score between 0-2 which can be interpreted as following:
  < 1: Classified as hate speech
  around 1 and up to 1.5: classified as offensive language
  above 1.5: classified as non-offensive
  
  The classifications are based on a collection of 15K tweets (the model was trained on only 8.5K which were cleaned on time). The curated tweet collection that served as the basis for this project is at https://github.com/t-davidson/hate-speech-and-offensive-language, and it is part of a broader research project undertaken by : Thomas Davidson, Dana Warmsley, Michael Macy, Ingmar Weber as was published in their paper Automated Hate Speech Detection and the Problem of Offensive Language (March 2017).
  
Only twitclas.py is required to run this program, and it can run as the backend of a larger website or application (sent.py includes additional tools to work with and extract information about the various measures of sentiment analysis; mlttwitter.py focuses on the machine learning part)


  
This project was built as part of the Princeton 2017 Hackathon (31 March-2 April 2017). 
