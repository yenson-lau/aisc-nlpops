import os, re, tarfile
from easydict import EasyDict as edict
from random import randint
from torch.utils.data import Dataset, DataLoader
from urllib import request


def doclen(fpath):
  with open(fpath, 'r') as f:
    for i, l in enumerate(f,1): pass
    if l=='':  i -= 1
    return i

def getlines(fpath, idx, flen=None):
  # This function will not work if idx is a tuple with duplicates

  # convert into a list of indices
  t = type(idx)
  assert t in [int, tuple, slice], 'Index must be an int, tuple, or slice.'

  if t == tuple:  idxs = list(idx)

  if t == int:
    if idx < 0:
      assert (flen is not None), \
        'When using a negative int, file length (flen) must be specified.'
      idx += flen
    idxs = [idx]

  if t == slice:
    assert (flen is not None), \
      'When using a slice, file length (flen) must be specified.'
    idxs = list(range(flen))[idx]

  # create a list of outputs
  out = [None]*len(idxs)
  rem = idxs.copy()
  with open(fpath, 'r') as f:
    for i, l in enumerate(f):
      if i in rem:            # if line in remaining indices
        j = idxs.index(i)     # find corresponding index
        out[j] = l            # update the output
        # idxs[j] = None      # remove from idxs (in case of duplicates)
        rem.remove(i)
      if len(rem)==0: break

  return out[0] if type(idx)==int else out



class GigaWord(Dataset):
  def __init__(self, directory='data/sumdata/train',
               split='train', outFilt=None):
    super(GigaWord, self).__init__()

    self.split = split
    if split=='train':
      self.fpaths = dict(src='train.article.txt', tgt='train.title.txt')
    else:
      self.fpaths = dict(src='valid.article.filter.txt', tgt='valid.title.filter.txt')
    self.fpaths = edict({k: os.path.join(directory, v) for k,v in self.fpaths.items()})
    self.len = doclen(self.fpaths.src)

  def __len__(self):
    return self.len

  def __getitem__(self, idx):
    out = edict({k: getlines(v,idx,self.len) for k,v in self.fpaths.items()})
    return out if (self.outFilt is None) else self.outFilt(out)



class CNNDailyMail(Dataset):
  def __init__(self, directory='data/cnndm', split='train', outFilt=None):
    super(CNNDailyMail, self).__init__()

    self.directory = directory
    self.split = split
    self.outFilt = outFilt

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
          tar.extractall(path=self.directory)

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

  def strip_tags(self, seg, split=False):
    lines = map(lambda l: re.sub('<t>','',l).strip(), seg.split(r'</t>'))
    lines = filter(lambda line: len(line)>0, lines)
    return list(lines) if split else ''.join(lines)

  def __len__(self):
    return self.len

  def __getitem__(self, idx):
    out = edict({k: getlines(v,idx,self.len) for k,v in self.fpaths.items()})
    return out if (self.outFilt is None) else self.outFilt(out)
