#!/usr/bin/env python3
import sys
import random
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, get_random_bytes
from helpers import abort

to_append = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = get_random_bytes(16)

def find_block(target, ciphertext):
  cipher_blocks = (ciphertext[i:i+16] for i in range(0, len(ciphertext), 16))
  for block in ciphertext:
    if block == target:
      print("FOUND")
      print(target)
  

def oracle(plaintext, append, key):
  random_prefix = get_random_bytes(random.randrange(1, 16))
  to_cipher = random_prefix + plaintext.encode() + append.encode()
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

if __name__ == "__main__":
  if len(sys.argv) == 1:
    oracle("aaaaaaaa", to_append, key)
    fake = aes_ecb_encrypt(16*b"a", key)
    print("fake:", fake)
    

  else:
    abort(f'{sys.argv[0]}: filename')
