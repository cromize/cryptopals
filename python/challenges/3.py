#!/usr/bin/env python3
import sys
import binascii

enc_str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

if __name__ == "__main__":
  raw_str = binascii.unhexlify(enc_str) 
  for key in range(0, 128):
    xored_str = "" 
    for ch in raw_str:
      xored_str += chr(ch ^ key)
    print(bytes(xored_str, 'ascii')) 
    
