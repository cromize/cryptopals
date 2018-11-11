#!/usr/bin/env python3
import sys
import random
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, aes_cbc_encrypt, aes_cbc_decrypt, aes_ecb_detect, pkcs7_pad
from base64 import b64decode, b64encode
from helpers import abort

def aes_get_random_key(size):
  key = b"".join((bytes([random.randrange(1, 256)]) for x in range(size)))
  return key

def aes_mode_oracle(cipher):
  pass

def blackbox(plain):
  append = random.randrange(5, 11)
  appended = aes_get_random_key(append)
  appended += plain
  append = random.randrange(5, 11)
  appended += aes_get_random_key(append)
  
  random_key = aes_get_random_key(16)
  coin_toss = bool(random.getrandbits(1))
  if coin_toss == True:
    print(appended)
    cipher = aes_ecb_encrypt(16*b"A" + pkcs7_pad(appended, 16) + 16*b"A", random_key)
    print("coin_toss: ECB")
  else:
    random_iv = aes_get_random_key(16)
    cipher = aes_cbc_encrypt(16*b"A" + pkcs7_pad(appended, 16) + 16*b"A", random_key, random_iv)
    print("coin_toss: CBC")
  return cipher
  
if __name__ == "__main__":
  if len(sys.argv) == 2:
    # generate
    cipher_file = None
    with open(sys.argv[1], 'rb') as f:
      cipher_file = f.read() 
    cipher_file = b64decode(cipher_file)
    blackbox_output = blackbox(cipher_file)
    print("here", len("Write a function that encrypts data under an unknown key")%16)
    print("len:", len(blackbox_output))
    print()

    # predict
    dup_count = aes_ecb_detect(blackbox_output)
    print(dup_count)

  else:
    abort(f'{sys.argv[0]}: [-d] filename password iv')
