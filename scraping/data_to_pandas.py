import os
import pandas as pd

df = pd.DataFrame(index=[], columns=['onsen', 'is_review', 'comment'])
for data in os.listdir('data'):
  with open('data/' + data, mode='r') as f:
    for i, line in enumerate(f.readlines()):
      comment = line.strip()
      is_review = i != 0
      row = pd.Series([data.replace('.txt', ''), is_review, comment], index=df.columns)
      df = df.append(row, ignore_index=True)
df.to_pickle('onsen_dataset.pkl')