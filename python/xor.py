#!/usr/bin/env python3
import itertools
from helpers import hamming_dst

def score_string(string):
  score_table = "etaoinshrdlcu mwfgypbvkjxqz"[::-1]
  score = 0
  for idx, k in enumerate(score_table):
    if k in string:  
      score += idx 
    elif k.upper() in string:
      score += idx//2 
    else:
      score -= 1
  return score

def xor_key(string, key):
  xored_str = "" 
  for ch in string:
    xored_str += chr(ch ^ key)
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
  for key in range(0, 128):
    xored_str = xor_key(cipher, key)
    score = score_string(xored_str)
    if score > best_score:
      best_score = score  
      best_str = xored_str
  return best_str, best_score


import sys
import array
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
  
def transpose_chunks(chunks, keysize, inverse):
  # transpose blocks
  t_chunks = [b""] * keysize
  for i in range(len(chunks)//keysize):
    for j in range(keysize):
      t_chunks[j] += bytes([chunks[j+i*keysize]])
  return t_chunks
  
def crack_multibyte_xor(cipher):
  keysize = get_avg_keysize(cipher)
  plaintext_chunks = ""
  cipher_chunks = [b""] * keysize
  cipher_chunks = transpose_chunks(cipher, keysize, False)

  cracked_chunks = b""
  for chunk in cipher_chunks:
    cracked = crack_singlebyte_xor(chunk)[0]
    cracked_chunks += bytes(cracked, 'ascii')

  plaintext = transpose_chunks(cracked_chunks, keysize, True)
  print(cracked_chunks[:keysize])
  sys.exit(0)

  plaintext = ""
  plaintext_chunks = [b""] * keysize
  for idx, chunk in enumerate(cipher_chunks):
    cracked = crack_singlebyte_xor(chunk)[0]
    for i in range(0, len(cracked)):
      plaintext_chunks[idx] += str(cracked[i])

  plaintext = transpose_chunks(plaintext_chunks, keysize)
  print(plaintext)
  #plaintext_chunks.append(cracked)
  #plaintext_chunks[idx] = ([cracked[i] for i in range(keysize)])
#print(plaintext_chunks)

  #cipher_chunks = [cipher[i*keysize] for i in range(keysize)]
  print(plaintext_chunks) 
  sys.exit(0)
  plaintext_chunks = [crack_singlebyte_xor(cipher_chunks[i]) for i in range(len(cipher_chunks))]
  print(plaintext_chunks)
  sys.exit(0)


  b1 = cipher[0:keysize]
  b2 = cipher[keysize:keysize*2]

  print(cipher[0:4])
  print('\n')

  print(b1)
  print('\n')
  print(b2)

  print(hamming_dst(b1, b2))
  
  
