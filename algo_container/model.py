import warnings
warnings.filterwarnings('ignore', category=FutureWarning)

import pandas as pd
from tqdm import tqdm
tqdm.pandas(desc="progress-bar")
pd.options.mode.chained_assignment = None
import numpy as np
import re

import gensim
from gensim.models.word2vec import Word2Vec

import nltk
from nltk.tokenize import TweetTokenizer
nltk.download('omw-1.4', quiet=True)
nltk.download('wordnet', quiet=True)
from nltk.stem import WordNetLemmatizer

from algo_container.tfidf import load_tfidf
from algo_container.utils import load_modeljson

# ceci nous permet de nous débarrasser des warnings de dépreciation
import logging, os
logging.disable(logging.WARNING)
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"


###################################################
#                                                 #
#               TOKENIZING TWEETS                 #
#                                                 #
###################################################

# On va transformer chaque tweet en tokens, on en profite pour virer ce qui nous intéresse pas
# en utilisant regex : les urls et les mentions

# Notez que je ne filtre pas les stopwords ici, j'ai remarqué que cela baissait les performances de mon modèle,
# ce qui est normal puisque si je prends les phrases "i am happy" et "i am not happy" et que je vire "not" qui
# fait partie des stopwords, les 2 phrases pourtant opposées prennent alors le même sens.

# Enfin notons que je garde aussi les hashtags parce qu'ils sont très souvent utilisés pour rajouter du sens
# et du contexte à un tweet, par exemple: "Donald did what? #idiot #demon #theworst" ou même "cats are the #greatest".

def preprocess(tweet):

    # Tokenize les tweets :
    tknzr = TweetTokenizer(preserve_case=False)
    tokens = tknzr.tokenize(tweet)

    # Vire les tokens qu'on ne veut pas garder :
    url = re.compile('https?://[A-Za-z0-9./]+')  # url
    mention = re.compile('@(\w+)')   # mentions
    tokens = [t for t in tokens if not url.search(t)]
    tokens = [t for t in tokens if not mention.search(t)]
    tokens = [t for t in tokens if not t.isdigit()]  # on vire les nombres

    # OPTION : Vire les lettres qui se répètent dans un mot, dans la limite de 2 lettres
    # (loveeee => lovee), on limite à 2 sinon on aura un souci avec les mots comme
    # "good" qui deviendrait "god" et prendrait un tout autre sens
    #tokens = [re.sub(r'(.)\1{2,}', r'\1\1', t) for t in tokens]

    # La lemmatization marche très bien avec Word2vec par rapport au stemming
    # Dans mon cas ça ne me permet pas d'améliorer mes performances de façon importante
    # mais ça me permet de réduire la taille de mon vocabulaire
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]

    return tokens


# Transforme chaque tweet de notre corpus (ici 1,6M) en tokens avec la fonction précédente preprocess()

def postprocess(data, n=1600000):
    data = data.head(n).copy(deep=True)
    data['tokens'] = data['text'].progress_map(preprocess)
    return data


# W2V MODEL CONFIG:

N_DIM = 300  # dimension du vecteur de mot

###################################################
#                                                 #
#             SAVING/LOADING W2V MODEL            #
#                                                 #
###################################################

# Charge le modèle W2v sur l'ordinateur

def load_w2vmodel(filename):
    print("Loading the W2V model from disk...")
    return gensim.models.Word2Vec.load(filename)


###################################################
#                                                 #
#            WORD VECTOR CONSTRUCTION             #
#                                                 #
###################################################

# Construction des vecteurs des mots à partir d'une liste de mots (les tokens des tweets)
# et la dimension du vecteur, on multiplie ensuite chaque terme du vecteur W2V avec
# son importance dans TFIDF. Ce dernier point me permet de bien améliorer la performance du modèle.

def build_word_vector(w2v_model, tfidf, tokens, size):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in tokens:
        try:
            vec += w2v_model.wv[word].reshape((1, size)) * tfidf[word]
            count += 1.
        except KeyError:
            continue
    if count != 0:
        vec /= count
    return vec


def load_models(model_config_path, model_weights_path, w2v_path, tfidf_path):
    try:
        model = load_modeljson(model_config_path, model_weights_path)
        w2v_model = load_w2vmodel(w2v_path)
        tfidf = load_tfidf(tfidf_path)
        return model, w2v_model, tfidf
    except FileNotFoundError:
        exit('No model found.\nPlease run the engine first or make sure you have the right path.')


model, w2v_model, tfidf = load_models('./model_config.json', './model_weights.h5',
                                      './my_w2vmodel', './tfidf.pickle')


