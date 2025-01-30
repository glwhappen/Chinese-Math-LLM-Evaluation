#!/bin/bash

# 定义变量
PYTHON_PATH="/usr/bin/python3"  # Python解释器的路径
CURRENT_TIME=$(date +"%Y%m%d_%H%M%S")  # 当前时间戳
NUM_PROBLEMS=100
OUTPUT_PATH="../dataset/data.jsonl"
SCRIPT_PATH="../src/生成数据集.py"

# 运行Python脚本
echo "开始生成数据..."

# 两位数加法 (2D+)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "2D+" --num_problems $NUM_PROBLEMS

# 两位数减法 (2D-)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "2D-" --num_problems $NUM_PROBLEMS --append

# 三位数加法 (3D+)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "3D+" --num_problems $NUM_PROBLEMS --append

# 三位数减法 (3D-)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "3D-" --num_problems $NUM_PROBLEMS --append

# 四位数加法 (4D+)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "4D+" --num_problems $NUM_PROBLEMS --append

# 四位数减法 (4D-)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "4D-" --num_problems $NUM_PROBLEMS --append

# 五位数加法 (5D+)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "5D+" --num_problems $NUM_PROBLEMS --append

# 五位数减法 (5D-)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "5D-" --num_problems $NUM_PROBLEMS --append

# 两位数乘法 (2Dx)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "2Dx" --num_problems $NUM_PROBLEMS --append

# 一位数综合运算 (1DC)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "1DC" --num_problems $NUM_PROBLEMS --append

# 中文汉字数量计算 (CCC)
$PYTHON_PATH "$SCRIPT_PATH" --output_path "$OUTPUT_PATH" --problem_type "CCC" --num_problems $NUM_PROBLEMS --append


echo "数据生成完成！"