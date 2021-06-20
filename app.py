from flask import Flask, render_template, request

import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, TfidfTransformer
import tweets,clean

#__name__ == __main__
app = Flask(__name__)

countizer = joblib.load('count_vectorizer.pkl')
tfidfizer = joblib.load('tfidf.pkl')

personality_type = [ "IE: Introversion (I) / Extroversion (E)", "NS: Intuition (N) / Sensing (S)", 
                   "FT: Feeling (F) / Thinking (T)", "JP: Judging (J) / Perceiving (P)"  ]

b_Pers_list = [{0:'I', 1:'E'}, {0:'N', 1:'S'}, {0:'F', 1:'T'}, {0:'J', 1:'P'}]

def translate_back(personality):
    # transform binary vector to mbti personality
    s = ""
    for i, l in enumerate(personality):
        s += b_Pers_list[i][l]
    return s

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/predict', methods=['POST'])
def personality():
        if request.method == 'POST':
                twitter_handle = request.form['username']
                tweet = tweets.fetch(twitter_handle)
                data = pd.DataFrame(data={'type':['ENTP'], 'posts':[tweet]})
                text, dummy = clean.pre_process_text(data, remove_stop_words=True, remove_mbti_profiles=True)
                cnt = countizer.transform(text)
                tfidf = tfidfizer.transform(cnt).toarray()

                result = []

                for i in range(len(personality_type)):
                        #load the model
                        model = joblib.load('model_'+str(i)+'.pkl')
                        #make predictions for the tweets
                        pred = model.predict(tfidf)
                        result.append(pred[0])
                res = translate_back(result)
        return render_template("index.html", personality = "Personality type is {}".format(res))


if __name__ == '__main__':
	app.run(debug = True)