import argparse
import json
import os
import random
from typing import List, Dict, Callable
from enum import Enum

class ProblemType(Enum):
    TWO_DIGIT_ADDITION = "2D+"
    TWO_DIGIT_SUBTRACTION = "2D-"
    THREE_DIGIT_ADDITION = "3D+"
    THREE_DIGIT_SUBTRACTION = "3D-"
    FOUR_DIGIT_ADDITION = "4D+"
    FOUR_DIGIT_SUBTRACTION = "4D-"
    FIVE_DIGIT_ADDITION = "5D+"
    FIVE_DIGIT_SUBTRACTION = "5D-"
    TWO_DIGIT_MULTIPLICATION = "2Dx"
    ONE_DIGIT_COMPOSITE = "1DC"

class MathProblemGenerator:
    @staticmethod
    def generate_addition(a: int, b: int) -> Dict:
        return {
            "problem": f"{a} 加 {b} 是多少？",
            "answer": str(a + b),
            "operands": [a, b],
            "operation": "addition"
        }

    @staticmethod
    def generate_subtraction(a: int, b: int) -> Dict:
        return {
            "problem": f"{a} 减 {b} 是多少？",
            "answer": str(a - b),
            "operands": [a, b],
            "operation": "subtraction"
        }

    @staticmethod
    def generate_multiplication(a: int, b: int) -> Dict:
        return {
            "problem": f"{a} 乘以 {b} 是多少？",
            "answer": str(a * b),
            "operands": [a, b],
            "operation": "multiplication"
        }

    @staticmethod
    def generate_composite(a: int, b: int, c: int, op1: str, op2: str) -> Dict:
        operations = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y
        }
        
        result = operations[op2](b, c)
        final_result = operations[op1](a, result)
        
        return {
            "problem": f"{a}{op1}({b}{op2}{c}) 是多少？",
            "answer": str(final_result),
            "operands": [a, b, c],
            "operations": [op1, op2]
        }

def generate_problems(problem_type: ProblemType, num_problems: int) -> List[Dict]:
    problems = []
    ranges = {
        ProblemType.TWO_DIGIT_ADDITION: (0, 100),
        ProblemType.TWO_DIGIT_SUBTRACTION: (0, 100),
        ProblemType.THREE_DIGIT_ADDITION: (0, 1000),
        ProblemType.THREE_DIGIT_SUBTRACTION: (0, 1000),
        ProblemType.FOUR_DIGIT_ADDITION: (0, 10000),
        ProblemType.FOUR_DIGIT_SUBTRACTION: (0, 10000),
        ProblemType.FIVE_DIGIT_ADDITION: (0, 100000),
        ProblemType.FIVE_DIGIT_SUBTRACTION: (0, 100000),
        ProblemType.TWO_DIGIT_MULTIPLICATION: (0, 100),
        ProblemType.ONE_DIGIT_COMPOSITE: (0, 10)
    }

    range_start, range_end = ranges[problem_type]
    
    for _ in range(num_problems):
        if problem_type == ProblemType.ONE_DIGIT_COMPOSITE:
            a = random.randint(range_start, range_end-1)
            b = random.randint(range_start, range_end-1)
            c = random.randint(range_start, range_end-1)
            op1 = random.choice(['+', '-', '*'])
            op2 = random.choice(['+', '-', '*'])
            problem_data = MathProblemGenerator.generate_composite(a, b, c, op1, op2)
        else:
            a = random.randint(range_start, range_end-1)
            b = random.randint(range_start, range_end-1)
            
            if "ADDITION" in problem_type.name:
                problem_data = MathProblemGenerator.generate_addition(a, b)
            elif "SUBTRACTION" in problem_type.name:
                problem_data = MathProblemGenerator.generate_subtraction(a, b)
            elif "MULTIPLICATION" in problem_type.name:
                problem_data = MathProblemGenerator.generate_multiplication(a, b)
        
        problem_data["type"] = problem_type.value
        problems.append(problem_data)
    
    return problems

def save_to_json(data: List[Dict], output_path: str, append: bool = False) -> None:
    mode = 'a' if append else 'w'
    try:
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_path, mode, encoding='utf-8') as f:
            for sample in data:
                json.dump(sample, f, ensure_ascii=False)
                f.write('\n')
                
    except Exception as e:
        raise IOError(f"保存文件时出错: {str(e)}")

def main(output_path: str, problem_type: str, num_problems: int, append: bool) -> None:
    try:
        problem_type_enum = ProblemType(problem_type)
        problems = generate_problems(problem_type_enum, num_problems)
        save_to_json(problems, output_path, append)
        print(f"成功生成 {num_problems} 个 {problem_type} 类型的问题" + 
              f"并{'追加' if append else '写入'}到 {output_path}")
    except Exception as e:
        print(f"程序执行出错: {str(e)}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="生成数学问题数据集")
    parser.add_argument('--output_path', type=str, required=True,
                       help="生成的数据集保存路径")
    parser.add_argument('--problem_type', type=str, required=True,
                       choices=[pt.value for pt in ProblemType],
                       help="要生成的问题类型")
    parser.add_argument('--num_problems', type=int, default=10,
                       help="要生成的问题数量(默认: 10)")
    parser.add_argument('--append', action='store_true',
                       help="是否追加到现有文件（默认为覆盖）")
    
    args = parser.parse_args()
    main(args.output_path, args.problem_type, args.num_problems, args.append)