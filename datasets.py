import os
from linereader import dopen
from random import randint
from torch.utils.data import Dataset, DataLoader


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