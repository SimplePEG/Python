Python version of SimplePEG
--------

To use, simply do::

    >>> import SPEG from simplepeg
    >>> parser = s.SPEG()
    >>> # will throw Exception if grammar is invalid
    >>> parser.parse_grammar('GRAMMAR test b -> "a";')
    >>> # will throw Exception if text have invalid grammar
    >>> ast = parser.parse_text('a')
    >>> print ast.to_json()

or::

    >>> import SPEG from simplepeg
    >>> parser = s.SPEG()
    >>> ast = parser.parse('GRAMMAR test b -> "a";', 'a')
    >>> print ast.to_json()