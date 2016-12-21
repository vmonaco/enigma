'''
Functions to create and configure a random, valid Enigma

Created on Dec 21, 2012

@author: vinnie
'''

import string
from copy import copy
from random import shuffle, randint
from enigma import *


def create_rotor(symbols):
    '''
    Create a random, valid rotor
    '''
    perm = copy(symbols)
    shuffle(perm)
    return Rotor(symbols, perm)


def create_reflector(symbols=list(string.ascii_uppercase)):
    '''
    
    '''
    n_symbols = len(symbols)
    # reflector and stecker require an even number of symbols
    assert n_symbols % 2 == 0

    half_n = n_symbols / 2
    head = symbols[:half_n]
    tail = symbols[half_n:]
    shuffle(tail)

    perm = {h: t for h, t in zip(head, tail)}
    perm.update({t: h for h, t in zip(head, tail)})

    return perm


def empty_stecker():
    '''
    A stecker with no connections
    '''
    return {c: c for c in string.ascii_uppercase}


def create_enigma(symbols=list(string.ascii_uppercase), n_rotors=3):
    '''
    
    '''
    # create the non-replaceable parts
    n_symbols = len(symbols)
    rotors = [create_rotor(symbols) for n in range(3)]
    reflector = create_reflector(symbols)
    e = Enigma(rotors, reflector)

    # now configure
    stecker = create_reflector(symbols)
    odometer_start = [randint(0, n_symbols - 1) for i in range(n_rotors - 1)]
    #    odometer_start = [0] * (n_rotors-1)
    e.configure(stecker, odometer_start)
    rotor_positions = [randint(0, n_symbols - 1) for i in range(n_rotors)]
    e.set_rotor_positions(rotor_positions)

    return e
