import ctypes
import getopt
import hashlib
import hmac
import sys

from Crypto.Cipher import AES

SQLITE_FILE_HEADER = bytes('SQLite format 3', encoding='ASCII') + bytes(1)
IV_SIZE = 16
HMAC_SHA1_SIZE = 20
KEY_SIZE = 32
DEFAULT_PAGESIZE = 4096
DEFAULT_ITER = 64000
opts, args = getopt.getopt(sys.argv[1:], 'hk:d:')
input_pass = ''
input_dir = ''

for op, value in opts:
    if op == '-k':
        input_pass = value
    else:
        if op == '-d':
            input_dir = value

password = bytes.fromhex(input_pass.replace(' ', ''))

with open(input_dir, 'rb') as (f):
    blist = f.read()
print(len(blist))
salt = blist[:16]
key = hashlib.pbkdf2_hmac('sha1', password, salt, DEFAULT_ITER, KEY_SIZE)
first = blist[16:DEFAULT_PAGESIZE]
mac_salt = bytes([x ^ 58 for x in salt])
mac_key = hashlib.pbkdf2_hmac('sha1', key, mac_salt, 2, KEY_SIZE)
hash_mac = hmac.new(mac_key, digestmod='sha1')
hash_mac.update(first[:-32])
hash_mac.update(bytes(ctypes.c_int(1)))

if hash_mac.digest() == first[-32:-12]:
    print('Decryption Success')
else:
    print('Password Error')
blist = [blist[i:i + DEFAULT_PAGESIZE] for i in range(DEFAULT_PAGESIZE, len(blist), DEFAULT_PAGESIZE)]

with open(input_dir, 'wb') as (f):
    f.write(SQLITE_FILE_HEADER)
    t = AES.new(key, AES.MODE_CBC, first[-48:-32])
    f.write(t.decrypt(first[:-48]))
    f.write(first[-48:])
    for i in blist:
        t = AES.new(key, AES.MODE_CBC, i[-48:-32])
        f.write(t.decrypt(i[:-48]))
        f.write(i[-48:])
