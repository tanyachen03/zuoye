#!/usr/bin/env python3
import os
import shutil

def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {filepath}")

def main():
    # 读取 project1.html
    template_content = read_file('/workspace/data-analytics-platform/projects/project1.html')
    
    # 逐个修复 project3-10
    project_numbers = list(range(3, 11))
    
    for i in project_numbers:
        src_file = f'/workspace/data-analytics-platform/projects/project{i}.html'
        if not os.path.exists(src_file):
            continue
            
        src_content = read_file(src_file)
        
        # 开始构建新内容
        new_content = template_content
        
        # 1. 替换标题
        title_start = src_content.find('<title>')
        title_end = src_content.find('</title>')
        new_title = src_content[title_start:title_end + len('</title>')]
        new_content = new_content.replace(
            '<title>项目1：销售数据清洗 - 数析学院</title>',
            new_title
        )
        
        # 2. 替换 header 部分
        header_start = src_content.find('<div class="project-header">')
        header_mid = src_content.find('</div>', src_content.find('</div>', header_start + 1) + 1) + 6
        header_end = src_content.find('</div>', header_mid) + 6
        new_header = src_content[header_start:header_end]
        
        old_header_start = template_content.find('<div class="project-header">')
        old_header_mid = template_content.find('</div>', template_content.find('</div>', old_header_start + 1) + 1) + 6
        old_header_end = template_content.find('</div>', old_header_mid) + 6
        
        new_content = new_content.replace(
            template_content[old_header_start:old_header_end],
            new_header
        )
        
        # 3. 替换 sidebar
        sidebar_start = src_content.find('<div class="project-sidebar">')
        sidebar_end = src_content.find('</div>', src_content.find('</div>', sidebar_start + 1) + 1) + 6
        new_sidebar = src_content[sidebar_start:sidebar_end]
        
        old_sidebar_start = template_content.find('<div class="project-sidebar">')
        old_sidebar_end = template_content.find('</div>', template_content.find('</div>', old_sidebar_start + 1) + 1) + 6
        
        new_content = new_content.replace(
            template_content[old_sidebar_start:old_sidebar_end],
            new_sidebar
        )
        
        # 4. 替换 project-main 中 code-playground 之前的内容
        main_start = src_content.find('<div class="project-main">')
        main_end = src_content.find('<div class="code-playground"')
        new_main = src_content[main_start:main_end]
        
        old_main_start = template_content.find('<div class="project-main">')
        old_main_end = template_content.find('<div class="code-playground"')
        new_content = new_content.replace(
            template_content[old_main_start:old_main_end],
            new_main
        )
        
        # 5. 替换 defaultCode
        def_extract = src_content.find("const defaultCode")
        if def_extract == -1:
            def_extract = src_content.find("editor.value = `")
            if def_extract != -1:
                code_start = src_content.find('`', def_extract) + 1
                code_end = src_content.find('`;', code_start)
                default_code_str = src_content[code_start:code_end]
                
                old_def_start = template_content.find("const defaultCode = `")
                old_def_end = template_content.find('`;', old_def_start + 1)
                
                new_content = new_content.replace(
                    template_content[old_def_start:old_def_end + 2],
                    f"const defaultCode = `{default_code_str}`;"
                )
        else:
            old_def_start = template_content.find("const defaultCode = `")
            old_def_end = template_content.find('`;', old_def_start + 1)
            
            def_start = src_content.find('`', def_extract) + 1
            def_end = src_content.find('`;', def_start)
            new_code = src_content[def_start:def_end]
            new_content = new_content.replace(
                template_content[old_def_start:old_def_end + 2],
                f"const defaultCode = `{new_code}`;"
            )
            
        # 6. 替换参考答案
        answer_start = src_content.find('<div class="answer-content">')
        if answer_start != -1:
            answer_h4 = src_content.find('<h4>', answer_start)
            answer_pre = src_content.find('<pre>', answer_h4)
            answer_end = src_content.find('</pre>', answer_pre) + 6
            answer_div_end = src_content.find('</div>', answer_end) + 6
            new_answer = src_content[answer_start:answer_div_end]
            
            old_ans_start = template_content.find('<div class="answer-content">')
            old_ans_h4 = template_content.find('<h4>', old_ans_start)
            old_ans_pre = template_content.find('<pre>', old_ans_h4)
            old_ans_end = template_content.find('</pre>', old_ans_pre) + 6
            old_ans_div_end = template_content.find('</div>', old_ans_end) + 6
            
            new_content = new_content.replace(
                template_content[old_ans_start:old_ans_div_end],
                new_answer
            )
        
        # 7. 保留项目特有的函数（在 script 中）
        # 检查是否有 renderDataTable 等函数
        script_start = src_content.find('<script src="../script.js"></script>')
        if script_start != -1:
            script_content = src_content[script_start:]
            # 寻找项目特有函数
            func_names = ['renderDataTable', 'renderVisualization', 'generateExampleData', 'rawData']
            extra_funcs = []
            
            for name in func_names:
                if name in script_content:
                    # 尝试提取该函数/变量
                    if name == 'rawData':
                        idx = script_content.find(f'const {name}')
                        if idx != -1:
                            end_idx = script_content.find('];', idx) + 2
                            extra_funcs.append(script_content[idx:end_idx])
                    else:
                        idx = script_content.find(f'function {name}')
                        if idx != -1:
                            brace_count = 0
                            i = script_content.find('{', idx)
                            if i == -1:
                                continue
                            func_start = idx
                            i += 1
                            brace_count = 1
                            while i < len(script_content) and brace_count > 0:
                                if script_content[i] == '{':
                                    brace_count += 1
                                elif script_content[i] == '}':
                                    brace_count -= 1
                                i += 1
                            extra_funcs.append(script_content[func_start:i])
            
            # 添加到模板的 script 开头
            if extra_funcs:
                insert_point = new_content.find('<script src="../script.js"></script>\n    <script>\n        ')
                if insert_point != -1:
                    insert_str = '\n        '.join(extra_funcs)
                    new_content = new_content[:insert_point + len('<script src="../script.js"></script>\n    <script>\n        ')] + insert_str + '\n        ' + new_content[insert_point + len('<script src="../script.js"></script>\n    <script>\n        '):]
            
            # 在 DOMContentLoaded 中添加调用
            dom_idx = new_content.find('document.addEventListener(\'DOMContentLoaded\', () => {')
            if dom_idx != -1:
                init_idx = new_content.find('initEditor();', dom_idx)
                extra_inits = []
                for func in extra_funcs:
                    if 'function' in func:
                        fn_name = func.split('function ')[1].split('(')[0].strip()
                        extra_inits.append(f'{fn_name}();')
                if extra_inits:
                    insert_str = '\n            '.join(extra_inits)
                    new_content = new_content[:init_idx - 12] + '\n            ' + insert_str + '\n            ' + new_content[init_idx:]
        
        write_file(src_file, new_content)
        
if __name__ == '__main__':
    main()
