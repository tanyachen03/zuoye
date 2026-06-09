#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最简单的方法：直接读取各个JS文件，转义换行符后写入
"""

import re

def process_js_file(file_path):
    """读取JS文件并正确处理换行符"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 确保代码中的换行符被正确转义（在字符串内部的）
    # 这里的问题是：当我们有一个字符串 "code: \"abc\\ndef\""，在JS中需要正确表示
    
    return content

def main():
    print("使用最简单的方法生成...")
    
    # 读取模板
    with open('/workspace/template_new.html', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 读取各个数据文件
    courses = process_js_file('/workspace/js/data/courses.js')
    projects = process_js_file('/workspace/js/data/projects.js')
    datasets = process_js_file('/workspace/js/data/datasets.js')
    achievements = process_js_file('/workspace/js/data/achievements.js')
    
    # 构建完整的script部分
    data_script = f"""{courses}
{projects}
{datasets}
{achievements}"""
    
    # 找到script标签内的部分并替换
    # 简单的方法：用我们的数据替换占位符
    result = template
    result = result.replace('<!--COURSES_DATA_PLACEHOLDER-->', courses)
    result = result.replace('<!--PROJECTS_DATA_PLACEHOLDER-->', projects)
    result = result.replace('<!--DATASETS_PLACEHOLDER-->', datasets)
    result = result.replace('<!--ACHIEVEMENTS_DATA_PLACEHOLDER-->', achievements)
    
    # 写入文件
    with open('/workspace/index.html', 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"完成！index.html已生成，共 {len(result):,} 字符")
    
    # 验证
    print("\n验证:")
    check_strings = ['const COURSES_DATA', 'const PROJECTS_DATA', 'const DATASETS', 'const ACHIEVEMENTS_DATA']
    for s in check_strings:
        if s in result:
            print(f"  ✓ {s}")
        else:
            print(f"  ✗ {s} 缺失")

if __name__ == '__main__':
    main()
