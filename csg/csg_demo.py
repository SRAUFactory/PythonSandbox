"""
CSG (Constructive Solid Geometry) デモスクリプト

CADの3大概念の1つ「CSG」をCadQueryで体験・分析するスクリプトです。
基本立体（Box, Cylinder等）を用意し、ブーリアン演算（和・差・積）を組み合わせることで
複雑な機械パーツ（T字配管バルブボディ）を構築します。
"""

import os
import cadquery as cq


def print_brep_info(name: str, shape: cq.Workplane):
    """ソリッドのB-Rep構造（面・辺・頂点）の数をコンソールに出力する関数"""
    val = shape.val()
    faces = len(val.Faces())
    edges = len(val.Edges())
    vertices = len(val.Vertices())
    print(f"[{name}]")
    print(f"  - 面 (Faces)   : {faces} 個")
    print(f"  - 辺 (Edges)   : {edges} 個")
    print(f"  - 頂点(Vertices): {vertices} 個\n")


def main():
    print("=" * 60)
    print("1. CSG (Constructive Solid Geometry) の原理と実装")
    print("=" * 60)

    # 1-1. 基本立体の生成 (Primitives)
    print("\n--- Step 1: 基本立体の作成 (Primitives) ---")
    
    # 主本体: 直方体 (40mm x 40mm x 40mm)
    main_block = cq.Workplane("XY").box(40, 40, 40)
    print_brep_info("1. 主本体 (Box 40x40x40)", main_block)

    # 左右配管部: 直径30mm, 長さ70mmの円柱
    pipe_cylinder = cq.Workplane("YZ").cylinder(height=70, radius=15)
    print_brep_info("2. 左右配管部 (Cylinder R15, H70)", pipe_cylinder)

    # 上部ポート: 直径24mm, 長さ30mmの円柱
    top_port = cq.Workplane("XY").workplane(offset=20).cylinder(height=30, radius=12)
    print_brep_info("3. 上部ポート (Cylinder R12, H30)", top_port)

    # 1-2. ブーリアン和 (Union / Add)
    print("--- Step 2: ブーリアン和 (Union) ---")
    print("主本体、左右配管部、上部ポートを結合して1つの統合ソリッドを生成します。")
    combined_body = main_block.union(pipe_cylinder).union(top_port)
    print_brep_info("4. 結合後のソリッド (Union Result)", combined_body)

    # 1-3. ブーリアン差 (Cut / Difference)
    print("--- Step 3: ブーリアン差 (Cut) ---")
    print("内部を通る流路穴（貫通シリンダー）を生成し、結合ソリッドから削り取ります。")
    
    # 水平流路（直径20mm）
    h_bore = cq.Workplane("YZ").cylinder(height=80, radius=10)
    # 垂直流路（直径16mm）
    v_bore = cq.Workplane("XY").cylinder(height=60, radius=8)
    
    bores = h_bore.union(v_bore)
    valve_body = combined_body.cut(bores)
    print_brep_info("5. 流路穴あけ後 (Cut Result)", valve_body)

    # 1-4. ブーリアン積 (Intersection)
    print("--- Step 4: ブーリアン積 (Intersection) の応用 ---")
    print("ソリッドと球の交差領域（積）を取得して、交差点の補強エリアを確認します。")
    center_sphere = cq.Workplane("XY").sphere(radius=22)
    reinforced_core = valve_body.intersect(center_sphere)
    print_brep_info("6. 中心球との交差領域 (Intersection Result)", reinforced_core)

    # 1-5. 仕上げフィレット加工とSTEPファイル出力
    print("--- Step 5: 仕上げとSTEPファイル出力 ---")
    # CSGで出来上がった最終ソリッドの外周に補強フィレットを追加
    final_model = valve_body.edges("(>Z or <Z or >X or <X)").fillet(1.5)
    print_brep_info("7. 最終モデル (Filleted Model)", final_model)

    output_path = os.path.join(os.path.dirname(__file__), "output_csg.step")
    cq.exporters.export(final_model, output_path)
    print(f"✅ STEPファイルを正常に出力しました: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
