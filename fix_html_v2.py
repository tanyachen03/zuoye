#!/usr/bin/env python3
import json

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

# 找到COURSES_DATA的开始位置
start_marker = 'const COURSES_DATA='
start_pos = content.find(start_marker)

if start_pos == -1:
    print("✗ 未找到 COURSES_DATA")
    exit(1)

# 从开始位置继续找到第一个分号（在JSON对象结束后的分号）
# 从start_pos开始，找到第一个 }; 的位置
search_start = start_pos + len(start_marker)
end_pos = content.find('};', search_start)

if end_pos == -1:
    print("✗ 未找到 COURSES_DATA 结束位置")
    exit(1)

# end_pos 指向};的开始，所以实际结束位置是end_pos + 1（分号）
end_pos += 1

print(f"COURSES_DATA范围: {start_pos} - {end_pos}")

# 替换内容
new_content = content[:start_pos] + 'const COURSES_DATA=' + courses_json + ';' + content[end_pos+1:]

print(f"修改后文件长度: {len(new_content)} 字符")

# 验证JSON是否正确
try:
    test_courses = new_content[start_pos + len(start_marker):start_pos + len(start_marker) + len(courses_json)]
    json.loads(test_courses)
    print("✓ 新COURSES_DATA JSON验证通过")
except json.JSONDecodeError as e:
    print(f"✗ JSON验证失败: {e}")
    print(f"错误位置: {e.pos}")
    # 显示错误上下文
    start = max(0, e.pos - 50)
    end = min(len(test_courses), e.pos + 50)
    print(f"错误上下文: {test_courses[start:end]}")
    exit(1)

# 保存修改后的HTML
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✓ 已更新 index.html")
print(f"✓ 课程数量: {len(courses_data)}")
print(f"✓ 总课时: {sum(len(c['lessons']) for c in courses_data)}")
