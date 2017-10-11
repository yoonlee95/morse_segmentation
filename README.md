# MORpheme SEgment-er

Multi-language full pipeline of MORpheme Segementor based on [1]

## Requirement

**System Requirement**

Linux enviorment with

1. CUDA enabled GPU
2. Recommended 32GB or more of RAM

**Dependencies**

* wget
* cuda
* python2.7

    1. [numpy](http://www.numpy.org/)
    2. [gensim](https://radimrehurek.com/gensim/)
    3. [pycuda](https://documen.tician.de/pycuda/)

    Run `suda pip install -r requrements.txt`    

## How to use

### Training

Run `python main.py` with the following arguments. Values from `default-config.json` will be used if argument is not given.

```
train.py
  FASTTEXT MODEL mode(default mode):
  -l <input language>       Language to run Morse Segmentation
  
  External MODEL Mode(when <external mode> is used)
  -e <external model dir>   Directory of the external model
  -t <model type>           model to load the external model (<fasttext> or <word2vec>)
  
  General Configuations:
  -b <batch size>           Number of words to segment from model( -1 for full dataset)
  -p <partition size>       Number of words to group as a partition( -1 for no partition)
  
  -m  <external mode>       <True> or <False> value if external model is going to be used
  
  Output Directories:
  -s <ss, score directory>  Output directory for the  support set and scores
  -o <model output dir>     Output directory for the model
  
  PREFIX Rules:
  --pw <base word>           Minimum length of a word
  --pe <edit distance>       Maximum edit distance a word can have beween another word in a SS
  
  SUFFIX Rules:
  --sw <base word>           Minimum length of a word
  --se <edit distance>       Maximum edit distance a word can have beween another word in a SS

```
#### example

`python train.py -l korean -b 500000 -s korean_500k -o korean_model --pw 1 --pe 2 --sw 1 --se 3`

#### Output

* **Output Model** in `model output directory`

* **10 types of files** in `ss score directory`.

    * **[PRE + SUF]__ss_[0-9]** - Contains Support sets
    * **[PRE + SUF]__w_sem_[0-9]**, **[PRE + SUF]__loc_sem_[0-9]**, **[PRE + SUF]__r_sem_[0-9]** and **[PRE + SUF]__r_orth_[0-9]** - Contains Scores calculated described in [1] 



**Notes**
* Currently only support word2vec mode ( python fasttext needs to be updated)
* You should consider to use smaller partition_size if you want to run a bigger number of words
* Pre-Trained language are downloaded from https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md 
* With 16GB of RAM you should be able run a batch size of 1M (Can vary with base word and edit distance).

----

### Inference

run `python MORSE.py` with the arguments [**model_dir**,**input.txt**,**output.txt**]

#### example

`python MORSE.py ../english_output input.txt output.txt`



## Reference

[1] Tarek Sakakini, Suma Bhat, Pramod Viswanath, [MORSE: Semantic-ally Drive-n MORpheme SEgment-er](https://arxiv.org/abs/1702.02212)
 
## Authors

* **Jong Yoon Lee(UIUC)** - jlee642@illinois.edu

Supervised By
* **Tarek Sakakini(UIUC)** - sakakini@illinois.edu
