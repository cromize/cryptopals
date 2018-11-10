#!/usr/bin/env python3
import itertools
from helpers import hamming_dst

def score_string(string):
  score_table = b"etaoinshrdlcu mwfgypbvkjxqz"[::-1]
  score = 0
  for idx, k in enumerate(score_table):
    if k in string:  
      score += idx 
    elif str(k).upper() in str(string):
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
  chunk_size = len(cipher)
  # we can divide large cipher text by 2-8 to speed up
  if len(cipher) >= 1500:
    chunk_size //= 8
    
  for keysize in range(2, KEYSIZE_MAX):
    chunks = [cipher[i:i+keysize] for i in range(0, chunk_size, keysize)]
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
  
# **** vigenere crack ****
def vig_divide_text(text, keysize):
  chunks = []
  for offset in range(keysize):
    idx_gen = (i for i in range(0, len(text), keysize) if i+offset < len(text))
    chunk = b"".join(bytes([text[i+offset]]) for i in idx_gen)
    chunks.append(chunk)
  return chunks

def vig_combine_chunks(chunks):
  text = b""
  for offset in range(len(chunks[0])):
    idx_gen = (i for i in range(len(chunks)) if len(chunks[i]) > offset)
    chunk = (bytes([chunks[i][offset]]) for i in idx_gen)
    text += b"".join(chunk)
  return text
  
def crack_multibyte_xor(cipher):
  multibyte_key = b""
  keysize = get_avg_keysize(cipher)
  cipher_chunks = vig_divide_text(cipher, keysize)
  cracked_chunks = []
  for chunk in cipher_chunks:
    cracked, _, singlebyte_key = crack_singlebyte_xor(chunk)
    multibyte_key += singlebyte_key
    cracked_chunks.append(cracked)

  plaintext = vig_combine_chunks(cracked_chunks)
  return plaintext, multibyte_key

