import nltk
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
import nltk

import json
import os
import string

lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

def lemmatize_recursive(data):
    if isinstance(data, str):
        palavras = word_tokenize(data)
        lemmatized_words = [lemmatizer.lemmatize(word, get_wordnet_pos(word)) for word in palavras]

        processed_text = ""
        for i, word in enumerate(lemmatized_words):
            if i > 0 and word not in string.punctuation:
                processed_text += " "
            processed_text += word
        return processed_text
    elif isinstance(data, list):
        return [lemmatize_recursive(item) for item in data]
    elif isinstance(data, dict):
        return {key: lemmatize_recursive(value) for key, value in data.items()}
    else:
        return data

def lemmatize_dnd_data_structured(data_type, item_name):
    if data_type == "classe":
        input_path = f"JsonSoup/JsonClasses/{item_name}.json"
        output_dir = "JsonSoup/JsonClasses"
    elif data_type == "raca":
        input_path = f"JsonSoup/{item_name}.json"
        output_dir = "JsonSoup"
    else:
        print("Invalid data_type specified. Use 'classe' or 'raca'.")
        return

    if not os.path.exists(input_path):
        print(f"Input file not found: {input_path}")
        return

    with open(input_path, "r") as f:
        data = json.load(f)

    lemmatized_structured_data = lemmatize_recursive(data)

    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/{item_name}_lemmatized_structured.json", "w") as f:
        json.dump(lemmatized_structured_data, f, indent=4)

    print(f"Structured lemmatization completed for {data_type}: {item_name}")

lemmatize_dnd_data_structured("raca", "dragonborn")
# lemmatize_dnd_data_structured("classe", "wizard")