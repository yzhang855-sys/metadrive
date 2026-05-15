import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ============================================
# 图1：BaseEnv各方法圈复杂度对比图
# ============================================

methods = [
    '_post_process_config',
    'export_scenarios', 
    '_get_step_return',
    'switch_to_third_person_view',
    'reset',
    'reset_sensors',
    '__init__',
    '_preprocess_actions',
]
scores = [27, 15, 11, 10, 8, 8, 7, 6]
grades = ['D', 'C', 'C', 'B', 'B', 'B', 'B', 'B']

# 根据评级设置颜色
colors = []
for g in grades:
    if g == 'D':
        colors.append('#d32f2f')   # 红色
    elif g == 'C':
        colors.append('#f57c00')   # 橙色
    else:
        colors.append('#388e3c')   # 绿色

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(methods, scores, color=colors)
ax.set_xlabel('Cyclomatic Complexity Score')
ax.set_title('BaseEnv Methods: Cyclomatic Complexity', fontsize=13)
ax.axvline(x=10, color='orange', linestyle='--', alpha=0.7, label='Grade C threshold (10)')
ax.axvline(x=15, color='red', linestyle='--', alpha=0.7, label='Grade D threshold (15)')

# 在每个bar右侧标注分数和等级
for bar, score, grade in zip(bars, scores, grades):
    ax.text(score + 0.3, bar.get_y() + bar.get_height()/2,
            f'{score} ({grade})', va='center', fontsize=10)

# 图例
red_patch = mpatches.Patch(color='#d32f2f', label='Grade D - High Risk')
orange_patch = mpatches.Patch(color='#f57c00', label='Grade C - Moderate Risk')
green_patch = mpatches.Patch(color='#388e3c', label='Grade B - Acceptable')
ax.legend(handles=[red_patch, orange_patch, green_patch], loc='lower right')

plt.tight_layout()
plt.savefig('/Users/pangjugua/metadrive/cc_baseenv.png', dpi=150)
print("图1已保存：cc_baseenv.png")

# ============================================
# 图2：代码构成饼图
# ============================================

fig2, ax2 = plt.subplots(figsize=(7, 7))
labels = ['Source Code\n(SLOC)', 'Comments', 'Multi-line\nStrings/Docs', 'Blank Lines']
sizes = [70787, 7322, 8600, 16462]
colors2 = ['#1976d2', '#43a047', '#fb8c00', '#9e9e9e']
explode = (0.05, 0, 0, 0)

wedges, texts, autotexts = ax2.pie(
    sizes, labels=labels, colors=colors2,
    explode=explode, autopct='%1.1f%%',
    startangle=140, textprops={'fontsize': 11}
)
ax2.set_title('MetaDrive Codebase Composition\n(Total Lines)', fontsize=13)
plt.tight_layout()
plt.savefig('/Users/pangjugua/metadrive/code_composition.png', dpi=150)
print("图2已保存：code_composition.png")

# ============================================
# 图3：已有重构commits时间线
# ============================================

refactor_events = [
    ('2021-03', 'Refactor config system'),
    ('2021-03', 'Extract BaseEnv class'),
    ('2021-04', 'Refactor Traffic manager'),
    ('2021-08', 'Refactor observation system'),
    ('2022-03', 'Refactor MA envs'),
    ('2022-05', 'Refactor Map class'),
    ('2023-04', 'Refactor managers'),
    ('2023-05', 'Refactor sensor API'),
    ('2023-06', 'Refactor agent manager'),
]

import matplotlib.dates as mdates
from datetime import datetime

dates = [datetime.strptime(e[0], '%Y-%m') for e in refactor_events]
labels_r = [e[1] for e in refactor_events]

fig3, ax3 = plt.subplots(figsize=(12, 4))
ax3.scatter(dates, [1]*len(dates), s=100, color='steelblue', zorder=5)

for i, (date, label) in enumerate(zip(dates, labels_r)):
    offset = 0.03 if i % 2 == 0 else -0.03
    va = 'bottom' if i % 2 == 0 else 'top'
    ax3.annotate(label, (date, 1),
                xytext=(date, 1 + offset),
                fontsize=7.5,
                ha='center', va=va,
                rotation=15)

ax3.set_ylim(0.85, 1.2)
ax3.set_yticks([])
ax3.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax3.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.xticks(rotation=45)
ax3.set_title('MetaDrive Refactoring History Timeline', fontsize=13)
ax3.grid(True, axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('/Users/pangjugua/metadrive/refactor_timeline.png', dpi=150)
print("图3已保存：refactor_timeline.png")

print("\n全部完成！共生成3张图表用于报告。")