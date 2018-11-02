#!/usr/bin/env python3
import sys

# **** helpers ****
def abort(msg):
  print(msg)
  sys.exit(1)

def xor(s1, s2):
  output = b''
  if not len(s1) == len(s2):
    raise ValueError("input string lengths doesn't match")

  for i in range(len(s1)):
    output += bytes([s1[i] ^ s2[i]])

  return output
