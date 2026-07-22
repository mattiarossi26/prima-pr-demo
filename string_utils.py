def capitalize_words(text):
    return " ".join(word.capitalize() for word in text.split())


def reverse_words(text):
    return " ".join(reversed(text.split()))


def is_palindrome(text):
    normalized = "".join(text.lower().split())
    return normalized == normalized[::-1]
