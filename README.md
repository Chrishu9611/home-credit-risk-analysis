# Home Credit Credit Risk Analysis

基于 Kaggle 2024 竞赛 **"Home Credit - Credit Risk Model Stability"** 的信贷风险数据分析项目，用于支持东南亚（印度尼西亚）风险数据分析师求职。

## 项目目标

- 构建稳健的信用评分模型，预测客户违约概率
- 展示完整的数据分析、特征工程、建模和评估流程
- 体现对信贷风险业务和数据科学的深入理解

## 数据集

| 数据集 | 说明 | 位置 |
|--------|------|------|
| Home Credit CRMS 2024 | 主数据集（25GB，Parquet/CSV 格式） | `../home_credit_crms_2024/` |
| Home Credit Default Risk 2018 | 辅助数据集（CSV 格式） | `../` |

## 项目结构

```
.
├── data/                  # 数据目录（软链接或说明）
├── notebooks/             # Jupyter Notebook（EDA、分析）
├── src/                   # Python 源代码（工具函数、特征工程、建模）
├── models/                # 保存训练好的模型
├── reports/               # 分析报告、可视化图表
├── requirements.txt       # Python 依赖
└── README.md             # 项目说明
```

## 环境要求

- Python 3.10+
- 16GB+ 内存（推荐 32GB）
- 50GB+ 磁盘空间

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动 Jupyter
jupyter lab

# 3. 打开 notebooks/ 目录下的 notebook 开始分析
```

## 分析流程

1. **数据探索（EDA）**：理解数据分布、缺失值、目标变量分布
2. **数据清洗**：处理异常值、缺失值、数据类型转换
3. **特征工程**：基于信贷业务知识构建有效特征
4. **模型训练**：LightGBM / XGBoost / CatBoost
5. **模型评估**：AUC、KS、Gini、PSI 稳定性指标
6. **结果解释**：SHAP 分析、特征重要性、业务洞察

## 联系方式

- GitHub: [@Chrishu9611](https://github.com/Chrishu9611)
- 项目链接: https://github.com/Chrishu9611/home-credit-risk-analysis
