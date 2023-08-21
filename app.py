import dataclasses
from collections import defaultdict
from typing import Dict
from flask import Flask, render_template, abort
from tqdm import tqdm
from glob import glob

app = Flask(__name__)


@app.template_filter("format_size")
def format_size(size):
    if size < 1000:
        return f"{size} B"
    elif size < 1024**2:
        return f"{size/1024:,.0f} KiB"
    elif size < 1024**3:
        return f"{size/1024**2:,.0f} MiB"
    elif size < 1024**4:
        return f"{size/1024**3:,.0f} GiB"
    else:
        return f"{size/1024**4:,.1f} TiB"


@app.template_filter("sort_by_size")
def sort_by_size(children):
    return sorted(children, key=lambda n: n.size, reverse=True)


@dataclasses.dataclass
class Node:
    size: int = 0
    children: Dict[str, "Node"] = dataclasses.field(
        default_factory=lambda: defaultdict(Node)
    )
    name: str = None

    def add(self, size, path):
        self.size += size
        if "/" in path:
            name, rest = path.split("/", 1)
            self.children[name].add(size, rest)
            self.children[name].name = name
        else:
            self.children[path] = Node(size, name=path)

    def __getitem__(self, key):
        return self.children[key]


lines = []
for path in glob("data/*.txt"):
    with open(path, "r") as f:
        lines.extend(f.readlines())

root = Node(name="/")
for line in tqdm(lines):
    line = line.strip().split()
    size = int(line[0])
    path = line[1][len("gs://") :]
    root.add(size, path)

del lines


@app.route("/")
def index():
    return render_template("template.html", node=root, fullpath="/")


@app.route("/<path:dynamic_route>/")
def dynamic_path(dynamic_route):
    route_list = dynamic_route.split("/")
    node = root
    for name in route_list:
        if name not in node.children:
            abort(404)
        node = node.children[name]
    return render_template("template.html", node=node, fullpath=f"/{dynamic_route}/")


if __name__ == "__main__":
    app.run(debug=True)
