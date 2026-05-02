#!/usr/bin/env python3
import os
import re

LIGHT_THEME_STYLES = '''
        :root {
            --editor-bg: #ffffff;
            --editor-line-num: #999999;
            --editor-line-num-bg: #f5f5f5;
            --editor-selection: #b3d7ff;
            --editor-word: #333333;
        }

        .project-page {
            padding-top: 70px;
            min-height: 100vh;
            background: #f8fafc;
        }

        .project-header {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
            color: white;
            padding: 2rem;
        }

        .project-header-content {
            max-width: 1400px;
            margin: 0 auto;
        }

        .project-container {
            max-width: 95%;
            margin: 1.5rem auto;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 1.5rem;
        }

        .project-sidebar {
            position: sticky;
            top: 90px;
        }

        .tips-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }

        .tips-card h3 {
            font-size: 1rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.75rem;
        }

        .tip-item {
            padding: 0.5rem 0;
            border-bottom: 1px solid #f1f5f9;
            color: #64748b;
            font-size: 0.85rem;
        }

        .project-main {
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        .project-section {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
        }

        .section-header {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid #e2e8f0;
        }

        .section-header i {
            font-size: 1.25rem;
            color: #3b82f6;
        }

        .section-header h2 {
            font-size: 1.25rem;
            font-weight: 600;
            color: #1e293b;
            margin: 0;
        }

        .section-content {
            color: #475569;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .task-description {
            background: #eff6ff;
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid #3b82f6;
        }

        .tip-box {
            background: #fffbeb;
            border-left: 3px solid #f59e0b;
            padding: 0.875rem 1rem;
            margin: 0.75rem 0;
            border-radius: 0 6px 6px 0;
        }

        .tip-box .tip-title {
            font-weight: 600;
            color: #92400e;
            margin-bottom: 0.375rem;
        }

        .tip-box .tip-content {
            color: #78350f;
        }

        .error-box {
            background: #fef2f2;
            border-left: 3px solid #ef4444;
            padding: 0.875rem 1rem;
            margin: 0.75rem 0;
            border-radius: 0 6px 6px 0;
        }

        .error-box .error-title {
            font-weight: 600;
            color: #991b1b;
            margin-bottom: 0.375rem;
        }

        .error-box .error-content {
            color: #7f1d1d;
        }

        .code-example {
            background: #f8fafc;
            border-radius: 6px;
            padding: 0.875rem;
            margin: 0.75rem 0;
            border: 1px solid #e2e8f0;
        }

        .code-example pre {
            margin: 0;
            color: #1e293b;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 0.85rem;
        }

        .learning-step {
            background: #f0f9ff;
            border-radius: 6px;
            padding: 1rem;
            margin-bottom: 0.75rem;
            border-left: 3px solid #3b82f6;
        }

        .learning-step h4 {
            font-size: 0.95rem;
            font-weight: 600;
            color: #1e40af;
            margin-bottom: 0.5rem;
        }

        .description-toggle {
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
        }

        .description-toggle i {
            transition: transform 0.2s;
        }

        .description-toggle.collapsed i {
            transform: rotate(-90deg);
        }

        .description-content {
            overflow: hidden;
            transition: max-height 0.3s;
        }

        .description-content.collapsed {
            max-height: 0 !important;
        }

        .description-inner {
            padding-top: 1rem;
        }

        .code-playground {
            background: #ffffff;
            border: 1px solid #e2e8f0;
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
            background: #f8fafc;
            border-bottom: 1px solid #e2e8f0;
        }

        .code-playground-title {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            color: #1e293b;
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

        .run-btn { background: #22c55e; color: white; }
        .run-btn:hover { background: #16a34a; }
        .reset-btn { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
        .reset-btn:hover { background: #e2e8f0; }
        .answer-btn { background: #f59e0b; color: white; }
        .answer-btn:hover { background: #d97706; }
        .fullscreen-btn { background: #64748b; color: white; }
        .fullscreen-btn:hover { background: #475569; }
        .split-btn { background: #64748b; color: white; }
        .split-btn:hover { background: #475569; }
        .split-btn.active { background: #3b82f6; }

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
            background: #f8fafc;
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #e2e8f0;
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
            border-right: 1px solid #e2e8f0;
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
            background: #f8fafc;
        }

        .code-editor::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 5px;
        }

        .code-editor::selection {
            background: var(--editor-selection);
        }

        .autocomplete-dropdown {
            position: absolute;
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 4px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
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
            color: #1e293b;
            cursor: pointer;
            font-family: 'Fira Code', monospace;
            font-size: 14px;
        }

        .autocomplete-item:hover,
        .autocomplete-item.selected {
            background: #eff6ff;
        }

        .autocomplete-item .item-type {
            color: #3b82f6;
            font-size: 0.75rem;
            margin-left: 0.5rem;
        }

        .resize-handle {
            width: 6px;
            background: #e2e8f0;
            cursor: col-resize;
            position: relative;
        }

        .resize-handle:hover,
        .resize-handle.active {
            background: #3b82f6;
        }

        .resize-handle::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 2px;
            height: 30px;
            background: #cbd5e1;
            border-radius: 1px;
        }

        .code-output-panel {
            background: #f8fafc;
            display: flex;
            flex-direction: column;
        }

        .code-output-label {
            padding: 0.5rem 1rem;
            background: #f1f5f9;
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #e2e8f0;
        }

        .code-output {
            padding: 1rem;
            flex: 1;
            overflow-y: auto;
            color: #1e293b;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.5;
        }

        .code-output .placeholder {
            color: #94a3b8;
            font-style: italic;
        }

        .code-output .error {
            color: #dc2626;
        }

        .code-output pre {
            margin: 0;
            white-space: pre-wrap;
        }

        .answer-section {
            display: none;
            background: #f8fafc;
            border-top: 1px solid #e2e8f0;
        }

        .answer-section.show {
            display: block;
        }

        .answer-content {
            padding: 1rem;
        }

        .answer-content h4 {
            color: #16a34a;
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }

        .answer-content pre {
            background: #f8fafc;
            color: #1e293b;
            padding: 1rem;
            border-radius: 6px;
            font-size: 14px;
            max-height: 300px;
            overflow: auto;
            border: 1px solid #e2e8f0;
        }

        .split-panel-label {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            background: #f8fafc;
            color: #64748b;
            font-size: 0.8rem;
            font-weight: 500;
            border-bottom: 1px solid #e2e8f0;
        }

        .split-panel-label.reference {
            color: #16a34a;
        }

        .difficulty-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }

        .difficulty-badge.beginner { background-color: rgba(16, 185, 129, 0.15); color: #10b981; }
        .difficulty-badge.intermediate { background-color: rgba(59, 130, 246, 0.15); color: #3b82f6; }
        .difficulty-badge.advanced { background-color: rgba(239, 68, 68, 0.15); color: #ef4444; }

        @media (max-width: 1200px) {
            .project-container { grid-template-columns: 1fr; }
            .project-sidebar { position: static; display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }
        }

        @media (max-width: 768px) {
            .code-editor-wrapper,
            .code-editor-wrapper.split-mode { grid-template-columns: 1fr; }
            .resize-handle { display: none; }
            .code-controls { flex-wrap: wrap; }
        }
'''

def update_file(filepath):
    print(f"Updating: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find and replace the style block
        style_pattern = r'<style>.*?</style>'
        match = re.search(style_pattern, content, re.DOTALL)
        if match:
            content = content[:match.start()] + f'<style>\n{LIGHT_THEME_STYLES}\n    </style>' + content[match.end():]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Updated: {filepath}")
    except Exception as e:
        print(f"  Error: {e}")

# Update all project files
projects_dir = '/workspace/data-analytics-platform/projects'
for i in range(1, 11):
    filepath = os.path.join(projects_dir, f'project{i}.html')
    if os.path.exists(filepath):
        update_file(filepath)

print("All projects updated to light theme!")
