# How to get GigaWords dataset

- Download `summary.tar.gz` to the `data` directory
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