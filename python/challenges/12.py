#!/usr/bin/env python3
import sys
import string
sys.path.append('..')
from helpers import abort
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect, aes_mode_oracle
from base64 import b64decode, b64encode

to_append = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

# key must be the same every invocation! 
key = get_random_bytes(16)

def blackbox(plaintext, append, key):
  to_cipher = plaintext + append
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

def ecb_determine_blocksize():
  for blocksize in range(32):
    cipher = blackbox(2 * blocksize * b"A", b64decode(to_append), key)
    dup_count = aes_ecb_detect(cipher)
    if dup_count:
      return blocksize
  return 0

def gen_identical_bytes(blocksize):
  return b'A' * blocksize

def make_dictionary(template):
  dictionary = dict()
  for x in string.ascii_uppercase + string.ascii_lowercase:
    cipher = blackbox(template + x.encode(), b64decode(to_append), key)
    dictionary[template + x.encode()] = cipher[0:16]
  return dictionary

def match_dictionary(cipher, dictionary):
  div = (cipher[i:i+16] for i in range(0, len(cipher), 1))
  block = cipher[0:16]
  for block in div:
    for k, v in dictionary.items():
      if block == v:
        return k.decode()

# byte at a time decryption
def ecb_crack_block(blocksize):
  matches = "" 
  for i in range(1, blocksize):
    blackbox_template = gen_identical_bytes(blocksize - i) + matches.encode()
    cipher = blackbox(blackbox_template, b64decode(to_append)[i-1:], key)
    dictionary = make_dictionary(blackbox_template)
    match = match_dictionary(cipher, dictionary)
    try:
      matches += match[-1:]
    except Exception:
      matches += " "
      pass
  print(f'matches: {matches}, len: {len(matches)}')
  
if __name__ == "__main__":
  if len(sys.argv) == 1:
    blocksize = ecb_determine_blocksize()
    is_ecb = aes_mode_oracle(blackbox(32*b"a", b64decode(to_append), key))

    print("block size:", blocksize)
    print("is ECB:", is_ecb)

    ecb_crack_block(blocksize)

  else:
    abort(f'{sys.argv[0]}: filename')
