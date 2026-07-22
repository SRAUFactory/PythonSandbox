# PythonSandbox

Personal sandbox repository for Python experimentation and learning.

## ディレクトリ構成とコンテンツ一覧

```text
PythonSandbox/
├── README.md
├── cad_3_concepts.md
├── venv/
├── b_rep/
│   └── b_rep.py
├── csg/
│   ├── csg_demo.py
│   └── output_csg.step
├── constraint/
│   ├── constraint_demo.py
│   └── output_constraint.step
├── feature_hierarchy/
│   ├── feature_hierarchy_demo.py
│   └── output_feature_hierarchy.step
├── ai_cad_pipeline/
│   ├── ai_cad_pipeline_demo.py
│   ├── output_raw_ai.step
│   ├── output_raw_ai.stl
│   ├── output_refined_ai.step
│   └── output_refined_ai.stl
├── mongodb_sample/
└── use_llm.py
```

### 3D CADプログラミング (CadQuery)
- 📘 **[CADの3大概念およびAIコード生成パイプラインの解説と実装](./cad_3_concepts.md)**
  - [`b_rep/b_rep.py`](./b_rep/b_rep.py): B-Rep（境界表現）の基本構造（面・辺・頂点）アクセス
  - [`csg/csg_demo.py`](./csg/csg_demo.py): 基本立体の集合演算（和・差・積）とバルブボディ構築
  - [`constraint/constraint_demo.py`](./constraint/constraint_demo.py): 2D/3D拘束とパラメータ可変配管フランジ設計
  - [`feature_hierarchy/feature_hierarchy_demo.py`](./feature_hierarchy/feature_hierarchy_demo.py): フィーチャー加工履歴と順序依存性の検証
  - [`ai_cad_pipeline/ai_cad_pipeline_demo.py`](./ai_cad_pipeline/ai_cad_pipeline_demo.py): CADCoder（Vision-AI）が生成したコードの受領と、パラメータ・公差・DfAM面取り補正パイプライン

### その他
- [`use_llm.py`](./use_llm.py): LLM API試作スクリプト
- `mongodb_sample/`: MongoDB / PyMongo 接続サンプル
