import os
import sys
import re
import neologdn
import MeCab

def clean(doc):
  doc = doc.rstrip()
  # 各種文字の正規化
  doc = neologdn.normalize(doc)
  # URL文字列の削除
  doc = re.sub(r'(http|https)://([-\w]+\.)+[-\w]+(/[-\w./?%&=]*)?', "", doc)
  return doc



def doc_to_words(doc):
  mecab = MeCab.Tagger("-Ochasen")
  lines = mecab.parse(doc).splitlines()
  words = []
  for line in lines:
    chunks = line.split('\t')
    # 名詞のみを文書の特徴として用いる
    if len(chunks) > 3 and (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数')):
    #and (chunks[3].startswith('動詞') or chunks[3].startswith('形容詞') or (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数'))):
    # and (chunks[3].startswith('名詞') and not chunks[3].startswith('名詞-数')):
      words.append(chunks[0])
  return words

# if not os.path.exists('preprocessed'):
#   os.mkdir('preprocessed')
# with open(filename.replace('extracted/', 'preprocessed/').replace('.txt', '.tsv'), mode='w') as f:
#   for doc in docs:
#     line = '\t'.join(doc_to_words(doc))
#     f.write(line + '\n')

