"""
Docstring for cs336_basics.tokenizer

Unicode: maps characters to integer code points, 154998 chars 
ord() -> converts unicode char into integer rep
chr() -> converts code point into a string of char

Unicode encoding for training:
converts unicode char into seq of bytes, w/ UTF-8

Subword tokenization: midpoint between word-level & byte-level tokenizers
Ex: "the" shows up a lot, so it can assume an entry in the vocab,
and this reduces the 3-token seq to a single token
-> to do this, byte-pair encoding:
-iteratively replace/merge the most freq pair of bytes with single, new unused index
The BPE Tokenizer: subword tokenizer with vocabularies constructed from BPE
Training Procedure:
1. Vocab Initialization
-Mapping from bytestring token to integer ID, 256 initial size (8 bytes)
-> 256, and we can combine common ones into different tokens
2. Pre-Tokenization
Count how often pairs of chars appear
use re.finditer()
3. Compute BPE Merges
-Iteratively counts every pair of bytes -> identifies most freq pair
-Merge each occurrence of pair, replaced with new token
-Add new token to vocab
-Total vocab becomes size of initial vocab + # merge operations
-For merges of = freq, use lexiographically greater pair
"""

# 2.1/2.2/2.3
'''
c = chr(97)
print(ord(c))
print(c)
print(f"this is a {c} test")

test = "asdsdfsd"
encode = test.encode("utf-8")
print(list(encode))
'''

# 2.4
import regex as re
import multiprocessing
from collections.abc import Iterable
from collections import defaultdict

PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
file_path_train = "data/TinyStoriesV2-GPT4-train.txt"
file_path_valid = "data/TinyStoriesV2-GPT4-valid.txt"

def max_freq_key(hash):

    max_freq = max(hash.values())

    freq_pairs = [pair for pair, val in hash if val == max_freq]
    
    # Sort in lexiographically highest to lowest
    freq_pairs.sort()
    freq_pairs.reverse()
    return freq_pairs[0]

def train_bpe(input_path: str, vocab_size: int, special_tokens: list[str]):
    """
    Given a path to an input text file, trains a BPE tokenizer.
    Returns:
    - the tokenizer vocab mapping from token ID to bytes
    - list of BPE emrges produced from training. EAch list item is a tuple of bytes (<token1>, <token2>)
        -> ordered by order of creation
    """
    vocab = {}
    merges = []

    # 1. Initialize Vocab: Add special tokens to vocab
    ind = 0
    for special in special_tokens:
        if special not in vocab:
            vocab[ind] = special
            ind += 1

    # Separate by special token and remove trailing whitespace.
    with open(input_path, 'r') as file:
        data = file.read().split('<|endoftext|>')
    data = [d.strip() for d in data]
    
    # 2. Pre-tokenization of each paragraph.
    pre_tokenizer = []
    for d in data:
        pre_tokenizer.append(re.finditer(PAT, d))
    
    i = 1

    # 3. Merges
    """
    TODO(): Get the merging working for one paragraph.
    Merging should continue until either the vocab size is full,
    or the dict has values of all 1's. 
    Additionally, though no merging is taking place between docs,
    THE HASH MERGES_ITER SHOULD HOLD FREQS FOR THE ENTIRE DOC. 
    It can be used to merge for separate cases. 
    
    """
    for encoding in pre_tokenizer[0:2]:
        merges_iter = defaultdict(int)
        prev_token_str = ""
        for token in encoding:
            token_str = token.group(0)
            if prev_token_str != "":
                pair = (prev_token_str, token_str)
                merges_iter[pair] += 1
            prev_token_str = token_str
        
        key_freq = max_freq_key(merges_iter)
        merges.append(key_freq)
        vocab[i + vocab_size] = key_freq
        i += 1
        

            
    return

class Tokenizer:
    def __init__(self, vocab: dict[int, bytes], merges: list[tuple[bytes, bytes]], special_tokens=None):
        self.vocab = vocab
        self.merges = merges
    
    def from_files(cls, vocab_filepath, merges_filepath, special_tokens=None):
        """
        Constructs and returns a Tokenizer from a serialized vocab and list
        of merges, and optionally a list of special tokens.
        """
        return

    def encode(self, text: str):
        """
        Encode an input text into a sequence of token IDs.
        """
        return
    def encode_iterable(self, iterable: Iterable[str]):
        """
        Given an iterbale of strings, return generator that lazily yields token IDs.
        Required for memory-efficient tokenization of large files.
        """
        return
    def decode(self, ids: list[int]):
        """
        Decode sequence of token IDs into text.
        """
        return

vocab_size = 10000
special_tokens = ["<|endoftext|>"]
test = train_bpe(file_path_valid, vocab_size, special_tokens)
print(test)