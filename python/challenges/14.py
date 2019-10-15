#!/usr/bin/env python3
import sys
import random
import string
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect, pkcs7_unpad
from helpers import abort, generate_template
from collections import Counter
from base64 import b64decode, b64encode

# *** we need to offset align blocks ***
#  1. forge a cipherblock 16*b"p" for detecting even ciphertext
#  2. forge a cipherblock b"abcdefghijklmnop" for fast detection of zero offset cipher
#  3. generate target ciphertext until offset is zero using forged cipherblock
#  4. do one-byte at a time crack from challenge 12.py

# note: we need to remove the first byte from template for
#       every next byte we are going to crack

# we memoize aes encryption of offset pattern block for speed up

append = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = get_random_bytes(16)

check_block = b""
sentinel_block = b""

even_cipher_cache = dict()

def oracle(plaintext, key):
  random_prefix = get_random_bytes(random.randrange(1, 48))
  to_cipher = random_prefix + plaintext + b64decode(append)
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

# byte at a time decryption with an offset
def ecb_crack_block(blocksize, cracked):
  matches = b""
  i = 1

  # aes padding block
  global check_block, sentinel_block
  check_block = craft_aes_block_slower(16*b"p")
  sentinel_block = craft_aes_block_slower(b"abcdefghijklmnop")

  template = generate_template(cracked[-16:], blocksize - i)
  it = generate_template(16*b"X", blocksize - i)

  while i <= blocksize: 
    cipher = generate_even_cipher(it)
    dictionary = make_dictionary(template + matches)

    # match the dictionary
    try:
      matches += match_dictionary(cipher, dictionary, len(cracked))[-1].encode('ascii')
      print(matches)
      i += 1
      template = generate_template(cracked[-16:], blocksize - i)
      it = generate_template(16*b"X", blocksize - i)
    except TypeError as e:
      # all done
      return matches

  return matches

# generates cipher that has even length
def generate_even_cipher(template):
  # if last cipher block matches our pad_block, we know that offset is zero
  if template in even_cipher_cache:
    return even_cipher_cache[template]

  cipher_blocks = []
  cipher = b""
  while check_block not in cipher_blocks:
    cipher = oracle(16*b"p" + template, key)
    cipher_blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]

  # memoize
  if template not in even_cipher_cache:
    even_cipher_cache[template] = cipher  
  return cipher

def make_dictionary(template):
  dictionary = dict()
  xx = string.printable.encode() + b"\x01"
  for x in xx:
    cipher_block = craft_aes_block(template + bytes([x]))
    dictionary[template + bytes([x])] = cipher_block
  return dictionary

def match_dictionary(cipher, dictionary, cracked_len):
  cipher_blocks = [cipher[cracked_len+i:cracked_len+i+16] for i in range(0, len(cipher), 16)]
  for k, v in dictionary.items():
    if v in cipher_blocks:
      return k.decode()

# when we want to crack the last byte of a block, we need to check for one more of the same block, because it's included in target we want to crack
def craft_aes_block_slower(plain):
  block_count = 0
  while not (block_count == 4 or block_count == 5):
   cipher = oracle(4*plain, key)
   common, block_count = find_most_common_block(cipher)
  return common

# looking for known sentinel block is faster than looking for most common block
def craft_aes_block(plain):
  # if last cipher block matches our pad_block, we know that offset is zero
  cipher_blocks = []
  cipher = b""
  while sentinel_block not in cipher_blocks:
    cipher = oracle(b"abcdefghijklmnop" + plain, key)
    cipher_blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
    offset = cipher.find(sentinel_block) + 16
    target = cipher[offset:offset+16]
  return target

def find_most_common_block(ciphertext):
  cipher_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  counter = Counter(cipher_blocks)
  return counter.most_common()[0]

if __name__ == "__main__":
  if len(sys.argv) == 1:
    # lets crack the blocks
    cracked = b""
    while len(cracked) <= len(b64decode(append)):
      cracked += ecb_crack_block(16, cracked or 16*b"X")
    print("cracked:\n", pkcs7_unpad(cracked).decode())
    
  else:
    abort(f'{sys.argv[0]}: filename')
