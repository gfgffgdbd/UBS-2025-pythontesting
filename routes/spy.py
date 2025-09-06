import json
import logging
from flask import request
from routes import app

logger = logging.getLogger(__name__)

class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        px = self.find(x)
        py = self.find(y)
        if px == py: # if already part of same set, forms cycle, remove edge 
            return False
        self.parent[py] = px
        return True
    
def find_channels(edges):
    uf = UnionFind()
    final_edges = []
    for edge in edges:
        if uf.union(edge['spy1'], edge['spy2']):
            final_edges.append(edge)  
    return final_edges


@app.route('/investigate', methods=['POST'])
def spy_evaluate():
    data = request.get_json()
    logger.info(f"Data sent for evaluation: {data}")

    output = {"networks": []}

    for network in data.get("networks", []):
        network_id = network.get("networkId")
        edges = network.get("network", [])
        channels = find_channels(edges)
        output["networks"].append({
            "networkId": network_id,
            "extraChannels": channels
        })

    logger.info(f"Result: {output}")
    return json.dumps(output)