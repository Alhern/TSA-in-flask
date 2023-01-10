from algo_container.analyzer import predict_this, tokenize_tweets, dataset_prediction
from flask import Flask, request
import json

###################################################
#                                                 #
#                START THE ENGINE!                #
#                                                 #
###################################################

app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def predict():
    if 'text' in request.form:
        text = request.form['text']
        result = predict_this(text)
        return result
    elif request.files['file']:
        try:
            file = request.files['file']
            file.seek(0)
            try:
                data = json.loads(file.read().decode('utf-8'))
            except ValueError as e:
                print(f"Invalid JSON file: {e}")
                app.logger.error(e)
                return e
            tokens = tokenize_tweets(data)
            pos_tweets, neg_tweets = dataset_prediction(tokens)
            result = json.dumps({"pos": pos_tweets, "neg": neg_tweets})
            return result
        except Exception as e:
            app.logger.error(e)
            return e
    else:
        return "", 200


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)
