def test_short_phrase():
    phrase = input("Set a phrase: ")
    expected_len = 15
    assert len(phrase) < expected_len, f"Frase is equal or more {expected_len}"
