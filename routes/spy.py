import json
import logging
from flask import request
from routes import app

# Configure logging to print to console
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

def find_cycles(edges):
    from collections import defaultdict

    graph = defaultdict(list)
    for edge in edges:
        graph[edge['spy1']].append((edge['spy2'], edge))
        graph[edge['spy2']].append((edge['spy1'], edge))

    visited = set()
    parent = {}
    cycle_edges = set()

    def dfs(node, par):
        visited.add(node)
        for neighbor, edge in graph[node]:
            if neighbor == par:
                continue
            if neighbor in visited:
                # reconstruct the cycle path from node -> ... -> neighbor
                cur = node
                while cur is not None and cur != neighbor:
                    prev = parent[cur]
                    if prev is None:  # stop at root
                        break
                    key = tuple(sorted((cur, prev)))
                    cycle_edges.add(key)
                    cur = prev
                # also add the back edge itself
                cycle_edges.add(tuple(sorted((node, neighbor))))
            else:
                parent[neighbor] = node
                dfs(neighbor, node)

    for node in graph:
        if node not in visited:
            parent[node] = None
            dfs(node, None)

    # Return all edges that are part of cycles
    result = []
    for edge in edges:
        key = tuple(sorted((edge['spy1'], edge['spy2'])))
        if key in cycle_edges:
            result.append(edge)
    return result


@app.route('/investigate', methods=['POST'])
@app.route('/investigate', methods=['POST'])
def spy_evaluate():
    try:
        data = request.get_json()
        logger.info(f"Received POST data: {json.dumps(data)}")

        output = {"networks": []}

        # Support both {"networks": [...]} and top-level list
        networks = data.get("networks") if isinstance(data, dict) else data

        for network in networks:
            network_id = network.get("networkId")
            edges = network.get("network", [])
            extra_channels = find_cycles(edges)
            output["networks"].append({
                "networkId": network_id,
                "extraChannels": extra_channels
            })

        logger.info(f"Computed result: {json.dumps(output)}")
        return json.dumps(output)

    except Exception as e:
        logger.exception("Error in /investigate")
        return json.dumps({"error": str(e)}), 500