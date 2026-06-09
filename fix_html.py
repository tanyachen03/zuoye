#!/usr/bin/env python3
import json
import re

# 读取JSON数据
with open('courses_data.json', 'r', encoding='utf-8') as f:
    courses_data = json.load(f)

# 将JSON转换为紧凑的JavaScript字符串
courses_json = json.dumps(courses_data, ensure_ascii=False)

print(f"课程数据长度: {len(courses_json)} 字符")

# 读取HTML文件
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print(f"原始文件长度: {len(content)} 字符")

# 替换COURSES_DATA
# 使用正则表达式找到COURSES_DATA部分并替换
pattern = r'const COURSES_DATA=.*?;'
replacement = f'const COURSES_DATA={courses_json};'
new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

print(f"修改后文件长度: {len(new_content)} 字符")

# 验证JSON是否正确
try:
    test_match = re.search(r'const COURSES_DATA=(.*?);', new_content, re.DOTALL)
    if test_match:
        json.loads(test_match.group(1))
        print("✓ 新COURSES_DATA JSON验证通过")
except json.JSONDecodeError as e:
    print(f"✗ JSON验证失败: {e}")
    exit(1)

# 保存修改后的HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✓ 已更新 index.html")
print(f"✓ 课程数量: {len(courses_data)}")
print(f"✓ 总课时: {sum(len(c['lessons']) for c in courses_data)}")
