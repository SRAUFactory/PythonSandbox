"""
Constraint (拘束・パラメータ制約) デモスクリプト

CADの3大概念の1つ「Constraint（拘束）」をCadQueryで体験・分析するスクリプトです。
「ボルト穴は常にPCD上に均等配置する」「内径は外径より必ず小さく同心円とする」といった
幾何学的・寸法的な拘束（制約関係）をコードで構築し、パラメータ変更時にも
設計意図（Design Intent）が崩れない配管フランジを生成します。
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


def create_parametric_flange(
    outer_diam: float = 120.0,
    inner_diam: float = 50.0,
    thickness: float = 15.0,
    pcd: float = 90.0,
    bolt_count: int = 6,
    bolt_diam: float = 10.0,
) -> cq.Workplane:
    """
    パラメータ拘束に基づきフランジ配管パーツを構築する関数

    【設計拘束 (Design Constraints)】
    1. 同心円拘束: 内径 hole と外径 flange は共通の中心軸（原点）を持つ。
    2. PCD位置拘束: すべてのボルト穴は中心から半径 (pcd / 2) のピッチ円上に配置。
    3. 円周等配拘束: bolt_count の個数に応じて 360° / bolt_count の角度毎に穴を生成。
    """
    # 1. 2Dスケッチによる輪郭と拘束の定義
    # 外径と内径穴の同心円拘束（mode="s" は減算模式）
    sketch = (
        cq.Sketch()
        .circle(outer_diam / 2.0)  # 外径
        .circle(inner_diam / 2.0, mode="s")  # 内径穴（同心減算）
    )

    # 2. 3Dソリッドの押し出し (Extrude)
    base_flange = cq.Workplane("XY").placeSketch(sketch).extrude(thickness)

    # 3. PCD上のボルト穴配置（幾何的等配拘束）
    # polarArray を用いて中心軸周りに角度等角ピッチでボルト穴を自動計算配置
    flange_with_holes = (
        base_flange.faces(">Z")
        .workplane()
        .polarArray(radius=pcd / 2.0, startAngle=0, angle=360, count=bolt_count)
        .hole(bolt_diam)
    )

    # 4. 外周エッジの chamfer (面取り) 追加
    final_flange = flange_with_holes.edges(">Z").chamfer(1.0)
    return final_flange


def main():
    print("=" * 60)
    print("2. Constraint (拘束・パラメータ制約) の原理と実装")
    print("=" * 60)

    # 2-1. 標準パラメータでのモデル構築
    print("\n--- Step 1: 標準拘束パラメータでのフランジ作成 ---")
    print("パラメータ: 外径=120mm, 内径=50mm, PCD=90mm, ボルト穴=6個(径10mm)")
    
    flange_std = create_parametric_flange(
        outer_diam=120.0,
        inner_diam=50.0,
        thickness=15.0,
        pcd=90.0,
        bolt_count=6,
        bolt_diam=10.0,
    )
    print_brep_info("標準フランジ (Standard Flange)", flange_std)

    # 2-2. パラメータ変更実験（拘束関係の自動維持検証）
    print("--- Step 2: パラメータ変更による幾何的拘束の検証 ---")
    print("パラメータ変更: ボルト穴数を 6個 -> 8個、外径を 120mm -> 150mm、PCDを 90mm -> 120mm に変更")
    print("-> コードで定義された「等配拘束」と「同心拘束」によって、自動的に正しいレイアウトが生成されます。")

    flange_large = create_parametric_flange(
        outer_diam=150.0,
        inner_diam=60.0,
        thickness=20.0,
        pcd=120.0,
        bolt_count=8,
        bolt_diam=12.0,
    )
    print_brep_info("大型8穴フランジ (Large 8-Bolt Flange)", flange_large)

    # 2-3. STEPファイルの出力
    output_path = os.path.join(os.path.dirname(__file__), "output_constraint.step")
    cq.exporters.export(flange_large, output_path)
    print(f"✅ STEPファイルを正常に出力しました: {output_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
