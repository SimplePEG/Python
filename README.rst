Python version of SimplePEG
--------

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