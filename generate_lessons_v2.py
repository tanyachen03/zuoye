#!/usr/bin/env python3
import os

def create_lesson_html(lesson_num, module_key, module_name, module_tag, lesson_title, lesson_desc, lesson_id):
    filepath = f"/workspace/data-analytics-platform/course/{module_key}/lesson{lesson_num}.html"
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{lesson_title} - 数析学院</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/monokai.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        :root {{ --primary: #3b82f6; --bg: #f8fafc; --white: #fff; }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: #1e293b; line-height: 1.7; }}
        .navbar {{ position: fixed; top: 0; left: 0; right: 0; background: var(--white); box-shadow: 0 2px 8px rgba(0,0,0,0.08); z-index: 100; }}
        .navbar-container {{ max-width: 1400px; margin: 0 auto; padding: 0 2rem; display: flex; align-items: center; justify-content: space-between; height: 60px; }}
        .navbar-logo {{ display: flex; align-items: center; gap: 0.5rem; font-size: 1.25rem; font-weight: 700; color: var(--primary); text-decoration: none; }}
        .back-link {{ color: #64748b; text-decoration: none; font-size: 0.9rem; }}
        .back-link:hover {{ color: var(--primary); }}
        .lesson-container {{ display: grid; grid-template-columns: 260px 1fr; gap: 2rem; max-width: 1400px; margin: 80px auto 2rem; padding: 0 2rem; }}
        .sidebar {{ position: sticky; top: 80px; height: fit-content; }}
        .sidebar-card {{ background: var(--white); border-radius: 12px; padding: 1.5rem; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .sidebar-title {{ font-size: 0.9rem; font-weight: 600; color: #64748b; margin-bottom: 1rem; }}
        .lesson-nav-item {{ display: flex; align-items: center; padding: 0.75rem; border-radius: 8px; text-decoration: none; color: #1e293b; font-size: 0.9rem; margin-bottom: 0.5rem; transition: all 0.2s; }}
        .lesson-nav-item:hover {{ background: #f1f5f9; }}
        .lesson-nav-item.active {{ background: #eff6ff; color: var(--primary); font-weight: 600; }}
        .nav-number {{ width: 24px; height: 24px; border-radius: 50%; background: #e2e8f0; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; margin-right: 0.75rem; }}
        .nav-title {{ flex: 1; }}
        .main-content {{ background: var(--white); border-radius: 12px; padding: 2rem; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .lesson-header {{ border-bottom: 2px solid #f1f5f9; padding-bottom: 1.5rem; margin-bottom: 2rem; }}
        .lesson-meta {{ display: flex; gap: 1rem; margin-bottom: 0.75rem; }}
        .meta-tag {{ padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.8rem; font-weight: 600; }}
        .meta-tag.module {{ background: #eff6ff; color: var(--primary); }}
        .lesson-header h1 {{ font-size: 1.75rem; font-weight: 700; color: #1e293b; margin-bottom: 0.5rem; }}
        .lesson-header p {{ color: #64748b; font-size: 1rem; }}
        .section {{ margin-bottom: 2rem; }}
        .section h2 {{ font-size: 1.25rem; font-weight: 700; color: #1e293b; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid #e2e8f0; }}
        .section p {{ color: #475569; margin-bottom: 1rem; }}
        .section ul {{ padding-left: 1.5rem; color: #475569; margin-bottom: 1rem; }}
        .section li {{ margin-bottom: 0.5rem; }}
        .tip-box {{ background: #eff6ff; border-left: 4px solid var(--primary); padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
        .tip-box .tip-title {{ font-weight: 600; color: var(--primary); margin-bottom: 0.5rem; }}
        .error-box {{ background: #fef2f2; border-left: 4px solid #ef4444; padding: 1rem; border-radius: 8px; margin: 1rem 0; }}
        .error-box .error-title {{ font-weight: 600; color: #ef4444; margin-bottom: 0.5rem; }}
        .editor-container {{ background: white; border-radius: 12px; overflow: hidden; border: 1px solid #e2e8f0; margin: 1.5rem 0; }}
        .editor-toolbar {{ background: #f8fafc; padding: 12px 16px; border-bottom: 1px solid #e2e8f0; display: flex; gap: 10px; }}
        .editor-toolbar button {{ padding: 8px 16px; border: none; border-radius: 6px; font-size: 14px; font-weight: 500; cursor: pointer; }}
        .btn-run {{ background: #22c55e; color: white; }}
        .btn-reset {{ background: #f1f5f9; color: #475569; }}
        .CodeMirror {{ height: 300px !important; font-size: 14px; }}
        .output-area {{ background: #0f172a; padding: 16px; }}
        .output-area pre {{ margin: 0; color: #e2e8f0; font-family: monospace; font-size: 14px; }}
        .complete-btn {{ display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; background: linear-gradient(135deg, #10b981, #06b6d4); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; }}
        @media (max-width: 1024px) {{ .lesson-container {{ grid-template-columns: 1fr; }} .sidebar {{ position: static; }} }}
    </style>
</head>
<body>
    <header class="navbar">
        <div class="navbar-container">
            <a href="../../course-center.html" class="back-link"><i class="fas fa-arrow-left"></i> 返回课程中心</a>
            <a href="../../index.html" class="navbar-logo"><i class="fas fa-chart-bar"></i> 数析学院</a>
        </div>
    </header>

    <div class="lesson-container">
        <aside class="sidebar">
            <div class="sidebar-card">
                <div class="sidebar-title">{module_name}</div>
                {lesson_nav}
            </div>
        </aside>

        <main class="main-content">
            <div class="lesson-header">
                <div class="lesson-meta">
                    <span class="meta-tag module">{module_tag}</span>
                </div>
                <h1>{lesson_title}</h1>
                <p>{lesson_desc}</p>
            </div>

            <div class="section">
                <h2>学习目标</h2>
                <ul>
                    <li>理解{lesson_title}的核心概念</li>
                    <li>掌握相关的代码实现方法</li>
                    <li>能够在实际项目中应用</li>
                </ul>
            </div>

            <div class="section">
                <h2>知识点讲解</h2>
                <p>{lesson_desc}。本节将详细介绍相关概念和实用技巧。</p>
            </div>

            <div class="tip-box">
                <div class="tip-title">小贴士</div>
                <p>多动手实践，遇到问题多查看官方文档。</p>
            </div>

            <div class="section">
                <h2>代码示例</h2>
                <p>在下方编辑器中尝试运行代码：</p>
            </div>

            <div class="editor-container">
                <div class="editor-toolbar">
                    <button class="btn-run" onclick="runCode()"><i class="fas fa-play"></i> 运行</button>
                    <button class="btn-reset" onclick="resetCode()"><i class="fas fa-undo"></i> 重置</button>
                    <span id="status" style="margin-left:auto;color:#64748b;font-size:14px;">环境加载中...</span>
                </div>
                <div id="code-editor"></div>
                <div class="output-area">
                    <pre id="output"></pre>
                </div>
            </div>

            <div class="error-box">
                <div class="error-title">常见错误</div>
                <p>注意代码缩进，确保Python语法正确。</p>
            </div>

            <div style="margin-top:2rem;padding-top:2rem;border-top:2px solid #f1f5f9;">
                <button class="complete-btn" id="completeBtn" onclick="markComplete()">
                    <i class="fas fa-check-circle"></i>
                    <span id="btnText">标记为已完成</span>
                </button>
            </div>
        </main>
    </div>

    <script>
        let editor;
        let pyodide;

        function initEditor() {{
            editor = CodeMirror(document.getElementById('code-editor'), {{
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                tabSize: 4,
                value: "# " + "{lesson_title}" + "\\nprint('欢迎学习数据分析!')"
            }});
        }}

        async function initPyodide() {{
            try {{
                pyodide = await loadPyodide();
                document.getElementById('status').textContent = '环境就绪';
            }} catch (err) {{
                document.getElementById('status').textContent = '加载失败';
            }}
        }}

        async function runCode() {{
            if (!pyodide) {{
                document.getElementById('output').textContent = '环境加载中...';
                return;
            }}
            const code = editor.getValue();
            document.getElementById('output').textContent = '运行中...';
            try {{
                pyodide.runPython("import sys; from io import StringIO; sys.stdout = StringIO()");
                await pyodide.runPythonAsync(code);
                const output = pyodide.runPython("sys.stdout.getvalue()");
                document.getElementById('output').textContent = output || '（无输出）';
            }} catch (err) {{
                document.getElementById('output').textContent = '错误: ' + err;
            }}
        }}

        function resetCode() {{
            editor.setValue("# " + "{lesson_title}" + "\\nprint('欢迎学习数据分析!')");
            document.getElementById('output').textContent = '';
        }}

        function markComplete() {{
            const completed = JSON.parse(localStorage.getItem('completedLessons') || '{{}}');
            completed['{lesson_id}'] = true;
            localStorage.setItem('completedLessons', JSON.stringify(completed));
            const btn = document.getElementById('completeBtn');
            btn.innerHTML = '<i class="fas fa-check-circle"></i> 已完成';
            btn.disabled = true;
        }}

        document.addEventListener('DOMContentLoaded', function() {{
            initEditor();
            initPyodide();
            const completed = JSON.parse(localStorage.getItem('completedLessons') || '{{}}');
            if (completed['{lesson_id}']) {{
                const btn = document.getElementById('completeBtn');
                btn.innerHTML = '<i class="fas fa-check-circle"></i> 已完成';
                btn.disabled = true;
            }}
        }});
    </script>
</body>
</html>'''
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return filepath

def generate_lessons():
    modules = {
        'module1': {'name': '模块一：数据分析前置基础', 'tag': '入门必学', 'count': 5},
        'module2': {'name': '模块二：Pandas核心基础', 'tag': '必会', 'count': 7},
        'module3': {'name': '模块三：数据清洗与预处理', 'tag': '工作最常用', 'count': 7},
        'module4': {'name': '模块四：数据可视化分析', 'tag': '进阶', 'count': 5},
    }
    
    lessons = {
        'module1': [
            '数据分析行业前景与岗位介绍',
            '数据分析思维',
            'Python极简入门',
            'Anaconda与Jupyter环境',
            '在线编程平台使用'
        ],
        'module2': [
            'Pandas与Series',
            'DataFrame结构',
            '读取各类数据',
            '数据查看方法',
            '行列选取与筛选',
            '缺失值与重复值',
            '类型转换与重命名'
        ],
        'module3': [
            '异常值识别与处理',
            '字符串数据清洗',
            '时间日期处理',
            '新增字段与分箱',
            '多表合并',
            '分组聚合groupby',
            '透视表实战'
        ],
        'module4': [
            'Matplotlib基础',
            '常用图表类型',
            '分布分析图表',
            '图表美化',
            '业务报表实战'
        ]
    }
    
    descs = {
        'module1': [
            '了解数据分析行业的发展趋势、岗位需求和薪资水平',
            '培养数据分析思维，掌握业务分析方法',
            '变量、列表、字典、循环、函数基础',
            '安装配置Anaconda和Jupyter Notebook',
            '浏览器中编写和运行Python代码'
        ],
        'module2': [
            'Pandas库介绍和Series数据结构',
            '掌握DataFrame二维表格结构',
            'Excel、CSV、在线数据集读取',
            'head、tail、info、describe',
            'loc、iloc、布尔索引',
            '处理缺失值和重复数据',
            '数据类型转换和字段重命名'
        ],
        'module3': [
            'IQR法、Z-score法',
            '拆分、替换、提取',
            'pd.to_datetime、日期提取',
            '计算字段、cut、qcut',
            'merge、concat',
            'sum、mean、count、agg',
            'pivot_table多维分析'
        ],
        'module4': [
            'figure、axes、plot',
            '折线图、柱状图、饼图',
            '直方图、箱线图',
            '子图布局、配色',
            '综合案例'
        ]
    }
    
    for mod_key, mod_data in modules.items():
        for i in range(1, mod_data['count'] + 1):
            lesson_id = f'm{int(mod_key[-1)}l{i}'
            lesson_title = lessons[mod_key][i-1]
            lesson_desc = descs[mod_key][i-1]
            
            # Generate lesson nav
            lesson_nav = ''
            for j in range(1, mod_data['count'] + 1):
                active = 'active' if j == i else ''
                lesson_nav += f'<a href="lesson{j}.html" class="lesson-nav-item {active}"><span class="nav-number">{j}</span><span class="nav-title">{lessons[mod_key][j-1]}</span></a>'
            
            # Replace placeholder
            filepath = create_lesson_html(i, mod_key, mod_data['name'], mod_data['tag'], lesson_title, lesson_desc, lesson_id)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            content = content.replace('{lesson_nav}', lesson_nav)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f'已生成: {filepath}')

if __name__ == '__main__':
    generate_lessons()
    print('\n所有课程小节页面已生成！')
