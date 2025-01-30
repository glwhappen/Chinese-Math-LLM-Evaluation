import argparse
import json
import os
import random
from typing import List, Dict, Callable
from enum import Enum
import re

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
    CHINESE_CHARACTER_COUNT = "CCC"

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

    @staticmethod
    def generate_random_chinese_text(length: int) -> str:
        # 定义一个包含常用汉字的字符串
        common_chars = "的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞"
        
        return ''.join(random.choice(common_chars) for _ in range(length))
    @staticmethod
    def generate_chinese_character_count(text: str) -> Dict:
        char_count = len(re.findall(r'[\u4e00-\u9fff]', text))
        return {
            "problem": f"下面这段话中有多少中文汉字呢：{text}",
            "answer": str(char_count),
            "text": text,
            "operation": "character_count"
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
        ProblemType.ONE_DIGIT_COMPOSITE: (0, 10),
        ProblemType.CHINESE_CHARACTER_COUNT: (10, 30)  # 生成10到30个字符的文本
    }

    range_start, range_end = ranges[problem_type]
    
    for _ in range(num_problems):
        if problem_type == ProblemType.CHINESE_CHARACTER_COUNT:
            text_length = random.randint(*ranges[problem_type])
            text = MathProblemGenerator.generate_random_chinese_text(text_length)
            problem_data = MathProblemGenerator.generate_chinese_character_count(text)
        elif problem_type == ProblemType.ONE_DIGIT_COMPOSITE:
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