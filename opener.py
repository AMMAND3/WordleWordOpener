import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
import re
from collections import Counter
from tqdm import tqdm
from pyod.models.copod import COPOD

def read_word_list(file_name:str):
    result = []
    with open(file_name) as fp:
        result.extend([word.strip() for word in fp.readlines()])
    return result


"""create the data into a list for both word lists"""
possible_words_list = read_word_list("possible_answers.txt")
accepted_words_list = read_word_list("accepted_words.txt")

# Create a list of each letter in the alphabet
ALPHABET = list(string.ascii_lowercase)

# Create a letter occurrence dictionary
words_string = ''.join(accepted_words_list)
letter_counts = dict(Counter(words_string))


# Create letter frequency dictionary
letter_frequencies = {k:v/len(accepted_words_list) for k,v in letter_counts.items()}
#letter_frequencies = {k:v/len(accepted_words_list) for k,v in letter_counts.items()}

# Create letter frequency DataFrame
#letter_frequencies = pd.DataFrame({'Letter':list(letter_frequencies.keys()), 'Frequency':list(letter_frequencies.values())}).sort_values('Frequency', ascending=False)
letter_frequencies = pd.DataFrame({'Letter':list(letter_frequencies.keys()), 'Frequency':list(letter_frequencies.values())})
#print(letter_frequencies)

fig,ax = plt.subplots(figsize=(10,6))
bargraph = sns.barplot(x='Letter', y='Frequency', data=letter_frequencies)
#print(type(bargraph))


"""to get the graph"""
figuree = bargraph.get_figure()
#figuree.savefig("outy.png")

letter_freq_cols = []
for letter in ALPHABET:
    for position in range(5):
        letter_freq_cols.append(f'{letter}{position}')


# Create letter/position occurrence matrix
letter_pos_freq = pd.DataFrame()

# For each word in the list of accepted words
for word in tqdm(accepted_words_list):

    # Convert the word to it letter-position format
    word_and_pos = ''.join([f"{letter}{pos}" for pos, letter in enumerate(word)])

    # Create letter-position counter dictionary
    letter_pos_counter = {}
    for wp in letter_freq_cols:
        letter_pos_counter[wp] = len(re.findall(wp, word_and_pos))

    tmp_pos_freq = pd.DataFrame(letter_pos_counter, index=[word])
    letter_pos_freq = pd.concat([letter_pos_freq, tmp_pos_freq])

#letter_pos_freq.head()

letter_pos_freq.to_csv('letter.csv')


#print(type(letter_pos_freq))
#print(letter_pos_freq.index[letter_pos_freq.query('s0 == 1 and o1 == 1 and e4 == 1')]).tolist()

# What's the probability that the fourth letter is 'r' given that the first three letter are 's','h', and 'a'?
#print(letter_pos_freq.query('s0 == 1 and o1 == 1 and e4 == 1').mean())


#print(letter_pos_freq.query('(x0==1 or x1==1 or x2==1 or x3==1 or x4==1) and (y0==1 or y1==1 or y2==1 or y3==1 or y4==1)').index.tolist())
