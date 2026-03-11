Great — this is a **core implementation repository in the architecture**, and it must be designed very carefully because **this is where most engineers will actually work**.

This repo must:

* allow **domain teams to build AI systems**
* prevent **governance logic leakage**
* prevent **adapter/infrastructure coupling**
* keep **determinism intact**
* allow **intent-driven execution**

The rule for this repository is:

```
Domain Services define WHAT the system does
Platform SDK decides HOW it runs
Adapters decide WHERE it runs
```

So the Domain Service repo must contain:

```
intents
tasks
workflows
domain schemas
model logic
evaluation logic
service configs
```

but **must never contain**:

```
governance rules
artifact hashing
reconciliation
plan compilation
infrastructure adapters
```

Those belong to **Platform SDK**.

Below is a **production-grade Domain Service repository structure**.

---

# 📦 Repository C — Domain Service

Example: `forex-ml-service`

```
forex-ml-service/
│
├── README.md
├── LICENSE
├── CODEOWNERS
├── pyproject.toml
├── Makefile
│
├── docs/
│   ├── service_architecture.md
│   ├── model_design.md
│   ├── feature_definitions.md
│   └── evaluation_strategy.md
│
├── configs/
│   ├── service_config.yaml
│   ├── runtime_settings.yaml
│   └── model_config.yaml
│
├── intents/                         # USER INTENT DEFINITIONS
│   ├── forex_training_intent.yaml
│   ├── forex_inference_intent.yaml
│   └── forex_backtest_intent.yaml
│
├── intent_schemas/
│   ├── training_intent_schema.yaml
│   ├── inference_intent_schema.yaml
│   └── backtest_intent_schema.yaml
│
├── workflows/                       # WORKFLOW DEFINITIONS
│
│   ├── training/
│   │   ├── training_workflow.py
│   │   ├── dataset_pipeline.py
│   │   ├── feature_pipeline.py
│   │   ├── model_training.py
│   │   └── evaluation_pipeline.py
│   │
│   ├── inference/
│   │   ├── inference_workflow.py
│   │   └── prediction_pipeline.py
│   │
│   └── backtest/
│       ├── backtest_workflow.py
│       └── strategy_simulation.py
│
├── tasks/                           # ATOMIC EXECUTION UNITS
│
│   ├── data/
│   │   ├── ingest_forex_data.py
│   │   └── clean_forex_data.py
│   │
│   ├── features/
│   │   ├── compute_features.py
│   │   ├── feature_normalization.py
│   │   └── feature_selection.py
│   │
│   ├── training/
│   │   ├── train_model.py
│   │   ├── hyperparameter_search.py
│   │   └── model_serialization.py
│   │
│   ├── evaluation/
│   │   ├── evaluate_model.py
│   │   ├── compute_metrics.py
│   │   └── generate_report.py
│   │
│   └── inference/
│       ├── load_model.py
│       └── generate_predictions.py
│
├── models/                          # MODEL IMPLEMENTATIONS
│   ├── architectures/
│   │   ├── xgboost_model.py
│   │   ├── lstm_model.py
│   │   └── transformer_model.py
│   │
│   ├── training/
│   │   ├── training_loop.py
│   │   └── loss_functions.py
│   │
│   └── serialization/
│       └── model_serializer.py
│
├── features/                        # FEATURE DEFINITIONS
│   ├── price_features.py
│   ├── volatility_features.py
│   ├── technical_indicators.py
│   └── feature_registry.py
│
├── datasets/                        # DATASET DEFINITIONS
│   ├── forex_dataset.py
│   ├── dataset_schema.py
│   └── dataset_validation.py
│
├── evaluation/                      # MODEL EVALUATION
│   ├── metrics/
│   │   ├── sharpe_ratio.py
│   │   ├── qlike.py
│   │   └── directional_accuracy.py
│   │
│   ├── validation/
│   │   ├── cross_validation.py
│   │   └── rolling_window_validation.py
│   │
│   └── reporting/
│       └── evaluation_report.py
│
├── domain_logic/                    # DOMAIN-SPECIFIC RULES
│   ├── forex_market_hours.py
│   ├── currency_pair_registry.py
│   └── trading_calendar.py
│
├── planners/                        # OPTIONAL DOMAIN PLANNERS
│   └── workflow_planner.py
│
├── cli/
│   ├── run_training.py
│   ├── run_backtest.py
│   └── run_inference.py
│
├── examples/
│   ├── training_intent_example.yaml
│   ├── inference_intent_example.yaml
│   └── backtest_example.yaml
│
├── ci_cd/
│   ├── service_compile.yaml
│   ├── workflow_tests.yaml
│   └── model_validation.yaml
│
└── tests/
│
    ├── tasks/
    │   ├── test_data_tasks.py
    │   ├── test_feature_tasks.py
    │   └── test_training_tasks.py
    │
    ├── workflows/
    │   ├── test_training_workflow.py
    │   └── test_inference_workflow.py
    │
    ├── models/
    │   └── test_models.py
    │
    └── evaluation/
        └── test_metrics.py
```

---

# Key Architectural Rules for Domain Services

## 1️⃣ Domain Services Define Business Logic Only

Allowed:

```
datasets
features
models
workflows
tasks
evaluation metrics
domain rules
```

Not allowed:

```
artifact hashing
reconciliation
governance policy enforcement
plan compilation
adapter implementation
```

Those live in **Platform SDK**.

---

# 2️⃣ Workflows Compose Tasks

Example training workflow:

```
ingest_data
     ↓
feature_pipeline
     ↓
training
     ↓
evaluation
```

The workflow **declares the execution graph**, but execution is performed by the **Platform Runtime**.

---

# 3️⃣ Intents Define User Interface

Example intent:

```yaml
kind: ForexTraining

spec:
  dataset: eurusd_hourly
  prediction_target: volatility
  training_frequency: weekly
```

The planner converts this into **platform plans**.

---

# 4️⃣ Tasks Must Be Deterministic

Every task must:

```
take immutable inputs
produce immutable outputs
declare artifacts
```

Example:

```
train_model(dataset_hash, feature_hash) → model_hash
```

---

# 5️⃣ Domain Services Cannot Directly Access Infrastructure

No direct use of:

```
AWS SDK
Spark clusters
Kubernetes
```

All execution goes through **adapters selected by the Platform SDK**.

---

# 6️⃣ Testing Strategy

Domain repos must test:

```
tasks
workflows
models
evaluation metrics
```

But not:

```
governance
artifact registry
reconciliation
```

Those are tested in **Platform SDK**.

---

# Final System Architecture

After defining all three repos:

```
platform-sdk
        ↓
platform-adapters
        ↓
domain-services
```

Conceptually:

```
Kernel → Platform SDK
Drivers → Adapter Packs
Applications → Domain Services
```

---

# Result

This architecture allows organizations to build **hundreds of domain services safely**, while the governance kernel guarantees:

```
deterministic execution
artifact lineage
policy enforcement
reproducibility
```

---
