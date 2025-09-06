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

def find_extra_channels(edges):
    """
    Returns edges that form cycles (i.e., redundant connections).
    Uses Union-Find (Disjoint Set Union).
    """
    parent = {}

    def find(x):
        if x not in parent:
            parent[x] = x
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False  # already connected -> edge is extra
        parent[py] = px
        return True

    extra_edges = []
    for edge in edges:
        if not union(edge['spy1'], edge['spy2']):
            extra_edges.append(edge)

    return extra_edges

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
            extra_channels = find_extra_channels(edges)
            output["networks"].append({
                "networkId": network_id,
                "extraChannels": extra_channels
            })

        logger.info(f"Computed result: {json.dumps(output)}")
        return json.dumps(output)

    except Exception as e:
        logger.exception("Error in /investigate")
        return json.dumps({"error": str(e)}), 500