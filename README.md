# 🚀 CreditGuard AI — Credit Risk Modeling System

CreditGuard AI is an end-to-end machine learning system designed to predict **loan default probability** using engineered financial features derived from multiple credit data sources.

The system leverages **LightGBM + feature engineering + SHAP explainability** to build a production-ready credit scoring pipeline.

---

# 📊 Project Overview

The model is trained on multiple financial data sources:

- Application data
- Bureau credit history
- Previous loan applications
- Installment payment history
- POS-CASH balance history
- Credit card balance history
- Bureau balance repayment behavior

Each dataset is transformed into **aggregated behavioral features** to capture customer credit risk patterns.

---

# 🤖 Model Configuration

- **Algorithm:** LightGBM
- **Hyperparameter Optimization:** Optuna
- **Validation Strategy:** Stratified Train/Validation Split
- **Cross Validation:** 5-Fold Stratified CV
- **Evaluation Metric:** ROC-AUC

---

# 📈 Model Performance

### 📊 Incremental Feature Engineering Impact

| Version                      | Feature Set Description                              | ROC-AUC |
|-----------------------------|-----------------------------------------------------|--------:|
| Baseline LightGBM           | Application + Bureau + Previous                    | 0.7730  |
| + Installments              | Payment behavior features                          | 0.7776  |
| + POS Cash                  | Delinquency + installment behavior                | 0.7817  |
| + Credit Card               | Credit utilization + payment behavior             | 0.7829  |
| + Bureau Balance            | Repayment history features                        | 0.7830  |
| Tuned LightGBM              | Manual hyperparameter tuning                      | 0.7867  |
| Optuna CV Tuned Model       | 5-Fold cross-validation tuning                    | 0.7883  |
| Bureau Features V2          | Advanced bureau ratios                            | 0.7880  |
| Previous Features V2        | Advanced application behavior                     | **0.7885** |

---

# 📊 Performance Gain by Feature Groups

| Feature Group                 | ROC-AUC Gain |
|------------------------------|-------------:|
| Bureau Features              | +0.02 ~ +0.03 |
| Previous Application Features| +0.01        |
| Installments Features        | +0.0046      |
| POS Cash Features            | +0.0041      |
| Credit Card Features         | +0.0012      |
| Bureau Balance Features      | +0.0001      |

---

# 🔄 Cross Validation Results (5-Fold)

| Fold | ROC-AUC |
|------|--------:|
| Fold 1 | 0.7804 |
| Fold 2 | 0.7870 |
| Fold 3 | 0.7822 |
| Fold 4 | 0.7850 |
| Fold 5 | 0.7794 |

**Mean ROC-AUC:** 0.7828  
**Std ROC-AUC:** 0.0029  

✔ Low variance indicates stable model performance across different splits.

---

# 📦 Feature Store

The feature store includes engineered features from all financial sources:

- Application-level features
- Bureau aggregated features
- Previous application features
- Installment payment features
- POS-CASH features
- Credit card features
- Bureau balance features

**Total Features:** ~200  
**Final Training Features:** 151 (after feature selection & pruning)

---

# 🏆 Most Important Features

Top predictive features identified via SHAP + feature importance:

- EXT_SOURCE_1 / 2 / 3
- pos_avg_future_installments
- total_payment_amount
- late_payment_ratio
- avg_days_late
- cc_utilization_ratio
- bureau_debt_credit_ratio
- credit_term
- annuity_credit_ratio
- refusal_rate
- prev_avg_credit_amount
- bb_record_count

These features capture **customer behavioral risk patterns** beyond raw application data.

---

# 🔍 Model Explainability (SHAP)

SHAP analysis confirms that both external risk scores and engineered behavioral features are critical in prediction.

### Key Insights:

- External sources (EXT_SOURCE) remain strong predictors
- Behavioral credit patterns significantly improve model performance
- Bureau + credit card utilization features strongly correlate with default risk

---

# 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- LightGBM
- Optuna
- Scikit-learn
- SHAP
- FastAPI
- Joblib
- Parquet

---

# 🚀 System Architecture

1. Data Extraction (raw Home Credit datasets)
2. Feature Engineering (aggregation + behavioral metrics)
3. Feature Selection (Correlation + SHAP pruning)
4. Model Training (LightGBM + Optuna tuning)
5. Feature Freeze (FINAL_FEATURES contract)
6. API Deployment (FastAPI inference service)

---

# ⚡ API (Production Ready)

- `/predict` → single risk score prediction
- Input: JSON feature dictionary
- Output:
  - risk_score (0–1)
  - risk_level (LOW / MEDIUM / HIGH)

---

# 📌 Key Achievement

✔ End-to-end ML pipeline  
✔ Feature engineering from 7 datasets  
✔ Stable cross-validation performance  
✔ SHAP explainability integration  
✔ Production-ready FastAPI service  