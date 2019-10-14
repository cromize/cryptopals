#!/usr/bin/env python3
import sys
import random
import string
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect, pkcs7_unpad
from helpers import abort, generate_template
from collections import Counter
from base64 import b64decode, b64encode

# *** we need to somehow align blocks ***
# old approach:
#   1. encrypt our input with blocks that help us determine the offset (too many blocks!)
#   2. brute force blocks until offset is zero (very slow!)
#   3. do one byte at a time crack from challenge 12.py

# note: we need to remove the first byte from template for
#       every next byte we are going to crack

# TODO: we can memoize aes encryption of offset pattern block for speed up
# TODO: let's also put sentinel more blocks behind unknown string, so we can precompute all characters and not deal with offsets

# NOTE: we can abuse the fact that when padding size is 0, whole chunk of block size value is appended.
#       bruteforcing this last block could give us needed offset, instead of bruteforcing whole text with added blocks for offset detection

to_append = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = get_random_bytes(16)

pad_block = b""
check_block = b""
sentinel_block = b""

def oracle(plaintext, append, key):
  random_prefix = get_random_bytes(random.randrange(1, 48))
  to_cipher = random_prefix + plaintext + append
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

# byte at a time decryption with an offset
def ecb_crack_block(to_append_plain, blocksize, cracked):
  matches = b""
  success_times = 0
  i = 1

  # aes padding block
  global pad_block, check_block, sentinel_block
  pad_block = craft_aes_block(16*b"\x10")
  check_block = craft_aes_block(16*b"p")
  sentinel_block = craft_aes_block(b"abcdefghijklmnop")

  template = generate_template(cracked[-16:], blocksize - i)

  while i <= blocksize: 
    # TODO: we could pre-generate cipher for each of 16 offsets
    cipher = generate_even_cipher(template)

    dictionary = make_dictionary(template + matches)

    # match the dictionary
    try:
      matches += match_dictionary(cipher, dictionary, len(cracked))[-1].encode('ascii')
      print(matches)
      i += 1
      template = generate_template(cracked[-16:], blocksize - i)
    except TypeError as e:
      # all done
      if matches[-1] == 1:
        return matches

  return matches

# generates cipher that has even length
def generate_even_cipher(template):
  # if last cipher block matches our pad_block, we know that offset is zero
  cipher_blocks = []
  cipher = b""
  while check_block not in cipher_blocks:
    cipher = oracle(16*b"p" + template, b64decode(to_append), key)
    cipher_blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
  return cipher

# TODO: let's think about this more...
def make_dictionary(template):
  dictionary = dict()
  xx = string.printable.encode() + b"\x01"
  for x in xx:
    #sentinel = make_offset_sentinel_pattern()
    cipher_block = better_craft_aes_block(template + bytes([x]))
    #cipher = oracle(template + chr(x).encode(), b64decode(to_append), key)
    #sentinel_idx, dup_cnt, offset = find_sentinel(cipher)
    #print(aes_ecb_decrypt(cipher, key)[(16*sentinel_idx):(16*sentinel_idx)+16])
    # dict_key for first block only?
    #dict_key = ((offset-1) * b"p" + (16-offset) * b"X")#[:-1]
    #print(dict_key, len(dict_key), offset)
    dictionary[template + bytes([x])] = cipher_block
  return dictionary

def match_dictionary(cipher, dictionary, cracked_len):
  #cipher = aes_ecb_decrypt(cipher, key)
  cipher_blocks = [cipher[cracked_len+i:cracked_len+i+16] for i in range(0, len(cipher), 16)]
  #print(cipher_blocks)
  #print(block)
  #print(aes_ecb_decrypt(block, key))
  #print(dictionary)
  #sys.exit(0)
  for k, v in dictionary.items():
    if v in cipher_blocks:
      return k.decode()

# TODO: looking for known sentinel block could be better than looking for most common block
# when we want to crack the last byte of a block, we need to check for one more of the same block, because it's included in target we want to crack
def craft_aes_block(plain):
  block_count = 0
  while not (block_count == 4 or block_count == 5):
   cipher = oracle(plain + 16*b"a" + plain + 16*b"b" + plain + 16*b"c" + plain + 16*b"d", b64decode(to_append), key)
   common, block_count = find_most_common_block(cipher)
  return common

def better_craft_aes_block(plain):
  # if last cipher block matches our pad_block, we know that offset is zero
  cipher_blocks = []
  cipher = b""
  while sentinel_block not in cipher_blocks:
    cipher = oracle(b"abcdefghijklmnop" + plain, b64decode(to_append), key)
    cipher_blocks = [cipher[i:i+16] for i in range(0, len(cipher), 16)]
    offset = cipher.find(sentinel_block) + 16
    target = cipher[offset:offset+16]
  return target

def find_most_common_block(ciphertext):
  # verbose stuff
  #plain = aes_ecb_decrypt(ciphertext, key)
  #plain_blocks = [plain[i:i+16] for i in range(0, len(plain), 16)]
  cipher_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  counter = Counter(cipher_blocks)
  #plain_counter = Counter(plain_blocks)
  #print(plain_counter.most_common())
  return counter.most_common()[0]

# find the most common block, get idx, duplicate count and offset from that
def find_sentinel(ciphertext):
  sentinel_cipher = find_most_common_block(ciphertext)
  last_sentinel_idx = 0
  for idx, block in enumerate(cipher_blocks):
    if block == sentinel_cipher:
      #print("FOUND")
      #print(block)
      last_sentinel_idx = idx
  
  occurrence = [counter.most_common()[idx][1] for idx in range(len(counter.most_common()))]
  idx_start = 0
  for idx, i in enumerate(occurrence):
    dup_cnt = counter.most_common()[idx][1]
    if idx_start == 0 and idx != 1:
      idx_start = idx
    if (i % 2.0) == 0:
      if dup_cnt >= 32:
        return last_sentinel_idx + 1, dup_cnt, idx - idx_start
      else:
        return last_sentinel_idx + 1, dup_cnt, idx - idx_start + 1
  return None, None, None

def make_offset_sentinel_pattern():
  pattern = b""
  for idx, i in enumerate(range(4, 36, 2)):
    pattern += i * 16 * string.ascii_lowercase[idx].encode() + b"Z"
  return pattern[:-1]
  
if __name__ == "__main__":
  if len(sys.argv) == 1:
    sentinel_sled = make_offset_sentinel_pattern()
    print("sentinel pattern len:", len(sentinel_sled))

    # lets crack the blocks
    cracked = b""
    plain_blocks = (b64decode(to_append)[i:i+16] for i in range(0, len(b64decode(to_append)), 16))
    for idx, block in enumerate(plain_blocks):
      if cracked == b"":
        cracked += ecb_crack_block(block, 16, 16*b"X")
      else:
        cracked += ecb_crack_block(block, 16, cracked)
    print("cracked:\n", pkcs7_unpad(cracked).decode())
    
  else:
    abort(f'{sys.argv[0]}: filename')
