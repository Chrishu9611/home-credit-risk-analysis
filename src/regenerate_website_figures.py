"""
统一配色风格重生成网站所有配图
网站配色方案：
- 主色:    #1a365d (深蓝)
- 强调:    #f6ad55 (金色)
- 正面/好: #3182ce (品牌蓝)
- 负面/坏: #e53e3e (红色)
- 成功:    #38a169 (绿色)
- 中性/参考:#718096 (灰色)
- 背景:    #ffffff (白色)
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# ============================================
# 统一配色配置
# ============================================
COLORS = {
    'primary': '#1a365d',
    'accent': '#f6ad55',
    'positive': '#3182ce',
    'negative': '#e53e3e',
    'success': '#38a169',
    'neutral': '#718096',
    'light': '#e2e8f0',
    'bg': '#f7fafc',
    'text': '#2d3748',
    'text_light': '#718096',
}

# 统一 matplotlib 样式
plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.edgecolor': COLORS['light'],
    'axes.labelcolor': COLORS['text'],
    'axes.titlecolor': COLORS['primary'],
    'xtick.color': COLORS['text_light'],
    'ytick.color': COLORS['text_light'],
    'grid.color': COLORS['light'],
    'grid.alpha': 0.5,
    'text.color': COLORS['text'],
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.dpi': 150,
})

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 路径
PROJECT_DIR = Path('E:/cursor/PROJECT/home_credit_default_risk/home-credit-risk-analysis')
DATA_DIR = PROJECT_DIR / 'data'
REPORTS_DIR = PROJECT_DIR / 'reports'
MODEL_DIR = DATA_DIR / 'model_outputs'
MODEL_V2_DIR = DATA_DIR / 'model_outputs_v2'
TRAIN_DIR = PROJECT_DIR.parent / 'home_credit_crms_2024/parquet_files/train'
WEBSITE_IMG_DIR = PROJECT_DIR / 'docs/images'
WEBSITE_IMG_DIR.mkdir(parents=True, exist_ok=True)


def setup_axis(ax):
    """统一坐标轴样式"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLORS['light'])
    ax.spines['bottom'].set_color(COLORS['light'])
    ax.tick_params(colors=COLORS['text_light'])


# ============================================
# 图1: 目标变量分布
# ============================================
def fig_target_distribution():
    base = pd.read_parquet(TRAIN_DIR / 'train_base.parquet')
    target_counts = base['target'].value_counts().sort_index()
    target_ratio = base['target'].value_counts(normalize=True).sort_index()

    fig, ax = plt.subplots(1, 2, figsize=(12, 4.5))

    # 左图：柱状图（深蓝+橙色）
    bars = ax[0].bar(['正常 (0)', '违约 (1)'], target_counts.values,
                     color=[COLORS['primary'], COLORS['accent']],
                     width=0.5, edgecolor='white', linewidth=2)
    ax[0].set_title('目标变量分布（绝对数）', fontsize=13, fontweight='bold', color=COLORS['primary'])
    ax[0].set_ylabel('样本数', fontsize=11)
    setup_axis(ax[0])
    ax[0].yaxis.grid(True, linestyle='--', alpha=0.4)
    ax[0].set_axisbelow(True)

    for bar, val in zip(bars, target_counts.values):
        ax[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 15000,
                   f'{val:,}', ha='center', va='bottom', fontsize=11, fontweight='bold',
                   color=COLORS['text'])

    # 右图：饼图（环形图，深蓝+橙色）
    wedges, texts, autotexts = ax[1].pie(
        target_counts.values,
        labels=[f'正常\n{target_counts[0]:,} ({target_ratio[0]*100:.2f}%)',
                f'违约\n{target_counts[1]:,} ({target_ratio[1]*100:.2f}%)'],
        autopct='',
        startangle=90,
        colors=[COLORS['primary'], COLORS['accent']],
        wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3),
        textprops=dict(fontsize=11, color=COLORS['text']),
    )
    ax[1].set_title('目标变量占比', fontsize=13, fontweight='bold', color=COLORS['primary'])

    # 中心文字（橙色）
    ax[1].text(0, 0, f'违约率\n{target_ratio[1]*100:.2f}%',
               ha='center', va='center', fontsize=14, fontweight='bold',
               color=COLORS['accent'])

    plt.suptitle('目标变量分布分析', fontsize=15, fontweight='bold', color=COLORS['primary'],
                 y=1.02)
    plt.tight_layout()
    plt.savefig(WEBSITE_IMG_DIR / '01_target_distribution.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print('[OK] 01_target_distribution.png')
    plt.close()


# ============================================
# 图2: WEEK_NUM 时间结构与违约率波动
# ============================================
def fig_time_analysis():
    base = pd.read_parquet(TRAIN_DIR / 'train_base.parquet')
    base['date_decision'] = pd.to_datetime(base['date_decision'])

    fig, ax = plt.subplots(1, 2, figsize=(14, 5))

    # 左图：WEEK_NUM 样本分布
    week_counts = base['WEEK_NUM'].value_counts().sort_index()
    ax[0].fill_between(week_counts.index, week_counts.values, alpha=0.15, color=COLORS['primary'])
    ax[0].bar(week_counts.index, week_counts.values, color=COLORS['primary'],
              alpha=0.8, width=0.8, edgecolor='white', linewidth=0.3)
    ax[0].set_title('WEEK_NUM 样本分布', fontsize=13, fontweight='bold', color=COLORS['primary'])
    ax[0].set_xlabel('WEEK_NUM', fontsize=11)
    ax[0].set_ylabel('样本数', fontsize=11)
    setup_axis(ax[0])
    ax[0].yaxis.grid(True, linestyle='--', alpha=0.4)
    ax[0].set_axisbelow(True)

    # 右图：WEEK_NUM 违约率趋势（橙色）
    week_default = base.groupby('WEEK_NUM')['target'].agg(['mean', 'count']).reset_index()
    ax[1].fill_between(week_default['WEEK_NUM'], week_default['mean'] * 100,
                       alpha=0.12, color=COLORS['accent'])
    ax[1].plot(week_default['WEEK_NUM'], week_default['mean'] * 100,
               color=COLORS['accent'], marker='o', markersize=3.5,
               linewidth=1.8, label='周违约率')
    ax[1].axhline(y=base['target'].mean() * 100, color=COLORS['neutral'],
                  linestyle='--', linewidth=1.5, alpha=0.8,
                  label=f'整体违约率 {base["target"].mean()*100:.2f}%')
    ax[1].set_title('WEEK_NUM 违约率趋势', fontsize=13, fontweight='bold', color=COLORS['primary'])
    ax[1].set_xlabel('WEEK_NUM', fontsize=11)
    ax[1].set_ylabel('违约率 (%)', fontsize=11)
    ax[1].legend(fontsize=10, loc='upper right', frameon=True, fancybox=True,
                 edgecolor=COLORS['light'])
    setup_axis(ax[1])
    ax[1].yaxis.grid(True, linestyle='--', alpha=0.4)
    ax[1].set_axisbelow(True)

    plt.suptitle('时间结构分析', fontsize=15, fontweight='bold', color=COLORS['primary'],
                 y=1.02)
    plt.tight_layout()
    plt.savefig(WEBSITE_IMG_DIR / '01_time_analysis.png', dpi=150, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print('[OK] 01_time_analysis.png')
    plt.close()


# ============================================
# 图3: XGBoost TOP10 重要性
# ============================================
def fig_xgb_importance():
    imp = pd.read_csv(MODEL_V2_DIR / 'xgboost_importance_all_with_cn.csv')
    imp_top10 = imp.head(10).copy()
    imp_top10['feature_cn'] = imp_top10['feature_cn'].replace({
        'lastrejectreason_759M_目标编码': '上次被拒原因_目标编码',
        'lastcancelreason_561M_目标编码': '上次取消原因_目标编码',
    })

    fig, ax = plt.subplots(figsize=(10, 6))

    # 使用统一配色渐变
    colors = [COLORS['primary'] if i < 3 else COLORS['positive'] if i < 7 else COLORS['neutral']
              for i in range(len(imp_top10))]

    bars = ax.barh(range(len(imp_top10)), imp_top10['importance'],
                   color=colors, edgecolor='white', linewidth=1.5, height=0.65)
    ax.set_yticks(range(len(imp_top10)))
    ax.set_yticklabels(imp_top10['feature_cn'], fontsize=11)
    ax.invert_yaxis()
    ax.set_xlabel('重要性（Gain）', fontsize=12)
    setup_axis(ax)
    ax.xaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, imp_top10['importance']):
        ax.text(bar.get_width() + 3, bar.get_y() + bar.get_height()/2,
                f'{val:.1f}', va='center', fontsize=9, color=COLORS['text_light'])

    # 图例
    legend_elements = [
        mpatches.Patch(facecolor=COLORS['primary'], label='TOP 1-3'),
        mpatches.Patch(facecolor=COLORS['positive'], label='TOP 4-7'),
        mpatches.Patch(facecolor=COLORS['neutral'], label='TOP 8-10'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=9,
              frameon=True, fancybox=True, edgecolor=COLORS['light'])

    plt.title('XGBoost 变量重要性 TOP10', fontsize=15, fontweight='bold',
              color=COLORS['primary'], pad=15)
    plt.tight_layout()
    plt.savefig(WEBSITE_IMG_DIR / '01_xgboost_importance_top10_cn.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print('[OK] 01_xgboost_importance_top10_cn.png')
    plt.close()


# ============================================
# 图4: XGBoost 评分区间分析
# ============================================
def prob_to_score(prob, base_score=600, pdo=20, odds_base=1/19):
    prob = np.clip(prob, 1e-6, 1 - 1e-6)
    odds = prob / (1 - prob)
    factor = pdo / np.log(2)
    offset = base_score - factor * np.log(odds_base)
    return offset - factor * np.log(odds)


def fig_xgb_score_bins():
    df = pd.read_parquet(DATA_DIR / 'train_final_features.parquet')
    iv_df = pd.read_csv(DATA_DIR / 'iv_all_features.csv')
    psi_df = pd.read_csv(DATA_DIR / 'psi_all_features.csv')
    merged = iv_df.merge(psi_df[['feature', 'max_psi']], on='feature', how='inner')
    selected = merged[(merged['iv'] > 0.02) & (merged['max_psi'] <= 0.25)]
    selected_features = selected['feature'].tolist()

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
    X_test = test_df[numeric_features]
    y_test = test_df['target']

    import xgboost as xgb
    model = xgb.Booster()
    model.load_model(str(MODEL_DIR / 'xgb_model.json'))
    prob = model.predict(xgb.DMatrix(X_test, missing=np.nan))
    score = prob_to_score(prob)

    df_score = pd.DataFrame({'score': score, 'target': y_test.values})
    df_score['score_bin'] = pd.cut(df_score['score'], bins=10)

    summary = []
    for interval, group in df_score.groupby('score_bin', observed=False):
        if len(group) == 0:
            continue
        summary.append({
            'interval': f"{interval.left:.0f}-{interval.right:.0f}",
            'count': len(group),
            'bad_rate': group['target'].mean(),
            'pct': len(group) / len(df_score),
        })

    bins_df = pd.DataFrame(summary).sort_values('interval').reset_index(drop=True)

    fig, ax1 = plt.subplots(figsize=(12, 6))
    x_pos = np.arange(len(bins_df))

    # 柱状图：客户数占比（深蓝）
    bars = ax1.bar(x_pos, bins_df['pct'] * 100,
                   color=COLORS['primary'], alpha=0.75,
                   edgecolor='white', linewidth=1.5, width=0.65,
                   label='客户数占比')
    ax1.set_xlabel('评分区间', fontsize=12)
    ax1.set_ylabel('客户数占比 (%)', fontsize=12, color=COLORS['primary'])
    ax1.tick_params(axis='y', labelcolor=COLORS['primary'])
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(bins_df['interval'], rotation=45, ha='right')
    setup_axis(ax1)
    ax1.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax1.set_axisbelow(True)

    # 折线图：坏客率（橙色）
    ax2 = ax1.twinx()
    ax2.plot(x_pos, bins_df['bad_rate'] * 100, color=COLORS['accent'],
             marker='o', linewidth=2.5, markersize=7, label='坏客户占比',
             markerfacecolor='white', markeredgewidth=2)
    ax2.set_ylabel('坏客户占比 (%)', fontsize=12, color=COLORS['accent'])
    ax2.tick_params(axis='y', labelcolor=COLORS['accent'])
    ax2.spines['top'].set_visible(False)

    # 数值标注
    for bar, pct in zip(bars, bins_df['pct']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{pct*100:.1f}%', ha='center', va='bottom', fontsize=8,
                color=COLORS['primary'], fontweight='bold')
    for x, br in zip(x_pos, bins_df['bad_rate']):
        ax2.text(x, br*100 + 0.2, f'{br*100:.2f}%', ha='center', va='bottom',
                fontsize=8, color=COLORS['accent'], fontweight='bold')

    # 合并图例
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10,
               frameon=True, fancybox=True, edgecolor=COLORS['light'])

    plt.title('XGBoost 评分区间：客户分布与坏客户占比', fontsize=15, fontweight='bold',
              color=COLORS['primary'], pad=15)
    plt.tight_layout()
    plt.savefig(WEBSITE_IMG_DIR / '01_xgboost_score_bins_analysis.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print('[OK] 01_xgboost_score_bins_analysis.png')
    plt.close()


# ============================================
# 图5: XGBoost 好坏客户评分分布
# ============================================
def fig_xgb_score_distribution():
    df = pd.read_parquet(DATA_DIR / 'train_final_features.parquet')
    iv_df = pd.read_csv(DATA_DIR / 'iv_all_features.csv')
    psi_df = pd.read_csv(DATA_DIR / 'psi_all_features.csv')
    merged = iv_df.merge(psi_df[['feature', 'max_psi']], on='feature', how='inner')
    selected = merged[(merged['iv'] > 0.02) & (merged['max_psi'] <= 0.25)]
    selected_features = selected['feature'].tolist()

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
    X_test = test_df[numeric_features]
    y_test = test_df['target']

    import xgboost as xgb
    model = xgb.Booster()
    model.load_model(str(MODEL_DIR / 'xgb_model.json'))
    prob = model.predict(xgb.DMatrix(X_test, missing=np.nan))
    score = prob_to_score(prob)

    good_scores = score[y_test.values == 0]
    bad_scores = score[y_test.values == 1]

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.hist(good_scores, bins=60, alpha=0.65, label='好客户',
            color=COLORS['primary'], density=True, edgecolor='white', linewidth=0.3)
    ax.hist(bad_scores, bins=60, alpha=0.55, label='坏客户',
            color=COLORS['accent'], density=True, edgecolor='white', linewidth=0.3)

    ax.axvline(np.median(good_scores), color=COLORS['primary'], linestyle='--',
               linewidth=2, label=f'好客户中位数 {np.median(good_scores):.0f}')
    ax.axvline(np.median(bad_scores), color=COLORS['accent'], linestyle='--',
               linewidth=2, label=f'坏客户中位数 {np.median(bad_scores):.0f}')

    ax.set_xlabel('信用评分', fontsize=12)
    ax.set_ylabel('密度', fontsize=12)
    setup_axis(ax)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(fontsize=10, loc='upper left', frameon=True, fancybox=True,
              edgecolor=COLORS['light'])

    plt.title('XGBoost 好坏客户评分分布', fontsize=15, fontweight='bold',
              color=COLORS['primary'], pad=15)
    plt.tight_layout()
    plt.savefig(WEBSITE_IMG_DIR / '01_xgboost_score_distribution.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print('[OK] 01_xgboost_score_distribution.png')
    plt.close()


# ============================================
# 图6: 通过率 vs 风险降幅权衡曲线
# ============================================
def fig_threshold_risk_reduction():
    xgb_df = pd.read_csv(REPORTS_DIR / 'threshold_xgb_analysis.csv')
    overall_bad_rate = xgb_df['bad_rate_admit'].iloc[0]

    fig, ax = plt.subplots(figsize=(11, 6))

    xgb_reduction = (overall_bad_rate - xgb_df['bad_rate_admit']) / overall_bad_rate * 100

    ax.plot(xgb_df['pass_rate'] * 100, xgb_reduction,
            color=COLORS['primary'], linewidth=2.8, label='XGBoost')
    ax.fill_between(xgb_df['pass_rate'] * 100, xgb_reduction, alpha=0.08,
                    color=COLORS['primary'])

    # 标注关键阈值点
    key_thresholds = [720, 740, 760, 780, 800, 820]
    for t in key_thresholds:
        subset = xgb_df[xgb_df['threshold'] == t]
        if len(subset) > 0:
            pt = subset.iloc[0]
            reduction = (overall_bad_rate - pt['bad_rate_admit']) / overall_bad_rate * 100
            ax.scatter(pt['pass_rate']*100, reduction, color=COLORS['accent'],
                       s=120, zorder=5, edgecolors='white', linewidth=2)
            ax.annotate(f'{t}分\n(降{reduction:.0f}%)',
                       (pt['pass_rate']*100 + 1.5, reduction - 1.5),
                       fontsize=9, color=COLORS['primary'], ha='left',
                       fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                edgecolor=COLORS['light'], alpha=0.9))

    # 参考线
    ax.axhline(y=50, color=COLORS['success'], linestyle='--', linewidth=1.2,
               alpha=0.6, label='风险降50%')
    ax.axhline(y=70, color=COLORS['accent'], linestyle='--', linewidth=1.2,
               alpha=0.6, label='风险降70%')

    ax.set_xlabel('客户通过率 (%)', fontsize=12)
    ax.set_ylabel('风险降幅 (%)', fontsize=12)
    ax.legend(fontsize=10, loc='lower left', frameon=True, fancybox=True,
              edgecolor=COLORS['light'])
    setup_axis(ax)
    ax.yaxis.grid(True, linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)

    plt.title(f'通过率 vs 风险降幅权衡曲线（XGBoost）\n整体违约率 {overall_bad_rate*100:.2f}% 作为基准',
              fontsize=14, fontweight='bold', color=COLORS['primary'], pad=15)
    plt.tight_layout()
    plt.savefig(WEBSITE_IMG_DIR / 'threshold_risk_reduction.png', dpi=150,
                bbox_inches='tight', facecolor='white', edgecolor='none')
    print('[OK] threshold_risk_reduction.png')
    plt.close()


# ============================================
# 主入口
# ============================================
if __name__ == '__main__':
    print('=' * 60)
    print('统一配色风格重生成网站配图')
    print('=' * 60)
    print(f'输出目录: {WEBSITE_IMG_DIR}')
    print(f'配色方案: 主色={COLORS["primary"]} 强调={COLORS["accent"]}')
    print('-' * 60)

    fig_target_distribution()
    fig_time_analysis()
    fig_xgb_importance()
    fig_xgb_score_bins()
    fig_xgb_score_distribution()
    fig_threshold_risk_reduction()

    print('-' * 60)
    print('全部完成！图片已保存到 docs/images/')
    print('=' * 60)
