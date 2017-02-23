#!/usr/bin/env python3

import base64
import itertools
import string

# ALLOWED_CHARS = string.printable
ALLOWED_CHARS = string.ascii_lowercase + ' '
ALLOWED_CHARS_ORD = [ord(c) for c in ALLOWED_CHARS]

BASE64_CHARS = string.ascii_uppercase + string.ascii_lowercase + string.digits + "+/"
BASE64_MISSING_VALUE = ' '
BASE64_MISSING_VALUE_TRESHOLD = 1

MSG_ENCODING = 'ascii'

VERBOSE = False

def oneliner(s):
    return ''.join([(base64.b64decode(s[x:x+4]).decode() if ' ' not in s[x:x+4] else '___') for x in range(0, len(s), 4)])

def log(s):
    if VERBOSE:
        print(s)

def valid_msg_chunk(chunk):
    return all([(c in ALLOWED_CHARS_ORD) for c in chunk])

def get_possible_chunks(chunk):
    if chunk.count(' ') > BASE64_MISSING_VALUE_TRESHOLD:
        log("Too many missing characters in chunk: {0}".format(chunk))
        return ["___"]
    # If base64 character is missing, replace with all possible chars
    possible_characters = [
        (c if c != BASE64_MISSING_VALUE else BASE64_CHARS)
        for c
        in chunk]
    # decode b64 > bytestring
    decoded_chunks = [
        base64.b64decode(''.join(c))
        for c
        in itertools.product(*possible_characters)]
    # decode bytestring > string
    return [
        c.decode(MSG_ENCODING)
        for c 
        in decoded_chunks
        if valid_msg_chunk(c)]

def split_into_chunks(s):
   return [s[x:x+4] for x in range(0, len(s), 4)] 

def possible_messages(base64string):
    chunks = split_into_chunks(base64string)
    possible_chunks = [get_possible_chunks(c) for c in chunks]
    possibilities = [''.join(p) for p in itertools.product(*possible_chunks)]
    return possibilities

if __name__ == '__main__':
    partial_b64_string  = "dGVnZ    GUg    b29tIGluIHRlZ2VuIGRlIHN0cm9vb    iB0ZWdlbiBkZSBzdHJ   0gaW4  GVnZW4gZGUgc3Ryb29tIGlu"

    if VERBOSE:
        print("Decoding known chunks:\n{0}\n".format(oneliner(partial_b64_string)))
        input()

    for p in possible_messages(partial_b64_string):
        print(p)


