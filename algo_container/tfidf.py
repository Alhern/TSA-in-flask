import pickle

###########################################
##########   TF-IDF UTILITIES    ##########
###########################################

# TF-IDF - Term Frequency–Inverse Document Frequency (variante avancée de BoW - Bag of Words)
# Il va s'agir d'évaluer la pertinence (le poids) d'un terme suivant sa fréquence dans le corpus (Term Frequency)
# et le nombre de documents contenant ce terme (Inverse Document Frequency) au sein de ce même corpus.
# Plus un mot est fréquent dans le corpus, plus son poids sera léger. Il en va de même si le mot est très rare.

# Chargement du vecteur TF-IDF à partir de l'ordi

def load_tfidf(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)
