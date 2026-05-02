#!/usr/bin/env python3
import re
import os

# 新样式模板
NEW_STYLES = '''
        :root {
            --editor-bg: #1e1e1e;
            --editor-line-num: #858585;
            --editor-selection: #264f78;
            --editor-word: #d4d4d4;
            --editor-keyword: #569cd6;
            --editor-string: #ce9178;
            --editor-comment: #6a9955;
            --editor-function: #dcdcaa;
            --editor-number: #b5cea8;
        }

        .project-page {
            padding-top: 70px;
            min-height: 100vh;
            background: #0d1117;
        }

        .project-header {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
            color: white;
            padding: 2rem;
            position: relative;
            overflow: hidden;
        }

        .project-header-content {
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        .project-back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: rgba(255, 255, 255, 0.9);
            text-decoration: none;
            margin-bottom: 1rem;
            transition: all 0.2s ease;
        }

        .project-back-link:hover {
            color: white;
            transform: translateX(-5px);
        }

        .project-title-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .project-title-row h1 {
            font-size: 1.75rem;
            font-weight: 700;
            margin: 0;
        }

        .project-meta-info {
            display: flex;
            gap: 1.5rem;
            margin-top: 0.75rem;
            flex-wrap: wrap;
        }

        .project-meta-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }

        .project-container {
            max-width: 95%;
            margin: 1.5rem auto;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 1.5rem;
            align-items: start;
        }

        .project-sidebar {
            position: sticky;
            top: 90px;
        }

        .tips-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }

        .tips-card h3 {
            font-size: 1rem;
            font-weight: 600;
            color: #f0f6fc;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .tips-card h3 i {
            color: #f59e0b;
        }

        .tip-item {
            padding: 0.5rem 0;
            border-bottom: 1px solid #21262d;
            color: #8b949e;
            font-size: 0.85rem;
        }

        .tip-item:last-child {
            border-bottom: none;
        }

        .project-main {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .project-section {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 1.5rem;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid #30363d;
        }

        .section-header i {
            font-size: 1.25rem;
            color: #58a6ff;
        }

        .section-header h2 {
            font-size: 1.25rem;
            font-weight: 600;
            color: #f0f6fc;
            margin: 0;
        }

        .section-content {
            color: #c9d1d9;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .section-content p {
            margin: 0.5rem 0;
        }

        .task-description {
            background: rgba(56, 139, 253, 0.1);
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid #58a6ff;
        }

        .task-description h3 {
            font-size: 1rem;
            font-weight: 600;
            color: #f0f6fc;
            margin-bottom: 0.75rem;
        }

        .task-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }

        .task-list li {
            padding: 0.5rem 0;
            padding-left: 1.5rem;
            position: relative;
            color: #c9d1d9;
            font-size: 0.9rem;
        }

        .task-list li::before {
            content: '✓';
            position: absolute;
            left: 0;
            color: #3fb950;
            font-weight: bold;
        }

        .data-table-container {
            overflow-x: auto;
            margin-top: 0.75rem;
            max-height: 300px;
            overflow-y: auto;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.85rem;
        }

        .data-table th {
            background: #21262d;
            color: #f0f6fc;
            padding: 0.625rem;
            text-align: left;
            font-weight: 600;
            position: sticky;
            top: 0;
            border-bottom: 1px solid #30363d;
        }

        .data-table td {
            padding: 0.5rem 0.625rem;
            border-bottom: 1px solid #21262d;
            color: #c9d1d9;
        }

        .data-table tr:hover {
            background-color: #1c2128;
        }

        .data-table .missing {
            background-color: rgba(248, 81, 73, 0.15);
            color: #f85149;
        }

        .data-table .anomaly {
            background-color: rgba(210, 153, 34, 0.15);
            color: #d29922;
        }

        .tip-box {
            background: rgba(219, 188, 32, 0.1);
            border-left: 3px solid #d29922;
            padding: 0.875rem 1rem;
            margin: 0.75rem 0;
            border-radius: 0 6px 6px 0;
        }

        .tip-box .tip-title {
            font-weight: 600;
            color: #d29922;
            margin-bottom: 0.375rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }

        .tip-box .tip-content {
            color: #c9d1d9;
            font-size: 0.9rem;
        }

        .error-box {
            background: rgba(248, 81, 73, 0.1);
            border-left: 3px solid #f85149;
            padding: 0.875rem 1rem;
            margin: 0.75rem 0;
            border-radius: 0 6px 6px 0;
        }

        .error-box .error-title {
            font-weight: 600;
            color: #f85149;
            margin-bottom: 0.375rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
        }

        .error-box .error-content {
            color: #c9d1d9;
            font-size: 0.9rem;
        }

        .code-example {
            background: #0d1117;
            border-radius: 6px;
            padding: 0.875rem;
            margin: 0.75rem 0;
            overflow-x: auto;
            border: 1px solid #30363d;
        }

        .code-example pre {
            margin: 0;
            color: #c9d1d9;
            font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
        }

        .learning-step {
            background: rgba(56, 139, 253, 0.05);
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 3px solid #58a6ff;
        }

        .learning-step:last-child {
            margin-bottom: 0;
        }

        .learning-step h4 {
            font-size: 0.95rem;
            font-weight: 600;
            color: #58a6ff;
            margin-bottom: 0.5rem;
        }

        .learning-step p {
            color: #c9d1d9;
            font-size: 0.9rem;
            margin: 0.5rem 0;
        }

        .code-playground {
            background: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .code-playground.fullscreen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999;
            border-radius: 0;
            margin: 0;
        }

        .code-playground-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1rem;
            background: #161b22;
            border-bottom: 1px solid #30363d;
            flex-shrink: 0;
        }

        .code-playground-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            color: #f0f6fc;
            font-size: 0.95rem;
        }

        .code-controls {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }

        .run-btn, .reset-btn, .answer-btn, .fullscreen-btn {
            padding: 0.5rem 0.875rem;
            border: none;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 0.375rem;
        }

        .run-btn {
            background: #238636;
            color: white;
        }

        .run-btn:hover {
            background: #2ea043;
        }

        .reset-btn {
            background: #21262d;
            color: #c9d1d9;
            border: 1px solid #30363d;
        }

        .reset-btn:hover {
            background: #30363d;
        }

        .answer-btn {
            background: #9e6a03;
            color: white;
        }

        .answer-btn:hover {
            background: #bb7b08;
        }

        .fullscreen-btn {
            background: #6e7681;
            color: white;
        }

        .fullscreen-btn:hover {
            background: #8b949e;
        }

        .fullscreen-btn.active {
            background: #58a6ff;
        }

        .code-editor-wrapper {
            display: grid;
            grid-template-columns: 60% 40%;
            min-height: 500px;
            flex: 1;
            position: relative;
        }

        .code-editor-wrapper.resizing {
            user-select: none;
        }

        .code-editor-panel {
            background: var(--editor-bg);
            display: flex;
            flex-direction: column;
        }

        .code-editor-label {
            padding: 0.5rem 1rem;
            background: #1a1a1a;
            color: #858585;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #333;
            flex-shrink: 0;
        }

        .code-editor-container {
            flex: 1;
            position: relative;
            overflow: hidden;
        }

        .code-editor {
            width: 100%;
            height: 100%;
            min-height: 500px;
            padding: 1rem;
            border: none;
            background: var(--editor-bg);
            color: var(--editor-word);
            font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 15px;
            line-height: 1.6;
            resize: none;
            outline: none;
            tab-size: 4;
            overflow: auto;
        }

        .code-editor::selection {
            background: var(--editor-selection);
        }

        .code-editor::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        .code-editor::-webkit-scrollbar-track {
            background: var(--editor-bg);
        }

        .code-editor::-webkit-scrollbar-thumb {
            background: #444;
            border-radius: 5px;
        }

        .code-editor::-webkit-scrollbar-thumb:hover {
            background: #555;
        }

        .resize-handle {
            width: 6px;
            background: #30363d;
            cursor: col-resize;
            position: relative;
            flex-shrink: 0;
        }

        .resize-handle:hover,
        .resize-handle.active {
            background: #58a6ff;
        }

        .resize-handle::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 2px;
            height: 30px;
            background: #6e7681;
            border-radius: 1px;
        }

        .code-output-panel {
            background: #0d1117;
            display: flex;
            flex-direction: column;
        }

        .code-output-label {
            padding: 0.5rem 1rem;
            background: #161b22;
            color: #858585;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #30363d;
            flex-shrink: 0;
        }

        .code-output {
            padding: 1rem;
            flex: 1;
            overflow-y: auto;
            color: #c9d1d9;
            font-family: 'Fira Code', 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            line-height: 1.5;
            background: #0d1117;
        }

        .code-output::-webkit-scrollbar {
            width: 10px;
            height: 10px;
        }

        .code-output::-webkit-scrollbar-track {
            background: #0d1117;
        }

        .code-output::-webkit-scrollbar-thumb {
            background: #444;
            border-radius: 5px;
        }

        .code-output .placeholder {
            color: #6e7681;
            font-style: italic;
        }

        .code-output .error {
            color: #f85149;
        }

        .code-output .success {
            color: #3fb950;
        }

        .code-output pre {
            margin: 0;
            white-space: pre-wrap;
            word-wrap: break-word;
        }

        .answer-section {
            margin-top: 0;
            display: none;
            background: #161b22;
            border-top: 1px solid #30363d;
        }

        .answer-section.show {
            display: block;
        }

        .answer-content {
            background: #161b22;
            padding: 1rem;
        }

        .answer-content h4 {
            color: #3fb950;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }

        .answer-content pre {
            background: var(--editor-bg);
            color: #c9d1d9;
            padding: 1rem;
            border-radius: 6px;
            overflow-x: auto;
            font-size: 14px;
            line-height: 1.5;
            max-height: 400px;
            overflow-y: auto;
        }

        .description-toggle {
            background: #21262d;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 0.75rem 1rem;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #f0f6fc;
            font-weight: 600;
            transition: all 0.2s;
        }

        .description-toggle:hover {
            background: #30363d;
        }

        .description-toggle i {
            transition: transform 0.2s;
        }

        .description-toggle.collapsed i {
            transform: rotate(-90deg);
        }

        .description-content {
            overflow: hidden;
            transition: max-height 0.3s ease;
        }

        .description-content.collapsed {
            max-height: 0 !important;
        }

        .description-inner {
            padding-top: 1rem;
        }

        .difficulty-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .difficulty-badge.beginner {
            background-color: rgba(16, 185, 129, 0.15);
            color: #10b981;
        }

        .difficulty-badge.intermediate {
            background-color: rgba(59, 130, 246, 0.15);
            color: #3b82f6;
        }

        .difficulty-badge.advanced {
            background-color: rgba(239, 68, 68, 0.15);
            color: #ef4444;
        }

        @media (max-width: 1200px) {
            .project-container {
                grid-template-columns: 1fr;
            }

            .project-sidebar {
                position: static;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
            }

            .tips-card {
                margin-bottom: 0;
            }
        }

        @media (max-width: 768px) {
            .project-header {
                padding: 1.5rem 1rem;
            }

            .project-title-row h1 {
                font-size: 1.5rem;
            }

            .project-meta-info {
                flex-direction: column;
                gap: 0.5rem;
            }

            .project-container {
                max-width: 100%;
                padding: 0 1rem;
                margin: 1rem auto;
            }

            .code-editor-wrapper {
                grid-template-columns: 1fr;
                min-height: 400px;
            }

            .resize-handle {
                display: none;
            }

            .code-controls {
                flex-wrap: wrap;
            }

            .run-btn, .reset-btn, .answer-btn, .fullscreen-btn {
                padding: 0.375rem 0.625rem;
                font-size: 0.8rem;
            }
        }
'''

def update_file(filepath):
    print(f"Updating: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换样式部分
    style_pattern = r'<style>.*?</style>'
    content = re.sub(style_pattern, f'<style>\n{NEW_STYLES}\n    </style>', content, flags=re.DOTALL)
    
    # 更新code-playground-header，添加全屏按钮
    old_header = r'<div class="code-playground-header">\s*<div class="code-playground-title">(.*?)</div>\s*<div class="code-controls">\s*(.*?)\s*</div>\s*</div>'
    
    def update_header(match):
        title = match.group(1)
        controls = match.group(2)
        # 在按钮后添加全屏按钮
        fullscreen_btn = '<button class="fullscreen-btn" id="fullscreen-btn" onclick="toggleFullscreen()"><i class="fas fa-expand"></i> 全屏</button>'
        return f'''<div class="code-playground-header">
                        <div class="code-playground-title">{title}</div>
                        <div class="code-controls">
                            {controls}
                            {fullscreen_btn}
                        </div>
                    </div>'''
    
    content = re.sub(old_header, update_header, content, flags=re.DOTALL)
    
    # 添加JavaScript函数
    js_functions = '''
        function toggleFullscreen() {
            const playground = document.getElementById('code-playground');
            const btn = document.getElementById('fullscreen-btn');
            
            if (!document.fullscreenElement) {
                playground.requestFullscreen().then(() => {
                    playground.classList.add('fullscreen');
                    btn.classList.add('active');
                    btn.innerHTML = '<i class="fas fa-compress"></i> 退出全屏';
                }).catch(err => {
                    console.log('Fullscreen error:', err);
                });
            } else {
                document.exitFullscreen().then(() => {
                    playground.classList.remove('fullscreen');
                    btn.classList.remove('active');
                    btn.innerHTML = '<i class="fas fa-expand"></i> 全屏';
                });
            }
        }

        document.addEventListener('fullscreenchange', function() {
            const playground = document.getElementById('code-playground');
            const btn = document.getElementById('fullscreen-btn');
            
            if (!document.fullscreenElement) {
                playground.classList.remove('fullscreen');
                btn.classList.remove('active');
                btn.innerHTML = '<i class="fas fa-expand"></i> 全屏';
            }
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && document.fullscreenElement) {
                const playground = document.getElementById('code-playground');
                playground.classList.remove('fullscreen');
            }
        });

        function toggleDescription() {
            const content = document.getElementById('description-content');
            const toggle = document.querySelector('.description-toggle');
            
            content.classList.toggle('collapsed');
            toggle.classList.toggle('collapsed');
        }

        function initResize() {
            const handle = document.getElementById('resize-handle');
            const wrapper = document.getElementById('editor-wrapper');
            if (!handle || !wrapper) return;
            
            let isResizing = false;
            let startX, startWidth;

            handle.addEventListener('mousedown', function(e) {
                isResizing = true;
                startX = e.clientX;
                const editorPanel = wrapper.querySelector('.code-editor-panel');
                startWidth = editorPanel.offsetWidth;
                wrapper.classList.add('resizing');
                handle.classList.add('active');
                document.body.style.cursor = 'col-resize';
                e.preventDefault();
            });

            document.addEventListener('mousemove', function(e) {
                if (!isResizing) return;
                
                const diff = e.clientX - startX;
                const editorPanel = wrapper.querySelector('.code-editor-panel');
                const outputPanel = wrapper.querySelector('.code-output-panel');
                const totalWidth = wrapper.offsetWidth;
                
                let newEditorWidth = startWidth + diff;
                const minWidth = totalWidth * 0.3;
                const maxWidth = totalWidth * 0.7;
                
                if (newEditorWidth < minWidth) newEditorWidth = minWidth;
                if (newEditorWidth > maxWidth) newEditorWidth = maxWidth;
                
                editorPanel.style.flex = 'none';
                editorPanel.style.width = newEditorWidth + 'px';
                outputPanel.style.flex = '1';
            });

            document.addEventListener('mouseup', function() {
                if (isResizing) {
                    isResizing = false;
                    wrapper.classList.remove('resizing');
                    handle.classList.remove('active');
                    document.body.style.cursor = '';
                }
            });
        }
    '''
    
    # 在DOMContentLoaded中添加initResize调用
    if 'initResize();' not in content:
        content = content.replace(
            'renderDataTable();',
            'renderDataTable();\n            initResize();\n            \n            const descriptionContent = document.getElementById(\'description-content\');\n            if (descriptionContent) {\n                descriptionContent.style.maxHeight = descriptionContent.scrollHeight + \'px\';\n            }'
        )
    
    # 在script标签末尾添加新函数（在</script>之前）
    content = content.replace(
        '    </script>\n</body>',
        f'{js_functions}\n    </script>\n</body>'
    )
    
    # 添加resize-handle到编辑器
    if '<div class="resize-handle"' not in content:
        content = content.replace(
            '</div>\n                        <div class="code-output-panel">',
            '</div>\n                        <div class="resize-handle" id="resize-handle"></div>\n                        <div class="code-output-panel">'
        )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Updated: {filepath}")

# 更新所有项目页面
projects_dir = '/workspace/data-analytics-platform/projects'
for i in range(2, 11):
    filepath = os.path.join(projects_dir, f'project{i}.html')
    if os.path.exists(filepath):
        update_file(filepath)

print("All project files updated!")
