# linsys

[Lindenmayer systems](https://en.wikipedia.org/wiki/L-system) in python.


## Usage

1. Specify an L-system by its production rules

```python
>>> algae = Lsys({'A': 'AB'})
```

1. Alphabet consisting of both variables and constants is inferred from the rules.

```python
>>> algae.variables() == {'A'}
True
>>> algae.constants() == {'B'}
True
>>> algae.alphabet() == {'A', 'B'}
True
```

1. Apply the (for now) single rule

```python
>>> algae('A')
'AB'
```

1. Add another production rule

```python
algae['B'] = 'A'
algae.variables == {'A', 'B'}
True
```

1. Apply the production rules to some string

```python
>>> algae('AB')
'ABA'
```

1. Or iterate over the applications of rules

```python
for i, state in enumerate(algae.iter('A')):
    print(i, state)
```

```sh
0 A
1 AB
2 ABA
3 ABAAB
4 ABAABABA
5 ABAABABAABAAB
6 ABAABABAABAABABAABABA
7 ABAABABAABAABABAABABAABAABABAABAAB
...
```
