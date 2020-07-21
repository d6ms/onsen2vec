import sys
import pandas as pd
from gensim.models.doc2vec import Doc2Vec

model = Doc2Vec.load('onsen2vec.model')
corpus = pd.read_pickle('onsen2vec.corpus')

def search_similar_texts(words):
  x = model.infer_vector(words)
  most_similar_texts = model.docvecs.most_similar([x])
  for similar_text in most_similar_texts:
    print(similar_text)

def search_similar_words(words):
  for word in words:
    print()
    print(word + ':')
    for result in model.wv.most_similar(positive=word, topn=10):
      print(result)

def search_similar_onsen(onsen):
  target = corpus[corpus['onsen'] == onsen]
  if len(target) == 0:
    print('no such onsen in the corpus: ' + onsen)
    return
  words = target.iloc[0]['words']
  search_similar_texts(words)


if __name__ == '__main__':
  word = sys.argv[1]
  search_similar_onsen(word)