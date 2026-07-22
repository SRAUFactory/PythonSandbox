import cadquery as cq

# 1. 10x10x10の立方体を作る
box = cq.Workplane("XY").box(10, 10, 10)

# 「Z軸のプラス方向にある面」を選択し、その周囲の「辺」に半径1mmの丸みをつける
box = box.faces(">Z").edges().fillet(1)

# 2. B-Rep要素へのアクセス
faces = box.faces().vals()  # 面（Face）のリスト
edges = box.edges().vals()  # 辺（Edge）のリスト
vertices = box.vertices().vals()  # 頂点（Vertex）のリスト

print(f"面は {len(faces)} つあります。")
print(f"辺は {len(edges)} つあります。")
print(f"頂点は {len(vertices)} つあります。")
