Readlike
========

A Python module that provides `GNU Readline`_-like line editing functions (the
default Emacs-style ones). If you just want to use Readline, use the readline_
package in the standard library--but this package allows access to those
capabilties in settings outside of a standard CLI.

Currently, all stateless Readline commands are implemented. This means that
yanking and history aren't supported yet (but they are on the to-do list).

This module is especially well-suited to interfacing with Urwid_ due to a
shared syntax for describing key inputs.

Installation
------------

Install or upgrade to the latest version from PyPI_::

	[sudo] pip install -U readlike

Quick example
-------------

Transpose words::

	>>> import readlike
	>>> readlike.edit('perilous siege', 9, 'meta t')
	('siege perilous', 14)

.. _GNU Readline: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
.. _readline: https://docs.python.org/3/library/readline.html
.. _PyPI: https://pypi.python.org/pypi/readlike
.. _Urwid: http://urwid.org/
