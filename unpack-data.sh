#/bin/sh

cd data

# GigaWords
tar -xvf summary.tar.gz --skip-old-files
cd sumdata/train
yes n | gunzip *.gz --keep
cd ../..

# CNN Daily Mail
wget https://s3.amazonaws.com/opennmt-models/Summary/cnndm.tar.gz cnndm.tar.gz -nc
mkdir cnndm | true
tar -xvf cnndm.tar.gz -C cnndm --skip-old-files
rm cnndm.tar.gz
