import os
import requests
from time import sleep
from bs4 import BeautifulSoup

def onsen_data():
  with open('onsen_list.tsv', mode='r') as f:
    for line in f.readlines():
      data = line.split('\t')
      name, url, detail = data[0], data[1], data[2].rstrip()
      yield name, url, detail

def get_parsed_html(url):
  user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
  headers = {'User-Agent': user_agent}
  r = requests.get(url, headers=headers)
  if r.status_code != 200:
    return None
  return BeautifulSoup(r.text, 'html.parser')

def get_reviews(base_url):
  i = 1
  while True:
    sleep(0.2)
    url = f'{base_url}/kuchikomi'
    if i > 1:
      url = f'{url}?&page={i}'
    soup = get_parsed_html(url)
    if soup is None:
      i += 1
      break
    reviews = soup.find_all('p', {'class': 'review-area__text'})
    if len(reviews) == 0:
      break
    for review in reviews:
      review = review.text.strip().replace('\n', '').replace('\t', '')
      if len(review) > 0:
        yield review
    i += 1

if not os.path.exists('data'):
  os.mkdir('data')
for name, url, detail in onsen_data():
  sleep(0.5)
  try:
    with open(f'data/{name}.txt', mode='w') as f:
      f.write(detail + '\n')
      for review in get_reviews(url):
        f.write(review + '\n')
    print('processed ' + name)
  except:
    print('error at ' + name)