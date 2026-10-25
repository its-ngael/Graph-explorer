import math
import heapq
from flask import Flask, jsonify, request, render_template

class Vertex:
    def __init__(self, value, x, y):
        self.value = value   
        self.x = x           
        self.y = y           


class Graph:
    def __init__(self, size):
        self.size = size
        self.vertices = []
        self.adj_matrix = [[0] * size for _ in range(size)]

    def add_vertex(self, vertex):
        self.vertices.append(vertex)

    def add_edge(self, name1, name2):
        i = self.index_of(name1)
        j = self.index_of(name2)
        self.adj_matrix[i][j] = 1
        self.adj_matrix[j][i] = 1

    def index_of(self, name):
        for i in range(len(self.vertices)):
            if self.vertices[i].value == name:
                return i
        return -1

    def distance(self, i, j):
        a = self.vertices[i]
        b = self.vertices[j]
        return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

    def neighbors(self, i):
        result = []
        for j in range(self.size):
            if self.adj_matrix[i][j] == 1:
                result.append(j)
        return result

vertex_data = [
    ("V1", 499, 969), ("V2", 428, 970), ("V3", 423, 812), ("V4", 494, 813),
    ("V5", 329, 741), ("V6", 489, 653), ("V7", 417, 667), ("V8", 331, 674),
    ("V9", 258, 674), ("V10", 225, 741), ("V11", 217, 553), ("V12", 7, 549),
    ("V13", 451, 525), ("V14", 517, 591), ("V15", 549, 1024),
    ("V17", 121, 468), ("V18", 479, 456), ("V19", 115, 305), ("V20", 177, 301),
    ("V21", 160, 93), ("V22", 326, 86), ("V23", 270, 146), ("V24", 164, 154),
    ("V25", 332, 172), ("V26", 414, 174), ("V27", 329, 48), ("V28", 477, 42),
    ("V29", 406, 46), ("V30", 409, 95), ("V31", 485, 92), ("V32", 515, 458),
    ("V34", 242, 463), ("V35", 240, 413), ("V36", 431, 404), ("V37", 435, 455),
    ("V38", 480, 346), ("V39", 432, 346), ("V40", 420, 312), ("V41", 420, 285),
    ("V42", 493, 284), ("V43", 417, 238), ("V44", 493, 235), ("V46", 466, 547),
    ("V47", 120, 548), ("V48", 121, 531),
]

edge_data = [
    ("V1", "V2"), ("V1", "V4"), ("V1", "V15"),
    ("V2", "V3"), ("V3", "V4"), ("V3", "V7"),
    ("V4", "V6"), ("V6", "V7"), ("V6", "V14"),
    ("V7", "V8"), ("V8", "V9"), ("V8", "V5"),
    ("V5", "V10"), ("V10", "V11"),
    ("V11", "V47"), ("V11", "V46"), ("V47", "V12"),
    ("V12", "V48"), ("V48", "V13"), ("V13", "V46"),
    ("V46", "V14"), ("V13", "V32"), ("V18", "V32"),
    ("V48", "V17"), ("V47", "V48"),
    ("V17", "V19"), ("V17", "V34"),
    ("V34", "V35"), ("V34", "V37"), ("V35", "V36"),
    ("V37", "V36"), ("V37", "V18"), ("V18", "V38"),
    ("V36", "V39"), ("V39", "V40"), ("V40", "V41"),
    ("V41", "V42"), ("V41", "V43"), ("V43", "V44"), ("V43", "V26"),
    ("V26", "V30"), ("V26", "V25"), ("V30", "V31"), ("V30", "V29"),
    ("V29", "V27"), ("V29", "V28"), ("V27", "V22"),
    ("V22", "V21"), ("V22", "V25"), ("V21", "V24"),
    ("V24", "V23"), ("V24", "V20"), ("V20", "V19"),
]

graph = Graph(len(vertex_data))
for name, x, y in vertex_data:
    graph.add_vertex(Vertex(name, x, y))
for name1, name2 in edge_data:
    graph.add_edge(name1, name2)

def find_route(start_name, goal_name, algorithm):
    start = graph.index_of(start_name)
    goal = graph.index_of(goal_name)

    queue = [(0, start)]           
    came_from = {start: None}       
    cost_so_far = {start: 0}        
    visited = []                    
    steps = []                      

    while len(queue) > 0:
        priority, current = heapq.heappop(queue)

        if current in visited:
            continue
        visited.append(current)

        parent = came_from[current]
        parent_name = None
        if parent is not None:
            parent_name = graph.vertices[parent].value
        steps.append({"vertex": graph.vertices[current].value, "from": parent_name})

        if current == goal:
            break

        for n in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.distance(current, n)
            left = graph.distance(n, goal)   

            if algorithm == "greedy":
                if n not in came_from:
                    came_from[n] = current
                    cost_so_far[n] = new_cost
                    heapq.heappush(queue, (left, n))
            else:
                if n not in cost_so_far or new_cost < cost_so_far[n]:
                    cost_so_far[n] = new_cost
                    came_from[n] = current
                    if algorithm == "astar":
                        heapq.heappush(queue, (new_cost + left, n))
                    else:  # uniform cost
                        heapq.heappush(queue, (new_cost, n))

    if goal not in came_from:
        return {"found": False, "steps": steps, "visited": [graph.vertices[i].value for i in visited]}

    path = []
    step = goal
    while step is not None:
        path.append(step)
        step = came_from[step]
    path.reverse()

    total = 0
    for k in range(len(path) - 1):
        total += graph.distance(path[k], path[k + 1])

    return {
        "found": True,
        "path": [graph.vertices[i].value for i in path],
        "steps": steps,
        "visited": [graph.vertices[i].value for i in visited],
        "distance": round(total),
    }


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/graph")
def api_graph():
    vertices = [{"name": v.value, "x": v.x, "y": v.y} for v in graph.vertices]
    return jsonify({"vertices": vertices, "edges": edge_data})


@app.route("/api/route")
def api_route():
    start = request.args.get("start")
    goal = request.args.get("goal")
    algorithm = request.args.get("algorithm")
    return jsonify(find_route(start, goal, algorithm))


if __name__ == "__main__":
    app.run(debug=True, port=5000)