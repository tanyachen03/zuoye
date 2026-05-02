#!/usr/bin/env python3
import os
import re

NEW_STYLE_BLOCK = '''
        :root {
            --editor-bg: #1e1e1e;
            --editor-line-num: #858585;
            --editor-line-num-bg: #252526;
            --editor-selection: #264f78;
            --editor-word: #d4d4d4;
        }

        .code-playground.fullscreen {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: 9999;
            border-radius: 0;
        }

        .code-playground.split-view {
            display: grid;
            grid-template-columns: 50% 50%;
        }

        .code-playground-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0.75rem 1rem;
            background: #161b22;
            border-bottom: 1px solid #30363d;
        }

        .code-controls {
            display: flex;
            gap: 0.5rem;
        }

        .run-btn, .reset-btn, .answer-btn, .fullscreen-btn, .split-btn {
            padding: 0.5rem 0.875rem;
            border: none;
            border-radius: 6px;
            font-size: 0.85rem;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.375rem;
        }

        .run-btn { background: #238636; color: white; }
        .run-btn:hover { background: #2ea043; }
        .reset-btn { background: #21262d; color: #c9d1d9; border: 1px solid #30363d; }
        .reset-btn:hover { background: #30363d; }
        .answer-btn { background: #9e6a03; color: white; }
        .answer-btn:hover { background: #bb7b08; }
        .fullscreen-btn { background: #6e7681; color: white; }
        .fullscreen-btn:hover { background: #8b949e; }
        .split-btn { background: #6e7681; color: white; }
        .split-btn:hover { background: #8b949e; }
        .split-btn.active { background: #58a6ff; }

        .code-editor-wrapper {
            display: grid;
            grid-template-columns: 60% 40%;
            min-height: 500px;
            flex: 1;
        }

        .code-editor-wrapper.split-mode {
            grid-template-columns: 50% 50%;
        }

        .code-editor-panel {
            background: var(--editor-bg);
            display: flex;
            flex-direction: column;
            position: relative;
        }

        .code-editor-label {
            padding: 0.5rem 1rem;
            background: #1a1a1a;
            color: #858585;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #333;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .code-editor-container {
            flex: 1;
            display: flex;
            position: relative;
            overflow: hidden;
        }

        .line-numbers {
            background: var(--editor-line-num-bg);
            color: var(--editor-line-num);
            padding: 1rem 0.75rem;
            text-align: right;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.6;
            user-select: none;
            min-width: 50px;
            border-right: 1px solid #333;
            overflow: hidden;
        }

        .code-editor-wrapper-textarea {
            flex: 1;
            position: relative;
        }

        .code-editor {
            width: 100%;
            height: 100%;
            min-height: 500px;
            padding: 1rem;
            border: none;
            background: transparent;
            color: var(--editor-word);
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 15px;
            line-height: 1.6;
            resize: none;
            outline: none;
            tab-size: 4;
            white-space: pre;
            overflow: auto;
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

        .code-editor::selection {
            background: var(--editor-selection);
        }

        .autocomplete-dropdown {
            position: absolute;
            background: #252526;
            border: 1px solid #3c3c3c;
            border-radius: 4px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            max-height: 200px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            min-width: 200px;
        }

        .autocomplete-dropdown.show {
            display: block;
        }

        .autocomplete-item {
            padding: 0.5rem 1rem;
            color: #d4d4d4;
            cursor: pointer;
            font-family: 'Fira Code', monospace;
            font-size: 14px;
        }

        .autocomplete-item:hover,
        .autocomplete-item.selected {
            background: #094771;
        }

        .autocomplete-item .item-type {
            color: #9cdcfe;
            font-size: 0.75rem;
            margin-left: 0.5rem;
        }

        .resize-handle {
            width: 6px;
            background: #30363d;
            cursor: col-resize;
            position: relative;
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
        }

        .code-output {
            padding: 1rem;
            flex: 1;
            overflow-y: auto;
            color: #c9d1d9;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.5;
        }

        .code-output .placeholder {
            color: #6e7681;
            font-style: italic;
        }

        .code-output .error {
            color: #f85149;
        }

        .code-output pre {
            margin: 0;
            white-space: pre-wrap;
        }

        .split-panel-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: #1a1a1a;
            color: #858585;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #333;
        }

        .split-panel-label.reference {
            color: #3fb950;
        }

        @media (max-width: 768px) {
            .code-editor-wrapper,
            .code-editor-wrapper.split-mode {
                grid-template-columns: 1fr;
            }
            .resize-handle {
                display: none;
            }
            .code-controls {
                flex-wrap: wrap;
            }
        }
'''

NEW_JS_FUNCTIONS = '''
        let editor, lineNumbers;
        let splitViewActive = false;
        let autocompleteVisible = false;
        let selectedAutocompleteIndex = -1;
        let currentAutocompleteItems = [];

        const autocompleteData = [
            { label: 'pd.DataFrame', type: 'class', desc: '创建DataFrame对象' },
            { label: 'pd.read_csv', type: 'function', desc: '读取CSV文件' },
            { label: 'pd.read_excel', type: 'function', desc: '读取Excel文件' },
            { label: 'pd.to_datetime', type: 'function', desc: '转换日期格式' },
            { label: 'pd.isnull', type: 'function', desc: '检测缺失值' },
            { label: 'pd.notnull', type: 'function', desc: '检测非缺失值' },
            { label: 'pd.merge', type: 'function', desc: '合并数据' },
            { label: 'pd.concat', type: 'function', desc: '拼接数据' },
            { label: 'pd.groupby', type: 'function', desc: '分组聚合' },
            { label: 'df.head', type: 'method', desc: '查看前N行' },
            { label: 'df.tail', type: 'method', desc: '查看后N行' },
            { label: 'df.info', type: 'method', desc: '查看数据信息' },
            { label: 'df.describe', type: 'method', desc: '查看统计描述' },
            { label: 'df.shape', type: 'property', desc: '数据维度' },
            { label: 'df.columns', type: 'property', desc: '列名列表' },
            { label: 'df.fillna', type: 'method', desc: '填充缺失值' },
            { label: 'df.dropna', type: 'method', desc: '删除缺失值' },
            { label: 'df.sum', type: 'method', desc: '求和' },
            { label: 'df.mean', type: 'method', desc: '求均值' },
            { label: 'df.sort_values', type: 'method', desc: '排序' },
            { label: 'df.to_string', type: 'method', desc: '转换为字符串' },
            { label: 'df.rename', type: 'method', desc: '重命名列' },
            { label: 'df.drop', type: 'method', desc: '删除行/列' },
            { label: 'plt.figure', type: 'function', desc: '创建图表' },
            { label: 'plt.plot', type: 'function', desc: '绘制折线图' },
            { label: 'plt.bar', type: 'function', desc: '绘制柱状图' },
            { label: 'plt.scatter', type: 'function', desc: '绘制散点图' },
            { label: 'plt.show', type: 'function', desc: '显示图表' },
            { label: 'plt.title', type: 'function', desc: '设置标题' },
            { label: 'plt.xlabel', type: 'function', desc: '设置X轴标签' },
            { label: 'plt.ylabel', type: 'function', desc: '设置Y轴标签' },
            { label: 'print', type: 'function', desc: '打印输出' },
            { label: 'len', type: 'function', desc: '获取长度' },
        ];

        function initEditor() {
            editor = document.getElementById('code-editor');
            lineNumbers = document.getElementById('line-numbers');
            
            updateLineNumbers();
            
            editor.addEventListener('input', updateLineNumbers);
            editor.addEventListener('scroll', syncScroll);
            editor.addEventListener('keydown', handleKeyDown);
            editor.addEventListener('input', handleAutocomplete);
            editor.addEventListener('blur', () => {
                setTimeout(() => hideAutocomplete(), 200);
            });
        }

        function updateLineNumbers() {
            if (!editor || !lineNumbers) return;
            const lines = editor.value.split('\\n').length;
            let html = '';
            for (let i = 1; i <= lines; i++) {
                html += i + '\\n';
            }
            lineNumbers.textContent = html;
        }

        function syncScroll() {
            if (lineNumbers) lineNumbers.scrollTop = editor.scrollTop;
        }

        function handleKeyDown(e) {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = editor.selectionStart;
                const end = editor.selectionEnd;
                editor.value = editor.value.substring(0, start) + '    ' + editor.value.substring(end);
                editor.selectionStart = editor.selectionEnd = start + 4;
                updateLineNumbers();
            }
            
            if (autocompleteVisible) {
                if (e.key === 'ArrowDown') {
                    e.preventDefault();
                    navigateAutocomplete(1);
                } else if (e.key === 'ArrowUp') {
                    e.preventDefault();
                    navigateAutocomplete(-1);
                } else if (e.key === 'Enter' || e.key === 'Tab') {
                    e.preventDefault();
                    if (selectedAutocompleteIndex >= 0) {
                        selectAutocompleteItem(currentAutocompleteItems[selectedAutocompleteIndex]);
                    }
                } else if (e.key === 'Escape') {
                    hideAutocomplete();
                }
            }
        }

        function handleAutocomplete(e) {
            const cursorPos = editor.selectionStart;
            const textBeforeCursor = editor.value.substring(0, cursorPos);
            const lastWord = textBeforeCursor.match(/[\\w.]+$/);
            
            if (lastWord && lastWord[0].length >= 1) {
                const prefix = lastWord[0].toLowerCase();
                const matches = autocompleteData.filter(item => 
                    item.label.toLowerCase().startsWith(prefix)
                );
                
                if (matches.length > 0) {
                    currentAutocompleteItems = matches;
                    showAutocomplete(matches);
                    return;
                }
            }
            hideAutocomplete();
        }

        function showAutocomplete(items) {
            const dropdown = document.getElementById('autocomplete-dropdown');
            if (!dropdown) return;
            
            dropdown.innerHTML = items.map((item, index) => 
                `<div class="autocomplete-item ${index === 0 ? 'selected' : ''}" data-index="${index}">
                    ${item.label}<span class="item-type">${item.type}</span>
                </div>`
            ).join('');
            
            dropdown.classList.add('show');
            autocompleteVisible = true;
            selectedAutocompleteIndex = 0;
            
            dropdown.querySelectorAll('.autocomplete-item').forEach(el => {
                el.addEventListener('click', () => {
                    const idx = parseInt(el.dataset.index);
                    selectAutocompleteItem(items[idx]);
                });
            });
        }

        function navigateAutocomplete(direction) {
            const items = document.querySelectorAll('.autocomplete-item');
            items[selectedAutocompleteIndex]?.classList.remove('selected');
            
            selectedAutocompleteIndex += direction;
            if (selectedAutocompleteIndex < 0) selectedAutocompleteIndex = items.length - 1;
            if (selectedAutocompleteIndex >= items.length) selectedAutocompleteIndex = 0;
            
            items[selectedAutocompleteIndex]?.classList.add('selected');
        }

        function selectAutocompleteItem(item) {
            const cursorPos = editor.selectionStart;
            const textBeforeCursor = editor.value.substring(0, cursorPos);
            const lastWord = textBeforeCursor.match(/[\\w.]+$/);
            
            if (lastWord) {
                const start = cursorPos - lastWord[0].length;
                editor.value = editor.value.substring(0, start) + item.label + editor.value.substring(cursorPos);
                editor.selectionStart = editor.selectionEnd = start + item.label.length;
            }
            
            hideAutocomplete();
            updateLineNumbers();
        }

        function hideAutocomplete() {
            const dropdown = document.getElementById('autocomplete-dropdown');
            if (dropdown) dropdown.classList.remove('show');
            autocompleteVisible = false;
            selectedAutocompleteIndex = -1;
        }

        function toggleFullscreen() {
            const playground = document.getElementById('code-playground');
            const btn = document.getElementById('fullscreen-btn');
            
            if (!document.fullscreenElement) {
                playground.requestFullscreen().then(() => {
                    playground.classList.add('fullscreen');
                    btn.innerHTML = '<i class="fas fa-compress"></i> 退出全屏';
                });
            } else {
                document.exitFullscreen().then(() => {
                    playground.classList.remove('fullscreen');
                    btn.innerHTML = '<i class="fas fa-expand"></i> 全屏';
                });
            }
        }

        function toggleSplitView() {
            const wrapper = document.getElementById('editor-wrapper');
            const playground = document.getElementById('code-playground');
            const btn = document.getElementById('split-btn');
            const panel = document.getElementById('editor-panel');
            
            splitViewActive = !splitViewActive;
            
            if (splitViewActive) {
                wrapper.classList.add('split-mode');
                playground.classList.add('split-view');
                btn.classList.add('active');
                
                const answerPre = document.getElementById('answer-section')?.querySelector('pre');
                const answerCode = answerPre ? answerPre.textContent : '# 参考答案代码';
                
                const splitPanel = document.createElement('div');
                splitPanel.className = 'code-editor-panel';
                splitPanel.style.borderLeft = '1px solid #333';
                splitPanel.innerHTML = `
                    <div class="split-panel-label reference">
                        <i class="fas fa-book"></i> 参考答案
                    </div>
                    <div class="code-editor-container">
                        <div class="line-numbers" id="ref-line-numbers">${answerCode.split('\\n').map((_, i) => i + 1).join('\\n')}</div>
                        <textarea class="code-editor" id="reference-editor" readonly style="color:#858585;cursor:default;">${answerCode}</textarea>
                    </div>
                `;
                wrapper.insertBefore(splitPanel, document.getElementById('output-panel'));
            } else {
                wrapper.classList.remove('split-mode');
                playground.classList.remove('split-view');
                btn.classList.remove('active');
                
                const refPanel = panel.nextElementSibling;
                if (refPanel && refPanel.classList.contains('code-editor-panel')) {
                    refPanel.remove();
                }
            }
        }

        function initResize() {
            const handle = document.getElementById('resize-handle');
            const wrapper = document.getElementById('editor-wrapper');
            if (!handle || !wrapper) return;
            
            let isResizing = false;
            let startX, startWidth;

            handle.addEventListener('mousedown', (e) => {
                isResizing = true;
                startX = e.clientX;
                const editorPanel = wrapper.querySelector('.code-editor-panel');
                startWidth = editorPanel.offsetWidth;
                handle.classList.add('active');
                e.preventDefault();
            });

            document.addEventListener('mousemove', (e) => {
                if (!isResizing) return;
                const diff = e.clientX - startX;
                const editorPanel = wrapper.querySelector('.code-editor-panel');
                const totalWidth = wrapper.offsetWidth;
                
                let newWidth = startWidth + diff;
                newWidth = Math.max(totalWidth * 0.3, Math.min(totalWidth * 0.7, newWidth));
                editorPanel.style.flex = 'none';
                editorPanel.style.width = newWidth + 'px';
            });

            document.addEventListener('mouseup', () => {
                if (isResizing) {
                    isResizing = false;
                    handle.classList.remove('active');
                }
            });
        }
'''

def update_file(filepath):
    print(f"Updating: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add split button to toolbar
        if 'class="split-btn"' not in content:
            old_toolbar = r'(<button class="fullscreen-btn".*?</button>\s*</div>\s*</div>)'
            new_toolbar = r'''<button class="split-btn" id="split-btn" onclick="toggleSplitView()">
                                <i class="fas fa-columns"></i> 分屏
                            </button>
                            \1'''
            content = re.sub(old_toolbar, new_toolbar, content, flags=re.DOTALL)
        
        # Add line numbers div
        if '<div class="line-numbers"' not in content:
            old_structure = r'(<div class="code-editor-container">)\s*(<textarea class="code-editor")'
            new_structure = r'''\1
                                <div class="line-numbers" id="line-numbers">1</div>
                                <div class="code-editor-wrapper-textarea">
                                    <textarea class="code-editor"'''
            content = re.sub(old_structure, new_structure, content)
            
            # Close the wrapper div
            content = content.replace(
                '</textarea>\n                            </div>\n                        </div>',
                '</textarea>\n                                    <div class="autocomplete-dropdown" id="autocomplete-dropdown"></div>\n                                </div>\n                            </div>\n                        </div>'
            )
        
        # Add resize handle
        if '<div class="resize-handle"' not in content:
            content = content.replace(
                '</div>\n                        <div class="code-output-panel">',
                '</div>\n                        <div class="resize-handle" id="resize-handle"></div>\n                        <div class="code-output-panel">'
            )
        
        # Add JS functions before DOMContentLoaded
        if 'let editor, lineNumbers;' not in content:
            content = content.replace(
                'document.addEventListener(\'DOMContentLoaded\'',
                NEW_JS_FUNCTIONS + '\n\n        document.addEventListener(\'DOMContentLoaded\''
            )
        
        # Update init call
        if 'initEditor();' not in content:
            content = content.replace(
                'renderDataTable();',
                'renderDataTable();\n            initEditor();'
            )
        
        # Add style block before </style>
        if ':root {' in content and '--editor-bg:' not in content:
            content = content.replace(
                '/* ==================== 学习模块样式 ==================== */',
                NEW_STYLE_BLOCK + '\n\n        /* ==================== 学习模块样式 ==================== */'
            )
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Updated: {filepath}")
    except Exception as e:
        print(f"  Error: {e}")

# Update project files
projects_dir = '/workspace/data-analytics-platform/projects'
for i in range(2, 11):
    filepath = os.path.join(projects_dir, f'project{i}.html')
    if os.path.exists(filepath):
        update_file(filepath)

print("All projects updated!")
