# import json
# import logging
# from flask import request
# from routes import app

# # Configure logging to print to console
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s"
# )
# logger = logging.getLogger(__name__)

# class UnionFind:
#     def __init__(self):
#         self.parent = {}

#     def find(self, x):
#         if x not in self.parent:
#             self.parent[x] = x
#         if self.parent[x] != x:
#             self.parent[x] = self.find(self.parent[x])
#         return self.parent[x]

#     def union(self, x, y):
#         px = self.find(x)
#         py = self.find(y)
#         if px == py: # if already part of same set, forms cycle, remove edge 
#             return False
#         self.parent[py] = px
#         return True
    
# def find_extra_channels(edges):
#     """
#     Returns the edges that create cycles (extra channels)
#     """
#     sorted_edges = sorted(edges, key=lambda e: (min(e['spy1'], e['spy2']), max(e['spy1'], e['spy2'])))

#     uf = UnionFind()
#     extra_edges = []
#     for edge in sorted_edges:
#         if not uf.union(edge['spy1'], edge['spy2']):
#             extra_edges.append(edge)
#     return extra_edges


# @app.route('/investigate', methods=['POST'])
# @app.route('/investigate', methods=['POST'])
# def spy_evaluate():
#     try:
#         data = request.get_json()
#         logger.info(f"Received POST data: {json.dumps(data)}")

#         output = {"networks": []}

#         # Support both {"networks": [...]} and top-level list
#         networks = data.get("networks") if isinstance(data, dict) else data

#         for network in networks:
#             network_id = network.get("networkId")
#             edges = network.get("network", [])
#             extra_channels = find_extra_channels(edges)
#             output["networks"].append({
#                 "networkId": network_id,
#                 "extraChannels": extra_channels
#             })

#         logger.info(f"Computed result: {json.dumps(output)}")
#         return json.dumps(output)

#     except Exception as e:
#         logger.exception("Error in /investigate")
#         return json.dumps({"error": str(e)}), 500