import warnings

warnings.filterwarnings('ignore', category=FutureWarning)
import numpy as np
from collections import Counter
from algo_container.utils import read_json, valid_json
from algo_container.filter import filter_stopwords
import algo_container.plots
from algo_container.model import preprocess, build_word_vector, model, N_DIM, w2v_model, tfidf
import matplotlib.pyplot as plt
from tqdm import tqdm

tqdm.pandas(desc="progress-bar")


################ TOOLS TO ANALYZE USER'S DATASET ################


# Les fonctions ici vont permettre d'analyser les tweets récupéré via MINER.PY :

# 1) On commence par passer le dataset dans valid_json(), on va récupérer un fichier json valide
# 2) On passe ce nouveau fichier json dans read_json avant de pouvoir récupérer son contenu
# 3) On va tokenizer les données obtenues avec tokenize_tweets()
# 4) On passe ces tokens dans dataset_prediction()
# 5) On obtient grâce à calculate_result() les pourcentages de tweets positifs et négatifs.

# MAIN FUNCTIONS:
# 1- tokenize_tweets(data)
# 2- calculate_result(result)
# 3- dataset_prediction(tokens)

# EXTRA FUNCTIONS:
# 1- predict_this(str)
# 2- most_common_words(tokens, n)


################# MAIN FUNCTIONS ################

# Transforme nos tweets en tokens (nettoyés avec un combo preprocess() + filter_stopwords())

def tokenize_tweets(data):
    data_length = len(data)
    tokens = []
    for i in range(data_length):
        tweet = data[i]['text']
        tokens.append(filter_stopwords(preprocess(tweet)))
    return tokens


# Traduction des prédictions en pourcentage :

def calculate_result(result, plot=False):
    neg = 0
    pos = 0
    for i, j in enumerate(result):
        if result[i].item() == 1:
            pos += 1
        else:
            neg += 1
    all_res = len(result)
    pos_tweets = (pos / all_res) * 100
    neg_tweets = (neg / all_res) * 100
    print("PREDICTION PERCENTAGES:")
    print("Positive: %.2f%%" % pos_tweets)
    print("Negative: %.2f%%" % neg_tweets)

    # Si on veut un pie chart en plus :
    if plot:
        plt.pie([pos_tweets, neg_tweets],
                labels=['Positive tweets', 'Negative tweets'],
                colors=['limegreen', 'crimson'],
                startangle=90,
                autopct='%1.1f%%')
        plt.title('Sentiment analysis:')
        plt.show()
    return pos_tweets, neg_tweets


# Prédictions sur une liste de tokens,
# on va se servir des tokens qu'on a récupéré dans notre corpus json avec tokenize_tweets()

def dataset_prediction(tokens):
    tokens = np.array(tokens, dtype=object)
    print("\nAnalyzing sentiments...")
    query_vec = np.concatenate([build_word_vector(w2v_model, tfidf, t, N_DIM) for t in tqdm(map(lambda x: x, tokens))])
    result = model.predict_classes(query_vec)
    pos_tweets, neg_tweets = calculate_result(result, False)  # False si on ne veut pas de pie chart
    return pos_tweets, neg_tweets


################# EXTRA FUNCTIONS ################

# Prédiction d'une chaîne (voir tests.py pour des tests) :

def predict_this(str):
    query_tokens = preprocess(str)
    query_vec = build_word_vector(w2v_model, tfidf, query_tokens, N_DIM)
    result = model.predict_classes(query_vec).item()
    if result == 1:
        result_polarity = "Positive"
        return f'{result_polarity}: {str}'
    else:
        result_polarity = "Negative"
        return f'{result_polarity}: {str}'


# predict_this("I'm tired because my computer is so slow and old, ugh")


# Si on veut connaître les N mots les plus communs dans notre corpus
# (Penser à ajouter les stopwords dans la stoplist de filter.py si on ne veut pas les voir)

def most_common_words(tokens, n):
    tf = Counter()
    for t in range(len(tokens)):
        tf.update(tokens[t])
    print(f"{n} most common words in corpus:")
    for tag, count in tf.most_common(n):
        print(f"{tag}: \t{count}")
