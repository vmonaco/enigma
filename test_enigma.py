'''
Created on Aug 4, 2012

@author: vinnie
'''

import string
from collections import Counter
from enigma import *
from enigma_factory import *

def test_reflector():
    
    reflector = create_reflector(list(string.ascii_uppercase))
    for s in reflector.keys():
        assert s == reflector[reflector[s]]
    
    return


def test_rotor():
    rotor = create_rotor(list(string.ascii_uppercase))
    
    print rotor
    for i in range(rotor.n_symbols):
        rotor.step()
#    assert rotor.odometer == 0
    print rotor
    
    state = rotor.state()
    key_space = set(state.keys())
    value_space = set(state.values())
    try:
        assert len(value_space) == rotor.n_symbols
    except:
        missing = set(key_space).difference(value_space)
        c = Counter([v for v in state.values()])
        duplicates = filter(lambda x: x[1] > 1, c.iteritems())
        print "ERROR: invalid permutation"
        print "Missing symbols: " + str(missing)
        print "Duplicates: " + str(duplicates)
    
    return

def test_enigma():
    str_in = "THISISATEST"

    e = create_enigma()
    print e
    rotor_positions = e.get_rotor_positions()
    enc_str = e.encrypt(str_in)
    
    # reset the rotors since they moved during encryption
    # the original state is restored
    e.set_rotor_positions(rotor_positions)
    dec_str = e.decrypt(enc_str)

    assert str_in == dec_str
    
    print "Plaintext: ", str_in
    print "Encrypted: ", enc_str
    print "Decrypted: ", dec_str
    
    return

if __name__ == '__main__':
    test_rotor()
    test_enigma()
