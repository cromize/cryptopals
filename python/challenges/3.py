#!/usr/bin/env python3
import sys
import binascii

enc_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
#enc_str = '''3116581b0a01080c171f0a1908100154580c101d580b111508141d5820372a581b1108101d0a58110b5819580c01081d58171e58191c1c110c110e1d581b1108101d0a54581916581d161b0a01080c1117165819141f170a110c1015580c10190c'''

def score_string(string):
  score_table = "etaoinshrdlcu mwfgypbvkjxqz"[::-1]
  score = 0
  for idx, k in enumerate(score_table):
    if k in string.lower():
      score += idx 
    else:
      score -= 5
  return score

def xor_key(string, key):
  xored_str = "" 
  for ch in string:
    xored_str += chr(ch ^ key)
  return xored_str

if __name__ == "__main__":
  best_score = 0
  best_str = ""
  raw_str = binascii.unhexlify(enc_str) 
  xored_str = ""
  for key in range(0, 128):
    xored_str = xor_key(raw_str, key)
    score = score_string(xored_str)
    if score > best_score:
      best_score = score  
      best_str = xored_str

  print(best_str) 
    
