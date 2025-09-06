import json
import logging
from flask import request, jsonify
from routes import app

logger = logging.getLogger(__name__)

def solve_part_one(part_one):
    ratios = part_one["ratios"]
    goods = part_one["goods"]

    """
    4 goods -> small graph -> dfs brute force 
    check all cycles up to length 4 
    if final amt > 1, record path and gain 
    """
    # Build adjacency dict
    graph = {i: [] for i in range(len(goods))} # add nodes 
    for u, v, rate in ratios:
        graph[int(u)].append((int(v), rate)) # add edges 

    best_gain = 1.0
    best_path = []

    def dfs(start, current, visited, product, path):
        nonlocal best_gain, best_path
        if len(path) > 1 and current == start:
            if product > best_gain:
                best_gain = product
                best_path = [goods[i] for i in path]
            return
        if len(path) > len(goods):  # stop at length 5, visited every node and returned, cannot go anymore
            return
        for nxt, rate in graph[current]:
            dfs(start, nxt, visited, product * rate, path + [nxt])

    for i in range(len(goods)):
        dfs(i, i, set(), 1.0, [i])

    return best_path, (best_gain - 1) * 100


def solve_part_two(part_two):
    return [], 0.0

@app.route('/The-Ink-Archive', methods=['POST'])
def evaluate_inkarchive():
    data = request.get_json()  
    part_one = data[0]
    part_two = data[1]
    path_one, gain_one = solve_part_one(part_one)
    path_two, gain_two = solve_part_two(part_two)
    output = [
        {"path": path_one, "gain": gain_one},
        {"path": path_two, "gain": gain_two}
    ]

    return output