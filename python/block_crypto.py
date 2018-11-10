#!/usr/bin/env python3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from collections import Counter

def aes_ecb_encrypt(plaintext, key):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  return encryptor.update(plaintext)

def aes_ecb_decrypt(ciphertext, key):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()
  return decryptor.update(ciphertext) 

def detect_aes_ecb(cipher_lines):
  most_common_block = 0
  best_idx = 0
  for idx, line in enumerate(cipher_lines):
    # divide blocks
    blocks = [line[i:i+16] for i in range(0, len(line), 16)]
    counter = Counter(blocks)
    # sorted blocks by occurrence, most occurred at [0]
    counted_blocks = counter.most_common()[0]
    if counted_blocks[1] > best_idx:
      most_common_block = counted_blocks
      best_idx = idx
  return best_idx

def pkcs7_pad(text, size):
  if len(text) < size:
    left = size - len(text)
  else:
    left = size % len(text)
  text += b'\x04' * left
  return text

