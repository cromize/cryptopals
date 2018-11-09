#!/usr/bin/env python3
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def aes_ebc_encrypt(plaintext, key):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
  encryptor = cipher.encryptor()
  return encryptor.update(plaintext)

def aes_ebc_decrypt(ciphertext, key):
  backend = default_backend()
  cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
  decryptor = cipher.decryptor()
  return decryptor.update(ciphertext) 
