import sys
import collections
import pandas as pd
from gensim.models.doc2vec import TaggedDocument, Doc2Vec
from gensim.models.callbacks import CallbackAny2Vec

class EpochLogger(CallbackAny2Vec):
  def __init__(self, docs):
    self.epoch = 1
    self.docs = docs
  def on_epoch_begin(self, model):
    print("Epoch #{} start".format(self.epoch))
  def on_epoch_end(self, model):
    ranks = []
    for doc_id in range(len(self.docs)):
      inferred_vector = model.infer_vector(self.docs[doc_id].words)
      sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
      rank = [docid for docid, sim in sims].index(self.docs[doc_id].tags[0])
      ranks.append(rank)
    count = collections.Counter(ranks)
    print(f'top 1 accuracy: {count[0] / len(self.docs)}')
    print(f'top 3 accuracy: {(count[0] + count[1] + count[2]) / len(self.docs)}')
    print(f'top 5 accuracy: {(count[0] + count[1] + count[2] + count[3] + count[4]) / len(self.docs)}')
    print("Epoch #{} end".format(self.epoch))
    self.epoch += 1


def train(docs):
  model = Doc2Vec(vector_size=400, alpha=0.06, sample=1e-4, min_count=1, window=1, workers=4, epochs=30, callbacks=[EpochLogger(docs)], seed=0)
  model.build_vocab(docs)
  model.train(docs, total_examples=model.corpus_count, epochs=model.epochs)
  return model

def train_pretrained(docs, wordvecs):
  model = Doc2Vec(vector_size=400, alpha=0.03, sample=1e-4, min_count=1, window=1, workers=4, epochs=30, callbacks=[EpochLogger(docs)], seed=0, pretrained_emb=wordvecs)
  model.build_vocab(docs)
  model.train(docs, total_examples=model.corpus_count, epochs=model.epochs)
  return model

def save_corpus(train_corpus, name='train_corpus.pkl'):
  df = pd.DataFrame(index=[], columns=['onsen', 'words'])
  for doc in train_corpus:
    row = pd.Series([doc.tags[0], doc.words], index=df.columns)
    df = df.append(row, ignore_index=True)
    df.to_pickle(name)
