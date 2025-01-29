#!/bin/bash

# 定义变量
PYTHON_PATH="../.venv/bin/python3"
SCRIPT_PATH="../src/评估openai模型.py"
INPUT_PATH="../dataset/data.jsonl"
OUTPUT_PATH="../results"

# 确保输出目录存在
mkdir -p $(dirname "$OUTPUT_PATH")

# 运行评估
echo "开始评估..."
$PYTHON_PATH "$SCRIPT_PATH" \
    --input_path "$INPUT_PATH" \
    --output_path "$OUTPUT_PATH/gpt-4o_evaluation_results.json" \
    --model "gpt-4o"

echo "评估完成！结果已保存到 $OUTPUT_PATH"