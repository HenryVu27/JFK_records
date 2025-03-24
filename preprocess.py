import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")

def build_vocab():
    vocab = Counter()
    data_path = os.path.join(os.path.dirname(__file__), "texts")
    count = 0
    for file in os.listdir(data_path):
        if file.endswith(".txt"): 
            count += 1
            file_path = os.path.join(data_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    vocab.update(line.strip().lower().split())
            if count > 100: break
    return vocab

if __name__ == "__main__":
    vocab = build_vocab()
    # filtered = [word for word in vocab.keys() if word not in nlp.Defaults.stop_words]
    # filtered.sort(key=lambda word: vocab[word], reverse=True)
    
    # zero_count = sum(1 for word in filtered if vocab[word] == 0)
    # print(zero_count)
    # for word in filtered[:5]:
    #     print(f"word {word} with frequency: {vocab[word]}")
    print(vocab["camera"])