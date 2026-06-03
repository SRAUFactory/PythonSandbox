import cadquery as cq

# 1. 10x10x10の立方体を作る
box = cq.Workplane("XY").box(10, 10, 10)

# 2. B-Rep要素へのアクセス
faces = box.faces().vals()  # 面（Face）のリスト
edges = box.edges().vals()  # 辺（Edge）のリスト
vertices = box.vertices().vals()  # 頂点（Vertex）のリスト

print(f"面は {len(faces)} つあります。")
print(f"辺は {len(edges)} つあります。")
