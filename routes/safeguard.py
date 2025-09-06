import json
import logging
from flask import request, jsonify
from routes import app
from collections import OrderedDict

logger = logging.getLogger(__name__)
def mirror_words_decode(x):
    return " ".join(word[::-1] for word in x.split())

def encode_mirror_alphabet_decode(x):
    def mirror_char(c):
        if c.islower():
            return chr(219 - ord(c))  # 'a' ↔ 'z'
        elif c.isupper():
            return chr(155 - ord(c))  # 'A' ↔ 'Z'
        else:
            return c
    return "".join(mirror_char(c) for c in x)

def toggle_case_decode(x):
    return x.swapcase()

def swap_pairs_decode(x):
    def swap_word(w):
        chars = list(w)
        for i in range(0, len(chars) - 1, 2):
            chars[i], chars[i+1] = chars[i+1], chars[i]
        return "".join(chars)
    return " ".join(swap_word(word) for word in x.split())

def encode_index_parity_decode(x):
    def reorder_word(w):
        n = len(w)
        even_count = (n + 1) // 2
        even_chars = w[:even_count]
        odd_chars = w[even_count:]
        res = [''] * n
        res[::2] = even_chars
        res[1::2] = odd_chars
        return "".join(res)
    return " ".join(reorder_word(word) for word in x.split())

def double_consonants_decode(x):
    vowels = "aeiouAEIOU"
    res = []
    i = 0
    while i < len(x):
        c = x[i]
        if c.isalpha() and c not in vowels:
            # If next char is same consonant, skip one
            if i + 1 < len(x) and x[i+1] == c:
                res.append(c)
                i += 2
                continue
        res.append(c)
        i += 1
    return "".join(res)

def solve_one(transformations, encrypted_word):

    # step 1 - expand nested transformations, 
    cleaned = transformations[1:-1]
    cleaned = cleaned.split(", ")[::-1]
    expanded = []
    for transformation in cleaned:
        parts = transformation.split("(")
        for part in parts[:-1]:
            expanded.append(part.strip())
    print(expanded)
    res = encrypted_word
    for transformation in expanded:
        if transformation == "mirror_words":
            res = mirror_words_decode(res)
        elif transformation == "encode_mirror_alphabet":
            res = encode_mirror_alphabet_decode(res)
        elif transformation == "toggle_case":
            res = toggle_case_decode(res)
        elif transformation == "swap_pairs":
            res = swap_pairs_decode(res)
        elif transformation == "encode_index_parity":
            res = encode_index_parity_decode(res)
        elif transformation == "double_consonants":
            res = double_consonants_decode(res)
        else:
            print(f"Unknown function '{transformation}'")

    return res



@app.route('/operation-safeguard', methods=['POST'])
def process_items():
    data = request.get_json()  
    output = {}

    challenge_one_data = data.get("challenge_one", "sos")
    transformations = challenge_one_data.get("transformations")
    encrypted_word = challenge_one_data.get("transformed_encrypted_word")
    challenge_one_res = solve_one(transformations, encrypted_word)

    output = {
        "challenge_one": challenge_one_res,
        "challenge_two": "abc",
        "challenge_three": "def",
        "challenge_four": "looking for answers",
    }
    # output = OrderedDict()
    # output["challenge_one"] = challenge_one_res
    # output["challenge_two"] = "abc"
    # output["challenge_three"] = "def"
    # output["challenge_four"] = "looking for answers"

    return output