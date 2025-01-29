# 数学问题求解能力评估工具

这个项目提供了一个自动化工具，用于评估大语言模型（如 GPT-3.5、GPT-4）解决基础数学问题的能力。

## 项目结构

```
.
├── src/
│   ├── generate_data.py    # 数据集生成脚本
│   └── evaluate.py         # 模型评估脚本
├── scripts/
│   ├── generate_all.sh     # 生成数据集的执行脚本
│   └── evaluate.sh         # 运行评估的执行脚本
├── dataset/                # 存放生成的数据集
├── results/                # 存放评估结果
├── .env                    # 环境变量配置文件
└── README.md              
```

## 功能特性

### 支持的数学问题类型

1. **两位数加法 (2D+)** - 从 [0,100) 范围内随机选择两个整数相加
2. **两位数减法 (2D-)** - 从 [0,100) 范围内随机选择两个整数相减
3. **三位数加法 (3D+)** - 从 [0,1000) 范围内随机选择两个整数相加
4. **三位数减法 (3D-)** - 从 [0,1000) 范围内随机选择两个整数相减
5. **四位数加法 (4D+)** - 从 [0,10000) 范围内随机选择两个整数相加
6. **四位数减法 (4D-)** - 从 [0,10000) 范围内随机选择两个整数相减
7. **五位数加法 (5D+)** - 从 [0,100000) 范围内随机选择两个整数相加
8. **五位数减法 (5D-)** - 从 [0,100000) 范围内随机选择两个整数相减
9. **两位数乘法 (2Dx)** - 从 [0,100) 范围内随机选择两个整数相乘
10. **一位数综合运算 (1DC)** - 三个一位数的综合运算，包括加减乘

## 安装和配置

### 环境要求

- Python 3.8+
- OpenAI API 密钥

### 安装依赖

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# 安装依赖包
pip install -r requirements.txt
```

### 配置环境变量

创建 `.env` 文件并配置以下变量：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_API_BASE=https://api.openai.com/v1
USE_PROXY=false  # 是否使用代理（可选）
```

## 使用说明

### 生成数据集

```bash
# 运行数据生成脚本
./scripts/generate_all.sh
```

这将在 `dataset` 目录下生成包含所有类型数学问题的数据集。

### 运行评估

```bash
# 运行评估脚本
./scripts/evaluate.sh
```

评估结果将保存在 `results` 目录下，包括：
- 每个问题的具体评估结果
- 按问题类型统计的正确率
- 详细的错误分析（如果有）

## 评估结果示例

```json
{
  "statistics": {
    "2D+": {
      "correct": 95,
      "total": 100,
      "accuracy": "95.00%"
    },
    // ... 其他类型的统计信息
  },
  "results": [
    {
      "problem": "48 加 76 是多少？",
      "correct_answer": "124",
      "model_answer": "124",
      "is_correct": true,
      "problem_type": "2D+"
    },
    // ... 更多详细结果
  ]
}
```

## 自定义和扩展

### 添加新的问题类型

1. 在 `generate_data.py` 中添加新的问题生成函数
2. 更新 `ProblemType` 枚举类
3. 在生成脚本中添加新类型的处理逻辑

### 修改评估参数

可以通过命令行参数调整评估行为：
- `--model`: 选择使用的模型（默认：gpt-3.5-turbo）
- `--input_path`: 指定输入数据集路径
- `--output_path`: 指定结果保存路径

## 注意事项

1. 请确保 `.env` 文件中的 API 密钥安全性
2. 评估过程可能需要较长时间，取决于数据集大小和 API 响应速度
3. 建议定期备份评估结果
4. API 调用可能产生费用，请注意控制数据集大小

## 贡献指南

欢迎提交 Issues 和 Pull Requests 来改进这个项目。

## 许可证

[MIT License](LICENSE)

## 联系方式

如有问题或建议，请通过 Issues 联系我们。