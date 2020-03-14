import os, tarfile
from easydict import EasyDict as edict
from random import randint
from torch.utils.data import Dataset, DataLoader
from urllib import request


def doclen(fpath):
  with open(fpath, 'r') as f:
    for i, l in enumerate(f,1): pass
    if l=='':  i -= 1
    return i

def getline(fpath, idx):
  with open(fpath, 'r') as f:
    for i, l in enumerate(f):
      if i == idx:  return l
    return None


class GigaWord(Dataset):
  def __init__(self, directory='data/sumdata/train', split='train'):
    super(GigaWord, self).__init__()

    self.split = split
    if split=='train':
      self.fpaths = dict(src='train.article.txt', tgt='train.title.txt')
    else:
      self.fpaths = dict(src='valid.article.filter.txt', tgt='valid.title.filter.txt')
    self.fpaths = edict({k: os.path.join(directory, v) for k,v in self.fpaths.items()})
    self.len = None

  def __len__(self):
    if self.len is None:  self.len = doclen(self.fpaths.src)
    return self.len

  def __getitem__(self, idx):
    return edict({k: getline(v,idx) for k,v in self.fpaths.items()})


class CNNDailyMail(Dataset):
  def __init__(self, directory='data/cnndm', split='train'):
    super(CNNDailyMail, self).__init__()

    self.directory = directory
    self.split = split

    self.fpaths = edict(src=None, tgt=None)
    self.len = None
    self.get_data()

  def get_data(self, split=None):
    if split is not None:  self.split = split

    # Download data if necessary
    if not os.path.isdir(self.directory):
      url = 'https://s3.amazonaws.com/opennmt-models/Summary/cnndm.tar.gz'
      fname = 'cnndm.tar.gz'

      try:
        print(f'Downloading {fname}.')
        request.urlretrieve(url, fname)

        print('Extracting.')
        with tarfile.open(fname, 'r:gz') as tar:
          tar.extractall(path=directory)

        print('Done.', end=' ')

      finally:
        if os.path.isfile(fname):
          print(f'Removing {fname}.')
          os.remove(fname)
    else:
      print('Using existing data.')

    # Get the appropriate files
    self.fpaths = edict(
      src = os.path.join(self.directory, f'{self.split}.txt.src'),
      tgt = os.path.join(self.directory, f'{self.split}.txt.tgt.tagged')
    )

    # Get dataset length
    self.len = doclen(self.fpaths.src)

  def __len__(self):
    return self.len

  def __getitem__(self, idx):
    return edict({k: getline(v,idx) for k,v in self.fpaths.items()})