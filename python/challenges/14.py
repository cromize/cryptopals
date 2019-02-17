#!/usr/bin/env python3
import sys
import random
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
  to_cipher = random_prefix + plaintext + append
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

def make_sentinel_dictionary(template):
  dictionary = dict()
  for x in range(16):
    tmp = 4*16*b"b" + x*b"b" + template
    cipher = oracle(tmp, b64decode(to_append), key)
    sentinel_idx = find_sentinel(cipher)
    #print(aes_ecb_decrypt(cipher[16*(sentinel_idx+1):16*(sentinel_idx+2)], key))
    dictionary[tmp[0:16]] = cipher[16*(sentinel_idx+1):16*(sentinel_idx+2)]
  return dictionary
"""
  for x in range(16):
    tmp = template + x*b"b"
    cipher = oracle(tmp, b64decode(to_append), key)
    sentinel_idx = find_sentinel(cipher)
    # idx is last 16 bytes
    dictionary[tmp[len(tmp)-16:len(tmp)]] = cipher[16*(sentinel_idx+1):16*(1+sentinel_idx+1)]
"""

"""
# we need to make a function to forge blocks
# 4*prepend + sentinel + 4*append
def find_forge(ciphertext, offset):
  cipher_blocks = [ciphertext[i+offset:i+offset+16] for i in range(0, len(ciphertext), 16)]
  counter = Counter(cipher_blocks)
  forge_block = counter.most_common()[0][0]
  print(counter.most_common())
  last_sentinel_idx = 0
  for idx, block in enumerate(cipher_blocks):
    if block == forge_block:
      print("FOUND")
      print(block)
      last_sentinel_idx = idx
  return last_sentinel_idx

def make_forge_dict():
  unique_sled = b"0123456789abcdef"
  dictionary = dict()
  for x in range(16):
    tmp = 4*16*b"b" + x*b"b" + unique_sled + 4*16*b"c"
    cipher = oracle(tmp, b64decode(to_append), key)
    forge_a_idx = find_forge(cipher, 0)
    print("forge_a:", forge_a_idx)

    forge_b_idx = find_forge(cipher, 16*(forge_a_idx-1))
    print("forge_b:", forge_b_idx)

    diff = forge_b_idx - forge_a_idx
    #print(aes_ecb_decrypt(cipher[16*(diff+1):16*(diff+2)], key))
    sys.exit(0)
    dictionary[tmp[0:16]] = cipher[16*(sentinel_idx+1):16*(sentinel_idx+2)]
  return dictionary
"""

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
  for idx, i in enumerate(occurrence):
    if (i % 2.0) == 0:
      return last_sentinel_idx, counter.most_common()[idx][1]
  return None, None
      
if __name__ == "__main__":
  if len(sys.argv) == 1:
    sentinel_sled = 4*16*b"a" + b"z" + 6*16*b"b" + b"z" + 8*16*b"c" + b"z" + 10*16*b"d" + b"z"
    success_times = 1
    fail_times = 0
    while 1:
      cipher = oracle(sentinel_sled, to_append, key)
      sentinel_idx, dup_cnt = find_sentinel(cipher)
      if dup_cnt == 4 or dup_cnt == 6 or dup_cnt == 8:
        print(f"{success_times}/{fail_times}", "sucess/miss,", f"ratio {(success_times/fail_times)*100}%")
        success_times += 1
      else:
        fail_times += 1

    sys.exit(0)
    unique_sled = b"0123456789abcdef"
    sentinel_dict = make_sentinel_dictionary(unique_sled)
    #print(match_dictionary(cipher, sentinel_dict))

    #make_forge_dict()
    sys.exit(0)

    #TODO: lets crack tha blooocks
    cracked = ""
    plain_blocks = (b64decode(to_append)[i:i+16] for i in range(0, len(b64decode(to_append)), 16))
    for block in plain_blocks:
      cracked += ecb_crack_block(block, 16, sentinel_idx+1)
    print("cracked:", cracked)
    
  else:
    abort(f'{sys.argv[0]}: filename')
