import json
import logging
from flask import request
from routes import app

def solve_sailing_one(testcase):
    input = testcase["input"]
    input.sort(key=lambda x: x[0])

    merged = []
    for interval in input:
        if not merged:
            merged.append(interval)
        else:
            last = merged[-1]
            if interval[0] <= last[1]:  
                last[1] = max(last[1], interval[1]) 
            else:
                merged.append(interval)

    return merged

def solve_sailing_two(testcase):
    input = testcase["input"]

    if not input:
        return 0

    starts = sorted(interval[0] for interval in input)
    ends = sorted(interval[1] for interval in input)

    max_boats = 0
    current_boats = 0
    i = j = 0
    n = len(input)

    while i < n:
        if starts[i] < ends[j]: 
            current_boats += 1
            max_boats = max(max_boats, current_boats)
            i += 1
        else: 
            current_boats -= 1
            j += 1

    return max_boats

def solve_sailing(testcase):
    case_id = testcase["id"]
    merged = solve_sailing_one(testcase)
    boats = solve_sailing_two(testcase)

    return {
        "id": case_id,
        "sortedMergedSlots": merged,
        "minBoatsNeeded": boats
    }

@app.route('/', methods=['POST'])
def evaluate_sailing():
    data = request.get_json()  
    solutions = []
    for testcase in data["testCases"]:
        solutions.append(solve_sailing(testcase))
    return {"solutions": solutions}


# testcase1 = {
#             "id": "0000",
#             "input": [
#                 [15, 28], [49, 57], [8, 13], [51, 62], [16, 28], [66, 73], [83, 94], [44, 62], [69, 70], [4, 6]
#             ],
#         }
# testcase2 = {
#             "id": "0004",
#             "input": [
#                 [45, 62], [53, 62], [53, 62], [46, 48], [78, 86], [72, 73], [80, 90], [47, 54], [77, 90], [1, 5]
#             ],
#         }
# print(solve_sailing_one(testcase1))
# print(solve_sailing_two(testcase1))
# print(solve_sailing_one(testcase2))
# print(solve_sailing_two(testcase2))
