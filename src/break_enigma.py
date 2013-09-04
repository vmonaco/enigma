'''
Created on Dec 22, 2012

@author: vinnie
'''

from enigma import *
from enigma_factory import *
import networkx as nx
from copy import deepcopy
from pprint import pprint
from itertools import product
from collections import defaultdict, Counter

def get_perm_states(graph, cycle):
    '''
    Create a list of the permutation states given the node cycle
    '''
    perms = [graph[n1][n2]['P'] for (n1,n2) in zip(cycle[:-1],cycle[1:])]
    
    # add the last permutation state needed to complete the cycle 
    perms.append(graph[cycle[-1]][cycle[0]]['P'])
    return perms

def find_cycles(plaintext, ciphertext):
    '''
    Find all the permutation cycles that exist between the plaintext and ciphertext
    '''
    n_perm_states = len(plaintext)
    graph = nx.Graph()
    
    # create a graph with labeled edges between the plaintext and ciphertext
    graph.add_edges_from((n1,n2,{'P':i}) for (n1,n2,i) in 
                         zip(plaintext, ciphertext, range(n_perm_states)))
    
    cycles = [(c[0],get_perm_states(graph, c)) for c in nx.cycle_basis(graph)]
    return cycles

def valid_cycle(enigma, rotor_positions, E, perm_cycle):
    '''
    Check if the permutation cycle is valid for the given configuration
    '''
    c = E
    for P in perm_cycle:
        enigma.set_rotor_positions(rotor_positions)
        enigma.step_to(abs(P))
        c = enigma.encrypt(c)
    
    # reset the machine
    enigma.set_rotor_positions(rotor_positions)
    
    # the cycle holds if the input and output are the same
    if c == E:
        return True
    return False
    
def reduce_keyspace(rotors, reflector, 
                    plaintext, ciphertext, 
                    min_n_cycles=3, max_n_cycles=3, 
                    min_cycle_length=3, max_cycle_length=5,
                    symbol_space=list(string.uppercase)):
    '''
    Find the possible machine states given the rotors, reflector, plaintext and 
    ciphertext. This limits the possible key space by exploiting permutation 
    cycles in the machine. It attempts to find all the possible configurations 
    to generate the ciphertext.
    
    The number of cycles used for each input are bounded by min and max n_cycles
    The cycles length is bounded by min and max cycles_length
    
    Returns: a list of initial rotor positions and map of stecker configurations
    '''
    
    # create a machine to use in the search
    workspace = Enigma(rotors, reflector)
    workspace.stecker = empty_stecker()
    
    # dict accessed by the start/end value of each system of cycles
    cycles = find_cycles(plaintext, ciphertext)
    cycle_dict = defaultdict(list)
    for c in cycles:
        cycle_dict[c[0][0]].append(c[1])
    
    # filter the cycle length, # cycles, and finally sort by length for
    # efficiency (shorter cycles tested and disqualified first)
    for k,v in cycle_dict.items():
        cycle_dict[k] = filter(lambda x: len(x) >= min_cycle_length 
                               and len(x) <= max_cycle_length,
                               v)[:max_n_cycles]

        if len(cycle_dict[k]) < min_n_cycles:
            cycle_dict.pop(k)
        else:
            cycle_dict[k].sort(key=len)
            
    
    pprint(cycle_dict)
    print "Cycle groups: ", len(cycle_dict.items())
    # the initial rotor position key space
    rotor_positions = product(*[range(len(symbol_space))]*len(workspace.rotors)) 
    
    keyspace = defaultdict(dict)
    for cycle_head,L,P in product(cycle_dict.keys(),symbol_space,rotor_positions):
        workspace.stecker[cycle_head] = L
        workspace.stecker[L] = cycle_head
        
        if all(valid_cycle(workspace, P, cycle_head, c) for c in cycle_dict[cycle_head]):
            keyspace[P].setdefault(cycle_head, set())
            keyspace[P][cycle_head].add(L)
#            keyspace[(cycle_head,L)].append(P)
            print "S(%s)=%s for"%(cycle_head, L), P
        
        workspace.stecker[cycle_head] = cycle_head
        workspace.stecker[L] = L
    
    return keyspace

def guess_key(keyspace):
    '''
    Given a reduced keyspace (possible stecker connections with the corresponding
    rotor positions), attempt to guess the key
    '''
    
    P_counter = Counter()
    for P in keyspace.items():
        P_counter.update(P)
    
    
    return rotor_positions, stecker

def setup():
#    plaintext =  "OBERKOMMANDODERWEHRMACHT"
#    ciphertext = "ZMGERFEWMLKMTAWXTSWVUINZ"
    plaintext =  "OBERKOMMANDODERWEHRMACHTOBERKOMMANDODERWEHRMACHTOBERKOMMANDODERWEHRMACHT"
    
    unknown = create_enigma()
    unknown_rotor_positions = unknown.get_rotor_positions()
    rotors = deepcopy(unknown.rotors)
    reflector = deepcopy(unknown.reflector)
    
    ciphertext = unknown.encrypt(plaintext)
    print "Unknown machine with rotor positions:", unknown_rotor_positions
    print unknown
    keyspace = reduce_keyspace(rotors, reflector, plaintext, ciphertext)
    pprint(keyspace)
    return

if __name__ == '__main__':
    setup()
