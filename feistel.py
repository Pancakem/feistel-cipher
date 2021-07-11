#! /usr/bin/python3

import sys
import random

class Feistel:
    rounds = 1
    
    def __init__(self, l, r, key):
        self.l = l
        self.r = r
        self.keys = [key]        

    def _xor(self, value, key):
        return bytes(v^k for v, k in zip(value, key))
        
    def encode(self):
        for i in range(self.rounds):
            left = self.r
            right = self._xor(self.l, self.feistel(self.r, self.keys[i]))
            self.l = left
            self.r = right
        return self.l + self.r

    def decode(self):
        for i in reversed(range(self.rounds)):
            right = self.l
            left = self._xor(self.r, self.feistel(self.l, self.keys[i]))
            self.l = left
            self.r = right
        return self.l + self.r

    def feistel(self, value, key):
        return self._xor(value, key)


def strip_mid_padding(data):
    zero_count = 0
    current_index = 0
    
    def remove_at(i, s):
        return s[:i] + s[i+1:]
    
    for c in data:
        if c == '0':
            zero_count +=1
        else:
            if zero_count > 2:
                while zero_count != 0:
                    current_index -= 1
                    data = remove_at(current_index, data)
                    zero_count -= 1
            else:
                zero_count = 0
        current_index += 1
    return data
            


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python feistel 'INPUT' 'K'")
        exit(-1)
    
    byte_order = "big"
    byte_size = 5

    l = int(sys.argv[2], base=16).to_bytes(byte_size, byte_order)
    r = int(sys.argv[3], base=16).to_bytes(byte_size, byte_order)
    key = int(sys.argv[4], base=16).to_bytes(byte_size, byte_order)

    feistel = Feistel(l, r, key)
    if sys.argv[1] == 'e':
        cipher  = hex(int.from_bytes(feistel.encode(), byte_order))
        print("Encryption result: ", hex(int.from_bytes(r, byte_order)).upper()[2:] ,strip_mid_padding(cipher.upper()[2:]).strip(sys.argv[3]))
        
    elif sys.argv[1] == 'd':        
        data  = hex(int.from_bytes(feistel.decode(), byte_order))
        print("Decryption result: ", hex(int.from_bytes(r, byte_order)).upper()[2:] ,strip_mid_padding(data.upper()[2:]).strip(sys.argv[2]))

    else:
        print("Supply mode. Allowed modes are encode (e), decode (d)")
    
    

    
    

