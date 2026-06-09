"""
商务数据分析在线教育平台 - Flask 后端
运行: pip install -r requirements.txt && python generate_datasets.py && python app.py
访问: http://localhost:5000
"""
import os
import io
import sys
import json
import time
import random
import hashlib
import traceback
import sqlite3
from datetime import datetime, timedelta
from functools import wraps

from flask import (Flask, render_template, request, redirect, url_for,
                   session, jsonify, flash, send_from_directory, abort, g)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

# ============================================================
# 应用初始化
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'biz-analytics-edu-platform-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'platform.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

db = SQLAlchemy(app)


# ============================================================
# 数据库模型
# ============================================================
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    display_name = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    consecutive_days = db.Column(db.Integer, default=0)
    last_activity_date = db.Column(db.String(20))
    assessment_score = db.Column(db.Integer, default=0)

    chapters = db.relationship('ChapterProgress', backref='user', lazy=True)
    projects = db.relationship('ProjectProgress', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def check_password(self, password):
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()


class ChapterProgress(db.Model):
    __tablename__ = 'chapter_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)


class ProjectProgress(db.Model):
    __tablename__ = 'project_progress'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime)


class UserBadge(db.Model):
    __tablename__ = 'user_badges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    badge_key = db.Column(db.String(50), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)


# 徽章定义
BADGES = {
    'newbie':       {'icon': '🎉', 'name': '初来乍到',   'desc': '首次登录平台'},
    'coder':        {'icon': '💻', 'name': '代码新秀',   'desc': '完成 1 个项目'},
    'analyst':      {'icon': '📊', 'name': '数据分析师', 'desc': '完成 5 个项目'},
    'master':       {'icon': '🏆', 'name': '数据科学大师', 'desc': '完成 10 个项目'},
    'perfect':      {'icon': '🎯', 'name': '完美学霸',   'desc': '综合测评满分'},
    'persistence':  {'icon': '🔥', 'name': '坚持不懈',   'desc': '连续学习 7 天'},
}


# ============================================================
# 工具函数
# ============================================================
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.path))
        return f(*args, **kwargs)
    return wrapper


def current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None


def grant_badge(user, badge_key):
    """给用户颁发徽章，返回 True 表示是新获得的。"""
    existing = UserBadge.query.filter_by(user_id=user.id, badge_key=badge_key).first()
    if existing:
        return False
    b = UserBadge(user_id=user.id, badge_key=badge_key)
    db.session.add(b)
    db.session.commit()
    return True


def check_badges(user):
    """检查并颁发所有可能的徽章。返回新获得徽章列表。"""
    newly = []
    # 初来乍到：任何已登录用户
    if grant_badge(user, 'newbie'):
        newly.append('newbie')
    done_projects = ProjectProgress.query.filter_by(user_id=user.id, completed=True).count()
    if done_projects >= 1 and grant_badge(user, 'coder'):
        newly.append('coder')
    if done_projects >= 5 and grant_badge(user, 'analyst'):
        newly.append('analyst')
    if done_projects >= 10 and grant_badge(user, 'master'):
        newly.append('master')
    if (user.assessment_score or 0) >= 100 and grant_badge(user, 'perfect'):
        newly.append('perfect')
    if (user.consecutive_days or 0) >= 7 and grant_badge(user, 'persistence'):
        newly.append('persistence')
    return newly


def touch_activity(user):
    """记录每日学习活动，计算连续天数。"""
    today = datetime.utcnow().strftime('%Y-%m-%d')
    if user.last_activity_date == today:
        return
    yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
    if user.last_activity_date == yesterday:
        user.consecutive_days = (user.consecutive_days or 0) + 1
    else:
        user.consecutive_days = 1
    user.last_activity_date = today
    db.session.commit()


# ============================================================
# 课程数据（5门，每门 3-5 章）
# ============================================================
def make_chapter(cid, title, duration, theory, code_text, quiz, starter):
    return {'id': cid, 'title': title, 'duration': duration, 'theory': theory,
            'code_example': code_text, 'quiz': quiz, 'starter_code': starter}


COURSES = {
    1: {
        'id': 1, 'title': 'Python数据分析基础', 'icon': '🐍',
        'color': '#3776ab', 'level': '入门',
        'description': '掌握 NumPy、Pandas 等核心工具，奠定数据分析基础。',
        'chapters': [
            make_chapter(1, 'Python 基础与环境搭建', '15 分钟',
                '''<h3>一、为什么选择 Python 做数据分析？</h3><p>Python 已经成为全球数据科学领域的首选语言。根据 Kaggle、Stack Overflow 等多个年度调查，Python 在数据分析、机器学习领域的使用率连续多年排名第一。它的核心优势体现在以下几个方面：</p><ul><li><strong>生态完整</strong>：从数值计算（NumPy、SciPy）、表格处理（Pandas）、可视化（Matplotlib、Seaborn、Plotly）到机器学习（Scikit-learn、XGBoost、PyTorch），一条工具链走到底</li><li><strong>学习门槛低</strong>：语法简洁直观，非计算机专业的业务人员、产品经理也能快速上手</li><li><strong>通用性强</strong>：数据分析脚本可以无缝对接生产环境、自动化流程、Web 服务</li><li><strong>社区庞大</strong>：遇到问题几乎总能在 Stack Overflow、GitHub 上找到现成的解决方案</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Python 的真正价值不在于语言本身，而在于围绕它形成的「数据科学工具生态」——只要掌握 NumPy + Pandas + Matplotlib 三件套，就能独立完成 80% 以上的商务数据分析任务。</div><h3>二、环境搭建：三种方式对比</h3><p>搭建 Python 数据分析环境主要有三条路径，各有适用场景：</p><table><thead><tr><th>方案</th><th>说明</th><th>适用人群</th><th>推荐度</th></tr></thead><tbody><tr><td>Anaconda</td><td>一站式发行版，内置 Conda、NumPy、Pandas、Jupyter 等 200+ 工具</td><td>初学者、Windows 用户</td><td>⭐⭐⭐⭐⭐</td></tr><tr><td>原生 Python + pip</td><td>安装官方 Python，通过 pip install 按需安装包</td><td>有一定经验的开发者</td><td>⭐⭐⭐⭐</td></tr><tr><td>云端环境</td><td>Google Colab、Kaggle Kernels、JupyterHub 等</td><td>快速实验、教学场景</td><td>⭐⭐⭐</td></tr></tbody></table><h4>2.1 推荐的最小安装命令</h4><p>如果你选择原生 Python + pip 方案，只需一行命令即可搭建核心工具链：</p><pre><code>pip install numpy pandas matplotlib scipy scikit-learn openpyxl jupyter</code></pre><h4>2.2 验证安装</h4><p>安装完成后，在终端或 Jupyter 中运行以下代码来确认版本与可用性：</p><pre><code>import numpy as np
import pandas as pd

print("NumPy 版本:", np.__version__)
print("Pandas 版本:", pd.__version__)
print("数组测试:", np.array([1, 2, 3, 4, 5]).mean())</code></pre><h3>三、Python 与 Excel / SQL 的关系</h3><p>很多刚接触的同学会问：「我已经会用 Excel 做透视表了，为什么还要学 Python？」答案很简单——它们不是替代关系，而是互补关系：</p><ul><li><strong>Excel</strong>：数据量小（万级别）、即席分析、快速出表、给非技术同事看</li><li><strong>Python</strong>：数据量大（十万→千万行）、自动化重复工作、复杂统计与建模、可复现的分析流程</li><li><strong>SQL</strong>：从数据库取数、做简单聚合，与 Python 配合使用最为常见</li></ul><div class="tip-box"><strong>💡 小技巧：</strong>在公司的实际工作流程中，常见模式是「SQL 取数 → Python 清洗和分析 → Excel/PDF 输出结论」。三驾马车齐头并进，是数据分析师的标准工作方式。</div><h3>四、学习路径建议</h3><p>对于零编程基础的同学，建议按以下顺序循序渐进：</p><ul><li><strong>第 1 步：Python 语法基础</strong>——变量、列表、字典、循环、函数（1-2 周）</li><li><strong>第 2 步：NumPy 与 Pandas</strong>——掌握向量化思维与表格操作（2-3 周）</li><li><strong>第 3 步：数据可视化</strong>——用 Matplotlib / Seaborn 画图（1 周）</li><li><strong>第 4 步：真实项目实战</strong>——销售分析、用户分群、流失预测等（持续练习）</li></ul><div class="warn-box"><strong>⚠ 注意事项：</strong>不要陷入「语法学习的无限循环」。很多人学了半年的 for 循环、类、继承，但从来没有分析过一份真实数据。正确的节奏是：掌握基础语法（1-2 周）→ 立即开始做数据分析项目 → 在项目中按需补充语法知识。</div><h3>五、本章小结</h3><p>本章完成了三件事：理解 Python 的生态价值、搭建数据分析环境、规划学习路径。接下来我们将进入 NumPy 和 Pandas 的核心内容，真正开启数据分析之旅。记住：工具只是手段，<strong>把数据变成业务决策</strong> 才是最终目标。</p>''',
                'import numpy as np\nimport pandas as pd\nprint("NumPy:", np.__version__)\nprint("Pandas:", pd.__version__)\narr = np.array([1,2,3,4,5])\nprint("数组:", arr, "均值:", arr.mean())',
                [{'q':'Pandas 主要处理？','options':['图像数据','结构化表格数据','音频流','二进制'],'answer':1},
                 {'q':'安装 Pandas 用？','options':['pip install pandas','npm i pandas','apt pandas','gem pandas'],'answer':0},
                 {'q':'NumPy 相比 list 的优势？','options':['语法简单','向量化运算更快更省内存','支持任意对象','占用更多内存'],'answer':1},
                 {'q':'pip install numpy 命令的作用是？','options':['卸载 NumPy','安装 NumPy','更新 NumPy','测试 NumPy'],'answer':1},
                 {'q':'Anaconda 主要面向的用户群体？','options':['游戏开发者','数据科学初学者','Web 开发者','系统管理员'],'answer':1}],
                'import numpy as np\narr = np.array([10,20,30,40,50])\nprint("均值:", arr.mean())'),
            make_chapter(2, 'NumPy 数值计算', '25 分钟',
                '''<h3>一、NumPy 是什么？为什么它如此重要？</h3><p>NumPy（Numerical Python）是 Python 科学计算的基础设施。Pandas、Scikit-learn、Matplotlib、TensorFlow 等几乎所有数据科学库的底层都在使用 NumPy。它的核心数据结构是 <code>ndarray</code>（N-dimensional Array，多维数组），相比 Python 原生的 <code>list</code>，ndarray 有三大优势：</p><ul><li><strong>速度快 10-100 倍</strong>：底层用 C 实现，避免了 Python 循环的解释器开销</li><li><strong>内存更省</strong>：同类型数据紧凑存储，一个 100 万元素的数组只需约 4MB 内存</li><li><strong>向量化语法</strong>：用数学表达式代替循环，代码更简洁、更易读</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>NumPy 的核心思想是「向量化」——对整个数组做运算，而不是遍历每个元素。一旦你习惯了这种思维方式，Python 数据分析的大门就真正打开了。</div><h3>二、ndarray 的创建与属性</h3><h4>2.1 常见创建方式</h4><p>创建 ndarray 的方式主要有以下几种，各有适用场景：</p><table><thead><tr><th>方法</th><th>说明</th><th>示例</th></tr></thead><tbody><tr><td>np.array(list)</td><td>从 Python 列表转换</td><td><code>np.array([1,2,3,4,5])</code></td></tr><tr><td>np.zeros(shape)</td><td>全 0 数组</td><td><code>np.zeros((3,4))</code></td></tr><tr><td>np.ones(shape)</td><td>全 1 数组</td><td><code>np.ones((2,3))</code></td></tr><tr><td>np.arange(start, end, step)</td><td>等差序列</td><td><code>np.arange(0, 10, 2)</code></td></tr><tr><td>np.linspace(a, b, n)</td><td>n 个等距点</td><td><code>np.linspace(0, 1, 100)</code></td></tr><tr><td>np.random.randn(n)</td><td>标准正态随机数</td><td><code>np.random.randn(1000)</code></td></tr></tbody></table><h4>2.2 重要属性</h4><p>每个 ndarray 都有以下关键属性，理解它们是避免常见 bug 的关键：</p><ul><li><strong><code>.shape</code></strong>：数组的维度，例如 <code>(3, 4)</code> 表示 3 行 4 列的二维矩阵</li><li><strong><code>.ndim</code></strong>：维度的数量，标量为 0、向量为 1、矩阵为 2</li><li><strong><code>.dtype</code></strong>：数据类型，常见有 <code>int64</code>、<code>float64</code>、<code>bool</code></li><li><strong><code>.size</code></strong>：元素总数</li></ul><h3>三、核心操作：索引、切片与广播</h3><h4>3.1 索引与切片</h4><p>NumPy 的索引语法与 Python 列表类似，但更强大：</p><pre><code>arr = np.arange(12).reshape(3, 4)   # 创建 3x4 矩阵arr[0, 1]         # 第 0 行第 1 列元素arr[:, 1]         # 第 1 列所有行arr[1:3, :]       # 第 1-2 行所有列arr[arr > 5]      # 布尔索引：大于 5 的元素</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>布尔索引 <code>arr[condition]</code> 是数据分析中最常用的筛选手段。它的原理是：<code>condition</code> 会生成一个与 <code>arr</code> 同形状的布尔数组，然后用它来「遮盖」原数组，只保留 True 位置的元素。</div><h4>3.2 广播（Broadcasting）</h4><p>广播是 NumPy 最巧妙、最实用的特性。当两个数组形状不同但「兼容」时，NumPy 会自动扩展较小的数组来匹配较大的数组，从而避免显式循环：</p><pre><code>arr = np.array([[1, 2, 3], [4, 5, 6]])  # shape: (2, 3)arr + 10                                 # 标量广播到每个元素arr * np.array([10, 20, 30])             # 1D 广播到 2D 的每一行</code></pre><p>广播的规则可以概括为：从右往左比较维度长度，长度为 1 或缺省时可以自动扩展。</p><h3>四、常用统计与矩阵运算</h3><h4>4.1 聚合统计</h4><p>NumPy 提供了丰富的聚合函数，可以按整个数组或某个维度计算：</p><table><thead><tr><th>函数</th><th>说明</th><th>常见用法</th></tr></thead><tbody><tr><td>sum()</td><td>求和</td><td><code>arr.sum(axis=0)</code> 按列求和</td></tr><tr><td>mean()</td><td>均值</td><td><code>arr.mean()</code></td></tr><tr><td>std() / var()</td><td>标准差 / 方差</td><td><code>arr.std(ddof=1)</code> 样本标准差</td></tr><tr><td>min() / max()</td><td>最小 / 最大值</td><td><code>arr.max(axis=1)</code> 每行最大值</td></tr><tr><td>argmin() / argmax()</td><td>最小 / 最大值的索引</td><td><code>arr.argmax()</code></td></tr><tr><td>cumsum() / cumprod()</td><td>累计和 / 累计积</td><td><code>arr.cumsum()</code></td></tr></tbody></table><div class="warn-box"><strong>⚠ 注意事项：</strong>计算样本标准差/方差时，记得设置 <code>ddof=1</code>（Delta Degrees of Freedom），否则 NumPy 默认使用 <code>ddof=0</code>（总体方差），结果会比你预期的偏小。这是新手最常踩的坑之一。</div><h4>4.2 矩阵运算</h4><p>NumPy 支持完整的线性代数运算：</p><pre><code>A = np.array([[1, 2], [3, 4]])B = np.array([[5, 6], [7, 8]])A * B                    # 逐元素相乘（注意：不是矩阵乘法！）A @ B                    # 真正的矩阵乘法，等价于 np.dot(A, B)A.T                      # 转置np.linalg.inv(A)         # 逆矩阵np.linalg.eig(A)         # 特征值与特征向量</code></pre><h3>五、性能对比：NumPy vs Python 循环</h3><p>让我们用一个简单的实验来感受 NumPy 的威力。计算 100 万个随机数的平方和：</p><pre><code>import numpy as npimport time# Python 循环start = time.time()py_sum = sum(x**2 for x in range(1_000_000))print(f"Python: {time.time() - start:.4f}s")# NumPy 向量化start = time.time()np_sum = (np.arange(1_000_000) ** 2).sum()print(f"NumPy:  {time.time() - start:.4f}s")</code></pre><p>在普通笔记本上，Python 循环大约需要 0.15 秒，而 NumPy 只需要约 0.003 秒——<strong>50 倍的性能差距</strong>。对于更大规模的数据，差距会进一步扩大到数百倍。</p><h3>六、本章小结</h3><p>NumPy 是 Python 数据科学生态的基石。掌握它的<strong>向量化思维、索引与切片、广播机制、聚合统计</strong>，你就掌握了所有上层工具的底层原理。接下来学习 Pandas 时，你会发现很多概念是相通的——因为 Pandas 的 <code>Series</code> 和 <code>DataFrame</code> 本质上就是带有标签的 NumPy 数组。</p>''',
                'import numpy as np\na = np.arange(12).reshape(3,4)\nprint("矩阵:\\n", a)\nprint("按列均值:", a.mean(axis=0))\nprint("a * 2:\\n", a * 2)',
                [{'q':'np.zeros((3,4)) 形状？','options':['3元素','3列4行','3行4列','12行'],'answer':2},
                 {'q':'广播指的是？','options':['不同形状数组自动扩展后运算','手动复制','网络传输','压缩'],'answer':0},
                 {'q':'标准差用？','options':['std()','mean()','var()','sum()'],'answer':0},
                 {'q':'ndarray 的 .shape 属性返回什么？','options':['元素总数','维度数量','数组的形状元组','数据类型'],'answer':2},
                 {'q':'np.arange(0, 10, 2) 返回几个元素？','options':['2个','5个','10个','8个'],'answer':1},
                 {'q':'布尔索引 arr[arr > 5] 的作用是？','options':['修改大于5的元素','筛选大于5的元素','统计大于5的元素个数','删除大于5的元素'],'answer':1}],
                'import numpy as np\nm = np.array([[1,2,3],[4,5,6],[7,8,9]])\nprint("行均值:", m.mean(axis=1))'),
            make_chapter(3, 'Pandas 数据处理', '30 分钟',
                '''<h3>一、Pandas 是什么？与 NumPy 的关系</h3><p>Pandas 是 Python 生态中最强大的表格数据处理库。你可以把它想象成「Python 版的 Excel」——但比 Excel 强大得多。它的两个核心数据结构是：</p><ul><li><strong><code>Series</code></strong>：一维带标签的数组，类似于 Excel 中的一列数据</li><li><strong><code>DataFrame</code></strong>：二维带标签的表格，类似于 Excel 中的工作表</li></ul><p>与 NumPy 相比，Pandas 的关键差异在于「带标签」——每一行每一列都有明确的名称（而不仅仅是数字索引），这让数据分析变得直观得多。</p><div class="key-point"><strong>⭐ 核心要点：</strong>Pandas 是数据分析实际工作中<strong>使用频率最高</strong>的工具。一个经验数据：在典型的商务数据分析项目中，大约 70% 的代码是 Pandas 操作（读取、清洗、过滤、分组、合并），20% 是可视化，10% 是统计建模。</div><h3>二、数据读写：从多种来源获取数据</h3><p>Pandas 支持几乎所有常见的数据格式，这是它能成为「数据枢纽」的原因：</p><table><thead><tr><th>格式</th><th>读取方法</th><th>写入方法</th><th>典型场景</th></tr></thead><tbody><tr><td>CSV</td><td>pd.read_csv()</td><td>df.to_csv()</td><td>从系统导出、与人共享</td></tr><tr><td>Excel</td><td>pd.read_excel()</td><td>df.to_excel()</td><td>业务部门提供的报表</td></tr><tr><td>SQL</td><td>pd.read_sql()</td><td>df.to_sql()</td><td>从数据库直接取数</td></tr><tr><td>JSON</td><td>pd.read_json()</td><td>df.to_json()</td><td>API 返回的数据</td></tr><tr><td>Parquet</td><td>pd.read_parquet()</td><td>df.to_parquet()</td><td>大数据场景的高效格式</td></tr></tbody></table><h4>2.1 读取 CSV 的常见参数</h4><p>一个典型的 CSV 读取场景可能需要以下参数：</p><pre><code>df = pd.read_csv(    "sales_data.csv",    encoding="utf-8-sig",     # 处理中文 BOM    sep=",",                   # 分隔符（有些欧洲数据用 ;）    parse_dates=["日期"],      # 自动解析日期列    dtype={"订单号": str},     # 某些列强制为字符串    na_values=["NULL", "NA"]   # 识别缺失值标记)</code></pre><h3>三、核心操作：选择、过滤与修改</h3><h4>3.1 选择列与行</h4><p>Pandas 提供了两套索引器，功能各有分工：</p><ul><li><strong><code>df["列名"]</code></strong>：按列名选择一列，返回 Series</li><li><strong><code>df[["列1", "列2"]]</code></strong>：选择多列，返回 DataFrame</li><li><strong><code>df.loc[行标签, 列名]</code></strong>：按标签名称索引（最推荐）</li><li><strong><code>df.iloc[行位置, 列位置]</code></strong>：按整数位置索引</li></ul><div class="tip-box"><strong>💡 小技巧：</strong>99% 的场景下推荐使用 <code>.loc[]</code> 而不是 <code>df.列名</code> 这种简写。原因有三：（1）列名包含空格或中文时不会出错；（2）能同时指定行和列；（3）语义清晰，他人易读。</div><h4>3.2 条件过滤（布尔索引）</h4><p>过滤行是最常用的操作之一，语法简洁而强大：</p><pre><code># 单条件：销售额 > 1000df[df["销售额"] > 1000]# 多条件：销售额 > 1000 且 城市 == "北京"df[(df["销售额"] > 1000) & (df["城市"] == "北京")]# 使用 query 写法（更接近 SQL）df.query("销售额 > 1000 and 城市 == '北京'")# isin 多选：城市在北京、上海、广州之中df[df["城市"].isin(["北京", "上海", "广州"])]</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>Pandas 的条件组合要用 <code>&</code>（与）、<code>|</code>（或）、<code>~</code>（非），而不是 Python 原生的 <code>and</code>、<code>or</code>、<code>not</code>。并且每个条件<strong>必须用括号括起来</strong>，否则会因为运算符优先级导致难以调试的逻辑错误。</div><h4>3.3 添加/修改列</h4><pre><code># 直接赋值（最常见）df["客单价"] = df["销售额"] / df["订单数"]# 根据条件赋值df["高价值"] = np.where(df["销售额"] > df["销售额"].median(), "是", "否")# 更复杂的条件df["等级"] = pd.cut(    df["销售额"],    bins=[0, 1000, 5000, float("inf")],    labels=["低", "中", "高"])</code></pre><h3>四、分组聚合（Group By）：Pandas 最强大的功能</h3><p>「分组-应用-合并」（Split-Apply-Combine）是 Pandas 的精髓，对应 SQL 的 <code>GROUP BY</code>、Excel 的数据透视表：</p><pre><code># 基础用法：按城市分组，计算销售额的总和与均值df.groupby("城市")["销售额"].agg(["sum", "mean", "count"])# 多列分组 + 多指标聚合result = df.groupby(["城市", "品类"]).agg(    总销售额=("销售额", "sum"),    平均单价=("客单价", "mean"),    订单数=("订单ID", "nunique")).round(2)# transform：保持原始行数，常用于「组内标准化」df["组内均值"] = df.groupby("城市")["销售额"].transform("mean")df["组内偏差"] = df["销售额"] - df["组内均值"]</code></pre><h3>五、合并与连接：多表操作</h3><p>Pandas 提供了多种合并方式，对应关系型数据库的 JOIN 操作：</p><table><thead><tr><th>方法</th><th>功能</th><th>对应 SQL</th></tr></thead><tbody><tr><td>pd.merge(a, b, on="key")</td><td>按键列连接（最常用）</td><td>JOIN</td></tr><tr><td>pd.concat([a, b])</td><td>纵向堆叠 / 横向拼接</td><td>UNION ALL / 多列并排</td></tr><tr><td>df.join(other)</td><td>按索引连接</td><td>JOIN（按主键）</td></tr></tbody></table><pre><code># 左连接：保留左侧表的所有行orders = pd.merge(users, orders, left_on="用户ID", right_on="uid", how="left")# 纵向堆叠：把多个月的数据拼在一起all_data = pd.concat([jan_data, feb_data, mar_data], ignore_index=True)# 注意：ignore_index=True 会重置索引，避免重复的 0,1,2...</code></pre><h3>六、常见操作速查表</h3><table><thead><tr><th>目标</th><th>推荐写法</th></tr></thead><tbody><tr><td>查看基本信息</td><td><code>df.info()</code></td></tr><tr><td>查看统计摘要</td><td><code>df.describe(include="all")</code></td></tr><tr><td>每列缺失值数量</td><td><code>df.isnull().sum()</code></td></tr><tr><td>去重后的唯一值</td><td><code>df["城市"].unique()</code></td></tr><tr><td>各类计数</td><td><code>df["城市"].value_counts()</code></td></tr><tr><td>按列排序</td><td><code>df.sort_values("销售额", ascending=False)</code></td></tr><tr><td>重命名列</td><td><code>df.rename(columns={"old": "new"})</code></td></tr><tr><td>删除列</td><td><code>df.drop(columns=["不需要的列"])</code></td></tr><tr><td>删除缺失值所在行</td><td><code>df.dropna(subset=["销售额"])</code></td></tr><tr><td>填充缺失值</td><td><code>df["列"].fillna(df["列"].median())</code></td></tr></tbody></table><h3>七、本章小结</h3><p>Pandas 的功能非常丰富，掌握它需要「<strong>在做中学</strong>」。本章的核心内容可以概括为一张清单：<strong>数据读写 → 选择与过滤 → 新增列 → 分组聚合 → 多表合并</strong>。只要熟练掌握这五个操作，你就能独立完成 90% 以上的商务数据分析任务。建议配合课程项目反复练习，形成肌肉记忆。</p>''',
                'import pandas as pd\ndf = pd.DataFrame({"产品":["A","B","A","B"],"销量":[100,200,150,250]})\nprint(df.groupby("产品")["销量"].sum())',
                [{'q':'读 CSV 用？','options':['pd.read_csv','pd.load_csv','pd.open_csv','csv.read'],'answer':0},
                 {'q':'按列聚合求和？','options':['df.groupby("col").sum()','df.sum.by("col")','df.sum("col")','sum(df.col)'],'answer':0},
                 {'q':'删除缺失值？','options':['df.dropna()','df.nan()','df.clean()','df.rm()'],'answer':0},
                 {'q':'df.loc 和 df.iloc 的主要区别是？','options':['没有区别','loc按标签，iloc按位置','loc按位置，iloc按标签','仅适用于行'],'answer':1},
                 {'q':'读取 Excel 文件需要哪个库？','options':['openpyxl 或 xlrd','json库','xml库','yaml库'],'answer':0},
                 {'q':'value_counts() 的作用是？','options':['计算均值','计算总和','统计各值出现次数','删除重复'],'answer':2}],
                'import pandas as pd\ndf = pd.DataFrame({"类别":["X","Y","X","Y"],"金额":[10,20,30,40]})\nprint(df.groupby("类别")["金额"].sum())'),
            make_chapter(4, '数据清洗实战', '25 分钟',
                '''<h3>一、为什么数据清洗如此重要？</h3><p>在数据分析行业有一句广为流传的话：「<strong>Garbage in, garbage out</strong>（垃圾进，垃圾出）」。无论你的分析方法多么巧妙、模型多么强大，如果输入的数据本身存在严重质量问题，得出的结论必然是误导性的。</p><p>数据清洗通常占据一个数据分析师 <strong>50%~80%</strong> 的工作时间。听起来很枯燥，但它是一切有价值洞察的前提。</p><div class="key-point"><strong>⭐ 核心要点：</strong>数据质量问题有多种表现形式，但可以归纳为四大类：<strong>缺失值、重复值、异常值、类型不一致</strong>。掌握这四类问题的识别与处理方法，就能应对 95% 的清洗场景。</div><h3>二、数据质量诊断：先看清问题再动手</h3><p>在开始清洗之前，必须先对数据做全面「体检」。推荐使用以下 Pandas 诊断命令：</p><pre><code>df.info()                         # 查看各列数据类型与非空数量
df.describe(include="all")        # 数值列统计 + 类别列概览
df.isnull().sum()                 # 每列缺失值数量
df.duplicated().sum()             # 完全重复行的数量
df["关键列"].value_counts()       # 某列的取值分布
df.head(20)                       # 人工抽样观察</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>在 Jupyter Notebook 中，可以用 <code>df.sample(n=20)</code> 随机抽取 20 行进行肉眼检查，这比只看 <code>df.head()</code>（前 20 行）更容易发现随机分布的问题。</div><h3>三、缺失值处理：删除还是填充？</h3><p>缺失值是最常见的数据质量问题。处理策略主要有三类：</p><table><thead><tr><th>策略</th><th>方法</th><th>适用场景</th><th>注意事项</th></tr></thead><tbody><tr><td><strong>直接删除</strong></td><td>df.dropna()</td><td>缺失占比 &lt; 5% 且随机分布</td><td>避免删除过多样本导致偏差</td></tr><tr><td><strong>统计填充</strong></td><td>fillna(mean/median)</td><td>数值列的少量缺失</td><td>中位数对异常值更稳健</td></tr><tr><td><strong>业务填充</strong></td><td>fillna(0/"未知")</td><td>缺失本身有业务含义</td><td>需与业务方对齐理解</td></tr><tr><td><strong>模型预测</strong></td><td>KNN/回归插补</td><td>缺失模式有规律</td><td>复杂度高，慎用</td></tr></tbody></table><pre><code># 判断每列缺失比例
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
print(missing_pct.sort_values(ascending=False))

# 数值列用中位数填充
for col in df.select_dtypes(include=[np.number]).columns:
    df[col] = df[col].fillna(df[col].median())

# 类别列用众数填充或标记为"未知"
df["城市"] = df["城市"].fillna(df["城市"].mode()[0])
df["产品类别"] = df["产品类别"].fillna("未知")</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>不要不加思考地对所有列使用 <code>fillna(0)</code>。0 在数值列中可能被误认为是真实值（例如销售额为 0 意味着没有交易），从而扭曲统计结果。一定要结合业务含义来选择填充策略。</div><h3>四、重复值处理</h3><p>重复值可能来自系统导出错误、多次导入、合并操作不当等。识别和处理方式：</p><pre><code># 查看完全重复的行
print("完全重复行数:", df.duplicated().sum())

# 基于特定关键字段判断重复
print("订单号重复:", df.duplicated(subset=["订单号"]).sum())

# 删除重复行（保留第一次出现的）
df_clean = df.drop_duplicates()

# 删除重复行（基于关键字段）
df_clean = df.drop_duplicates(subset=["订单号"], keep="first")</code></pre><h3>五、异常值识别与处理</h3><p>异常值（Outlier）会严重扭曲均值、标准差等统计量，必须谨慎处理。常用识别方法：</p><h4>5.1 IQR 方法（箱线图原理）</h4><p>四分位距（Interquartile Range）是最常用、最稳健的异常值检测方法：</p><pre><code>Q1 = df["销售额"].quantile(0.25)
Q3 = df["销售额"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR    # 下界
upper = Q3 + 1.5 * IQR    # 上界

outliers = df[(df["销售额"] < lower) | (df["销售额"] > upper)]
print(f"异常值数量: {len(outliers)} (占比 {len(outliers)/len(df):.2%})")</code></pre><h4>5.2 3σ 原则（正态分布假设）</h4><p>如果数据近似正态分布，那么超出均值 ±3 倍标准差范围的观测值可视为异常（约占 0.3%）。</p><h4>5.3 异常值的处理策略</h4><ul><li><strong>直接删除</strong>：确认是录入错误或测试数据时使用</li><li><strong>截断（Winsorize）</strong>：将超出上下界的值替换为边界值，保留样本</li><li><strong>分箱处理</strong>：将数值转换为分位数区间，降低极端值影响</li><li><strong>保留不处理</strong>：如果异常值是真实业务现象（如双十一爆量），应该保留并单独分析</li></ul><h3>六、数据类型与一致性</h3><p>新手常忽视的问题是数据类型错误，例如：</p><ul><li>日期列被读取为字符串 object，而不是 datetime64</li><li>金额列因包含逗号或人民币符号被读取为字符串</li><li>订单号等编码字段被读取为整数（导致前导零丢失）</li></ul><pre><code># 日期类型转换
df["日期"] = pd.to_datetime(df["日期"], errors="coerce")

# 金额列清洗（去除 ¥ 和逗号）
df["金额"] = df["金额"].str.replace("¥", "").str.replace(",", "").astype(float)

# 订单号保持为字符串
df["订单号"] = df["订单号"].astype(str)

# 类别列优化为 category 类型（节省内存）
for col in ["城市", "品类", "渠道"]:
    df[col] = df[col].astype("category")</code></pre><h3>七、完整清洗流程示例</h3><p>一个标准的数据清洗流程如下：</p><pre><code># 1. 读取数据
df = pd.read_csv("raw_sales.csv")

# 2. 诊断
print("原始行数:", len(df))
print("缺失情况:\n", df.isnull().sum())
print("重复行数:", df.duplicated().sum())

# 3. 去重
df = df.drop_duplicates()

# 4. 缺失值处理
df["销售额"] = df["销售额"].fillna(df["销售额"].median())
df["城市"] = df["城市"].fillna("未知")

# 5. 类型矫正
df["日期"] = pd.to_datetime(df["日期"], errors="coerce")

# 6. 异常值处理
Q1, Q3 = df["销售额"].quantile([0.25, 0.75])
IQR = Q3 - Q1
df = df[(df["销售额"] >= Q1 - 1.5*IQR) & (df["销售额"] <= Q3 + 1.5*IQR)]

# 7. 输出清洗后数据
print("清洗后行数:", len(df))
df.to_csv("clean_sales.csv", index=False)</code></pre><h3>八、本章小结</h3><p>数据清洗不是一次性的「大扫除」，而是每次分析前都要执行的<strong>标准流程</strong>。记住四个字：<strong>「望、闻、问、切」</strong>——先用 <code>info/describe/sample</code> 望诊数据，再用缺失值和重复值分析「闻」出问题，「问」业务方确认含义，最后用「切」的方法动手清洗。清洗之后，你的分析结论才能真正让人信服。</p>''',
                'import pandas as pd, numpy as np\ndf = pd.DataFrame({"id":[1,2,3,3],"age":[20,np.nan,30,30]})\nprint(df.drop_duplicates().fillna(df.age.mean()))',
                [{'q':'检测重复？','options':['df.duplicated()','df.dup()','dup(df)','find.dup'],'answer':0},
                 {'q':'IQR = ?','options':['max-min','Q3-Q1','均值-中位数','std*2'],'answer':1},
                 {'q':'转为日期？','options':['pd.to_datetime','as_date','convert.date','date()'],'answer':0}],
                'import pandas as pd, numpy as np\ndf = pd.DataFrame({"n":["a","b","a"],"s":[1,np.nan,3]})\nprint(df.fillna(df.s.mean()))'),
            make_chapter(5, '综合案例：销售分析', '30 分钟',
                '''<h3>一、案例背景：从原始数据到业务洞察</h3><p>假设你是一家零售公司的数据分析师，业务负责人给你一份 90 天的销售明细数据，要求你在 1 小时内给出一份销售现状分析报告。这是商务数据分析中最经典的场景——时间紧、数据杂、结论要能落地。</p><p>我们将按照「<strong>读取 → 诊断 → 清洗 → 日期解析 → 多维聚合 → 结论输出</strong>的标准流程完成分析。</p><div class="key-point"><strong>⭐ 核心要点：</strong>一个优秀的数据分析不是代码有多复杂，而是能否在有限时间内提炼出业务关心的结论。记住：<strong>「什么时间维度看趋势、品类维度看结构、区域维度看分布</strong>」——三个维度交叉分析是销售分析的「黄金三角。</div><h3>二、步骤 1：数据读取与快速诊断</h3><pre><code>import pandas as pd
import numpy as np

# 模拟一份 90 天、3 个城市、5 个品类的销售数据
dates = pd.date_range("2024-01-01", periods=90, freq="D")
df = pd.DataFrame({
    "日期": np.repeat(dates, 15),
    "城市": np.tile(np.repeat(["北京", "上海", "广州"], 5), 30),
    "品类": np.tile(["电子", "服装", "食品", "家居", "美妆"], 54),
    "销售额": np.random.randint(500, 8000, 1350),
    "数量": np.random.randint(1, 20, 1350)
})

# 快速诊断
print("数据形状:", df.shape)
print("\n基本信息:")
df.info()
print("\n数值摘要:")
print(df.describe())</code></pre><h3>三、步骤 2：日期解析与时间维度</h3><p>日期是销售分析中最重要的维度。必须把日期字段解析后，我们可以按日、周、月等多种粒度进行聚合：</p><pre><code>df["日期"] = pd.to_datetime(df["日期"])
df["月份"] = df["日期"].dt.to_period("M")
df["周"] = df["日期"].dt.isocalendar().week.astype(int)
df["星期"] = df["日期"].dt.dayofweek.map({0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"})
df["是否周末"] = df["星期"].isin(["周六", "周日"])

# 按日汇总
daily = df.groupby("日期")["销售额"].sum()

# 按月汇总
monthly = df.groupby("月份")["销售额"].sum()

# 计算环比增长率
monthly_pct = monthly.pct_change() * 100
print("月度销售额及环比增长率:")
result = pd.DataFrame({"销售额": monthly, "环比%": monthly_pct.round(2))
print(result)</code></pre><h3>四、步骤 3：品类结构分析</h3><p>品类分析的核心问题是：<strong>各品类的销售贡献是否均衡，谁在增长、谁在衰退。</p><pre><code># 品类总销售额
by_category = df.groupby("品类").agg(
    总销售额=("销售额", "sum"),
    平均单价=("销售额", "mean"),
    订单数=("销售额", "count")
).round(2)

by_category = by_category.sort_values("总销售额", ascending=False)
by_category["占比%"] = (by_category["总销售额"] / by_category["总销售额"].sum() * 100).round(2)

print("品类销售贡献:")
print(by_category)

# 品类 x 月份交叉分析（透视表）
pivot = df.pivot_table(
    index="月份",
    columns="品类",
    values="销售额",
    aggfunc="sum",
    fill_value=0,
    margins=True,
    margins_name="合计"
)
print("\n月度 x 品类透视表:")
print(pivot.round(0))</code></pre><h3>五、步骤 4：城市维度与多维度组合分析</h3><pre><code># 城市 x 品类交叉
cross = df.pivot_table(
    index="城市",
    columns="品类",
    values="销售额",
    aggfunc="sum",
    fill_value=0
)

# 计算客单价
df["客单价"] = df["销售额"] / df["数量"]

# 各城市的客单价均值
city_avg = df.groupby("城市")["客单价"].mean().round(2)
print("各城市客单价:")
print(city_avg.sort_values(ascending=False))

# 工作日 vs 周末对比
weekend_vs_weekday = df.groupby("是否周末")["销售额"].agg(["sum", "mean", "count"])
print("\n周末 vs 工作日:")
print(weekend_vs_weekday)</code></pre><h3>六、步骤 5：输出业务结论</h3><p>分析不是目的，<strong>给出行动建议才是价值</strong>。将以上数据转换为业务可以直接使用的表格：</p><pre><code># 汇总关键指标
total_sales = df["销售额"].sum()
avg_daily = df.groupby("日期")["销售额"].sum().mean()
top_category = by_category.index[0]
top_city = df.groupby("城市")["销售额"].sum().idxmax()

print("=" * 50)
print("📊 销售分析报告")
print("=" * 50)
print(f"分析周期: {df['日期'].min().date()} 至 {df['日期'].max().date()}")
print(f"总销售额: ¥{total_sales:,.0f}")
print(f"日均销售额: ¥{avg_daily:,.0f}")
print(f"销售最高品类: {top_category} (¥{by_category.loc[top_category, '总销售额']:,.0f)
print(f"销售最高城市: {top_city}")
print(f"客单价: ¥{df['客单价'].mean():,.2f}")
print("=" * 50)
</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>在真实工作场景中，建议将分析结果整理为「<strong>一个总览 + 三张关键图（趋势图 + 结构图 + 排名表</strong>」的结构。业务方通常只需 3 分钟就能读完。</div><h3>七、常见错误与最佳实践</h3><ul><li><strong>忘记设置日期索引</strong>：做时间序列分析前，一定要把日期列设为索引（<code>df.set_index("日期")</code>），否则 <code>resample</code>、<code>rolling</code> 等时间相关函数才能正常工作。</li><li><strong>忽略季节性</strong>：月度对比中，不要只看本月 vs 上月，还要对比去年同月（同比），因为销售数据有很强的季节性（春节、暑假、双十一等）。</li><li><strong>只看绝对值</strong>：一定要计算占比和增长率，绝对值无法判断规模变化。</li><li><strong>未去重</strong>：如果数据中存在重复订单，总销售额会被高估。</li></ul><h3>八、本章小结</h3><p>本章我们用一个完整的销售分析案例，将前面四章的知识点串联起来：<strong>Pandas 读写 → 数据诊断 → 日期解析 → 分组聚合 → 透视表 → 业务结论</strong>。这就是一个数据分析师每天的工作内容——看似简单的工具组合，却能产出高价值的业务洞察。建议你可以用自己公司的真实数据替换示例数据，重复一遍这个流程，你会发现数据分析真正入门。</p>''',
                'import pandas as pd, numpy as np\nidx = pd.date_range("2024-01-01", periods=30)\ndf = pd.DataFrame({"日期": np.repeat(idx,3), "类别": np.tile(["A","B","C"],30), "销售额": np.random.randint(1000,5000,90)})\nprint(df.groupby("类别")["销售额"].sum().sort_values(ascending=False))',
                [{'q':'30 个连续日期用？','options':['pd.date_range','pd.range','pd.period','np.dates'],'answer':0},
                 {'q':'聚合 sum/mean/count 同时算？','options':['.agg(["sum","mean","count"])','.all()','.multi()','.stats()'],'answer':0},
                 {'q':'排序默认？','options':['升序','降序','随机','不排序'],'answer':0}],
                'import pandas as pd, numpy as np\nnp.random.seed(0)\ndf = pd.DataFrame({"c": np.tile(["A","B","C"], 20), "v": np.random.randint(10,100,60)})\nprint(df.groupby("c").v.agg(["sum","mean","max"]))'),
        ]
    },
    2: {
        'id': 2, 'title': 'Pandas 高级数据分析', 'icon': '📊',
        'color': '#e67e22', 'level': '进阶',
        'description': '分组、透视、合并、窗口函数——进阶 Pandas。',
        'chapters': [
            make_chapter(1, 'Groupby 深度', '25 分钟',
                '''<h3>一、理解 Group By 的底层原理</h3><p>Hadley Wickham（ggplot2、tidyverse 的作者）在 2011 年提出了「Split-Apply-Combine」（拆分-应用-合并）的数据分析范式。这一思想深刻影响了 Pandas 的设计，也成为所有数据分析师必须掌握的核心思维模型。</p><p>它的执行过程分为三步：</p><ul><li><strong>Split（拆分）</strong>：按照一个或多个关键字段将数据切成若干组（Groups）</li><li><strong>Apply（应用）</strong>：对每个组独立执行某种计算（求和、均值、排名、转换、过滤等）</li><li><strong>Combine（合并）</strong>：将各组的计算结果重新拼成一张表</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Group By 不只是「<strong>分组求和</strong>」那么简单。它实际上是一种通用的「分而治之」策略，可以实现聚合、转换、过滤、自定义操作四种核心模式。</div><h3>二、四种 Group By 操作模式</h3><h4>2.1 聚合（Aggregation）：缩小行数</h4><p>聚合是最常见的用法。每组输出一行汇总结果，行数从 N 行缩小到 K 组。</p><table><thead><tr><th>方式</th><th>功能</th><th>示例</th></tr></thead><tbody><tr><td>单函数</td><td>对每组所有数值列统一应用</td><td><code>df.groupby("城市").sum()</code></td></tr><tr><td>多函数</td><td>同时应用多种统计方法</td><td><code>df.groupby("城市")["销售额"].agg(["sum", "mean", "count"])</code></td></tr><tr><td>命名字典</td><td>对不同列应用不同函数并命名</td><td><code>df.groupby("城市").agg(总销售=("销售额","sum"), 均价=("单价","mean"))</code></td></tr></tbody></table><pre><code># 最灵活的命名聚合语法（Pandas 0.25+ 支持）result = df.groupby(["城市", "品类"]).agg(    总销售额=("销售额", "sum"),    平均单价=("单价", "mean"),    订单数=("订单ID", "nunique"),    最高单客=("客户ID", "nunique"),    销售标准差=("销售额", lambda x: x.std(ddof=1))).round(2)# 结果排序result = result.sort_values("总销售额", ascending=False)</code></pre><h4>2.2 转换（Transformation）：保持原行数</h4><p>转换（transform）与聚合最关键的区别在于：<strong>它不缩小行数，而是为每一行附加组级别的统计信息。</strong>这在「组内标准化」「对比均值」「相对排名」等场景中特别有用。</p><pre><code># 为每一行附加「所在城市的平均销售额」df["城市均销"] = df.groupby("城市")["销售额"].transform("mean")# 计算每行与其所在组均值的偏差（常用于识别组内异常）df["组内偏差"] = df["销售额"] - df["城市均销"]# 组内排名（每个城市内部按销售额排名）df["城市内排名"] = df.groupby("城市")["销售额"].rank(ascending=False, method="dense")# 组内归一化（Min-Max 标准化到 0-1 区间）def min_max_norm(x):    return (x - x.min()) / (x.max() - x.min()) if x.max() != x.min() else 0df["组内归一化"] = df.groupby("城市")["销售额"].transform(min_max_norm)</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>当你发现自己在写 <code>for group_name, group_df in df.groupby("城市"):</code> 循环时，先问自己两个问题：（1）能否用 <code>.agg()</code> 或 <code>.transform()</code> 替代？（2）操作的输出是「一行一组」还是「与原表同长」？几乎所有场景都能找到非循环的向量化写法，性能通常提升 10-100 倍。</div><h4>2.3 过滤（Filtering）：删除整组</h4><p>filter 用于「基于组级条件删除整个组」，例如「删除总销售额不足 1 万元的城市」——它的输出是原始粒度的行，但只保留满足条件的那些组。</p><pre><code># 只保留总销售额 > 100000 的城市数据filtered = df.groupby("城市").filter(lambda g: g["销售额"].sum() > 100000)# 只保留样本量 > 30 的组（避免小样本造成的统计偏差）filtered = df.groupby("品类").filter(lambda g: len(g) > 30)</code></pre><h4>2.4 自定义应用（Apply）：万能但慢</h4><p>当以上三种模式都无法满足需求时，可以使用 <code>apply</code> 传入任意 Python 函数。它最灵活，但速度最慢（逐组调用 Python 函数，无法享受到 C 优化）。</p><pre><code># 自定义：每组取销售额前 20% 的行def top20_percent(group):    threshold = group["销售额"].quantile(0.8)    return group[group["销售额"] >= threshold]top_rows = df.groupby("城市", group_keys=False).apply(top20_percent)# 注意：Pandas 2.2+ 建议显式设置 group_keys=False 避免索引冲突</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>不要在 <code>apply</code> 中做简单的聚合操作。如果你发现自己写的是 <code>df.groupby(...).apply(lambda g: g["销售额"].sum())</code>，请立即改为 <code>df.groupby(...)["销售额"].sum()</code>——速度差 5-50 倍。只有当输出结构复杂时才应使用 apply。</div><h3>三、多级索引（MultiIndex）与分组</h3><p>按多个字段分组会产生多级索引（MultiIndex），处理方式如下：</p><pre><code># 按城市 x 品类分组，产生 MultiIndexmulti = df.groupby(["城市", "品类"])["销售额"].sum()# 查看索引print("索引层级:", multi.index.names)# 选择特定城市print(multi.loc["北京"])# 重置索引为普通列，方便进一步操作flat = multi.reset_index(name="总销售额")# 排序：先按城市，再按销售额倒序flat = flat.sort_values(["城市", "总销售额"], ascending=[True, False])</code></pre><h3>四、性能优化与最佳实践</h3><ul><li><strong>优先 agg，其次 transform，最后 apply</strong>：按性能优先级选择</li><li><strong>groupby 后先选择列再操作</strong>：<code>df.groupby("城市")["销售额"].sum()</code> 比 <code>df.groupby("城市").sum()["销售额"]</code> 快得多（避免对无关列计算）</li><li><strong>用 category 类型优化分组键</strong>：字符串列转 <code>category</code> 后分组性能可提升 2-3 倍</li><li><strong>大型数据用 sort=False</strong>：<code>groupby(key, sort=False)</code> 可以跳过结果排序，节省时间</li><li><strong>避免 in-place 修改</strong>：尽量链式调用产生新对象，避免 SettingWithCopyWarning</li></ul><h3>五、本章小结</h3><p>Group By 的四种模式——<strong>聚合、转换、过滤、自定义应用</strong>——覆盖了数据分析中 90% 以上的「分而治之」需求。记住一句话：能 agg 不 transform，能 transform 不 apply。理解这句话，你就真正掌握了 Pandas 的精髓。</p>''',
                'import pandas as pd, numpy as np\ndf = pd.DataFrame({"g": list("AABBCAABBC"), "v": [10,20,15,30,25,12,18,28,22,35]})\nprint(df.groupby("g").v.agg(["sum","mean","count"]))',
                [{'q':'同时 sum/mean？','options':['.agg(["sum","mean"])','.multi()','.sum_mean()','df.stats()'],'answer':0},
                 {'q':'transform 与 agg 区别？','options':['无区别','transform 返回与原表同长度','transform 更快','transform 只做一次'],'answer':1},
                 {'q':'按组筛选行？','options':['.filter()','.where()','.drop()','.select()'],'answer':0}],
                'import pandas as pd, numpy as np\nnp.random.seed(0)\ndf = pd.DataFrame({"g": np.random.choice(["X","Y","Z"],100), "v": np.random.randn(100)*10+50})\nprint(df.groupby("g").v.agg(["count","sum","mean","std"]))'),
            make_chapter(2, '合并与连接', '25 分钟',
                '''<h3>一、为什么需要多表合并？</h3><p>真实业务场景中，数据很少整齐地放在一张表里。常见的拆分方式包括：</p><ul><li><strong>按主题拆分</strong>：用户表、订单表、商品表、门店表</li><li><strong>按时间拆分</strong>：2024-01.csv、2024-02.csv……</li><li><strong>按系统拆分</strong>：CRM 数据、ERP 数据、物流系统数据</li></ul><p>数据分析师 50% 以上的工作都在处理「把多张表拼在一起」。Pandas 提供了三套核心工具：<strong>merge、join、concat</strong>，分别对应不同场景。</p><div class="key-point"><strong>⭐ 核心要点：</strong>记住一个简单的决策规则——<strong>按关键字段横向拼接用 merge，按索引横向拼接用 join，纵向堆叠用 concat</strong>。理解它们的区别，你就能处理 99% 的多表操作。</div><h3>二、Merge：SQL JOIN 的 Pandas 版本</h3><h4>2.1 四种连接类型（how 参数）</h4><table><thead><tr><th>类型</th><th>含义</th><th>典型场景</th></tr></thead><tbody><tr><td>inner（默认）</td><td>只保留两边都匹配的行</td><td>取交集，最严谨</td></tr><tr><td>left</td><td>保留左表全部，右表未匹配处填 NaN</td><td>以订单表为主，关联用户信息</td></tr><tr><td>right</td><td>保留右表全部，左表未匹配处填 NaN</td><td>以用户表为主，看其是否有订单</td></tr><tr><td>outer</td><td>保留两边全部，未匹配处填 NaN</td><td>全量合并，不丢失任何信息</td></tr></tbody></table><h4>2.2 基本用法</h4><pre><code># 最常用：两表通过共同字段连接orders = pd.merge(users, orders, on="用户ID", how="left")# 左右表字段名不同时orders = pd.merge(    users, orders,    left_on="用户ID",      # 左表字段名    right_on="uid",         # 右表字段名    how="left")# 多字段连接（最安全的方式，避免重复匹配）sales = pd.merge(    daily_sales, product_info,    left_on=["日期", "SKU"],    right_on=["日期", "SKU"],    how="inner")# 连接后检查：行数变化 & 缺失值print(f"连接前行数: {len(users)} → 连接后: {len(orders)}")print("新产生的缺失:")print(orders[["用户姓名", "订单金额"]].isnull().sum())</code></pre><h4>2.3 连接中的常见陷阱</h4><div class="warn-box"><strong>⚠ 注意事项（1）：重复键导致行数膨胀。</strong>如果连接键在右表不唯一（例如一个用户有多个订单），连接后的行数会超过左表。这不是 bug，而是预期行为——但如果你的意图是「给左表加一列信息」，一定要先确认右表的键是否唯一。检查方法：<code>right_df[key].duplicated().sum()</code>。</div><div class="warn-box"><strong>⚠ 注意事项（2）：字段名冲突。</strong>如果两表存在重名字段，merge 会自动加上 <code>_x</code>、<code>_y</code> 后缀（如 <code>created_at_x</code>、<code>created_at_y</code>）。强烈建议使用 <code>suffixes=("_用户表", "_订单表")</code> 参数给它们加上有业务含义的后缀。</div><h3>三、Concat：纵向堆叠与横向并排</h3><h4>3.1 纵向堆叠（最常用）</h4><p>当你的数据按月份或按部门分散在多个 CSV/Sheet 中，纵向堆叠是第一选择：</p><pre><code># 手动堆叠 2-3 个文件combined = pd.concat([jan_data, feb_data, mar_data], ignore_index=True)# 批量读取 + 堆叠（推荐写法）import globfiles = sorted(glob.glob("sales_2024-*.csv"))dfs = [pd.read_csv(f) for f in files]all_data = pd.concat(dfs, ignore_index=True)# 高级：加一列来源标识，便于后续追溯dfs = []for f in files:    tmp = pd.read_csv(f)    tmp["来源文件"] = f    dfs.append(tmp)all_data = pd.concat(dfs, ignore_index=True)print(f"合并了 {len(dfs)} 个文件，总 {len(all_data)} 行")</code></pre><h4>3.2 横向并排（较少用，但要懂）</h4><p>当你有结构相同但内容互补的两张表（例如一张放销售指标、一张放用户指标），可以 <code>axis=1</code> 横向拼接：</p><pre><code># 注意：横向拼接依赖索引对齐，必须确保两张表的行顺序和数量完全一致！# 不推荐用 axis=1，更推荐用 merge 按关键键连接side_by_side = pd.concat([sales_metrics, user_metrics], axis=1)</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>使用 <code>pd.concat()</code> 纵向堆叠时，记得加上 <code>ignore_index=True</code>，否则每段数据的索引会保持原值（0,1,2...0,1,2...），后续 <code>.loc[0]</code> 会取出多行。如果你需要保留原始位置标识，用 <code>keys=["Jan","Feb","Mar"]</code> 参数添加层级索引。</div><h3>四、Join：按索引的简化版 Merge</h3><p><code>df.join()</code> 本质是基于索引的 <code>merge</code> 简化版。它在以下场景最方便：</p><pre><code># 把索引设为日期后，join 可以非常自然地拼接daily_idx = daily_sales.set_index("日期")daily_idx2 = daily_users.set_index("日期")combined = daily_idx.join(daily_idx2, how="inner")</code></pre><h3>五、大型数据的合并优化策略</h3><ul><li><strong>先筛选再合并</strong>：先对右表做 <code>df[df["日期"].isin(need_dates)]</code> 缩小内存占用</li><li><strong>选择正确的连接类型</strong>：需要左表全量就用 left，不要用 inner 然后再补数据</li><li><strong>检查键的唯一性</strong>：<code>df[key].is_unique</code> 返回 True 时连接可预期</li><li><strong>category 类型键</strong>：对字符串键列用 <code>.astype("category")</code> 节省内存并加速</li><li><strong>超大数据用分区</strong>：千万行以上数据建议分块处理，参考 <code>chunksize</code> 参数或 Dask</li></ul><h3>六、本章小结</h3><p>多表合并是数据分析师的基本功。一句话总结：<strong>横向按字段匹配用 merge，纵向堆叠用 concat，按索引对齐用 join</strong>。合并前后务必检查行数、键的唯一性和缺失值——看似简单的操作，往往是分析结果正确性的第一道防线。</p>''',
                'import pandas as pd\nusers = pd.DataFrame({"id":[1,2,3],"name":["A","B","C"]})\norders = pd.DataFrame({"uid":[1,1,2,3],"amt":[100,200,150,300]})\nprint(pd.merge(users, orders, left_on="id", right_on="uid", how="left"))',
                [{'q':'left join 保留？','options':['两表交集','左表全部，右表匹配不到为 NaN','右表全部','随机'],'answer':1},
                 {'q':'纵向堆叠？','options':['pd.concat([a,b])','pd.merge(a,b)','a+b','df.stack()'],'answer':0},
                 {'q':'merge 默认？','options':['left','right','inner','outer'],'answer':2}],
                'import pandas as pd\nL = pd.DataFrame({"k":["A","B","C"], "x":[1,2,3]})\nR = pd.DataFrame({"k":["A","B","D"], "y":[4,5,6]})\nprint(pd.merge(L, R, on="k", how="left"))'),
            make_chapter(3, '透视表与交叉表', '25 分钟',
                '''<h3>一、透视表：Excel 用户最熟悉的工具</h3><p>透视表（Pivot Table）是数据分析中使用频率最高的工具之一。Excel 用户几乎人人都会，但用 Pandas 做透视表有三大优势：可重复、可自动化、可嵌入分析流程。</p><p>Pandas 提供两个函数：<code>pivot_table</code>（通用透视表）和 <code>crosstab</code>（交叉表/频率表）。两者底层逻辑相似，但用法各有所长。</p><div class="key-point"><strong>⭐ 核心要点：</strong>透视表的本质是「<strong>二维 Group By + 多列展示</strong>」——行（index）× 列（columns）× 值（values）× 聚合方式（aggfunc），四个参数就定义了整张表。</div><h3>二、Pivot Table 详解</h3><h4>2.1 标准用法</h4><pre><code># 基础：行=城市，列=品类，值=销售额，聚合=求和
pivot = pd.pivot_table(
    df,
    index="城市",
    columns="品类",
    values="销售额",
    aggfunc="sum",
    fill_value=0           # 空单元格填充 0
).round(0)

# 同时输出行/列汇总
pivot_total = pd.pivot_table(
    df,
    index="城市",
    columns="品类",
    values="销售额",
    aggfunc="sum",
    margins=True,          # 添加汇总行/列
    margins_name="合计",
    fill_value=0
).round(0)

# 同时应用多种聚合方式
pivot_multi = pd.pivot_table(
    df,
    index=["城市", "渠道"],
    columns="品类",
    values=["销售额", "数量"],
    aggfunc={"销售额": "sum", "数量": "mean"},
    fill_value=0
)</code></pre><h4>2.2 多字段透视与多级索引</h4><p>当 index 或 columns 参数传入多个字段时，会产生多级索引（MultiIndex）：</p><pre><code># 行=城市×渠道，列=品类
pivot = pd.pivot_table(
    df,
    index=["城市", "渠道"],
    columns="品类",
    values="销售额",
    aggfunc="sum",
    fill_value=0
)

# 多级索引的选择方式
print(pivot.loc["北京"])               # 取北京所有渠道
print(pivot.loc[("北京", "线上")])     # 取北京-线上
print(pivot.xs("线上", level="渠道"))   # 跨城市取线上渠道</code></pre><h3>三、Crosstab：交叉表与频率分析</h3><p><code>crosstab</code> 专门用于计算两个（或多个）分类字段的交叉频率，非常适合做卡方检验的数据准备。</p><h4>3.1 计数与占比</h4><pre><code># 基础：城市 vs 品类的订单数量（计数）
ct = pd.crosstab(
    index=df["城市"],
    columns=df["品类"],
    margins=True,
    margins_name="合计"
)

# 行百分比：每行的百分比构成（加起来=100%）
ct_row_pct = pd.crosstab(
    index=df["城市"],
    columns=df["品类"],
    normalize="index",   # 按行归一化
    margins=True
).round(4) * 100

# 列百分比
ct_col_pct = pd.crosstab(
    index=df["城市"],
    columns=df["品类"],
    normalize="columns",  # 按列归一化
    margins=True
).round(4) * 100

# 全表百分比（占总样本）
ct_all_pct = pd.crosstab(
    index=df["城市"],
    columns=df["品类"],
    normalize="all"       # 全表归一化
).round(4) * 100</code></pre><h4>3.2 交叉表中聚合数值字段</h4><p>crosstab 不仅能计数，还能聚合数值：</p><pre><code># 城市 x 品类的平均销售额
ct_agg = pd.crosstab(
    index=df["城市"],
    columns=df["品类"],
    values=df["销售额"],
    aggfunc="mean",
    fill_value=0
).round(0)</code></pre><h3>四、实战：销售结构分析</h3><p>将以上工具组合起来，完成一个完整的销售结构分析案例：</p><pre><code># 1. 品类销售占比
by_cat = df.groupby("品类")["销售额"].sum()
cat_pct = (by_cat / by_cat.sum() * 100).round(1).sort_values(ascending=False)
print("品类占比:")
for cat, pct in cat_pct.items():
    print(f"  {cat}: {pct}%")

# 2. 城市 x 品类透视
pivot = pd.pivot_table(
    df, index="城市", columns="品类",
    values="销售额", aggfunc="sum", fill_value=0,
    margins=True, margins_name="合计"
).round(0)

# 3. 转化为行百分比结构（每行加起来=100）
pivot_pct = pivot.div(pivot["合计"], axis=0) * 100

# 4. 排序：按合计降序
pivot_pct = pivot_pct.sort_values("合计", ascending=False)
print("\n城市品类结构(%)：")
print(pivot_pct.round(1))</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>做结构分析时，同时展示「绝对值」和「百分比」两张表是最佳实践。绝对值告诉业务方规模，百分比告诉业务方结构。两者结合才能做出正确的业务判断（一个品类占比下降可能是绝对值上升但其他品类增长更快）。</div><h3>五、常见陷阱与最佳实践</h3><ul><li><strong>NaN 未填充</strong>：透视表中没有数据的交叉点默认为 NaN，记得用 <code>fill_value=0</code> 填充，否则求和会被遗漏。</li><li><strong>多级列名难以操作</strong>：透视表多级列名可用 <code>df.columns = df.columns.map('_'.join)</code> 展平成单级列名，方便后续筛选。</li><li><strong>忘记数据类型检查</strong>：透视前确保数值列是 numeric，避免出现「求和后变成字符串拼接」的诡异错误。</li><li><strong>过度透视</strong>：一张表里放超过 3 个维度的结果可读性极差，建议拆成多张透视表，逐步深入。</li></ul><h3>六、本章小结</h3><p>透视表和交叉表是商务数据分析中使用频率最高的工具之一。掌握 <code>pivot_table</code> 的四要素（行/列/值/聚合方式）和 <code>crosstab</code> 的三种归一化方法（index/columns/all），你就能快速产出高质量的结构分析报告。配合后续章节的可视化工具，可以直接生成业务方喜欢的图表 dashboard。</p>''',
                'import pandas as pd, numpy as np\nnp.random.seed(0)\ndf = pd.DataFrame({"地区": np.repeat(["华北","华东","华南"], 10), "产品": np.tile(["A","B","C","D","E"],6), "销量": np.random.randint(100,1000,30)})\nprint(df.pivot_table(index="地区", columns="产品", values="销量", aggfunc="sum", fill_value=0))',
                [{'q':'pivot_table 默认聚合？','options':['sum','count','mean','max'],'answer':2},
                 {'q':'增加行/列汇总？','options':['margins=True','total=True','sum=True','row_total=True'],'answer':0},
                 {'q':'crosstab 做？','options':['列联表/频率','时间序列','图像','导出'],'answer':0}],
                'import pandas as pd, numpy as np\nnp.random.seed(1)\ndf = pd.DataFrame({"渠道": np.repeat(["线上","线下"],20), "品类": np.tile(["甲","乙","丙","丁"],10), "金额": np.random.randint(1000,5000,40)})\nprint(df.pivot_table(index="渠道", columns="品类", values="金额", aggfunc="sum", margins=True))'),
            make_chapter(4, '时间序列', '30 分钟',
                '''<h3>一、时间序列分析为什么重要？</h3><p>时间序列（Time Series）是商务数据分析中最常见的数据形态之一——销售额、活跃用户数、库存水平、网站流量……几乎所有核心业务指标都天然带有时间属性。掌握时间序列分析，你就能回答：</p><ul><li><strong>趋势</strong>：业务整体是上升还是下降？</li><li><strong>季节性</strong>：周几/季度有明显波动？</li><li><strong>同比/环比</strong>：本月 vs 上月、本月 vs 去年同月？</li><li><strong>异常检测</strong>：哪些日期是离群点（节假日、促销、故障）？</li><li><strong>预测</strong>：未来一周/一月/一季度会怎样？</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Pandas 时间序列的精髓在于「<strong>把日期设为索引</strong>」——一旦设置 DatetimeIndex，就解锁了三大神器：<strong>resample</strong>（时间粒度重采样）、<strong>rolling</strong>（滚动窗口）、<strong>shift</strong>（平移对比）。</div><h3>二、第一步：把字符串日期转为日期类型</h3><h4>2.1 日期解析</h4><pre><code># 基本用法：字符串 → datetime64
df["日期"] = pd.to_datetime(df["日期"])

# 更安全的写法：指定格式，加快解析 + 避免歧义
df["日期"] = pd.to_datetime(
    df["日期"],
    format="%Y-%m-%d",   # 显式格式，比自动推断快数倍
    errors="coerce"      # 无法解析的转为 NaT（Not a Time）
)

# 检查转换后有多少解析失败
print(f"解析失败: {df['日期'].isna().sum()} 条")

# 设置为索引（解锁时间序列三大神器）
df = df.set_index("日期").sort_index()

# 直接按日期切片
print(df["2024-01":"2024-03"])     # 取 1-3 月
print(df.loc["2024-06-18"])         # 取特定日期</code></pre><h4>2.2 从日期中提取字段</h4><pre><code>df["年份"] = df.index.year
df["月份"] = df.index.month
df["周数"] = df.index.isocalendar().week.astype(int)
df["星期几"] = df.index.dayofweek.map({0:"周一",1:"周二",2:"周三",3:"周四",4:"周五",5:"周六",6:"周日"})
df["是否周末"] = df.index.dayofweek >= 5
df["季度"] = df.index.quarter
df["年月"] = df.index.to_period("M")</code></pre><h3>三、Resample：改变时间粒度</h3><p>resample 将数据从一种时间频率转换到另一种，例如「按日 → 按月聚合」或「按小时 → 按日汇总」。它本质上是「基于时间窗口的 Group By」。</p><h4>3.1 常见频率规则</h4><table><thead><tr><th>频率代码</th><th>含义</th><th>示例输出</th></tr></thead><tbody><tr><td>D</td><td>按日</td><td>2024-01-01, 2024-01-02...</td></tr><tr><td>W</td><td>按周</td><td>每周日/周一</td></tr><tr><td>M</td><td>按月（月末）</td><td>2024-01-31, 2024-02-29...</td></tr><tr><td>Q</td><td>按季度</td><td>2024-03-31, 2024-06-30...</td></tr><tr><td>Y</td><td>按年</td><td>2024-12-31...</td></tr><tr><td>H / T / S</td><td>小时 / 分钟 / 秒</td><td>细粒度数据</td></tr></tbody></table><h4>3.2 典型用法</h4><pre><code># 按日求和（最常见：订单数据 → 每日销售）
daily = df["销售额"].resample("D").sum()

# 按月聚合：同时计算多个指标
monthly = df.resample("M").agg(
    总销售=("销售额", "sum"),
    日均销售=("销售额", "mean"),
    最高日销=("销售额", "max"),
    订单数=("订单ID", "nunique"),
    活跃城市=("城市", "nunique")
).round(0)

# 按周聚合 + 百分比变化
weekly = df["销售额"].resample("W").sum()
weekly_pct = weekly.pct_change() * 100</code></pre><h3>四、Rolling：滚动窗口计算</h3><p>rolling 让你对每个位置之前（或周围）的若干数据点做聚合，用来平滑波动、发现趋势。</p><h4>4.1 基础：移动平均（MA）</h4><pre><code># 7 日移动平均（周平滑）
df["MA_7"] = df["销售额"].rolling(window=7).mean()

# 30 日移动平均（月平滑）
df["MA_30"] = df["销售额"].rolling(window=30).mean()

# 同步计算移动标准差（识别波动性）
df["STD_7"] = df["销售额"].rolling(window=7).std()

# 更稳健的中位数（对异常值不敏感）
df["MEDIAN_7"] = df["销售额"].rolling(window=7).median()

# 滚动求和（7 日累计销售额）
df["ROLLING_SUM_7"] = df["销售额"].rolling(window=7).sum()</code></pre><h4>4.2 进阶：指数加权移动平均（EWM）</h4><p>普通滚动平均给每个窗口内的数据相同权重，而 EWM 给最近的数据更高权重，能更快响应最新变化。</p><pre><code># alpha=0.3 表示最近一期权重 30%，历史数据权重衰减
df["EWMA_7"] = df["销售额"].ewm(alpha=0.3, adjust=False).mean()

# 也可以用 span 参数指定半衰期天数
df["EWMA_30"] = df["销售额"].ewm(span=30, adjust=False).mean()</code></pre><h3>五、Shift：对比历史数据</h3><p>shift 将整列数据平移若干周期，用于计算同比/环比、差分。</p><pre><code># 环比：前一天 vs 当天
df["昨日销售额"] = df["销售额"].shift(1)
df["日环比%"] = (df["销售额"] / df["昨日销售额"] - 1) * 100

# 周同比：与上周同一天对比（shift(7)）
df["上周同日"] = df["销售额"].shift(7)
df["周同比%"] = (df["销售额"] / df["上周同日"] - 1) * 100

# 月同比：与上月同一天对比（shift(30) 近似，更严谨用 resample + shift）
monthly = df["销售额"].resample("M").sum()
monthly_pct = (monthly / monthly.shift(1) - 1) * 100  # 环比
monthly_yoy = (monthly / monthly.shift(12) - 1) * 100  # 同比（去年同月）

# 差分（增长量）
df["日增长"] = df["销售额"].diff()  # 等价于 df["销售额"] - df["销售额"].shift(1)</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>做时间序列同比/环比分析时，一个非常实用的诊断工具是「先画图」。把 <code>pct_change</code> 的结果画成折线图，可以快速发现周期性模式和异常日期，而不是先纠结计算公式是否正确。</div><h3>六、综合案例：销售额趋势诊断</h3><p>以下是一个可以直接使用的「销售诊断」函数：</p><pre><code># 假设 ts 是按日汇总的销售额时间序列
import pandas as pd, numpy as np

dates = pd.date_range("2024-01-01", periods=180)
ts = pd.Series(
    np.random.randint(8000, 15000, 180) + np.sin(np.arange(180)/10) * 2000,
    index=dates, name="销售额"
)

# 1. 基础指标
print(f"分析区间: {ts.index.min().date()} ~ {ts.index.max().date()}")
print(f"总销售额: {ts.sum():,.0f}")
print(f"日均销售: {ts.mean():,.0f}")
print(f"最高日销: {ts.max():,.0f} (日期: {ts.idxmax().date()})")

# 2. 月度聚合
monthly = ts.resample("M").sum()
print("\n月度销售额:")
print(monthly.round(0))

# 3. 环比变化
mom = monthly.pct_change() * 100
print("\n月度环比(%):")
print(mom.round(1))

# 4. 7日移动平均 vs 原始
ma7 = ts.rolling(7).mean()
print(f"\n近7天平均: {ma7.iloc[-1]:,.0f}, 近30天平均: {ts.rolling(30).mean().iloc[-1]:,.0f}")

# 5. 周几特征
dow = ts.groupby(ts.index.dayofweek).mean()
dow.index = ["周一","周二","周三","周四","周五","周六","周日"]
print("\n平均日销按周几分布:")
print(dow.round(0).sort_values(ascending=False))</code></pre><h3>七、常见坑与最佳实践</h3><ul><li><strong>日期有重复/缺失</strong>：用 <code>df.index.is_unique</code> 检查唯一性；用 <code>.asfreq("D")</code> 填充缺失日期，再用 <code>.fillna(method="ffill")</code> 或 0 填充。</li><li><strong>时区混乱</strong>：跨时区数据先统一为 UTC 或当地时区（<code>.tz_localize</code> / <code>.tz_convert</code>）。</li><li><strong>resample 与 groupby 混用</strong>：先 <code>groupby("城市")</code> 再 <code>.resample("M").sum()</code>，会自动按城市分别按月聚合，非常方便。</li><li><strong>shift 在不均匀时间点上出问题</strong>：<code>shift(7)</code> 只适用于每天一条记录且无中断的情况。如果数据稀疏，应该用 <code>rolling(window="7D").mean()</code>（基于真实时间间隔的窗口）。</li></ul><h3>八、本章小结</h3><p>时间序列是数据分析皇冠上的明珠。记住三个核心操作：<strong>resample 改变粒度、rolling 平滑波动、shift 做同比/环比</strong>。再配合日期索引切片、星期几/月份/季度特征提取，你就能回答业务中 90% 的「时间相关问题」。而当你需要更复杂的预测建模时（ARIMA、Prophet、LSTM 等），这些预处理步骤也是必不可少的基础。</p>''',
                'import pandas as pd, numpy as np\nidx = pd.date_range("2024-01-01", periods=120, freq="D")\nts = pd.Series(np.cumsum(np.random.randn(120)*10+50), index=idx)\nprint(ts.resample("M").sum().tail())\nprint(ts.rolling(7).mean().tail())',
                [{'q':'按周聚合？','options':['W','M','D','Y'],'answer':0},
                 {'q':'rolling(7) 指？','options':['随机 7 行','7 期滚动窗口','每 7 行取一条','删除 7 行'],'answer':1},
                 {'q':'把日期设为索引的好处？','options':['resample / 时间切片 / rolling 更方便','会自动删除 NA','更省内存','无好处'],'answer':0}],
                'import pandas as pd, numpy as np\nidx = pd.date_range("2024-01-01", periods=180)\nts = pd.Series(np.cumsum(np.random.randn(180)*5+100), index=idx)\nprint(ts.resample("M").mean())\nprint(ts.rolling(30).mean().tail())')
        ]
    },
    3: {
        'id': 3, 'title': '数据可视化', 'icon': '📈',
        'color': '#27ae60', 'level': '进阶',
        'description': 'Matplotlib & Seaborn 做专业商务图表。',
        'chapters': [
            make_chapter(1, 'Matplotlib 基础', '25 分钟',
                '''<h3>一、为什么需要数据可视化？</h3><p>在数据分析中，人类大脑处理图像信息的速度比处理表格数据快 60,000 倍。一张精心设计的图表可以在 3 秒内传达出 100 行数据才能讲清的信息。</p><p>Python 生态提供了三套主流工具链：</p><ul><li><strong>Matplotlib</strong>：最底层、最灵活，适合精细控制每一个细节</li><li><strong>Seaborn</strong>：基于 Matplotlib 的统计图表库，适合快速探索性分析</li><li><strong>Plotly / Bokeh</strong>：可交互图表，适合 dashboard 和 Web 展示</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Matplotlib 是所有 Python 可视化库的基础。掌握它的两大范式（<strong>pyplot 状态机</strong> 和 <strong>面向对象 API</strong>），你就能轻松驾驭所有上层库。</div><h3>二、Matplotlib 两大绘图范式</h3><h4>2.1 范式一：pyplot 状态机（快速画图）</h4><p>这套 API 模仿 MATLAB，每次调用都会在「当前活动的图」上操作。代码最短，适合快速探索：</p><pre><code>import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 4))
plt.plot(x, y, label="sin(x)", linewidth=2, color="#3776ab")
plt.title("正弦函数示例", fontsize=14)
plt.xlabel("x 轴")
plt.ylabel("y 轴")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()</code></pre><h4>2.2 范式二：面向对象 API（精细控制，推荐）</h4><p>显式创建 Figure 和 Axes 对象，操作更清晰，不会因为状态机的隐式行为出 bug。是生产代码的首选：</p><pre><code>fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(x, y, label="sin(x)", linewidth=2, color="#3776ab")
ax.plot(x, np.cos(x), label="cos(x)", linewidth=2, color="#e67e22")

ax.set_title("正弦与余弦函数", fontsize=14, pad=15)
ax.set_xlabel("x", fontsize=11)
ax.set_ylabel("y", fontsize=11)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False)  # 隐藏上边框
ax.spines["right"].set_visible(False) # 隐藏右边框

fig.tight_layout()
fig.savefig("my_chart.png", dpi=150, bbox_inches="tight")</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>99% 的场景下推荐使用面向对象的 <code>fig, ax = plt.subplots()</code> 写法。它更清晰、更易维护、更适合多子图布局。pyplot 状态机只在 3 行以内的超快速探索时使用。</div><h3>三、常见图表类型与适用场景</h3><table><thead><tr><th>图表类型</th><th>Matplotlib 函数</th><th>典型用途</th></tr></thead><tbody><tr><td>折线图</td><td>ax.plot()</td><td>时间序列、趋势展示</td></tr><tr><td>柱状图</td><td>ax.bar()</td><td>不同类别间对比</td></tr><tr><td>水平柱状图</td><td>ax.barh()</td><td>排名类数据（Top N）</td></tr><tr><td>散点图</td><td>ax.scatter()</td><td>两个数值变量的相关性</td></tr><tr><td>直方图</td><td>ax.hist()</td><td>单变量分布形态</td></tr><tr><td>箱线图</td><td>ax.boxplot()</td><td>多组分布与异常值</td></tr><tr><td>饼图</td><td>ax.pie()</td><td>简单占比展示（慎用）</td></tr><tr><td>热力图</td><td>ax.imshow()</td><td>二维密度 / 相关矩阵</td></tr></tbody></table><h3>四、中文字体与样式优化</h3><p>中文字体乱码是 Matplotlib 最常见的问题。以下是完整的解决方案：</p><pre><code>import matplotlib
matplotlib.use("Agg")  # 服务器无 GUI 环境
import matplotlib.pyplot as plt

# 方案一：全局设置字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False  # 解决负号显示为方框

# 方案二：使用 style 预设样式
plt.style.use("seaborn-v0_8-whitegrid")  # 白背景 + 细网格

# 方案三：自定义配色（商务蓝橙配色示例）
colors = ["#3776ab", "#e67e22", "#27ae60", "#8e44ad", "#2980b9"]</code></pre><h3>五、多子图布局与组合图表</h3><h4>5.1 规则网格布局（subplots）</h4><pre><code># 2 行 2 列的子图布局
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].plot(x, np.sin(x))
axes[0, 0].set_title("子图 1")

axes[0, 1].bar(["A", "B", "C"], [3, 7, 5])
axes[0, 1].set_title("子图 2")

axes[1, 0].scatter(np.random.randn(100), np.random.randn(100), alpha=0.5)
axes[1, 0].set_title("子图 3")

axes[1, 1].hist(np.random.randn(1000), bins=30, edgecolor="white")
axes[1, 1].set_title("子图 4")

fig.tight_layout()  # 自动调整间距，避免标题重叠</code></pre><h4>5.2 复杂布局（GridSpec）</h4><pre><code># 使用 GridSpec 实现跨列/跨行的不规则布局
fig = plt.figure(figsize=(12, 8))
gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.2)

ax1 = fig.add_subplot(gs[0, :])   # 第一行跨两列（主图）
ax2 = fig.add_subplot(gs[1, 0])   # 第二行左（细节图1）
ax3 = fig.add_subplot(gs[1, 1])   # 第二行右（细节图2）</code></pre><h3>六、图表美化：让你的图「显得专业」</h3><p>下面是几条能显著提升图表观感的最佳实践：</p><ul><li><strong>移除顶部和右侧边框</strong>：<code>ax.spines["top"].set_visible(False)</code>，让图表更「通透」</li><li><strong>加粗重点线条</strong>：主趋势线 linewidth=2，次要线条 1</li><li><strong>直接在柱顶标数字</strong>：<code>for i, v in enumerate(values): ax.text(i, v+0.5, str(v), ha="center")</code></li><li><strong>慎用饼图</strong>：超过 5 个类别时，请改用水平柱状图，可读性大幅提升</li><li><strong>保持配色一致</strong>：一张图里不超过 5 种颜色，可以从 coolors.co 获取专业配色</li><li><strong>添加数据源标注</strong>：<code>fig.text(0.1, 0.01, "数据来源: XXX 系统", fontsize=8, color="gray")</code></li></ul><div class="warn-box"><strong>⚠ 注意事项：</strong>在服务器/脚本环境（如无 GUI 的 Linux 容器）中，需要在 <code>import matplotlib.pyplot</code> 之前设置 <code>matplotlib.use("Agg")</code>，否则会因为找不到显示驱动而报错。如果你在 Jupyter Notebook 中，则无需此设置，加上 <code>%matplotlib inline</code> 即可。</div><h3>七、本章小结</h3><p>Matplotlib 是 Python 可视化的基石。掌握它的<strong>面向对象 API（fig + ax）</strong>、<strong>常见图表类型</strong>、<strong>中文字体配置</strong>和<strong>图表美化</strong>四要素，你就能画出不逊色于商业 BI 工具的专业图表。下一章节我们将学习 Seaborn，它基于 Matplotlib，能让你用更少的代码画出更专业的统计图表。</p>''',
                'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport numpy as np\nx = np.linspace(0,10,100)\nfig, ax = plt.subplots(figsize=(8,4))\nax.plot(x, np.sin(x), label="sin"); ax.plot(x, np.cos(x), label="cos")\nax.legend(); ax.grid(True, alpha=0.3)\nprint("绘图完成")',
                [{'q':'创建子图？','options':['plt.subplots()','plt.make()','plt.figure()','plt.axes()'],'answer':0},
                 {'q':'服务器端（无 GUI）常设置？','options':['matplotlib.use("Agg")','plt.nogui()','mpl.server=True','skip display'],'answer':0},
                 {'q':'柱状图？','options':['plt.bar()','plt.pie()','plt.col()','plt.hist()'],'answer':0}],
                'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nfig, ax = plt.subplots()\nax.bar(["A","B","C","D"], [23,45,17,38], color="#3776ab")\nfor i,v in enumerate([23,45,17,38]):\n    ax.text(i, v+1, str(v), ha="center")\nprint("柱状图完成")'),
            make_chapter(2, 'Seaborn 统计图', '25 分钟',
                '''<h3>一、Seaborn 是什么？与 Matplotlib 的关系</h3><p>Seaborn 是基于 Matplotlib 的高层统计可视化库，专为统计数据分析而生。它的定位很像「Matplotlib + 统计 + 主题模板 + 简洁 API」。它的核心价值在于三件事：</p><ul><li>提供美观的默认主题与美观配色</li><li>内置常用统计图（箱线图、热力图、分布图）</li><li>与 Pandas DataFrame 无缝配合的 API（可以直接传入列名）</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>可以这样使用 Seaborn 的核心心智模型的正确姿势是「用 Matplotlib 建画布，用 Seaborn 画图」——两者混用、协同工作。记住：<code>fig, ax = plt.subplots()</code> 建画布，然后用 <code>sns.boxplot(data=df, ax=ax)</code> 把图「画到」指定的 axes 上。</div><h3>二、Seaborn 的主题与配色</h3><h4>2.1 主题设置</h4><pre><code>import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# 可选主题：whitegrid / darkgrid / white / dark / ticks
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.1)  # talk 适配字体大小

# 中文兼容
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False</code></pre><h4>2.2 配色（Palette）</h4><pre><code># 离散配色：适合分类变量
pal = sns.color_palette("Set2", 10)  # 10 种颜色
sns.barplot(x="城市", y="销售额", data=df, palette=pal)

# 连续色：适合数值大小变化
cmap = sns.diverging_palette(220, 20, as_cmap=True)
sns.heatmap(corr_matrix, cmap=cmap)

# 常用颜色名称：husl, Set2, coolwarm, RdBu, viridis, magma</code></pre><h3>三、七类核心统计图表</h3><h4>3.1 箱线图（Boxplot）：分布与异常值</h4><p>箱线图展示了数据的四分位数结构，一眼发现异常值，是探索性分析（EDA）的第一步。</p><pre><code>fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(data=df, x="品类", y="销售额", ax=ax, palette="Set2")
ax.set_title("各品类销售额分布", fontsize=14, pad=15)
ax.set_xlabel(""); ax.set_ylabel("销售额")
fig.tight_layout()</code></pre><h4>3.2 热力图（Heatmap）：相关性矩阵</h4><p>热力图用于展示二维矩阵，最常见用途是<strong>相关系数矩阵</strong>。</p><pre><code># 计算相关系数
corr = df.select_dtypes(include=[np.number]).corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr, annot=True, cmap="coolwarm", center=0,
    square=True, linewidths=0.5, fmt=".2f", ax=ax
)
ax.set_title("数值变量相关系数热力图", fontsize=14)</code></pre><h4>3.3 分布图（Histogram / KDE）：分布形态</h4><pre><code>fig, axes = plt.subplots(1, 2, figsize=(12, 4))
# 直方图
sns.histplot(data=df, x="销售额", bins=30, kde=True, ax=axes[0])
axes[0].set_title("销售额分布")
# 按分组的密度图
sns.kdeplot(data=df, x="销售额", hue="城市", fill=True, alpha=0.3, ax=axes[1])
axes[1].set_title("各城市销售额密度对比")</code></pre><h4>3.4 散点图 / 联合分布图（Scatter / Jointplot）</h4><p>用于探索两个数值变量的关系。</p><pre><code># 带回归线的散点图
sns.scatterplot(data=df, x="客单价", y="复购率", hue="城市", size="订单数", sizes=(50, 400), alpha=0.7)

# 带边缘分布的联合图
sns.jointplot(data=df, x="客单价", y="复购率", kind="reg", height=6)

# 多变量散点矩阵（Pairplot）
sns.pairplot(df[["销售额", "客单价", "复购率", "客户年龄"]], diag_kind="kde", corner=True)</code></pre><h4>3.5 小提琴图（Violinplot）：箱线图 + 密度</h4><pre><code>fig, ax = plt.subplots(figsize=(10, 5))
sns.violinplot(data=df, x="品类", y="客单价", ax=ax, palette="Set2", inner="quartile")</code></pre><h4>3.6 条形图（Barplot）：带置信区间的均值</h4><pre><code># 自动计算并显示置信区间（默认 95%）
sns.barplot(data=df, x="城市", y="销售额", ax=ax, ci=95)</code></pre><h4>3.7 折线图（Lineplot）：带误差的时间趋势</h4><pre><code>sns.lineplot(data=df, x="月份", y="销售额", hue="城市", ci="sd", ax=ax)</code></pre><h3>四、实战：客户分群可视化流水线</h3><p>下面是一个可以直接复用的数据分析全流程可视化：</p><pre><code>import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

sns.set_style("whitegrid")
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

np.random.seed(0)
df = pd.DataFrame({
    "品类": np.repeat(["A","B","C","D", 50),
    "销售额": np.concatenate([np.random.normal(mu, sigma, 50) for mu, sigma in [(2000,300),(3000,500),(2500,400),(4000,600)])
})

# 2行 2列综合图
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 子图1: 箱线图
sns.boxplot(data=df, x="品类", y="销售额", ax=axes[0, 0], palette="Set2")
axes[0, 0].set_title("品类销售额分布")

# 子图2: 小提琴图
sns.violinplot(data=df, x="品类", y="销售额", ax=axes[0, 1], inner="quartile")
axes[0, 1].set_title("销售额密度（小提琴图")

# 子图3: 柱状图（均值+置信区间）
sns.barplot(data=df, x="品类", y="销售额", ax=axes[1, 0])
axes[1, 0].set_title("品类均值对比")

# 子图4: 直方图（按品类）
for cat in df["品类"].unique():
    sns.histplot(df[df["品类"]==cat]["销售额"], kde=True, label=cat, ax=axes[1, 1], alpha=0.3)
axes[1, 1].legend()
axes[1, 1].set_title("各品类分布直方图")
fig.tight_layout()</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>数据分析中请养成「先画图再解释的习惯——先看散点图看分布，再做统计检验，最后写结论」，可以显著减少被误导的概率。很多异常值分布是否正态，再做统计检验，最后写结论」，可以显著减少被误导的概率。</div><h3>五、常见问题与最佳实践</h3><ul><li><strong>中文乱码</strong>：必须在任何时候都加上字体设置，确保中文字体名称（SimHei、Microsoft YaHei）</li><li><strong>类别太多</strong>：当类别超过 10 个以上时，用水平条形图替代垂直条形图，避免标签堆叠</li><li><strong>相关性解释相关系数 ≠ 因果</strong>：相关系数 ≠ 因果，不要在报告中混用</li><li><strong>颜色不要过度解读</strong>：一张图不要超过 6-7 个类别，超出请改用子图</li></ul><h3>六、本章小结</h3><p>Seaborn 让你用 3 行代码画出过去需要 30 行代码才能完成的统计图表。核心是<strong>箱线图、热力图、分布图、散点图、小提琴图、条形图、折线图七类图表。配合 Matplotlib 的子图布局，你就能完成从原始数据到专业分析图的完整分析。</p>''',
                'import matplotlib\nmatplotlib.use("Agg")\nimport seaborn as sns; import matplotlib.pyplot as plt\nimport pandas as pd, numpy as np\nnp.random.seed(0)\ndf = pd.DataFrame({"g": np.repeat(["A","B","C"],50), "v": np.concatenate([np.random.randn(50)*5+x for x in [20,30,25]])})\nfig, ax = plt.subplots()\nsns.boxplot(data=df, x="g", y="v", ax=ax)\nprint("seaborn 绘制完成")',
                [{'q':'看两个数值列相关性？','options':['散点图 / pairplot / heatmap','饼图','折线图','面积图'],'answer':0},
                 {'q':'画热力图？','options':['sns.heatmap()','sns.heat()','plt.heatmap()','sns.hotmap()'],'answer':0},
                 {'q':'快速查看多变量分布？','options':['sns.pairplot','sns.lineplot','sns.pointplot','plt.grid'],'answer':0}],
                'import matplotlib\nmatplotlib.use("Agg")\nimport seaborn as sns; import matplotlib.pyplot as plt\nimport pandas as pd, numpy as np\nnp.random.seed(0)\ndf = pd.DataFrame(np.random.randn(5,5), columns=list("ABCDE"))\nfig, ax = plt.subplots()\nsns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)\nprint("相关系数热力图完成")'),
            make_chapter(3, '商务图表实战', '30 分钟',
                '''<h3>一、选对图表，分析已经成功一半</h3><p>商业数据分析中，最常见的场景可以归纳为 5 类：<strong>对比、趋势、构成、分布、相关</strong>。选对了图表类型，业务方一眼就能理解你的结论。下表是面向商务场景的「选图指南」。</p><table><thead><tr><th>分析场景</th><th>首选图表</th><th>次选图表</th><th>示例</th></tr></thead><tbody><tr><td>对比（不同类别谁更好）</td><td>条形图 / 柱状图</td><td>点图</td><td>各城市销售额对比</td></tr><tr><td>趋势（随时间变化）</td><td>折线图</td><td>面积图</td><td>月度销售额趋势</td></tr><tr><td>构成（整体由什么组成）</td><td>堆叠柱状图</td><td>堆叠面积图</td><td>各品类销售占比</td></tr><tr><td>分布（数据长什么样）</td><td>直方图 / 箱线图</td><td>小提琴图</td><td>客单价分布</td></tr><tr><td>相关（两个变量关系）</td><td>散点图</td><td>气泡图</td><td>广告投入 vs 销售</td></tr><tr><td>排名（Top N）</td><td>水平条形图（按数值排序）</td><td>热力图</td><td>Top 10 产品</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>在商务报告中，<strong>饼图的信息密度最低，慎用</strong>。当类别超过 5 个时，人脑难以比较饼图的切片大小——请改用水平柱状图（按数值降序排列，配合柱顶标注数字），可读性提升 10 倍。</div><h3>二、商务图表设计的 7 条黄金规则</h3><ul><li><strong>规则 1：一张图只讲一个故事</strong>。不要把「趋势、排名、结构」塞进同一张图。</li><li><strong>规则 2：数字直接标注</strong>。柱顶 / 线端直接写数字，让读者无需「用眼睛估读」。</li><li><strong>规则 3：按数值排序</strong>。不要按字母序，除非轴是时间维度。</li><li><strong>规则 4：大数字 + 小标题</strong>。dashboard 顶部应该有 3-5 个关键指标（KPI）。</li><li><strong>规则 5：同一尺度配色</strong>。一个报告内的同一组数据用同一种颜色，避免混乱。</li><li><strong>规则 6：留白与对齐</strong>。图表之间的间距、对齐，直接决定专业感。</li><li><strong>规则 7：标注数据来源与时间</strong>。无数据来源的图表 = 不权威。</li></ul><h3>三、实战 1：月度销售趋势图（折线图）</h3><pre><code>import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

# 中文字体
plt.rcParams["font.sans-serif"] = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

months = ["1月", "2月", "3月", "4月", "5月", "6月"]
online = [320, 380, 420, 460, 500, 580]
offline = [200, 210, 230, 220, 215, 210]

fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(months, online, marker="o", linewidth=2.5, color="#3776ab", label="线上", markersize=8)
ax.plot(months, offline, marker="s", linewidth=2.5, color="#e67e22", label="线下", markersize=8)

# 美化
ax.set_title("2024 H1 线上 vs 线下销售额（万元）", fontsize=14, pad=15, loc="left")
ax.set_ylabel("销售额 (万元)", fontsize=11)
ax.legend(fontsize=10, frameon=False)
ax.grid(True, alpha=0.3, linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 在每个数据点标数值
for x, y in zip(months, online):
    ax.text(x, y + 20, f"{y}", ha="center", fontsize=9, color="#3776ab", fontweight="bold")
for x, y in zip(months, offline):
    ax.text(x, y - 25, f"{y}", ha="center", fontsize=9, color="#e67e22", fontweight="bold")

# 千分位格式（如果数值较大）
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{int(x):,}"))

fig.tight_layout()</code></pre><h3>四、实战 2：品类销售贡献（水平条形图 + 排序）</h3><pre><code>categories = ["电子产品", "服装", "家居", "美妆", "食品"]
sales = [480, 360, 280, 190, 150]

# 按销售额降序排序（水平条形图需要从下往上画，所以再反转一次）
order = np.argsort(sales)
cats_sorted = [categories[i] for i in order]
sales_sorted = [sales[i] for i in order]

fig, ax = plt.subplots(figsize=(10, 5))
bars = ax.barh(cats_sorted, sales_sorted, color="#3776ab", height=0.6, edgecolor="white")

# 柱右侧标注数字
for bar, v in zip(bars, sales_sorted):
    ax.text(v + 10, bar.get_y() + bar.get_height()/2, f"{v} 万", va="center", fontsize=10, fontweight="bold")

ax.set_title("2024 H1 各品类销售贡献（万元）", fontsize=14, pad=15, loc="left")
ax.set_xlabel("销售额（万元）", fontsize=11)
ax.grid(True, alpha=0.3, axis="x", linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.set_xlim(0, max(sales)*1.2)  # 右侧留出空间给数值标注
fig.tight_layout()</code></pre><h3>五、实战 3：品类占比堆叠柱状图</h3><pre><code>months = ["1月", "2月", "3月", "4月", "5月", "6月"]
cat_a = [120, 130, 145, 160, 180, 200]
cat_b = [80, 90, 100, 110, 105, 120]
cat_c = [60, 70, 75, 85, 90, 100]

fig, ax = plt.subplots(figsize=(9, 4))
ax.bar(months, cat_a, label="A 品类", color="#3776ab")
ax.bar(months, cat_b, bottom=cat_a, label="B 品类", color="#e67e22")
ax.bar(months, cat_c, bottom=[a+b for a, b in zip(cat_a, cat_b)], label="C 品类", color="#27ae60")

ax.set_title("各月销售构成", fontsize=14, pad=15, loc="left")
ax.legend(fontsize=10, frameon=False, ncol=3)
ax.grid(True, alpha=0.3, axis="y", linestyle="--")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()</code></pre><h3>六、实战 4：Top N 产品排行榜 + KPI 数字卡</h3><pre><code># KPI 卡片式展示（适用于 dashboard 首页）
total_sales = sum(online) + sum(offline)
growth_rate = (online[-1] / online[0] - 1) * 100

fig, axes = plt.subplots(1, 3, figsize=(14, 4))
kpi_data = [
    ("H1 总销售额（万元）", f"{total_sales:,}", "#3776ab"),
    ("上半年环比增长(%)", f"{growth_rate:.1f}%", "#27ae60"),
    ("线上/线下占比", f"{sum(online)/(total_sales)*100:.0f}% / {sum(offline)/(total_sales)*100:.0f}%", "#e67e22")
]
for ax, (title, value, color) in zip(axes, kpi_data):
    ax.text(0.5, 0.75, value, fontsize=22, fontweight="bold", ha="center", color=color)
    ax.text(0.5, 0.45, title, fontsize=11, ha="center", color="gray")
    ax.set_frame_on(False)  # 去掉边框
    ax.set_xticks([]); ax.set_yticks([])  # 去掉坐标轴
fig.suptitle("📊 业务关键指标概览", fontsize=14, y=0.05)
plt.tight_layout()</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>做商业报告时，请永远记住「业务方只有 30 秒时间看你的图」。最简单的检查方法是：你画完图后闭上眼睛，能否用一句话说清楚这张图在讲什么？如果不能，说明图表设计还不够聚焦。</div><h3>七、常见错误清单</h3><ul><li><strong>用饼图展示 8+ 个类别</strong> → 请改用水平条形图，按数值排序</li><li><strong>颜色太花哨</strong> → 一套报告使用 2-3 个主色 + 1-2 个强调色即可</li><li><strong>时间轴顺序错乱</strong> → 永远检查 1 月到 12 月是否正确排序</li><li><strong>忘记标注单位</strong> → 是「万元」还是「元」？务必写清楚</li><li><strong>Y 轴不从 0 开始</strong> → 会放大差异、误导读者（除非是小额变化的放大展示，且明确标注）</li></ul><h3>八、本章小结</h3><p>本章节我们从「图表选型 → 设计原则 → 三个真实业务场景代码模板 → 常见错误清单」完整介绍了商务图表实战。掌握这一套模板，你可以在 15 分钟内画出专业级别的商业分析报告配图。记住一句话：<strong>图表的目的不是炫技，而是讲清楚业务故事。</strong></p>''',
                'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nimport pandas as pd\ndf = pd.DataFrame({"m":["1月","2月","3月","4月","5月","6月"], "online":[320,380,420,460,500,580], "offline":[200,210,230,220,215,210]})\nfig, ax = plt.subplots(figsize=(9,4))\nax.plot(df.m, df.online, marker="o", label="线上", linewidth=2)\nax.plot(df.m, df.offline, marker="s", label="线下", linewidth=2)\nax.legend(); ax.grid(alpha=0.3)\nprint("趋势图完成")',
                [{'q':'画多条线区分？','options':['加 label 再 legend()','不同文件保存','文字说明','无法做到'],'answer':0},
                 {'q':'加圆点标记？','options':['marker="o"','dot=True','circle=True','mark=True'],'answer':0},
                 {'q':'看占比？','options':['饼图 / 堆叠柱','折线图','散点图','直方图'],'answer':0}],
                'import matplotlib\nmatplotlib.use("Agg")\nimport matplotlib.pyplot as plt\nm = ["Q1","Q2","Q3","Q4"]\na,b,c = [100,150,200,250],[80,90,120,150],[50,60,70,80]\nfig, ax = plt.subplots()\nax.bar(m, a, label="A")\nax.bar(m, b, bottom=a, label="B")\nax.bar(m, c, bottom=[a[i]+b[i] for i in range(4)], label="C")\nax.legend(); ax.set_title("季度堆叠贡献")\nprint("堆叠柱完成")')
        ]
    },
    4: {
        'id': 4, 'title': 'SQL 商业数据分析', 'icon': '🗄️',
        'color': '#2980b9', 'level': '进阶',
        'description': '用 SQL 做商业指标分析、JOIN、窗口函数。',
        'chapters': [
            make_chapter(1, 'SQL 基础', '20 分钟',
                '''<h3>一、SQL 是什么？为什么数据分析师必须掌握它？</h3><p>SQL（Structured Query Language，结构化查询语言）是与关系型数据库「对话」的标准语言。在真实企业中，99% 的原始业务数据存放在数据库中（MySQL、PostgreSQL、Oracle、SQL Server 等）。用 Excel 打开 CSV 文件只是分析的最后一步，前面从数据库取数的过程必须用 SQL。</p><p>SQL 的核心价值：</p><ul><li><strong>取数能力</strong>：从百万、千万行表中快速筛选出你需要的数据</li><li><strong>聚合能力</strong>：按任意维度汇总统计（GROUP BY）</li><li><strong>关联能力</strong>：跨表、跨维度组合信息（JOIN）</li><li><strong>可复现性</strong>：一条 SQL 可以被同事、被未来的你复用</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>数据分析师的 SQL 能力不需要达到 DBA 级别，但你必须熟练掌握<strong>「SELECT 六子句 + JOIN + 窗口函数」</strong>三件套。这三件套能覆盖你工作中 95% 的取数需求。</div><h3>二、SELECT 六子句执行顺序（最常被误解的知识点）</h3><p>SQL 语句的<strong>书写顺序</strong>和<strong>执行顺序</strong>并不相同。理解执行顺序是理解 SQL 行为的关键：</p><table><thead><tr><th>执行顺序</th><th>关键字</th><th>功能</th></tr></thead><tbody><tr><td>1</td><td>FROM / JOIN</td><td>从哪些表取数据、如何关联</td></tr><tr><td>2</td><td>WHERE</td><td>先筛掉不需要的<strong>行</strong>（分组前过滤）</td></tr><tr><td>3</td><td>GROUP BY</td><td>按哪些字段做分组聚合</td></tr><tr><td>4</td><td>HAVING</td><td>过滤聚合后的结果（分组后过滤）</td></tr><tr><td>5</td><td>SELECT</td><td>选择输出哪些列（含聚合表达式）</td></tr><tr><td>6</td><td>ORDER BY</td><td>对结果排序</td></tr><tr><td>7</td><td>LIMIT</td><td>只取前 N 行</td></tr></tbody></table><p>对应的<strong>书写顺序</strong>是：<code>SELECT ... FROM ... WHERE ... GROUP BY ... HAVING ... ORDER BY ... LIMIT</code></p><div class="warn-box"><strong>⚠ 注意事项：</strong>初学者最常犯的错误是「在 WHERE 中使用聚合函数」。例如 <code>WHERE SUM(amount) > 1000</code> 是非法的，因为 WHERE 在 GROUP BY 之前执行，此时 SUM 还没算出来。正确做法是用 <code>HAVING SUM(amount) > 1000</code>。</div><h3>三、经典聚合函数与分组</h3><pre><code>-- 1) 基础聚合：COUNT / SUM / AVG / MIN / MAX
SELECT
    COUNT(*)             AS 订单数,
    SUM(amount)          AS 总销售额,
    AVG(amount)          AS 平均客单价,
    MIN(amount)          AS 最小订单,
    MAX(amount)          AS 最大订单
FROM orders;

-- 2) 按维度分组（GROUP BY）：按城市统计销售额
SELECT
    city,
    COUNT(*)             AS 订单数,
    SUM(amount)          AS 总销售额,
    SUM(amount)/COUNT(*) AS 平均客单价
FROM orders
WHERE order_date BETWEEN '2024-01-01' AND '2024-06-30'
GROUP BY city
ORDER BY 总销售额 DESC
LIMIT 10;

-- 3) 多字段分组：按城市 x 品类，并过滤聚合结果
SELECT
    city,
    category,
    SUM(amount) AS total_sales
FROM orders
GROUP BY city, category
HAVING SUM(amount) > 100000  -- 只看总销售额超过 10 万的组合
ORDER BY total_sales DESC;</code></pre><h3>四、条件与分支（CASE WHEN）</h3><p>CASE WHEN 是 SQL 中的「if-else」，非常实用：</p><pre><code>-- 给订单打标签
SELECT
    order_id,
    amount,
    CASE
        WHEN amount >= 1000 THEN 'A-高价值'
        WHEN amount >= 500  THEN 'B-中等'
        WHEN amount >= 100  THEN 'C-普通'
        ELSE 'D-小额'
    END AS 客户分级
FROM orders;

-- 配合聚合做结构分析：按分类统计各段订单数
SELECT
    CASE WHEN amount >= 1000 THEN 'A'
         WHEN amount >= 500  THEN 'B'
         WHEN amount >= 100  THEN 'C'
         ELSE 'D' END AS tier,
    COUNT(*) AS cnt,
    SUM(amount) AS sum_amount
FROM orders
GROUP BY tier;</code></pre><h3>五、去重、Top N、空值处理</h3><pre><code>-- 去重：不重复的城市
SELECT DISTINCT city FROM orders;

-- 空值处理：IFNULL / COALESCE
SELECT COALESCE(city, '未知城市') AS city, COUNT(*) FROM orders GROUP BY city;

-- Top N 产品：按销售额排序取前 10
SELECT product_id, SUM(amount) AS s
FROM orders
GROUP BY product_id
ORDER BY s DESC
LIMIT 10;

-- 注意：LIMIT 没有「跳过前 N 个取后 M 个」的标准写法，不同数据库不同
-- MySQL/PostgreSQL: LIMIT 10 OFFSET 20; SQL Server: OFFSET 20 ROWS FETCH NEXT 10 ONLY</code></pre><h3>六、Python 调用 SQL（SQLite 示例）</h3><p>在 Python 脚本中可以直接执行 SQL 语句，再用 Pandas 处理结果：</p><pre><code>import sqlite3
import pandas as pd

conn = sqlite3.connect("your_database.db")

# 方案一：用原生 sqlite3 执行
cur = conn.cursor()
for row in cur.execute("""
    SELECT city, SUM(amount) AS total
    FROM orders
    GROUP BY city
    ORDER BY total DESC
    LIMIT 10
"""):
    print(row)

# 方案二：直接读取为 DataFrame（最推荐）
df = pd.read_sql_query("""
    SELECT city, SUM(amount) AS total_sales
    FROM orders
    GROUP BY city
    ORDER BY total_sales DESC
""", conn)

conn.close()</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>分析工作中建议用「SQL 取数 + Python/Pandas 二次分析」的工作流：先用 SQL 完成 JOIN、WHERE、GROUP BY 等<em>结构性操作</em>，把数据拉回本地（通常是几万到几十万行），再用 Python 完成复杂的统计、建模、可视化。</div><h3>七、本章小结</h3><p>本章介绍了 SQL 的<strong>六子句执行顺序、五大聚合函数、CASE WHEN 条件分支、去重与 Top N</strong>。这是 SQL 最核心的 20% 知识，却能解决你 80% 的取数需求。下一章节将进入更高级的主题：<strong>JOIN 多表关联与子查询</strong>，它们才是真正解锁「跨维度分析」能力的钥匙。</p>''',
                'import sqlite3\nconn = sqlite3.connect(":memory:")\nc = conn.cursor()\nc.execute("CREATE TABLE sales (region TEXT, amount REAL, qty INT)")\nc.executemany("INSERT INTO sales VALUES (?,?,?)", [("华北",100,2),("华东",300,5),("华南",150,3),("华北",250,4)])\nconn.commit()\nfor row in c.execute("SELECT region, SUM(amount) FROM sales GROUP BY region ORDER BY 2 DESC"):\n    print(row)\nconn.close()',
                [{'q':'聚合后过滤？','options':['WHERE','HAVING','IF','GROUP'],'answer':1},
                 {'q':'限制行数？','options':['TOP','LIMIT','FIRST','MAXROWS'],'answer':1},
                 {'q':'SUM(amount) 中 amount 是？','options':['表名','列名','函数','库名'],'answer':1}],
                'import sqlite3\nconn = sqlite3.connect(":memory:")\nc = conn.cursor()\nc.execute("CREATE TABLE orders (id INT, city TEXT, total REAL)")\nc.executemany("INSERT INTO orders VALUES (?,?,?)", [(1,"北京",200),(2,"上海",300),(3,"北京",150),(4,"广州",400)])\nconn.commit()\nfor row in c.execute("SELECT city, COUNT(*), SUM(total) FROM orders GROUP BY city"):\n    print(row)\nconn.close()'),
            make_chapter(2, '多表连接与子查询', '25 分钟',
                '''<h3>一、为什么需要 JOIN？真实世界的数据是分散的</h3><p>在任何一个真实业务系统中，数据都不会整齐地放在一张表里。典型的零售公司数据库可能有：</p><ul><li><strong>用户表（users）</strong>：用户ID、昵称、注册时间、城市</li><li><strong>订单表（orders）</strong>：订单ID、用户ID、金额、下单时间</li><li><strong>商品表（products）</strong>：商品ID、品类、价格、库存</li><li><strong>门店表（stores）</strong>：门店ID、城市、面积</li></ul><p>「统计北京市 2024 年 6 月电子品类的销售额」这个问题，需要把 4 张表连起来才能回答。<strong>JOIN 就是把多张表按某个关键字拼接起来的操作。</strong></p><div class="key-point"><strong>⭐ 核心要点：</strong>记住四种 JOIN 的逻辑区别：<code>INNER JOIN</code>（交集）、<code>LEFT JOIN</code>（保留左表全部，右表补 null）、<code>RIGHT JOIN</code>（保留右表全部）、<code>FULL OUTER JOIN</code>（两边全部）。在实际工作中，<strong>LEFT JOIN 占了 80% 的使用场景</strong>，因为我们通常想要「以某张表为基础去关联」。</div><h3>二、四种 JOIN 的图解</h3><table><thead><tr><th>类型</th><th>含义</th><th>何时用</th><th>风险</th></tr></thead><tbody><tr><td>INNER JOIN</td><td>只保留两边 key 都存在的行</td><td>需要「严格匹配」时</td><td>可能丢失用户（没有订单的用户会被排除）</td></tr><tr><td>LEFT JOIN</td><td>保留左表全部行，右表未匹配处填 NULL</td><td>用户为基础去看他的订单等</td><td>需要处理 NULL（用 COALESCE 转 0 或"未知"）</td></tr><tr><td>RIGHT JOIN</td><td>保留右表全部行，左表未匹配处填 NULL</td><td>等价于把表反过来的 LEFT JOIN</td><td>可读性差，建议重写为 LEFT JOIN</td></tr><tr><td>FULL OUTER JOIN</td><td>两边全部保留，未匹配处填 NULL</td><td>比较两个数据源差异</td><td>可能产生大量 NULL 行</td></tr></tbody></table><h3>三、典型应用场景代码</h3><h4>3.1 用户表 LEFT JOIN 订单表（最常见）</h4><pre><code>-- 统计每个用户的累计订单数和金额（包括零订单用户）SELECT    u.user_id,    u.city,    COUNT(o.order_id)            AS order_count,    COALESCE(SUM(o.amount), 0)  AS total_amountFROM users uLEFT JOIN orders o    ON u.user_id = o.user_id   AND o.order_date >= '2024-01-01'  -- 注意：过滤条件放在 ON 里（左连接时）GROUP BY u.user_id, u.cityHAVING COUNT(o.order_id) >= 5ORDER BY total_amount DESCLIMIT 20;</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>LEFT JOIN 时，<strong>对右表的过滤条件应该写在 ON 子句中</strong>，而不是 WHERE。如果写在 WHERE，NULL 行会被过滤掉，效果等同于 INNER JOIN。这是最常见的 SQL bug 之一！</div><h4>3.2 多表链式 JOIN</h4><pre><code>-- 订单 → 商品 → 品类 → 门店，跨 4 张表分析SELECT    s.city,    p.category,    SUM(o.amount) AS total_salesFROM orders oINNER JOIN products p ON o.product_id = p.product_idINNER JOIN stores s   ON o.store_id = s.store_idWHERE o.order_date BETWEEN '2024-06-01' AND '2024-06-30'GROUP BY s.city, p.categoryORDER BY total_sales DESC;</code></pre><h3>四、子查询与派生表</h3><p>子查询就是「查询里面嵌查询」，主要有三种用法：</p><h4>4.1 派生表（Derived Table，FROM 子句中的子查询）</h4><pre><code>-- 先聚合再过滤，避免在最外层写复杂逻辑SELECT city, AVG(user_total) AS avg_user_totalFROM (    SELECT u.user_id, u.city, SUM(o.amount) AS user_total    FROM users u    LEFT JOIN orders o ON u.user_id = o.user_id    GROUP BY u.user_id, u.city) user_summary  -- 这就是「派生表」，必须给别名GROUP BY cityORDER BY avg_user_total DESC;</code></pre><h4>4.2 相关子查询（Correlated Subquery）</h4><p>内部查询依赖外部查询的字段，相当于「每行执行一次」。概念好用，但性能较差，大表慎用：</p><pre><code>-- 每个用户单笔最大订单金额SELECT    u.user_id,    (SELECT MAX(amount) FROM orders o WHERE o.user_id = u.user_id) AS max_orderFROM users u;</code></pre><h4>4.3 IN / EXISTS 子查询</h4><pre><code>-- 找出「至少有一笔订单超过 5000 元」的用户SELECT user_id, cityFROM users uWHERE EXISTS (    SELECT 1 FROM orders o    WHERE o.user_id = u.user_id      AND o.amount > 5000);</code></pre><h3>五、JOIN 可能带来的坑</h3><ul><li><strong>一对多导致「行数膨胀」</strong>：用户表 1 行，订单表 5 行，JOIN 后变成 5 行。如果你在 SELECT 中用 <code>COUNT(*)</code> 会得到订单数而非用户数，要用 <code>COUNT(DISTINCT user_id)</code>。</li><li><strong>多对多导致笛卡尔积</strong>：两边 key 都不唯一时，行数会「爆炸」。必须理解业务关系再做 JOIN。</li><li><strong>NULL 处理</strong>：LEFT JOIN 后右表字段可能为 NULL，统计汇总时要用 <code>COALESCE(col, 0)</code> 转 0，否则 SUM 结果会被 NULL 传染。</li><li><strong>键的类型不一致</strong>：字符串"123" 与数字 123 在某些数据库中可能不匹配，导致 JOIN 结果为 0 行。</li></ul><h3>六、本章小结</h3><p>JOIN + 子查询是 SQL 的第二道门槛（第一道是 GROUP BY）。掌握<strong>四种 JOIN 的语义区别、ON 与 WHERE 的放置位置、派生表、EXISTS</strong>这四个核心概念，你就能解决几乎所有复杂的跨维度取数问题。下一章节将学习窗口函数——SQL 的「第三层功力」，让你在不减少行数的情况下做排名、累计、同环比。</p>''',
                'import sqlite3\nconn = sqlite3.connect(":memory:")\nc = conn.cursor()\nc.execute("CREATE TABLE users (id INT, name TEXT)")\nc.execute("CREATE TABLE orders (uid INT, amt REAL)")\nc.executemany("INSERT INTO users VALUES (?,?)",[(1,"A"),(2,"B"),(3,"C")])\nc.executemany("INSERT INTO orders VALUES (?,?)",[(1,100),(1,200),(2,150),(4,500)])\nconn.commit()\nfor row in c.execute("SELECT u.name, COALESCE(SUM(o.amt),0) FROM users u LEFT JOIN orders o ON u.id=o.uid GROUP BY u.name"):\n    print(row)\nconn.close()',
                [{'q':'LEFT JOIN 右表未匹配？','options':['空字符串','NULL','0','报错'],'answer':1},
                 {'q':'NULL 转 0？','options':['IFNULL/COALESCE','NVL2','EMPTY()','NOT NULL'],'answer':0},
                 {'q':'子查询做派生表写在？','options':['WHERE','FROM 后面','SELECT','不能写'],'answer':1}],
                'import sqlite3\nconn = sqlite3.connect(":memory:")\nc = conn.cursor()\nc.execute("CREATE TABLE dept (id INT, name TEXT)")\nc.execute("CREATE TABLE emp (id INT, name TEXT, dept_id INT, sal REAL)")\nc.executemany("INSERT INTO dept VALUES (?,?)",[(1,"研发"),(2,"市场")])\nc.executemany("INSERT INTO emp VALUES (?,?,?,?)",[(1,"王",1,8000),(2,"李",1,12000),(3,"张",2,9000),(4,"赵",2,10000)])\nconn.commit()\nfor row in c.execute("SELECT d.name, COUNT(*), AVG(e.sal) FROM dept d JOIN emp e ON d.id=e.dept_id GROUP BY d.name"):\n    print(row)\nconn.close()'),
            make_chapter(3, '窗口函数与商业指标', '30 分钟',
                '''<h3>一、窗口函数：SQL 的「第三层功力」</h3><p>标准 GROUP BY 聚合会把 N 行压缩成 K 行（K 是组数）。而窗口函数（Window Function）<strong>保持原有的 N 行不变</strong>，但在每一行上附加一个「窗口内的计算结果」——这个能力在计算排名、同环比、移动平均、累计求和等高级指标时无比强大。</p><p>窗口函数的通用语法结构是：</p><pre><code>函数名(参数) OVER (
    [PARTITION BY 分组字段]
    [ORDER BY 排序字段]
    [ROWS/RANGE BETWEEN ...]
)</code></pre><div class="key-point"><strong>⭐ 核心要点：</strong>窗口函数有四大类：<strong>排名类（ROW_NUMBER/RANK/DENSE_RANK）、聚合类（SUM/AVG/COUNT 等 OVER）、相对位置类（LAG/LEAD/FIRST_VALUE/LAST_VALUE）、分布类（NTILE/PERCENT_RANK）</strong>。掌握排名类 + LAG/LEAD + 累计 SUM OVER，就能解决 90% 的商务分析需求。</div><h3>二、排名类窗口函数</h3><p>排名函数是最常用的窗口函数，区别主要在于「遇到相同值怎么处理」：</p><table><thead><tr><th>函数</th><th>行为</th><th>示例结果（值 100/100/80/70）</th></tr></thead><tbody><tr><td>ROW_NUMBER()</td><td>连续编号，绝不重复</td><td>1, 2, 3, 4</td></tr><tr><td>RANK()</td><td>相同值同排名，跳过被占用名次</td><td>1, 1, 3, 4</td></tr><tr><td>DENSE_RANK()</td><td>相同值同排名，不跳过名次</td><td>1, 1, 2, 3</td></tr><tr><td>NTILE(n)</td><td>均分到 n 个分桶</td><td>1,1,2,2（n=2 时）</td></tr></tbody></table><pre><code>-- 场景：每个城市内按销售额排名
SELECT
    city,
    product_id,
    amount,
    ROW_NUMBER() OVER (PARTITION BY city ORDER BY amount DESC) AS rn,
    RANK()       OVER (PARTITION BY city ORDER BY amount DESC) AS rk,
    DENSE_RANK() OVER (PARTITION BY city ORDER BY amount DESC) AS dr
FROM orders
ORDER BY city, amount DESC;</code></pre><h3>三、聚合类窗口函数：累计与移动平均</h3><p>把普通聚合函数放在 <code>OVER()</code> 后面就变成窗口函数。典型用途：</p><h4>3.1 累计求和（Running Total）</h4><pre><code>-- 每日累计销售额到当前日期
SELECT
    order_date,
    SUM(amount) AS daily_sales,
    SUM(SUM(amount)) OVER (ORDER BY order_date ROWS UNBOUNDED PRECEDING) AS cumulative_sales
FROM orders
GROUP BY order_date
ORDER BY order_date;</code></pre><h4>3.2 组内占比（百分比）</h4><pre><code>-- 各城市销售额及该城市在全国的占比
SELECT
    city,
    SUM(amount) AS city_sales,
    SUM(amount) / SUM(SUM(amount)) OVER () AS pct_of_total
FROM orders
GROUP BY city
ORDER BY city_sales DESC;</code></pre><h4>3.3 7 日移动平均</h4><pre><code>SELECT
    order_date,
    AVG(SUM(amount)) OVER (
        ORDER BY order_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS ma_7d
FROM orders
GROUP BY order_date
ORDER BY order_date;</code></pre><h3>四、LAG / LEAD：同比环比利器</h3><p><code>LAG(col, n)</code> 取「前 n 行的 col 值」，<code>LEAD(col, n)</code> 取「后 n 行的 col 值」。这是计算同环比的标准做法。</p><pre><code>-- 环比：本月 vs 上月
SELECT
    DATE_TRUNC('month', order_date) AS mon,
    SUM(amount) AS monthly_sales,
    LAG(SUM(amount), 1) OVER (ORDER BY DATE_TRUNC('month', order_date)) AS prev_month,
    ROUND(
        (SUM(amount) - LAG(SUM(amount),1) OVER (ORDER BY DATE_TRUNC('month', order_date))) * 100.0
        / NULLIF(LAG(SUM(amount),1) OVER (ORDER BY DATE_TRUNC('month', order_date)), 0),
        2
    ) AS mom_pct
FROM orders
GROUP BY 1
ORDER BY 1;

-- 同比（去年同月）：把 LAG 的偏移量改为 12
LAG(SUM(amount), 12) OVER (ORDER BY mon) AS same_month_last_year</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>在真实工作中，LAG/LEAD + GROUP BY 日期是你最常用的组合。它比你在 Python 里用 df.shift(1) 要快得多，因为可以让数据库在数据源头就做好。</div><h3>五、综合实战：用户价值分层（RFM 简化版）</h3><p>一个经典的商业分析案例：基于 R（最近购买间隔）、F（购买频次）、M（购买金额）为用户打标签：</p><pre><code>WITH user_rfm AS (
    SELECT
        user_id,
        CURRENT_DATE - MAX(order_date) AS recency,      -- R：最近一次到今天的天数
        COUNT(*) AS frequency,                            -- F：总订单数
        SUM(amount) AS monetary                          -- M：总金额
    FROM orders
    GROUP BY user_id
)
SELECT
    user_id,
    recency, frequency, monetary,
    CASE
        WHEN recency  <= 30 AND frequency >= 10 AND monetary >= 2000 THEN '重要价值用户'
        WHEN recency  <= 60 AND frequency >= 5  AND monetary >= 1000 THEN '一般价值用户'
        WHEN recency  > 180 THEN '流失用户'
        ELSE '普通用户'
    END AS user_tier
FROM user_rfm
ORDER BY monetary DESC;</code></pre><h3>六、窗口函数的常见错误</h3><ul><li><strong>窗口别名未复用：</strong>每次都写完整 OVER(...)，可以用 <code>WINDOW w AS (PARTITION BY city ORDER BY amount DESC)</code> 复用</li><li><strong>ORDER BY 缺失：</strong>排名类函数必须有 ORDER BY，累计求和也必须有</li><li><strong>分区错误：</strong>忘了 PARTITION BY 就变成「全表一起排」，结果可能不是你想要的</li><li><strong>性能问题：</strong>大数据表上开多个窗口会触发多次排序，可以先按分区键建索引或用 CTE 减少扫描</li></ul><h3>七、本章小结</h3><p>窗口函数是 SQL 进阶的必学技能。记住三个能力：<strong>排名（ROW_NUMBER/RANK）、累计与占比（SUM OVER）、同环比（LAG/LEAD）</strong>。一旦熟练，你就能用一条 SQL 产出过去在 Excel 里需要花几小时才能完成的分析报告。配合前两章所学的 JOIN 与 GROUP BY，你的 SQL 能力就足以应付绝大多数企业的数据分析岗位要求。</p>''',
                'import sqlite3\nconn = sqlite3.connect(":memory:")\nc = conn.cursor()\nc.execute("CREATE TABLE t (month TEXT, region TEXT, sales REAL)")\nc.executemany("INSERT INTO t VALUES (?,?,?)", [("M1","A",100),("M1","B",150),("M2","A",200),("M2","B",180),("M3","A",250),("M3","B",220)])\nconn.commit()\ntry:\n    for row in c.execute("SELECT month, region, sales, ROW_NUMBER() OVER(PARTITION BY month ORDER BY sales DESC) rk FROM t"):\n        print(row)\nexcept Exception as e:\n    print("SQLite 版本可能不支持窗口函数：", e)\n    print("替代方案：ORDER BY + 应用层排序")\n    for row in c.execute("SELECT month, region, sales FROM t ORDER BY month, sales DESC"):\n        print(row)\nconn.close()',
                [{'q':'组内排名？','options':['SUM() OVER','ROW_NUMBER() OVER / RANK() OVER','MIN() OVER','AVG() OVER'],'answer':1},
                 {'q':'累计求和？','options':['SUM(x) OVER(ORDER BY date ROWS UNBOUNDED PRECEDING)','CUMULATE(x)','TOTAL(x)','RUNSUM(x)'],'answer':0},
                 {'q':'PARTITION BY 类似？','options':['WHERE','GROUP BY 分组逻辑','ORDER BY','LIMIT'],'answer':1}],
                'import sqlite3\nconn = sqlite3.connect(":memory:")\nc = conn.cursor()\nc.execute("CREATE TABLE t (d TEXT, val INT)")\nc.executemany("INSERT INTO t VALUES (?,?)",[("D1",10),("D2",20),("D3",30),("D4",40)])\nconn.commit()\ntotal = 0\nfor d, v in c.execute("SELECT d, val FROM t ORDER BY d"):\n    total += v\n    print(d, v, "累计:", total)\nconn.close()')
        ]
    },
    5: {
        'id': 5, 'title': '统计分析基础', 'icon': '📐',
        'color': '#8e44ad', 'level': '进阶',
        'description': '描述统计、假设检验、相关与回归。',
        'chapters': [
            make_chapter(1, '描述统计', '20 分钟',
                '''<h3>一、什么是描述统计？为什么需要它？</h3><p>面对一堆数据（10,000 个客户的消费金额），人类大脑无法直接理解。描述统计（Descriptive Statistics）的目标就是<strong>用少数几个关键数字来刻画整组数据的特征</strong>。你可以把它理解成「数据的摘要」。</p><p>描述统计主要回答四类问题：</p><ul><li><strong>集中趋势</strong>：数据「中心」在哪里？——均值、中位数、众数</li><li><strong>离散程度</strong>：数据「有多分散」？——极差、方差、标准差、四分位距</li><li><strong>分布形状</strong>：是否对称、有没有极端值？——偏度、峰度、箱线图</li><li><strong>相对位置</strong>：某个值在整体中排第几？——百分位、Z-score</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>永远不要只看均值。均值 + 中位数 + 标准差组合使用，才能对数据有全面的了解。当均值和中位数相差很大时，意味着数据存在严重的偏态或异常值，此时中位数比均值更有代表性。</div><h3>二、集中趋势的三种度量</h3><table><thead><tr><th>度量</th><th>含义</th><th>优点</th><th>缺点</th><th>适用场景</th></tr></thead><tbody><tr><td>均值（Mean）</td><td>所有值之和 ÷ 数量</td><td>利用全部数据信息；数学上易处理</td><td>受极端值影响大</td><td>对称分布的数值数据</td></tr><tr><td>中位数（Median）</td><td>排序后中间那个值</td><td>对异常值不敏感（稳健）</td><td>只用到了排序信息，丢失数值</td><td>有离群值、偏态数据</td></tr><tr><td>众数（Mode）</td><td>出现频率最高的值</td><td>任何类型数据都可算</td><td>可能不唯一；对数值数据不够精细</td><td>分类数据的「中心」</td></tr></tbody></table><pre><code>import numpy as npimport statistics as stdata = [12, 15, 18, 20, 22, 25, 28, 30, 35, 100]print(f"均值:   {np.mean(data):.2f}")     # 30.50（被 100 拉高）print(f"中位数: {np.median(data):.1f}")   # 23.50（更稳健）print(f"众数:   {st.mode(data)}")         # 所有值都只出现一次，返回第一个print(f"下四分位: {np.percentile(data, 25)}")  # 18.5print(f"上四分位: {np.percentile(data, 75)}")  # 29.5</code></pre><h3>三、离散程度：数据「有多散」</h3><h4>3.1 极差（Range）</h4><p>最大值 - 最小值，最简单但对异常值极度敏感。</p><h4>3.2 方差与标准差（Variance & Standard Deviation）</h4><p>方差是每个数据点到均值的平均平方距离。标准差是方差的开方，单位和原始数据一致，更易解释。</p><table><thead><tr><th>类型</th><th>公式</th><th>说明</th></tr></thead><tbody><tr><td>总体方差（σ²）</td><td>Σ(x-μ)² / N</td><td>数据就是全部总体时使用</td></tr><tr><td>样本方差（s²）</td><td>Σ(x-x̄)² / (n-1)</td><td>数据只是样本时使用（除以 n-1 叫贝塞尔校正）</td></tr></tbody></table><div class="warn-box"><strong>⚠ 注意事项：</strong>NumPy 的 <code>np.var()</code> 默认 <code>ddof=0</code>（总体方差），而 Pandas 的 <code>df.var()</code> 默认 <code>ddof=1</code>（样本方差）。同一份数据用两个库算出的方差会不一样，这是新手最容易踩的坑。做数据分析时，通常你手上的是「样本」，请务必用 <code>ddof=1</code>。</div><h4>3.3 四分位距（IQR = Q3 - Q1）</h4><p>中间 50% 数据的跨度，是箱线图的核心，对异常值极其稳健。</p><h3>四、分布形态：偏度与箱线图</h3><h4>4.1 偏度（Skewness）</h3><ul><li><strong>对称分布（Skewness ≈ 0）</strong>：均值 ≈ 中位数 ≈ 众数。典型的是正态分布。</li><li><strong>右偏（正偏，Skewness > 0）</strong>：存在大的极端值将均值向右拉。典型场景：收入、房价、销售额——均值 > 中位数。</li><li><strong>左偏（负偏，Skewness < 0）</strong>：存在小的极端值将均值向左拉。典型场景：考试成绩（满分上限）。</li></ul><h4>4.2 异常值检测（1.5×IQR 规则）</h4><pre><code>Q1 = np.percentile(data, 25)Q3 = np.percentile(data, 75)IQR = Q3 - Q1lower = Q1 - 1.5 * IQRupper = Q3 + 1.5 * IQRoutliers = [x for x in data if x < lower or x > upper]print(f"下界: {lower:.1f}, 上界: {upper:.1f}")print(f"异常值: {outliers}")</code></pre><h3>五、Z-score：把绝对值变成相对位置</h3><p>Z-score 回答「某个值距离均值有多少个标准差」：</p><pre><code>Z = (x - x̄) / s</code></pre><ul><li>Z = 0：正好是均值</li><li>Z = +1：比均值高 1 个标准差（大约比 84% 的数据高）</li><li>Z = -2：比均值低 2 个标准差（大约比 97.5% 的数据低）</li></ul><p>Z-score 的核心价值是<strong>标准化</strong>：可以将不同量纲的数据转换到同一个尺度上做对比。</p><h3>六、Pandas 一行搞定描述统计</h3><pre><code>import pandas as pdimport numpy as npdf = pd.DataFrame({    "销售额": np.random.normal(500, 120, 1000),    "客单价": np.random.normal(120, 30, 1000),    "城市": np.random.choice(["北京","上海","广州","深圳"], 1000)})# 数值列的完整描述summary = df.describe(include="all").round(2)print(summary)# 按城市分组后做描述by_city = df.groupby("城市")["销售额"].agg(    ["count", "mean", "median", "std", "min", "max"]).round(2)print(by_city)</code></pre><div class="tip-box"><strong>💡 小技巧：</strong>分析数据分布时，强烈建议「先画图再写结论」。用 Seaborn 的 <code>sns.boxplot</code> 和 <code>sns.histplot</code>，花 10 秒钟画出来就能发现很多纯数字看不出的问题——比如 bimodal 双峰分布、严重的长尾等。</div><h3>七、本章小结</h3><p>描述统计是所有数据分析的「基本功第一招」。核心记住三件事：<strong>用均值+中位数看中心、用标准差+IQR看离散、用箱线图+直方图看分布</strong>。永远不要只给业务方一个均值——均值掩盖了所有的故事，而标准差、分位数、分布形态才是洞察的起点。</p>''',
                'import numpy as np, statistics as st\ndata = [12,15,18,20,22,25,28,30,35,100]\nprint("均值:", np.mean(data))\nprint("中位数:", np.median(data))\nprint("众数:", st.mode(data))\nprint("方差:", np.var(data, ddof=1))\nprint("标准差:", np.std(data, ddof=1))\nprint("四分位:", np.percentile(data, [25,50,75]))',
                [{'q':'受极端值影响最大？','options':['中位数','均值','众数','四分位'],'answer':1},
                 {'q':'np.percentile(data,50) == ?','options':['均值','中位数','方差','众数'],'answer':1},
                 {'q':'样本方差自由度？','options':['n','n-1','n+1','n/2'],'answer':1}],
                'import numpy as np\nscores = np.array([68,72,75,78,80,82,85,88,90,92,95,100,60,55,77])\nprint("n={} 均值={:.2f} 标准差={:.2f}".format(len(scores), scores.mean(), scores.std(ddof=1)))\nprint("min={} max={}".format(scores.min(), scores.max()))\nprint("25/50/75 分位:", np.percentile(scores, [25,50,75]))'),
            make_chapter(2, '假设检验', '25 分钟',
                '''<h3>一、什么是假设检验？</h3><p>假设检验（Hypothesis Testing）是统计学中最核心的思想之一。它用来回答一个问题：<strong>「我观察到的这个差异，到底是真的有意义，还是只是随机波动？」</strong></p><p>举一个典型的业务例子：你的网站改版后，A 版本转化率 3.1%，B 版本 3.5%。你能断言 B 更好吗？不一定——也许只是今天刚好有一批高意向用户涌入 B 组。假设检验会告诉你：<em>如果真的没有差异，观察到这么大差距的概率是多少</em>。</p><div class="key-point"><strong>⭐ 核心要点：</strong>假设检验的逻辑框架可以用一句话概括：<strong>「先假设没有差异（H0），然后看在这个假设下观察到当前数据的极端程度（p 值），如果极端到低于某个阈值（通常 0.05），就拒绝这个假设，认为差异是真实存在的。」</strong></div><h3>二、核心概念</h3><table><thead><tr><th>概念</th><th>含义</th><th>通俗类比</th></tr></thead><tbody><tr><td>原假设 H0</td><td>「没有差异 / 没有效果」的默认假设</td><td>被告无罪（需要被证伪）</td></tr><tr><td>备择假设 H1</td><td>「存在差异 / 有效果」的假设</td><td>被告有罪（需要证据支持）</td></tr><tr><td>p 值</td><td>如果 H0 为真，观察到当前结果（或更极端）的概率</td><td>无罪情况下出现当前证据的概率</td></tr><tr><td>显著性水平 α</td><td>用来判断 p 值的阈值，通常取 0.05</td><td>「怀疑程度超过 95%」就定罪</td></tr><tr><td>统计显著</td><td>p < α → 拒绝 H0，认为差异真实</td><td>「证据足够，认定有罪」</td></tr><tr><td>不显著</td><td>p ≥ α → 没有足够证据拒绝 H0</td><td>「证据不足，无罪释放」</td></tr></tbody></table><div class="warn-box"><strong>⚠ 常见误解：</strong>「p = 0.04」不代表「有 96% 的概率差异是真实的」。它只代表「如果真的没有差异，观察到当前结果的概率是 4%」。p 值不是 H0 为真的概率，而是数据在 H0 下的稀有度。</div><h3>三、常见检验方法选型</h3><p>不同数据类型和问题场景需要用不同检验方法，下表是业务分析师最常用的 4 个：</p><table><thead><tr><th>问题场景</th><th>推荐检验方法</th><th>Python 函数</th></tr></thead><tbody><tr><td>一组均值 vs 固定值（比如某产品客单价是否=200）</td><td>单样本 t 检验</td><td>scipy.stats.ttest_1samp</td></tr><tr><td>两组独立样本均值对比（A/B 两版转化率）</td><td>独立双样本 t 检验</td><td>scipy.stats.ttest_ind</td></tr><tr><td>成对样本（同一用户前后变化）</td><td>配对样本 t 检验</td><td>scipy.stats.ttest_rel</td></tr><tr><td>两个分类变量是否相关（城市 vs 是否转化）</td><td>卡方检验（Chi-Square）</td><td>scipy.stats.chi2_contingency</td></tr><tr><td>多组均值对比（3+个城市销售额）</td><td>单因素方差分析（ANOVA）</td><td>scipy.stats.f_oneway</td></tr></tbody></table><h3>四、完整案例 1：A/B 测试两版转化率</h3><pre><code>import numpy as npfrom scipy import stats as snp.random.seed(0)# 模拟 A 版：500 个访问，转化率均值 3.1%# 模拟 B 版：500 个访问，转化率均值 3.5%A = np.random.binomial(1, 0.031, 500).astype(float)B = np.random.binomial(1, 0.035, 500).astype(float)# 独立双样本 t 检验t_stat, p_val = s.ttest_ind(A, B, equal_var=False)print(f"t 统计量: {t_stat:.3f}")print(f"p 值: {p_val:.4f}")alpha = 0.05if p_val < alpha:    print(f"✅ p={p_val:.4f} < 0.05，拒绝原假设 → 两版差异统计显著")else:    print(f"⚠️  p={p_val:.4f} ≥ 0.05，证据不足 → 两版差异不显著")# 同时看实际差异幅度print(f"A 均值: {A.mean():.4f}, B 均值: {B.mean():.4f}, 提升: {(B.mean()-A.mean())*100:.2f} 个百分点")</code></pre><h3>五、完整案例 2：卡方检验判断城市与转化是否独立</h3><pre><code># 列联表：行=城市，列=转化/未转化#          转化   未转化# 北京      45    1955# 上海      58    2442# 广州      32    1568obs = [[45, 1955], [58, 2442], [32, 1568]]chi2, p, dof, expected = s.chi2_contingency(obs)print(f"卡方统计量: {chi2:.2f}, p 值: {p:.4f}, 自由度: {dof}")if p < 0.05:    print("✅ 城市与转化率不独立 → 城市差异显著影响转化")else:    print("⚠️  城市与转化率无显著差异")</code></pre><h3>六、第一类错误 vs 第二类错误</h3><p>假设检验可能犯两种错误，理解它们的含义对业务决策至关重要：</p><table><thead><tr><th>类型</th><th>含义</th><th>业务后果</th></tr></thead><tbody><tr><td>第一类错误（Type I / α）</td><td>「其实没有差异，但错误地认为有差异」</td><td>上线无效的改版 → 浪费资源</td></tr><tr><td>第二类错误（Type II / β）</td><td>「其实有差异，但未能检测出来」</td><td>错过好机会 → 本该上线的功能没上</td></tr></tbody></table><p>两者是此消彼长的关系。降低 α（从 0.05 降到 0.01）会减少第一类错误，但增加第二类错误的风险。<strong>样本量越大</strong>，两种错误都能同时降低——这就是为什么做 A/B 测试需要先算最小样本量。</p><h3>七、常见错误清单</h3><ul><li><strong>把「不显著」解读为「没有差异」</strong>：p > 0.05 代表「证据不足」，不代表 H0 为真。也许只是样本不够大。</li><li><strong>把「统计显著」当成「业务上有意义」</strong>：样本量足够大时，极小的差异也会显著，但 0.01% 的转化率提升对业务可能毫无意义。务必同时看效应大小（effect size）。</li><li><strong>多次检验不校正</strong>：对同一份数据做 20 次检验，平均会有 1 次假阳性。用 Bonferroni 校正（α 除以检验次数）。</li><li><strong>数据不符合检验前提</strong>：t 检验假设近似正态分布或大样本；小样本偏态数据用 Mann-Whitney U 非参数检验更合适。</li></ul><h3>八、本章小结</h3><p>假设检验是数据分析「从描述到判断」的关键一跳。核心掌握：<strong>1）原假设/备择假设的逻辑；2）p 值的正确解读；3）t 检验与卡方检验的应用场景；4）样本量与显著性的关系</strong>。有了它，你就能从「看着像」的直觉判断升级为「有统计证据支持」的科学判断。</p>''',
                'import numpy as np\nfrom scipy import stats as s\nnp.random.seed(0)\nA = np.random.normal(100, 10, 50)\nB = np.random.normal(105, 10, 50)\nt_stat, p_val = s.ttest_ind(A, B)\nprint(f"t={t_stat:.3f}, p={p_val:.4f}")\nprint("显著" if p_val < 0.05 else "不显著")',
                [{'q':'p<0.05 一般意味着？','options':['结果正确','可拒绝 H0','数据无效','样本不足'],'answer':1},
                 {'q':'两组独立样本均值？','options':['卡方检验','独立样本 t 检验','ANOVA','Z 检验'],'answer':1},
                 {'q':'检验两变量独立性？','options':['t 检验','卡方检验','F 检验','u 检验'],'answer':1}],
                'import numpy as np\nfrom scipy import stats as s\nnp.random.seed(0)\nctrl = np.random.normal(60, 8, 30)\ntest = np.random.normal(65, 8, 30)\nt_, p = s.ttest_ind(ctrl, test)\nprint(f"t={t_:.3f}, p={p:.4f}")\nprint("显著" if p < 0.05 else "不显著")'),
            make_chapter(3, '相关与回归', '25 分钟',
                '''<h3>一、相关分析：两个变量的关系</h3><p>相关分析（Correlation Analysis）用来回答一个简单问题：<strong>「当 A 变化时，B 是否也跟着变？变化方向和强度如何？」</strong>它是很多分析中最常用的工具之一，也是回归、推荐、因果推断的基础。</p><h4>1.1 Pearson 相关系数 r</h4><p>Pearson r 是最常用的相关系数，衡量两个变量的线性关系强度，取值 [-1, 1]：</p><ul><li>r > 0：正相关（A 越大 B 越大）</li><li>r < 0：负相关（A 越大 B 越小）</li><li>r = 0：无线性相关</li><li>r ≈ ±0.1：弱相关</li><li>r ≈ ±0.3：中等相关</li><li>r ≈ ±0.5：强相关</li></ul><div class="key-point"><strong>⭐ 核心要点：相关 ≠ 因果。</strong>冰淇淋销量和溺水死亡人数高度正相关，但它们都受「夏天」这第三个变量驱动。永远不要把相关关系解读为因果关系。</div><h4>1.2 用 Pandas + NumPy 计算相关矩阵</h4><pre><code>import numpy as np
import pandas as pd

np.random.seed(0)
x = np.random.uniform(10, 50, 100)    # 广告投入
y = 2 + 1.5 * x + np.random.randn(100) * 5  # 销售额

# 1) 两个变量的 Pearson 相关系数
r = np.corrcoef(x, y)[0, 1]
print(f"Pearson r = {r:.3f}")

# 2) 多变量的相关矩阵（常用写法
df = pd.DataFrame({
    "广告投入": np.random.uniform(10, 100, 200),
    "销售额":   np.random.uniform(100, 500, 200),
    "访问量":   np.random.uniform(1000, 5000, 200),
    "客单价":   np.random.uniform(80, 200, 200),
})
print(df.corr().round(3))</code></pre><h4>1.3 相关系数的可视化</h4><pre><code>import seaborn as sns
import matplotlib.pyplot as plt

# 散点图 + 回归线
sns.jointplot(x="广告投入", y="销售额", data=df, kind="reg", height=5)

# 相关矩阵热力图
fig, ax = plt.subplots()
sns.heatmap(df.corr(), annot=True, cmap="coolwarm", center=0)
</code></pre><h3>二、线性回归：从相关到预测</h3><p>相关系数告诉我们「A 和 B 有关系」，而线性回归（Linear Regression）进一步回答「A 变化 1 个单位，B 平均变化多少」，并用一条直线来量化它们的关系。</p><h4>2.1 简单线性回归模型</h4><p>模型形式为：y = a + bx + ε</p><ul><li>y：因变量（被预测变量，比如销售额）</li><li>x：自变量（解释变量，如广告投入）</li><li>a（截距）和 b（斜率）：需要从数据中估计</li><li>ε：噪声（模型无法解释的部分）</li></ul><h4>2.2 用 statsmodels 做完整 OLS 回归</h4><pre><code>import numpy as np
import statsmodels.api as sm

np.random.seed(0)
x = np.random.uniform(10, 50, 30)
y = 2 + 1.5 * x + np.random.randn(30) * 3

# statsmodels 默认不带截距项的列（需要手动加常数项
X = sm.add_constant(x)
model = sm.OLS(y, X).fit()
print(model.summary())</code></pre><h4>2.3 回归输出结果重点看什么？</h4><pre><code>
# 解释三个核心指标
print(f"R² = {model.rsquared:.3f}")
print(f"系数 a (截距): {model.params[0]:.2f}")
print(f"系数 b (广告投入系数): {model.params[1]:.2f}")
print(f"方程: 销售额 = {model.params[0]:.2f} + {model.params[1]:.2f} × 广告投入")</code></pre><h3>三、回归结果解释</h3><table><thead><tr><th>指标</th><th>含义</th><th>推荐阈值</th></tr></thead><tbody><tr><td>R²</td><td>y 的变异中被模型解释的比例</td><td>越接近 1 越好</td></tr><tr><td>系数 b</td><td>x 每增加 1 单位，y 平均变化多少</td><td>符号方向与业务逻辑一致</td></tr><tr><td>p 值（P>|t|）</td><td>系数是否显著不为 0</td><td>< 0.05 则显著</td></tr><tr><td>F 统计量</td><td>整个模型是否显著</td><td>p < 0.05 则整体显著</td></tr></tbody></table><h3>四、回归的 5 个前提假设（LINE）</h3><p>线性回归有5 个核心前提假设（缩写 LINE），不满足时结果会出问题：</p><ul><li><strong>L</strong>inearity（线性）：关系是直线关系</li><li><strong>I</strong>ndependence（独立）：残差独立</li><li><strong>N</strong>ormality（正态）：残差近似正态分布</li><li><strong>E</strong>qual variance（等方差）：残差方差恒定</li></ul><h3>五、多元线性回归（Multiple Regression</h3><pre><code># 用 pandas DataFrame 做多元回归
import statsmodels.formula.api as smf

df = pd.DataFrame({
    "sales": np.random.randn(100)*10+100,
    "ads":  np.random.randn(100)*2+50,
    "price":np.random.randn(100)+10+50,
    "promo": np.random.choice([0, 1], 100)
})

model = smf.ols("sales ~ ads + price + promo", data=df).fit()
print(model.summary().tables[1])</code></pre><h3>六、本章小结</h3><p>相关与回归是数据分析从「描述」升级为「解释」和「预测」的桥梁。要点：</p><ul><li>用相关系数 <strong>衡量关系强度与方向</strong></li><li>用线性回归 <strong>量化变化幅度</strong></li><li>用 R²、p 值、残差分析 <strong>判断模型质量</strong></li><li>永远记住：<strong>相关 ≠ 因果</strong></li></ul><p>掌握这三个工具，你就能回答「什么因素影响最大」「A/B 测试之外的大部分分析需求。</p>''',
                'import numpy as np\nimport statsmodels.api as sm\nnp.random.seed(0)\nx = np.random.uniform(10, 50, 30)\ny = 2 + 1.5 * x + np.random.randn(30) * 3\nX = sm.add_constant(x)\nmodel = sm.OLS(y, X).fit()\nprint("R²:", model.rsquared.round(4))\nprint("系数:", model.params.round(3))\nprint("预测 x=30 时 y:", model.predict([1, 30])[0].round(2))',
                [{'q':'R² 衡量？','options':['速度','可解释方差比例','样本量','p 值'],'answer':1},
                 {'q':'拟合 y=a+bx？','options':['KMeans','statsmodels.OLS / sklearn LinearRegression','Tree','fit()'],'answer':1},
                 {'q':'相关系数 r 范围？','options':['[0,1]','[-1,1]','[0,inf)','任意'],'answer':1}],
                'import numpy as np, statsmodels.api as sm\nnp.random.seed(1)\nx = np.linspace(0, 20, 40)\ny = 5 + 2.2 * x + np.random.randn(40) * 4\nres = sm.OLS(y, sm.add_constant(x)).fit()\nprint("系数:", res.params)\nprint("R²:", res.rsquared.round(3))')
        ]
    },
    6: {
        'id': 6, 'title': '机器学习入门', 'icon': '🤖',
        'color': '#e74c3c', 'level': '进阶',
        'description': '用 scikit-learn 做分类、回归与聚类，从零理解建模流程。',
        'chapters': [
            make_chapter(1, '机器学习导论与 scikit-learn 基础', '25 分钟',
                '''<h3>一、什么是机器学习？为什么它重要？</h3><p>机器学习（Machine Learning）是让计算机<strong>从数据中学习规律</strong>并用这些规律做预测或决策的技术。传统程序是「人写规则 → 机器执行」，机器学习是「人给数据 → 机器自己学规则」。</p><h4>1.1 三大类别</h4><table><thead><tr><th>类别</th><th>核心</th><th>典型业务问题</th><th>代表算法</th></tr></thead><tbody><tr><td><strong>监督学习</strong></td><td>有「正确答案」标签</td><td>客户是否会流失？明天销售额？</td><td>逻辑回归、随机森林、XGBoost</td></tr><tr><td><strong>无监督学习</strong></td><td>没有标签，找结构</td><td>客户分群？异常交易？</td><td>K-Means、层次聚类、PCA</td></tr><tr><td><strong>强化学习</strong></td><td>从反馈中学习策略</td><td>推荐系统排序、自动驾驶</td><td>DQN、PPO</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>对于商务数据分析师，<strong>监督学习中的「分类」与「回归」 + 无监督学习中的「聚类」</strong>是最实用的三件套——它们能直接产出业务价值（流失预警、客群分群、销售额预测等）。</div><h3>二、监督学习的标准工作流</h3><p>所有监督学习项目都遵循相同的 7 步流程，记住它就像记住做菜的步骤一样重要：</p><pre><code>1) 业务理解 → 明确预测目标、评估指标
2) 数据准备 → 清洗缺失值、类型转换、特征工程
3) 训练/测试集切分 → train_test_split
4) 选择模型 → 从简单模型开始（逻辑回归/随机森林）
5) 训练模型 → model.fit(X_train, y_train)
6) 评估模型 → 准确率、AUC、MAE、混淆矩阵
7) 部署/应用 → 把模型用在真实业务</code></pre><h3>三、scikit-learn：入门首选</h3><p>scikit-learn（sklearn）是业界最友好的机器学习库，它的 API 设计极其一致——所有模型都遵循同一个 4 步模式：</p><pre><code># 统一 API 模式
from sklearn.模型类别 import 模型名

# 1) 初始化模型（设置超参数）
model = 模型名(n_estimators=100, random_state=42)

# 2) 在训练集上训练
model.fit(X_train, y_train)

# 3) 在测试集上预测
y_pred = model.predict(X_test)

# 4) 评估
score = model.score(X_test, y_test)  # 或者用 metrics 包</code></pre><h3>四、完整案例：客户流失预测（分类问题）</h3><pre><code>import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report,
    confusion_matrix
)

# 1) 构造模拟数据：1000 个客户，10 个特征（约 20% 流失率）
np.random.seed(42)
X, y = make_classification(
    n_samples=1000, n_features=10, n_informative=5,
    n_redundant=2, n_classes=2, weights=[0.8, 0.2],
    random_state=42
)

# 2) 切分训练/测试集（70%/30% 是行业标准）
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3) 训练：随机森林
clf = RandomForestClassifier(
    n_estimators=100, max_depth=5,
    class_weight="balanced", random_state=42
).fit(X_train, y_train)

# 4) 预测 + 评估
y_pred = clf.predict(X_test)
y_prob = clf.predict_proba(X_test)[:, 1]
print(f"准确率:  {accuracy_score(y_test, y_pred):.3f}")
print(f"精确率:  {precision_score(y_test, y_pred):.3f}")
print(f"召回率:  {recall_score(y_test, y_pred):.3f}")
print(f"F1:      {f1_score(y_test, y_pred):.3f}")
print(f"AUC:     {roc_auc_score(y_test, y_prob):.3f}")
print("\n混淆矩阵:")
print(confusion_matrix(y_test, y_pred))
print("\n分类报告:")
print(classification_report(y_test, y_pred))</code></pre><h3>五、评估指标：比准确率更重要的是什么？</h3><table><thead><tr><th>指标</th><th>含义</th><th>适用场景</th></tr></thead><tbody><tr><td>准确率 Accuracy</td><td>（TP+TN）/总样本</td><td>均衡数据</td></tr><tr><td>精确率 Precision</td><td>被标为正例中，真正是正例的比例</td><td>误判代价高的场景（如垃圾邮件过滤）</td></tr><tr><td>召回率 Recall</td><td>真正正例中被抓出来的比例</td><td>漏检代价高（如流失预警、疾病筛查）</td></tr><tr><td>F1 Score</td><td>精确率与召回率的调和平均</td><td>需要两者平衡时</td></tr><tr><td>AUC</td><td>ROC 曲线下面积</td><td>整体排序能力评估（最推荐）</td></tr></tbody></table><div class="warn-box"><strong>⚠ 注意事项：</strong>在类别不平衡数据中（流失率 20%、点击率 3%），准确率是非常有误导性的指标。比如 98% 的用户不流失，模型「全猜不流失」就能拿到 98% 的准确率，但对业务完全无用。请务必使用 <strong>AUC、召回率、F1</strong> 等指标。</div><h3>六、回归问题模板</h3><pre><code>from sklearn.datasets import make_regression
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

X, y = make_regression(n_samples=500, n_features=10, noise=15, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

for ModelCls, name in [(LinearRegression, "线性回归"), (RandomForestRegressor, "随机森林")]:
    m = ModelCls().fit(X_train, y_train)
    pred = m.predict(X_test)
    print(f"{name}: R²={r2_score(y_test, pred):.3f}, MAE={mean_absolute_error(y_test, pred):.2f}")</code></pre><h3>七、过拟合与欠拟合：模型的两种病</h3><p>一个初学者常陷入的误区：「模型越复杂越准确。」实际情况是这样的：</p><ul><li><strong>欠拟合（Underfitting）</strong>：模型太简单，连训练集都学不好 → 增加特征、换更复杂模型</li><li><strong>过拟合（Overfitting）</strong>：模型把训练集的噪声都学到了，换一批数据就崩 → 增加训练数据、正则化、剪枝、交叉验证</li></ul><p>最实用的检测方法是<strong>交叉验证（Cross-Validation）</strong>：把数据切成 K 份，轮换训练和验证。如果某份数据的表现和训练集差距很大 → 过拟合。</p><h3>八、本章小结</h3><p>机器学习入门并不难——记住 3 件事：</p><ul><li><strong>7 步工作流</strong>（业务理解 → 数据 → 切分 → 选模型 → 训练 → 评估 → 部署）</li><li><strong>scikit-learn 统一 API</strong>（fit/predict/score 三件套）</li><li><strong>用 AUC/F1 而不是准确率</strong>（不平衡数据的黄金准则）</li></ul><p>掌握这些，你就能独立完成一个从 0 到 1 的机器学习项目。</p>''',
                'import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.tree import DecisionTreeClassifier\nfrom sklearn.metrics import accuracy_score, classification_report\nnp.random.seed(0)\nX, y = make_classification(n_samples=500, n_features=8, n_informative=5, n_classes=2)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\nclf = DecisionTreeClassifier(max_depth=5, random_state=42)\nclf.fit(X_train, y_train)\ny_pred = clf.predict(X_test)\nprint("准确率:", accuracy_score(y_test, y_pred).round(3))\nprint(classification_report(y_test, y_pred))',
                [{'q':'fit() 做？','options':['预测','训练模型','输出结果','保存模型'],'answer':1},
                 {'q':'划分训练/测试？','options':['train_test_split','split_data','divide()','train()'],'answer':0},
                 {'q':'分类评估首选？','options':['MAE','准确率 / 混淆矩阵 / F1','R²','余弦相似度'],'answer':1}],
                'import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.metrics import accuracy_score, confusion_matrix\nnp.random.seed(0)\nX, y = make_classification(n_samples=300, n_features=10)\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)\nclf = RandomForestClassifier(n_estimators=50, random_state=42)\nclf.fit(X_train, y_train)\nprint("准确率:", accuracy_score(y_test, clf.predict(X_test)).round(3))\nprint("混淆矩阵:\\n", confusion_matrix(y_test, clf.predict(X_test)))'),
            make_chapter(2, '分类建模与评估', '30 分钟',
                '''<h3>一、分类问题：预测离散标签</h3><p>分类（Classification）是监督学习中最常见的任务之一——输出一个离散标签而非连续数值。典型业务场景包括：</p><ul><li>客户是否会流失？（是 / 否）</li><li>交易是否存在欺诈风险？（高 / 中 / 低）</li><li>客户会购买哪一类产品？（品类 A / B / C / D）</li></ul><h4>1.1 三大常用分类器对比</h4><table><thead><tr><th>模型</th><th>优点</th><th>缺点</th><th>适用场景</th></tr></thead><tbody><tr><td><strong>逻辑回归</strong></td><td>可解释（系数可解读）、训练快、对特征尺度敏感但可标准化</td><td>只能学习线性关系</td><td>首版基线模型；需要向业务解释特征贡献</td></tr><tr><td><strong>随机森林</strong></td><td>对异常值不敏感；非线性关系强；无需特征缩放</td><td>训练慢、文件大、有过拟合风险</td><td>复杂非线性数据；精度优先场景</td></tr><tr><td><strong>XGBoost / LightGBM</strong></td><td>业界竞赛标配；性能强；对缺失值友好</td><td>参数敏感、易过拟合</td><td>结构化数据的高精度要求</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>在任何真实项目中，<strong>请从逻辑回归或简单决策树作为 Baseline（基线）开始</strong>，然后再逐步尝试更复杂的模型。原因有二：1）基线模型训练快、可解释；2）更复杂的模型如果不能显著优于基线，就没有上线意义。</div><h3>二、完整多模型对比案例</h3><pre><code>import numpy as np
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, roc_curve, confusion_matrix
)

np.random.seed(0)
X, y = make_classification(
    n_samples=1000, n_features=12, n_informative=6,
    n_redundant=2, n_classes=2, weights=[0.75, 0.25]
)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 注意：逻辑回归对特征尺度敏感，需标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# 模型对比
models = {
    "逻辑回归": LogisticRegression(max_iter=1000, class_weight="balanced"),
    "随机森林": RandomForestClassifier(n_estimators=100, max_depth=6, class_weight="balanced", n_jobs=-1),
}

results = []
for name, model in models.items():
    X_tr = X_train_scaled if "逻辑" in name else X_train
    X_te = X_test_scaled  if "逻辑" in name else X_test
    model.fit(X_tr, y_train)
    y_pred = model.predict(X_te)
    y_prob = model.predict_proba(X_te)[:, 1]
    cv5 = cross_val_score(model, X_tr, y_train, cv=5, scoring="roc_auc").mean()
    results.append({
        "模型": name,
        "准确率":  accuracy_score(y_test, y_pred).round(3),
        "精确率":  precision_score(y_test, y_pred, zero_division=0).round(3),
        "召回率":  recall_score(y_test, y_pred, zero_division=0).round(3),
        "F1":      f1_score(y_test, y_pred, zero_division=0).round(3),
        "测试AUC": roc_auc_score(y_test, y_prob).round(3),
        "5折CV AUC": cv5.round(3),
    })
for r in results:
    print(r)
</code></pre><h3>三、分类评估指标深度解读</h3><p>评估分类模型的质量，关键是看混淆矩阵（Confusion Matrix）：</p><table><thead><tr><th>n=1000</th><th>预测：正例</th><th>预测：负例</th></tr></thead><tbody><tr><td>实际：正例（250）</td><td>TP=180（真阳性）</td><td>FN=70（假阴性/漏检）</td></tr><tr><td>实际：负例（750）</td><td>FP=60（假阳性/误报）</td><td>TN=690（真阴性）</td></tr></tbody></table><p>基于这个 2×2 表格可以衍生出所有重要指标：</p><pre><code>精确率 Precision = TP / (TP + FP)  → 「我们标为正例的样本中，真正是正例的比例」
召回率   Recall = TP / (TP + FN)   → 「所有真正的正例中，我们成功抓出了多少」
F1 Score  = 2 × P × R / (P + R)    → 两者的调和平均
准确率 Accuracy = (TP+TN)/Total    → 「整体正确率」</code></pre><h3>四、ROC / AUC：不依赖阈值的综合评估</h3><p>ROC 曲线绘制「不同概率阈值下，真阳性率 vs 假阳性率」的轨迹，而 AUC 是曲线下面积。</p><pre><code># 画 ROC 曲线（可选）
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
for name, model in models.items():
    X_te = X_test_scaled if "逻辑" in name else X_test
    y_prob = model.predict_proba(X_te)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_prob)
    ax.plot(fpr, tpr, label=f"{name} AUC={roc_auc_score(y_test, y_prob):.3f}")
ax.plot([0,1],[0,1], "k--", label="随机")
ax.legend()
ax.set_title("ROC 曲线")
</code></pre><h3>五、阈值选择：业务决策的最后一公里</h3><p>模型输出的是 0~1 的概率，最终预测还取决于你选择「概率 ≥ 多少算正例」。默认 0.5 不一定最优：</p><ul><li>漏检代价高（如流失预警、疾病筛查）→ 阈值降低到 0.3，宁可多报，不可漏</li><li>误报代价高（如风控拦截、反欺诈）→ 阈值提高到 0.7，减少误拦</li></ul><h3>六、交叉验证：让评估结果更可信</h3><p>单次 train_test_split 有随机性（换一个 seed 结果可能差很多）。<strong>K 折交叉验证</strong>是行业标准做法：</p><pre><code># 5 折交叉验证，评估 AUC
from sklearn.model_selection import cross_val_score
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="roc_auc")
print(f"5 折 CV AUC: 均值 {cv_scores.mean():.3f}, 标准差 {cv_scores.std():.3f}")
</code></pre><h3>七、本章小结</h3><p>本章讲清了分类问题的完整工作流：1）<strong>从简单模型开始做基线</strong>；2）<strong>用 AUC/F1/精确率/召回率做评估</strong>；3）<strong>用交叉验证判断稳定性</strong>；4）<strong>按业务代价选择概率阈值</strong>。记住：精度不是一切——业务可解释性、训练/推理速度、上线成本同等重要。</p>''',
                'import numpy as np\nfrom sklearn.datasets import load_breast_cancer\nfrom sklearn.model_selection import train_test_split, cross_val_score\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.ensemble import RandomForestClassifier\nfrom sklearn.preprocessing import StandardScaler\ndata = load_breast_cancer()\nX = StandardScaler().fit_transform(data.data); y = data.target\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)\nmodels = {"LogReg": LogisticRegression(max_iter=500), "RF": RandomForestClassifier(n_estimators=80, random_state=42)}\nfor name, m in models.items():\n    m.fit(X_train, y_train)\n    cv = cross_val_score(m, X_train, y_train, cv=5, scoring="roc_auc").mean()\n    print(f"{name}: 测试准确率={m.score(X_test, y_test):.3f}, 训练 AUC={cv:.3f}")',
                [{'q':'不平衡样本优先关注？','options':['准确率','召回率 / F1 / AUC','R²','MAE'],'answer':1},
                 {'q':'逻辑回归输出？','options':['类别标签','概率值 p(y=1|x)','连续整数','树结构'],'answer':1},
                 {'q':'交叉验证做？','options':['cross_val_score','cv()','validate()','kfold()'],'answer':0}],
                'import numpy as np\nfrom sklearn.datasets import make_classification\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import roc_auc_score\nX, y = make_classification(n_samples=600, n_features=10, random_state=0)\nclf = LogisticRegression(max_iter=500).fit(X, y)\ny_prob = clf.predict_proba(X)[:, 1]\nprint("AUC:", roc_auc_score(y, y_prob).round(3))'),
            make_chapter(3, '回归与聚类', '30 分钟',
                '''<h3>一、回归问题：预测连续数值</h3><p>回归（Regression）用来预测一个连续值——「这家店下月销售额多少」「这个客户价值多少」「未来 30 天收入预测」，都是典型的回归问题。</p><h4>1.1 回归与分类的区别</h4><table><thead><tr><th>维度</th><th>分类</th><th>回归</th></tr></thead><tbody><tr><td>输出</td><td>离散标签（0/1、A/B/C）</td><td>连续数值（金额、数量、温度</td></tr><tr><td>评估</td><td>准确率、AUC、F1</td><td>MAE、RMSE、R²</td></tr><tr><td>典型模型</td><td>逻辑回归、随机森林分类</td><td>线性回归、随机森林回归、XGBoost 回归</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>业务中最常见的三种回归评估指标：<strong>MAE（平均绝对误差）越小越好、RMSE（均方根误差）对大误差惩罚更重；R²（决定系数）衡量「模型解释的方差比例，取值 [-inf, 1]，越接近 1 越好。</div><h3>二、完整回归案例：预测销售额</h3><pre><code>import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 模拟一份 500 样本、10 特征的回归数据
X, y = make_regression(n_samples=500, n_features=10, noise=15, random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

# 方案一：线性回归（可解释性强
lr = LinearRegression().fit(X_train, y_train)
pred_lr = lr.predict(X_test)

# 方案二：Ridge（带 L2 正则化线性回归
ridge = Ridge(alpha=1.0).fit(X_train, y_train)
pred_ridge = ridge.predict(X_test)

# 方案三：随机森林回归（非线性
rf = RandomForestRegressor(n_estimators=100, random_state=0).fit(X_train, y_train)
pred_rf = rf.predict(X_test)

# 对比评估
for pred, name in [(pred_lr, "线性回归"), (pred_ridge, "Ridge"), (pred_rf, "随机森林"):
    print(f"{name}: R²={r2_score(y_test, pred):.3f}, MAE={mean_absolute_error(y_test, pred):.2f}, RMSE={np.sqrt(mean_squared_error(y_test, pred)):.2f}")

# 特征重要性（线性回归系数
importance = pd.DataFrame({
    "特征": [f"f{i}" for i in range(X.shape[1])],
    "线性回归系数": lr.coef_.round(2),
    "随机森林重要性": rf.feature_importances_.round(3),
})
print(importance.sort_values("随机森林重要性", ascending=False).to_string())</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>回归问题同样有几个非常容易忽略的问题：1）<strong>变量尺度差异</strong>：线性模型对特征尺度敏感，务必用 StandardScaler 做标准化；2）<strong>对数变换</strong>：像收入、销售额这类长尾分布的目标变量取对数后再建模，性能通常能显著提高表现（因为线性回归假设误差方差恒定；3）<strong>不要用准确率评估回归</strong>：回归不能用准确率做指标。</div><h3>三、聚类分析：无监督的客户分群</h3><p>聚类是无监督学习中最实用的工具——当你没有「客户类型」这样的标签时，让算法自动找出「自己把相似的样本自动归到一类。最常用的是 K-Means。</p><h4>3.1 K-Means 的流程</h4><pre><code>import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_blobs

# 模拟 4 组客户
X, _ = make_blobs(n_samples=300, centers=4, n_features=5, random_state=42)

# 注意：K-Means 基于距离，必须标准化！
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

km = KMeans(n_clusters=4, n_init=10, random_state=42)
labels = km.fit_predict(X_scaled)
</code></pre><h4>3.2 如何选 K：肘部法则（Elbow Method）</h4><pre><code>inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0)
    km.fit(X_scaled)
    inertias.append(km.inertia_)

# 寻找「拐点所在位置即推荐 k 值
for k, val in enumerate(inertias, start=1):
    print(f"k={k}, inertia={val:.1f}")
</code></pre><h4>3.3 给每个客户打标签</h4><pre><code>import pandas as pd
df = pd.DataFrame(X_scaled, columns=["收入评分", "消费频次", "客单价", "最近活跃天数", "品牌忠诚度"])
df["cluster"] = labels
for name, group in df.groupby("cluster"):
    print(f"\n群 {name}: 大小 {len(group)} 人")
    print(group.mean().round(2))</code></pre><h3>四、聚类的常见问题</h3><ul><li><strong>必须标准化</strong>：K-Means 基于欧氏距离，尺度不同会被大尺度变量主导</li><li><strong>选择 k 值</strong>：用肘部法则 / 轮廓系数辅助判断</li><li><strong>类别不均衡</strong>：真实业务中的聚类数量通常不是球形分布，结果要结合业务解释</li><li><strong>只适合标签≠ 不要把聚类结果只能作为特征工程的输入之一

<h3>五、本章小结</h3><p>本章介绍了两个核心：1）<strong>回归预测连续值用 R²、MAE、RMSE 评估</strong>；2）<strong>聚类找客户分群</strong>用 K-Means + 标准化 + 业务解读；3）<strong>聚类结果可作为下游建模特征</strong>。这两套工具是数据分析的核心。</p>''',
                'import numpy as np\nfrom sklearn.datasets import make_regression, make_blobs\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.cluster import KMeans\nfrom sklearn.metrics import r2_score, mean_absolute_error\nnp.random.seed(0)\nX, y = make_regression(n_samples=400, n_features=10, noise=10)\nreg = LinearRegression().fit(X[:300], y[:300])\ny_pred = reg.predict(X[300:])\nprint("线性回归 R²:", r2_score(y[300:], y_pred).round(3), "MAE:", mean_absolute_error(y[300:], y_pred).round(2))\nX2, _ = make_blobs(n_samples=300, centers=4, n_features=5, random_state=42)\nkm = KMeans(n_clusters=4, n_init=10, random_state=42).fit(X2)\nprint("样本 → 聚类:", np.bincount(km.labels_))',
                [{'q':'回归评估？','options':['MAE/RMSE/R²','准确率','F1','混淆矩阵'],'answer':0},
                 {'q':'KMeans 的 n_clusters 指？','options':['迭代次数','聚类数目','特征数','样本量'],'answer':1},
                 {'q':'聚类前需要？','options':['标准化/归一化特征','做 PCA','先做回归','填充 0'],'answer':0}],
                'import numpy as np\nfrom sklearn.datasets import make_regression\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.metrics import mean_absolute_error, r2_score\nnp.random.seed(1)\nX, y = make_regression(n_samples=500, n_features=12, noise=8)\nreg = RandomForestRegressor(n_estimators=60, random_state=0).fit(X[:400], y[:400])\ny_pred = reg.predict(X[400:])\nprint("R²:", r2_score(y[400:], y_pred).round(3), "MAE:", mean_absolute_error(y[400:], y_pred).round(2))')
        ]
    },
    7: {
        'id': 7, 'title': '商业指标体系', 'icon': '📈',
        'color': '#16a085', 'level': '入门',
        'description': '从 GMV、DAU、留存到 AARRR——搭建业务指标体系。',
        'chapters': [
            make_chapter(1, '核心商业指标', '20 分钟',
                '''<h3>一、指标体系：用数字管理业务</h3><p>指标（Metrics）是业务健康度的温度计。它们的核心价值有三点：</p><ul><li><strong>诊断问题</strong>：哪个环节出了问题？</li><li><strong>衡量成果</strong>：我们做对了什么？</li><li><strong>指导行动</strong>：下周应该把精力投入哪里？</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>所有商业指标体系都可以归纳为三层结构：<strong>北极星指标（One Metric That Matters）</strong> → <strong>一级 KPI</strong> → <strong>二级细分指标</strong>。业务方、管理层、数据团队看的是不同层次，但都从同一个北极星指标出发。</div><h3>二、北极星指标（North Star Metric / OMTM）</h3><p>北极星指标是一个单一、最重要、能代表当前阶段「业务是否健康」的指标。选择标准：</p><ul><li><strong>能带来收入</strong>或直接相关</li><li><strong>可度量</strong>（能被准确统计）</li><li><strong>可控</strong>（团队能通过行动影响它）</li></ul><p>不同业务阶段的典型北极星指标：</p><table><thead><tr><th>业务类型</th><th>北极星指标</th><th>解读</th></tr></thead><tbody><tr><td>电商</td><td>GMV（成交总额）</td><td>GMV = 订单数 × 客单价</td></tr><tr><td>社交产品</td><td>DAU（日活跃用户）</td><td>每日至少使用一次的用户数</td></tr><tr><td>SaaS</td><td>MRR（月度经常性收入）</td><td>当月订阅费总和</td></tr><tr><td>内容平台</td><td>用户消费时长</td><td>总观看/阅读时间</td></tr><tr><td>交易平台</td><td>月交易额 / 付费用户数</td><td>平台价值的核心</td></tr></tbody></table><h3>三、从北极星指标展开一级 KPI</h3><p>以电商为例，GMV 可以拆解为：</p><pre><code>GMV = 流量 × 转化率 × 客单价 × 复购率    = (自然流量 + 付费流量 + 私域流量)    × (点击转化率 × 下单转化率 × 支付成功率)    × (品类A客单价 × 品类A占比 + ...)    × (新客占比 × 新客客单价 + 老客占比 × 老客客单价)</code></pre><h3>四、按业务场景分类的核心指标速查表</h3><h4>4.1 收入/销售</h4><table><thead><tr><th>指标</th><th>公式</th><th>含义</th></tr></thead><tbody><tr><td>GMV</td><td>订单金额总和（含取消/退款）</td><td>平台总流水</td></tr><tr><td>净营收</td><td>GMV - 取消/退款 - 优惠</td><td>真实收入</td></tr><tr><td>客单价 AOV</td><td>销售额 / 订单数</td><td>每位客户的平均订单金额</td></tr><tr><td>毛利率</td><td>(销售额 - 成本) / 销售额</td><td>赚钱能力</td></tr></tbody></table><h4>4.2 用户增长</h4><table><thead><tr><th>指标</th><th>公式</th><th>含义</th></tr></thead><tbody><tr><td>DAU / MAU</td><td>日/月活跃用户数</td><td>产品粘性</td></tr><tr><td>新增用户</td><td>首次使用/下单的用户数</td><td>增长速度</td></tr><tr><td>留存率</td><td>第 N 天仍活跃的注册用户占比</td><td>产品吸引力</td></tr><tr><td>获客成本 CAC</td><td>市场费用 / 新增付费用户数</td><td>增长质量</td></tr><tr><td>用户生命周期价值 LTV</td><td>一个客户平均总收入</td><td>长期价值</td></tr></tbody></table><h4>4.3 转化漏斗</h4><table><thead><tr><th>环节</th><th>含义</th></tr></thead><tbody><tr><td>曝光 → 点击率 CTR</td><td>广告/商品吸引力</td></tr><tr><td>浏览 → 加购率</td><td>购买意向</td></tr><tr><td>加购 → 下单率</td><td>结算流程体验</td></tr><tr><td>下单 → 支付率</td><td>支付体验 + 价格</td></tr><tr><td>整体转化率 CVR</td><td>最终下单用户 / 访问用户</td></tr></tbody></table><h3>五、用 Python 计算核心指标（实战代码）</h3><pre><code>import pandas as pdimport numpy as np# 模拟 30 天销售数据dates = pd.date_range("2024-06-01", periods=30)np.random.seed(42)df = pd.DataFrame({    "日期": np.repeat(dates, 200),    "城市": np.tile(np.random.choice(["北京","上海","广州","深圳"], 200), 30),    "品类": np.tile(np.random.choice(["电子","服装","食品","家居","美妆"], 200), 30),    "销售额": np.random.randint(50, 2000, 6000),    "是否新客": np.random.choice([0, 1], 6000, p=[0.85, 0.15]),})# 1) GMV & 日均 GMVtotal_gmv = df["销售额"].sum()daily_gmv = df.groupby("日期")["销售额"].sum()print(f"周期 GMV: ¥{total_gmv:,.0f}，日均 ¥{daily_gmv.mean():,.0f}")# 2) 客单价 AOVorders_per_day = df.groupby("日期").size().mean()aov = total_gmv / (orders_per_day * 30)print(f"平均客单价: ¥{aov:,.2f}")# 3) 各城市销售贡献by_city = df.groupby("城市")["销售额"].sum().sort_values(ascending=False)by_city_pct = (by_city / total_gmv * 100).round(1)print("\n城市销售构成 (%):")print(by_city_pct.to_string())# 4) 新客占比new_cust_ratio = (df["是否新客"].mean() * 100).round(1)print(f"\n新客占比: {new_cust_ratio}%")# 5) 同店环比（本月 vs 上月）this_month = df[df["日期"].dt.month == 6]["销售额"].sum()print(f"本月销售额: ¥{this_month:,.0f}")</code></pre><h3>六、避免指标体系的常见陷阱</h3><ul><li><strong>虚荣指标 vs 可行动指标</strong>：「总用户数 100 万」是虚荣指标，「30 天活跃率 40%」才是可行动指标</li><li><strong>只看绝对值，不看变化</strong>：指标本身不重要，重要的是它的趋势和同比/环比</li><li><strong>指标太多没有重点</strong>：业务方能记住的指标不超过 5 个，其他都是「诊断工具」</li><li><strong>口径不一致</strong>：活跃用户到底是「登录即活跃」还是「有行为算活跃」？全公司必须统一口径</li></ul><h3>七、本章小结</h3><p>好的指标体系是一家公司的「商业GPS」。记住三层结构：<strong>1 个北极星指标 → 5 个一级 KPI → 20 个二级诊断指标</strong>。每一层次对应不同业务场景，但都需要能被量化、能被行动所影响、能被定期追踪。配合课程 8 的 BI 仪表板，就能让指标体系可视化、自动化。</p>''',
                'import pandas as pd, numpy as np\ndf = pd.DataFrame({"date": pd.date_range("2024-06-01", periods=30),\n    "orders": np.random.randint(80,200,30), "aov": np.random.uniform(150,250,30)})\ndf["gmv"] = df.orders * df.aov\nprint("总 GMV: {:.0f}".format(df.gmv.sum()))\nprint("日均 GMV: {:.0f}".format(df.gmv.mean()))\nprint("周均 GMV:\\n", df.set_index("date").gmv.resample("W").sum().round(0))',
                [{'q':'GMV = ?','options':['订单数 × 客单价','用户数 × 留存','DAU × ARPU','销售额 - 成本'],'answer':0},
                 {'q':'电商北极星指标？','options':['页面浏览','GMV / 订单数','员工数','服务器负载'],'answer':1},
                 {'q':'AOV 指？','options':['平均订单金额','用户平均活跃','订单方差','平均运营成本'],'answer':0}],
                'import pandas as pd, numpy as np\ndf = pd.DataFrame({"date": pd.date_range("2024-07-01", periods=60),\n    "users": np.random.randint(2000,5000,60), "orders": np.random.randint(100,400,60),\n    "aov": np.random.uniform(100,300,60)})\ndf["gmv"] = df.orders * df.aov\nprint("月 GMV:\\n", df.set_index("date").gmv.resample("ME").sum().round(0))'),
            make_chapter(2, '用户增长与 AARRR', '25 分钟',
                '''<h3>一、AARRR：用户生命周期的 5 个阶段</h3><p>AARRR（又称「海盗模型」）是增长黑客（Growth Hacker）最经典的用户生命周期分析框架，由 Dave McClure 在 2007 年提出。它把用户从接触产品到付费传播的全流程拆解为 5 个关键阶段，每个阶段对应一个核心动作和一个可量化指标。</p><table><thead><tr><th>阶段</th><th>中文</th><th>业务含义</th><th>核心指标</th></tr></thead><tbody><tr><td><strong>A</strong>cquisition</td><td>获客</td><td>让用户知道并来到产品</td><td>新增用户数 / 获客成本 CAC</td></tr><tr><td><strong>A</strong>ctivation</td><td>激活</td><td>用户第一次体验到核心价值</td><td>激活率 / 首单转化率</td></tr><tr><td><strong>R</strong>etention</td><td>留存</td><td>用户留下来反复使用</td><td>次日 / 7 日 / 30 日留存率</td></tr><tr><td><strong>R</strong>evenue</td><td>变现</td><td>用户为产品付费</td><td>LTV、付费率、ARPU</td></tr><tr><td><strong>R</strong>eferral</td><td>传播</td><td>用户推荐给朋友</td><td>推荐率 / K 系数</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>海盗模型的精髓不是记住这 5 个阶段——而是要识别哪个环节流失最严重、<strong>找到最大的「漏水桶」</strong>。一个典型的漏斗：1000 人访问 → 200 人注册 → 80 人下单 → 30 人复购 → 3 人推荐。每个环节的转化率直接决定最终商业效率。</div><h3>二、获客（Acquisition）</h3><ul><li><strong>渠道结构</strong>：自然流量 / 搜索引擎 / 社交 / 付费投放 / 私域 / 线下…</li><li><strong>核心公式</strong>：ROI = (LTV / CAC，比值越高越好</li><li><strong>陷阱</strong>：只看新增量不看质量——便宜渠道带来的可能是低转化用户，长期不划算</li></ul><h3>三、激活（Activation）：找到 Aha Moment</h3><p>「激活」不是指「登录一次」，而是指用户真正体验到产品核心价值的那一刻。不同产品的 Aha Moment 各不相同：</p><ul><li>Twitter：关注 30 人</li><li>Facebook：7 天内加 10 个好友</li><li>电商：完成第一次下单</li></ul><p><strong>激活率 = 完成激活动作的用户 / 全部新用户</strong></p><h3>四、留存（Retention）：衡量产品粘性的黄金标准</h3><p>留存是增长中最被低估但最重要的指标。没有留存，所有增长只是一个漏水的桶。</p><pre><code>经典留存公式：D1/D7/D30 留存率 = 第 N 天仍活跃的用户 / 总注册用户数周留存 / 月留存同理</code></pre><h4>4.1 留存曲线解读</h4><pre><code>import pandas as pdimport numpy as np# 简化版 cohort（按注册周 × 活跃周留存矩阵np.random.seed(0)cohorts = pd.DataFrame({    "注册月": np.repeat(["2024-01", 5).tolist() + np.repeat(["2024-02", 5).tolist() + np.repeat(["2024-03", 5).tolist(),    "月份偏移": [0,1,2,3,4]*3,    "活跃用户数": [1000,650,450,350,300,800,520,360,280,240,600,400,280,0,0],})for c, g in cohorts.groupby("注册月"):    base = g.loc[g.月份偏移==0,"活跃用户数"].values[0]    print(f"\n注册月 {c} 留存率: {(g.活跃用户数.values / base).round(2)}")</code></pre><h3>五、变现（Revenue）：从用户愿不愿意花钱</h3><table><thead><tr><th>指标</th><th>公式</th><th>含义</th></tr></thead><tbody><tr><td>付费率</td><td>付费用户 / 活跃用户</td><td>付费意愿</td></tr><tr><td>ARPU</td><td>总收入 / 活跃用户数</td><td>每个用户平均收入</td></tr><tr><td>ARPPU</td><td>总收入 / 付费用户数</td><td>付费用户平均收入</td></tr><tr><td>LTV</td><td>ARPU × 用户平均生命周期</td><td>一个客户终身价值</td></tr><tr><td>复购率</td><td>复购用户 / 付费用户</td><td>用户粘性与产品力</td></tr></tbody></table><h3>六、传播（Referral）：病毒式传播</h3><p>推荐/传播指标衡量用户自发推荐行为。常见 K 因子（K-Factor）：</p><pre><code>K = 平均每个用户邀请人数 × 被邀请者转化率若 K > 1 → 病毒式增长；K < 1 → 需要付费买量</code></pre><h3>七、完整 AARRR 计算示例</h3><pre><code># 假设数据：某电商 1 月新注册 10000 人注册月 = 10000激活数     = 4500     # 完成首次下单D30留存 = 1500     # 30 天内再次活跃付费人数   = 800      # 至少付费一次总营收   = 80000    # 这些付费用户总收入推荐人数   = 300      # 至少推荐成功带来新注册人数 = 120</pre><code>print(f"获客:  {注册月} 人激活率:   {激活数/注册月:.2%}D30 留存: {D30留存/激活数:.2%}付费率:   {付费人数/激活数:.2%}ARPPU: ¥{总营收/付费人数:,.0f}推荐率:   {推荐人数/付费人数:.2%}K 因子:  {推荐人数/激活数 * (120/推荐人数):.2f}</code></pre><h3>八、常见陷阱清单</h3><ul><li><strong>只看增长不看留存</strong>：常见陷阱是看增长不看质量——大量一次性用户带来高流失率</li><li><strong>只看活跃不看价值</strong>：活跃不等于付费，高 DAU 不等于高营收</li><li><strong>忽略季节性</strong>：大促当月留存高不是真留存，次月复购率才是真产品力</li><li><strong>LTV 不考虑成本</strong>：LTV 应该是净利润不是总收入，获客成本要扣除</li></ul><h3>九、本章小结</h3><p>AARRR 把复杂的增长问题拆解为 5 个可量化环节，让你精准定位「最大的漏水桶」在哪里。配合下一章节「漏斗分析与 AB 测试」就能把这些环节变成业务增长引擎。</p>''',
                'import pandas as pd, numpy as np\ncohorts = pd.DataFrame({"注册月":["2024-01"]*5+["2024-02"]*5+["2024-03"]*5,\n    "月份偏移":[0,1,2,3,4]*3, "活跃":[1000,650,450,350,300,800,520,360,280,0,600,400,280,0,0]})\nfor c, g in cohorts.groupby("注册月"):\n    base = g.loc[g.月份偏移==0, "活跃"].values[0]\n    print(f"{c} 留存率:", (g.活跃.values / base).round(2))',
                [{'q':'AARRR 第一个 A 指？','options':['Activation','Acquisition','Active','Attribute'],'answer':1},
                 {'q':'留存率 = ?','options':['期末用户 / 期初用户','第 N 期仍活跃 / 期初注册','DAU / MAU','收入 / 用户'],'answer':1},
                 {'q':'MAU / DAU 反映？','options':['用户粘性','收入规模','成本','服务器负载'],'answer':0}],
                'import pandas as pd, numpy as np\ndau = pd.Series(np.random.randint(8000,15000,30), index=pd.date_range("2024-08-01", periods=30))\nprint("DAU 均值:", dau.mean().round(0))\nprint("MAU(该月):", dau.max())\nprint("粘性系数(DAU/MAU): {:.2%}".format(dau.mean() / dau.max()))'),
            make_chapter(3, '漏斗分析与 AB 测试', '25 分钟',
                '''<h3>一、漏斗分析（Funnel Analysis）：找到最大的漏水桶</h3><p>漏斗分析是业务增长诊断最实用的工具之一：把一个多步骤的业务流程拆解成层层递进的「事件 1 → 事件 2 → 事件 3 → …」，然后看每个环节的转化率，定位流失最严重的环节。</p><h4>1.1 典型漏斗：电商下单流程</h4><table><thead><tr><th>步骤</th><th>事件</th><th>人数</th><th>环节转化率</th><th>相对整体</th></tr></thead><tbody><tr><td>1</td><td>商品详情页浏览</td><td>10000</td><td>100%</td><td>100%</td></tr><tr><td>2</td><td>加购</td><td>2500</td><td>25.0%</td><td>25%</td></tr><tr><td>3</td><td>进入结算页</td><td>1500</td><td>60.0%</td><td>15%</td></tr><tr><td>4</td><td>提交订单</td><td>1000</td><td>66.7%</td><td>10%</td></tr><tr><td>5</td><td>支付成功</td><td>800</td><td>80.0%</td><td>8%</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>最大的流失往往不是发生在支付环节，而是<strong>「浏览→加购」这一步</strong>。在本例中，92% 的用户最终没完成购买，其中 75% 直接在第一步就流失了——优先优化它，收益最大。</div><h4>1.2 用 Python 计算漏斗</h4><pre><code>import pandas as pdsteps = ["浏览", "加购", "结算", "下单", "支付"]counts = [10000, 2500, 1500, 1000, 800]funnel = pd.DataFrame({"步骤": steps, "人数": counts})funnel["单步转化率"] = funnel.人数 / funnel.人数.shift(1).fillna(funnel.人数[0])funnel["整体转化率"] = funnel.人数 / funnel.人数.iloc[0]funnel["流失率"] = 1 - funnel.单步转化率print(funnel.round(4))</code></pre><h3>二、A/B 测试：让数据代替「我觉得」</h3><p>A/B 测试（又称对照实验）是把相同用户流量随机切分为两组：一组用老方案（对照组/Control），一组用新方案（实验组/Treatment），通过比较关键指标的差异判断「新方案是否真的更优」。</p><h4>2.1 A/B 测试的基本流程</h4><ul><li><strong>1. 提出假设</strong>：「按钮颜色从蓝色改成红色，能显著提升 CTR。」</li><li><strong>2. 选定指标</strong>：CTR = 点击数 / 浏览数</li><li><strong>3. 计算样本量</strong>：保证有足够的统计功效</li><li><strong>4. 随机切分流量</strong>：A/B 两组</li><li><strong>5. 运行测试</strong>：一般至少需要完整的一周（工作日+周末周期）</li><li><strong>6. 统计检验</strong>：p 值 < 0.05 认为差异显著</li></ul><h4>2.2 用 Python 做 A/B 测试（比例型指标）</h4><pre><code>import numpy as npfrom scipy import stats as st# 对照组：10000 浏览，400 次点击n_control, click_control = 10000, 400# 实验组：10000 浏览，500 次点击n_treat, click_treat = 10000, 500# 比例检验（两独立样本 z 检验）p_control = click_control / n_controlp_treat = click_treat / n_treatp_pool = (click_control + click_treat) / (n_control + n_treat)se = np.sqrt(p_pool * (1 - p_pool) * (1/n_control + 1/n_treat))z = (p_treat - p_control) / sep_value = 2 * st.norm.cdf(-np.abs(z))print(f"对照组 CTR: {p_control:.2%}")print(f"实验组 CTR: {p_treat:.2%}")print(f"z 值: {z:.2f}, p 值: {p_value:.4f}")if p_value < 0.05:    print("✅ 差异显著，可以上线新方案")else:    print("❌ 差异不显著，需进一步观察")</code></pre><h4>2.3 数值型指标（平均客单价）的两样本 t 检验</h4><pre><code># 两组客单价np.random.seed(0)group_a = np.random.normal(200, 60, 200)group_b = np.random.normal(215, 70, 200)t_stat, p_val = st.ttest_ind(group_a, group_b, equal_var=False)print(f"t={t_stat:.3f}, p={p_val:.4f}")print(f"A 组均值 ¥{group_a.mean():.2f}, B 组均值 ¥{group_b.mean():.2f}")</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>A/B 测试最容易犯的几个致命错误：<strong>1）提前偷看结果</strong>——数据量不够就下结论，假阳性率极高；<strong>2）同时测太多指标</strong>——多重比较问题，随机因素容易「显著」；<strong>3）样本量不足</strong>——小差异需要大样本才能检测到；<strong>4）没做随机分配验证</strong>——两组用户画像必须均衡，否则结果不可信。</div><h3>三、统计显著性 vs 业务显著性</h3><table><thead><tr><th>维度</th><th>统计显著</th><th>业务显著</th></tr></thead><tbody><tr><td>判断</td><td>p < 0.05 或 置信区间不包含 0</td><td>提升幅度是否值得投入成本</td></tr><tr><td>含义</td><td>「观测差异不太可能是随机波动造成」</td><td>「差异虽小但业务价值是否足够大」</td></tr><tr><td>决策</td><td>不能直接代替决策</td><td>结合成本-收益决定是否上线</td></tr></tbody></table><h3>四、本章小结</h3><p>漏斗分析帮你「定位哪里出问题」，A/B 测试帮你「验证哪个方案更优」。这两套工具是业务增长的「手术刀」——前者找到病灶，后者做临床实验。使用时要注意：<strong>统计显著不等于业务显著</strong>，也不等于一定要上线，还要结合成本与风险综合评估。</p>''',
                'import pandas as pd\nsteps = pd.DataFrame({"环节":["曝光","点击","加购","下单","支付"], "人数":[100000,25000,8000,4000,3200]})\nsteps["转化率"] = steps.人数 / steps.人数.iloc[0]\nsteps["环节转化"] = steps.人数 / steps.人数.shift(1)\nprint(steps.round(3))\nprint("整体转化率: {:.2%}".format(steps.人数.iloc[-1]/steps.人数.iloc[0]))\n# AB 测试卡方\nfrom scipy.stats import chi2_contingency\nobs = [[320, 10000-320], [380, 10000-380]]  # A, B 转化/未转化\nchi2, p, _, _ = chi2_contingency(obs)\nprint("AB 测试 p={:.4f}".format(p), "显著" if p<0.05 else "不显著")',
                [{'q':'环节之间流失最大点？','options':['最高转化率','最低环节转化率','曝光数','最后环节'],'answer':1},
                 {'q':'AB 测试两比例比较？','options':['卡方检验 / 双比例 z','t 检验','ANOVA','F 检验'],'answer':0},
                 {'q':'AB 测试样本不足？','options':['继续收集到所需样本量','直接看差异','改用均值检验','停止测试'],'answer':0}],
                'import pandas as pd\nfrom scipy.stats import chi2_contingency\nfunnel = pd.DataFrame({"step":["view","click","add","pay"],"users":[50000,12000,4000,3000]})\nfunnel["conv"] = funnel.users / funnel.users.iloc[0]\nprint(funnel)\nobs = [[3000, 50000-3000], [3600, 50000-3600]]\n_, p, _, _ = chi2_contingency(obs)\nprint("AB 试验 p={:.4f}".format(p))')
        ]
    },
    8: {
        'id': 8, 'title': 'BI 仪表板与数据可视化实战', 'icon': '📊',
        'color': '#d35400', 'level': '进阶',
        'description': '用 Plotly Dash / Streamlit 构建可交互的商业仪表板。',
        'chapters': [
            make_chapter(1, 'Plotly 交互图', '25 分钟',
                '''<h3>一、Plotly：让图表动起来的 Python 库</h3><p>Plotly 是一个商业级的数据可视化库，它把 Python 脚本转化为在浏览器中可交互的 HTML+JavaScript 图表。相比 matplotlib，Plotly 的核心优势是：</p><ul><li><strong>交互性</strong>：鼠标悬浮查看详情、缩放、框选、下载 PNG</li><li><strong>美观度</strong>：默认风格就是现代 BI 仪表盘水准</li><li><strong>一键导出</strong>：HTML 文件可直接嵌入任何 BI 工具</li><li><strong>3D/地理图</strong>：对地图、3D 散点、桑基图的原生支持</li></ul><div class="key-point"><strong>⭐ 核心要点：</strong>Plotly 提供两个接口——<strong>plotly.express (px)</strong> 是高层简洁 API（5 行代码出图），<strong>plotly.graph_objects (go)</strong> 是底层灵活 API（精确控制每一个元素）。日常 90% 的场景用 px 就够了。</div><h3>二、Plotly Express 速查：常见图表类型</h3><h4>2.1 折线图（时间趋势）</h4><pre><code>import plotly.express as pximport pandas as pdimport numpy as npdf = pd.DataFrame({    "日期": pd.date_range("2024-01-01", periods=30),    "销售额": np.random.randint(100, 500, 30).cumsum(),    "渠道": np.random.choice(["线上","线下"], 30),})fig = px.line(df, x="日期", y="销售额", color="渠道",              title="销售额时间趋势", markers=True)fig.update_layout(xaxis_title="日期", yaxis_title="销售额（元）")fig.show()</code></pre><h4>2.2 柱状图（分类对比）</h4><pre><code>df2 = pd.DataFrame({"城市":["北京","上海","广州","深圳"], "GMV":[850,760,620,580]})fig = px.bar(df2, x="城市", y="GMV", text="GMV", color="城市",             title="各城市 GMV（万元）")fig.update_traces(textposition="outside")fig.show()</code></pre><h4>2.3 散点图（相关性）</h4><pre><code>df3 = pd.DataFrame({"广告投放": np.random.uniform(10,100,50), "GMV": np.random.uniform(50,300,50)})fig = px.scatter(df3, x="广告投放", y="GMV", trendline="ols", title="投放 vs GMV 相关性")fig.show()</code></pre><h4>2.4 热力图（矩阵关系）</h4><pre><code>import plotly.figure_factory as ffcorr = df3.corr()fig = ff.create_annotated_heatmap(    z=corr.values, x=list(corr.columns), y=list(corr.columns),    colorscale="RdBu", zmin=-1, zmax=1, showscale=True, annotation_text=corr.round(2).values)fig.update_layout(title="特征相关性矩阵")fig.show()</code></pre><h4>2.5 桑基图（业务流向）</h4><pre><code>fig = px.sankey(    node=dict(label=["访问", "浏览", "加购", "下单", "支付", "流失"]),    link=dict(source=[0,0,1,1,2,2,3,3],              target=[1,5,2,5,3,5,4,5],              value=[10000,3000,2500,4500,1500,1000,1000,500]),    title="用户转化漏斗（桑基图）")fig.show()</code></pre><h3>三、导出为 HTML：离线分享</h3><pre><code>fig.write_html("sales_dashboard.html", include_plotlyjs="cdn")</code></pre><h3>四、常见陷阱与最佳实践</h3><ul><li><strong>中文显示</strong>：Plotly 原生支持 UTF-8 中文，只要源字符串是中文就没问题</li><li><strong>大数据量卡顿</strong>：散点图超过 1 万个点会明显变慢，可用 <code>px.scatter</code> 做降采样</li><li><strong>导出文件太大</strong>：用 <code>include_plotlyjs="cdn"</code> 可把文件从 MB 级降到 KB 级</li><li><strong>颜色过饱和</strong>：默认模板 <code>plotly_white</code> 比 <code>plotly_dark</code> 更适合打印</li></ul><h3>五、本章小结</h3><p>Plotly 是 Python 可视化的「瑞士军刀」。配合下一章 Streamlit，<code>px</code> 出图 + <code>st.plotly_chart</code> 就能快速搭建完整的交互式 BI 仪表盘。</p>''',
                'import plotly.express as px\nimport plotly.io as pio\nimport pandas as pd, numpy as np\npio.templates.default = "plotly_white"\nnp.random.seed(0)\ndf = pd.DataFrame({"日期": pd.date_range("2024-01-01", periods=180),\n    "品类": np.tile(["A","B","C"],60), "销售额": np.random.randint(500, 5000, 180)})\nfig = px.line(df, x="日期", y="销售额", color="品类", title="各品类销售趋势")\nfig.write_html("data/sales_trend.html")\nprint("图表已生成: data/sales_trend.html")\nfig2 = px.bar(df.groupby("品类", as_index=False).销售额.sum(), x="品类", y="销售额", color="品类", text="销售额", title="品类销售贡献")\nfig2.write_html("data/sales_bar.html")\nprint("柱状图已生成")',
                [{'q':'Plotly 的核心优势？','options':['速度最快','可输出可交互 HTML','完全无需代码','只支持 Python'],'answer':1},
                 {'q':'快速画多条线？','options':['px.line(..., color="品类")','px.multi()','plt.lines()','plot.multi()'],'answer':0},
                 {'q':'Plotly 保存？','options':['fig.write_html()','fig.save()','fig.dump()','fig.store()'],'answer':0}],
                'import plotly.express as px, plotly.io as pio\npio.templates.default = "plotly_white"\nimport pandas as pd, numpy as np\nnp.random.seed(1)\ndf = pd.DataFrame({"x": np.random.randn(200), "y": np.random.randn(200)*2+10, "g": np.random.choice(["A","B","C"], 200)})\nfig = px.scatter(df, x="x", y="y", color="g", trendline="ols", title="散点图 + OLS 趋势")\nfig.write_html("data/scatter.html")\nprint("散点图已生成")'),
            make_chapter(2, 'Streamlit 极简仪表板', '25 分钟',
                '''<h3>一、Streamlit：把 Python 脚本变成 Web 应用</h3><p>Streamlit 是 2019 年诞生的一款革命性 Python Web 框架，它最吸引人的理念是——<strong>Python 脚本即前端</strong>。你不需要写 HTML/CSS/JavaScript，不需要懂 Flask/Django，只要 10 行 Python 代码就能构建一个可交互的 BI 仪表盘。</p><h4>为什么选 Streamlit？</h4><table><thead><tr><th>维度</th><th>Streamlit</th><th>Plotly Dash</th><th>Grafana</th></tr></thead><tbody><tr><td>学习曲线</td><td>极低（1 小时上手）</td><td>中等（需理解回调机制）</td><td>中等（UI 配置）</td></tr><tr><td>代码量</td><td>最少</td><td>较多</td><td>主要靠 UI 配置</td></tr><tr><td>灵活度</td><td>中</td><td>高</td><td>中</td></tr><tr><td>与 Python 生态融合</td><td>原生支持所有数据工具</td><td>以 Plotly 为中心</td><td>插件体系</td></tr></tbody></table><div class="key-point"><strong>⭐ 核心要点：</strong>Streamlit 的核心机制是「脚本从上到下重跑」——用户每一次交互（改下拉框、点按钮），整个 Python 脚本都会重新执行一遍。虽然简单，但必须理解 <code>st.session_state</code>（跨运行状态）和 <code>@st.cache_data</code>（缓存昂贵操作）才能构建真正的应用。</div><h3>二、核心 API 速查</h3><h4>2.1 文本与数据展示</h4><pre><code>import streamlit as st
import pandas as pd
import numpy as np

st.title("📊 销售 BI 仪表盘")
st.subheader("核心指标概览")
st.write("把表格、图表、Markdown 全部用 st.write 展示")

df = pd.DataFrame({
    "日期": pd.date_range("2024-01-01", periods=10),
    "GMV": np.random.randint(100, 500, 10).cumsum(),
    "订单数": np.random.randint(50, 200, 10),
})
st.dataframe(df, use_container_width=True)
st.metric("本月 GMV", "¥12,345", delta="+8.2%")
</code></pre><h4>2.2 交互式图表</h4><pre><code>import plotly.express as px

fig = px.line(df, x="日期", y="GMV", title="GMV 时间趋势", markers=True)
st.plotly_chart(fig, use_container_width=True)

# 多列布局
col1, col2 = st.columns(2)
with col1:
    st.bar_chart(df.set_index("日期")[["订单数"]])
with col2:
    st.line_chart(df.set_index("日期")[["GMV"]])
</code></pre><h4>2.3 交互控件</h4><pre><code>city = st.selectbox("选择城市", ["全部","北京","上海","广州"])
start, end = st.slider("选择时间段", 1, 30, (1, 30))
threshold = st.number_input("GMV 阈值", min_value=0, value=1000)
if st.button("重新运行"):
    st.success("已更新！")
</code></pre><h3>三、完整 BI 仪表盘模板</h3><pre><code>import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="销售 BI 仪表盘", layout="wide", page_icon="📊")

# 顶部标题
st.title("📊 销售 BI 仪表盘")
st.markdown("实时追踪销售额、订单、客单价与同比环比")

# 侧边栏
with st.sidebar:
    st.header("⚙️ 筛选器")
    channel = st.multiselect("渠道", ["线上","线下"], default=["线上","线下"])
    date_range = st.date_input("日期范围", value=[])

# 模拟数据
np.random.seed(42)
n = 180
df = pd.DataFrame({
    "日期": pd.date_range("2024-06-01", periods=n),
    "渠道": np.random.choice(["线上","线下"], n),
    "销售额": np.random.randint(500, 5000, n),
    "订单数": np.random.randint(30, 200, n),
    "客单价": np.random.uniform(100, 300, n),
})

# KPI 卡片
col1, col2, col3, col4 = st.columns(4)
col1.metric("总销售额", f"¥{df['销售额'].sum():,.0f}", "+8.2%")
col2.metric("总订单数", f"{df['订单数'].sum():,}", "+5.1%")
col3.metric("平均客单价", f"¥{df['客单价'].mean():,.2f}", "+2.3%")
col4.metric("日均值", f"¥{df['销售额'].mean():,.0f}", "+10.5%")

# 图表
tab1, tab2, tab3 = st.tabs(["时间趋势","渠道对比","数据明细"])
with tab1:
    daily = df.groupby("日期", as_index=False).agg({"销售额":"sum","订单数":"sum"})
    fig1 = px.line(daily, x="日期", y="销售额", title="每日销售额趋势", markers=True)
    st.plotly_chart(fig1, use_container_width=True)
with tab2:
    by_channel = df.groupby("渠道", as_index=False).销售额.sum()
    fig2 = px.bar(by_channel, x="渠道", y="销售额", color="渠道", text="销售额", title="渠道销售贡献")
    st.plotly_chart(fig2, use_container_width=True)
with tab3:
    st.dataframe(df.sort_values("日期", ascending=False), use_container_width=True)
</code></pre><h3>四、运行方法</h3><pre><code>pip install streamlit
streamlit run app.py
</code></pre><div class="warn-box"><strong>⚠ 注意事项：</strong>Streamlit 有几个容易踩坑的地方：<strong>1）数据缓存</strong>：用 <code>@st.cache_data</code> 缓存读取操作；<strong>2）会话状态</strong>：用 <code>st.session_state</code> 保存用户交互产生的状态；<strong>3）性能</strong>：大 DataFrame 直接 st.dataframe 会明显变慢，建议分页或降采样；<strong>4）部署</strong>：Streamlit Community Cloud 免费托管，或用 Docker 部署到自己的服务器。</div><h3>五、本章小结</h3><p>Streamlit + Plotly 是当今数据分析团队构建 BI 仪表盘的最佳组合之一。<strong>1 分钟启动、1 小时搭建、1 天迭代</strong>的速度，让你可以专注在分析本身而不是前端技术上。</p>''',
                'dashboard_code = """\n# 保存为 dashboard_run.py\nimport streamlit as st, pandas as pd, numpy as np\nst.set_page_config(page_title="销售仪表盘", layout="wide")\nnp.random.seed(42)\n@st.cache_data\ndef load():\n    return pd.DataFrame({"date": pd.date_range("2024-01-01", periods=120),\n        "region": np.tile(["华北","华东","华南","西南"],30),\n        "category": np.repeat(["电子","服饰","食品","家居"],30),\n        "sales": np.random.randint(1000,10000,120),\n        "profit": np.random.randint(100,3000,120)})\ndf = load()\nst.title("📊 销售仪表盘")\nreg = st.sidebar.multiselect("选择区域", df.region.unique(), default=list(df.region.unique()))\ncat = st.sidebar.multiselect("选择品类", df.category.unique(), default=list(df.category.unique()))\nflt = df[df.region.isin(reg) & df.category.isin(cat)]\nc1, c2, c3 = st.columns(3)\nc1.metric("总销售额", f"{flt.sales.sum():,}")\nc2.metric("总利润", f"{flt.profit.sum():,}")\nc3.metric("订单数", len(flt))\nst.subheader("时间趋势")\nst.line_chart(flt.set_index("date").sales.resample("W").sum())\nst.subheader("区域贡献")\nst.bar_chart(flt.groupby("region").sales.sum())\nwith st.expander("查看明细数据"):\n    st.dataframe(flt, use_container_width=True)\n"""\nwith open("data/dashboard_demo.py","w", encoding="utf-8") as f:\n    f.write(dashboard_code)\nprint("仪表盘脚本已保存到 data/dashboard_demo.py")\nprint("运行: streamlit run data/dashboard_demo.py")',
                [{'q':'Streamlit 部署命令？','options':['python run app.py','streamlit run your_script.py','sl start','launch streamlit'],'answer':1},
                 {'q':'缓存数据？','options':['@st.cache_data','@cache','@save','st.cache()'],'answer':0},
                 {'q':'Streamlit 特色？','options':['脚本即应用，无需写 HTML/CSS','需要前端配合','仅支持 Linux','必须懂 React'],'answer':0}],
                'import pandas as pd, numpy as np\n# 模拟一个最小版仪表盘计算\nnp.random.seed(0)\ndf = pd.DataFrame({"region": np.repeat(["A","B","C","D"], 30),\n    "sales": np.random.randint(100, 1000, 120), "profit": np.random.randint(10, 300, 120)})\nagg = df.groupby("region").agg(total_sales=("sales","sum"), total_profit=("profit","sum"), orders=("sales","count"))\nagg["利润率"] = (agg.total_profit / agg.total_sales * 100).round(2)\nprint("区域汇总:\\n", agg)'),
            make_chapter(3, '设计一个好用的看板', '20 分钟',
                '''<h3>一、从「能看」到「好用」：BI 看板的本质</h3><p>一个真正好用的 BI 看板不是图表的堆砌，而是「帮助业务方在 30 秒内回答一个问题」。好的看板 = 清晰的业务问题 × 简洁的数据呈现 × 可下钻的路径。</p><div class="key-point"><strong>⭐ 核心要点：</strong>看板设计有一个被广泛验证的黄金布局——<strong>「KPI 卡片顶部（看是否正常） → 趋势图中间（看怎么变化） → 细分图 / 明细表底部（看哪里出问题）」</strong>。从上到下、从宏观到微观，这是业务方最自然的思考路径。</div><h3>二、看板设计的 8 条黄金规则</h3><table><thead><tr><th>规则</th><th>说明</th><th>常见错误</th></tr></thead><tbody><tr><td><strong>1. 一张图只讲一个故事</strong></td><td>每一个独立的可视单元只传递一个核心信息</td><td>一张图塞 10 条线、5 个指标</td></tr><tr><td><strong>2. 大数字放顶部</strong></td><td>3-5 个 KPI 卡片作为第一屏，一眼能看是否异常</td><td>顶部直接放复杂图表</td></tr><tr><td><strong>3. 同尺度 + 同配色</strong></td><td>同类数据用相同颜色（例如收入=绿色，成本=橙色）</td><td>同一张报告里颜色含义不一致</td></tr><tr><td><strong>4. 按数值排序</strong></td><td>非时间维度的柱状图，一定要按数值降序/升序</td><td>按字母序、随机序，让读者猜</td></tr><tr><td><strong>5. 数字直接标注</strong></td><td>柱顶、线端直接写数字，不用让读者「用眼睛估读」</td><td>只有图形，没有数值标注</td></tr><tr><td><strong>6. 提供筛选与下钻</strong></td><td>允许按时间、区域、渠道筛选；允许从总览→明细</td><td>只有静态图，没有交互</td></tr><tr><td><strong>7. 标注数据来源与时间</strong></td><td>数据到哪天、来自哪个系统，都要写清楚</td><td>无来源、无时间戳</td></tr><tr><td><strong>8. 同环比不可少</strong></td><td>任何 KPI 都要看「和上周/上月比怎么样」</td><td>只看绝对值，没有比较</td></tr></tbody></table><h3>三、典型销售看板的信息架构</h3><p>以销售型 BI 看板为例，一个信息密度合理的一屏布局应该是：</p><h4>顶部：KPI 卡片（4-5 个）</h4><ul><li>总销售额（含同比/环比）</li><li>总订单数</li><li>客单价</li><li>毛利率</li><li>本月完成率（进度条）</li></ul><h4>中间：趋势 + 结构（2-3 个图）</h4><ul><li>每日 / 每周销售趋势线图</li><li>各区域/各品类销售贡献柱图</li><li>渠道占比饼图或堆叠柱图</li></ul><h4>底部：异常提醒 + 明细表</h4><ul><li>「低于目标 80% 的区域」红色高亮</li><li>Top 10 产品 / Bottom 10 产品表格</li><li>原始明细表（可选下载）</li></ul><h3>四、用 Python 构建一个简单的看板模拟器</h3><pre><code>import pandas as pdimport numpy as npnp.random.seed(42)n = 200df = pd.DataFrame({    "部门": np.tile(["市场","销售","产品","运营","研发"], 40),    "预算": np.repeat([120,180,90,70,150], 40),    "花费": np.random.randint(50, 200, 200),})# 1) 顶部 KPItotal_budget = df["预算"].sum()total_spent  = df["花费"].sum()rate = total_spent / total_budget * 100print(f"🎯 总览: 预算 ¥{total_budget:,.0f} | 实际 ¥{total_spent:,.0f} | 执行率 {rate:.1f}%")# 2) 部门执行率排名agg = df.groupby("部门").agg(    预算=("预算","sum"),    实际=("花费","sum"),).eval("执行率 = 实际 / 预算 * 100").round(1)agg["状态"] = agg.执行率.apply(lambda x: "✅ 正常" if 80<=x<=110 else ("⚠️ 偏低" if x<80 else "🚨 超支"))print("\n部门排名:")print(agg.sort_values("执行率", ascending=False).to_string())# 3) 异常提醒（超预算 110% 的部门）alert = agg[agg.执行率 > 110]if not alert.empty:    print("\n⚠️ 需要关注:")    print(alert[["预算","实际","执行率"]].to_string())</code></pre><h3>五、常见陷阱与最佳实践清单</h3><ul><li><strong>不要做「仪表盘艺术」</strong>：图表 3-5 个就够，太多反而让读者失去焦点</li><li><strong>不要默认降序以外的排序</strong>：除非轴是时间维度，否则一定要按数值排序</li><li><strong>颜色不要超过 5 种</strong>：每多一种颜色，读者的认知负担都会增加</li><li><strong>中文字体缺失会显示方框</strong>：Streamlit/Plotly 部署时，确保服务器安装中文字体（例如 WenQuanYi、思源黑体）</li><li><strong>绝对数字要有比较意义</strong>：单独的「本月销售 100 万」没有意义，必须配合同比/环比/目标</li></ul><h3>六、本章小结</h3><p>好的 BI 看板设计，80% 的精力应该用在「思考业务方真正关心什么」，只有 20% 用在代码与图表上。记住三个原则：<strong>KPI 置顶、趋势为主、筛选下钻</strong>，再配合 Python 数据计算与 Streamlit/Plotly 可视化，你就能产出真正被业务方「每天都打开」的看板。</p>''',
                'import pandas as pd, numpy as np\nnp.random.seed(0)\ndf = pd.DataFrame({"部门":["市场","销售","产品","运营","研发"],\n    "预算":[120,180,90,70,150], "花费":[115,170,88,75,160]})\ndf["执行率"] = (df.花费 / df.预算 * 100).round(1)\ndf["状态"] = df.执行率.apply(lambda x: "✅ 正常" if 80<=x<=110 else ("⚠️ 偏低" if x<80 else "🚨 超支"))\nprint(df.sort_values("执行率", ascending=False).to_string(index=False))\n# 顶部大数字 KPI\ntotal_budget, total_spent = df.预算.sum(), df.花费.sum()\nprint("\\n🎯 KPI 总览: 预算 {} / 花费 {} / 执行率 {:.1f}%".format(total_budget, total_spent, total_spent/total_budget*100))',
                [{'q':'仪表板顶部通常放？','options':['明细表格','大数字 KPI','原始 SQL','服务器日志'],'answer':1},
                 {'q':'多图对比应该？','options':['使用相同尺度与配色','每图不同颜色更花哨','堆叠所有数据','全部用饼图'],'answer':0},
                 {'q':'下钻/筛选的意义？','options':['美化页面','由汇总进入明细，帮助定位问题','增加服务器负载','欺骗老板'],'answer':1}],
                'import pandas as pd, numpy as np\nnp.random.seed(42)\nkpi = pd.DataFrame({"周":["W1","W2","W3","W4","W5","W6"], "GMV":[100,110,130,125,150,165], "DAU":[5000,5200,5500,5400,5800,6200]})\nkpi["GMV_环比%"] = kpi.GMV.pct_change().round(4)*100\nkpi["DAU_环比%"] = kpi.DAU.pct_change().round(4)*100\nprint(kpi.fillna(0))')
        ]
    },
}


# ============================================================
# 10 个项目
# ============================================================
def make_project(pid, title, level, color, duration, dataset, bg, goal, code, starter, tips, pitfalls):
    return {
        'id': pid, 'title': title, 'level': level, 'level_color': color,
        'duration': duration, 'dataset': dataset,
        'background': bg, 'goal': goal,
        'code': code, 'starter_code': starter,
        'tips': tips, 'pitfalls': pitfalls
    }


PROJECTS = {p['id']: p for p in [
    make_project(1,'电商销售数据清洗','初级','success','45 分钟','sales_raw.csv',
        '某电商平台积累了大量原始订单数据，但存在缺失值、重复值、异常值。你需要清洗这些数据。',
        '1) 处理缺失值 2) 去重 3) 识别异常值 4) 输出摘要',
'''import pandas as pd, numpy as np
df = pd.read_csv("data/sales_raw.csv")
print("原始:", len(df))
print("缺失:\\n", df.isnull().sum())
df = df.drop_duplicates()
for col in df.select_dtypes(include=[np.number]).columns:
    df[col] = df[col].fillna(df[col].median())
if "金额" in df.columns:
    q1,q3 = df["金额"].quantile([0.25,0.75])
    iqr = q3 - q1
    df = df[(df["金额"] >= q1 - 1.5*iqr) & (df["金额"] <= q3 + 1.5*iqr)]
print("清洗后:", len(df))
print(df.describe(include="all"))''',
'''import pandas as pd, numpy as np
df = pd.read_csv("data/sales_raw.csv")
print("原始行数:", len(df))
# 继续...''',
        ['先做 df.info() + df.describe()','数值缺失可用中位数，文本缺失视业务','IQR 比 3σ 更稳','drop_duplicates 会完全匹配','保存时保留版本号'],
        ['把日期列当数值处理会 NaN','整表 fillna(0) 会污染字符串','缺失会影响 count 但不影响 sum','SettingWithCopyWarning','忘记重置索引导致错误合并']),
    make_project(2,'销售趋势分析','初级','success','45 分钟','sales_trend.csv',
        '两年多渠道销售数据，需按时间维度分析趋势。',
        '1) 按月汇总 2) 按类别对比 3) 计算环比',
'''import pandas as pd, numpy as np
df = pd.read_csv("data/sales_trend.csv")
df["日期"] = pd.to_datetime(df["日期"])
df["月份"] = df["日期"].dt.to_period("M")
monthly = df.groupby("月份")["销售额"].sum()
print("月度:\\n", monthly.tail(12))
print("类别:\\n", df.groupby("类别")["销售额"].sum().sort_values(ascending=False))
m = monthly.to_frame()
m["环比%"] = m["销售额"].pct_change() * 100
print(m.tail(6).round(2))''',
'''import pandas as pd
df = pd.read_csv("data/sales_trend.csv")
df["日期"] = pd.to_datetime(df["日期"])
# 继续...''',
        ['pd.to_datetime 解析日期','dt.to_period("M") 方便按月分组','pct_change 可算环比','中文需要字体','注意节假日单独标注'],
        ['字符串日期做排序会出错','pct_change 除 0 得 inf','同比要用 shift(12)','忘记先排序导致顺序混乱']),
    make_project(3,'用户消费分层（RFM）','中级','warning','60 分钟','rfm_data.csv',
        '基于 Recency/Frequency/Monetary 进行客户价值分层。',
        '1) 计算 RFM 2) 分位数打分 3) 组合分层',
'''import pandas as pd, numpy as np
df = pd.read_csv("data/rfm_data.csv")
print(df.head())
r = "最近一次消费(天前)" if "最近一次消费(天前)" in df.columns else df.columns[1]
f = "消费频次" if "消费频次" in df.columns else df.columns[2]
m = "消费总金额" if "消费总金额" in df.columns else df.columns[3]
df["R_score"] = pd.qcut(df[r], 5, labels=[5,4,3,2,1]).astype(int)
df["F_score"] = pd.qcut(df[f].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
df["M_score"] = pd.qcut(df[m].rank(method="first"), 5, labels=[1,2,3,4,5]).astype(int)
df["RFM_total"] = df["R_score"] + df["F_score"] + df["M_score"]
def tier(row):
    if row["R_score"]>=4 and row["F_score"]>=4 and row["M_score"]>=4: return "重要价值客户"
    if row["R_score"]<=2 and row["F_score"]>=3: return "流失预警客户"
    if row["R_score"]>=4 and row["F_score"]<=2: return "新客户"
    return "一般客户"
df["分层"] = df.apply(tier, axis=1)
print("\\n分层:\\n", df["分层"].value_counts())''',
'''import pandas as pd
df = pd.read_csv("data/rfm_data.csv")
# 继续 RFM 分析...''',
        ['R 越小越好所以标签反向','rank(method="first") 避免同分位数报错','分层需与业务同学对齐','结果可对接 CRM'],
        ['R 与 F/M 方向搞反','qcut 遇大量相同值报错','apply 全表遍历太慢','极值未截断导致分位数扭曲']),
    make_project(4,'商品关联规则挖掘','中级','warning','60 分钟','transactions.csv',
        '购物篮分析，发现商品组合关系。',
        '1) 整理事务列表 2) 计算支持度/置信度/提升度 3) 找 Top 组合',
'''import pandas as pd
from itertools import combinations
from collections import Counter
df = pd.read_csv("data/transactions.csv")
trans = []
for row in df.itertuples(index=False):
    items = [x for x in row[1:] if pd.notna(x) and str(x).strip()]
    if items: trans.append(items)
print("交易数:", len(trans))
single, pair = Counter(), Counter()
for t in trans:
    for i in set(t): single[i] += 1
    for a,b in combinations(sorted(set(t)), 2): pair[(a,b)] += 1
N = len(trans)
for it, cnt in single.most_common(5):
    print(f"{it}: {cnt/N:.2%}")
rows = []
for (a,b),cab in pair.most_common(30):
    rows.append((a,b,cab/N, cab/single[a], (cab/single[a])/(single[b]/N)))
for a,b,s,c,l in sorted(rows, key=lambda x:-x[4])[:10]:
    print(f"{a} -> {b}: 支持 {s:.2%} 置信 {c:.2%} 提升 {l:.2f}")''',
'''import pandas as pd
from itertools import combinations
from collections import Counter
df = pd.read_csv("data/transactions.csv")
# 继续...''',
        ['三大指标：支持度/置信度/提升度','提升度 > 1 才有正向意义','大规模数据用 mlxtend Apriori','关注低支持高提升长尾组合'],
        ['只看置信度忽略提升度','重复商品未去重','组合数爆炸未做最小支持','只看高频组合而忽略价值']),
    make_project(5,'客户流失预测','高级','danger','75 分钟','churn_data.csv',
        '构建流失预测模型并排序高风险客户。',
        '1) 特征矩阵 2) 训练逻辑回归 3) 评估 4) 概率排序',
'''import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, roc_auc_score
df = pd.read_csv("data/churn_data.csv")
print("样本:", len(df), "流失率:", df["是否流失"].mean())
drop_cols = ["是否流失","客户ID"] + [c for c in df.columns if "ID" in c]
X = df.select_dtypes(include=[np.number]).drop(columns=[c for c in drop_cols if c in df.columns], errors="ignore")
y = df["是否流失"]
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)
sc = StandardScaler(); X_tr_s = sc.fit_transform(X_tr); X_te_s = sc.transform(X_te)
clf = LogisticRegression(max_iter=1000, class_weight="balanced")
clf.fit(X_tr_s, y_tr)
y_pred = clf.predict(X_te_s); y_prob = clf.predict_proba(X_te_s)[:,1]
print(classification_report(y_te, y_pred))
print("AUC:", round(roc_auc_score(y_te, y_prob), 4))
coef = pd.DataFrame({"特征": X.columns, "系数": clf.coef_[0]}).sort_values("系数", key=lambda s: s.abs(), ascending=False)
print(coef.head(10))''',
'''import pandas as pd, numpy as np
from sklearn.linear_model import LogisticRegression
df = pd.read_csv("data/churn_data.csv")
print("流失率:", df["是否流失"].mean())
# 继续...''',
        ['类别不平衡：class_weight="balanced"','评估优先看 AUC/Recall','特征工程比模型更重要','逻辑回归解释性强'],
        ['没做标准化（正则化敏感）','用 accuracy 评估不平衡数据','默认 max_iter 100 不收敛','在全数据集上 fit scaler 导致泄漏']),
    make_project(6,'销售数据仪表板','中级','warning','60 分钟','dashboard_data.csv',
        '为业务团队构建 KPI 与可视化。',
        '1) KPI 2) 区域对比 3) 月度趋势',
'''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
df = pd.read_csv("data/dashboard_data.csv")
total_sales = df["销售额"].sum(); total_orders = df["订单数"].sum()
aov = total_sales / total_orders
print(f"总销售: {total_sales:,.0f} 订单: {total_orders:,} AOV: {aov:,.2f}")
by_region = df.groupby("区域")["销售额"].sum().sort_values(ascending=False)
by_month = df.groupby("月份")["销售额"].sum()
print("区域:\\n", by_region); print("月度:\\n", by_month)
fig, axes = plt.subplots(1, 2, figsize=(12,4))
by_region.plot(kind="bar", ax=axes[0], color="#2980b9", rot=0)
axes[0].set_title("Sales by Region")
by_month.plot(kind="line", ax=axes[1], marker="o", color="#27ae60")
axes[1].grid(alpha=0.3); axes[1].set_title("Sales by Month")
plt.tight_layout()
print("仪表板图表已构建 (真实环境 plt.show() 查看)")''',
'''import pandas as pd
df = pd.read_csv("data/dashboard_data.csv")
# 构建 KPI + 图表...''',
        ['KPI 优先（总销售/订单/客单价/同环比）','图表 3-5 个即可','Plotly Dash 做交互','统一配色'],
        ['中文字体缺失会显示方框','图太多无重点','只看绝对值不看同比环比']),
    make_project(7,'时间序列预测（ARIMA）','高级','danger','75 分钟','timeseries_sales.csv',
        '基于历史销售预测未来 30 天，支持库存决策。',
        '1) 时序探索 2) ARIMA 建模 3) 预测并绘图',
'''import pandas as pd, numpy as np
from statsmodels.tsa.arima.model import ARIMA
df = pd.read_csv("data/timeseries_sales.csv")
df["日期"] = pd.to_datetime(df["日期"]); df = df.set_index("日期").sort_index()
ts = df["历史销售额"].asfreq("D").ffill()
print("序列长度:", len(ts))
model = ARIMA(ts, order=(3,1,3)).fit()
print("AIC:", round(model.aic, 2))
forecast = model.get_forecast(steps=30).summary_frame()
print("\\n未来 30 天预测（前 5 天）:")
print(forecast[["mean"]].head().round(2))
print(f"\\n30 天预测总和: {forecast['mean'].sum():,.2f}")''',
'''import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
df = pd.read_csv("data/timeseries_sales.csv")
df["日期"] = pd.to_datetime(df["日期"])
# 继续 ARIMA 建模...''',
        ['先做平稳性检验（ADF）','用 ACF/PACF 选 AR/MA 阶数','季节性数据用 SARIMA','结合节假日变量'],
        ['未设置频率会报错','阶数过高过拟合','未与业务基准对比','忽略趋势/季节性直接建模']),
    make_project(8,'A/B 测试分析','中级','warning','60 分钟','ab_test_data.csv',
        '新方案 vs 旧方案，用假设检验判断效果。',
        '1) 汇总点击/转化 2) 卡方检验 3) 结论',
'''import pandas as pd, numpy as np
from scipy import stats as s
df = pd.read_csv("data/ab_test_data.csv")
summary = df.groupby("组别").agg(用户数=("用户ID","nunique"), 点击=("是否点击","sum"), 转化=("是否转化","sum")).reset_index()
summary["点击率%"] = (summary["点击"]/summary["用户数"]*100).round(2)
summary["转化率%"] = (summary["转化"]/summary["用户数"]*100).round(2)
print(summary)
# 卡方检验（转化）
table = [[summary.loc[summary["组别"]=="实验组","转化"].iloc[0], summary.loc[summary["组别"]=="实验组","用户数"].iloc[0]-summary.loc[summary["组别"]=="实验组","转化"].iloc[0]],
         [summary.loc[summary["组别"]=="对照组","转化"].iloc[0], summary.loc[summary["组别"]=="对照组","用户数"].iloc[0]-summary.loc[summary["组别"]=="对照组","转化"].iloc[0]]]
chi2, p, dof, ex = s.chi2_contingency(table)
print(f"卡方={chi2:.3f} p={p:.4f}")
print("显著差异" if p < 0.05 else "无显著差异")''',
'''import pandas as pd
from scipy import stats as s
df = pd.read_csv("data/ab_test_data.csv")
# 继续 A/B 测试分析...''',
        ['两变量用卡方/两比例 z 检验','看 p 值 < 0.05','注意样本量是否足够','关注业务显著性（效应量）'],
        ['实验未做随机分配导致偏差','仅看转化忽略点击','多次比较未校正 alpha','提前停止实验']),
    make_project(9,'文本情感分析','高级','danger','75 分钟','reviews.csv',
        '基于评论文本做评分、正负情感、关键词提取。',
        '1) 基础词频 2) 评分分布 3) 简易情感评分',
'''import pandas as pd
from collections import Counter
import re
df = pd.read_csv("data/reviews.csv")
print("评论数:", len(df))
print("平均评分:", round(df["评分"].mean(), 2))
print("评分分布:\\n", df["评分"].value_counts().sort_index())
# 中文分词（简易版：按标点与常见词）
neg_words = set("差 不好 不行 慢 垃圾 失望 问题 糟糕 退换 假 骗 投诉 差评 退货 差 糟糕".split())
pos_words = set("好 棒 赞 喜欢 满意 推荐 不错 快 正品 惊喜 五星 好评 优秀 给力 完美".split())
def score(text):
    words = re.findall(r"[\u4e00-\u9fa5A-Za-z]+", str(text))
    return sum(w in pos_words for w in words) - sum(w in neg_words for w in words)
df["情感分"] = df["评论文本"].apply(score)
print("\\n情感分均值:", round(df["情感分"].mean(), 2))
print("Top 正样本 3 条:")
print(df.sort_values("情感分", ascending=False)[["评论文本","评分"]].head(3).to_string())
print("\\nTop 负样本 3 条:")
print(df.sort_values("情感分")[["评论文本","评分"]].head(3).to_string())''',
'''import pandas as pd, re
df = pd.read_csv("data/reviews.csv")
neg = set("差 不好 慢 垃圾 失望 问题 糟糕".split())
pos = set("好 棒 赞 喜欢 满意 推荐 不错 快 惊喜".split())
# 继续情感分析...''',
        ['中文分词建议 jieba','结合 wordcloud 做词云','需要标注数据时可使用 SnowNLP','用评分作为弱监督信号'],
        ['简易词典法精度有限','标点/表情符号未处理','未考虑否定词（如"不好"）','只看词频忽略上下文']),
    make_project(10,'KMeans 聚类分析','高级','danger','75 分钟','customer_clusters.csv',
        '基于用户年收入与消费评分进行分群，辅助 CRM 运营。',
        '1) 数据标准化 2) 肘部法则选 k 3) KMeans 聚类 4) 结果解读',
'''import pandas as pd, numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
df = pd.read_csv("data/customer_clusters.csv")
print(df.head())
X = df[["年收入(万)","消费评分(1-100)"]].copy()
sc = StandardScaler(); Xs = sc.fit_transform(X)
inertias = []
for k in range(1, 11):
    km = KMeans(n_clusters=k, n_init=10, random_state=0)
    km.fit(Xs); inertias.append(km.inertia_)
print("肘部法则 inertias:", [round(x,1) for x in inertias])
k = 4
km = KMeans(n_clusters=k, n_init=10, random_state=0)
df["cluster"] = km.fit_predict(Xs)
print("\\n各群数量:")
print(df["cluster"].value_counts().sort_index())
print("\\n各群均值:")
print(df.groupby("cluster")[["年收入(万)","消费评分(1-100)"]].mean().round(1))
fig, ax = plt.subplots()
for c in range(k):
    sub = df[df["cluster"]==c]
    ax.scatter(sub["年收入(万)"], sub["消费评分(1-100)"], label=f"Cluster {c}", s=40)
ax.set_xlabel("年收入"); ax.set_ylabel("消费评分"); ax.legend()
ax.set_title("客户 KMeans 聚类")
print("\\n聚类图已构建")''',
'''import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
df = pd.read_csv("data/customer_clusters.csv")
# 继续聚类...''',
        ['聚类前务必标准化','用肘部法则/轮廓系数选 k','特征工程比 k 值更影响结果','结合业务为每个分群命名'],
        ['忘记标准化（尺度大的变量主导）','只依赖默认 k=8','用聚类结果直接做因果推断','未对结果做业务解读']),
]}


# ============================================================
# 综合测评（20 题）
# ============================================================
ASSESSMENT = [
    {'q':'Pandas 中读取 CSV 的函数是？', 'options':['pd.load_csv','pd.read_csv','pd.open_csv','csv.load_pd'], 'answer':1},
    {'q':'以下哪个是 NumPy 的数组类型？', 'options':['list','tuple','ndarray','arraylist'], 'answer':2},
    {'q':'删除缺失值的方法是？', 'options':['df.dropna()','df.nan()','df.clean()','df.rm_nan()'], 'answer':0},
    {'q':'按某列分组后求和的链式调用是？', 'options':['df.groupby("col").sum()','df.sum("col").groupby()','df.gather("col").sum()','df.sum.by("col")'],'answer':0},
    {'q':'左连接保留？', 'options':['两表交集','左表全部记录','右表全部记录','随机记录'], 'answer':1},
    {'q':'IQR 指？', 'options':['最大值-最小值','Q3-Q1','均值-中位数','标准差*2'], 'answer':1},
    {'q':'画柱状图用？', 'options':['plt.bar()','plt.pie()','plt.scatter()','plt.hist()'], 'answer':0},
    {'q':'画热力图最常用的 Seaborn 函数？', 'options':['sns.heatmap','sns.heat','plt.heatmap','sns.hotmap'],'answer':0},
    {'q':'时间序列按周重采样的频率代码？', 'options':['W','D','M','Y'],'answer':0},
    {'q':'滚动 7 天均值用？', 'options':['df.shift(7)','df.rolling(7).mean()','df.diff(7)','df.take(7)'],'answer':1},
    {'q':'SQL 中聚合后过滤用？', 'options':['WHERE','HAVING','IF','GROUP BY'],'answer':1},
    {'q':'样本方差自由度一般用？', 'options':['n','n-1','n+1','n/2'],'answer':1},
    {'q':'p 值 < 0.05 一般意味着？', 'options':['结果一定正确','可拒绝原假设','数据无效','样本太小'], 'answer':1},
    {'q':'比较两组独立样本均值差异常用？', 'options':['卡方检验','独立样本 t 检验','ANOVA','Z 检验'], 'answer':1},
    {'q':'相关系数 r 的范围？', 'options':['[0, 1]','[-1, 1]','[0, +∞)','任意实数'], 'answer':1},
    {'q':'逻辑回归输出常用的评估指标？', 'options':['AUC / F1 / Recall','MAE','R²','余弦相似度'], 'answer':0},
    {'q':'RFM 模型中 R 表示？', 'options':['收益','最近一次消费时间','消费频次','消费金额'], 'answer':1},
    {'q':'客户流失预测中最应关注的指标？', 'options':['AUC / Recall（流失召回率）','准确率','MAE','R²'], 'answer':0},
    {'q':'关联规则中提升度 Lift > 1 表示？', 'options':['负相关','正相关（比随机更可能同时出现）','无关联','等于支持度'], 'answer':1},
    {'q':'KMeans 聚类前最重要的预处理是？', 'options':['归一化/标准化','缺失值填充为 0','复制数据','无需任何处理'], 'answer':0},
]


# ============================================================
# 运行前创建表
# ============================================================
with app.app_context():
    db.create_all()


# ============================================================
# 路由
# ============================================================
@app.context_processor
def inject_user():
    return {'current_user': current_user()}


@app.route('/')
def index():
    u = current_user()
    stats = None
    user_course_stats = {}
    recommendations = []
    recent_items = []
    if u:
        touch_activity(u)
        total_chapters = sum(len(c['chapters']) for c in COURSES.values())
        total_projects = len(PROJECTS)
        done_chapters = ChapterProgress.query.filter_by(user_id=u.id, completed=True).count()
        done_projects = ProjectProgress.query.filter_by(user_id=u.id, completed=True).count()
        badge_ids = set(b.badge_id for b in UserBadge.query.filter_by(user_id=u.id).all())
        for cid, course in COURSES.items():
            total = len(course['chapters'])
            done = 0
            next_ch = course['chapters'][0]['id']
            for i, ch in enumerate(course['chapters']):
                if ChapterProgress.query.filter_by(user_id=u.id, chapter_id=ch['id'], course_id=cid, completed=True).first():
                    done += 1
                else:
                    if next_ch == course['chapters'][0]['id']:
                        next_ch = ch['id']
            if done == total:
                next_ch = None
            user_course_stats[cid] = {'done': done, 'total': total, 'pct': int(done/total*100) if total else 0, 'next_chapter': next_ch, 'next_index': (done % total) + 1 if total else 1}
        for cid, cs in user_course_stats.items():
            if cs['pct'] < 100 and cs['next_chapter']:
                recommendations.append({'type': '课程', 'title': COURSES[cid]['title'], 'sub': '继续第 %d 章' % cs['next_index'], 'url': '/course/%d/chapter/%d' % (cid, cs['next_chapter']), 'icon': 'book', 'pct': cs['pct']})
        for pid, p in PROJECTS.items():
            if not ProjectProgress.query.filter_by(user_id=u.id, project_id=pid, completed=True).first():
                recommendations.append({'type': '项目', 'title': p['title'], 'sub': p['level'] + ' · ' + p['duration'], 'url': '/project/%d' % pid, 'icon': 'rocket', 'pct': 0})
                if len([r for r in recommendations if r['type'] == '项目']) >= 3:
                    break
        recommendations = recommendations[:6]
        recent_cp = ChapterProgress.query.filter_by(user_id=u.id, completed=True).order_by(ChapterProgress.completed_at.desc()).limit(4).all()
        for cp in recent_cp:
            c = COURSES.get(cp.course_id, {})
            chs = c.get('chapters', [])
            ch = next((x for x in chs if x['id'] == cp.chapter_id), None)
            if ch:
                recent_items.append({'kind': '章节', 'title': ch['title'], 'url': '/course/%d/chapter/%d' % (cp.course_id, cp.chapter_id), 'at': cp.completed_at.strftime('%m-%d %H:%M')})
        recent_pp = ProjectProgress.query.filter_by(user_id=u.id, completed=True).order_by(ProjectProgress.completed_at.desc()).limit(3).all()
        for pp in recent_pp:
            p = PROJECTS.get(pp.project_id)
            if p:
                recent_items.append({'kind': '项目', 'title': p['title'], 'url': '/project/%d' % pp.project_id, 'at': pp.completed_at.strftime('%m-%d %H:%M')})
        recent_items.sort(key=lambda x: x['at'], reverse=True)
        recent_items = recent_items[:5]
        stats = {
            'done_chapters': done_chapters, 'total_chapters': total_chapters,
            'done_projects': done_projects, 'total_projects': total_projects,
            'chapter_pct': int(done_chapters/total_chapters*100) if total_chapters else 0,
            'project_pct': int(done_projects/total_projects*100) if total_projects else 0,
            'badges': len(badge_ids), 'total_badges': len(BADGES),
            'badge_ids': badge_ids, 'username': u.username,
            'since': u.created_at.strftime('%Y-%m-%d'),
        }
    total_chapters_count = sum(len(c['chapters']) for c in COURSES.values())
    return render_template('index.html',
                           courses=list(COURSES.values()),
                           projects=list(PROJECTS.values()),
                           stats=stats,
                           user_course_stats=user_course_stats,
                           recommendations=recommendations,
                           recent_items=recent_items,
                           badges_list=list(BADGES.items()),
                           total_chapters_count=total_chapters_count)


# ======== 认证 ========
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        password2 = request.form.get('password2', '')
        if len(username) < 3 or len(password) < 6:
            flash('用户名至少 3 位，密码至少 6 位。', 'warning')
        elif password != password2:
            flash('两次输入的密码不一致。', 'warning')
        elif User.query.filter((User.username == username) | (User.email == email)).first():
            flash('用户名或邮箱已被注册。', 'warning')
        else:
            u = User(username=username, email=email, display_name=username)
            u.set_password(password)
            db.session.add(u); db.session.commit()
            session['user_id'] = u.id
            flash('注册成功！欢迎加入。', 'success')
            check_badges(u)
            return redirect(url_for('index'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        u = User.query.filter((User.username == username) | (User.email == username)).first()
        if u and u.check_password(password):
            session['user_id'] = u.id
            u.last_login = datetime.utcnow()
            db.session.commit()
            check_badges(u)
            flash(f'欢迎回来，{u.display_name}！', 'success')
            return redirect(request.args.get('next') or url_for('index'))
        flash('用户名或密码错误。', 'warning')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('你已退出登录。', 'info')
    return redirect(url_for('index'))


# ======== 课程 ========
@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = COURSES.get(course_id)
    if not course:
        abort(404)
    u = current_user()
    done_chapters = set()
    if u:
        done_chapters = set(c.chapter_id for c in ChapterProgress.query.filter_by(user_id=u.id, course_id=course_id, completed=True).all())
    total = len(course['chapters'])
    done = len(done_chapters)
    next_chapter = None
    for ch in course['chapters']:
        if ch['id'] not in done_chapters:
            next_chapter = ch
            break
    return render_template('course_detail.html', course=course, done_chapters=done_chapters,
                          total=total, done=done, pct=int(done/total*100) if total else 0,
                          next_chapter=next_chapter)


@app.route('/course/<int:course_id>/chapter/<int:chapter_id>')
def chapter_page(course_id, chapter_id):
    course = COURSES.get(course_id)
    if not course: abort(404)
    chapters = course['chapters']
    idx = next((i for i, c in enumerate(chapters) if c['id'] == chapter_id), -1)
    if idx < 0: abort(404)
    chapter = chapters[idx]
    prev_ch = chapters[idx - 1] if idx > 0 else None
    next_ch = chapters[idx + 1] if idx < len(chapters) - 1 else None
    u = current_user()
    is_complete = False
    done_chapters = set()
    if u:
        p = ChapterProgress.query.filter_by(user_id=u.id, course_id=course_id, chapter_id=chapter_id, completed=True).first()
        is_complete = bool(p)
        done_chapters = set(c.chapter_id for c in ChapterProgress.query.filter_by(user_id=u.id, course_id=course_id, completed=True).all())
    return render_template('chapter_page.html', course=course, chapter=chapter,
                          is_complete=is_complete, chapter_index=idx + 1, total_chapters=len(chapters),
                          prev_chapter=prev_ch, next_chapter=next_ch, done_chapters=done_chapters)


@app.route('/api/chapter/complete', methods=['POST'])
@login_required
def api_complete_chapter():
    data = request.get_json() or request.form
    course_id = int(data.get('course_id', 0))
    chapter_id = int(data.get('chapter_id', 0))
    if not COURSES.get(course_id):
        return jsonify({'ok': False, 'error': '课程不存在'})
    u = current_user()
    p = ChapterProgress.query.filter_by(user_id=u.id, course_id=course_id, chapter_id=chapter_id).first()
    if not p:
        p = ChapterProgress(user_id=u.id, course_id=course_id, chapter_id=chapter_id)
        db.session.add(p)
    p.completed = True
    p.completed_at = datetime.utcnow()
    db.session.commit()
    touch_activity(u)
    new_badges = check_badges(u)
    return jsonify({'ok': True, 'new_badges': new_badges})


# ======== 项目 ========
@app.route('/projects')
def projects_list():
    u = current_user()
    done = set()
    if u:
        done = set(pp.project_id for pp in ProjectProgress.query.filter_by(user_id=u.id, completed=True).all())
    return render_template('projects_list.html', projects=list(PROJECTS.values()), done=done)


@app.route('/project/<int:project_id>')
def project_page(project_id):
    project = PROJECTS.get(project_id)
    if not project: abort(404)
    u = current_user()
    is_complete = False
    if u:
        p = ProjectProgress.query.filter_by(user_id=u.id, project_id=project_id, completed=True).first()
        is_complete = bool(p)
    dataset_path = os.path.join(DATA_DIR, project['dataset'])
    dataset_exists = os.path.exists(dataset_path)
    return render_template('project.html', project=project, is_complete=is_complete, dataset_exists=dataset_exists)


@app.route('/data/<path:filename>')
def download_dataset(filename):
    return send_from_directory(DATA_DIR, filename, as_attachment=True)


@app.route('/api/project/complete', methods=['POST'])
@login_required
def api_complete_project():
    data = request.get_json() or request.form
    project_id = int(data.get('project_id', 0))
    if not PROJECTS.get(project_id):
        return jsonify({'ok': False, 'error': '项目不存在'})
    u = current_user()
    p = ProjectProgress.query.filter_by(user_id=u.id, project_id=project_id).first()
    if not p:
        p = ProjectProgress(user_id=u.id, project_id=project_id)
        db.session.add(p)
    p.completed = True
    p.completed_at = datetime.utcnow()
    db.session.commit()
    touch_activity(u)
    new_badges = check_badges(u)
    done_projects = ProjectProgress.query.filter_by(user_id=u.id, completed=True).count()
    return jsonify({'ok': True, 'done_projects': done_projects, 'new_badges': new_badges})


# ======== 代码运行（沙箱：仅展示 stdout）========
@app.route('/api/run_code', methods=['POST'])
def api_run_code():
    data = request.get_json() or request.form
    code = (data.get('code') or '')[:5000]
    old = sys.stdout, sys.stderr
    buf = io.StringIO()
    sys.stdout = buf; sys.stderr = buf
    status, output = 'ok', ''
    try:
        # 限制可执行环境：仅允许白名单模块
        safe_globals = {'__builtins__': __builtins__}
        try:
            import numpy; safe_globals['np'] = numpy
        except Exception: pass
        try:
            import pandas; safe_globals['pd'] = pandas
        except Exception: pass
        try:
            import matplotlib; matplotlib.use('Agg')
            safe_globals['matplotlib'] = matplotlib
            safe_globals['plt'] = matplotlib.pyplot
        except Exception: pass
        exec(code, safe_globals)
    except Exception as e:
        status = 'error'
        print(f"[{type(e).__name__}] {e}")
    finally:
        sys.stdout, sys.stderr = old
    output = buf.getvalue()
    return jsonify({'status': status, 'output': output[-4000:]})


# ======== 测评 ========
@app.route('/assessment', methods=['GET', 'POST'])
def assessment():
    u = current_user()
    if request.method == 'POST':
        if not u:
            flash('请先登录再参与测评。', 'warning')
            return redirect(url_for('login', next='/assessment'))
        correct = 0
        user_answers = []
        for i, q in enumerate(ASSESSMENT):
            ua = request.form.get(f'q{i}')
            try:
                ua = int(ua) if ua is not None else -1
            except Exception:
                ua = -1
            user_answers.append(ua)
            if ua == q['answer']:
                correct += 1
        score = round(correct / len(ASSESSMENT) * 100)
        u.assessment_score = max(u.assessment_score or 0, score)
        db.session.commit()
        new_badges = check_badges(u)
        return render_template('assessment_result.html', score=score, correct=correct,
                              total=len(ASSESSMENT), user_answers=user_answers,
                              questions=ASSESSMENT, new_badges=new_badges)
    return render_template('assessment.html', questions=ASSESSMENT)


# ======== 个人中心 ========
@app.route('/dashboard')
@login_required
def dashboard():
    u = current_user()
    touch_activity(u)
    done_chapters = ChapterProgress.query.filter_by(user_id=u.id, completed=True).count()
    total_chapters = sum(len(c['chapters']) for c in COURSES.values())
    done_projects = ProjectProgress.query.filter_by(user_id=u.id, completed=True).count()
    total_projects = len(PROJECTS)
    badges = [b.badge_key for b in UserBadge.query.filter_by(user_id=u.id).all()]
    return render_template('dashboard.html',
                        stats={
                            'done_chapters': done_chapters, 'total_chapters': total_chapters,
                            'chapter_pct': int(done_chapters/total_chapters*100) if total_chapters else 0,
                            'done_projects': done_projects, 'total_projects': total_projects,
                            'project_pct': int(done_projects/total_projects*100) if total_projects else 0,
                        },
                        badges=badges, BADGES=BADGES)


# ======== 启动 ========
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
