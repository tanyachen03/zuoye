#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的 index.html 文件 - 修复版本
将数据文件正确地转义为JavaScript字符串
"""

import json
import os

def escape_js_string(s):
    """转义字符串以安全地嵌入JavaScript中"""
    if s is None:
        return 'null'
    
    # 使用json.dumps来正确转义字符串
    return json.dumps(s)

def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def parse_js_data(js_content, var_name):
    """从JS文件中解析数据，转换为Python对象"""
    # 这里我们手动解析，避免使用js2py等依赖
    # 关键是找到对象/数组的开始和结束位置
    
    start = js_content.find(f'const {var_name} = ')
    if start == -1:
        start = js_content.find(f'const {var_name} = ')
    
    if start == -1:
        raise ValueError(f'Could not find {var_name} in JS file')
    
    # 跳过声明部分
    start = js_content.find('=', start) + 1
    
    # 找到结束位置（注意：这是简化版本）
    # 对于数组
    if js_content[start:].strip().startswith('['):
        bracket_count = 0
        end = None
        in_string = False
        escape = False
        for i in range(start, len(js_content)):
            char = js_content[i]
            if escape:
                escape = False
                continue
            if char == '\\':
                escape = True
            elif char in ('"', "'"):
                in_string = not in_string
            elif not in_string and char == '[':
                bracket_count += 1
            elif not in_string and char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    end = i + 1
                    break
    # 对于对象
    elif js_content[start:].strip().startswith('{'):
        bracket_count = 0
        end = None
        in_string = False
        escape = False
        for i in range(start, len(js_content)):
            char = js_content[i]
            if escape:
                escape = False
                continue
            if char == '\\':
                escape = True
            elif char in ('"', "'"):
                in_string = not in_string
            elif not in_string and char == '{':
                bracket_count += 1
            elif not in_string and char == '}':
                bracket_count -= 1
                if bracket_count == 0:
                    end = i + 1
                    break
    else:
        raise ValueError(f'Could not determine data type for {var_name}')
    
    if end is None:
        raise ValueError(f'Could not find end of data for {var_name}')
    
    data_str = js_content[start:end].strip()
    
    # 将JS对象语法转换为JSON语法
    # 需要转义字符串中的实际换行符
    data_str = data_str.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')
    
    # 尝试使用json.loads，但需要先转换JS对象为JSON
    # 需要将单引号替换为双引号，但要小心字符串内部的引号
    # 简单方法：使用ast.literal_eval
    try:
        import ast
        data = ast.literal_eval(data_str)
    except:
        # 如果ast失败，尝试修复字符串
        data_str_fixed = data_str
        # 将键名加上双引号
        import re
        data_str_fixed = re.sub(r'([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*:)', r'\1"\2"\3', data_str_fixed)
        data_str_fixed = data_str_fixed.replace("'", '"')
        data = json.loads(data_str_fixed)
    
    return data

def main():
    print("开始生成 index.html (修复版本)...")

    # 读取模板文件
    template_path = '/workspace/template_new.html'
    template = read_file(template_path)
    print(f"✓ 模板文件读取成功 ({len(template)} 字符)")

    # 读取并解析数据文件
    courses_js = read_file('/workspace/js/data/courses.js')
    projects_js = read_file('/workspace/js/data/projects.js')
    datasets_js = read_file('/workspace/js/data/datasets.js')
    achievements_js = read_file('/workspace/js/data/achievements.js')

    try:
        courses_data = parse_js_data(courses_js, 'COURSES_DATA')
        projects_data = parse_js_data(projects_js, 'PROJECTS_DATA')
        datasets_data = parse_js_data(datasets_js, 'DATASETS')
        achievements_data = parse_js_data(achievements_js, 'ACHIEVEMENTS_DATA')
        print("✓ 数据解析成功")
    except Exception as e:
        print(f"✗ 数据解析失败: {e}")
        return

    # 将数据转换为JSON字符串
    courses_json = json.dumps(courses_data, ensure_ascii=False, indent=2)
    projects_json = json.dumps(projects_data, ensure_ascii=False, indent=2)
    datasets_json = json.dumps(datasets_data, ensure_ascii=False, indent=2)
    achievements_json = json.dumps(achievements_data, ensure_ascii=False, indent=2)

    print(f"✓ 数据JSON转换完成:")
    print(f"  - COURSES_DATA: {len(courses_json):,} 字符")
    print(f"  - PROJECTS_DATA: {len(projects_json):,} 字符")
    print(f"  - DATASETS: {len(datasets_json):,} 字符")
    print(f"  - ACHIEVEMENTS_DATA: {len(achievements_json):,} 字符")

    # 构建要插入的JS代码
    data_code = f"""const COURSES_DATA = {courses_json};
const PROJECTS_DATA = {projects_json};
const DATASETS = {datasets_json};
const ACHIEVEMENTS_DATA = {achievements_json};"""

    # 替换占位符
    result = template

    # 找到占位符区域并替换
    start_marker = '<!--COURSES_DATA_PLACEHOLDER-->'
    end_marker = '<!--ACHIEVEMENTS_DATA_PLACEHOLDER-->'

    start_idx = result.find(start_marker)
    end_idx = result.find(end_marker) + len(end_marker)

    if start_idx != -1 and end_idx != -1:
        result = result[:start_idx] + data_code + result[end_idx:]
        print("✓ 数据嵌入成功")
    else:
        print("✗ 无法找到占位符")
        return

    # 写入index.html
    output_path = '/workspace/index.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    print(f"✓ index.html 生成成功 ({len(result):,} 字符)")
    print(f"文件路径: {output_path}")

    # 验证文件
    with open(output_path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"\n文件统计:")
    print(f"  - 总字符数: {len(content):,}")
    print(f"  - 文件大小: {len(content.encode('utf-8')):,} 字节")
    print(f"  - 包含 COURSES_DATA: {'const COURSES_DATA' in content}")
    print(f"  - 包含 PROJECTS_DATA: {'const PROJECTS_DATA' in content}")
    print(f"  - 包含 DATASETS: {'const DATASETS' in content}")
    print(f"  - 包含 ACHIEVEMENTS_DATA: {'const ACHIEVEMENTS_DATA' in content}")

    # 简单语法检查
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as tmp:
        # 只提取数据部分进行检查
        script_start = content.find('<script>')
        if script_start != -1:
            script_end = content.find('</script>', script_start)
            if script_end != -1:
                js_content = content[script_start+8:script_end]
                tmp.write(js_content)
                tmp_path = tmp.name
    
    # 使用Node.js检查语法
    import subprocess
    try:
        result = subprocess.run(['node', '--check', tmp_path], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("\n✓ JavaScript语法检查通过！")
        else:
            print(f"\n✗ JavaScript语法错误:")
            print(result.stderr)
    except Exception as e:
        print(f"\n⚠ 语法检查执行失败: {e}")
    finally:
        try:
            os.unlink(tmp_path)
        except:
            pass

if __name__ == '__main__':
    main()
