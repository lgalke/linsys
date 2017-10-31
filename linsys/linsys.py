"""
Module for Lindenmayer system implementation
>>> algae = Lsys({'A': 'AB', 'B': 'A'})
>>> algae.variables() == algae.alphabet() == {'A', 'B'}
True
>>> algae.constants() == set()  # no terminal symbols
True
>>> algae('AB')
'ABA'
>>> gen = algae.iter('A')
>>> next(gen)
'A'
>>> next(gen)
'AB'
>>> next(gen)
'ABA'
>>> next(gen)
'ABAAB'
>>> next(gen)
'ABAABABA'
>>> next(gen)
'ABAABABAABAAB'
>>> next(gen)
'ABAABABAABAABABAABABA'
>>> next(gen)
'ABAABABAABAABABAABABAABAABABAABAAB'
"""

from collections import Counter


def _check_production_rule(p):
    if len(p) != 1:
        raise ValueError("Multiple symbols on LHS of production!")


class Lsys(dict):
    """ Class for Lindenmayer systems, specified by a set of rules """
    def __init__(self, P):
        """
        Arguments
        =========

        p:
            dictionary specifying production rules


        >>> algae = Lsys({'A': 'AB', 'B': 'A'})
        >>> algae['A']
        'AB'
        >>> algae['B']
        'A'
        >>> algae['X'] # should not be replaced
        'X'
        """
        for p in P:
            _check_production_rule(p)
        super(Lsys, self).__init__(P)

    def __missing__(self, key):
        return key

    def __setitem__(self, key, value):
        """
        >>> d = Lsys({'A': 'B'})
        >>> d['BB'] = 'C'
        Traceback (most recent call last):
          File "/usr/lib64/python3.6/doctest.py", line 1330, in __run
            compileflags, 1), test.globs)
          File "<doctest __main__.Lsys.__setitem__[1]>", line 1, in <module>
            d['BB'] = 'C'
          File "linsys.py", line 55, in __setitem__
            _check_production_rule(key)
          File "linsys.py", line 8, in _check_production_rule
            raise ValueError("Multiple symbols on LHS of production!")
        ValueError: Multiple symbols on LHS of production!
        >>> d['B'] = ''
        >>> d.constants()
        set()
        """
        _check_production_rule(key)
        super(Lsys, self).__setitem__(key, value)

    def variables(self):
        """
        Return set of variables, do not cache, rules may have changed
        >>> l = Lsys({'S': 'BB'})
        >>> l.variables()
        {'S'}
        >>> l['B'] = 'X'
        >>> l.variables() == {'S', 'B'}
        True
        """
        # Keys are only allowed to be single symbols
        return set(self.keys())

    def constants(self):
        """
        >>> l = Lsys({'S': 'SB'})
        >>> l.constants()
        {'B'}
        """
        # Values may have multiple symbols
        return set(''.join(self.values())) - self.variables()

    def alphabet(self):
        """
        Returns the alphabet (variables and constants)
        >>> l = Lsys({'S': 'BB'})
        >>> l.alphabet() == {'S', 'B'}
        True
        """
        return self.variables() | self.constants()

    def __call__(self, input):
        """
        >>> algae = Lsys({'A': 'AB', 'B': 'A'})
        >>> it = algae('A')
        >>> it
        'AB'
        >>> it = algae(it)
        >>> it
        'ABA'
        """
        symbols, output = str(input), ''
        for symbol in symbols:
            output += self[symbol]
        return output

    def apply(self, input, n=1):
        """
        Apply :code:`self` to :code:`input` :code:`n` times.
        """
        for __ in range(n):
            input = self(input)
        return input

    def count_variables(self, input):
        """
        Counts the occurrences of any variables.
        >>> d = Lsys({'A': 'B', 'C': 'D'})
        >>> d.count_variables('AACCB')
        4
        >>> d.count_variables('BBBDDD')
        0
        """
        c = Counter(input)
        return sum(c[v] for v in self.variables())

    def contains_variable(self, input):
        """ Faster than count_variables > 0 for checking an input
        >>> d = Lsys({'A': 'B', 'C': 'D'})
        >>> d.contains_variable('XXXXABC')
        True
        >>> d.contains_variable('XXXXX')
        False
        >>> d.contains_variable('BDBDBDBDBD')
        False
        >>> d.contains_variable('XAXA')
        True
        >>> d.contains_variable('')
        False
        """
        for v in self.variables():
            if v in input:
                return True
        else:
            return False

    def iter(self, input):
        """
        Iterate through applications of production rules with axiom omega

        Arguments
        =========
        input: initial state
        >>> algae = Lsys({'A': 'AB', 'B': 'A'})
        >>> gen = algae.iter('A')
        >>> next(gen)
        'A'
        >>> next(gen)
        'AB'
        >>> next(gen)
        'ABA'
        >>> algae['A'] = 'X'
        >>> algae['B'] = 'X'
        >>> next(gen)
        'XXX'
        >>> next(gen)
        Traceback (most recent call last):
          File "/usr/lib64/python3.6/doctest.py", line 1330, in __run
            compileflags, 1), test.globs)
          File "<doctest __main__.Lsys.iter[7]>", line 1, in <module>
            next(gen)
        StopIteration
        """
        yield input
        while self.contains_variable(input):
            input = self(input)
            yield input



if __name__ == '__main__':
    import doctest
    doctest.testmod()
    algae = Lsys({'A': 'AB', 'B': 'A'})
    for i, state in enumerate(algae.iter('A')):
        print(i, state)
        input()
