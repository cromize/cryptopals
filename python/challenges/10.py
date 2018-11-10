#!/usr/bin/env python3
import sys
sys.path.append('..')
from helpers import abort
from block_crypto import aes_cbc_encrypt, aes_cbc_decrypt
from base64 import b64encode, b64decode

if __name__ == "__main__":
  if len(sys.argv) == 4 and not sys.argv[1] == '-d':
    with open(sys.argv[1], 'rb') as f:
      plain = f.read().rstrip()
      key = sys.argv[2].encode()
      iv = bytes([int(sys.argv[3])])
      ciphertext = aes_cbc_encrypt(plain, key, iv)
      print(b64encode(ciphertext))

  elif len(sys.argv) == 5 and sys.argv[1] == '-d':
    with open(sys.argv[2], 'rb') as f:
      cipher = b64decode(f.read().rstrip())
      key = sys.argv[3].encode()
      iv = bytes([int(sys.argv[4])])
      plaintext = aes_cbc_decrypt(cipher, key, iv).decode()
      print(plaintext)
  else:
    abort(f'{sys.argv[0]}: [-d] filename password iv')
