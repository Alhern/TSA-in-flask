from flask import Flask, request, render_template
import requests

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def home():
    url = 'http://algo_container:5000'
    if request.method == 'POST':
        if 'text' in request.form:
            text = request.form['text']
            r = requests.post(url=url, data={"text": text})
            string_prediction = r.text
            return render_template('index.html', string_prediction=string_prediction)
        elif request.files['file']:
            file = request.files['file']
            try:
                r = requests.post(url=url, files={"file": file})
                if r.ok:
                    pos_tweets = r.json()['pos']
                    neg_tweets = r.json()['neg']
                    return render_template('index.html', pos_tweets=pos_tweets, neg_tweets=neg_tweets)
                else:
                    error = r.text
                    return render_template('index.html', error=error)
            except Exception as e:
                app.logger.error(e)
                return render_template('index.html')
    return render_template('index.html')


app.run(host='0.0.0.0', port=5001, debug=False)
