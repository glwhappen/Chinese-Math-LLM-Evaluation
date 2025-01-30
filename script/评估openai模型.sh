#!/bin/bash

# 定义变量
PYTHON_PATH="../.venv/bin/python3"
SCRIPT_PATH="../src/评估openai模型.py"
INPUT_PATH="../dataset/data.jsonl"
OUTPUT_DIR="../results"
MODELS=("gpt-3.5-turbo" "gpt-4" "gpt-4o" "claude-3-5-sonnet-latest" "deepseek-chat")  # 添加你想要评估的模型

# 确保输出目录存在
mkdir -p $(dirname "$OUTPUT_PATH")

# 汇总结果文件
SUMMARY_FILE="$OUTPUT_DIR/summary_results.json"
echo "{" > "$SUMMARY_FILE"

# 运行评估
echo "开始评估..."

for MODEL in "${MODELS[@]}"; do
    echo "评估模型：${MODEL}"
    OUTPUT_PATH="$OUTPUT_DIR/evaluation_results_${MODEL}.json"
    # 检查结果文件是否已存在
    if [ -f "$OUTPUT_PATH" ]; then
        echo "结果文件 $OUTPUT_PATH 已存在，跳过评估。"
    else
        $PYTHON_PATH "$SCRIPT_PATH" \
            --input_path "$INPUT_PATH" \
            --output_path "$OUTPUT_PATH" \
            --model "gpt-4o" \
            --max_workers 50
    fi

    # 将模型的结果写入汇总文件
    echo "\"$MODEL\":" >> "$SUMMARY_FILE"
    # 使用 jq 提取统计信息
    cat "$OUTPUT_PATH" | jq '.statistics' >> "$SUMMARY_FILE"
    echo "," >> "$SUMMARY_FILE"
done

# 移除最后一个逗号并闭合 JSON 对象
sed -i '$ s/},/}/' "$SUMMARY_FILE"

# 删除文件的最后一行
sed -i '$d' "$SUMMARY_FILE"
sed -i '$d' "$SUMMARY_FILE"

echo "}" >> "$SUMMARY_FILE"


echo "评估完成！结果已保存到 $OUTPUT_PATH"