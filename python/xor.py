#!/usr/bin/env python3
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

def crack_cipher(cipher):
  best_score = 0
  best_str = ""
  for key in range(0, 128):
    xored_str = xor_key(cipher, key)
    score = score_string(xored_str)
    if score > best_score:
      best_score = score  
      best_str = xored_str
  return best_str, best_score
