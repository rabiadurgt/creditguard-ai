### 🚀 Baseline Model Results

The current baseline model was trained using the following data sources:

* **Application data**
* **Bureau credit history aggregations**
* **Previous application aggregations**
* **Installments payment behavior**
* **POS Cash balance history**
* **Credit Card balance history**
* **Bureau Balance repayment history**

#### 🤖 Model Configuration

* **Algorithm:** LightGBM
* **Validation Strategy:** Stratified Train/Validation Split
* **Evaluation Metric:** ROC-AUC

#### 📊 Performance

| Version           | Features                                            | ROC-AUC    |
| ----------------- | --------------------------------------------------- | ---------- |
| LightGBM Baseline | Application + Bureau + Previous                     | 0.7730     |
| + Installments    | Payment behavior features                           | 0.7776     |
| + POS Cash        | Delinquency & remaining installment features        | 0.7817     |
| + Credit Card     | Credit card utilization & payment behavior features | 0.7829     |
| + Bureau Balance  | Bureau repayment history features                   | **0.7830** |

#### 📈 Performance Gain

| Feature Group                 | ROC-AUC Gain |
| ----------------------------- | -----------: |
| Bureau Features               |   +0.02~0.03 |
| Previous Application Features |        +0.01 |
| Installments Features         |      +0.0046 |
| POS Cash Features             |      +0.0041 |
| Credit Card Features          |      +0.0012 |
| Bureau Balance Features       |      +0.0001 |

**Current Best Validation ROC-AUC:** **0.7830**

---

### 📦 Current Feature Store

The feature store currently contains:

* Raw application features
* Application engineered features
* Bureau aggregated features
* Previous application aggregated features
* Installments payment features
* POS Cash aggregated features
* Credit Card aggregated features
* Bureau Balance aggregated features

ℹ️ **Total Features:** 180 columns in feature store
ℹ️ **Training Features:** 178 columns after preprocessing and target separation

---

### 🏆 Most Important Engineered Features

Among the engineered features, the following variables consistently rank among the most predictive:

* `credit_term`
* `annuity_credit_ratio`
* `bureau_total_credit`
* `bureau_debt_credit_ratio`
* `bureau_total_debt`
* `credit_income_ratio`
* `annuity_income_ratio`
* `age_years`
* `prev_avg_application_amount`
* `prev_avg_credit_amount`
* `installment_count`
* `avg_days_late`
* `late_payment_ratio`
* `total_payment_amount`
* `pos_active_contracts`
* `pos_avg_future_installments`
* `cc_utilization_ratio`
* `cc_avg_drawings`
* `bb_record_count`
* `bb_history_length`

These features significantly improve the model's ability to capture customer credit risk patterns beyond the raw application data.

---

### 🔍 Model Explainability (SHAP)

To improve model transparency and interpretability, SHAP (SHapley Additive exPlanations) analysis was performed on the final LightGBM model.

#### Most Influential Features

The SHAP analysis showed that, besides the well-known Home Credit external risk scores (`EXT_SOURCE_1`, `EXT_SOURCE_2`, `EXT_SOURCE_3`), several engineered features became among the most important predictors:

* `pos_avg_future_installments`
* `total_payment_amount`
* `late_payment_ratio`
* `avg_days_late`
* `cc_utilization_ratio`
* `bureau_debt_credit_ratio`
* `credit_term`
* `annuity_credit_ratio`
* `refusal_rate`
* `bb_record_count`

These results confirm that the engineered behavioral credit-risk features significantly contribute to the model's predictive performance and provide meaningful business insights regarding customer repayment behavior.
