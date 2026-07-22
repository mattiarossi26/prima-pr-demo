from string_utils import capitalize_words, reverse_words, is_palindrome


def test_capitalize_words():
    assert capitalize_words("ciao mondo") == "Ciao Mondo"


def test_reverse_words():
    assert reverse_words("uno due tre") == "tre due uno"


def test_is_palindrome_true():
    assert is_palindrome("anna") is True
    assert is_palindrome("a nna") is True


def test_is_palindrome_false():
    assert is_palindrome("ciao") is False
