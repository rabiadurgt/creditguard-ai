### 🚀 Baseline Model Results

The current baseline model was trained using the following data sources:
* **Application data**
* **Bureau credit history aggregations**
* **Previous application aggregations**

#### 🤖 Model Configuration
* **Algorithm:** LightGBM
* **Validation Strategy:** Stratified Train/Validation Split
* **Evaluation Metric:** ROC-AUC

#### 📊 Performance
| Version | Features | ROC-AUC |
|----------|----------|----------|
| LightGBM Baseline | Application + Bureau + Previous | 0.7730 |
| + Installments | Payment behavior features | 0.7776 |
| + POS Cash | Delinquency & remaining installment features | 0.7817 |
---

### 📦 Current Feature Store

* **Raw application features**
* **Application engineered features**
* **Bureau aggregated features**
* **Previous application aggregated features**

ℹ️ **Total Features:** 150