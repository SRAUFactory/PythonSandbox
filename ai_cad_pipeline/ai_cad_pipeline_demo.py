"""
AI CADコード自動生成（CADCoder連携）デモスクリプト

本スクリプトは、CADCoder等のVision AIが「画像から生成したベタ書きのCadQueryコード」を
人間（またはLLM）が読み解き、パラメータ化・公差（Clearance）・DfAM面取りを追加して
「3Dプリント可能な実用モデル」へと精緻化する2段階パイプラインを再現・体験するデモです。
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


def generate_raw_ai_model() -> cq.Workplane:
    """
    【Phase 1: 生のAI生成コードの再現 (Raw AI Output)】
    
    CADCoderなどのVision-LLMモデルが画像から推論・出力する典型的なスタイルのコード。
    - 直線補間 (moveTo / lineTo) と固定の浮動小数点数値によるべた書き。
    - 変数パラメータ化なし、公差設定なし、面取り/フィレットなし。
    """
    wp = cq.Workplane("XY")
    # 固定座標でL字型の輪郭を描画し、そのまま一定値で押し出し
    sketch_loop = (
        wp.moveTo(0.0, 0.0)
        .lineTo(50.0, 0.0)
        .lineTo(50.0, 15.0)
        .lineTo(15.0, 15.0)
        .lineTo(15.0, 50.0)
        .lineTo(0.0, 50.0)
        .close()
    )
    raw_solid = wp.add(sketch_loop).extrude(30.0)
    
    # 穴あけも固定の座標指定
    raw_model = (
        raw_solid.faces("<Y")
        .workplane()
        .pushPoints([(7.5, 15.0)])
        .hole(6.0)
    )
    return raw_model


def generate_refined_model(
    base_length: float = 60.0,
    base_height: float = 60.0,
    thickness: float = 15.0,
    width: float = 40.0,
    hole_diam: float = 6.0,
    clearance: float = 0.3,
    chamfer_size: float = 1.0,
) -> cq.Workplane:
    """
    【Phase 2: パラメータ・公差・DfAM補正後の精緻化コード (Refined Output)】
    
    AIが作ったプロトタイプコードを解析し、実用設計へと落とし込んだコード。
    - パラメータ設計: 寸法を変数管理（base_length, width 等）。
    - 公差考慮: 実機プリント時のプラスチック収縮に備え clearance 補正を加算。
    - DfAM面取り: オーバーハング崩れを防ぐための面取り (chamfer) と補強フィレット。
    """
    # 補正後のボルト穴径
    actual_hole_diam = hole_diam + clearance

    # パラメータ駆動によるL字スケッチの生成
    sketch = (
        cq.Sketch()
        .segment((0, 0), (base_length, 0))
        .segment((base_length, thickness))
        .segment((thickness, thickness))
        .segment((thickness, base_height))
        .segment((0, base_height))
        .close()
        .assemble()
    )

    # 押し出し
    base_solid = cq.Workplane("XY").placeSketch(sketch).extrude(width)

    # 拘束（中心基準のオフセット指定）を用いた座ぐりボルト穴の追加
    hole_offset_x = thickness / 2.0
    hole_offset_z = base_height / 2.0
    
    refined_holes = (
        base_solid.faces("<Y")
        .workplane()
        .pushPoints([(hole_offset_x, hole_offset_z)])
        .cboreHole(diameter=actual_hole_diam, cboreDiameter=actual_hole_diam * 1.6, cboreDepth=3.0)
    )

    # 3Dプリント向け面取り (Chamfer) と補強フィレット
    final_refined_model = (
        refined_holes.edges(">Z or <Z or >X or <X")
        .chamfer(chamfer_size)
    )
    return final_refined_model


def main():
    print("=" * 65)
    print("4. AI CADコード自動生成（CADCoder）と精緻化パイプラインの検証")
    print("=" * 65)

    base_dir = os.path.dirname(__file__)

    # --- Phase 1: 生のAI生成コードの実行と評価 ---
    print("\n--- Phase 1: 生のAI生成コード (Raw AI Output) の評価 ---")
    print("特徴: 固定座標のベタ書き。変数なし、公差なし、面取りなし。")
    raw_model = generate_raw_ai_model()
    print_brep_info("1. 生のAI生成モデル (Raw AI Model)", raw_model)

    raw_step_path = os.path.join(base_dir, "output_raw_ai.step")
    raw_stl_path = os.path.join(base_dir, "output_raw_ai.stl")
    cq.exporters.export(raw_model, raw_step_path)
    cq.exporters.export(raw_model, raw_stl_path)
    print(f"  └─ STEP: {raw_step_path}")
    print(f"  └─ STL : {raw_stl_path}")

    # --- Phase 2: パラメータ・公差補正コードの実行と評価 ---
    print("\n--- Phase 2: 精緻化コード (Refined Parametric Model) の評価 ---")
    print("特徴: パラメータ変数化、公差(clearance=0.3mm)、3Dプリント面取り(Chamfer)。")
    refined_model = generate_refined_model(
        base_length=60.0,
        base_height=60.0,
        thickness=15.0,
        width=40.0,
        hole_diam=6.0,
        clearance=0.3,
        chamfer_size=1.0,
    )
    print_brep_info("2. 精緻化モデル (Refined Parametric Model)", refined_model)

    refined_step_path = os.path.join(base_dir, "output_refined_ai.step")
    refined_stl_path = os.path.join(base_dir, "output_refined_ai.stl")
    cq.exporters.export(refined_model, refined_step_path)
    cq.exporters.export(refined_model, refined_stl_path)
    print(f"  └─ STEP: {refined_step_path}")
    print(f"  └─ STL : {refined_stl_path}")

    print("\n" + "=" * 65)
    print("✅ 2段階パイプラインの実行およびSTEP/STL出力が正常に完了しました！")
    print("=" * 65)


if __name__ == "__main__":
    main()
