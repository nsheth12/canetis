# Canetis

Canetis is a recursive forced aligner built on Gentle. On particularly long and/or noisy audio files, 
small errors have the potential to accumulate within forced aligners such as Gentle. In order to
resolve this issue, our aligner implements the recursive algorithm described by Moreno et al. in the paper [“A Recursive Algorithm for the Forced Alignment of Very Long Audio Segments”](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.649.6346&rep=rep1&type=pdf).

This paper proposes the creation of these so-called “anchor points” of consecutively aligned words. A stretch of audio is an anchor point if it contains N number of 
consecutive correctly aligned words. The aligner then continues to run recursively in the space between these anchor points until no further improvements can be attained.

<p align="center">
  <img src="pictures/AnchorPoints.png" width="350"/>
  <br>
  The larger the N, the more accurate the model will be. The smaller the N, the faster the model will be.
</p>

With these anchor points having been located, our wrapper will then run Gentle recursively on each individual non-anchored 
section of audio. This isolation of non-aligned clips should in general reduce the number of errors in alignment, as well as increase
the total number of aligned words. 

## Installation Process

**Dependencies**

1. Python 2
2. Pip

**Install**

Clone the source onto your machine. `cd` into the `canetis` directory and run the following:
```bash
sudo ./install.sh
source ~/.profile
```

This will install all required dependencies, install Canetis, and perform required configuration.

## Usage

```bash
python2 align.py audio.wav transcript.txt output.txt
```

Puts a JSONified dictionary into the output.txt file, containing the following keys:
1. "start" - the start audio time
2. "end" - the end audio time
3. "word" - the word
4. "success" - whether the word was successfully aligned or not

## Contributors

This project was created by [Nihar Sheth](http://github.com/nsheth12) and [Kian Ghodoussi](http://github.com/ghodouss).
