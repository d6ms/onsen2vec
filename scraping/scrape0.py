import requests
from bs4 import BeautifulSoup
from time import sleep


def get_onsen_data(onsen_id):
  url = f'https://www.yukoyuko.net/onsen/{str(onsen_id).zfill(4)}'
  user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
  headers = {'User-Agent': user_agent}
  r = requests.get(url, headers=headers)
  if r.status_code != 200:
    return None, url, None

  soup = BeautifulSoup(r.text, 'html.parser')
  title = soup.find('title').text
  name = title[:title.index('温泉') + 2]

  detail_lead = soup.find('p',{'class': 'onsenDetail_contents_info_lead'}).text
  detail_txt = soup.find('p',{'class': 'onsenDetail_contents_info_txt'}).text
  detail = (detail_lead + '。' + detail_txt).replace('\n', '').replace('\t', '')
  
  return name, url, detail

with open('onsen_list.tsv', mode='w') as f:
  for i in range(2, 2400):
    sleep(0.5)
    try:
      name, url, detail = get_onsen_data(i)
    except:
      print('error at ' + str(i))
      continue
    if name is None:
      continue
    print(name, url, detail)
    f.write(f'{name}\t{url}\t{detail}\n')