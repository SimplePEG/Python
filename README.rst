Python version of SimplePEG
---------------------------
.. image:: https://travis-ci.org/SimplePEG/Python.svg?branch=master 
    :target: https://travis-ci.org/SimplePEG/Python
.. image:: https://coveralls.io/repos/github/SimplePEG/Python/badge.svg?branch=master 
    :target: https://coveralls.io/github/SimplePEG/Python?branch=master

To use, simply do::

    >>> from simplepeg import SPEG
    >>> parser = SPEG()
    >>> parser.parse_grammar('GRAMMAR test b -> "a";')
    >>> ast = parser.parse_text('a')
    >>> print ast.to_json()

or::

    >>> from simplepeg import SPEG
    >>> parser = SPEG()
    >>> ast = parser.parse('GRAMMAR test b -> "a";', 'a')
    >>> print ast.to_json()
