# How to get GigaWords dataset

- Download `summary.tar.gz` [from here](https://drive.google.com/file/d/0B6N7tANPyVeBNmlSX19Ld2xDU1E/view) to the `data` directory
- Run `unpack-data.sh`
- Make sure your Python environment has the packages from `requirements.txt` installed
    - e.g. run `pip install -r requirements.txt`
- In Python, run `from datasets import GigaWords`

Then you can just create the dataset:
```
from datasets import GigaWords

ds = GigaWords(split='valid')  # 'train' or 'valid'
print(ds[0])
print(len(ds))
```