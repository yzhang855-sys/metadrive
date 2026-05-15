import os
import ast

METADRIVE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadrive')
ENTRY_POINTS = [
    'metadrive/envs/base_env.py',
    'metadrive/envs/metadrive_env.py',
    'metadrive/envs/safe_metadrive_env.py',
]

def module_to_path(module_name):
    parts = module_name.split('.')
    if parts[0] != 'metadrive':
        return None
    rel = os.path.join(*parts) + '.py'
    full = os.path.join(os.path.dirname(METADRIVE_ROOT), rel)
    if os.path.exists(full):
        return full
    init = os.path.join(os.path.dirname(METADRIVE_ROOT), os.path.join(*parts), '__init__.py')
    if os.path.exists(init):
        return init
    return None

def get_imports(filepath):
    imports = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            tree = ast.parse(f.read(), filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith('metadrive'):
                        imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.startswith('metadrive'):
                    imports.append(node.module)
    except Exception:
        pass
    return imports

def dfs(entry_files):
    visited = set()
    stack = list(entry_files)
    while stack:
        path = stack.pop()
        if path in visited:
            continue
        if not os.path.exists(path):
            continue
        visited.add(path)
        for module in get_imports(path):
            resolved = module_to_path(module)
            if resolved and resolved not in visited:
                stack.append(resolved)
    return visited

def get_all_py_files():
    all_files = set()
    for root, dirs, files in os.walk(METADRIVE_ROOT):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for f in files:
            if f.endswith('.py'):
                all_files.add(os.path.join(root, f))
    return all_files

if __name__ == '__main__':
    print("=== R1 Dependency Analysis ===\n")
    base = os.path.dirname(os.path.abspath(__file__))
    entries = [os.path.join(base, ep) for ep in ENTRY_POINTS
               if os.path.exists(os.path.join(base, ep))]
    print("Entry points: {}".format(len(entries)))
    for e in entries:
        print("  {}".format(os.path.relpath(e)))
    print("\nRunning DFS traversal...")
    reachable = dfs(entries)
    all_files = get_all_py_files()
    unreachable = all_files - reachable
    reachable_in_pkg = reachable & all_files
    print("\nTotal Python files in package : {}".format(len(all_files)))
    print("Reachable from entry points   : {}".format(len(reachable_in_pkg)))
    print("Unreachable (candidates)      : {}".format(len(unreachable)))
    pct = len(unreachable) / len(all_files) * 100
    print("Unreachable percentage        : {:.1f}%".format(pct))
    print("\nSample unreachable files (first 20):")
    for f in sorted(unreachable)[:20]:
        print("  {}".format(os.path.relpath(f)))
    out = os.path.join(base, 'unreachable_files.txt')
    with open(out, 'w') as f:
        for path in sorted(unreachable):
            f.write(os.path.relpath(path) + '\n')
    print("\nFull list saved to: unreachable_files.txt")