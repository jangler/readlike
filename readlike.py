"""This module provides access to GNU Readline-like line editing functions."""

__all__ = ['edit', 'keys']


def _backward_char(text, pos):
    # move back a character.
    return text, max(0, pos - 1)


def _backward_delete_char(text, pos):
    # delete the character behind the cursor.
    if pos == 0:
        return text, pos
    return text[:pos - 1] + text[pos:], pos - 1


def _beginning_of_line(text, pos):
    # move to the start of the current line.
    return text, 0


def _delete_char(text, pos):
    # delete the character at pos.
    return text[:pos] + text[pos + 1:], pos


def _forward_char(text, pos):
    # move forward a character.
    return text, min(pos + 1, len(text))


def _kill_line(text, pos):
    # kill the text from pos to the end of the line.
    return text[:pos], pos


def _transpose_chars(text, pos):
    # drag the character before pos forward over the character at pos, moving
    # pos forward as well. if point is at the end of the line, then this
    # transposes the two characters before point.
    if len(text) < 2 or pos == 0:
        return text, pos
    if pos == len(text):
        return text[:pos - 2] + text[pos - 1] + text[pos - 2], pos
    return text[:pos - 1] + text[pos] + text[pos - 1] + text[pos + 1:], pos + 1


def _unix_line_discard(text, pos):
    # kill backward from pos to the beginning of the line.
    return text[pos:], 0


def _unix_word_rubout(text, pos):
    # kill the word behind pos, using white space as a word boundary.
    words = text[:pos].rsplit(None, 1)
    if len(words) < 2:
        return text[pos:], 0
    else:
        index = text.rfind(words[1], 0, pos)
        return text[:index] + text[pos:], index


_key_bindings = {
    # not implemented: C-@ (set-mark)
    'ctrl a': _beginning_of_line,
    'ctrl b': _backward_char,
    'ctrl d': _delete_char,
    'ctrl f': _forward_char,
    # not implemented: C-G (abort)
    'ctrl h': _backward_delete_char,
    # not implemented: C-I (complete)
    # not implemented: C-J (accept-line)
    'ctrl k': _kill_line,
    # not implemented: C-L (clear-screen)
    # not implemented: C-M (accept-line)
    # not implemented: C-N (next-history)
    # not implemented: C-P (previous-history)
    # not implemented: C-Q (quoted-insert)
    # not implemented: C-R (reverse-search-history)
    # not implemented: C-S (forward-search-history)
    'ctrl t': _transpose_chars,
    'ctrl u': _unix_line_discard,
    # not implemented: C-V (quoted-insert)
    'ctrl w': _unix_word_rubout,
    # not implemented: C-Y (yank)
    # not implemented: C-] (character-search)
    # not implemented: C-_ (undo)?
    # not implemented: C-? (backward-delete-char)
}

_keys = frozenset(_key_bindings.keys())


def edit(text, pos, key):
    """Process the key and return the resulting text and cursor position."""
    if key in _key_bindings:
        return _key_bindings[key](text, pos)
    elif len(key) == 1:
        return text[:pos] + key + text[pos:], pos + 1
    else:
        return text, pos


def keys():
    """Return a frozenset of supported key strings."""
    return _keys
