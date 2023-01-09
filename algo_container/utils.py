import json
from tensorflow.python.keras.models import model_from_json


###########################################
##########    SAVE/LOAD MODEL    ##########
###########################################

# Loading the model configuration and its weights

def load_modeljson(filename, weights):
    with open(filename) as f:
        model = model_from_json(f.read())
        model.load_weights(weights)
    return model


###########################################
######### READ/VALIDATE JSON FILE #########
###########################################

# FUNCTIONS:
# 1- valid_json(file, new_file)
# 2- read_json(file)

# ------------------------------------------

# Le dataset récupéré avec miner.py n'a pas un format json valide,
# le fichier est une suite de listes contenant des chaînes.
# valid_json va transformer ce fichier en fichier json valide.

def valid_json(file):
    new_file = "valid_" + file
    try:
        with open(file) as f, open(new_file, 'w', encoding='utf-8') as valid_file:
            data = json.loads("[" + f.read().replace("}{", "},\n{") + "]")  # magie
            json.dump(data, valid_file, ensure_ascii=False, indent=4)
            print("%s created." % new_file)
    except IOError as e:
        print(f"File not found: {e}")
        return None


# Chargement du fichier json à partir de l'ordi

def read_json(file):
    with open(file, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except ValueError as e:
            print(f"Invalid JSON file: {e}")
            return None
