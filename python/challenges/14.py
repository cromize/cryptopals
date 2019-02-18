#!/usr/bin/env python3
import sys
import random
import string
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect
from helpers import abort, gen_identical_bytes
from collections import Counter
from base64 import b64decode, b64encode

# we need to somehow align blocks

to_append = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = get_random_bytes(16)

def oracle(plaintext, append, key):
  random_prefix = get_random_bytes(random.randrange(1, 48))
  to_cipher = random_prefix + plaintext + b64decode(append)
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

"""
# byte at a time decryption with an offset
def ecb_crack_block(to_append_plain, blocksize, offset=0):
  matches = "" 
  for i in range(1, blocksize+1):
    # build the dictionary
    sentinel_sled = 4*16*b"a"
    template = gen_identical_bytes(blocksize - i) + matches.encode()
    cipher = oracle(sentinel_sled + template, to_append_plain, key)
    sentinel_idx = find_sentinel(cipher)
    dictionary = make_dictionary(template)

    # sentinel blocks
    print("idx:", sentinel_idx, cipher[16*(sentinel_idx):])
    print("idx:", sentinel_idx-1, cipher[16*(sentinel_idx-1):])
    print("idx:", sentinel_idx-2, cipher[16*(sentinel_idx-2):])
    print()
    
    # match the dictionary
    match = match_dictionary(cipher[16*(sentinel_idx+1):], dictionary)
    print(dictionary)
    try:
      matches += match[-1:]
      print("MATCH")
      print(match.encode("hex"))
      sys.exit(0)
    except Exception:
      pass
  return matches
"""

def make_dictionary(template):
  dictionary = dict()
  for x in range(256):
    cipher = oracle(4*16*b"b" + template + chr(x).encode(), b64decode(to_append), key)
    sentinel_idx = find_sentinel(cipher)
    dictionary[template + chr(x).encode()] = cipher[16*(sentinel_idx+1):16*(1+sentinel_idx+1)]
  return dictionary

def match_dictionary(cipher, dictionary):
  block = cipher[0:16]
  for k, v in dictionary.items():
    if block == v:
      return k.decode()

# find the most common block, get idx and dup. count from that
def find_sentinel(ciphertext):
  cipher_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  counter = Counter(cipher_blocks)
  sentinel_cipher = counter.most_common()[0][0]
  last_sentinel_idx = 0
  for idx, block in enumerate(cipher_blocks):
    if block == sentinel_cipher:
      #print("FOUND")
      #print(block)
      last_sentinel_idx = idx
  
  occurrence = [counter.most_common()[idx][1] for idx in range(len(counter.most_common()))]
  idx_start = 0
  for idx, i in enumerate(occurrence):
    dup_cnt = counter.most_common()[idx][1]
    if idx_start == 0 and idx != 1:
      idx_start = idx
    if (i % 2.0) == 0:
      if dup_cnt >= 32:
        return last_sentinel_idx, dup_cnt, idx - idx_start + 1
      else:
        return last_sentinel_idx, dup_cnt, idx - idx_start + 3
  return None, None, None

def make_offset_sentinel_pattern():
  pattern = b""
  for idx, i in enumerate(range(4, 36, 2)):
    pattern += 16 * i * string.ascii_lowercase[idx].encode() + b"Z"
  return pattern
  
if __name__ == "__main__":
  if len(sys.argv) == 1:
    #sentinel_sled = 4*16*b"a" + b"z" + 6*16*b"b" + b"z" + 8*16*b"c" + b"z" + 10*16*b"d" + b"z"
    sentinel_sled = make_offset_sentinel_pattern()
    #print(len(sentinel_sled))
    #sys.exit(0)
    success_times = 0
    i = 0
    while 1:
      cipher = oracle(sentinel_sled, to_append, key)
      sentinel_idx, dup_cnt, idx_start = find_sentinel(cipher)
      i += 1
      if dup_cnt != None and (dup_cnt % 2) == 0:
        print("aligned sentinel block idx:", sentinel_idx)
        print("align offset in block:", idx_start)
        print(aes_ecb_decrypt(cipher[16*(sentinel_idx+1):16*(sentinel_idx+2)], key)[idx_start:])
        sys.exit(0)
        success_times += 1
        print(f"{success_times}/{i}", "sucess/all,", f"ratio {(success_times/i)*100:.2f}%")

    sys.exit(0)

    #TODO: lets crack tha blooocks
    cracked = ""
    plain_blocks = (b64decode(to_append)[i:i+16] for i in range(0, len(b64decode(to_append)), 16))
    for block in plain_blocks:
      cracked += ecb_crack_block(block, 16, sentinel_idx+1)
    print("cracked:", cracked)
    
  else:
    abort(f'{sys.argv[0]}: filename')
