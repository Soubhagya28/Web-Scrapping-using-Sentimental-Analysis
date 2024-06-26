# -*- coding: utf-8 -*-
"""Sentimental Analysis 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pVWl7JG89dpqkrvDdgPUOYp1lpOlYSGu
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import bs4
import textblob
import re

api = requests.get("https://www.zdnet.com/article/what-is-ai-heres-everything-you-need-to-know-about-artificial-intelligence/")

from bs4 import BeautifulSoup

content = BeautifulSoup(api.content, 'lxml')
content = content.getText(strip=True)

content

!pip install nltk
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.probability import FreqDist
!python3 -m nltk.downloader averaged_perceptron_tagger
from nltk import pos_tag

sentence = sent_tokenize(content)

len(sentence)

from textblob import TextBlob

# Calculation positive, negative, polarity of words
def analyze_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

sentence = pd.DataFrame(sentence)
sentence.columns = ['sentence']
sentence['sentiment'] = [str(analyze_sentiment(x)) for x in sentence.sentence]
sentence.sentiment.value_counts()

content_words=word_tokenize(content)
content_words=[word for word in content_words if word.isalnum()]

stop_words = set(stopwords.words('english'))
content_words = [word for word in content_words if not str.lower(word) in stop_words]

wordfreq = FreqDist(content_words)
print(wordfreq)

# Calculation average length
word_length = []
for word in content_words:
  word_length.append(len(word))
average_length = (sum(word_length)/len(word_length))
print(round(average_length))

# Calculation average_sentence_length
average_sentence_length = len(content_words) / len(sentence)
print(round(average_sentence_length))

!pip install syllables
import syllables

# Calculate syllables_per_word
total_syllables = 0
total_words = len(content_words)
for word in content_words:
      total_syllables += syllables.estimate(word)
syllables_per_word = total_syllables / total_words
print(syllables_per_word)

#calculate average words per sentence
avg_words_per_sentence = total_words / len(sentence)
print(avg_words_per_sentence)

#calculate total complex words
total_complex_words = 0
for word in content_words:
  if syllables.estimate(word)>=3:
    total_complex_words += 1
print(total_complex_words)

# Calculate percentage of complex words
if total_words > 0:
    percentage_complex_words = (total_complex_words / total_words) * 100
else:
    percentage_complex_words = 0
print(percentage_complex_words)

# Calculate subjectivity score
blob = TextBlob(content)
subjectivity_score = blob.sentiment.subjectivity
print(subjectivity_score)

# Calculate personal pronouns
tagged_words = pos_tag(content_words)
personal_pronouns = ["I", "me", "my", "mine", "myself", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "we", "us", "our", "ours", "ourselves", "they", "them", "their", "theirs", "themselves"]
personal_pronoun_count = sum(1 for word, pos in tagged_words if word.lower() in personal_pronouns)
print(personal_pronoun_count)

#calculate fog index
fog_index = 0.4 * (avg_words_per_sentence + percentage_complex_words)
print(fog_index)

