#!/usr/bin/env python3
import itertools
from helpers import hamming_dst

def score_string(string):
  score_table = "etaoinshrdlcu mwfgypbvkjxqz"[::-1]
  score = 0
  for idx, k in enumerate(score_table):
    if k in string.decode():  
      score += idx 
    elif k.upper() in string.decode():
      score += idx//2 
    else:
      score -= 1
  return score

def xor_key(string, key):
  xored_str = b"" 
  for ch in string:
    xored_str += bytes([ch ^ key])
  return xored_str

def xor_repeating_key(string, key):
  xored_str = b"" 
  idx = 0 
  for ch in string:
    xored_str += bytes([ord(ch) ^ ord(key[idx])])
    idx += 1
    if idx >= len(key):
      idx = 0
  return xored_str

def crack_singlebyte_xor(cipher):
  best_score = 0
  best_str = ""
  best_key = 0
  for key in range(0, 128):
    xored_str = xor_key(cipher, key)
    score = score_string(xored_str)
    if score > best_score:
      best_score = score  
      best_str = xored_str
      best_key = key
  return best_str, best_score, bytes([best_key])

def get_avg_keysize(cipher):
  KEYSIZE_MAX = 40
  avg_min = 65535
  best_keysize = 0
  for keysize in range(2, KEYSIZE_MAX):
    # we can divide large cipher text by 2-8 to speed up
    chunks = [cipher[i:i+keysize] for i in range(0, (len(cipher)//8)-keysize, keysize)]
    chunk_pairs = list(itertools.combinations(chunks, 2))
    avg_dst = 0

    for pair in chunk_pairs:
      dst = hamming_dst(pair[0], pair[1]) / keysize
      avg_dst += dst

    avg_dst /= len(chunk_pairs)
    if avg_dst < avg_min:
      avg_min = avg_dst
      best_keysize = keysize
  return best_keysize
  
# we added one chunk, if we have odd keylength
# not ideal solution
def divide_text(text, keysize):
  # transpose blocks
  t_chunks = [b""] * (keysize+1)
  for i in range((len(text)//keysize)+1):
    for j in range(keysize):
      if j+i*keysize <= 2875:
        t_chunks[j] += bytes([text[j+i*keysize]])
  return t_chunks

# not sure if try, except is right method
def combine_chunks(chunks, keysize):
  text = b""
  for i in range(len(chunks[0])):
    for chunk in chunks:
      try:
        text += bytes([chunk[i]])
      except Exception:
        pass
  return text
  
import sys
def crack_multibyte_xor(cipher):
  multibyte_key = b""
  keysize = get_avg_keysize(cipher)
  cipher_chunks = divide_text(cipher, keysize)
  cracked_chunks = []

  for chunk in cipher_chunks:
    cracked, __, singlebyte_key = crack_singlebyte_xor(chunk)
    multibyte_key += singlebyte_key
    cracked_chunks.append(cracked)

  plaintext = combine_chunks(cracked_chunks, keysize)
  return plaintext, multibyte_key

