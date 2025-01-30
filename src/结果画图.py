# pip install matplotlib seaborn pandas

import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# 读取评估结果
with open('./results/summary_results.json', 'r') as f:
    results = json.load(f)

# 准备数据
data = []
for model, model_results in results.items():
    for problem_type, scores in model_results.items():
        accuracy = (scores['correct'] / scores['total']) * 100
        data.append({
            'Model': model,
            'Problem Type': problem_type,
            'Accuracy': accuracy
        })

df = pd.DataFrame(data)

# 设置图表样式
plt.figure(figsize=(15, 10))
sns.set(style="whitegrid")

# 创建热力图
pivot_table = df.pivot(index="Problem Type", columns="Model", values="Accuracy")
heatmap = sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu", vmin=0, vmax=100)

plt.title("Model Performance Across Different Problem Types")
plt.tight_layout()
plt.savefig('model_performance_heatmap.png')
plt.close()

# 创建条形图
plt.figure(figsize=(15, 10))
sns.barplot(x="Problem Type", y="Accuracy", hue="Model", data=df)
plt.title("Model Performance Comparison")
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.tight_layout()
plt.savefig('model_performance_barplot.png')
plt.close()

print("图表已生成：model_performance_heatmap.png 和 model_performance_barplot.png")