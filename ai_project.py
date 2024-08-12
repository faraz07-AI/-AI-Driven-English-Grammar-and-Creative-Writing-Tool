# -*- coding: utf-8 -*-
"""AI_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16LEG5hevjKIJab9zpMfqc8zi88DwW22-

Author_1: Faraz Gurramkonda

Author_2: Kritika sharma

Artificial Intelligence

Final Project on NLP Techniques of English Language
"""

import gensim
from gensim.models import Word2Vec, KeyedVectors
import pandas as pd

# Import train_rel_2.tsv into Python
with open('/content/Train_data.txt', 'r') as f:
    lines = f.readlines()
    columns = lines[0].split('\t')
    response = []
    for line in lines[1:]:
        temp = line.split('\t')
        print(temp)
        response.append(temp[-1])  # Select "EssayText" as a corpus

# Construct a dataframe ("data") which includes only response column
data = pd.DataFrame(list(zip(response)))
data.columns = ['response']
print(data)

data.response[0]

new_response =data.response.apply(gensim.utils.simple_preprocess)
new_response

model=gensim.models.Word2Vec(window=5, min_count=2, workers=4, sg=0)
model.build_vocab(new_response, progress_per=1000)
model.train(new_response, total_examples=model.corpus_count, epochs=model.epochs)
model.save("./respon.model")

model.wv["critical"]

from scipy.spatial.distance import cosine

import math
import numpy as np

with open("/content/drive/MyDrive/src6/vectors/words.txt") as f:
    words = dict()
    for line in f:
        row = line.split()
        word = row[0]
        print(word)
        print("printing row:",row[1:])
        vector = np.array([float(x) for x in row[1:]])
        words[word] = vector


def distance(w1, w2):
    return cosine(w1, w2)


def closest_words(embedding):
    distances = {
        w: distance(embedding, words[w])
        for w in words
    }
    return sorted(distances, key=lambda w: distances[w])[:10]


def closest_word(embedding):
    return closest_words(embedding)[0]

print(distance(words["book"],words["library"]))

print(closest_words(words["book"])[:10])

print(closest_words(words["king"]- words["man"]+ words["woman"])[:1])

import nltk
nltk.download('punkt')

import nltk



def main():

    # Read data from files


    directory_name = input("enter the directory_name:")
    positives, negatives = load_data(directory_name)

    # Create a set of all words
    words = set()
    for document in positives:
        words.update(document)
    for document in negatives:
        words.update(document)

    # Extract features from text
    training = []
    training.extend(generate_features(positives, words, "Positive"))
    training.extend(generate_features(negatives, words, "Negative"))

    # Classify a new sample
    classifier = nltk.NaiveBayesClassifier.train(training)
    s = input("s: ")
    result = (classify(classifier, s, words))
    for key in result.samples():
        print(f"{key}: {result.prob(key):.4f}")


def extract_words(document):
    return set(
        word.lower() for word in nltk.word_tokenize(document)
        if any(c.isalpha() for c in word)
    )


def load_data(directory):
    result = []
    directory = "/content/drive/MyDrive/src6/sentiment/"+ directory
    for filename in ["positives.txt","negatives.txt"]:
        with open(directory+"/"+filename) as f:
            result.append([
                extract_words(line)
                for line in f.read().splitlines()
            ])
    return result


def generate_features(documents, words, label):
    features = []
    for document in documents:
        features.append(({
            word: (word in document)
            for word in words
        }, label))
    return features


def classify(classifier, document, words):
    document_words = extract_words(document)
    features = {
        word: (word in document_words)
        for word in words
    }
    return classifier.prob_classify(features)


if __name__ == "__main__":
    main()

pip install markovify

from collections import Counter

import math
import nltk



def main():
    """Calculate top term frequencies for a corpus of documents."""


    print("Loading data...")

    n = int(input("number of ngrams:"))
    data_choosen = input("enter the doirectory file to be loaded:")
    corpus = load_data(data_choosen)

    # Compute n-grams
    ngrams = Counter(nltk.ngrams(corpus, n))

    # Print most common n-grams
    for ngram, freq in ngrams.most_common(10):
        print(f"{freq}: {ngram}")


def load_data(directory):
    contents = []

    # Read all files and extract words
    directory  = "/content/drive/MyDrive/src6/ngrams/" + directory
    for filename in ["bachelor.txt","blaze.txt","blaze.txt","bohemia.txt","boscombe.txt","carbuncle.txt","clerk.txt","copper.txt","coronet.txt","engineer.txt","face.txt","gloria_scott.txt","interpreter.txt","league.txt","patient.txt","problem.txt","ritual.txt","speckled.txt","squires.txt","treaty.txt","twisted.txt"]:
        with open(directory + "/" +filename) as f:
            contents.extend([
                word.lower() for word in
                nltk.word_tokenize(f.read())
                if any(c.isalpha() for c in word)
            ])
    return contents

# /content/drive/MyDrive/src6/ngrams/holmes
if __name__ == "__main__":
    main()

import markovify

# /content/drive/MyDrive/src6/markov/shakespeare.txt
directory = "/content/drive/MyDrive/src6/markov/"
filename = input("please enter the file name:")
path = directory + filename
with open(path) as f:
    text = f.read()

# Train model
text_model = markovify.Text(text)

# Generate sentences
print()
for i in range(10):
    print(text_model.make_sentence())
    print()

import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP

    NP -> D N | N
    VP -> V | V NP

    D -> "the" | "a"
    N -> "she" | "city" | "car"
    V -> "saw" | "walked"
""")

parser = nltk.ChartParser(grammar)

sentence = input("Sentence: ").split()
try:
    for tree in parser.parse(sentence):
        tree.pretty_print()
except ValueError:
    print("No parse tree possible.")

import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP

    AP -> A | A AP
    NP -> N | D NP | AP NP | N PP
    PP -> P NP
    VP -> V | V NP | V NP PP

    A -> "big" | "blue" | "small" | "dry" | "wide"
    D -> "the" | "a" | "an"
    N -> "she" | "city" | "car" | "street" | "dog" | "binoculars"
    P -> "on" | "over" | "before" | "below" | "with"
    V -> "saw" | "walked"
""")

parser = nltk.ChartParser(grammar)

sentence = input("Sentence: ").split()
try:
    for tree in parser.parse(sentence):
        tree.pretty_print()
except ValueError:
    print("No parse tree possible.")