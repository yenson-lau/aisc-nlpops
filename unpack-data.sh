#/bin/sh

cd data
tar -xvf summary.tar.gz
cd sumdata/train
gzip -d *.gz
