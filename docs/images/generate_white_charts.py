import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 网页配色方案
PRIMARY = '#1a365d'
PRIMARY_LIGHT = '#2c5282'
ACCENT = '#f6ad55'
SUCCESS = '#38a169'
DANGER = '#e53e3e'
INFO = '#3182ce'
TEXT = '#2d3748'
TEXT_LIGHT = '#718096'
BG = '#f7fafc'
CARD_BG = '#ffffff'
BORDER = '#e2e8f0'

# 统一风格设置
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

# ===================== 图1：白户模型效果对比 =====================
print("生成图1: 白户模型效果对比...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
fig.patch.set_facecolor(BG)

# 左图：AUC对比
models = ['单模型\n(全量通用)', '双模型\n(白户子模型)']
white_auc = [0.7544, 0.8026]
nonwhite_auc = [0.8471, 0.8471]

x = np.arange(len(models))
width = 0.35

bars1 = axes[0].bar(x - width/2, white_auc, width, label='白户', color=ACCENT, edgecolor='white', linewidth=1.5, zorder=3)
bars2 = axes[0].bar(x + width/2, nonwhite_auc, width, label='非白户', color=PRIMARY_LIGHT, edgecolor='white', linewidth=1.5, zorder=3)

axes[0].set_ylabel('Test AUC', fontsize=12, fontweight='600')
axes[0].set_title('白户 vs 非白户：Test AUC 对比', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
axes[0].set_xticks(x)
axes[0].set_xticklabels(models, fontsize=11)
axes[0].legend(loc='lower right', frameon=True, fancybox=True, shadow=False, facecolor=CARD_BG, edgecolor=BORDER)
axes[0].set_ylim(0.70, 0.88)
axes[0].yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
axes[0].set_axisbelow(True)

# 添加数值标签
for bar in bars1:
    height = bar.get_height()
    axes[0].annotate(f'{height:.4f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='600', color=ACCENT)
for bar in bars2:
    height = bar.get_height()
    axes[0].annotate(f'{height:.4f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='600', color=PRIMARY_LIGHT)

# 右图：KS对比
white_ks = [0.3843, 0.4981]
nonwhite_ks = [0.5391, 0.5391]

bars3 = axes[1].bar(x - width/2, white_ks, width, label='白户', color=ACCENT, edgecolor='white', linewidth=1.5, zorder=3)
bars4 = axes[1].bar(x + width/2, nonwhite_ks, width, label='非白户', color=PRIMARY_LIGHT, edgecolor='white', linewidth=1.5, zorder=3)

axes[1].set_ylabel('Test KS', fontsize=12, fontweight='600')
axes[1].set_title('白户 vs 非白户：Test KS 对比', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
axes[1].set_xticks(x)
axes[1].set_xticklabels(models, fontsize=11)
axes[1].legend(loc='lower right', frameon=True, fancybox=True, shadow=False, facecolor=CARD_BG, edgecolor=BORDER)
axes[1].set_ylim(0.30, 0.60)
axes[1].yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
axes[1].set_axisbelow(True)

for bar in bars3:
    height = bar.get_height()
    axes[1].annotate(f'{height:.4f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='600', color=ACCENT)
for bar in bars4:
    height = bar.get_height()
    axes[1].annotate(f'{height:.4f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=10, fontweight='600', color=PRIMARY_LIGHT)

plt.tight_layout(pad=3)
plt.savefig(f'{output_dir}/white_model_comparison.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ===================== 图2：评分分布对比 =====================
print("生成图2: 白户评分分布对比...")
fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor(BG)

# 模拟评分分布（基于实际统计值）
np.random.seed(42)
# 白户单模型：均值805.49, std16.32
white_single = np.random.normal(805.49, 16.32, 5000)
white_single = np.clip(white_single, 650, 900)
# 白户双模型：均值729.35, std26.16
white_dual = np.random.normal(729.35, 26.16, 5000)
white_dual = np.clip(white_dual, 600, 850)
# 非白户：均值804.46, std36.78
nonwhite = np.random.normal(804.46, 36.78, 50000)
nonwhite = np.clip(nonwhite, 620, 920)

bins = np.linspace(600, 900, 50)
ax.hist(white_single, bins=bins, alpha=0.5, label='白户-单模型 (mean=805)', color=DANGER, density=True, zorder=2)
ax.hist(white_dual, bins=bins, alpha=0.7, label='白户-双模型 (mean=729)', color=ACCENT, density=True, zorder=3)
ax.hist(nonwhite, bins=bins, alpha=0.4, label='非白户 (mean=804)', color=PRIMARY_LIGHT, density=True, zorder=1)

ax.set_xlabel('信用评分', fontsize=12, fontweight='600')
ax.set_ylabel('密度', fontsize=12, fontweight='600')
ax.set_title('评分分布对比：单模型 vs 双模型', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
ax.legend(loc='upper left', frameon=True, fancybox=True, facecolor=CARD_BG, edgecolor=BORDER)
ax.yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
ax.set_axisbelow(True)
ax.set_xlim(600, 900)

# 添加阈值标注
ax.axvline(x=720, color=SUCCESS, linestyle='--', linewidth=2, alpha=0.8, label='非白户阈值 720')
ax.axvline(x=740, color=DANGER, linestyle='--', linewidth=2, alpha=0.8, label='白户阈值 740')

# 重新绘制legend以包含阈值线
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left', frameon=True, fancybox=True, facecolor=CARD_BG, edgecolor=BORDER)

plt.tight_layout(pad=2)
plt.savefig(f'{output_dir}/white_score_distribution.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ===================== 图3：白户评分卡分箱图 =====================
print("生成图3: 白户评分卡分箱图...")
fig, ax = plt.subplots(figsize=(12, 5.5))
fig.patch.set_facecolor(BG)

# 白户评分卡数据
score_bins = ['615~697', '697~707', '707~714', '714~721', '721~728', '728~736', '736~745', '745~755', '755~765', '765~807']
bad_rates = [9.28, 5.36, 1.86, 1.65, 1.44, 0.62, 0.62, 0.62, 0.41, 0.21]
cum_bad = [42.1, 66.4, 74.8, 82.2, 88.8, 91.6, 94.4, 97.2, 99.1, 100.0]

x_pos = np.arange(len(score_bins))
colors = [DANGER if br > 5 else (ACCENT if br > 1 else SUCCESS) for br in bad_rates]

bars = ax.bar(x_pos, bad_rates, color=colors, edgecolor='white', linewidth=1.5, zorder=3, width=0.7)

# 添加累积坏客率折线
ax2 = ax.twinx()
ax2.plot(x_pos, cum_bad, color=PRIMARY, marker='o', markersize=6, linewidth=2.5, zorder=5, label='累积坏客%')
ax2.set_ylabel('累积坏客占比 (%)', fontsize=11, fontweight='600', color=PRIMARY)
ax2.tick_params(axis='y', labelcolor=PRIMARY)
ax2.set_ylim(0, 110)
ax2.spines['top'].set_visible(False)

ax.set_xlabel('评分分段', fontsize=12, fontweight='600')
ax.set_ylabel('坏客率 (%)', fontsize=12, fontweight='600')
ax.set_title('白户评分卡：等频10分箱坏客率分布', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
ax.set_xticks(x_pos)
ax.set_xticklabels(score_bins, rotation=30, ha='right', fontsize=9)
ax.yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
ax.set_axisbelow(True)

# 添加数值标签
for i, (bar, br, cb) in enumerate(zip(bars, bad_rates, cum_bad)):
    ax.annotate(f'{br:.2f}%',
                xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 5), textcoords="offset points",
                ha='center', va='bottom', fontsize=8, fontweight='600', color=colors[i])

ax.legend(['坏客率'], loc='upper left', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)
ax2.legend(loc='upper center', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)

plt.tight_layout(pad=2)
plt.savefig(f'{output_dir}/white_scorecard_bins.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ===================== 图4：阈值策略图 =====================
print("生成图4: 阈值策略分析图...")
fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
fig.patch.set_facecolor(BG)

# 左图：白户阈值分析
thresholds = [660, 680, 700, 720, 740, 760, 780]
white_pass = [99.5, 97.5, 87.1, 61.7, 35.3, 15.8, 1.1]
white_bad = [2.03, 1.86, 1.25, 0.64, 0.47, 0.39, 0.00]

ax1 = axes[0]
ax1_twin = ax1.twinx()

l1 = ax1.plot(thresholds, white_pass, color=INFO, marker='o', markersize=7, linewidth=2.5, label='通过率', zorder=3)
l2 = ax1_twin.plot(thresholds, white_bad, color=DANGER, marker='s', markersize=7, linewidth=2.5, label='通过样本坏客率', zorder=3)

ax1.axvline(x=740, color=ACCENT, linestyle='--', linewidth=2, alpha=0.8)
ax1.annotate('推荐阈值 740', xy=(740, 50), xytext=(755, 60),
            fontsize=10, fontweight='600', color=ACCENT,
            arrowprops=dict(arrowstyle='->', color=ACCENT, lw=1.5))

ax1.set_xlabel('评分阈值', fontsize=12, fontweight='600')
ax1.set_ylabel('通过率 (%)', fontsize=11, fontweight='600', color=INFO)
ax1_twin.set_ylabel('通过样本坏客率 (%)', fontsize=11, fontweight='600', color=DANGER)
ax1.set_title('白户：阈值策略分析', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
ax1.tick_params(axis='y', labelcolor=INFO)
ax1_twin.tick_params(axis='y', labelcolor=DANGER)
ax1.yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
ax1.set_axisbelow(True)
ax1.set_ylim(0, 110)
ax1_twin.set_ylim(0, 3)
ax1_twin.spines['top'].set_visible(False)

lines = l1 + l2
labels = [l.get_label() for l in lines]
ax1.legend(lines, labels, loc='center right', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)

# 右图：非白户阈值分析
nonwhite_pass = [100.0, 99.9, 99.7, 98.7, 95.4, 87.6, 74.4]
nonwhite_bad = [2.16, 2.13, 2.05, 1.85, 1.49, 1.04, 0.64]

ax2 = axes[1]
ax2_twin = ax2.twinx()

l3 = ax2.plot(thresholds, nonwhite_pass, color=INFO, marker='o', markersize=7, linewidth=2.5, label='通过率', zorder=3)
l4 = ax2_twin.plot(thresholds, nonwhite_bad, color=DANGER, marker='s', markersize=7, linewidth=2.5, label='通过样本坏客率', zorder=3)

ax2.axvline(x=720, color=SUCCESS, linestyle='--', linewidth=2, alpha=0.8)
ax2.annotate('推荐阈值 720', xy=(720, 95), xytext=(735, 85),
            fontsize=10, fontweight='600', color=SUCCESS,
            arrowprops=dict(arrowstyle='->', color=SUCCESS, lw=1.5))

ax2.set_xlabel('评分阈值', fontsize=12, fontweight='600')
ax2.set_ylabel('通过率 (%)', fontsize=11, fontweight='600', color=INFO)
ax2_twin.set_ylabel('通过样本坏客率 (%)', fontsize=11, fontweight='600', color=DANGER)
ax2.set_title('非白户：阈值策略分析', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
ax2.tick_params(axis='y', labelcolor=INFO)
ax2_twin.tick_params(axis='y', labelcolor=DANGER)
ax2.yaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
ax2.set_axisbelow(True)
ax2.set_ylim(60, 105)
ax2_twin.set_ylim(0, 3)
ax2_twin.spines['top'].set_visible(False)

lines2 = l3 + l4
labels2 = [l.get_label() for l in lines2]
ax2.legend(lines2, labels2, loc='center right', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)

plt.tight_layout(pad=3)
plt.savefig(f'{output_dir}/white_threshold_strategy.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

# ===================== 图5：白户高IV特征TOP10 =====================
print("生成图5: 白户高IV特征TOP10...")
fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BG)

features = ['cb_pmt_avg', 'person_age_days', 'cb_pmt_count_total', 'person_age_gt50',
            'person_age_lt30', 'person_is_married', 'tax_registry_c_record_count',
            'cb_pmtscount', 'person_education_level', 'price_1097A']
white_iv = [0.197, 0.176, 0.162, 0.144, 0.127, 0.093, 0.069, 0.069, 0.061, 0.060]
all_iv = [0.093, 0.096, 0.055, 0.000, 0.000, 0.000, 0.028, 0.010, 0.014, 0.028]

y_pos = np.arange(len(features))
height = 0.35

bars1 = ax.barh(y_pos + height/2, white_iv, height, label='白户 IV', color=ACCENT, edgecolor='white', linewidth=1.5, zorder=3)
bars2 = ax.barh(y_pos - height/2, all_iv, height, label='全量 IV', color=PRIMARY_LIGHT, edgecolor='white', linewidth=1.5, zorder=3)

ax.set_yticks(y_pos)
ax.set_yticklabels(features, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Information Value (IV)', fontsize=12, fontweight='600')
ax.set_title('白户高IV特征 TOP10：白户 vs 全量对比', fontsize=14, fontweight='700', color=PRIMARY, pad=15)
ax.legend(loc='lower right', frameon=True, facecolor=CARD_BG, edgecolor=BORDER)
ax.xaxis.grid(True, linestyle='--', alpha=0.4, color=BORDER)
ax.set_axisbelow(True)
ax.set_xlim(0, 0.25)

# 添加数值标签
for bar, val in zip(bars1, white_iv):
    ax.annotate(f'{val:.3f}',
                xy=(bar.get_width(), bar.get_y() + bar.get_height()/2),
                xytext=(5, 0), textcoords="offset points",
                ha='left', va='center', fontsize=9, fontweight='600', color=ACCENT)

plt.tight_layout(pad=2)
plt.savefig(f'{output_dir}/white_top_iv_features.png', dpi=150, bbox_inches='tight', facecolor=BG)
plt.close()

print("\n所有配图生成完成！")
print("输出文件:")
print(f"  1. {output_dir}/white_model_comparison.png")
print(f"  2. {output_dir}/white_score_distribution.png")
print(f"  3. {output_dir}/white_scorecard_bins.png")
print(f"  4. {output_dir}/white_threshold_strategy.png")
print(f"  5. {output_dir}/white_top_iv_features.png")
