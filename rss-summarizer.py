import feedparser
import re, textwrap
from bs4 import BeautifulSoup
from html.parser import HTMLParser
from urllib.request import Request, urlopen
from summa.summarizer import summarize

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.summarizers.lsa import LsaSummarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer
from sumy.summarizers.text_rank import TextRankSummarizer


class TagRemover(HTMLParser):
  def __init__(self):
    super().__init__()
    self.data = ''

  def handle_data(self, data):
    self.data += data

  def parse(self, text):
    self.data = ''
    self.feed(text)
    return self.data

reSubs = [
  (r'\xa0', ' '),    # replace incorrect spaces
  (r'\.\.\.', '…')   # replace '...' with '…'; periods mistaken as a sentence
]


def get_soup(url):
  req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  html = urlopen(req).read().decode('utf8')
  soup = BeautifulSoup(html, 'html.parser')
  return soup

def process_soup(soup, soupTgts, join='\n\n'):
  story = []
  # Add elements from each target to story elements
  for tgt in soupTgts:
    element = soup
    tgt_len = len(tgt)
    for i, query in enumerate(tgt,1):
      if i == tgt_len:
        story += element.find_all(*query)
      else:
        element = element.find(*query)

  for sub in reSubs:
    story = [re.sub(sub[0], sub[1], str(p)) for p in story]
  story = (TagRemover().parse(p) for p in story)
  story = (p.strip() for p in story)
  story = list(story)
  return join.join(story), story

def print_text(text, width):
  for p in text.split('\n'):
    print(textwrap.fill(p, width))

def textrank(text, **kwargs):
  summary = summarize(text, **kwargs)
  summary = re.sub('\n','\n\n', summary)
  return summary

def sumysum(text, SumySummarizer, sentences=5):
  parser = PlaintextParser.from_string(text, Tokenizer("english"))
  summarizer = SumySummarizer()
  summary = summarizer(parser.document, sentences)
  summary = ' '.join(map(str, summary))
  return summary

rss ={
  'cbc-tech': {
    'url': 'https://www.cbc.ca/cmlink/rss-technology',
    'tgts': [ [('div', {'class': 'story'}), ('p',)] ],
  },
  'med-tds': {
    'url': 'https://medium.com/feed/towards-data-science',
    'tgts': [ [('p', {'data-selectable-paragraph': ''})] ],
  }
}

lwid = 70
truncate = lambda t, lim: t if len(t)<=lim else t[:lim-3]+'...'
for k, v in rss.items():
  print('='*lwid)
  print(truncate(f'{k.upper()} - {v["url"]}', lwid-5))
  print('='*lwid)

  feed = feedparser.parse(v['url'])

  for entry in feed.entries[:2]:
    soup = get_soup(entry.link)
    text, story = process_soup(soup, v['tgts'])

    # summary = textrank(text, words=50)
    summary = sumysum(text, TextRankSummarizer, sentences=3)

    print('-'*lwid)
    print(truncate(entry.title, lwid-5))
    print(truncate(entry.link, lwid))
    print('-'*lwid)
    print_text(summary, lwid)
    print('')

  print('')