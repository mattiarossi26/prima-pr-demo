from string_utils import capitalize_words, reverse_words


def test_capitalize_words():
    assert capitalize_words("ciao mondo") == "Ciao Mondo"


def test_reverse_words():
    assert reverse_words("uno due tre") == "tre due uno"
