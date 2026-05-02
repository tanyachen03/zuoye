import re
import os

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def extract_content_from_file(content):
    # Extract title
    title_match = re.search(r'<title>(.*?)</title>', content)
    title = title_match.group(1) if title_match else ''
    
    # Extract header content (project title, difficulty, meta)
    header_match = re.search(r'<div class="project-header">(.*?)</div>\s*</div>', content, re.DOTALL)
    header_content = header_match.group(1) if header_match else ''
    
    # Extract sidebar content
    sidebar_match = re.search(r'<div class="project-sidebar">(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
    sidebar_content = sidebar_match.group(1) if sidebar_match else ''
    
    # Extract main content before playground
    main_before_match = re.search(r'<div class="project-main">(.*?)<div class="code-playground"', content, re.DOTALL)
    main_before = main_before_match.group(1) if main_before_match else ''
    
    # Extract default code from textarea
    default_code_match = re.search(r'<textarea[^>]*id="code-editor"[^>]*>(.*?)</textarea>', content, re.DOTALL)
    if not default_code_match:
        default_code_match = re.search(r'resetCode\(\).*?editor\.value\s*=\s*`(.*?)`', content, re.DOTALL)
    default_code = default_code_match.group(1) if default_code_match else ''
    
    # Extract answer code from answer section
    answer_code_match = re.search(r'<div class="answer-section".*?<pre>(.*?)</pre>', content, re.DOTALL)
    answer_code = answer_code_match.group(1) if answer_code_match else ''
    
    # Extract raw data table content if exists
    raw_data_match = re.search(r'const rawData\s*=\s*(.*?);', content, re.DOTALL)
    raw_data_content = raw_data_match.group(1) if raw_data_match else ''
    
    # Extract renderDataTable function if exists
    render_data_table_match = re.search(r'(function renderDataTable\(\)\s*\{.*?\})', content, re.DOTALL)
    render_data_table = render_data_table_match.group(1) if render_data_table_match else ''
    
    return {
        'title': title,
        'header_content': header_content,
        'sidebar_content': sidebar_content,
        'main_before': main_before,
        'default_code': default_code,
        'answer_code': answer_code,
        'raw_data_content': raw_data_content,
        'render_data_table': render_data_table
    }

def generate_fixed_file(template, content_info):
    # Replace title
    result = re.sub(r'<title>.*?</title>', f'<title>{content_info["title"]}</title>', template)
    
    # Replace project header
    if content_info['header_content']:
        result = re.sub(
            r'<div class="project-header">.*?</div>\s*</div>',
            f'<div class="project-header">{content_info["header_content"]}</div></div>',
            result,
            flags=re.DOTALL
        )
    
    # Replace sidebar
    if content_info['sidebar_content']:
        result = re.sub(
            r'<div class="project-sidebar">.*?</div>\s*</div>\s*</div>',
            f'<div class="project-sidebar">{content_info["sidebar_content"]}</div></div></div>',
            result,
            flags=re.DOTALL
        )
    
    # Replace main content before playground
    if content_info['main_before']:
        result = re.sub(
            r'<div class="project-main">.*?<div class="code-playground"',
            f'<div class="project-main">{content_info["main_before"]}<div class="code-playground"',
            result,
            flags=re.DOTALL
        )
    
    # Replace default code in script
    if content_info['default_code']:
        # Escape backticks
        safe_code = content_info['default_code'].replace('\\', '\\\\').replace('`', '\\`')
        result = re.sub(
            r'const defaultCode\s*=\s*`.*?`;',
            f'const defaultCode = `{safe_code}`;',
            result,
            flags=re.DOTALL
        )
        
        # Also replace in resetCode if needed
        result = re.sub(
            r'resetCode\(\).*?editor\.value\s*=\s*`.*?`',
            f'resetCode() {{ editor.value = `{safe_code}`',
            result,
            flags=re.DOTALL
        )
    
    # Replace answer code
    if content_info['answer_code']:
        safe_answer = content_info['answer_code'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        result = re.sub(
            r'<div class="answer-section".*?<pre>.*?</pre>',
            f'<div class="answer-section" id="answer-section"><div class="answer-content"><h4><i class="fas fa-check-circle"></i> 参考答案代码：</h4><pre>{safe_answer}</pre></div></div>',
            result,
            flags=re.DOTALL
        )
    
    # Add raw data and renderDataTable if they exist in content_info
    if content_info['raw_data_content']:
        # Insert raw data and renderDataTable function into the script
        script_insert = f'''        const rawData = {content_info['raw_data_content']};
        {content_info['render_data_table'] if content_info['render_data_table'] else ''}
        
'''
        result = re.sub(
            r'(\s+<script src="\.\./script\.js">\s*<script>)',
            lambda m: m.group(1) + '\n' + script_insert,
            result
        )
    
    # Add renderDataTable call to DOMContentLoaded if needed
    if content_info['render_data_table']:
        result = re.sub(
            r'(document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{)',
            r'\1 renderDataTable();',
            result
        )
    
    return result

def fix_project_files():
    projects_dir = '/workspace/data-analytics-platform/projects'
    
    # Read template (project1.html)
    template = read_file(os.path.join(projects_dir, 'project1.html'))
    
    # List of project files to fix
    project_files = [
        'project2.html',
        'project3.html', 
        'project4.html',
        'project5.html',
        'project6.html',
        'project7.html',
        'project8.html',
        'project9.html',
        'project10.html'
    ]
    
    for filename in project_files:
        filepath = os.path.join(projects_dir, filename)
        if os.path.exists(filepath):
            print(f'Fixing {filename}...')
            content = read_file(filepath)
            content_info = extract_content_from_file(content)
            fixed_content = generate_fixed_file(template, content_info)
            write_file(filepath, fixed_content)
            print(f'Fixed {filename} successfully!')
        else:
            print(f'Warning: {filename} not found!')

if __name__ == '__main__':
    fix_project_files()
