import operator

import nltk
import matplotlib.pyplot as plt
import numpy as np
# nltk.download()
from nltk.book import *
from nltk.corpus import brown

#%%
text1.concordance()
text1.similar()
text1.common_contexts()
text1.dispersion_plot()

#hapaxes - unique words

list(bigrams(['more', 'is', 'said', 'than', 'done']))

#collocations - словосочетание

text1.collocations()

#%%
nltk.chat.chatbots()

nltk.Text

#%%
for fileid in gutenberg.fileids():
    num_chars = len(gutenberg.raw(fileid))
    num_words = len(gutenberg.words(fileid))
    num_sents = len(gutenberg.sents(fileid))
    num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
    print(round(num_chars/num_words, 2), round(num_words/num_sents, 2), round(num_words / num_vocab, 2), fileid)

#%%
cfd = nltk.ConditionalFreqDist((genre, word) for genre in brown.categories() for word in brown.words(categories=genre))
genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']

cfd.tabulate(conditions=genres, samples=modals)

#%%
cfd = nltk.ConditionalFreqDist(
    (target, fileid[:4])
    for fileid in inaugural.fileids()
    for w in inaugural.words(fileid)
    for target in ['america', 'citizen', 'freedom']
    if w.lower().startswith(target)
)

#%%
genre_word = [(genre, word)
              for genre in ['news', 'romance']
              for word in brown.words(categories=genre)]

#%%
from nltk.corpus import brown
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
genres = ["news", "romance"]
cfd = nltk.ConditionalFreqDist(
    (genre, day)
    for genre in genres
    for day in brown.words(categories=genre)
    if day in days

)

#%%
sent = ['In', 'the', 'beginning', 'God', 'created', 'the', 'heaven', 'and', 'the', 'earth', '.']

#%%
def generate_model(cfdist, word, num=15):
    for i in range(num):
        print(word, end = ' ')
        word = cfdist[word].max()

#%%
text = nltk.corpus.genesis.words('english-kjv.txt')
bigrams = nltk.bigrams(text)
cfd = nltk.ConditionalFreqDist(bigrams)

#%%
def unusual_words(text):
    text_vocab = set(w.lower() for w in text if w.isalpha())
    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
    unusual = text_vocab - english_vocab
    return sorted(unusual)

#%%
unusual_words(nltk.corpus.gutenberg.words('austen-sense.txt'))

#%%
def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('english')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content) / len(text)

#%%
puzzle_letters = nltk.FreqDist('egivrvonl')
obligatory = 'r'
wordlist = nltk.corpus.words.words()
[w for w in wordlist if len(w) >= 8 and obligatory in w and nltk.FreqDist(w) <= puzzle_letters]

#%%
names = nltk.corpus.names
male_names = names.words('male.txt')
female_names = names.words('female.txt')
[w for w in male_names if w in female_names]

#%%
cfd = nltk.ConditionalFreqDist(
    (fileid, name[-1])
    for fileid in names.fileids()
    for name in names.words(fileid)
)
cfd.plot()
plt.show()
cfd.tabulate()

#%%
from nltk.corpus import swadesh

#%%
from nltk.corpus import wordnet as wn
motorcar = wn.synset('car.n.01')
types_motorcar = motorcar.hyponyms()
sorted(lemma.name() for synset in types_motorcar for lemma in synset.lemmas())

#%%
motorcar.hypernym_paths()

#%%
motorcar.root_hypernyms()

#%%
motorcar.part_meronyms()

#%%
both_ = '''
Vengeance ruled his day and nights.An infamous sea captain of the British
 Royal Navy, Devlin O’Neill is consumed with the need to destroy the man
  who brutally murdered his father. Having nearly ruined the Earl of Eastleigh
   financially, he is waiting to strike the final blow. And his opportunity comes
    in the form of a spirited young American woman, the earl’s niece, who is about
     to set his cold, calculating world on fire.Pride inflamed her spirit.Born and
      raised on a tobacco plantation, orphan Virginia Hughes is determined 
to rebuild her beloved Sweet Briar. Daringly, she sails to England alone,
 hoping to convince her uncle to lend her the funds. Instead she finds
  herself ruthlessly kidnapped by the notorious Devlin O’Neill. As his
   hostage, she will soon find her best-laid plans thwarted by a passion
    that could seal their fates forever…Love conquered them both…'''
nltk.word_tokenize(both_)

#%%


#%%
wn.synsets('book')

#%%
wn.synset('book.n.01').definition()
