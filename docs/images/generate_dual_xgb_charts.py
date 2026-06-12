"""
生成双XGBoost模型对比配图（网页风格一致）
图1: 4种模型子群表现对比
图2: 双XGB关键变量TOP10
"""
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 网页配色方案
PRIMARY = '#1a365d'
PRIMARY_LIGHT = '#2c5282'
ACCENT = '#f6ad55'
SUCCESS = '#38a169'
DANGER = '#e53e3e'
INFO = '#3182ce'
PURPLE = '#805ad5'
TEXT = '#2d3748'
TEXT_LIGHT = '#718096'
BG = '#f7fafc'
CARD_BG = '#ffffff'
BORDER = '#e2e8f0'

plt.rcParams['axes.facecolor'] = CARD_BG
plt.rcParams['figure.facecolor'] = BG
plt.rcParams['axes.edgecolor'] = BORDER
plt.rcParams['axes.labelcolor'] = TEXT
plt.rcParams['xtick.color'] = TEXT_LIGHT
plt.rcParams['ytick.color'] = TEXT_LIGHT
plt.rcParams['text.color'] = TEXT
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False
plt.rcParams['figure.dpi'] = 150

output_dir = r'E:\cursor\PROJECT\home_credit_default_risk\home-credit-risk-analysis\docs\images'

# ==================== 图1：4种模型子群表现对比（非白户 & 白户） ====================
print("生成图1: 4种模型子群表现对比...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
fig.patch.set_facecolor(BG)

models = ['XGBoost', 'LightGBM', 'DecisionTree', 'Logistic\nRegression']
colors = [INFO, SUCCESS, ACCENT, PURPLE]

# 左图：非白户
nw_auc = [0.8457, 0.8453, 0.7754, 0.7955]
nw_ks = [0.5322, 0.5308, 0.4284, 0.4515]

x = np.arange(len(models))
width = 0.35

bars_nw1 = axes[0].bar(x - width/2, nw_auc, width, label='AUC', color=INFO, edgecolor='white', linewidth=1.5, zorder=3)
bars_nw2 = axes[0].bar(x + width/2, [v/2 for v in nw_ks], width, label='KS (×2)', color=ACCENT, edgecolor='white', linewidth=1.5, zorder=3)
# 实际上把KS放大2倍放同一刻度不太好看，让我用双y轴
axes[0].clear()
axes[0].set_facecolor(CARD_BG)
axes[0].set_axisbelow(True)

ax1_twin = axes[0].twinx()
bars_nw1 = axes[0].bar(x - width/2, nw_auc, width, label='AUC', color=INFO, edgecolor='white', linewidth=1.5, zorder=3)
bars_nw2 = ax1_twin.bar(x + width/2, nw_ks, width, label='KS', color=ACCENT, edgecolor='white', linewidth=1.5, zorder=3)

axes[0].set_ylabel('AUC', fontsize=12, fontweight='600', color=INFO)
axes[0].tick_params(axis='y', labelcolor=INFO)
ax1_twin.set_ylabel('KS', fontsize=12, fontweight='600', color=ACCENT)
ax1_twin.tick_params(axis='y', labelcolor=ACCENT)
ax1_twin.spines['top'].set_visible(False)
axes[0].set_title('非白户子群（测试集）', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
axes[0].set_xticks(x)
axes[0].set_xticklabels(models, fontsize=10)
axes[0].set_ylim(0.70, 0.90)
ax1_twin.set_ylim(0.30, 0.60)
axes[0].yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)

# 合并图例
lines1, labels1 = axes[0].get_legend_handles_labels()
lines2, labels2 = ax1_twin.get_legend_handles_labels()
axes[0].legend(lines1 + lines2, labels1 + labels2, loc='lower right', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)

for bar, val in zip(bars_nw1, nw_auc):
    axes[0].annotate(f'{val:.4f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=9, fontweight='600', color=INFO)
for bar, val in zip(bars_nw2, nw_ks):
    ax1_twin.annotate(f'{val:.4f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=9, fontweight='600', color=ACCENT)

# 右图：白户
w_auc = [0.8026, 0.8011, 0.7300, 0.6781]
w_ks = [0.4981, 0.4657, 0.3099, 0.3029]

ax2_twin = axes[1].twinx()
bars_w1 = axes[1].bar(x - width/2, w_auc, width, label='AUC', color=INFO, edgecolor='white', linewidth=1.5, zorder=3)
bars_w2 = ax2_twin.bar(x + width/2, w_ks, width, label='KS', color=ACCENT, edgecolor='white', linewidth=1.5, zorder=3)

axes[1].set_ylabel('AUC', fontsize=12, fontweight='600', color=INFO)
axes[1].tick_params(axis='y', labelcolor=INFO)
ax2_twin.set_ylabel('KS', fontsize=12, fontweight='600', color=ACCENT)
ax2_twin.tick_params(axis='y', labelcolor=ACCENT)
ax2_twin.spines['top'].set_visible(False)
axes[1].set_title('白户子群（测试集）', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
axes[1].set_xticks(x)
axes[1].set_xticklabels(models, fontsize=10)
axes[1].set_ylim(0.55, 0.88)
ax2_twin.set_ylim(0.15, 0.60)
axes[1].yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)

lines3, labels3 = axes[1].get_legend_handles_labels()
lines4, labels4 = ax2_twin.get_legend_handles_labels()
axes[1].legend(lines3 + lines4, labels3 + labels4, loc='lower right', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)

for bar, val in zip(bars_w1, w_auc):
    axes[1].annotate(f'{val:.4f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=9, fontweight='600', color=INFO)
for bar, val in zip(bars_w2, w_ks):
    ax2_twin.annotate(f'{val:.4f}', xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points", ha='center', va='bottom',
                fontsize=9, fontweight='600', color=ACCENT)

plt.tight_layout(pad=3)
plt.savefig(f'{output_dir}/four_models_subgroup_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  图1完成")

# ==================== 图2：双XGB关键变量TOP10对比 ====================
print("生成图2: 双XGB关键变量TOP10...")
fig, axes = plt.subplots(1, 2, figsize=(16, 6.5))
fig.patch.set_facecolor(BG)

# 非白户TOP10
nw_features_cn = [
    '账户关闭24月内\n平均逾期天数',
    '近9个月\n拒贷次数',
    '最近拒贷原因\n(WOE编码)',
    '历史申请D状态\n计数(近6月)',
    '征信局A\n逾期占比',
    '征信局A\n逾期>30天占比',
    '征信120天\n逾期天数',
    '近6月/近12月\n逾期比值',
    '历史申请\n最大期限(近6月)',
    '近6个月\n最大逾期天数',
]
nw_importance = [7.04, 5.83, 3.78, 3.36, 3.06, 2.86, 2.48, 2.35, 1.95, 1.76]

# 白户TOP10
w_features_cn = [
    '年龄<25岁',
    '已婚且有担保 🆕',
    '付款金额变异系数 🆕',
    '税务记录数',
    '月均付款/年金比 🆕',
    '年龄<30岁 🆕',
    '税务总收入',
    '征信月均付款金额',
    '信贷类型(WOE编码)',
    '年龄(岁)',
]
w_importance = [5.23, 3.34, 2.79, 2.75, 2.67, 2.54, 2.02, 1.93, 1.91, 1.84]

# 左图：非白户
y_nw = np.arange(len(nw_features_cn))
colors_nw = [DANGER if v > 5 else (ACCENT if v > 3 else INFO) for v in nw_importance]
bars_nw = axes[0].barh(y_nw, nw_importance, height=0.6, color=colors_nw, edgecolor='white', linewidth=1.5, zorder=3)

axes[0].set_yticks(y_nw)
axes[0].set_yticklabels(nw_features_cn, fontsize=8)
axes[0].invert_yaxis()
axes[0].set_xlabel('Gain 重要度占比 (%)', fontsize=11, fontweight='600')
axes[0].set_title('非白户 XGBoost 模型 TOP10', fontsize=13, fontweight='700', color=PRIMARY, pad=12)
axes[0].xaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
axes[0].set_axisbelow(True)

for bar, val in zip(bars_nw, nw_importance):
    axes[0].annotate(f'{val:.1f}%', xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                xytext=(5, 0), textcoords="offset points", ha='left', va='center',
                fontsize=9, fontweight='600', color=TEXT)

# 右图：白户
y_w = np.arange(len(w_features_cn))
colors_w = [SUCCESS if '🆕' in f else INFO for f in w_features_cn]
bars_w = axes[1].barh(y_w, w_importance, height=0.6, color=colors_w, edgecolor='white', linewidth=1.5, zorder=3)

axes[1].set_yticks(y_w)
axes[1].set_yticklabels(w_features_cn, fontsize=8)
axes[1].invert_yaxis()
axes[1].set_xlabel('Gain 重要度占比 (%)', fontsize=11, fontweight='600')
axes[1].set_title('白户 XGBoost 模型 TOP10', fontsize=13, fontweight='700', color=PRIMARY, pad=12)
axes[1].xaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
axes[1].set_axisbelow(True)

for bar, val in zip(bars_w, w_importance):
    axes[1].annotate(f'{val:.1f}%', xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                xytext=(5, 0), textcoords="offset points", ha='left', va='center',
                fontsize=9, fontweight='600', color=TEXT)

plt.tight_layout(pad=3)
plt.savefig(f'{output_dir}/dual_xgb_top10_features.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  图2完成")

# ==================== 图3：16种组合AUC矩阵热力图 ====================
print("生成图3: 16种组合AUC矩阵热力图...")
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor(BG)

auc_data = np.array([
    [0.8420, 0.8274, 0.8430, 0.8261],
    [0.8420, 0.8285, 0.8427, 0.8264],
    [0.7719, 0.7597, 0.7739, 0.7596],
    [0.7846, 0.7922, 0.7816, 0.7851],
])

im = ax.imshow(auc_data, cmap='YlOrRd', aspect='auto', vmin=0.75, vmax=0.85)

nw_labels = ['XGBoost', 'LightGBM', 'DecisionTree', 'Logistic\nRegression']
w_labels = ['XGBoost', 'LightGBM', 'DecisionTree', 'Logistic\nRegression']

ax.set_xticks(np.arange(len(w_labels)))
ax.set_yticks(np.arange(len(nw_labels)))
ax.set_xticklabels(w_labels, fontsize=11)
ax.set_yticklabels(nw_labels, fontsize=11)
ax.set_xlabel('白户子模型', fontsize=13, fontweight='700', color=PRIMARY)
ax.set_ylabel('非白户子模型', fontsize=13, fontweight='700', color=PRIMARY)
ax.set_title('16种双模型组合 — 全量测试集 AUC 矩阵', fontsize=14, fontweight='700', color=PRIMARY, pad=15)

# 添加数值标注
for i in range(len(nw_labels)):
    for j in range(len(w_labels)):
        val = auc_data[i, j]
        color = 'white' if val > 0.81 else TEXT
        weight = 'bold' if val == auc_data.max() else 'normal'
        ax.text(j, i, f'{val:.4f}', ha='center', va='center', fontsize=12, fontweight=weight, color=color)

# 高亮最优
best_idx = np.unravel_index(auc_data.argmax(), auc_data.shape)
ax.add_patch(plt.Rectangle((best_idx[1]-0.5, best_idx[0]-0.5), 1, 1, fill=False, edgecolor=SUCCESS, linewidth=3, linestyle='-'))

# 高亮双XGB
xgb_idx = (0, 0)
ax.add_patch(plt.Rectangle((xgb_idx[1]-0.5, xgb_idx[0]-0.5), 1, 1, fill=False, edgecolor='#1a365d', linewidth=3, linestyle='--'))
ax.annotate('⭐ 推荐', xy=(xgb_idx[1], xgb_idx[0]-0.6), ha='center', fontsize=10, fontweight='700', color='#1a365d')

cbar = plt.colorbar(im, ax=ax, shrink=0.85, pad=0.02)
cbar.set_label('AUC', fontsize=11, fontweight='600')

plt.tight_layout(pad=2)
plt.savefig(f'{output_dir}/cross_comparison_auc_matrix.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()
print("  图3完成")

print("\n所有配图生成完成！")
