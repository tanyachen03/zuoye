#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的 index.html 文件
将数据文件嵌入到HTML中，避免字符串替换导致的数据截断问题
"""

import re
import os

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_js_data(js_content):
    """从JS文件中提取数据（去掉 const DATA = 和结尾的分号）"""
    # 去掉 "const XXX_DATA = " 或 "const DATASETS = "
    content = re.sub(r'^const\s+\w+\s*=\s*', '', js_content.strip())
    # 去掉结尾的分号
    content = content.rstrip(';').rstrip()
    return content

def main():
    print("开始生成 index.html...")

    # 读取模板文件
    template_path = '/workspace/template_new.html'
    template = read_file(template_path)
    print(f"✓ 模板文件读取成功 ({len(template)} 字符)")

    # 读取数据文件
    courses_js = read_file('/workspace/js/data/courses.js')
    projects_js = read_file('/workspace/js/data/projects.js')
    datasets_js = read_file('/workspace/js/data/datasets.js')
    achievements_js = read_file('/workspace/js/data/achievements.js')

    # 提取JS数据
    courses_data = extract_js_data(courses_js)
    projects_data = extract_js_data(projects_js)
    datasets_data = extract_js_data(datasets_js)
    achievements_data = extract_js_data(achievements_js)

    print(f"✓ 数据提取成功:")
    print(f"  - COURSES_DATA: {len(courses_data)} 字符")
    print(f"  - PROJECTS_DATA: {len(projects_data)} 字符")
    print(f"  - DATASETS: {len(datasets_data)} 字符")
    print(f"  - ACHIEVEMENTS_DATA: {len(achievements_data)} 字符")

    # 替换占位符
    result = template

    # 使用正则表达式替换HTML注释占位符
    result = re.sub(
        r'<!--COURSES_DATA_PLACEHOLDER-->',
        f'const COURSES_DATA = {courses_data};',
        result
    )

    result = re.sub(
        r'<!--PROJECTS_DATA_PLACEHOLDER-->',
        f'const PROJECTS_DATA = {projects_data};',
        result
    )

    result = re.sub(
        r'<!--DATASETS_PLACEHOLDER-->',
        f'const DATASETS = {datasets_data};',
        result
    )

    result = re.sub(
        r'<!--ACHIEVEMENTS_DATA_PLACEHOLDER-->',
        f'const ACHIEVEMENTS_DATA = {achievements_data};',
        result
    )

    print(f"✓ 占位符替换完成")

    # 验证数据是否完整嵌入
    if 'const COURSES_DATA' in result:
        # 找到完整的COURSES_DATA
        match = re.search(r'const COURSES_DATA = (\[[\s\S]*?\]);', result)
        if match:
            courses_match = match.group(1)
            print(f"✓ COURSES_DATA 验证成功 ({len(courses_match)} 字符)")

            # 检查是否有多个课程
            course_count = courses_match.count('"id":')
            print(f"  课程数量: {course_count}")
        else:
            print("✗ COURSES_DATA 验证失败 - 无法找到完整数据")
    else:
        print("✗ COURSES_DATA 验证失败 - 未找到声明")

    # 写入index.html
    output_path = '/workspace/index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"✓ index.html 生成成功 ({len(result)} 字符)")
    print(f"文件路径: {output_path}")

    # 额外验证
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查HTML文件大小
    print(f"\n文件统计:")
    print(f"  - 总字符数: {len(content):,}")
    print(f"  - 文件大小: {len(content.encode('utf-8')):,} 字节")

    # 验证COURSES_DATA在文件中
    if 'const COURSES_DATA' in content:
        # 计算COURSES_DATA到第一个分号之间的字符数
        start = content.find('const COURSES_DATA = ')
        if start != -1:
            end = content.find('];', start)
            if end != -1:
                courses_section_len = end - start + 2
                print(f"  - COURSES_DATA 部分: ~{courses_section_len:,} 字符")
    else:
        print("  - COURSES_DATA: 未找到")

if __name__ == '__main__':
    main()
