#!/usr/bin/env python3
import sys

# **** helpers ****
def abort(msg):
  print(msg)
  sys.exit(1)

def xor(s1, s2):
  if len(s1) != len(s2):
    raise ValueError("input string lengths doesn't match")
  output = b''
  for i in range(len(s1)):
    output += bytes([s1[i] ^ s2[i]])
  return output

def hamming_dst(str1, str2):
  if len(str1) != len(str2):
    raise ValueError("input string lengths doesn't match")
  bcount = 0
  for i in range(len(str1)): 
    val = str1[i] ^ str2[i]
    while val:
      bcount += 1
      # remove 1 bit each time
      val &= val-1
  return bcount

def gen_identical_bytes(blocksize):
  return b'X' * blocksize
