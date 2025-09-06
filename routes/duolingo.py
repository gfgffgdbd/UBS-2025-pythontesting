import json
import logging
from flask import Flask, request, jsonify

from routes import app

logger = logging.getLogger(__name__)

# ------------------- Roman numeral conversion -------------------
roman_map = {
    'M': 1000, 'D': 500, 'C': 100, 'L': 50,
    'X': 10, 'V': 5, 'I': 1
}

def roman_to_int(roman_numeral_str):
    result = 0
    i = 0
    while i < len(roman_numeral_str):
        current_value = roman_map[roman_numeral_str[i]]
        if i + 1 < len(roman_numeral_str):
            next_value = roman_map[roman_numeral_str[i+1]]
            if current_value < next_value:
                result += (next_value - current_value)
                i += 2  # Skip both current and next characters
            else:
                result += current_value
                i += 1
        else:
            result += current_value
            i += 1
    return result

# ------------------- English number conversion -------------------
numwords = {}
units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

#building the dictionary
numwords.update({word: idx for idx, word in enumerate(units)})
numwords.update({word: 10 * (idx) for idx, word in enumerate(tens) if word})

numwords["hundred"] = 100
numwords["thousand"] = 1000
numwords["million"] = 1000000
numwords["billion"] = 1000000000

def english_to_int(textnum):
    #removes any - for standardisation
    textnum = textnum.replace('-', ' ')
    current = result = 0
    for word in textnum.split():
        if word not in numwords:
            continue
        scale = numwords[word]
        if scale == 100:
            current *= scale
        elif scale >= 1000:
            current *= scale
            result += current
            current = 0
        else:
            current += scale
    return result + current

# ------------------- German number conversion -------------------
units_de = {
    "null":0, "eins":1, "ein":1, "zwei":2, "drei":3, "vier":4, "fünf":5, "sechs":6, "sieben":7,
    "acht":8, "neun":9, "zehn":10, "elf":11, "zwölf":12, "dreizehn":13, "vierzehn":14,
    "fünfzehn":15, "sechzehn":16, "siebzehn":17, "achtzehn":18, "neunzehn":19
}

tens_de = {
    "zwanzig":20, "dreißig":30, "vierzig":40, "fünfzig":50,
    "sechzig":60, "siebzig":70, "achtzig":80, "neunzig":90
}

def german_to_int(word):
    word = word.lower()
    if word in units_de:
        return units_de[word]
    if word in tens_de:
        return tens_de[word]
    if "hundert" in word:
        parts = word.split("hundert")
        h = 1 if parts[0] in ("", "ein", "eins") else units_de.get(parts[0], 0)
        rest = german_to_int(parts[1]) if parts[1] else 0
        return h * 100 + rest
    if "und" in word:
        parts = word.split("und")
        left = units_de.get(parts[0], 0)
        right = tens_de.get(parts[1], 0)
        return left + right
    return 0

# ------------------- Chinese number conversion -------------------
chinese_digits = {
    '零':0,'一':1,'二':2,'三':3,'四':4,'五':5,'六':6,'七':7,'八':8,'九':9,
    '〇':0,'两':2
}

chinese_units = {
    '十':10,'百':100,'千':1000,'萬':10000,'万':10000,'億':100000000,'亿':100000000
}

def chinese_to_int(ch):
    total, section, number = 0, 0, 0
    for c in ch:
        if c in chinese_digits:
            number = chinese_digits[c]
        elif c in chinese_units:
            unit = chinese_units[c]
            if unit >= 10000:
                section = (section + number) * unit
                total += section
                section = 0
            else:
                section += number * unit
            number = 0
    return total + section + number

# ------------------- Detect language & convert -------------------
import re

def detect_and_convert(s):
    if s.isdigit():
        return int(s), "arabic"
    if re.fullmatch(r"[IVXLCDM]+", s):
        return roman_to_int(s), "roman"
    if re.search(r"[零一二三四五六七八九十百千萬亿億万兩两]", s):
        if "萬" in s or "億" in s:
            return chinese_to_int(s), "traditional"
        else:
            return chinese_to_int(s), "simplified"
    if any(w in s for w in numwords):
        return english_to_int(s), "english"
    if re.search(r"[a-zA-Zäöüß]", s):
        return german_to_int(s), "german"
    return 0, "arabic"

# ------------------- Main solver -------------------
order_priority = {
    "roman": 0,
    "english": 1,
    "traditional": 2,
    "simplified": 3,
    "german": 4,
    "arabic": 5
}

def solve(payload):
    part = payload["part"]
    unsorted_list = payload["challengeInput"]["unsortedList"]

    if part == "ONE":
        parsed = []
        for item in unsorted_list:
            if item.isdigit():
                parsed.append(int(item))
            else:
                parsed.append(roman_to_int(item))
        parsed.sort()
        return {"sortedList": [str(x) for x in parsed]}

    elif part == "TWO":
        parsed = []
        for item in unsorted_list:
            val, lang = detect_and_convert(item)
            parsed.append((val, order_priority[lang], item))
        parsed.sort(key=lambda x: (x[0], x[1]))
        return {"sortedList": [x[2] for x in parsed]}

# ------------------- Flask Endpoint -------------------
@app.route('/duolingo-sort', methods=['POST'])
def duolingo_sort():
    try:
        data = request.get_json(force=True)
        if data is None:
            logger.warning("No JSON data received")
            return jsonify({"sortedList": []}), 200

        result = solve(data)
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({"sortedList": []}), 200

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json'
    return response
