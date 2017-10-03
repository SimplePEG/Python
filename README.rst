Python version of SimplePEG
---------------------------

A very simple implementation of `PEG <https://en.wikipedia.org/wiki/Parsing_expression_grammar>`_ parser generator.

.. image:: https://badges.gitter.im/SimplePEG/Python.svg
   :alt: Join the chat at https://gitter.im/SimplePEG/Python
   :target: https://gitter.im/SimplePEG/Python?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. image:: https://travis-ci.org/SimplePEG/Python.svg?branch=master 
    :target: https://travis-ci.org/SimplePEG/Python
.. image:: https://coveralls.io/repos/github/SimplePEG/Python/badge.svg?branch=master 
    :target: https://coveralls.io/github/SimplePEG/Python?branch=master

To use, simply do

.. code-block:: python

    from simplepeg import SPEG
    parser = SPEG()
    parser.parse_grammar('GRAMMAR test b -> "a";')
    ast = parser.parse_text('a')
    print ast.to_json()

or

.. code-block:: python

    from simplepeg import SPEG
    parser = SPEG()
    ast = parser.parse('GRAMMAR test b -> "a";', 'a')
    print ast.to_json()

Grammar Example
-------------------------------
url.peg

.. code-block::

    GRAMMAR url

    url       ->  scheme "://" host pathname search hash?;
    scheme    ->  "http" "s"?;
    host      ->  hostname port?;
    hostname  ->  segment ("." segment)*;
    segment   ->  [a-z0-9-]+;
    port      ->  ":" [0-9]+;
    pathname  ->  "/" [^ ?]*;
    search    ->  ("?" [^ #]*)?;
    hash      ->  "#" [^ ]*;
