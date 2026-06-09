#!/usr/bin/env python3
import sys

# Read the file
with open('/workspace/app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the corrupted section and replace it
old_text = """            make_chapter(1, 'Python 基础与环境搭建', '15 分钟',
                '<h3>一、为什么选择 Python 做数据分析？</h3><p>Python 已经成为全球数据科学领域的首选语言。根据 Kaggle、Stack Overflow 等多个年度调查，Python 在数据分析、机器学习领域的使用率连续多年排名第一。它的核心优势体现在以下几个方面：</p><ul><li><strong>生态完整</strong>：从数值计算（NumPy、SciPy）、表格处理（Pandas）、可视化（Matplotlib、Seaborn、Plotly）到机器学习（Scikit-learn、XGBoost、PyTorch），一条工具链走到底</li><li><strong>学习门槛低</strong>：语法简洁直观，非计算机专业的业务人员、产品经理也能快速上手</li><li><strong>通用性强</strong>：数据分析脚本可以无缝对接生产环境、自动化流程、Web 服务</li><li><strong>社区庞大</strong>：遇到问题几乎总能在 Stack Overflow、GitHub 上找到现成的解决方案</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Python 的真正价值不在于语言本身，而在于围绕它形成的「数据科学工具生态」——只要掌握 NumPy + Pandas + Matplotlib 三件套，就能独立完成 80% 以上的商务数据分析任务。</div><h3>二、环境搭建：三种方式对比</h3><p>搭建 Python 数据分析环境主要有三条路径，各有适用场景：</p><table><thead><tr><th>方案</th><th>说明</th><th>适用人群</th><th>推荐度</th></tr></thead><tbody><tr><td>Anaconda</td><td>一站式发行版，内置 Conda、NumPy、Pandas、Jupyter 等 200+ 工具</td><td>初学者、Windows 用户</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td>原生 Python + pip</td><td>安装官方 Python，通过 pip install 按需安装包</td><td>有一定经验的开发者</td><td>⭐⭐⭐⭐</td></tr><tr><td>云端环境</td><td>Google Colab、Kaggle Kernels、JupyterHub 等</td><td>快速实验、教学场景</td><td>⭐⭐⭐</td></tr></tbody></table><h4>2.1 推荐的最小安装命令</h4><p>如果你选择原生 Python + pip 方案，只需一行命令即可搭建核心工具链：</p><pre><code>pip install numpy pandas matplotlib scipy scikit-learn openpyxl jupyter</code></pre><h4>2.2 验证安装</h4><p>安装完成后，在终端或 Jupyter 中运行以下代码来确认版本与可用性：</p><pre><code>import numpy as np
import pandas as pd

print("NumPy 版本:", np.__version__)
print("Pandas 版本:", pd.__version__)
print("数组测试:", np.array([1, 2, 3, 4, 5]).mean())</code></pre><h3>三、Python 与 Excel / SQL 的关系</h3><p>很多刚接触的同学会问：「我已经会用 Excel 做透视表了，为什么还要学 Python？」答案很简单——它们不是替代关系，而是互补关系：</p><ul><li><strong>Excel</strong>：数据量小（万级别）、即席分析、快速出表、给非技术同事看</li><li><strong>Python</strong>：数据量大（十万→千万行）、自动化重复工作、复杂统计与建模、可复现的分析流程</li><li><strong>SQL</strong>：从数据库取数、做简单聚合，与 Python 配合使用最为常见</li></ul><div class="tip-box"><strong>💡 小技巧：</strong>在公司的实际工作流程中，常见模式是「SQL 取数 → Python 清洗和分析 → Excel/PDF 输出结论」。三驾马车齐头并进，是数据分析师的标准工作方式。</div><h3>四、学习路径建议</h3><p>对于零编程基础的同学，建议按以下顺序循序渐进：</p><ul><li><strong>第 1 步：Python 语法基础</strong>——变量、列表、字典、循环、函数（1-2 周）</li><li><strong>第 2 步：NumPy 与 Pandas</strong>——掌握向量化思维与表格操作（2-3 周）</li><li><strong>第 3 步：数据可视化</strong>——用 Matplotlib / Seaborn 画图（1 周）</li><li><strong>第 4 步：真实项目实战</strong>——销售分析、用户分群、流失预测等（持续练习）</li></ul><div class="warn-box"><strong>⚠ 注意事项：</strong>不要陷入「语法学习的无限循环」。很多人学了半年的 for 循环、类、继承，但从来没有分析过一份真实数据。正确的节奏是：掌握基础语法（1-2 周）→ 立即开始做数据分析项目 → 在项目中按需补充语法知识。</div><h3>五、本章小结</h3><p>本章完成了三件事：理解 Python 的生态价值、搭建数据分析环境、规划学习路径。接下来我们将进入 NumPy 和 Pandas 的核心内容，真正开启数据分析之旅。记住：工具只是手段，<strong>把数据变成业务决策</strong> 才是最终目标。</p>',
                'import numpy as np\\nimport pandas as pd\\nprint("NumPy:", np.__version__)\\nprint("Pandas:", pd.__version__)\\narr = np.array([1,2,3,4,5])\\nprint("数组:", arr, "均值:", arr.mean())',
                [{'q':'Pandas 主要处理？','options':['图像数据','结构化表格数据','音频流','二进制'],'answer':1},
                 {'q':'安装 Pandas 用？','options':['pip install pandas','npm i pandas','apt pandas','gem pandas'],'answer':0},
                 {'q':'NumPy 相比 list 的优势？','options':['语法简单','向量化运算更快更省内存','支持任意对象','占用更多内存'],'answer':1}],
                'import numpy as np\\narr = np.array([10,20,30,40,50])\\nprint("均值:", arr.mean())'),"""

new_text = """            make_chapter(1, 'Python 基础与环境搭建', '15 分钟',
                '<h3>一、为什么选择 Python 做数据分析？</h3><p>Python 已经成为全球数据科学领域的首选语言。根据 Kaggle、Stack Overflow 等多个年度调查，Python 在数据分析、机器学习领域的使用率连续多年排名第一。它的核心优势体现在以下几个方面：</p><ul><li><strong>生态完整</strong>：从数值计算（NumPy、SciPy）、表格处理（Pandas）、可视化（Matplotlib、Seaborn、Plotly）到机器学习（Scikit-learn、XGBoost、PyTorch），一条工具链走到底</li><li><strong>学习门槛低</strong>：语法简洁直观，非计算机专业的业务人员、产品经理也能快速上手</li><li><strong>通用性强</strong>：数据分析脚本可以无缝对接生产环境、自动化流程、Web 服务</li><li><strong>社区庞大</strong>：遇到问题几乎总能在 Stack Overflow、GitHub 上找到现成的解决方案</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Python 的真正价值不在于语言本身，而在于围绕它形成的「数据科学工具生态」——只要掌握 NumPy + Pandas + Matplotlib 三件套，就能独立完成 80% 以上的商务数据分析任务。</div><h3>二、环境搭建：三种方式对比</h3><p>搭建 Python 数据分析环境主要有三条路径，各有适用场景：</p><table><thead><tr><th>方案</th><th>说明</th><th>适用人群</th><th>推荐度</th></tr></thead><tbody><tr><td>Anaconda</td><td>一站式发行版，内置 Conda、NumPy、Pandas、Jupyter 等 200+ 工具</td><td>初学者、Windows 用户</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td>原生 Python + pip</td><td>安装官方 Python，通过 pip install 按需安装包</td><td>有一定经验的开发者</td><td>⭐⭐⭐⭐</td></tr><tr><td>云端环境</td><td>Google Colab、Kaggle Kernels、JupyterHub 等</td><td>快速实验、教学场景</td><td>⭐⭐⭐</td></tr></tbody></table><h4>2.1 推荐的最小安装命令</h4><p>如果你选择原生 Python + pip 方案，只需一行命令即可搭建核心工具链：</p><pre><code>pip install numpy pandas matplotlib scipy scikit-learn openpyxl jupyter</code></pre><h4>2.2 验证安装</h4><p>安装完成后，在终端或 Jupyter 中运行以下代码来确认版本与可用性：</p><pre><code>import numpy as np\nimport pandas as pd\n\nprint("NumPy 版本:", np.__version__)\nprint("Pandas 版本:", pd.__version__)\nprint("数组测试:", np.array([1, 2, 3, 4, 5]).mean())</code></pre><h3>三、Python 与 Excel / SQL 的关系</h3><p>很多刚接触的同学会问：「我已经会用 Excel 做透视表了，为什么还要学 Python？」答案很简单——它们不是替代关系，而是互补关系：</p><ul><li><strong>Excel</strong>：数据量小（万级别）、即席分析、快速出表、给非技术同事看</li><li><strong>Python</strong>：数据量大（十万→千万行）、自动化重复工作、复杂统计与建模、可复现的分析流程</li><li><strong>SQL</strong>：从数据库取数、做简单聚合，与 Python 配合使用最为常见</li></ul><div class="tip-box"><strong>💡 小技巧：</strong>在公司的实际工作流程中，常见模式是「SQL 取数 → Python 清洗和分析 → Excel/PDF 输出结论」。三驾马车齐头并进，是数据分析师的标准工作方式。</div><h3>四、学习路径建议</h3><p>对于零编程基础的同学，建议按以下顺序循序渐进：</p><ul><li><strong>第 1 步：Python 语法基础</strong>——变量、列表、字典、循环、函数（1-2 周）</li><li><strong>第 2 步：NumPy 与 Pandas</strong>——掌握向量化思维与表格操作（2-3 周）</li><li><strong>第 3 步：数据可视化</strong>——用 Matplotlib / Seaborn 画图（1 周）</li><li><strong>第 4 步：真实项目实战</strong>——销售分析、用户分群、流失预测等（持续练习）</li></ul><div class="warn-box"><strong>⚠ 注意事项：</strong>不要陷入「语法学习的无限循环」。很多人学了半年的 for 循环、类、继承，但从来没有分析过一份真实数据。正确的节奏是：掌握基础语法（1-2 周）→ 立即开始做数据分析项目 → 在项目中按需补充语法知识。</div><h3>五、本章小结</h3><p>本章完成了三件事：理解 Python 的生态价值、搭建数据分析环境、规划学习路径。接下来我们将进入 NumPy 和 Pandas 的核心内容，真正开启数据分析之旅。记住：工具只是手段，<strong>把数据变成业务决策</strong> 才是最终目标。</p>',
                "import numpy as np\\nimport pandas as pd\\nprint('NumPy:', np.__version__)\\nprint('Pandas:', pd.__version__)\\narr = np.array([1,2,3,4,5])\\nprint('数组:', arr, '均值:', arr.mean())",
                [{'q':'Pandas 主要处理？','options':['图像数据','结构化表格数据','音频流','二进制'],'answer':1},
                 {'q':'安装 Pandas 用？','options':['pip install pandas','npm i pandas','apt pandas','gem pandas'],'answer':0},
                 {'q':'NumPy 相比 list 的优势？','options':['语法简单','向量化运算更快更省内存','支持任意对象','占用更多内存'],'answer':1}],
                "import numpy as np\\narr = np.array([10,20,30,40,50])\\nprint('均值:', arr.mean())"),"""

if old_text not in content:
    print("ERROR: Could not find old_text in content!")
    print("Searching for partial match...")
    if "make_chapter(1, 'Python 基础与环境搭建'" in content:
        print("Found make_chapter(1, ...) in content")
    sys.exit(1)

new_content = content.replace(old_text, new_text, 1)
with open('/workspace/app.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("File updated")

# Verify syntax
import ast
try:
    ast.parse(new_content)
    print("SYNTAX OK!")
except SyntaxError as e:
    print(f"SYNTAX ERROR: {e}")