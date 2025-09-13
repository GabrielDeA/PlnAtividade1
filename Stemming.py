import nltk
nltk.download('punkt_tab')

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

import json
import os
import string

stemmer = PorterStemmer()

def stem_recursive(data):
    
    if isinstance(data, str):
        palavras = word_tokenize(data)
        stemmed_words = [stemmer.stem(word) for word in palavras]

        processed_text = ""
        for i, word in enumerate(stemmed_words):
            if i > 0 and word not in string.punctuation:
                processed_text += " "
            processed_text += word
        return processed_text
    elif isinstance(data, list):
        return [stem_recursive(item) for item in data]
    elif isinstance(data, dict):
        return {key: stem_recursive(value) for key, value in data.items()}
    else:
        return data

def stem_dnd_data_structured(data_type, item_name):
    if data_type == "classe":
        input_path = f"JsonSoup/JsonClasses/{item_name}.json"
        output_dir = "JsonSoup/JsonClasses/stem"
    elif data_type == "raca":
        input_path = f"JsonSoup/JsonRacas/{item_name}.json"
        output_dir = "JsonSoup/JsonRacas/stem"
    else:
        print("Invalid data_type specified. Use 'classe' or 'raca'.")
        return

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    stemmed_structured_data = stem_recursive(data)

    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/{item_name}_stemmed_structured.json", "w") as f:
        json.dump(stemmed_structured_data, f, indent=4)

    print(f"Structured stemming completed for {data_type}: {item_name}")

#stem_dnd_data_structured("raca", "dragonborn")
#stem_dnd_data_structured("classe", "wizard")