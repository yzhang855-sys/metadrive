import ast
import os
import graphviz

envs_dir = "/Users/pangjugua/metadrive/metadrive/envs"
classes = {}

for filename in os.listdir(envs_dir):
    if not filename.endswith(".py"):
        continue
    filepath = os.path.join(envs_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read())
        except SyntaxError:
            print(f"Skipping {filename}")
            continue
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            bases = []
            for base in node.bases:
                if isinstance(base, ast.Name):
                    bases.append(base.id)
                elif isinstance(base, ast.Attribute):
                    bases.append(base.attr)
            classes[node.name] = bases
            print(f"Found: {node.name} -> {bases}")

print(f"\nTotal classes: {len(classes)}")

dot = graphviz.Digraph(name="MetaDrive_Envs_Class_Hierarchy")
dot.attr(rankdir="BT", splines="ortho", fontname="Helvetica")
dot.attr("node", shape="box", style="filled", fillcolor="lightblue", fontname="Helvetica")

all_names = set(classes.keys())
for classname, bases in classes.items():
    dot.node(classname)
    for base in bases:
        if base in all_names:
            dot.edge(classname, base)

output_path = "/Users/pangjugua/metadrive/envs_class_hierarchy"
dot.render(output_path, format="png", cleanup=True)
print(f"Saved: {output_path}.png")