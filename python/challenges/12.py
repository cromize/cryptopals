#!/usr/bin/env python3
import sys
import string
sys.path.append('..')
from helpers import abort, generate_template
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect, aes_mode_oracle, pkcs7_unpad
from base64 import b64decode, b64encode

append = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

# key must be the same every invocation! 
key = get_random_bytes(16)

def oracle(plaintext, key):
  to_cipher = plaintext + b64decode(append)
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

def ecb_determine_blocksize():
  for blocksize in range(32):
    cipher = oracle(2*blocksize * b"A", key)
    dup_count = aes_ecb_detect(cipher)
    if dup_count:
      return blocksize
  return 0

def make_dictionary(template):
  dictionary = dict()
  xx = string.printable.encode() + b"\x01"
  for x in xx:
    cipher = oracle(template + chr(x).encode(), key)
    dictionary[template + chr(x).encode()] = cipher[:16]
  return dictionary

def match_dictionary(cipher, dictionary, cracked_len):
  block = cipher[cracked_len:cracked_len+16]
  for k, v in dictionary.items():
    if block == v:
      return k.decode()

# byte at a time decryption
def ecb_crack_block(blocksize, cracked, written):
  matches = b"" 
  for i in range(1, blocksize+1):
    template = generate_template(cracked[-16:], blocksize - i)
    cipher = oracle(template, key)
    dictionary = make_dictionary(template + matches)
    match = match_dictionary(cipher, dictionary, written)
    try:
      matches += match[-1].encode()
    except Exception:
      pass
  return matches
  
if __name__ == "__main__":
  if len(sys.argv) == 1:
    blocksize = ecb_determine_blocksize()
    is_ecb = aes_mode_oracle(oracle(32*b"a", key))

    print("block size:", blocksize)
    print("is ECB:", is_ecb)
    print()

    if not is_ecb:
      abort("** cipher doesn't use ECB mode")

    cracked = b""
    written = 0
    while len(cracked) <= len(b64decode(append)):
      cracked_block = ecb_crack_block(blocksize, cracked or 16*b"a", written)
      cracked += cracked_block
      written += len(cracked_block)

    print(pkcs7_unpad(cracked).decode())
    print("plain len: ", len(b64decode(append)))
    print("cracked len: ", len(cracked))

  else:
    abort(f'{sys.argv[0]}: filename')
