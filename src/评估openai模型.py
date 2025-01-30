import argparse
import json
import os
from typing import List, Dict, Tuple
from openai import OpenAI
from tqdm import tqdm
import re
from collections import defaultdict
from dotenv import load_dotenv

from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# from tenacity import retry, wait_exponential

class MathProblemEvaluator:
    def __init__(self, model: str = "gpt-3.5-turbo", max_workers: int = 5):
        """
        初始化评估器
        
        Args:
            model: 使用的模型名称
        """
        load_dotenv()  # 加载 .env 文件中的环境变量
        # self.client = OpenAI(
        #     base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
        #     api_key=os.getenv("OPENAI_API_KEY"),
        # )
        self.model = model
        self.max_workers = max_workers
        self._thread_local = threading.local()
        
    def get_client(self):
        """为每个线程获取一个独立的 OpenAI client 实例"""
        if not hasattr(self._thread_local, 'client'):
            self._thread_local.client = OpenAI(
                base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1"),
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        return self._thread_local.client
    
    def extract_answer(self, response: str) -> str:
        """
        从模型响应中提取数值答案
        """
        numbers = re.findall(r'-?\d+', response)
        if numbers:
            return numbers[-1]  # 返回最后一个数字
        return response.strip()

    def evaluate_single_problem(self, problem: Dict) -> Dict:
        """
        评估单个问题
        """
        try:
            prompt = (
                "请你扮演一个数学助手，解答下面的数学问题。只需要回答最终的数值结果，不需要解题过程。\n"
                f"问题：{problem['problem']}\n"
                "答案："
            )

            response = self.get_client().chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个精确的数学计算助手。请只回答计算结果，不需要其他解释。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            model_answer = self.extract_answer(response.choices[0].message.content)
            correct_answer = problem['answer']

            is_correct = str(model_answer) == str(correct_answer)
            
            return {
                "problem": problem['problem'],
                "correct_answer": correct_answer,
                "model_answer": model_answer,
                "is_correct": is_correct,
                "problem_type": problem['type']
            }

        except Exception as e:
            print(f"评估问题时发生错误: {str(e)}")
            return {
                "problem": problem['problem'],
                "error": str(e),
                "is_correct": False,
                "problem_type": problem['type']
            }

    def evaluate_dataset(self, problems: List[Dict]) -> Tuple[List[Dict], Dict]:
        """
        使用线程池并行评估整个数据集
        """
        results = []
        type_statistics = defaultdict(lambda: {"correct": 0, "total": 0})
        
        # 创建进度条
        pbar = tqdm(total=len(problems), desc="评估进度")
        
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 提交所有任务
            future_to_problem = {
                executor.submit(self.evaluate_single_problem, problem): problem 
                for problem in problems
            }
            
            # 处理完成的任务
            for future in as_completed(future_to_problem):
                result = future.result()
                results.append(result)
                
                # 更新统计信息
                problem_type = result['problem_type']
                type_statistics[problem_type]["total"] += 1
                if result.get("is_correct", False):
                    type_statistics[problem_type]["correct"] += 1
                
                # 更新进度条
                pbar.update(1)
        
        pbar.close()
        return results, dict(type_statistics)

def format_statistics(statistics: Dict) -> str:
    """
    格式化统计结果
    """
    output = "\n=== 评估结果统计 ===\n"
    for problem_type, stats in statistics.items():
        correct = stats["correct"]
        total = stats["total"]
        accuracy = (correct / total * 100) if total > 0 else 0
        output += f"\n{problem_type}:\n"
        output += f"正确率: {accuracy:.2f}% ({correct}/{total})"
    return output

def main(input_path: str, output_path: str, model: str, max_workers):
    # 读取数据集
    problems = []
    with open(input_path, 'r', encoding='utf-8') as f:
        for line in f:
            problems.append(json.loads(line.strip()))

    # 创建评估器
    evaluator = MathProblemEvaluator(model, max_workers=max_workers)
    
    # 评估数据集
    results, statistics = evaluator.evaluate_dataset(problems)
    
    # 保存结果
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "model": model,
            "results": results,
            "statistics": statistics
        }, f, ensure_ascii=False, indent=2)
    
    # 打印统计信息
    print(format_statistics(statistics))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="评估OpenAI模型的数学问题解答能力")
    parser.add_argument('--input_path', type=str, required=True,
                       help="输入数据集的路径")
    parser.add_argument('--output_path', type=str, required=True,
                       help="评估结果的保存路径")
    parser.add_argument('--model', type=str, default="gpt-3.5-turbo",
                       help="使用的模型名称(默认: gpt-3.5-turbo)")
    parser.add_argument('--max_workers', type=int, default=5,
                       help="线程数量(默认: 5)")
    args = parser.parse_args()
    main(args.input_path, args.output_path, args.model, args.max_workers)