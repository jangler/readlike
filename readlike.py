"""
GNU Readline-like line editing functions

Only two public functions are exposed:

    - edit(), which returns the result of a key input on a line
    - keys(), which returns key names that correspond to commands

Private functions corresponding to each implemented Readline command are
accessible by replacing hyphens in the command name with underscores and
prefixing an underscore, as in _end_of_line() for `end-of-line'.

This module is especially well-suited to interfacing with Urwid, since
the edit() function's `key' argument uses the same format that Urwid
widget keypress() methods receive.

Implemented commands and their correspondings keys are as follows:

    backward-char            ctrl b, left
    backward-delete-char     ctrl h, backspace
    backward-kill-word       ctrl meta h, meta backspace
    backward-word            meta b, meta left
    beginning-of-history     meta <
    beginning-of-line        ctrl a, home
    capitalize-word          meta c
    delete-char              ctrl d, delete
    delete-horizontal-space  meta \\
    downcase-word            meta l
    end-of-history           meta >
    end-of-line              ctrl e, end
    forward-char             ctrl f, right
    forward-word             meta f, meta right
    kill-line                ctrl k
    kill-word                meta d, meta delete
    next-history             ctrl n, down
    previous-history         ctrl p, up
    transpose-chars          ctrl t
    transpose-words          meta t
    unix-line-discard        ctrl u
    unix-word-rubout         ctrl w
    upcase-word              meta u

For more information about each command, see readline(3) or use pydoc on
the specific private functions.
"""

__all__ = ['edit', 'keys']

_histories = {}
_history_size = -1


def _backward_char(text, pos, instance=None):
    """Move pos back a character."""
    return text, max(0, pos - 1)


def _backward_delete_char(text, pos, instance=None):
    """Delete the character behind pos."""
    if pos == 0:
        return text, pos
    return text[:pos - 1] + text[pos:], pos - 1


def _backward_kill_word(text, pos, instance=None):
    """"
    Kill the word behind pos. Word boundaries are the same as those
    used by _backward_word.
    """
    text, new_pos = _backward_word(text, pos)
    return text[:new_pos] + text[pos:], new_pos


def _backward_word(text, pos, instance=None):
    """
    Move pos back to the start of the current or previous word. Words
    are composed of alphanumeric characters (letters and digits).
    """
    while pos > 0 and not text[pos - 1].isalnum():
        pos -= 1
    while pos > 0 and text[pos - 1].isalnum():
        pos -= 1
    return text, pos


def _beginning_of_history(text, pos, instance=None):
    """Move to the first line in the history."""
    raise NotImplementedError()


def _beginning_of_line(text, pos, instance=None):
    """Move pos to the start of text."""
    return text, 0


def _capitalize_word(text, pos, instance=None):
    """Capitalize the current (or following) word."""
    while pos < len(text) and not text[pos].isalnum():
        pos += 1
    if pos < len(text):
        text = text[:pos] + text[pos].upper() + text[pos + 1:]
    while pos < len(text) and text[pos].isalnum():
        pos += 1
    return text, pos


def _delete_char(text, pos, instance=None):
    """Delete the character at pos."""
    return text[:pos] + text[pos + 1:], pos


def _delete_horizontal_space(text, pos, instance=None):
    """Delete all spaces and tabs around pos."""
    while pos > 0 and text[pos - 1].isspace():
        pos -= 1
    end_pos = pos
    while end_pos < len(text) and text[end_pos].isspace():
        end_pos += 1
    return text[:pos] + text[end_pos:], pos


def _downcase_word(text, pos, instance=None):
    """Lowercase the current (or following) word."""
    text, new_pos = _forward_word(text, pos)
    return text[:pos] + text[pos:new_pos].lower() + text[new_pos:], new_pos


def _end_of_history(text, pos, instance=None):
    """
    Move to the end of the history, i.e., the line currently being
    entered.
    """
    raise NotImplementedError()


def _end_of_line(text, pos, instance=None):
    """Move pos to the end of text."""
    return text, len(text)


def _forward_char(text, pos, instance=None):
    """Move pos forward a character."""
    return text, min(pos + 1, len(text))


def _forward_word(text, pos, instance=None):
    """
    Move pos forward to the end of the next word. Words are composed of
    alphanumeric characters (letters and digits).
    """
    while pos < len(text) and not text[pos].isalnum():
        pos += 1
    while pos < len(text) and text[pos].isalnum():
        pos += 1
    return text, pos


def _kill_line(text, pos, instance=None):
    """Kill from pos to the end of text."""
    return text[:pos], pos


def _kill_word(text, pos, instance=None):
    """
    Kill from pos to the end of the current word, or if between words,
    to the end of the next word. Word boundaries are the same as those
    used by _forward_word.
    """
    text, end_pos = _forward_word(text, pos)
    return text[:pos] + text[end_pos:], pos


def _next_history(text, pos, instance=None):
    """
    Fetch the next command from the history list, moving forward in the
    list.
    """
    raise NotImplementedError()


def _previous_history(text, pos, instance=None):
    """
    Fetch the previous command from the history list, moving back in the
    list.
    """
    raise NotImplementedError()


def _transpose_chars(text, pos, instance=None):
    """
    Drag the character before pos forward over the character at pos,
    moving pos forward as well. If pos is at the end of text, then this
    transposes the two characters before pos.
    """
    if len(text) < 2 or pos == 0:
        return text, pos
    if pos == len(text):
        return text[:pos - 2] + text[pos - 1] + text[pos - 2], pos
    return text[:pos - 1] + text[pos] + text[pos - 1] + text[pos + 1:], pos + 1


def _transpose_words(text, pos, instance=None):
    """
    Drag the word before pos past the word after pos, moving pos over
    that word as well. If pos is at the end of text, this transposes the
    last two words in text.
    """
    text, end2 = _forward_word(text, pos)
    text, start2 = _backward_word(text, end2)
    text, start1 = _backward_word(text, start2)
    text, end1 = _forward_word(text, start1)
    if start1 == start2:
        return text, pos
    return text[:start1] + text[start2:end2] + text[end1:start2:] + \
        text[start1:end1] + text[end2:], end2


def _unix_line_discard(text, pos, instance=None):
    """Kill backward from pos to the beginning of text."""
    return text[pos:], 0


def _unix_word_rubout(text, pos, instance=None):
    """
    Kill the word behind pos, using white space as a word boundary.
    """
    words = text[:pos].rsplit(None, 1)
    if len(words) < 2:
        return text[pos:], 0
    else:
        index = text.rfind(words[1], 0, pos)
        return text[:index] + text[pos:], index


def _upcase_word(text, pos, instance=None):
    """Uppercase the current (or following) word."""
    text, new_pos = _forward_word(text, pos)
    return text[:pos] + text[pos:new_pos].upper() + text[new_pos:], new_pos


_key_bindings = {
    # TODO: C-I/tab (complete) - 0.3.0
    # TODO: C-Y (yank) - 0.4.0
    # TODO: M-* (insert-completions) - 0.3.0
    # TODO: M-. (yank-last-arg) - 0.4.0
    # TODO: M-C-I (tab-insert) - 0.3.0
    # TODO: M-C-Y (yank-nth-arg) - 0.4.0
    # TODO: M-C-[ (complete) - 0.3.0
    # TODO: M-Y (yank-pop) - 0.4.0
    # TODO: M-_ (yank-last-arg) - 0.4.0
    'backspace': _backward_delete_char,
    'ctrl a': _beginning_of_line,
    'ctrl b': _backward_char,
    'ctrl d': _delete_char,
    'ctrl e': _end_of_line,
    'ctrl f': _forward_char,
    'ctrl h': _backward_delete_char,
    'ctrl k': _kill_line,
    'ctrl meta h': _backward_kill_word,
    'ctrl n': _next_history,
    'ctrl p': _previous_history,
    'ctrl t': _transpose_chars,
    'ctrl u': _unix_line_discard,
    'ctrl w': _unix_word_rubout,
    'delete': _delete_char,
    'down': _next_history,
    'end': _end_of_line,
    'home': _beginning_of_line,
    'left': _backward_char,
    'meta <': _beginning_of_history,
    'meta >': _end_of_history,
    'meta \\': _delete_horizontal_space,
    'meta b': _backward_word,
    'meta backspace': _backward_kill_word,
    'meta c': _capitalize_word,
    'meta d': _kill_word,
    'meta delete': _kill_word,
    'meta f': _forward_word,
    'meta l': _downcase_word,
    'meta left': _backward_word,
    'meta right': _forward_word,
    'meta t': _transpose_words,
    'meta u': _upcase_word,
    'right': _forward_char,
    'up': _previous_history,
}

_keys = frozenset(_key_bindings.keys())


def edit(text, pos, key, instance=None):
    """
    Process a key input in the context of a line, and return the
    resulting text and cursor position.

    `text' and `key' must be of type str or unicode, and `pos' must be
    an int in the range [0, len(text)]. `instance' may be any hashable
    type, is used to control which of multiple completion/history/kill
    ring states should be used.

    If `key' is in keys(), the corresponding command is executed on the
    line. Otherwise, if `key' is a single character, that character is
    inserted at the cursor position. If neither condition is met, `text'
    and `pos' are returned unmodified.
    """
    if key in _key_bindings:
        return _key_bindings[key](text, pos, instance)
    elif len(key) == 1:
        return text[:pos] + key + text[pos:], pos + 1
    else:
        return text, pos


def history_append(text, instance=None):
    """Append `text' to the history for `instance'."""
    if instance not in _histories:
        _histories[instance] = []
    _histories[instance].append(text)
    if _history_size >= 0 and len(_histories[instance]) > n:
        _histories[instance].pop(0)


def history_size(n):
    """
    Set the maximum number of history entries saved in the history list.
    If set to zero, any existing history entries are deleted and no new
    entries are saved. If set to a value less than zero, the number of
    history entries is not limited. By default, the number of history
    entries is not limited.
    """
    global _history_size
    _history_size = n
    if n >= 0:
        for k, v in range(_histories):
            _histories[k] = v[len(v) - n:]


def keys():
    """
    Return a frozenset of strings that describe key inputs corresponding
    to line editing commands.
    """
    return _keys
