#!/usr/bin/env python3
import sys
import uuid
sys.path.append('..')
from helpers import abort
from block_crypto import aes_ecb_encrypt, aes_ecb_decrypt, get_random_bytes, pkcs7_unpad

test_str = "foo=bar&baz=qux&zap=zazzle"

def parse(input_str):
  obj = dict()
  parse_gen = (x for x in input_str.split(b"&")) 
  for token in parse_gen:
    k = token.split(b"=")[0]
    v = token.split(b"=")[1]
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

def encrypt_profile(profile, password):
  buf = serialize(profile)
  cipher_prof = aes_ecb_encrypt(buf.encode(), password)
  return cipher_prof

def decrypt_profile(profile, password):
  decrypted = aes_ecb_decrypt(profile, password)
  return decrypted

def create_aes_block(plain, password):
  # first block contains garbage
  # second block contains our stuff
  offset_block = profile_for(10*"a" + "admin" + 11*"\x0b")
  encrypted = encrypt_profile(offset_block, password)
  cipher_blocks = [encrypted[i:i+16] for i in range(0, len(encrypted), 16)]

  crafted_block = cipher_blocks[1]
  return crafted_block

if __name__ == "__main__":
  password = get_random_bytes(16)
  if len(sys.argv) == 1:
    while 1:
      try:
        target_prof = profile_for("foooo@bar.com")
        print(target_prof)

        cipher_prof = encrypt_profile(target_prof, password)

        plain_prof = decrypt_profile(cipher_prof, password)
        print("decrypted:", plain_prof)
        print("len:", len(plain_prof))
        print()

        print("*** admin block ***")
        admin_block = create_aes_block("admin", password)
        print("admin block:", admin_block)

        cipher_blocks = [cipher_prof[i:i+16] for i in range(0, len(cipher_prof), 16)]
        cipher_blocks[2] = admin_block
        changed_prof = b"".join((x for x in cipher_blocks))
        print(changed_prof)
        print()

        decrypted_prof = decrypt_profile(changed_prof, password) 
        print(decrypted_prof)
        parsed_prof = parse(decrypted_prof)
        print(parsed_prof)
        break
      except:
        pass
  
  else:
    abort(f'{sys.argv[0]}: filename')
