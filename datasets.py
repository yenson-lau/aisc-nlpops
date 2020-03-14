import os, tarfile
from easydict import EasyDict as edict
from linereader import dopen
from random import randint
from torch.utils.data import Dataset, DataLoader
from urllib import request


class GigaWord(Dataset):
  def __init__(self, directory='data/sumdata/train', split='train'):
    super(GigaWord, self).__init__()

    self.split = split
    self.directory = directory
    if split=='train':
      self.fileNames = ('train.article.txt', 'train.title.txt')
    else:
      self.fileNames = ('valid.article.filter.txt', 'valid.title.filter.txt')

    self.inFile = dopen(os.path.join(directory, self.fileNames[0]))
    self.tgtFile = dopen(os.path.join(directory, self.fileNames[1]))
    self._len_ = None

  def __len__(self):
    if self._len_ is None:
      with open(os.path.join(self.directory, self.fileNames[0]),'r') as f:
        for i, l in enumerate(f,1): pass
        if l=='':  i -= 1
      self._len_ = i

    return self._len_

  def __getitem__(self, idx):
    idx += 1
    return (self.inFile.getline(idx).strip(),
            self.tgtFile.getline(idx).strip())


class CNNDailyMail(Dataset):
  def __init__(self, directory='data/cnndm', split='train'):
    self.directory = directory
    self.split = split

    self.fnames = edict(src=None, tgt=None)
    self.files = edict(src=None, tgt=None)
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
    self.files = edict({k: dopen(fp) for k, fp in self.fpaths.items()})

    # Get dataset length
    with open(self.fpaths.tgt,'r') as f:
      for self.len, l in enumerate(f,1): pass
      if l=='':  self.len -= 1

  def __len__(self):
    return self.len

  def __getitem__(self, idx):
    idx += 1
    out = edict({k: f.getline(idx).strip() for k, f in self.files.items()})
    return out