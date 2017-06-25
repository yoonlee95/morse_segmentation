# MORpheme SEgment-er

Multi-language full pipeline of MORpheme Segementor based on [1]

## Requirement

**System Requirement**

Linux enviorment with

1. NVIDIA GPU
2. Recommended 32GB or more RAM

**Dependencies**

* wget
* cuda
* python2.7

    1. [numpy](http://www.numpy.org/)
    2. [gensim](https://radimrehurek.com/gensim/)
    3. [pycuda](https://documen.tician.de/pycuda/)
    
    Can be installed with pip `sudo pip install --upgrade numpy gensim pycuda`

## How to use

Run `python main.py` with the following arguments. Values from `default-config.json` will be used if argument is not given.

```
main.py
 -l <input language>       Language to run morse segmentation on
 -b <batch size>           Number of words to segment from model( -1 for full dataset)
 -p <partition size>       Number of words to group as a partition( -1 for no partition)
 -m <mode>                 Segment type (<SUFFIX> or <PREFIX>)
 -t <model type>           Select mode (<fasttext> or <word2vec>)
 -o <output directory>     Output directory
 -w <base word>            Minimum length of a word
 -e <edit distance>        Maximum edit distance a word can have beween another word in a SS""" 


```
### example


`python main.py -l korean -b 1000000 -p -1 -m SUFFIX -t word2vec -o korean_1m -w 1 -e 3`
### Output

**In total 10 types of files**

* **[PRE + SUF]_ss_[0-9]** - Contains Support sets
* **[PRE + SUF]_w_sem_[0-9]**, **[PRE + SUF]_loc_sem_[0-9]**, **[PRE + SUF]_r_sem_[0-9]** and **[PRE + SUF]_r_orth_[0-9]** - Contains Scores calculated described in [1] in your `output directory`.

**Notes**
* Currently only support word2vec mode ( python fasttext needs to be updated)
* You should consider to use smaller partition_size if you want to run a bigger number of words
* Pre-Trained language are downloaded from https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md 
* With 16GB of RAM you should be able run a batch size of 1M (Can vary with base word and edit distance).

## Reference

[1] Tarek Sakakini, Suma Bhat, Pramod Viswanath, [MORSE: Semantic-ally Drive-n MORpheme SEgment-er](https://arxiv.org/abs/1702.02212)
 
## Authors

* **Jong Yoon Lee(UIUC)** - jlee642@illinois.edu

Supervised By
* **Tarek Sakakini(UIUC)** - sakakini@illinois.edu
