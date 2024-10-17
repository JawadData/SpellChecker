import os
from model.correction_model import NgramLanguageModel_2

def train_model(input_file):
    model = NgramLanguageModel_2()
    model.train_model(input_file)

    return model

if __name__ == '__main__':
    input_file = 'data/corrections.txt'  
    if not os.path.exists(input_file):
        print(f"Le fichier d'entrée {input_file} n'existe pas. Veuillez fournir un fichier de données d'entraînement.")
    else:
        model = train_model(input_file)
