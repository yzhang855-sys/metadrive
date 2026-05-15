import subprocess
import pandas as pd
import matplotlib.pyplot as plt

# 第一步：获取所有commit的hash和日期
result = subprocess.run(
    ['git', 'log', '--format=%H,%ad', '--date=short'],
    capture_output=True, text=True,
    cwd='/Users/pangjugua/metadrive'
)

commits = []
for line in result.stdout.strip().split('\n'):
    parts = line.split(',')
    if len(parts) == 2:
        commits.append({'hash': parts[0], 'date': parts[1]})

print(f"总commit数: {len(commits)}")

# 第二步：每隔30个commit采样一次（共约27个采样点）
sampled = commits[::30]
print(f"采样数量: {len(sampled)} 个commit")

# 第三步：对每个采样commit，统计当时有多少个Python文件
data = []
for i, c in enumerate(sampled):
    ls_result = subprocess.run(
        f"git ls-tree -r --name-only {c['hash']} | grep '\\.py$' | wc -l",
        shell=True, capture_output=True, text=True,
        cwd='/Users/pangjugua/metadrive'
    )
    py_files = ls_result.stdout.strip()
    data.append({
        'date': c['date'],
        'py_files': int(py_files) if py_files.isdigit() else 0
    })
    print(f"  [{i+1}/{len(sampled)}] {c['date']} - {py_files} 个Python文件")

# 第四步：整理数据并画图
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# 保存原始数据
df.to_csv('/Users/pangjugua/metadrive/evolution_data.csv', index=False)
print("\n数据已保存到 evolution_data.csv")

# 画折线图
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(df['date'], df['py_files'], 
        marker='o', markersize=4, 
        linewidth=1.5, color='steelblue')
ax.set_title('MetaDrive: Number of Python Files Over Time', fontsize=14)
ax.set_xlabel('Date')
ax.set_ylabel('Number of Python Files')
ax.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('/Users/pangjugua/metadrive/evolution_chart.png', dpi=150)
print("图表已保存到 evolution_chart.png")