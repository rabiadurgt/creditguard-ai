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
| Model | ROC-AUC |
| :--- | :--- |
| **LightGBM Baseline** | **0.7724** |

---

### 📦 Current Feature Store

* **Raw application features**
* **Application engineered features**
* **Bureau aggregated features**
* **Previous application aggregated features**

ℹ️ **Total Features:** 150
