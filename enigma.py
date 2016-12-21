'''
Created on Aug 4, 2012

@author: vinnie
'''


class Rotor(object):
    def __init__(self, symbols, permutation):
        '''
        
        '''
        self.states = []
        self.inverse_states = []
        self.n_symbols = len(symbols)
        for i in range(self.n_symbols):
            self.states.append({symbols[j]: permutation[(j + i) % self.n_symbols] for j in range(self.n_symbols)})
            self.inverse_states.append(
                {permutation[(j + i) % self.n_symbols]: symbols[j] for j in range(self.n_symbols)})
        self.odometer = 0
        return

    def state(self):
        '''
        Get the current encryption state
        '''
        return self.states[self.odometer]

    def inverse_state(self):
        '''
        Get the current decryption state
        '''
        return self.inverse_states[self.odometer]

    def step(self):
        '''
        Advance the rotor by one step.
        This is equivalent to shifting the offsets
        '''
        self.odometer = (self.odometer + 1) % self.n_symbols
        return

    def setOdometer(self, position):
        '''
        
        '''
        self.odometer = position % self.n_symbols

    def permute(self, symbol):
        '''
        Encrypt a symbol in the current state 
        '''
        return self.states[self.odometer][symbol]

    def invert(self, symbol):
        '''
        Decrypt a symbol in the current state 
        '''
        return self.inverse_states[self.odometer][symbol]

    def __str__(self, *args, **kwargs):
        output = "Permute\tInvert\n"
        for k in self.states[self.odometer].keys():
            output += "%s => %s\t%s => %s\n" \
                      % (str(k), self.states[self.odometer][k],
                         str(k), self.inverse_states[self.odometer][k])
        return output


class Enigma(object):
    '''
    The Enigma cipher
    '''

    def __init__(self, rotors, reflector):
        '''
        
        '''

        self.stecker = {}
        self.dec_stecker = {}
        self.rotors = rotors  # rotors go from left to right
        self.reflector = reflector
        self.dec_reflector = {reflector[s]: s for s in reflector.keys()}
        self.odometer_start = []

    def configure(self, stecker, odometer_start):
        '''
        
        '''
        assert len(odometer_start) == len(self.rotors) - 1

        self.stecker = stecker
        self.dec_stecker = {stecker[s]: s for s in stecker.keys()}
        self.odometer_start = odometer_start

        return

    def set_rotor_positions(self, rotor_positions):
        '''
        
        '''
        for r, p in zip(self.rotors, rotor_positions):
            r.setOdometer(p)
        return

    def get_rotor_positions(self):
        '''
        
        '''
        return [r.odometer for r in self.rotors]

    def step_to(self, P):

        for i in range(P):
            self.step_rotors()
        return

    def step_rotors(self):
        '''
        
        '''
        # step the rightmost rotor
        self.rotors[0].step()

        # step the remaining rotors in an odometer-like fashion
        for i in range(len(self.odometer_start)):
            if self.rotors[i + 1].odometer == self.odometer_start[i]:
                self.rotors[i + 1].step()

        return

    def translate_rotors(self, c):
        '''
        
        '''
        for r in self.rotors:
            c = r.permute(c)

        c = self.reflector[c]

        for r in reversed(self.rotors):
            c = r.invert(c)

        return c

    def encrypt(self, str):
        '''
        
        '''
        enc = ""
        for c in str:
            e = self.stecker[c]
            e = self.translate_rotors(e)
            e = self.stecker[e]
            self.step_rotors()
            enc += e
        return enc

    def decrypt(self, enc):
        '''
        The same function is used to both encrypt and decrypt.
        '''
        return self.encrypt(enc)

    def __str__(self, *args, **kwargs):
        output = ""
        for s in sorted(self.reflector.keys()):
            output += "%s => %s | " % (str(s), self.stecker[s])
            for r in self.rotors:
                output += "%s => %s  " % (str(s), r.permute(s))
                output += "%s => %s | " % (str(s), r.invert(s))
            output += "%s => %s" % (str(s), self.reflector[s])
            output += "\n"
        return output
