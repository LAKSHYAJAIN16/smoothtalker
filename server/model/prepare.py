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
data = json.load(open("data\data.json", encoding="utf8"))

# Loop through each data object
for i in data:
    try:

        # Remove Stopwords
        text = nltk.word_tokenize(i["line"].lower())
        stop_words = set(stopwords.words('english'))
        text = [word for word in text if word.isalpha()
                and not word in stop_words]
        finText = ' '.join(text)

        # Add to Corpus & Output
        corpus.append(finText)

        # Fit output data
        outbuf = []
        outbuf.append(i["scores"][0]["outthere"])
        outbuf.append(i["scores"][0]["corn"])
        outbuf.append(i["scores"][0]["weird"])
        outbuf.append(i["scores"][0]["good"])
        output.append(np.array(outbuf))
    except:
        print("One fault")

# Create Tokenizer
tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(corpus)
sequences = tokenizer.texts_to_sequences(corpus)
padded_sequences = pad_sequences(sequences, maxlen=4)

print(output)

pickle.dump(corpus, open("data/pickle/corpus.pkl", "wb"))
pickle.dump(sequences, open("data/pickle/sequences.pkl", "wb"))
pickle.dump(padded_sequences, open("data/pickle/xTrain.pkl", "wb"))
pickle.dump(output, open("data/pickle/yTrain.pkl", "wb"))
