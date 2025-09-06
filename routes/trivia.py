import json
from routes import app

@app.route('/trivia', methods=['GET'])
def trivia():
    answers = [
        3,  # Q1: "Trivia!" → 1 challenge ending with "!"
        1,  # Q2: "Ticketing Agent" → Concert
        2,  # Q3: "Blankety Blanks" → 100 lists x 1000 elements
        2,  # Q4: "Princess Diaries" → Fat Louie
        3,  # Q5: "MST Calculation" → 8
        4,  # Q6: "UBS Surveillance" → Amy Winehouse
        1,  # Q7: "Operation Safeguard" → 4px
        # 1,  # Q8: "Capture The Flag" → all are valid anagrams
        # 4   # Q9: "Filler 1" → Hong Kong, Singapore
    ]
    return json.dumps({"answers": answers})
