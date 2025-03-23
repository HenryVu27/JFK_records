import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter

def build_vocab():
    vocab = set()
    data_path = os.path.join(os.path.dirname(__file__), "texts")
    count = 0
    for file in os.listdir(data_path):
        if file.endswith(".txt"): 
            count += 1
            file_path = os.path.join(data_path, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    vocab.update(line.strip().split())
            if count > 50: break
    return vocab

if __name__ == "__main__":
    vocab = build_vocab()
    print(vocab)