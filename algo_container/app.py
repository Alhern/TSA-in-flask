from algo_container.analyzer import predict_this, most_common_words, tokenize_tweets, dataset_prediction
from algo_container.utils import read_json, valid_json
import algo_container.plots
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
    if request.method == 'POST':
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


# def main():
#     art = '''
# ████████ ███████  █████
#    ██    ██      ██   ██
#    ██    ███████ ███████
#    ██         ██ ██   ██
#    ██    ███████ ██   ██
#     '''
#
#     print(art)
#     print("---Welcome to TSA---")
#     while True:
#         print("---------------------------------------------------")
#         print("What would you like to do?\n")
#         print("\t1) Validate a json file")
#         print("\t2) Analyze a corpus of tweets")
#         print("\t3) Find the most common words in a corpus of tweets")
#         print("\t4) Predict a string")
#         print("\t5) Quit")
#         print("---------------------------------------------------")
#
#         choice = input("\nEnter your choice (1-5): ")
#
#         if choice == "1":
#             path = input("Enter the path to the json file: ")
#             try:
#                 valid_json(path)
#             except Exception as e:
#                 print(e)
#                 exit(1)
#
#         # /!\ On doit avoir passé le fichier obtenu avec miner.py dans valid_json() avant de lancer cette fonction
#         elif choice == "2":
#
#             # On charge le nouveau fichier json avec read_json()
#             path = input("Enter the path to the JSON corpus you want to analyze: ")
#             extra = input("Would you like to visualize extra data? (y/n): ")
#             try:
#                 data = read_json(path)
#                 tokens = tokenize_tweets(data)
#                 # Time to predict, on va calculer les taux de sentiments positifs et négatifs se trouvant dans notre corpus de tweets:
#                 dataset_prediction(tokens)
#
#                 if extra.lower() == "y":
#                     algo_container.plots.all_plots(path)
#             except Exception as e:
#                 print(e)
#                 exit(1)
#
#         elif choice == "3":
#             num = int(input("Enter the number of the most common words you want to see: "))
#             path = input("Enter the path to the JSON corpus you want to analyze: ")
#             try:
#                 data = read_json(path)
#                 tokens = tokenize_tweets(data)
#                 most_common_words(tokens, num)
#             except Exception as e:
#                 print(e)
#                 exit(1)
#
#         elif choice == "4":
#             string = input("Enter the string you want to predict: ")
#             predict_this(string)
#
#         elif choice == "5":
#             print("Bye!")
#             exit(0)
#
#         else:
#             print("Invalid choice\nPlease try entering 1, 2, 3, 4 or 5.")
#             exit(1)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=False)
