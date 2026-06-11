// ============================================================
// Pyodide 代码编辑器 - 简化版
// ============================================================

let pyodideReady = false;
let pyodideLoading = false;
let pyodideInstance = null;

async function initPyodide(statusElement, onReady) {
    if (pyodideReady) {
        if (onReady) onReady();
        return pyodideInstance;
    }

    if (pyodideLoading) {
        return new Promise(resolve => {
            const check = setInterval(() => {
                if (pyodideReady) {
                    clearInterval(check);
                    resolve(pyodideInstance);
                    if (onReady) onReady();
                }
            }, 100);
        });
    }

    pyodideLoading = true;
    if (statusElement) statusElement.textContent = '⏳ 加载 Python 运行时...';

    try {
        // 加载 Pyodide
        if (!window.loadPyodide) {
            await new Promise((resolve, reject) => {
                const script = document.createElement('script');
                script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/pyodide.js';
                script.onload = resolve;
                script.onerror = reject;
                document.head.appendChild(script);
            });
        }

        pyodideInstance = await window.loadPyodide({
            indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
        });

        if (statusElement) statusElement.textContent = '⏳ 加载 Pandas...';
        await pyodideInstance.loadPackage(['pandas', 'numpy']);

        // 初始化全局 Python 环境
        pyodideInstance.runPython(`
import sys
import io
import pandas as pd
import numpy as np

class _OutputCapture:
    def __init__(self):
        self._buffer = io.StringIO()
    def write(self, text):
        self._buffer.write(text)
        return len(text)
    def flush(self):
        pass
    def getvalue(self):
        return self._buffer.getvalue()

def _run_code(code, globals_dict=None):
    if globals_dict is None:
        globals_dict = {}
    globals_dict['pd'] = pd
    globals_dict['np'] = np
    
    capture = _OutputCapture()
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    sys.stdout = capture
    sys.stderr = capture
    
    try:
        # 先尝试作为表达式执行
        result = None
        try:
            result = eval(code, globals_dict)
            if result is not None:
                print(result)
        except SyntaxError:
            # 如果不是表达式，则作为语句执行
            exec(code, globals_dict)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")
    except Exception as e:
        print(f"{type(e).__name__}: {e}")
    finally:
        sys.stdout = old_stdout
        sys.stderr = old_stderr
    
    return capture.getvalue() or "(代码执行完成 - 如果你的代码没有 print 语句，则不会有输出)"

# 全局数据字典
_global_datasets = {}
print("Python 环境初始化完成 ✓")
print(f"Pandas: {pd.__version__}, NumPy: {np.__version__}")
`);

        pyodideReady = true;
        pyodideLoading = false;
        if (statusElement) statusElement.textContent = '✓ Python 就绪';

        if (onReady) onReady();
        return pyodideInstance;

    } catch (err) {
        pyodideLoading = false;
        console.error('Pyodide 初始化失败:', err);
        if (statusElement) statusElement.textContent = '✗ 初始化失败';
        throw err;
    }
}

async function executePythonCode(code, outputElement, statusElement) {
    try {
        if (statusElement) statusElement.textContent = '⏳ 执行中...';
        
        const pyodide = await initPyodide(statusElement);
        
        // 把代码传给 Python 执行
        pyodide.globals.set('_user_code', code);
        const result = pyodideInstance.runPython(`_run_code(_user_code)`);
        
        if (outputElement) {
            outputElement.textContent = result;
        }
        if (statusElement) statusElement.textContent = '✓ 执行完成';
        
        return result;
    } catch (err) {
        const errorMsg = `执行出错: ${err.message}`;
        if (outputElement) outputElement.textContent = errorMsg;
        if (statusElement) statusElement.textContent = '✗ 执行失败';
        return errorMsg;
    }
}

async function loadCSVToPython(csvUrl, variableName, outputElement, statusElement) {
    try {
        if (statusElement) statusElement.textContent = '⏳ 加载数据...';
        
        const pyodide = await initPyodide(statusElement);
        
        const response = await fetch(csvUrl);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        
        const csvText = await response.text();
        pyodide.globals.set('_csv_content', csvText);
        pyodide.globals.set('_var_name', variableName);
        
        const result = pyodideInstance.runPython(`
import io
globals()[_var_name] = pd.read_csv(io.StringIO(_csv_content))
df = globals()[_var_name]
info = f"✓ 数据集已加载为变量: {_var_name}"
info += f"\\n  形状: {df.shape[0]} 行 × {df.shape[1]} 列"
info += f"\\n  列名: {', '.join(df.columns[:6])}"
if len(df.columns) > 6:
    info += "..."
info += f"\\n\\n前 5 行数据:\\n"
info += df.head().to_string()
info
`);
        
        if (outputElement) outputElement.textContent = result;
        if (statusElement) statusElement.textContent = '✓ 数据已加载';
        return true;
        
    } catch (err) {
        const errorMsg = `加载失败: ${err.message}`;
        if (outputElement) outputElement.textContent = errorMsg;
        if (statusElement) statusElement.textContent = '✗ 加载失败';
        return false;
    }
}

// HTML 工具函数
function createCodeEditorHTML(options = {}) {
    const id = Math.random().toString(36).substr(2, 9);
    const defaultCode = options.defaultCode || `# ==========================================
# 🎯 在这里编写你的 Python 代码
# ==========================================
# 可用库: pandas (as pd), numpy (as np)
# 示例:
#   print("Hello World!")
#   df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
#   print(df)
#   print(df.describe())

print("开始编写代码吧!")
`;

    return `
        <div class="code-editor-wrapper" data-editor-id="${id}">
            <div class="card border-0 shadow-lg rounded-4 overflow-hidden mb-4">
                <!-- 头部 -->
                <div class="px-4 py-3 d-flex justify-content-between align-items-center" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
                    <div class="d-flex align-items-center gap-2">
                        <i class="bi bi-code-slash text-white fs-5"></i>
                        <span class="text-white fw-semibold">Python 代码编辑器</span>
                        <span class="badge bg-white bg-opacity-25 text-white rounded-pill px-3 py-1 small py-status" style="font-size: 0.75rem;">
                            <span class="spinner-border spinner-border-sm me-1" style="width: 0.7rem; height: 0.7rem;"></span>初始化中...
                        </span>
                    </div>
                    <div class="d-flex gap-2">
                        <button class="btn btn-sm btn-light rounded-pill px-4 py-2 fw-semibold py-clear-btn">
                            <i class="bi bi-eraser-fill"></i> 清除
                        </button>
                        <button class="btn btn-sm btn-light rounded-pill px-4 py-2 fw-semibold py-run-btn">
                            <i class="bi bi-play-fill"></i> 运行代码
                        </button>
                    </div>
                </div>
                
                <!-- 代码编辑区 -->
                <div class="p-3" style="background: #1e293b;">
                    <textarea class="py-code-input w-100" spellcheck="false" 
                        style="background: #1e293b; color: #e2e8f0; border: 1px solid #334155; border-radius: 8px; padding: 16px; font-family: 'Monaco', 'Menlo', 'Consolas', monospace; font-size: 14px; min-height: 200px; resize: vertical;">${defaultCode}</textarea>
                </div>
                
                <!-- 输出区 -->
                <div>
                    <div class="px-4 py-2 d-flex justify-content-between align-items-center" style="background: #0f172a;">
                        <span class="text-white-50 small"><i class="bi bi-terminal-fill me-1"></i>输出结果</span>
                        <button class="btn btn-sm py-clear-output-btn" style="color: #94a3b8; background: transparent; border: 1px solid #334155; border-radius: 20px; padding: 4px 12px; font-size: 0.8rem;">
                            <i class="bi bi-x-lg"></i> 清除输出
                        </button>
                    </div>
                    <pre class="py-code-output m-0" style="background: #0f172a; color: #4ade80; padding: 20px; font-family: 'Monaco', 'Menlo', monospace; font-size: 13px; min-height: 100px; max-height: 400px; overflow-y: auto; white-space: pre-wrap; word-wrap: break-word; margin: 0;">点击上方 "运行代码" 按钮开始编程...</pre>
                </div>
            </div>
        </div>
    `;
}

function initCodeEditorButtons() {
    document.querySelectorAll('.code-editor-wrapper').forEach(wrapper => {
        const runBtn = wrapper.querySelector('.py-run-btn');
        const clearBtn = wrapper.querySelector('.py-clear-btn');
        const clearOutputBtn = wrapper.querySelector('.py-clear-output-btn');
        const codeInput = wrapper.querySelector('.py-code-input');
        const output = wrapper.querySelector('.py-code-output');
        const status = wrapper.querySelector('.py-status');
        
        // 预初始化 Pyodide
        initPyodide(status);
        
        runBtn.addEventListener('click', () => {
            executePythonCode(codeInput.value, output, status);
        });
        
        clearBtn.addEventListener('click', () => {
            if (confirm('确定要清除所有代码吗？')) {
                codeInput.value = '';
            }
        });
        
        clearOutputBtn.addEventListener('click', () => {
            output.textContent = '输出已清除...';
        });
        
        // Ctrl+Enter 快捷键
        codeInput.addEventListener('keydown', (e) => {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                executePythonCode(codeInput.value, output, status);
            }
        });
    });
}

// 数据集管理
const DATASETS = {
    'sales_data': { name: '销售数据分析', file: 'sales_data.csv', desc: '电商平台销售记录，50 条数据' },
    'customer_data': { name: '客户流失分析', file: 'customer_data.csv', desc: '30 位客户的行为数据' },
    'inventory_data': { name: '库存管理', file: 'inventory_data.csv', desc: '4 款产品 10 天库存数据' }
};

async function loadDatasetToEditor(datasetKey, wrapper) {
    const output = wrapper.querySelector('.py-code-output');
    const status = wrapper.querySelector('.py-status');
    const codeInput = wrapper.querySelector('.py-code-input');
    
    const info = DATASETS[datasetKey];
    if (!info) {
        output.textContent = '未找到数据集: ' + datasetKey;
        return;
    }
    
    const csvUrl = `datasets/${info.file}`;
    const success = await loadCSVToPython(csvUrl, 'df', output, status);
    
    if (success) {
        codeInput.value = `# ==========================================
# 📊 数据集: ${info.name}
# ${info.desc}
# 数据已加载到变量: df
# ==========================================

import pandas as pd
import numpy as np

# 查看数据基本信息
print("=== 数据概览 ===")
print(df.head(10))

print("\\n=== 数据形状 ===")
print(f"共 {len(df)} 行，{len(df.columns)} 列")

print("\\n=== 数据统计 ===")
print(df.describe().to_string())

# 尝试一些分析
print("\\n=== 尝试你的分析代码! ===")
print("提示: 修改下面的代码来探索数据")

# 示例：分组统计
# print(df.groupby('地区')['金额'].sum().sort_values(ascending=False))
`;
    }
}

// 自动初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCodeEditorButtons);
} else {
    setTimeout(initCodeEditorButtons, 100);
}
