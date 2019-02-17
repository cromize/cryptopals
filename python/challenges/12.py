#!/usr/bin/env python3
import sys
import string
sys.path.append('..')
from helpers import abort, gen_identical_bytes
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect, aes_mode_oracle
from base64 import b64decode, b64encode

to_append = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

# key must be the same every invocation! 
key = get_random_bytes(16)

def oracle(plaintext, append, key):
  to_cipher = plaintext + append
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

def ecb_determine_blocksize():
  for blocksize in range(32):
    cipher = oracle(2 * blocksize * b"A", b64decode(to_append), key)
    dup_count = aes_ecb_detect(cipher)
    if dup_count:
      return blocksize
  return 0

def make_dictionary(template):
  dictionary = dict()
  for x in range(256):
    cipher = oracle(template + chr(x).encode(), b64decode(to_append), key)
    dictionary[template + chr(x).encode()] = cipher[0:16]
  return dictionary

def match_dictionary(cipher, dictionary):
  block = cipher[0:16]
  for k, v in dictionary.items():
    if block == v:
      return k.decode()

# byte at a time decryption
def ecb_crack_block(to_append_plain, blocksize):
  matches = "" 
  for i in range(1, blocksize+1):
    template = gen_identical_bytes(blocksize - i) + matches.encode()
    cipher = oracle(template, to_append_plain[i-1:], key)
    dictionary = make_dictionary(template)
    match = match_dictionary(cipher, dictionary)
    try:
      matches += match[-1:]
    except Exception:
      pass
  return matches
  
if __name__ == "__main__":
  if len(sys.argv) == 1:
    blocksize = ecb_determine_blocksize()
    is_ecb = aes_mode_oracle(oracle(32*b"a", b64decode(to_append), key))

    print("block size:", blocksize)
    print("is ECB:", is_ecb)
    print()

    cracked = ""
    plain_blocks = (b64decode(to_append)[i:i+16] for i in range(0, len(b64decode(to_append)), 16))
    for block in plain_blocks:
      cracked += ecb_crack_block(block, blocksize)

    print(cracked)
    print("plain len: ", len(b64decode(to_append)))
    print("cracked len: ", len(cracked))

  else:
    abort(f'{sys.argv[0]}: filename')
