#!/usr/bin/env python3
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('const COURSES_DATA=')
end = content.find(';', start + 20)
json_str = content[start + 19:end]

# 显示错误位置周围的内容
error_pos = 20534
context_start = max(0, error_pos - 200)
context_end = min(len(json_str), error_pos + 200)

print('错误位置周围的内容:')
print('=' * 80)
print(repr(json_str[context_start:context_end]))
print('=' * 80)

# 检查引号
print(f'\n总长度: {len(json_str)} 字符')
print(f'双引号数量: {json_str.count(chr(34))}')

# 检查是否有实际的换行符
if '\n' in json_str:
    print('\n警告: 发现实际的换行符，而不是\\n转义')
    lines = json_str.split('\n')
    print(f'总行数: {len(lines)}')
    # 显示包含换行的行
    for i, line in enumerate(lines):
        if len(line) > 100:
            print(f'行 {i+1} (长度 {len(line)}): {line[:50]}...')
