#!/usr/bin/env python3
import json

# 读取课程数据
with open('courses_data.json', 'r', encoding='utf-8') as f:
    courses_data = json.load(f)

# 生成JSON
courses_json = json.dumps(courses_data, ensure_ascii=False)

print(f"courses_json 长度: {len(courses_json)}")

# 检查前100个字符
print(f"\n前100个字符:")
print(repr(courses_json[:100]))

# 检查最后100个字符
print(f"\n最后100个字符:")
print(repr(courses_json[-100:]))

# 检查是否包含可能引起问题的字符
print(f"\n检查特殊字符:")
print(f"  双引号数量: {courses_json.count('\"')}")
print(f"  反斜杠数量: {courses_json.count('\\\\')}")
print(f"  换行符数量: {courses_json.count('\\n')}")

# 保存到临时文件
with open('temp_courses_json.txt', 'w', encoding='utf-8') as f:
    f.write(courses_json)

print("\n✓ courses_json已保存到 temp_courses_json.txt")
