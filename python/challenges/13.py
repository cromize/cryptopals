#!/usr/bin/env python3
import sys
import uuid
sys.path.append('..')
from helpers import abort
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes

test_str = "foo=bar&baz=qux&zap=zazzle"

def parse(input_str):
  obj = dict()
  parse_gen = (x for x in input_str.split("&")) 
  for token in parse_gen:
    k = token.split("=")[0]
    v = token.split("=")[1]
    obj[k] = v
  return obj

def serialize(obj):
  buf = ""
  for k, v in obj.items():
    buf += "%s=%s&" % (k, v)
  return buf[:-1]

def profile_for(input_str):
  if "&" in input_str or "=" in input_str:
    raise Exception("input cannot contain & or = symbol")
  profile = dict()
  profile["email"] = input_str
  profile["uid"] = uuid.uuid4().bytes[0]
  profile["role"] = "user"
  return profile

def encrypt_profile(profile):
  password = b"PABCDEFABCDEFGHJ" #get_random_bytes(16)
  buf = serialize(profile)
  cipher_prof = aes_ecb_encrypt(buf.encode(), password)
  return cipher_prof

def decrypt_profile(profile):
  pass

if __name__ == "__main__":
  password = b"PABCDEFABCDEFGHJ" #get_random_bytes(16)
  if len(sys.argv) == 1:
    #print(parse(test_str))
    profile = profile_for("foo@bar.com")
    ser_profile = serialize(profile)
    print(ser_profile)
    print("len:", len(ser_profile))
    print()
    cipher_profile = encrypt_profile(profile)
    print(cipher_profile)
    print("len:", len(cipher_profile))
    print()
    # TODO: decrypt doesn't work yet
    decrypted = aes_ecb_decrypt(cipher_profile, password)
    print(decrypted)
    print("len:", len(decrypted))
    print()
  
  else:
    abort(f'{sys.argv[0]}: filename')
