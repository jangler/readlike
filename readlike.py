"""
This module provides access to GNU Readline-like line editing functions.
"""

__all__ = ['edit', 'keys']


def _backward_char(text, pos):
    # Move pos back a character.
    return text, max(0, pos - 1)


def _backward_delete_char(text, pos):
    # Delete the character behind pos.
    if pos == 0:
        return text, pos
    return text[:pos - 1] + text[pos:], pos - 1


def _backward_kill_word(text, pos):
    # Kill the word behind pos. Word boundaries are the same as those
    # used by _backward_word.
    text, new_pos = _backward_word(text, pos)
    return text[:new_pos] + text[pos:], new_pos


def _backward_word(text, pos):
    # Move pos back to the start of the current or previous word. Words
    # are composed of alphanumeric characters (letters and digits).
    while pos > 0 and not text[pos - 1].isalnum():
        pos -= 1
    while pos > 0 and text[pos - 1].isalnum():
        pos -= 1
    return text, pos


def _beginning_of_line(text, pos):
    # Move pos to the start of text.
    return text, 0


def _capitalize_word(text, pos):
    # Capitalize the current (or following) word.
    while pos < len(text) and not text[pos].isalnum():
        pos += 1
    if pos < len(text):
        text = text[:pos] + text[pos].upper() + text[pos + 1:]
    while pos < len(text) and text[pos].isalnum():
        pos += 1
    return text, pos


def _delete_char(text, pos):
    # Delete the character at pos.
    return text[:pos] + text[pos + 1:], pos


def _delete_horizontal_space(text, pos):
    # Delete all spaces and tabs around pos.
    while pos > 0 and text[pos - 1].isspace():
        pos -= 1
    end_pos = pos
    while end_pos < len(text) and text[end_pos].isspace():
        end_pos += 1
    return text[:pos] + text[end_pos:], pos


def _downcase_word(text, pos):
    # Lowercase the current (or following) word.
    text, new_pos = _forward_word(text, pos)
    return text[:pos] + text[pos:new_pos].lower() + text[new_pos:], new_pos


def _forward_char(text, pos):
    # Move pos forward a character.
    return text, min(pos + 1, len(text))


def _forward_word(text, pos):
    # Move pos forward to the end of the next word. Words are composed
    # of alphanumeric characters (letters and digits).
    while pos < len(text) and not text[pos].isalnum():
        pos += 1
    while pos < len(text) and text[pos].isalnum():
        pos += 1
    return text, pos


def _kill_line(text, pos):
    # Kill from pos to the end of text.
    return text[:pos], pos


def _kill_word(text, pos):
    # Kill from pos to the end of the current word, or if between words,
    # to the end of the next word. Word boundaries are the same as those
    # used by _forward_word.
    text, end_pos = _forward_word(text, pos)
    return text[:pos] + text[end_pos:], pos


def _transpose_chars(text, pos):
    # Drag the character before pos forward over the character at pos,
    # moving pos forward as well. If pos is at the end of text, then
    # this transposes the two characters before pos.
    if len(text) < 2 or pos == 0:
        return text, pos
    if pos == len(text):
        return text[:pos - 2] + text[pos - 1] + text[pos - 2], pos
    return text[:pos - 1] + text[pos] + text[pos - 1] + text[pos + 1:], pos + 1


def _transpose_words(text, pos):
    # Drag the word before pos past the word after pos, moving pos over
    # that word as well. If pos is at the end of text, this transposes
    # the last two words in text.
    text, end2 = _forward_word(text, pos)
    text, start2 = _backward_word(text, end2)
    text, start1 = _backward_word(text, start2)
    text, end1 = _forward_word(text, start1)
    if start1 == start2:
        return text, pos
    return text[:start1] + text[start2:end2] + text[end1:start2:] + \
        text[start1:end1] + text[end2:], end2


def _unix_line_discard(text, pos):
    # Kill backward from pos to the beginning of text.
    return text[pos:], 0


def _unix_word_rubout(text, pos):
    # Kill the word behind pos, using white space as a word boundary.
    words = text[:pos].rsplit(None, 1)
    if len(words) < 2:
        return text[pos:], 0
    else:
        index = text.rfind(words[1], 0, pos)
        return text[:index] + text[pos:], index


def _upcase_word(text, pos):
    # Uppercase the current (or following) word.
    text, new_pos = _forward_word(text, pos)
    return text[:pos] + text[pos:new_pos].upper() + text[new_pos:], new_pos


_key_bindings = {
    'ctrl a': _beginning_of_line,
    'ctrl b': _backward_char,
    'ctrl d': _delete_char,
    'ctrl f': _forward_char,
    'ctrl h': _backward_delete_char,
    'backspace': _backward_delete_char,
    # TODO: C-I/tab (complete) - 0.2.0
    'ctrl k': _kill_line,
    # TODO: C-N (next-history) - 0.2.0
    # TODO: C-P (previous-history) - 0.2.0
    'ctrl t': _transpose_chars,
    'ctrl u': _unix_line_discard,
    'ctrl w': _unix_word_rubout,
    # TODO: C-Y (yank) - 0.3.0
    'ctrl meta h': _backward_kill_word,
    'meta backspace': _backward_kill_word,
    # TODO: M-C-I (tab-insert) - 0.2.0
    # TODO: M-C-Y (yank-nth-arg) - 0.3.0
    # TODO: M-C-[ (complete) - 0.2.0
    # TODO: M-* (insert-completions) - 0.2.0
    # TODO: M-. (yank-last-arg) - 0.3.0
    # TODO: M-< (beginning-of-history) - 0.2.0
    # TODO: M-> (end-of-history) - 0.2.0
    'meta b': _backward_word,
    'meta c': _capitalize_word,
    'meta d': _kill_word,
    'meta f': _forward_word,
    'meta l': _downcase_word,
    'meta t': _transpose_words,
    'meta u': _upcase_word,
    # TODO: M-Y (yank-pop) - 0.3.0
    'meta \\': _delete_horizontal_space,
    # TODO: M-_ (yank-last-arg) - 0.3.0
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
