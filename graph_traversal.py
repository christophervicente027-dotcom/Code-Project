import tkinter as tk
from collections import deque

# ======================
# DEFAULT GRAPH
# ======================
default_graph_text = """A:B,C
B:A,D,E
C:A,F
D:B
E:B,F
F:C,E"""

positions = {
    'A': (200, 60),
    'B': (100, 150),
    'C': (300, 150),
    'D': (60, 260),
    'E': (160, 260),
    'F': (300, 260)
}

# ======================
# WINDOW
# ======================
root = tk.Tk()
root.title("Graph Traversal Demo (BFS / DFS / Shortest Path)")
root.geometry("600x720")
root.configure(bg="#1e1b3a")

canvas = tk.Canvas(root, width=420, height=340, bg="#f4f6ff", highlightthickness=0)
canvas.pack(pady=8)

nodes = {}
labels = {}
step = 0

# ======================
# GRAPH PARSER
# ======================
def parse_graph():
    graph = {}
    lines = graph_input.get("1.0", tk.END).strip().splitlines()
    for line in lines:
        if ":" in line:
            node, nbrs = line.split(":")
            graph[node.strip()] = [n.strip() for n in nbrs.split(",") if n.strip()]
    return graph

# ======================
# DRAW GRAPH
# ======================
def draw_graph():
    global step
    step = 0
    step_label.config(text="Step: 0")
    status_label.config(text="Status: Ready")

    canvas.delete("all")
    nodes.clear()
    labels.clear()

    graph = parse_graph()

    for n, nbrs in graph.items():
        if n not in positions:
            continue
        x1, y1 = positions[n]
        for nb in nbrs:
            if nb in positions:
                x2, y2 = positions[nb]
                canvas.create_line(x1, y1, x2, y2, width=2)

    for n, (x, y) in positions.items():
        circle = canvas.create_oval(x-20, y-20, x+20, y+20,
                                    fill="#d1d5db", outline="#4338ca", width=2)
        text = canvas.create_text(x, y, text=n, font=("Arial", 12, "bold"))
        lbl = canvas.create_text(x, y+30, text="", font=("Arial", 8))
        nodes[n] = circle
        labels[n] = lbl

# ======================
# VISIT STEP
# ======================
def visit(node, color, text):
    global step
    step += 1
    step_label.config(text=f"Step: {step}")
    canvas.itemconfig(nodes[node], fill=color)
    canvas.itemconfig(labels[node], text=text)
    root.update()
    root.after(700)

# ======================
# BUTTON CONTROL
# ======================
def disable_buttons(state):
    for b in btns.winfo_children():
        b.config(state=state)

# ======================
# BFS
# ======================
def bfs():
    disable_buttons("disabled")
    draw_graph()
    graph = parse_graph()

    start = start_var.get()
    visited = {start}
    q = deque([start])

    status_label.config(text="Status: BFS Traversal")

    while q:
        node = q.popleft()
        visit(node, "#fde047", "Current")
        visit(node, "#4ade80", "Visited")

        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                q.append(nb)

    disable_buttons("normal")

# ======================
# DFS
# ======================
def dfs():
    disable_buttons("disabled")
    draw_graph()
    graph = parse_graph()
    visited = set()

    status_label.config(text="Status: DFS Traversal")

    def dfs_go(node):
        visited.add(node)
        visit(node, "#fde047", "Current")
        visit(node, "#4ade80", "Visited")
        for nb in graph.get(node, []):
            if nb not in visited:
                dfs_go(nb)

    dfs_go(start_var.get())
    disable_buttons("normal")

# ======================
# SHORTEST PATH
# ======================
def shortest():
    disable_buttons("disabled")
    draw_graph()
    graph = parse_graph()

    start = start_var.get()
    goal = goal_var.get()

    status_label.config(text=f"Finding shortest path from {start} to {goal}")

    q = deque([[start]])
    visited = {start}

    while q:
        path = q.popleft()
        node = path[-1]

        if node == goal:
            status_label.config(text="Status: Shortest Path Found")
            for n in path:
                visit(n, "#f87171", "Path")
            disable_buttons("normal")
            return

        for nb in graph.get(node, []):
            if nb not in visited:
                visited.add(nb)
                q.append(path + [nb])

    status_label.config(text="Status: No Path Found")
    disable_buttons("normal")

# ======================
# GRAPH INPUT
# ======================
tk.Label(root, text="Graph Input (Adjacency List)", fg="white", bg="#1e1b3a").pack()
graph_input = tk.Text(root, height=6, width=40)
graph_input.pack()
graph_input.insert(tk.END, default_graph_text)

# ======================
# CONTROLS
# ======================
control = tk.Frame(root, bg="#1e1b3a")
control.pack(pady=5)

start_var = tk.StringVar(value="A")
goal_var = tk.StringVar(value="F")

tk.Label(control, text="Start:", fg="white", bg="#1e1b3a").grid(row=0, column=0)
tk.OptionMenu(control, start_var, "A","B","C","D","E","F").grid(row=0, column=1)

tk.Label(control, text="Goal:", fg="white", bg="#1e1b3a").grid(row=0, column=2)
tk.OptionMenu(control, goal_var, "A","B","C","D","E","F").grid(row=0, column=3)

btns = tk.Frame(root, bg="#1e1b3a")
btns.pack(pady=8)

tk.Button(btns, text="▶ BFS", width=12, bg="#6366f1", fg="white", command=bfs).grid(row=0, column=0, padx=5)
tk.Button(btns, text="▶ DFS", width=12, bg="#8b5cf6", fg="white", command=dfs).grid(row=0, column=1, padx=5)
tk.Button(btns, text="▶ Shortest Path", width=28, bg="#ec4899", fg="white", command=shortest).grid(row=1, column=0, columnspan=2, pady=6)

# ======================
# LEGEND
# ======================
legend = tk.Frame(root, bg="#1e1b3a")
legend.pack()

tk.Label(legend, text="Legend:", fg="white", bg="#1e1b3a").grid(row=0, column=0)
tk.Label(legend, text="  ", bg="#fde047", width=2).grid(row=0, column=1)
tk.Label(legend, text="Current", fg="white", bg="#1e1b3a").grid(row=0, column=2)
tk.Label(legend, text="  ", bg="#4ade80", width=2).grid(row=0, column=3)
tk.Label(legend, text="Visited", fg="white", bg="#1e1b3a").grid(row=0, column=4)
tk.Label(legend, text="  ", bg="#f87171", width=2).grid(row=0, column=5)
tk.Label(legend, text="Path", fg="white", bg="#1e1b3a").grid(row=0, column=6)

step_label = tk.Label(root, text="Step: 0", fg="white", bg="#1e1b3a")
step_label.pack()

status_label = tk.Label(root, text="Status: Ready", fg="#c7d2fe", bg="#1e1b3a")
status_label.pack(pady=4)

draw_graph()
root.mainloop()

