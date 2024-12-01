import os
from collections import defaultdict
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def create_inverted_index(folder_path):
    stop_words = set(stopwords.words("english"))
    inverted_index = defaultdict(list)
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            words = word_tokenize(text.lower())
            words = [word for word in words if word.isalnum() and word not in stop_words]
            
            for word in set(words):
                inverted_index[word].append(file_name)
    
    return inverted_index
