"""
Feature Hierarchy (フィーチャー履歴・順序依存性) デモスクリプト

CADの3大概念の1つ「Feature Hierarchy（フィーチャー履歴）」をCadQueryで体験・分析するスクリプトです。
3D CADは「スケッチを描く」→「押し出す」→「穴を開ける」→「角を丸める」という
【操作履歴の積み重ね（フィーチャーのツリー構造）】で形状を管理します。

本スクリプトでは、L字マウントブラケットを題材に、操作手順の違い（フィーチャーの実行順序）が
最終的なB-Repトポロジーや形状にどのような影響を与えるかを比較検証します。
"""

import os
import cadquery as cq


def print_brep_info(name: str, shape: cq.Workplane):
    """ソリッドのB-Rep構造の数をコンソールに出力する関数"""
    val = shape.val()
    faces = len(val.Faces())
    edges = len(val.Edges())
    vertices = len(val.Vertices())
    print(f"[{name}]")
    print(f"  - 面 (Faces)   : {faces} 個")
    print(f"  - 辺 (Edges)   : {edges} 個")
    print(f"  - 頂点(Vertices): {vertices} 個\n")


def build_l_bracket_base() -> cq.Workplane:
    """ベースとなるL字ブラケットの素形材を押し出し形成するフィーチャー"""
    # L字型のスケッチ作成
    sketch = (
        cq.Sketch()
        .segment((0, 0), (60, 0))
        .segment((60, 15))
        .segment((15, 15))
        .segment((15, 60))
        .segment((0, 60))
        .close()
        .assemble()
    )
    # 幅 40mm で3D押し出し (Base Extrude Feature)
    return cq.Workplane("XY").placeSketch(sketch).extrude(40.0)


def main():
    print("=" * 60)
    print("3. Feature Hierarchy (フィーチャー履歴・順序依存性) の原理と実装")
    print("=" * 60)

    # 3-1. フィーチャー履歴のステップバイステップ構築
    print("\n--- Step 1: フィーチャーの積み重ね（L字ブラケット） ---")
    
    # Feature 1: ベース押し出し (Base Extrude)
    feat1_base = build_l_bracket_base()
    print_brep_info("Feature 1: ベースL字ソリッド (Base Extrude)", feat1_base)

    # Feature 2: Workplane参照選択 ＋ 座ぐり穴加工 (Counterbore Hole Feature)
    # 底面側(Y=0)の面にWorkplaneをセットし、取り付け座ぐり穴を開ける
    feat2_holes = (
        feat1_base.faces("<Y")
        .workplane()
        .pushPoints([(15, 20), (45, 20)])
        .cboreHole(diameter=8.0, cboreDiameter=14.0, cboreDepth=4.0)
    )
    print_brep_info("Feature 2: 座ぐり穴追加後 (Add Counterbore Holes)", feat2_holes)

    # Feature 3: 内角リブの角丸め (Fillet Feature)
    feat3_filleted = feat2_holes.edges("|Z").fillet(3.0)
    print_brep_info("Feature 3: 全エッジフィレット追加後 (Fillet Feature)", feat3_filleted)

    # 3-2. フィーチャー順序の入れ替え実験（順序依存性の検証）
    print("--- Step 2: フィーチャー実行順序の比較実験 ---")
    print("【パターン A】: 『穴あけ (Hole)』 -> 『全縦エッジのフィレット (Fillet)』")
    print("【パターン B】: 『全縦エッジのフィレット (Fillet)』 -> 『穴あけ (Hole)』")
    print("-> 順番を入れ替えることで、穴のエッジに対するフィレット計算の有無や、トポロジー構造に変化が発生します。")

    # パターン A: 穴あけ -> 全縦エッジフィレット
    pattern_a = (
        feat1_base.faces("<Y")
        .workplane()
        .pushPoints([(15, 20), (45, 20)])
        .cboreHole(diameter=8.0, cboreDiameter=14.0, cboreDepth=4.0)
        .edges()
        .fillet(1.0)
    )
    print_brep_info("パターン A (Hole -> FilletAll)", pattern_a)

    # パターン B: 先にベース外周フィレット -> 穴あけ
    pattern_b = (
        feat1_base.edges()
        .fillet(1.0)
        .faces("<Y")
        .workplane()
        .pushPoints([(15, 20), (45, 20)])
        .cboreHole(diameter=8.0, cboreDiameter=14.0, cboreDepth=4.0)
    )
    print_brep_info("パターン B (FilletAll -> Hole)", pattern_b)

    # 3-3. 最終モデルのSTEPファイル出力
    output_path = os.path.join(os.path.dirname(__file__), "output_feature_hierarchy.step")
    cq.exporters.export(feat3_filleted, output_path)
    print(f"✅ STEPファイルを正常に出力しました: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
