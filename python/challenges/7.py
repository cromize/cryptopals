#!/usr/bin/env python3
import sys
from base64 import b64encode, b64decode
sys.path.append('..')
from helpers import abort
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt

if __name__ == "__main__":
  if len(sys.argv) == 3 and not sys.argv[1] == '-d':
    with open(sys.argv[1], 'rb') as f:
      plaintext = f.read()
      key = sys.argv[2].encode()
      ciphertext = aes_ecb_encrypt(plaintext, key)
      print(b64encode(ciphertext))
  elif len(sys.argv) == 4 and sys.argv[1] == '-d':
    with open(sys.argv[2], 'rb') as f:
      ciphertext = b64decode(f.read().rstrip())
      key = sys.argv[3].encode()
      plaintext = aes_ecb_decrypt(ciphertext, key)
      print(plaintext.decode())
  else: 
    abort(f'{sys.argv[0]}: [-d] filename password')

