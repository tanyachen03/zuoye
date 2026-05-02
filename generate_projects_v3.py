#!/usr/bin/env python3
import os
import re

PROJECTS_DIR = "/workspace/data-analytics-platform/projects"

# 所有项目的配置
PROJECTS_CONFIG = {
    "project4.html": {
        "title": "项目4：RFM客户价值分析 - 数析学院",
        "project_name": "项目4：RFM客户价值分析",
        "difficulty": "中级",
        "time": "45分钟",
        "tech": "Python + Pandas",
        "data_info": "客户交易记录",
        "tips_title": "RFM分析技巧",
        "tips": [
            ("recency", "最近一次购买时间"),
            ("frequency", "购买频率"),
            ("monetary", "消费金额"),
            ("pd.qcut()", "分位数分组"),
        ],
        "goals": [
            "理解RFM模型原理",
            "学会客户分群方法",
            "掌握客户价值评估",
        ],
        "description": "某零售企业需要通过RFM模型对客户进行价值分群，找出高价值客户群体。",
        "task_title": "请完成以下分析任务：",
        "tasks": [
            "计算每个客户的R、F、M值",
            "对客户进行RFM评分",
        ],
        "default_code": '''import pandas as pd
from datetime import datetime

# 客户交易数据
data = [
    {"用户ID": "U001", "交易日期": "2024-01-15", "交易金额": 580},
    {"用户ID": "U001", "交易日期": "2024-02-20", "交易金额": 320},
    {"用户ID": "U001", "交易日期": "2024-03-10", "交易金额": 450},
    {"用户ID": "U002", "交易日期": "2023-12-05", "交易金额": 1200},
    {"用户ID": "U003", "交易日期": "2024-03-01", "交易金额": 280},
    {"用户ID": "U003", "交易日期": "2024-03-15", "交易金额": 350},
    {"用户ID": "U004", "交易日期": "2023-10-20", "交易金额": 890},
    {"用户ID": "U005", "交易日期": "2024-02-28", "交易金额": 1500},
    {"用户ID": "U005", "交易日期": "2024-03-05", "交易金额": 680},
    {"用户ID": "U005", "交易日期": "2024-03-12", "交易金额": 420},
]

df = pd.DataFrame(data)
df['交易日期'] = pd.to_datetime(df['交易日期'])
print("【原始数据】")
print(df.to_string(index=False))

# TODO: 完成RFM分析
# 1. 计算每个用户的R、F、M值
# 2. 对客户进行评分

print("\\n【RFM分析结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd
from datetime import datetime

data = [
    {"用户ID": "U001", "交易日期": "2024-01-15", "交易金额": 580},
    {"用户ID": "U001", "交易日期": "2024-02-20", "交易金额": 320},
    {"用户ID": "U001", "交易日期": "2024-03-10", "交易金额": 450},
    {"用户ID": "U002", "交易日期": "2023-12-05", "交易金额": 1200},
    {"用户ID": "U003", "交易日期": "2024-03-01", "交易金额": 280},
    {"用户ID": "U003", "交易日期": "2024-03-15", "交易金额": 350},
    {"用户ID": "U004", "交易日期": "2023-10-20", "交易金额": 890},
    {"用户ID": "U005", "交易日期": "2024-02-28", "交易金额": 1500},
    {"用户ID": "U005", "交易日期": "2024-03-05", "交易金额": 680},
    {"用户ID": "U005", "交易日期": "2024-03-12", "交易金额": 420},
]

df = pd.DataFrame(data)
df['交易日期'] = pd.to_datetime(df['交易日期'])

analysis_date = pd.to_datetime('2024-03-20')

rfm = df.groupby('用户ID').agg({
    '交易日期': lambda x: (analysis_date - x.max()).days,
    '用户ID': 'count',
    '交易金额': 'sum'
}).rename(columns={
    '交易日期': 'R',
    '用户ID': 'F',
    '交易金额': 'M'
})

rfm['R_Score'] = pd.qcut(rfm['R'], q=3, labels=[3, 2, 1])
rfm['F_Score'] = pd.qcut(rfm['F'], q=3, labels=[1, 2, 3], duplicates='drop')
rfm['M_Score'] = pd.qcut(rfm['M'], q=3, labels=[1, 2, 3])

print("【RFM分析结果】")
print(rfm.to_string())'''
    },
}

def generate_project_html(config):
    difficulty_class = "beginner" if config["difficulty"] == "初级" else "intermediate" if config["difficulty"] == "中级" else "advanced"
    
    tips_html = "\n".join([f'                    <div class="tip-item">\n                        <strong>{t[0]}</strong> - {t[1]}\n                    </div>' for t in config["tips"]])
    goals_html = "\n".join([f'                    <div class="tip-item">{g}</div>' for g in config["goals"]])
    tasks_html = "\n".join([f'                                <li style="padding:0.5rem 0;padding-left:1.5rem;position:relative;">\n                                    <span style="position:absolute;left:0;color:#3fb950;">✓</span>\n                                    {t}\n                                </li>' for t in config["tasks"]])
    
    default_code_escaped = config["default_code"].replace("\\", "\\\\").replace("`", "\\`")
    answer_code_escaped = config["answer_code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config["title"]}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../styles.css">
    
    <!-- CodeMirror -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/monokai.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>
    
    <!-- Pyodide -->
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    
    <style>
        .project-page {{
            padding-top: 70px;
            min-height: 100vh;
            background: #f8fafc;
        }}

        .project-header {{
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
            color: white;
            padding: 2rem;
        }}

        .project-header-content {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .project-container {{
            max-width: 95%;
            margin: 1.5rem auto;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 1.5rem;
        }}

        .project-sidebar {{
            position: sticky;
            top: 90px;
        }}

        .tips-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }}

        .tips-card h3 {{
            font-size: 1rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.75rem;
        }}

        .tip-item {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #f1f5f9;
            color: #64748b;
            font-size: 0.85rem;
        }}

        .project-main {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .project-section {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
        }}

        .section-content {{
            color: #475569;
            line-height: 1.6;
            font-size: 0.95rem;
        }}

        .task-description {{
            background: #eff6ff;
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid #3b82f6;
        }}

        .description-toggle {{
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 0.75rem 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #1e293b;
            font-weight: 600;
        }}

        .description-toggle i {{
            transition: transform 0.2s;
        }}

        .description-toggle.collapsed i {{
            transform: rotate(-90deg);
        }}

        .description-content {{
            overflow: hidden;
            transition: max-height 0.3s;
        }}

        .description-content.collapsed {{
            max-height: 0 !important;
        }}

        .description-inner {{
            padding-top: 1rem;
        }}
        
        .editor-container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }}
        
        .editor-toolbar {{
            background: #f8fafc;
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            gap: 10px;
        }}
        
        .editor-toolbar button {{
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        
        .btn-run {{
            background: #22c55e;
            color: white;
        }}
        
        .btn-run:hover {{
            background: #16a34a;
        }}
        
        .btn-reset {{
            background: #f1f5f9;
            color: #475569;
            border: 1px solid #e2e8f0;
        }}
        
        .btn-reset:hover {{
            background: #e2e8f0;
        }}
        
        .btn-answer {{
            background: #f59e0b;
            color: white;
        }}
        
        .btn-answer:hover {{
            background: #d97706;
        }}
        
        .btn-copy {{
            background: #3b82f6;
            color: white;
        }}
        
        .btn-copy:hover {{
            background: #2563eb;
        }}
        
        .btn-fullscreen {{
            background: #64748b;
            color: white;
        }}
        
        .btn-fullscreen:hover {{
            background: #475569;
        }}
        
        .editor-main {{
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .CodeMirror {{
            height: 500px !important;
            font-size: 15px;
        }}
        
        .output-area {{
            background: #0f172a;
            padding: 16px;
        }}
        
        .output-area pre {{
            margin: 0;
            color: #e2e8f0;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        
        .status {{
            padding: 8px 16px;
            background: #fffbeb;
            border-left: 3px solid #f59e0b;
            margin-bottom: 10px;
            border-radius: 0 6px 6px 0;
            color: #92400e;
        }}

        .difficulty-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .difficulty-badge.beginner {{
            background-color: rgba(16, 185, 129, 0.15);
            color: #10b981;
        }}
        
        .difficulty-badge.intermediate {{
            background-color: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
        }}
        
        .difficulty-badge.advanced {{
            background-color: rgba(239, 68, 68, 0.15);
            color: #ef4444;
        }}

        @media (max-width: 1200px) {{
            .project-container {{
                grid-template-columns: 1fr;
            }}

            .project-sidebar {{
                position: static;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="navbar">
        <div class="navbar-container">
            <div class="navbar-logo" onclick="location.href='../index.html'">
                <i class="fas fa-chart-bar"></i>
                <span>数析学院</span>
            </div>
            <nav class="navbar-menu">
                <a href="../index.html" class="nav-link">首页</a>
                <a href="#courses" class="nav-link">课程中心</a>
                <a href="../projects.html" class="nav-link active">实战项目</a>
                <a href="../achievements.html" class="nav-link">成就殿堂</a>
            </nav>
            <button class="hamburger-menu" id="hamburger-menu">
                <i class="fas fa-bars"></i>
            </button>
            <div class="navbar-auth">
                <button id="login-btn" class="auth-btn login-btn">
                    <i class="fas fa-sign-in-alt"></i> 登录
                </button>
                <button id="register-btn" class="auth-btn register-btn">
                    <i class="fas fa-user-plus"></i> 注册
                </button>
            </div>
        </div>
    </header>

    <div class="project-page">
        <div class="project-header">
            <div class="project-header-content">
                <a href="../projects.html" class="project-back-link" style="color:white;text-decoration:none;display:inline-flex;align-items:center;gap:0.5rem;">
                    <i class="fas fa-arrow-left"></i> 返回实战项目
                </a>
                <div class="project-title-row" style="display:flex;align-items:center;gap:1rem;margin-top:0.5rem;">
                    <h1 style="font-size:1.75rem;font-weight:700;">{config["project_name"]}</h1>
                    <span class="difficulty-badge {difficulty_class}">{config["difficulty"]}</span>
                </div>
                <div style="display:flex;gap:1.5rem;margin-top:0.75rem;font-size:0.9rem;">
                    <span><i class="fas fa-clock"></i> 预计时长：{config["time"]}</span>
                    <span><i class="fas fa-code"></i> 技术栈：{config["tech"]}</span>
                    <span><i class="fas fa-database"></i> 数据量：{config["data_info"]}</span>
                </div>
            </div>
        </div>

        <div class="project-container">
            <div class="project-sidebar">
                <div class="tips-card">
                    <h3><i class="fas fa-lightbulb"></i> {config["tips_title"]}</h3>
{tips_html}
                </div>
                <div class="tips-card">
                    <h3><i class="fas fa-check-circle"></i> 学习目标</h3>
{goals_html}
                </div>
            </div>

            <div class="project-main">
                <div class="project-section">
                    <div class="description-toggle" onclick="toggleDescription()">
                        <span><i class="fas fa-book"></i> 题目描述 & 学习内容</span>
                        <i class="fas fa-chevron-down"></i>
                    </div>
                    <div class="description-content" id="description-content">
                        <div class="description-inner">
                            <div class="section-content">
                                <p>{config["description"]}</p>
                            </div>

                            <div class="task-description" style="margin-top:1rem;">
                                <h3>{config["task_title"]}</h3>
                                <ul style="list-style:none;padding:0;">
{tasks_html}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="status" id="status">
                    <i class="fas fa-spinner fa-spin"></i> 环境加载中，请稍候...
                </div>

                <div class="editor-container">
                    <div class="editor-toolbar">
                        <button class="btn-run" onclick="runCode()">
                            <i class="fas fa-play"></i> 运行代码
                        </button>
                        <button class="btn-reset" onclick="resetCode()">
                            <i class="fas fa-undo"></i> 重置
                        </button>
                        <button class="btn-answer" onclick="toggleAnswer()">
                            <i class="fas fa-lightbulb"></i> 参考答案
                        </button>
                        <button class="btn-copy" onclick="copyAnswer()">
                            <i class="fas fa-clipboard"></i> 复制
                        </button>
                        <button class="btn-fullscreen" onclick="toggleFullscreen()">
                            <i class="fas fa-expand"></i> 全屏
                        </button>
                    </div>

                    <div class="editor-main">
                        <div id="code-editor"></div>
                    </div>

                    <div class="output-area">
                        <pre id="output">// 运行结果将显示在这里</pre>
                    </div>
                </div>

                <div id="answer-section" style="display:none; margin-top:20px; padding:16px; background:#f0fdf4; border-radius:8px; border:1px solid #86efac;">
                    <h3 style="margin:0 0 10px 0; color:#166534;"><i class="fas fa-check-circle"></i> 参考答案代码</h3>
                    <pre style="background:#e0f2fe; padding:12px; border-radius:6px; margin:0;">{answer_code_escaped}</pre>
                </div>

            </div>
        </div>
    </div>

    <script src="../script.js"></script>
    <script>
        let editor;
        let pyodide;
        let isRunning = false;

        const defaultCode = `{default_code_escaped}`;
        const answerCode = `{default_code_escaped.replace("\\", "\\\\").replace("`", "\\`")}`;

        function initEditor() {{
            editor = CodeMirror(document.getElementById('code-editor'), {{
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                tabSize: 4,
                indentUnit: 4,
                indentWithTabs: false,
                value: defaultCode
            }});
        }}

        async function initPyodide() {{
            try {{
                pyodide = await loadPyodide();
                document.getElementById('status').innerHTML =
                    '<i class="fas fa-check-circle"></i> 环境加载完成！可以开始编写代码了。';
                document.getElementById('status').style.background = '#f0fdf4';
                document.getElementById('status').style.borderLeftColor = '#22c55e';
                document.getElementById('status').style.color = '#166534';
            }} catch (err) {{
                document.getElementById('status').innerHTML =
                    '<i class="fas fa-exclamation-triangle"></i> 环境加载失败: ' + err;
                document.getElementById('status').style.background = '#fef2f2';
                document.getElementById('status').style.borderLeftColor = '#ef4444';
                document.getElementById('status').style.color = '#991b1b';
            }}
        }}

        async function runCode() {{
            if (!pyodide) {{
                document.getElementById('output').textContent = '环境还在加载中，请稍候...';
                return;
            }}

            if (isRunning) {{
                return;
            }}

            isRunning = true;
            const code = editor.getValue();
            const outputElement = document.getElementById('output');

            outputElement.textContent = '⏳ 正在运行...';

            try {{
                let output = '';
                pyodide.runPython(`
import sys
from io import StringIO
sys.stdout = StringIO()
`);

                await pyodide.runPythonAsync(code);

                output = pyodide.runPython(`
result = sys.stdout.getvalue()
sys.stdout = sys.__stdout__
result
`);

                if (output.trim() === '') {{
                    output = '✅ 代码运行成功！没有输出内容。';
                }}

                outputElement.textContent = output;
            }} catch (err) {{
                outputElement.textContent = '❌ 运行错误:\\n' + err;
            }} finally {{
                isRunning = false;
            }}
        }}

        function resetCode() {{
            editor.setValue(defaultCode);
            document.getElementById('output').textContent = '// 运行结果将显示在这里';
        }}

        function toggleAnswer() {{
            const answerSection = document.getElementById('answer-section');
            if (answerSection.style.display === 'none') {{
                answerSection.style.display = 'block';
            }} else {{
                answerSection.style.display = 'none';
            }}
        }}
        
        function copyAnswer() {{
            editor.setValue(answerCode);
            const btn = event.target.closest('button');
            const originalHTML = btn.innerHTML;
            btn.innerHTML = '<i class="fas fa-check"></i> 已复制';
            setTimeout(() => {{
                btn.innerHTML = originalHTML;
            }}, 1500);
        }}

        function toggleFullscreen() {{
            const container = document.querySelector('.editor-container');
            if (!document.fullscreenElement) {{
                container.requestFullscreen().catch(err => {{
                    console.log('全屏失败:', err);
                }});
            }} else {{
                document.exitFullscreen();
            }}
        }}

        function toggleDescription() {{
            const content = document.getElementById('description-content');
            const toggle = document.querySelector('.description-toggle');
            content.classList.toggle('collapsed');
            toggle.classList.toggle('collapsed');
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            initEditor();
            initPyodide();

            const descriptionContent = document.getElementById('description-content');
            if (descriptionContent) {{
                descriptionContent.style.maxHeight = descriptionContent.scrollHeight + 'px';
            }}
        }});
    </script>
</body>
</html>'''
    return html

def main():
    for filename, config in PROJECTS_CONFIG.items():
        print(f"正在生成 {filename}...")
        html = generate_project_html(config)
        filepath = os.path.join(PROJECTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ {filename} 生成完成")
    
    print("\n所有项目文件已更新！")

if __name__ == "__main__":
    main()
