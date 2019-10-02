#!/usr/bin/env python3
import sys
import random
import string
sys.path.append('..')
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, aes_ecb_detect
from helpers import abort, gen_identical_bytes
from collections import Counter
from base64 import b64decode, b64encode

# *** we need to somehow align blocks ***
# current approach:
#   1. encrypt our input with blocks that help us determine the offset (too many blocks!)
#   2. brute force blocks until offset is zero (very slow!)
#   3. do one byte at a time crack from challenge 12.py

# note: we need to remove the first byte from template for
#       every next byte we are going to crack

# old thought: maybe it's possible to obtain offset without big block overhead, but with just two blocks. we just need to compute all possible arrangements of pppp and XXXX sentinels 

# TODO: we can memoize aes encryption of offset pattern block for speed up
# TODO: let's also put sentinel more blocks behind unknown string, so we can precompute all characters and not deal with offsets

# NOTE: our implementation of pkcs7 is wrong. we can abuse the fact that when padding size is 0, whole chunk of block size value is appended.
#       bruteforcing this last block could give us needed offset, instead of bruteforcing whole text with added blocks for offset detection

to_append = b"Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

key = get_random_bytes(16)

# test stuff
#from block_crypto import pkcs7_pad, pkcs7_unpad
#t = pkcs7_pad(b"l", 3)
#print(pkcs7_unpad(t))
#sys.exit(0)

def oracle(plaintext, append, key):
  random_prefix = get_random_bytes(random.randrange(1, 48))
  to_cipher = random_prefix + plaintext + append
  cipher = aes_ecb_encrypt(to_cipher, key)
  return cipher

# byte at a time decryption with an offset
def ecb_crack_block(to_append_plain, blocksize, first_block=False):
  matches = "" 
  success_times = 0
  i = 1
  while i < blocksize: 
    # build the dictionary
    sentinel = make_offset_sentinel_pattern()
    template = gen_identical_bytes(blocksize - i)
    cipher = oracle(sentinel + template, to_append_plain, key)
    sentinel_idx, dup_cnt, offset = find_sentinel(cipher)
    dictionary = make_dictionary(template, first_block)

    # match the dictionary
    try:
      match = match_dictionary(cipher[16*sentinel_idx:], dictionary)
      #print(aes_ecb_decrypt(cipher, key)[(16*sentinel_idx)+offset:(16*sentinel_idx)+offset+16])
    except IndexError:
      return matches

    # verbose
    print(aes_ecb_decrypt(cipher[16*(sentinel_idx-1):16*(sentinel_idx-1)+16], key))
    print(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key), "offset:", offset)
    print(aes_ecb_decrypt(cipher[16*(sentinel_idx+1):16*(sentinel_idx+1)+16], key))

    # byte we want to crack
    target = chr(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key)[offset-1])

    print("sentinel 1:", chr(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key)[offset]))
    print("sentinel 2:", chr(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key)[offset+1]))

    print("cracked block:", matches)
    print()
    #print("dup_cnt: ", dup_cnt)

    # fails when aligned or when 1st to_append byte is in previous block
    # because we can't compare to_append with 'p' or 'X' (idx is then simply wrong)
    #assert chr(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key)[offset-1]) == 'p'
    #assert chr(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key)[offset]) == 'p'
    #assert chr(aes_ecb_decrypt(cipher[16*sentinel_idx:16*sentinel_idx+16], key)[offset+1]) == 'X'

    # if offset from unknown string is equal to 16, save the last byte from cracked block
    if offset == 0:
      try:
        matches += target
        print("MATCH")
        print(matches)
        print()
      except Exception:
        pass
      i += 1

  return matches

# TODO: let's think about this more...
def make_dictionary(template, first_block=False):
  dictionary = dict()
  for x in range(256):
    sentinel = make_offset_sentinel_pattern()
    cipher = oracle(sentinel + template + chr(x).encode(), b64decode(to_append), key)
    sentinel_idx, dup_cnt, offset = find_sentinel(cipher)
    #print(aes_ecb_decrypt(cipher, key)[(16*sentinel_idx):(16*sentinel_idx)+16])
    # dict_key for first block only?
    dict_key = ((offset-1) * b"p" + (16-offset) * b"X")#[:-1]
    #print(dict_key, len(dict_key), offset)
    if not first_block:
      dict_key = template
    dictionary[dict_key + chr(x).encode()] = cipher[(16*sentinel_idx):(16*sentinel_idx)+16]
  return dictionary

def match_dictionary(cipher, dictionary):
  block = cipher[0:16]
  #print(block)
  #print(aes_ecb_decrypt(block, key))
  #print(dictionary)
  #sys.exit(0)
  for k, v in dictionary.items():
    if block == v:
      return k.decode()

# find the most common block, get idx, duplicate count and offset from that
def find_sentinel(ciphertext):
  cipher_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
  counter = Counter(cipher_blocks)
  sentinel_cipher = counter.most_common()[0][0]
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

    # we will need this for debugging
    """
    success_times = 0
    i = 0
    while 1:
      cipher = oracle(sentinel_sled, to_append, key)
      sentinel_idx, dup_cnt, offset = find_sentinel(cipher)
      i += 1
      if dup_cnt != None and (dup_cnt % 2) == 0:
        print("aligned sentinel block idx:", sentinel_idx)
        print("offset in block:", offset)
        print(aes_ecb_decrypt(cipher[16*(sentinel_idx+1):16*(sentinel_idx+2)], key)[idx_start:])
        success_times += 1
        print(f"{success_times}/{i}", "sucess/all,", f"ratio {(success_times/i)*100:.2f}%")

    """

    # lets crack the blocks
    cracked = ""
    plain_blocks = (b64decode(to_append)[i:i+16] for i in range(0, len(b64decode(to_append)), 16))
    for idx, block in enumerate(plain_blocks):
      try:
        if idx == 0:
          cracked += ecb_crack_block(block, 16, True)
        else: 
          cracked += ecb_crack_block(block, 16)
      except IndexError:
        pass
      print(cracked)
    print("cracked:", cracked)
    
  else:
    abort(f'{sys.argv[0]}: filename')
