import json
import pickle
import numpy as np

import nltk
from nltk.corpus import stopwords

from keras.preprocessing.text import Tokenizer
from keras_preprocessing.sequence import pad_sequences

# Create Corupus
corpus = []
output = []

# Punctuation
PUNCTUATION = ["?", ",", "!", "_", "."]

# Load Data
data = json.loads(open('data\data.json').read())

# Loop through each data object
for i in data:
    # Remove Stopwords
    text = nltk.word_tokenize(i["text"].lower())
    stop_words = set(stopwords.words('english'))
    text = [word for word in text if word.isalpha() and not word in stop_words]
    finText = ' '.join(text)

    # Add to Corpus & Output
    corpus.append(finText)

    # Fit output data
    outbuf = []
    outbuf.append(i["output"]["fzness"])
    outbuf.append(i["output"]["flness"])
    outbuf.append(i["output"]["intrest"])
    outbuf.append(i["output"]["confidence"])
    outbuf.append(i["output"]["coolness"])
    output.append(np.array(outbuf))

# Create Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus)
sequences = tokenizer.texts_to_sequences(corpus)
padded_sequences = pad_sequences(sequences, maxlen=4)

print(output)

pickle.dump(corpus, open("data/pickle/corpus.pkl", "wb"))
pickle.dump(sequences, open("data/pickle/sequences.pkl", "wb"))
pickle.dump(padded_sequences, open("data/pickle/xTrain.pkl", "wb"))
pickle.dump(output, open("data/pickle/yTrain.pkl", "wb"))