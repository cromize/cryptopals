#!/usr/bin/env python3
import sys
import random
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, aes_cbc_encrypt, aes_cbc_decrypt, aes_ecb_detect, pkcs7_pad, get_random_bytes, aes_mode_oracle
from base64 import b64decode, b64encode
from helpers import abort

def blackbox(plain):
  append = random.randrange(5, 11)
  appended = get_random_bytes(append)
  appended += plain
  append = random.randrange(5, 11)
  appended += get_random_bytes(append)
  
  random_key = get_random_bytes(16)
  coin_toss = bool(random.getrandbits(1))
  if coin_toss == True:
    cipher = aes_ecb_encrypt(pkcs7_pad(appended, 16), random_key)
    print("coin_toss: ECB")
  else:
    random_iv = get_random_bytes(16)
    cipher = aes_cbc_encrypt(pkcs7_pad(appended, 16), random_key, random_iv)
    print("coin_toss: CBC")
  return cipher, coin_toss
  
if __name__ == "__main__":
  if len(sys.argv) == 2:
    test_file = None
    with open(sys.argv[1], 'rb') as f:
      test_file = f.read()

    blackbox_output, coin_toss = blackbox(test_file)
    guessed_mode = aes_mode_oracle(blackbox_output)
    if guessed_mode:
      print("mode: ECB")
    else:
      print("mode: CBC")
    if coin_toss != guessed_mode:
      print("FAIL: modes doesn't match!")
  else:
    abort(f'{sys.argv[0]}: filename')
