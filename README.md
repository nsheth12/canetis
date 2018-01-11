# Echo

Echo is a recursive forced aligner built on Gentle. On particularly long and/or noisy audio files, 
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
2. Pydub - `pip install pydub`
3. Gentle - Instructions available @ https://github.com/lowerquality/gentle

**Install**

Download the source code into a directory. The library will be run directly from the source code.

**Configuration**

Following installation of Gentle, you must also add Gentle to your permanent Python path, and you must add the `gentle` directory within the Gentle installation to the path. To do this, add the following 2 lines to your `.bashrc` file:

```bash
export PYTHONPATH=/path/to/gentle/download:${PYTHONPATH}
export PYTHONPATH=/path/to/gentle/downlaod/gentle:${PYTHONPATH}
```

Then go ahead and open another terminal window or run `source ~/.bashrc` to activative the changes within the current terminal window.

## Usage

```bash
python2 align.py audio.wav transcript.txt
```

Prints out each word in the transcript, whether each word is aligned or unaligned and the start time and end time of each aligned word.

