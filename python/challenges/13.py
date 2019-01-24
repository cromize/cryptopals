#!/usr/bin/env python3
import sys
import uuid
sys.path.append('..')
from helpers import abort
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, pkcs7_unpad

def parse(input_str):
  obj = dict()
  items = (x for x in input_str.split(b"&")) 
  for item in items:
    k = item.split(b"=")[0]
    v = item.split(b"=")[1]
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
  profile["uid"] = 10
  profile["role"] = "user"
  return profile

def encrypt_profile(profile, password):
  buf = serialize(profile)
  cipher_prof = aes_ecb_encrypt(buf.encode(), password)
  return cipher_prof

def decrypt_profile(profile, password):
  decrypted = aes_ecb_decrypt(profile, password)
  plain_prof = parse(decrypted)
  return plain_prof

def create_aes_ecb_block(plain, password):
  # first block contains garbage
  # second block contains our stuff
  pad_len = 16 - len(plain)
  offset_block = profile_for(10*"a" + plain + pad_len*chr(pad_len))
  encrypted = encrypt_profile(offset_block, password)
  cipher_blocks = [encrypted[i:i+16] for i in range(0, len(encrypted), 16)]

  crafted_block = cipher_blocks[1]
  return crafted_block

if __name__ == "__main__":
  password = get_random_bytes(16)
  if len(sys.argv) == 1:
    target_prof = profile_for(5*"o" + "@bar.com")
    cipher_prof = encrypt_profile(target_prof, password)
    admin_block = create_aes_ecb_block("admin", password)

    # replace 'user' with 'admin'
    cipher_blocks = [cipher_prof[i:i+16] for i in range(0, len(cipher_prof), 16)]
    cipher_blocks[2] = admin_block
    changed_prof = b"".join((x for x in cipher_blocks))

    decrypted_prof = decrypt_profile(changed_prof, password) 

    print("*** original ***")
    print(target_prof)
    print("\n*** cipher  ***")
    print(cipher_prof)
    print("\n*** modified ***")
    print(decrypted_prof)

  else:
    abort(f'{sys.argv[0]}: filename')
