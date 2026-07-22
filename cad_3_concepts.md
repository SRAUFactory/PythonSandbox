# CADの3大概念 (CSG, Constraint, Feature Hierarchy) とAI生成パイプラインのPython/CadQuery実装と解説

本ドキュメントは、CadQueryとPythonを用いて3D CADの基礎となる「CADの3大概念」および最新の「AIによるCADコード自動生成パイプライン」を体得・解説するための実践ガイドです。

---

## 目次
1. [概要と概念マッピング](#概要と概念マッピング)
2. [概念 1: CSG (Constructive Solid Geometry)](#概念-1-csg-constructive-solid-geometry)
3. [概念 2: Constraint (拘束・パラメータ制約)](#概念-2-constraint-拘束パラメータ制約)
4. [概念 3: Feature Hierarchy (フィーチャー履歴・順序依存性)](#概念-3-feature-hierarchy-フィーチャー履歴順序依存性)
5. [概念 4: AI CADコード自動生成とパイプライン精緻化 (CADCoder)](#概念-4-ai-cadコード自動生成とパイプライン精緻化-cadcoder)
6. [環境構築とスクリプト実行方法](#環境構築とスクリプト実行方法)

---

## 概要と概念マッピング

| 概念 | 実装スクリプト | 生成STEP/STLファイル | 主な学習・検証テーマ |
| :--- | :--- | :--- | :--- |
| **CSG** | [`csg_demo.py`](./csg_demo.py) | `output_csg.step` | 基本立体（Box, Cylinder, Sphere）の集合演算（Union, Cut, Intersection）によるバルブボディ生成とB-Repトポロジー変化 |
| **Constraint** | [`constraint_demo.py`](./constraint_demo.py) | `output_constraint.step` | 2Dスケッチ同心拘束とPCD円周等配拘束（`cq.Sketch` & `polarArray`）を用いたパラメータ可変フランジの設計 |
| **Feature Hierarchy** | [`feature_hierarchy_demo.py`](./feature_hierarchy_demo.py) | `output_feature_hierarchy.step` | L字ブラケットの加工履歴チェーン構築、および「穴あけ→フィレット」と「フィレット→穴あけ」の順序依存性比較 |
| **AI CAD Generation** | [`ai_cad_pipeline_demo.py`](./ai_cad_pipeline_demo.py) | `output_raw_ai.step`<br>`output_refined_ai.step`<br>`output_refined_ai.stl` | CADCoder等のVision-AIが生成した固定値コードを分析し、パラメータ化・公差 (Clearance)・DfAM面取りを追加する精緻化パイプライン |

---

## 概念 1: CSG (Constructive Solid Geometry)

### 概要
CSGは、球・円柱・直方体などの「プリミティブ（基本立体）」を用意し、以下の3つのブーリアン演算（集合演算）を重ね合わせることで複雑な3D形状を定義するアプローチです。
- **和 (Union / Add)**: 立体同士を統合する。
- **差 (Cut / Difference)**: 1つの立体から別の立体を削り取る（穴あけ・切削）。
- **積 (Intersection)**: 重なる領域のみを抽出する。

### コード解説 ([`csg_demo.py`](./csg_demo.py))
```python
# 1. プリミティブ生成
main_block = cq.Workplane("XY").box(40, 40, 40)
pipe_cylinder = cq.Workplane("YZ").cylinder(height=70, radius=15)

# 2. ブーリアン和
combined = main_block.union(pipe_cylinder)

# 3. ブーリアン差（内部流路の削り出し）
h_bore = cq.Workplane("YZ").cylinder(height=80, radius=10)
valve_body = combined.cut(h_bore)
```

### 検証結果（B-Rep構造の変化）
- **基本直方体**: 面 6 個 / 辺 12 個 / 頂点 8 個
- **パイプ結合後 (Union)**: 面 12 個 / 辺 21 個 / 頂点 14 個
- **貫通穴あけ後 (Cut)**: 面 16 個 / 辺 30 個 / 頂点 20 個
- **フィレット仕上げ後**: 面 26 個 / 辺 50 個 / 頂点 30 個 → STEPファイル: [`output_csg.step`](./output_csg.step)

---

## 概念 2: Constraint (拘束・パラメータ制約)

### 概要
Constraint（拘束）は、「同心円状に配置する」「PCD（ピッチ円）上に角度等分配置する」といった幾何学的・寸法的なルールを数値や関係式として定義する考え方です。これにより、外径やボルト穴数を変更しても、設計意図（Design Intent）が損なわれることなく全体の形状が自動的に正しく更新されます。

### コード解説 ([`constraint_demo.py`](./constraint_demo.py))
```python
# 2Dスケッチによる同心円拘束
sketch = (
    cq.Sketch()
    .circle(outer_diam / 2.0)
    .circle(inner_diam / 2.0, mode="s")  # 同心減算
)

# PCD（ピッチ円径）上の極座標アレイによる等配拘束
flange_with_holes = (
    base_flange.faces(">Z")
    .workplane()
    .polarArray(radius=pcd / 2.0, startAngle=0, angle=360, count=bolt_count)
    .hole(bolt_diam)
)
```

### 検証結果（パラメータ可変の実験）
- **標準仕様 (6穴/外径120mm/PCD90mm)**: 面 18 個 / 辺 40 個 / 頂点 24 個
- **大型仕様 (8穴/外径150mm/PCD120mm)**: 面 22 個 / 辺 50 個 / 頂点 30 個
- パラメータを変更するだけで、中心軸基準の同心関係と円周等角配置が自動維持されることを実証。 → STEPファイル: [`output_constraint.step`](./output_constraint.step)

---

## 概念 3: Feature Hierarchy (フィーチャー履歴・順序依存性)

### 概要
フィーチャー履歴（Feature Tree / Construction History）は、CADにおいて「スケッチを描く」→「押し出す」→「穴を開ける」→「角を丸める」といった操作を【実行順序を持つツリー構造】として保持する仕組みです。
フィーチャーの並び順（評価順序）を変えると、トポロジー構造（境界表現である面や辺の接続関係）や幾何形状に大きな変化が生じます。

### コード解説 ([`feature_hierarchy_demo.py`](./feature_hierarchy_demo.py))
```python
# パターン A: 穴あけ加工を行ってから全体エッジにフィレット適用
pattern_a = base.faces("<Y").workplane().cboreHole(...).edges().fillet(1.0)

# パターン B: 全体エッジにフィレット適用してから穴あけ加工
pattern_b = base.edges().fillet(1.0).faces("<Y").workplane().cboreHole(...)
```

### 検証結果（順序依存性の評価）
- **パターン A (`Hole` → `FilletAll`)**:
  - 穴が開けられた状態の境界線に対してフィレットが計算されるため、穴周りのエッジが多層的に交差し、**面: 62 個 / 辺: 126 個 / 頂点: 67 個** とトポロジーが複雑化。
- **パターン B (`FilletAll` → `Hole`)**:
  - フィレットされた角丸め形状を円柱状に貫通して穴を開けるため、**面: 47 個 / 辺: 98 個 / 頂点: 54 個** と比較的シンプルな構造に収まる。
- **結論**: CADプログラミングでは、コマンドの「呼び出し順序（Feature Hierarchy）」が最終ソリッドの品質や安定性に直結することを実証。 → STEPファイル: [`output_feature_hierarchy.step`](./output_feature_hierarchy.step)

---

## 概念 4: AI CADコード自動生成とパイプライン精緻化 (CADCoder)

### 概要
CADCoderなどのVision-AIモデルは、画像やスケッチから直接 CadQuery の Python コードを出力できます。しかし、AIが生み出す生のコード（Phase 1）は、座標値の固定値（ベタ書き）であり、変数が存在せず公差や3Dプリント向きの面取り（DfAM）が含まれていません。
本アプローチでは、「AIでラフコードを高速生成」→「人間またはLLMでパラメータ化・公差・面取り補正（Phase 2）」という2段階パイプラインを構築・実践します。

### コード解説 ([`ai_cad_pipeline_demo.py`](./ai_cad_pipeline_demo.py))
```python
# Phase 1: 生のAI生成コード（ベタ書き座標）
wp = cq.Workplane("XY")
sketch_loop = wp.moveTo(0, 0).lineTo(50, 0).lineTo(50, 15).lineTo(15, 15).lineTo(15, 50).lineTo(0, 50).close()
raw_model = wp.add(sketch_loop).extrude(30.0).faces("<Y").workplane().pushPoints([(7.5, 15.0)]).hole(6.0)

# Phase 2: パラメータ・公差(clearance=0.3mm)・DfAM面取り(chamfer)の追加
actual_hole_diam = hole_diam + clearance  # 公差考慮
sketch = cq.Sketch().segment((0, 0), (base_length, 0))...
refined_model = base_solid.faces("<Y").workplane().pushPoints([...]).cboreHole(...).edges(">Z or <Z or >X or <X").chamfer(1.0)
```

### 検証結果（B-Repと出力の比較）
- **Phase 1 (生のAIモデル)**: 面 9 個 / 辺 21 個 / 頂点 14 個 → STEP: [`output_raw_ai.step`](./output_raw_ai.step), STL: [`output_raw_ai.stl`](./output_raw_ai.stl)
- **Phase 2 (精緻化モデル)**: 面 35 個 / 辺 68 個 / 頂点 36 個 → STEP: [`output_refined_ai.step`](./output_refined_ai.step), STL: [`output_refined_ai.stl`](./output_refined_ai.stl)
- **結論**: AI生成コードをそのまま使うのではなく、変数の抽出と公差・面取りを追加するパイプラインを通すことで、一気に3Dプリント可能な高品質パーツへと昇華可能。

---

## 環境構築とスクリプト実行方法

### 動作環境
- Python 3.10+
- CadQuery 2.8+

### 実行コマンド
```bash
# PythonSandbox ディレクトリに移動
cd /Users/araiyuuki/Documents/GitHub/PythonSandbox

# スクリプトの実行
./venv/bin/python csg_demo.py
./venv/bin/python constraint_demo.py
./venv/bin/python feature_hierarchy_demo.py
./venv/bin/python ai_cad_pipeline_demo.py
```

生成された `.step` や `.stl` ファイルは、FreeCAD、Onshape、Fusion360、CQ-Editor、および各種スライサーソフト（Cura, PrusaSlicerなど）で閲覧・確認できます。
