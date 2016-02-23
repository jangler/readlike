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

Commands
--------

Implemented commands and their correspondings keys are as follows::

    backward-char            ctrl b, left
    backward-delete-char     ctrl h, backspace
    backward-kill-word       ctrl meta h, meta backspace
    backward-word            meta b, meta left
    beginning-of-line        ctrl a, home
    capitalize-word          meta c
    delete-char              ctrl d, delete
    delete-horizontal-space  meta \\
    downcase-word            meta l
    end-of-line              ctrl e, end
    forward-char             ctrl f, right
    forward-word             meta f, meta right
    kill-line                ctrl k
    kill-word                meta d, meta delete
    transpose-chars          ctrl t
    transpose-words          meta t
    unix-line-discard        ctrl u
    unix-word-rubout         ctrl w
    upcase-word              meta u

For more information about each command, see readline(3) or see the doc
strings in readlike.py_.

Projects using Readlike
-----------------------

- hangups_

.. _GNU Readline: http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html
.. _readline: https://docs.python.org/3/library/readline.html
.. _PyPI: https://pypi.python.org/pypi/readlike
.. _Urwid: http://urwid.org/
.. _readlike.py: https://github.com/jangler/readlike/blob/master/readlike.py
.. _hangups: https://github.com/tdryer/hangups
