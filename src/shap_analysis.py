"""
SHAP 可解释性分析脚本
生成：
1. SHAP Summary Plot (beeswarm) - 全局特征重要性
2. SHAP Dependence Plot - 关键特征依赖关系
3. SHAP Waterfall Plot - 单个样本解释
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
import xgboost as xgb
from pathlib import Path
import warnings
import json
warnings.filterwarnings('ignore')

# 统一配色
COLORS = {
    'primary': '#1a365d', 'accent': '#f6ad55',
    'positive': '#3182ce', 'negative': '#e53e3e',
    'success': '#38a169', 'neutral': '#718096',
    'light': '#e2e8f0', 'bg': '#f7fafc', 'text': '#2d3748',
}

plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.edgecolor': COLORS['light'], 'axes.labelcolor': COLORS['text'],
    'axes.titlecolor': COLORS['primary'], 'xtick.color': COLORS['text'],
    'ytick.color': COLORS['text'], 'grid.color': COLORS['light'],
    'grid.alpha': 0.5, 'text.color': COLORS['text'],
    'axes.spines.top': False, 'axes.spines.right': False,
    'figure.dpi': 150,
})
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 路径
PROJECT_DIR = Path('E:/cursor/PROJECT/home_credit_default_risk/home-credit-risk-analysis')
DATA_DIR = PROJECT_DIR / 'data'
MODEL_DIR = DATA_DIR / 'model_outputs'
REPORTS_DIR = PROJECT_DIR / 'reports'
WEBSITE_IMG_DIR = PROJECT_DIR / 'docs/images'
WEBSITE_IMG_DIR.mkdir(parents=True, exist_ok=True)

print('[INFO] 加载数据...')
df = pd.read_parquet(DATA_DIR / 'train_final_features.parquet')

# 特征选择（与模型一致）
iv_df = pd.read_csv(DATA_DIR / 'iv_all_features.csv')
psi_df = pd.read_csv(DATA_DIR / 'psi_all_features.csv')
merged = iv_df.merge(psi_df[['feature', 'max_psi']], on='feature', how='inner')
selected = merged[(merged['iv'] > 0.02) & (merged['max_psi'] <= 0.25)]
selected_features = selected['feature'].tolist()

# 加载模型
print('[INFO] 加载 XGBoost 模型...')
model = xgb.Booster()
model.load_model(str(MODEL_DIR / 'xgb_model.json'))

# 数据准备
test_mask = df['WEEK_NUM_x'] >= 76
test_df = df[test_mask].copy()

for col in selected_features:
    if col not in test_df.columns:
        continue
    test_df[col] = test_df[col].replace([np.inf, -np.inf], np.nan)
    if pd.api.types.is_numeric_dtype(test_df[col]):
        median_val = test_df[col].median()
        if pd.isna(median_val):
            median_val = 0
        test_df[col] = test_df[col].fillna(median_val)
    else:
        test_df[col] = test_df[col].fillna('Missing')

numeric_features = [c for c in selected_features if pd.api.types.is_numeric_dtype(test_df[c])]
X_test = test_df[numeric_features].copy()
y_test = test_df['target'].values

# 为了计算效率，采样 2000 条（保持违约率分布）
print(f'[INFO] 原始测试集大小: {len(X_test)}')
good_idx = np.where(y_test == 0)[0]
bad_idx = np.where(y_test == 1)[0]
np.random.seed(42)
sample_good = np.random.choice(good_idx, size=min(1800, len(good_idx)), replace=False)
sample_bad = np.random.choice(bad_idx, size=min(200, len(bad_idx)), replace=False)
sample_idx = np.concatenate([sample_good, sample_bad])
np.random.shuffle(sample_idx)

X_sample = X_test.iloc[sample_idx].reset_index(drop=True)
y_sample = y_test[sample_idx]

print(f'[INFO] 采样后大小: {len(X_sample)} (违约: {y_sample.sum()}, 正常: {len(y_sample)-y_sample.sum()})')

# 获取特征中文名映射
imp_df = pd.read_csv(DATA_DIR / 'model_outputs_v2/xgboost_importance_all_with_cn.csv')
cn_map = dict(zip(imp_df['feature'], imp_df['feature_cn']))
# 修正未完全翻译的字段（源CSV中该字段的"中文名"只是原名+后缀）
cn_map['lastrejectreason_759M_te'] = '上次被拒原因_目标编码'
# 保留英文列名用于SHAP计算（XGBoost兼容性问题）
X_sample_en = X_sample.copy()
X_sample_cn = X_sample.copy()
X_sample_cn.columns = [cn_map.get(c, c) for c in X_sample_cn.columns]

# ============================================
# 1. 计算 SHAP 值（使用英文列名）
# ============================================
print('[INFO] 计算 SHAP 值 (TreeExplainer)...')
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample_en)

print(f'[INFO] SHAP values shape: {shap_values.shape}')
print(f'[INFO] Expected value (base): {explainer.expected_value:.4f}')

# 计算完SHAP后，用中文列名替换
X_sample = X_sample_cn

# ============================================
# 2. SHAP Summary Plot (Beeswarm) - 全局
# ============================================
print('[INFO] 生成 SHAP Summary Plot...')
fig, ax = plt.subplots(figsize=(12, 10))

# 使用自定义颜色映射：红（负向影响）到蓝（正向影响）
shap.summary_plot(
    shap_values, X_sample,
    max_display=20,
    show=False,
    color_bar_label='特征值高低',
)

ax = plt.gca()
ax.set_title('SHAP 全局特征重要性（TOP20）', fontsize=15, fontweight='bold',
             color=COLORS['primary'], pad=15)
ax.set_xlabel('SHAP 值（对违约概率的影响）', fontsize=12)
ax.set_ylabel('')

# 调整颜色条
cbar = fig.axes[-1]
cbar.set_ylabel('特征值', fontsize=11)

plt.tight_layout()
plt.savefig(WEBSITE_IMG_DIR / '02_shap_summary.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('[OK] 02_shap_summary.png')
plt.close()

# ============================================
# 3. SHAP Bar Plot - 全局平均绝对值
# ============================================
print('[INFO] 生成 SHAP Bar Plot...')
fig, ax = plt.subplots(figsize=(10, 8))

shap.summary_plot(
    shap_values, X_sample,
    plot_type='bar',
    max_display=20,
    show=False,
    color=COLORS['primary'],
)

ax = plt.gca()
ax.set_title('SHAP 平均特征重要性（TOP20）', fontsize=15, fontweight='bold',
             color=COLORS['primary'], pad=15)
ax.set_xlabel('平均 |SHAP 值|', fontsize=12)
ax.set_ylabel('')

plt.tight_layout()
plt.savefig(WEBSITE_IMG_DIR / '02_shap_bar.png', dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
print('[OK] 02_shap_bar.png')
plt.close()

# ============================================
# 4. Dependence Plot - TOP3 特征
# ============================================
print('[INFO] 生成 Dependence Plots...')

# 获取TOP3特征名
top3_features = imp_df.head(3)['feature_cn'].tolist()
print(f'[INFO] TOP3 特征: {top3_features}')

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

for idx, feat_name in enumerate(top3_features):
    ax = axes[idx]
    if feat_name not in X_sample.columns:
        ax.text(0.5, 0.5, f'特征未找到\n{feat_name}', ha='center', va='center',
                transform=ax.transAxes, fontsize=12)
        continue

    feat_vals = X_sample[feat_name].values
    shap_vals = shap_values[:, X_sample.columns.get_loc(feat_name)]

    # 按SHAP值着色：负（红）→ 正（蓝）
    scatter = ax.scatter(
        feat_vals, shap_vals,
        c=shap_vals, cmap='RdBu_r', s=15, alpha=0.5,
        vmin=-abs(shap_vals).max(), vmax=abs(shap_vals).max(),
        edgecolors='none'
    )

    ax.axhline(y=0, color=COLORS['neutral'], linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel(feat_name, fontsize=11)
    ax.set_ylabel('SHAP 值', fontsize=11)
    ax.set_title(feat_name, fontsize=12, fontweight='bold', color=COLORS['primary'])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

plt.suptitle('关键特征依赖关系（SHAP Dependence Plot）', fontsize=15,
             fontweight='bold', color=COLORS['primary'], y=1.02)
plt.tight_layout()
plt.savefig(WEBSITE_IMG_DIR / '02_shap_dependence_top3.png', dpi=150,
            bbox_inches='tight', facecolor='white', edgecolor='none')
print('[OK] 02_shap_dependence_top3.png')
plt.close()

# ============================================
# 5. 选择典型样本进行个体解释
# ============================================
print('[INFO] 选择典型样本...')

# 计算预测概率
prob_sample = model.predict(xgb.DMatrix(X_sample_en, missing=np.nan))

# 选择样本：
# A: 预测违约概率最高的坏客户（真阳性）
bad_mask = y_sample == 1
worst_bad_idx = np.argmax(prob_sample[bad_mask])
worst_bad_global_idx = np.where(bad_mask)[0][worst_bad_idx]

# B: 预测违约概率最低的好客户（真阴性）
good_mask = y_sample == 0
best_good_idx = np.argmin(prob_sample[good_mask])
best_good_global_idx = np.where(good_mask)[0][best_good_idx]

# C: 一个容易被误判的样本（预测高但标签为0，或预测低但标签为1）
# 找预测概率最高的好客户（潜在误判）
best_good_pred_idx = np.argmax(prob_sample[good_mask])
best_good_pred_global_idx = np.where(good_mask)[0][best_good_pred_idx]

sample_cases = [
    ('高风险坏客户（实际违约）', worst_bad_global_idx, COLORS['negative']),
    ('低风险好客户（实际正常）', best_good_global_idx, COLORS['positive']),
    ('被误判为高风险的好客户', best_good_pred_global_idx, COLORS['accent']),
]

# 存储样本解释数据
sample_explanations = []

for case_name, idx, color in sample_cases:
    print(f'\n[INFO] === 样本案例: {case_name} ===')
    row = X_sample.iloc[idx]
    shap_row = shap_values[idx]
    pred_prob = prob_sample[idx]
    actual = y_sample[idx]

    print(f'  预测违约概率: {pred_prob:.4f}')
    print(f'  实际标签: {"违约" if actual == 1 else "正常"}')
    print(f'  基础概率 (Expected Value): {explainer.expected_value:.4f}')

    # 提取TOP推动特征
    feature_impacts = list(zip(X_sample.columns, shap_row, row.values))
    feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)

    print(f'  TOP5 推动因素:')
    for f_name, f_shap, f_val in feature_impacts[:5]:
        direction = '↑ 增加风险' if f_shap > 0 else '↓ 降低风险'
        print(f'    - {f_name}: SHAP={f_shap:+.4f} ({f_val:.4f}) {direction}')

    # 保存解释数据
    sample_explanations.append({
        'case_name': case_name,
        'predicted_prob': float(pred_prob),
        'actual_label': int(actual),
        'base_value': float(explainer.expected_value),
        'top_features': [
            {'name': f_name, 'shap': float(f_shap), 'value': float(f_val)}
            for f_name, f_shap, f_val in feature_impacts[:8]
        ]
    })

    # ============================================
    # 6. 为每个样本生成 Waterfall Plot
    # ============================================
    print(f'[INFO] 生成 Waterfall Plot: {case_name}...')

    fig, ax = plt.subplots(figsize=(12, 8))

    # 取TOP10特征
    top_n = 10
    top_features = feature_impacts[:top_n]

    # 准备数据
    labels = [f[0] for f in top_features]
    values = [f[1] for f in top_features]
    feature_vals = [f[2] for f in top_features]

    # 添加基础值
    cumulative = [explainer.expected_value]
    for v in values:
        cumulative.append(cumulative[-1] + v)

    # 颜色：正向（增加风险）用红色，负向（降低风险）用蓝色
    bar_colors = [COLORS['negative'] if v > 0 else COLORS['positive'] for v in values]

    y_pos = np.arange(len(labels) + 1)

    # 绘制 waterfall
    for i in range(len(values)):
        # 连接线
        ax.plot([i+0.5, i+0.5], [cumulative[i], cumulative[i+1]],
                color=bar_colors[i], linewidth=2, alpha=0.5)
        # 条形
        bottom = min(cumulative[i], cumulative[i+1])
        height = abs(values[i])
        ax.bar(i+1, height, bottom=bottom, color=bar_colors[i], alpha=0.8,
               edgecolor='white', linewidth=1, width=0.6)

    # 绘制累积线
    ax.plot(y_pos, cumulative, 'o-', color=COLORS['neutral'], markersize=4,
            linewidth=1.5, alpha=0.7, zorder=5)

    # 标注最终预测值
    ax.axhline(y=cumulative[-1], color=COLORS['accent'], linestyle='--', linewidth=2,
               label=f'预测概率: {cumulative[-1]:.4f}')

    # 标注基础值
    ax.axhline(y=explainer.expected_value, color=COLORS['neutral'], linestyle=':',
               linewidth=1.5, alpha=0.6, label=f'基础概率: {explainer.expected_value:.4f}')

    # 设置标签
    display_labels = [f'{labels[i]}\n({feature_vals[i]:.3f})' for i in range(len(labels))]
    ax.set_xticks(range(1, len(labels)+1))
    ax.set_xticklabels(display_labels, rotation=45, ha='right', fontsize=9)

    ax.set_ylabel('违约概率（log-odds转换）', fontsize=12)
    ax.set_title(f'个体样本解释：{case_name}\n预测概率={cumulative[-1]:.4f} | 实际={"违约" if actual==1 else "正常"}',
                 fontsize=14, fontweight='bold', color=COLORS['primary'], pad=15)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10, loc='upper left')

    # 添加图例说明颜色含义
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor=COLORS['negative'], label='增加违约风险'),
        Patch(facecolor=COLORS['positive'], label='降低违约风险'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              frameon=True, fancybox=True, edgecolor=COLORS['light'])

    plt.tight_layout()

    safe_name = case_name.replace('（', '_').replace('）', '').replace(' ', '_')
    plt.savefig(WEBSITE_IMG_DIR / f'02_shap_waterfall_{safe_name}.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print(f'[OK] 02_shap_waterfall_{safe_name}.png')
    plt.close()

# ============================================
# 7. 生成样本对比汇总图
# ============================================
print('\n[INFO] 生成样本对比汇总图...')

fig, axes = plt.subplots(1, 3, figsize=(18, 7), sharey=True)

for ax_idx, (case_name, idx, color) in enumerate(sample_cases):
    ax = axes[ax_idx]
    row = X_sample.iloc[idx]
    shap_row = shap_values[idx]
    pred_prob = prob_sample[idx]
    actual = y_sample[idx]

    feature_impacts = list(zip(X_sample.columns, shap_row, row.values))
    feature_impacts.sort(key=lambda x: abs(x[1]), reverse=True)

    top_n = 8
    top_features = feature_impacts[:top_n]
    labels = [f[0][:25] for f in top_features]
    values = [f[1] for f in top_features]

    colors = [COLORS['negative'] if v > 0 else COLORS['positive'] for v in values]

    bars = ax.barh(range(len(labels)), values, color=colors, alpha=0.8,
                   edgecolor='white', linewidth=1, height=0.6)
    ax.set_yticks(range(len(labels)))
    ax.set_yticklabels(labels, fontsize=9)
    ax.invert_yaxis()
    ax.axvline(x=0, color=COLORS['neutral'], linewidth=1.5)
    ax.set_xlabel('SHAP 值', fontsize=11)
    ax.set_title(f'{case_name}\n预测={pred_prob:.3f} | 实际={"违约" if actual==1 else "正常"}',
                 fontsize=11, fontweight='bold', color=color)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.xaxis.grid(True, linestyle='--', alpha=0.3)
    ax.set_axisbelow(True)

plt.suptitle('三个典型样本的 SHAP 解释对比', fontsize=15, fontweight='bold',
             color=COLORS['primary'], y=1.02)
plt.tight_layout()
plt.savefig(WEBSITE_IMG_DIR / '02_shap_sample_comparison.png', dpi=150,
            bbox_inches='tight', facecolor='white', edgecolor='none')
print('[OK] 02_shap_sample_comparison.png')
plt.close()

# ============================================
# 8. 保存样本解释 JSON
# ============================================
json_path = WEBSITE_IMG_DIR / 'shap_sample_explanations.json'
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(sample_explanations, f, ensure_ascii=False, indent=2)
print(f'[OK] 样本解释 JSON: {json_path}')

print('\n' + '='*60)
print('SHAP 分析全部完成！')
print('='*60)
print(f'输出文件:')
print(f'  - 02_shap_summary.png (全局 Beeswarm)')
print(f'  - 02_shap_bar.png (全局 Bar)')
print(f'  - 02_shap_dependence_top3.png (TOP3 依赖关系)')
print(f'  - 02_shap_waterfall_*.png (3个个体样本瀑布图)')
print(f'  - 02_shap_sample_comparison.png (样本对比)')
print(f'  - shap_sample_explanations.json (样本数据)')
print('='*60)
