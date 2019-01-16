#!/usr/bin/env python3
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from collections import Counter
from xor import xor_repeating_key

# **** ECB mode ****
def aes_ecb_encrypt(plaintext, key):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()

  ciphertext = b""
  plain_div = (plaintext[i:i+16] for i in range(0, len(plaintext), 16))
  for plain_block in plain_div:
    # pkcs7 pad, then encrypt
    ciphertext += encryptor.update(pkcs7_pad(plain_block, 16))
    #print(ciphertext)
    #print(aes_ecb_decrypt(ciphertext, key))
  return ciphertext + encryptor.finalize()

def aes_ecb_decrypt(ciphertext, key):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()

  plaintext = b""
  cipher_div = (ciphertext[i:i+16] for i in range(0, len(ciphertext), 16))
  for cipher_block in cipher_div:
    plaintext += decryptor.update(ciphertext) 
  return plaintext + decryptor.finalize()

# return the count of duplicate blocks == ecb mode
# works for min. 3 same blocks
def aes_ecb_detect(cipher):
  # divide blocks
  blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
  counter = Counter(blocks)
  # sorted blocks by occurrence, most occurred at [0]
  duplicate_count = counter.most_common()[0][1]
  if duplicate_count <= 1:
    duplicate_count = 0
  return duplicate_count

# **** CBC mode ****
def aes_cbc_encrypt(plaintext, key, iv):
  blocks = [plaintext[i:i+16] for i in range(0, len(plaintext), 16)]
  ciphertext = b""
  for block in blocks:
    xored_block = xor_repeating_key(block, iv) 
    ciphered = aes_ecb_encrypt(xored_block, key)
    iv = ciphered 
    ciphertext += ciphered
  return ciphertext

def aes_cbc_decrypt(ciphertext, key, iv):
  blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  plaintext = b""
  for block in blocks:
    deciphered = aes_ecb_decrypt(block, key)
    plain_block = xor_repeating_key(deciphered, iv) 
    iv = block 
    plaintext += plain_block
  return plaintext

# return 1 for ECB guess, return 0 for CBC or undecidable mode
def aes_mode_oracle(cipher):
  dup_count = aes_ecb_detect(cipher)
  if dup_count >= 2:
    return 1
  else:
    return 0

def get_random_bytes(size):
  key = b"".join((bytes([random.randrange(1, 256)]) for x in range(size)))
  return key
  
def pkcs7_pad(text, size):
  if len(text) < size:
    left = size - len(text)
  else:
    left = len(text) % size 
  text += ('%b'.encode() % bytes([left])) * left
  return text

