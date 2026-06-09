#!/usr/bin/env python3
import json

# Course data with properly escaped code examples
COURSES_DATA = [
    {
        "id": "python-basics",
        "title": "Python基础入门",
        "icon": "🐍",
        "description": "从零开始掌握Python编程基础",
        "difficulty": "入门",
        "lessons": [
            {
                "id": "1.1",
                "title": "变量与数据类型",
                "duration": "15分钟",
                "type": "图文",
                "content": {
                    "text": "变量是编程中最基本的概念之一。在Python中，我们使用变量来存储数据值。Python中的基本数据类型包括：整数（int）、浮点数（float）、字符串（str）、布尔值（bool）。",
                    "codeExamples": [
                        {
                            "title": "变量赋值基础",
                            "code": 'name = "小明"\nage = 25\nheight = 1.75\nis_student = True\nprint("姓名:", name)\nprint("年龄:", age)\nprint("类型:", type(age))'
                        },
                        {
                            "title": "类型转换",
                            "code": 'num_str = "42"\nnum_int = int(num_str)\nprint("字符串转整数:", num_int + 10)\nage = 25\nage_str = str(age)\nprint("整数转字符串:", "年龄是 " + age_str)'
                        }
                    ],
                    "tips": ["Python是动态类型语言，变量类型会在赋值时自动确定。", "使用有意义的变量名可以让代码更易读。"],
                    "commonErrors": ["变量名以数字开头会导致SyntaxError。", "字符串引号不匹配会导致SyntaxError。"]
                }
            },
            {
                "id": "1.2",
                "title": "运算符与表达式",
                "duration": "20分钟",
                "type": "图文",
                "content": {
                    "text": "运算符是用于执行各种数学和逻辑操作的符号。算术运算符包括加法(+)、减法(-)、乘法(*)、除法(/)、整除(//)、取余(%)、幂运算(**)。",
                    "codeExamples": [
                        {
                            "title": "算术运算符",
                            "code": 'a, b = 10, 3\nprint("加法:", a + b)\nprint("减法:", a - b)\nprint("乘法:", a * b)\nprint("除法:", a / b)\nprint("整除:", a // b)\nprint("取余:", a % b)\nprint("幂运算:", a ** b)'
                        }
                    ],
                    "tips": ["在Python中，整除 // 会向下取整。", "使用括号可以明确运算顺序。"],
                    "commonErrors": ["== 是比较运算符，= 是赋值运算符。", "除法 / 总是返回浮点数。"]
                }
            }
        ]
    },
    {
        "id": "pandas-intro",
        "title": "Pandas入门",
        "icon": "🐼",
        "description": "数据分析的核心工具Pandas",
        "difficulty": "入门",
        "lessons": [
            {
                "id": "2.1",
                "title": "Pandas简介",
                "duration": "15分钟",
                "type": "图文",
                "content": {
                    "text": "Pandas是Python数据分析的核心库，提供了高性能、易用的数据结构和数据分析工具。核心数据结构包括Series（一维数组）和DataFrame（二维表格）。",
                    "codeExamples": [
                        {
                            "title": "Series创建",
                            "code": 'import pandas as pd\ns = pd.Series([1, 3, 5, 7, 9])\nprint(s)'
                        },
                        {
                            "title": "DataFrame创建",
                            "code": 'import pandas as pd\ndata = {\n    "姓名": ["小明", "小红", "小刚"],\n    "年龄": [20, 19, 21],\n    "数学": [85, 92, 78]\n}\ndf = pd.DataFrame(data)\nprint(df)\nprint(df.shape)'
                        }
                    ],
                    "tips": ["使用pd.前缀调用Pandas函数是标准做法。", "NumPy常与Pandas一起使用。"],
                    "commonErrors": ["忘记导入pandas。", "Series和DataFrame混淆。"]
                }
            }
        ]
    }
]

def generate_course_js(courses):
    """Generate JavaScript for COURSES_DATA"""
    js_lines = ["const COURSES_DATA = "]
    
    def process_item(item):
        if isinstance(item, dict):
            return "{" + ",".join(f'{k}:{process_item(v)}' for k, v in item.items()) + "}"
        elif isinstance(item, list):
            return "[" + ",".join(process_item(i) for i in item) + "]"
        elif isinstance(item, str):
            escaped = item.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            return f'"{escaped}"'
        elif isinstance(item, bool):
            return 'true' if item else 'false'
        elif item is None:
            return 'null'
        else:
            return str(item)
    
    result = process_item(courses)
    return "const COURSES_DATA = " + result + ";"

if __name__ == "__main__":
    print(generate_course_js(COURSES_DATA))
