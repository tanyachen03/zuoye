#!/usr/bin/env python3
import re
import os

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

def extract_project_specific(html):
    # 提取项目标题和描述
    project_title = re.search(r'<title>(.*?)</title>', html).group(1)
    
    # 提取 defaultCode
    default_code = ''
    default_match = re.search(r'const defaultCode\s*=\s*`([\s\S]*?)`;', html)
    if default_match:
        default_code = default_match.group(1)
    else:
        # 尝试从 resetCode 函数中提取
        reset_match = re.search(r'editor.value\s*=\s*`([\s\S]*?)`', html)
        if reset_match:
            default_code = reset_match.group(1)
    
    # 提取参考答案
    answer_code = ''
    answer_match = re.search(r'<div class="answer-content">[\s\S]*?<h4>.*?</h4>[\s\S]*?<pre>([\s\S]*?)</pre>', html)
    if answer_match:
        answer_code = answer_match.group(1)
    
    # 提取项目特有函数
    specific_functions = []
    func_names = ['renderDataTable', 'renderVisualization', 'generateExampleData']
    
    for name in func_names:
        func_match = re.search(rf'(const {name}\s*=\s*\[|function {name}\([^)]*\)\s*{{)[\s\S]*?(?=^    (?:const|let|function|document\.addEventListener|\)\.|\})', html, re.MULTILINE)
        if func_match:
            # 调整匹配
            full_func_match = re.search(rf'(const {name}\s*=\s*\[|function {name}\([^)]*\)\s*{{)[\s\S]*?(?=\n    (?:const|let|function|document\.addEventListener|initEditor|toggleAnswer|resetCode|toggleFullscreen|toggleSplitView|initResize|runProjectCode))', html, re.MULTILINE)
            if full_func_match:
                specific_functions.append(full_func_match.group(0))
    
    # 提取项目特有的 sidebar 和 content
    header_content = re.search(r'<div class="project-header">[\s\S]*?</div>\s*</div>', html).group(0)
    sidebar_content = re.search(r'<div class="project-sidebar">[\s\S]*?</div>\s*</div>', html).group(0)
    
    main_content = re.search(r'<div class="project-main">([\s\S]*?)<div class="code-playground"', html).group(1)
    
    # 提取 DOMContentLoaded 中需要保留的部分
    init_extra = ''
    dom_match = re.search(r'document.addEventListener\([^)]+\)\s*=>\s*\{([\s\S]*?)\s*initEditor', html)
    if dom_match:
        init_part = dom_match.group(1)
        # 提取 render 等调用
        render_calls = re.findall(r'\s+\w+\(\);', init_part)
        if render_calls:
            init_extra = '\n'.join(render_calls)
    
    return {
        'title': project_title,
        'header': header_content,
        'sidebar': sidebar_content,
        'main_before': main_content,
        'default_code': default_code,
        'answer_code': answer_code,
        'specific_functions': specific_functions,
        'init_extra': init_extra
    }

def main():
    # 读取 project1.html 作为模板
    template = read_file('/workspace/data-analytics-platform/projects/project1.html')
    
    # 处理 project3-10
    for i in range(3, 11):
        filepath = f'/workspace/data-analytics-platform/projects/project{i}.html'
        if not os.path.exists(filepath):
            continue
            
        project_html = read_file(filepath)
        specific = extract_project_specific(project_html)
        
        # 替换模板内容
        new_html = template
        
        # 替换标题
        new_html = re.sub(r'<title>.*?</title>', f'<title>{specific["title"]}</title>', new_html)
        
        # 替换 header
        new_html = re.sub(r'<div class="project-header">[\s\S]*?</div>\s*</div>', specific['header'], new_html, 1)
        
        # 替换 sidebar
        new_html = re.sub(r'<div class="project-sidebar">[\s\S]*?</div>\s*</div>', specific['sidebar'], new_html, 1)
        
        # 替换 main_before
        new_html = re.sub(r'(<div class="project-main">)[\s\S]*?(<div class="code-playground")',
                         r'\1' + specific['main_before'] + r'\2', new_html, 1)
        
        # 替换 defaultCode
        new_html = re.sub(r'(const defaultCode\s*=\s*`)[\s\S]*?(?=`;)', 
                         r'\1' + specific['default_code'].replace('\\', '\\\\'), new_html, 1)
        
        # 替换 answerCode 在 answer-section
        answer_start = new_html.find('<div class="answer-content">')
        if answer_start != -1:
            pre_start = new_html.find('<pre>', answer_start)
            pre_end = new_html.find('</pre>', pre_start)
            new_html = new_html[:pre_start + 5] + specific['answer_code'] + new_html[pre_end:]
        
        # 处理特有函数
        if specific['specific_functions']:
            # 在 script 开头添加特有函数
            script_start = new_html.find('<script src="../script.js"></script>\n    <script>')
            if script_start != -1:
                insert_pos = script_start + len('<script src="../script.js"></script>\n    <script>\n')
                new_html = new_html[:insert_pos] + '\n        '.join(specific['specific_functions']) + '\n        ' + new_html[insert_pos:]
        
        # 在 DOMContentLoaded 中添加额外初始化
        if specific['init_extra']:
            new_html = re.sub(r'(document.addEventListener\([^)]+\)\s*=>\s*\{)\s*(initEditor)',
                             r'\1' + specific['init_extra'] + r'\n            \2', new_html, 1)
        
        write_file(filepath, new_html)
        
if __name__ == '__main__':
    main()
