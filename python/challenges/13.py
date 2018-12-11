#!/usr/bin/env python3
import sys
import uuid
sys.path.append('..')
from helpers import abort

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

if __name__ == "__main__":
  if len(sys.argv) == 1:
    #print(parse(test_str))
    profile = profile_for("foo@bar.com")
    print(serialize(profile))
  
  else:
    abort(f'{sys.argv[0]}: filename')
