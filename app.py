from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import sys
import io

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bizdata-edu-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///platform.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    last_login = db.Column(db.DateTime)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ChapterProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    chapter_id = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime)

class ProjectProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime)

class Badge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_key = db.Column(db.String(50), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.now)

class AssessmentResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.now)

with app.app_context():
    db.create_all()

COURSES = [
    {
        'id': 1,
        'title': 'Python数据分析基础',
        'description': '从零开始学习Python数据分析，掌握NumPy和Pandas核心技能',
        'level': '入门',
        'duration': '20小时',
        'color': 'primary',
        'chapters': [
            {'id': 1, 'title': 'Python基础语法回顾', 'duration': '2小时'},
            {'id': 2, 'title': 'NumPy数组操作', 'duration': '3小时'},
            {'id': 3, 'title': 'Pandas数据结构', 'duration': '4小时'},
            {'id': 4, 'title': '数据读取与清洗', 'duration': '5小时'},
            {'id': 5, 'title': '数据聚合与统计', 'duration': '6小时'}
        ]
    },
    {
        'id': 2,
        'title': 'Pandas高级数据分析',
        'description': '深入学习Pandas高级技巧，掌握数据处理与分析的进阶方法',
        'level': '进阶',
        'duration': '25小时',
        'color': 'success',
        'chapters': [
            {'id': 6, 'title': '高级索引与选择', 'duration': '3小时'},
            {'id': 7, 'title': '数据透视表与交叉表', 'duration': '4小时'},
            {'id': 8, 'title': '时间序列分析', 'duration': '6小时'},
            {'id': 9, 'title': '数据合并与连接', 'duration': '6小时'},
            {'id': 10, 'title': '性能优化技巧', 'duration': '6小时'}
        ]
    },
    {
        'id': 3,
        'title': '数据可视化(Matplotlib/Seaborn)',
        'description': '学习专业的数据可视化技术，用图表讲述数据故事',
        'level': '进阶',
        'duration': '18小时',
        'color': 'warning',
        'chapters': [
            {'id': 11, 'title': 'Matplotlib基础图表', 'duration': '4小时'},
            {'id': 12, 'title': 'Seaborn统计图表', 'duration': '5小时'},
            {'id': 13, 'title': '图表美化与配色', 'duration': '4小时'},
            {'id': 14, 'title': '交互式可视化', 'duration': '5小时'}
        ]
    },
    {
        'id': 4,
        'title': 'SQL商业数据分析',
        'description': '掌握SQL查询技能，从数据库中提取有价值的商业洞察',
        'level': '入门',
        'duration': '15小时',
        'color': 'info',
        'chapters': [
            {'id': 15, 'title': 'SQL基础语法', 'duration': '3小时'},
            {'id': 16, 'title': '多表连接查询', 'duration': '4小时'},
            {'id': 17, 'title': '聚合与分组', 'duration': '4小时'},
            {'id': 18, 'title': '子查询与窗口函数', 'duration': '4小时'}
        ]
    },
    {
        'id': 5,
        'title': '统计分析基础',
        'description': '学习统计学核心概念，为数据分析奠定坚实基础',
        'level': '入门',
        'duration': '22小时',
        'color': 'danger',
        'chapters': [
            {'id': 19, 'title': '描述统计与概率', 'duration': '5小时'},
            {'id': 20, 'title': '假设检验', 'duration': '6小时'},
            {'id': 21, 'title': '相关与回归分析', 'duration': '6小时'},
            {'id': 22, 'title': 'A/B测试原理', 'duration': '5小时'}
        ]
    }
]

CHAPTERS = {
    1: {'id': 1, 'course_id': 1, 'title': 'Python基础语法回顾', 'duration': '2小时',
        'content': '''<h4>Python语言概述</h4>
<p>Python是一种高级编程语言，由Guido van Rossum于1991年创建。它以简洁的语法、强大的库生态和广泛的应用场景而闻名，特别适合数据分析领域。</p>

<h4>为什么选择Python做数据分析？</h4>
<ul>
<li><strong>简洁易学</strong>：Python语法接近自然语言，学习曲线平缓</li>
<li><strong>丰富的库</strong>：Pandas、NumPy、Matplotlib等库提供了完整的数据分析工具链</li>
<li><strong>活跃社区</strong>：庞大的开发者社区提供了海量的学习资源和解决方案</li>
<li><strong>广泛应用</strong>：从Web开发到机器学习，Python在各领域都有出色表现</li>
</ul>

<h4>Python基本语法要点</h4>
<h5>1. 变量与数据类型</h5>
<pre class="bg-light p-3 rounded"># 变量赋值
name = "数据分析"      # 字符串
count = 100           # 整数
price = 99.9          # 浮点数
is_active = True      # 布尔值

# 查看数据类型
print(type(name))     # &lt;class 'str'&gt;</pre>

<h5>2. 数据结构</h5>
<pre class="bg-light p-3 rounded"># 列表（List）- 可变序列
fruits = ["苹果", "香蕉", "橙子"]
fruits.append("葡萄")  # 添加元素

# 字典（Dictionary）- 键值对
user = {"name": "张三", "age": 25}
print(user["name"])    # 张三

# 元组（Tuple）- 不可变序列
point = (10, 20)

# 集合（Set）- 无序不重复
colors = {"红", "蓝", "绿"}
colors.add("黄")</pre>

<h5>3. 控制流</h5>
<pre class="bg-light p-3 rounded"># 条件判断
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"

# 循环遍历
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# 列表推导式
squares = [x**2 for x in range(10)]</pre>

<h5>4. 函数定义</h5>
<pre class="bg-light p-3 rounded">def calculate_total(prices, tax=0.1):
    """计算总价（含税）"""
    subtotal = sum(prices)
    return subtotal * (1 + tax)

# 调用函数
total = calculate_total([100, 200, 300])
print(f"总价: {total}")</pre>''',
        'code_example': '''def analyze_data(data):
    """数据分析函数"""
    result = []
    for item in data:
        if isinstance(item, (int, float)):
            result.append(item * 2)
    return result

numbers = [1, 2, 3, 4, 5]
processed = analyze_data(numbers)
print(f"原始数据: {numbers}")
print(f"处理结果: {processed}")

doubled = [x * 2 for x in numbers]
print(f"列表推导式: {doubled}")

sales = {"一月": 100, "二月": 150, "三月": 120}
total_sales = sum(sales.values())
print(f"总销售额: {total_sales}")''',
        'tips': [
            '使用 type() 函数可以查看任何变量的数据类型',
            '列表推导式比普通for循环更简洁高效',
            '函数参数可以使用默认值，使调用更灵活',
            '字符串可以用 f"{}" 格式化输出',
            '字典的 values() 方法返回所有值，keys() 返回所有键',
            '使用 enumerate() 可以同时获取索引和值'
        ],
        'quiz': [
            {'q': 'Python中哪个库最适合处理表格数据？', 'options': ['Pandas', 'NumPy', 'Matplotlib', 'Scikit-learn'], 'answer': 0},
            {'q': '安装Python包使用哪个命令？', 'options': ['pip install', 'npm install', 'apt install', 'gem install'], 'answer': 0},
            {'q': 'NumPy数组相比Python列表的主要优势是什么？', 'options': ['更快的向量化运算', '更简洁的语法', '支持更多数据类型', '占用更多内存'], 'answer': 0}
        ]},
    2: {'id': 2, 'course_id': 1, 'title': 'NumPy数组操作', 'duration': '3小时',
        'content': '''<h4>NumPy简介</h4>
<p>NumPy（Numerical Python）是Python科学计算的基础库，提供了高性能的多维数组对象ndarray以及对这些数组进行计算的函数。相比Python原生列表，NumPy数组在存储和计算效率上有显著优势。</p>

<h4>为什么使用NumPy？</h4>
<ul>
<li><strong>性能高效</strong>：底层使用C语言实现，向量化运算比Python循环快数十到数百倍</li>
<li><strong>内存优化</strong>：NumPy数组存储在连续内存块中，比列表更节省内存</li>
<li><strong>功能强大</strong>：提供线性代数、傅里叶变换、随机数生成等数学函数</li>
<li><strong> Broadcasting</strong>：支持不同形状数组间的运算，无需显式循环</li>
</ul>

<h4>NumPy数组基础</h4>
<h5>1. 创建数组</h5>
<pre class="bg-light p-3 rounded">import numpy as np

# 从列表创建
arr1 = np.array([1, 2, 3, 4, 5])
arr2d = np.array([[1, 2, 3], [4, 5, 6]])

# 创建特殊数组
zeros = np.zeros((3, 4))      # 全零数组
ones = np.ones((2, 3))        # 全一数组
range_arr = np.arange(0, 10, 2)  # 0到10，步长2
linspace = np.linspace(0, 1, 5)   # 0到1，等分5份

print("一维数组:", arr1)
print("二维数组形状:", arr2d.shape)</pre>

<h5>2. 数组属性</h5>
<pre class="bg-light p-3 rounded">arr = np.array([[1, 2, 3], [4, 5, 6]])

print("形状:", arr.shape)      # (2, 3)
print("维度:", arr.ndim)      # 2
print("元素数:", arr.size)    # 6
print("数据类型:", arr.dtype)  # int64

# 重塑数组
reshaped = arr.reshape(3, 2)
print("重塑后:", reshaped.shape)</pre>

<h5>3. 数组索引与切片</h5>
<pre class="bg-light p-3 rounded">arr = np.arange(10)  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print("前5个:", arr[:5])      # [0, 1, 2, 3, 4]
print("最后3个:", arr[-3:])    # [7, 8, 9]
print("奇数索引:", arr[::2])   # [0, 2, 4, 6, 8]
print("反转:", arr[::-1])     # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

# 二维数组索引
arr2d = np.array([[1,2,3], [4,5,6], [7,8,9]])
print("第2行:", arr2d[1, :])   # [4, 5, 6]</pre>

<h5>4. 数组运算</h5>
<pre class="bg-light p-3 rounded">a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# 元素级运算
print("加法:", a + b)     # [5, 7, 9]
print("乘法:", a * b)     # [4, 10, 18]
print("幂运算:", a ** 2)   # [1, 4, 9]

# 聚合函数
print("求和:", arr.sum())    # 45
print("均值:", arr.mean())   # 4.5
print("最大值:", arr.max())  # 9
print("标准差:", arr.std())  # 2.872...</pre>''',
        'code_example': '''arr = [1, 2, 3, 4, 5]

result = [x * 2 + 1 for x in arr]
print("原始数组:", arr)
print("运算结果 (x*2+1):", result)

print("前3个:", arr[:3])
print("最后2个:", arr[-2:])
print("反转:", arr[::-1])

print("求和:", sum(arr))
print("均值:", sum(arr) / len(arr))
print("最大值:", max(arr))
print("最小值:", min(arr))''',
        'tips': [
            'np.array() 从列表创建数组，列表元素类型决定dtype',
            'np.arange(start, stop, step) 类似 range()，但返回数组',
            'np.zeros() 和 np.ones() 用于创建固定形状的数组',
            '数组切片 arr[::2] 表示步长为2，arr[::-1] 表示反转',
            '聚合函数 sum(), mean(), std(), max(), min() 可指定 axis 参数',
            '使用 arr.reshape() 重塑数组，新形状必须与原元素数相同'
        ],
        'quiz': [
            {'q': 'NumPy中创建全零数组的函数是？', 'options': ['np.zeros()', 'np.ones()', 'np.empty()', 'np.full()'], 'answer': 0},
            {'q': '数组形状为(3, 4)的矩阵有多少个元素？', 'options': ['12', '7', '34', '无法确定'], 'answer': 0},
            {'q': 'np.dot()函数用于计算什么？', 'options': ['矩阵乘法', '点积', '逐元素乘积', '矩阵求逆'], 'answer': 1}
        ]},
    3: {'id': 3, 'course_id': 1, 'title': 'Pandas数据结构', 'duration': '4小时',
        'content': '''<h4>Pandas简介</h4>
<p>Pandas是Python数据分析的核心库，由Wes McKinney于2008年开发。它提供了高性能、易用的数据结构和数据分析工具，特别适合处理表格型数据（如SQL表格、Excel数据）。</p>

<h4>为什么使用Pandas？</h4>
<ul>
<li><strong>数据读取</strong>：支持CSV、Excel、SQL、JSON等多种格式</li>
<li><strong>数据清洗</strong>：处理缺失值、重复值、异常值方便</li>
<li><strong>数据分析</strong>：分组聚合、透视表、统计计算强大</li>
<li><strong>数据可视化</strong>：与Matplotlib、Seaborn无缝集成</li>
</ul>

<h4>Pandas核心数据结构</h4>
<h5>1. Series（系列）</h5>
<p>Series是带索引的一维数组，类似于Excel中的一列或Python中的字典。</p>
<pre class="bg-light p-3 rounded">import pandas as pd

# 从列表创建Series
s = pd.Series([10, 20, 30, 40], index=['a', 'b', 'c', 'd'])
print(s)
print("索引:", s.index.tolist())
print("值:", s.values)

# 从字典创建Series
data = {"苹果": 100, "香蕉": 80, "橙子": 120}
fruits = pd.Series(data)
print("\\n水果销量:")
print(fruits)

# Series运算
print("\\n加10:", fruits + 10)</pre>

<h5>2. DataFrame（数据框）</h5>
<p>DataFrame是带标签的二维表格数据结构，类似于Excel表格或SQL表。</p>
<pre class="bg-light p-3 rounded"># 创建DataFrame
data = {
    "姓名": ["张三", "李四", "王五", "赵六"],
    "年龄": [25, 30, 35, 28],
    "城市": ["北京", "上海", "广州", "深圳"],
    "薪资": [15000, 20000, 18000, 22000]
}
df = pd.DataFrame(data)
print(df)

# 设置索引
df.index = ["A", "B", "C", "D"]
print("\\n设置索引后:")
print(df)

# DataFrame属性
print("\\n列名:", df.columns.tolist())
print("形状:", df.shape)
print("数据类型:\\n", df.dtypes)</pre>

<h5>3. 数据选择</h5>
<pre class="bg-light p-3 rounded"># 选择列
print(df["姓名"])          # 单列
print(df[["姓名", "薪资"]])  # 多列

# 选择行 - 标签索引
print(df.loc["A"])

# 选择行 - 位置索引
print(df.iloc[0:2])       # 前2行

# 条件筛选
print(df[df["薪资"] > 18000])
print(df[(df["年龄"] > 25) & (df["城市"] == "北京")])</pre>

<h5>4. 数据查看方法</h5>
<pre class="bg-light p-3 rounded"># 查看数据概览
print(df.head())      # 前5行
print(df.tail())      # 后5行
print(df.info())     # 数据类型和非空值
print(df.describe())  # 数值列统计

# 数值统计
print(df["薪资"].mean())   # 平均值
print(df["薪资"].median()) # 中位数
print(df["年龄"].min())    # 最小值
print(df["年龄"].max())    # 最大值</pre>''',
        'code_example': '''data = [
    {"姓名": "张三", "年龄": 25, "城市": "北京", "薪资": 15000},
    {"姓名": "李四", "年龄": 30, "城市": "上海", "薪资": 20000},
    {"姓名": "王五", "年龄": 35, "城市": "广州", "薪资": 18000},
]

print("=== 数据表 ===")
for row in data:
    print(row)

print("\\n=== 选择列 ===")
names = [d["姓名"] for d in data]
print("姓名:", names)

print("\\n=== 筛选条件 ===")
filtered = [d for d in data if d["薪资"] > 15000]
print("薪资>15000的员工:")
for p in filtered:
    print(f"  {p['姓名']}: ¥{p['薪资']}")

print("\\n=== 统计 ===")
ages = [d["年龄"] for d in data]
salaries = [d["薪资"] for d in data]
print(f"年龄范围: {min(ages)}-{max(ages)}")
print(f"平均薪资: {sum(salaries)/len(salaries):.0f}")''',
        'tips': [
            'Series和DataFrame都有index属性，可以自定义索引',
            'df["列名"] 返回Series，df[["列1", "列2"]] 返回DataFrame',
            'loc[] 基于标签索引，iloc[] 基于整数位置索引',
            'head(n) 和 tail(n) 分别查看前n行和后n行',
            'describe() 只对数值列显示统计信息',
            '使用 df.copy() 创建副本，避免修改原数据'
        ],
        'quiz': [
            {'q': 'Pandas中表示一维数据的对象是？', 'options': ['Series', 'DataFrame', 'Array', 'List'], 'answer': 0},
            {'q': 'df.head()默认显示前几行？', 'options': ['5', '10', '15', '全部'], 'answer': 0},
            {'q': '获取DataFrame的列名使用哪个属性？', 'options': ['df.columns', 'df.index', 'df.names', 'df.keys()'], 'answer': 0}
        ]},
    4: {'id': 4, 'course_id': 1, 'title': '数据读取与清洗', 'duration': '5小时',
        'content': '''<h4>数据读取</h4>
<p>数据分析的第一步是将数据加载到Python中。Pandas支持读取多种格式的数据文件。</p>

<h5>1. 读取CSV文件</h5>
<pre class="bg-light p-3 rounded">import pandas as pd

# 基本读取
df = pd.read_csv("sales.csv")

# 指定编码和分隔符
df = pd.read_csv("sales.csv", encoding="utf-8", sep=",")

# 只读取部分列
df = pd.read_csv("sales.csv", usecols=["日期", "销售额", "客户"])

# 设置索引列
df = pd.read_csv("sales.csv", index_col="订单号")

print(df.head())</pre>

<h5>2. 读取Excel文件</h5>
<pre class="bg-light p-3 rounded"># 读取Excel文件
df = pd.read_excel("sales.xlsx")

# 读取指定Sheet
df = pd.read_excel("sales.xlsx", sheet_name="2024年数据")

# 读取多个Sheet
sheets = pd.read_excel("sales.xlsx", sheet_name=None)</pre>

<h4>数据清洗</h4>

<h5>3. 处理缺失值</h5>
<pre class="bg-light p-3 rounded"># 查看缺失值
print(df.isnull().sum())
print(df.isna().sum())

# 删除缺失值
df_clean = df.dropna()                    # 删除任何含缺失值的行
df_clean = df.dropna(subset=["销售额"])    # 只删除指定列含缺失值的行

# 填充缺失值
df["销售额"] = df["销售额"].fillna(0)           # 用0填充
df["销售额"] = df["销售额"].fillna(df["销售额"].mean())  # 用均值填充
df["城市"] = df["城市"].fillna("未知")          # 用字符串填充
df = df.fillna(method="ffill")           # 用前一个值填充</pre>

<h5>4. 处理重复值</h5>
<pre class="bg-light p-3 rounded"># 检查重复
print(df.duplicated().sum())

# 删除重复
df_unique = df.drop_duplicates()

# 按指定列去重
df_unique = df.drop_duplicates(subset=["订单号"], keep="first")</pre>

<h5>5. 处理异常值</h5>
<pre class="bg-light p-3 rounded"># 使用IQR方法检测异常值
Q1 = df["销售额"].quantile(0.25)
Q3 = df["销售额"].quantile(0.75)
IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

# 过滤异常值
df_clean = df[(df["销售额"] >= lower) & (df["销售额"] <= upper)]

# 使用Z-score方法
from scipy import stats
z_scores = stats.zscore(df["销售额"])
df_clean = df[(z_scores > -3) & (z_scores < 3)]</pre>

<h5>6. 数据类型转换</h5>
<pre class="bg-light p-3 rounded"># 转换数据类型
df["订单号"] = df["订单号"].astype(str)
df["销售额"] = pd.to_numeric(df["销售额"], errors="coerce")
df["日期"] = pd.to_datetime(df["日期"])

# 转换后检查
print(df.dtypes)</pre>''',
        'code_example': '''sales = [
    {"订单号": 1, "客户": "张三", "销售额": 5800, "城市": "北京"},
    {"订单号": 2, "客户": "李四", "销售额": None, "城市": "上海"},
    {"订单号": 3, "客户": "王五", "销售额": 7200, "城市": "广州"},
    {"订单号": 1, "客户": "张三", "销售额": 5800, "城市": "北京"},  # 重复
]

print("=== 原始数据 ===")
for s in sales:
    print(s)

cleaned = [s for s in sales if s["销售额"] is not None]
print(f"\\n删除缺失值后: {len(cleaned)}条")

for s in sales:
    if s["销售额"] is None:
        s["销售额"] = 0

seen = set()
unique = []
for s in cleaned:
    if s["订单号"] not in seen:
        unique.append(s)
        seen.add(s["订单号"])

print(f"删除重复后: {len(unique)}条")
print("\\n=== 清洗后数据 ===")
for s in unique:
    print(s)''',
        'tips': [
            'pd.read_csv() 常用参数: encoding, sep, usecols, index_col, nrows',
            'isnull() 和 isna() 功能相同，都可用于检测缺失值',
            'fillna() 可以用均值、中位数、众数或指定值填充',
            'drop_duplicates() 默认保留第一次出现的记录',
            'IQR方法适合处理有明显异常值的数据',
            '处理前先备份数据，处理后用 describe() 验证'
        ],
        'quiz': [
            {'q': '删除含有缺失值的行使用哪个方法？', 'options': ['dropna()', 'remove_null()', 'clean()', 'drop_null()'], 'answer': 0},
            {'q': 'fillna(0)的作用是？', 'options': ['用0填充缺失值', '删除值为0的行', '将0替换为NaN', '过滤掉0'], 'answer': 0},
            {'q': 'pd.read_excel()需要安装哪个额外库？', 'options': ['openpyxl', 'xlrd', 'xlwt', '以上都需要'], 'answer': 0}
        ]},
    5: {'id': 5, 'course_id': 1, 'title': '数据聚合与统计', 'duration': '6小时',
        'content': '''<h4>数据聚合</h4>
<p>数据聚合是数据分析中最常见的操作之一，用于将数据按某个维度分组后进行汇总计算。</p>

<h5>1. 分组聚合基础</h5>
<pre class="bg-light p-3 rounded">import pandas as pd

# 创建示例数据
sales_data = {
    "日期": ["2024-01-01", "2024-01-01", "2024-01-02", "2024-01-02"],
    "类别": ["电子产品", "服装", "电子产品", "服装"],
    "销售额": [1000, 500, 1200, 600]
}
df = pd.DataFrame(sales_data)

# 单列分组聚合
category_sales = df.groupby("类别")["销售额"].sum()
print("按类别汇总:\\n", category_sales)

# 多列分组聚合
daily_category = df.groupby(["日期", "类别"])["销售额"].sum()
print("\\n按日期和类别:\\n", daily_category)</pre>

<h5>2. 常用聚合函数</h5>
<pre class="bg-light p-3 rounded"># 单一聚合
df.groupby("类别")["销售额"].sum()    # 求和
df.groupby("类别")["销售额"].mean()   # 均值
df.groupby("类别")["销售额"].count()   # 计数
df.groupby("类别")["销售额"].max()     # 最大值
df.groupby("类别")["销售额"].min()     # 最小值
df.groupby("类别")["销售额"].std()    # 标准差

# 多个聚合
df.groupby("类别").agg({
    "销售额": ["sum", "mean", "count"]
})</pre>

<h5>3. 高级聚合</h5>
<pre class="bg-light p-3 rounded"># 自定义聚合函数
def range_calc(x):
    return x.max() - x.min()

df.groupby("类别")["销售额"].agg(range_calc)

# 命名输出列
df.groupby("类别").agg(
    总销售额=("销售额", "sum"),
    平均销售额=("销售额", "mean"),
    订单数=("销售额", "count")
)</pre>

<h5>4. 数据透视表</h5>
<pre class="bg-light p-3 rounded"># 创建透视表
pivot = pd.pivot_table(
    df, 
    values="销售额", 
    index="类别", 
    columns="日期", 
    aggfunc="sum",
    fill_value=0
)
print(pivot)

# 添加汇总行/列
pivot_with_margins = pd.pivot_table(
    df, values="销售额", 
    index="类别", 
    aggfunc="sum",
    margins=True,
    margins_name="总计"
)</pre>

<h5>5. 统计描述</h5>
<pre class="bg-light p-3 rounded"># 描述性统计
print(df["销售额"].describe())

# 计算偏度和峰度
print(df["销售额"].skew())   # 偏度
print(df["销售额"].kurt())   # 峰度

# 相关性分析
correlation = df[["销售额", "数量"]].corr()
print(correlation)</pre>''',
        'code_example': '''from collections import defaultdict

sales = [
    {"类别": "电子产品", "销售额": 5800, "利润": 1200},
    {"类别": "服装", "销售额": 3200, "利润": 800},
    {"类别": "电子产品", "销售额": 7200, "利润": 1500},
    {"类别": "服装", "销售额": 2800, "利润": 700},
]

print("=== 按类别汇总 ===")
stats = defaultdict(lambda: {"销售额": 0, "利润": 0, "count": 0})
for s in sales:
    cat = s["类别"]
    stats[cat]["销售额"] += s["销售额"]
    stats[cat]["利润"] += s["利润"]
    stats[cat]["count"] += 1

for cat, st in stats.items():
    print(f"{cat}: 总计¥{st['销售额']}, 利润¥{st['利润']}, 订单{1}单")

print("\\n=== 筛选总额>5000 ===")
for cat, st in stats.items():
    if st["销售额"] > 5000:
        print(f"{cat}: ¥{st['销售额']}")''',
        'tips': [
            'groupby() 返回GroupBy对象，需配合聚合函数使用',
            'agg() 可以对不同列使用不同的聚合函数',
            'reset_index() 将分组后的索引转回为列',
            'pivot_table() 是二维分组聚合，比 groupby 更灵活',
            '使用 fill_value=0 避免透视表出现NaN',
            'agg() 中的列名可以用元组形式命名输出列'
        ],
        'quiz': [
            {'q': '按列分组并求和的正确语法是？', 'options': ['df.groupby("列名")["值"].sum()', 'df.sum().groupby("列名")', 'df.group.sum("列名")', 'df.sum.group("列名")'], 'answer': 0},
            {'q': 'agg()函数的作用是？', 'options': ['自定义聚合操作', '分组', '排序', '过滤'], 'answer': 0},
            {'q': 'reset_index()的作用是？', 'options': ['将索引转为列', '重置索引为0开始', '删除索引', '创建新索引'], 'answer': 0}
        ]},
    6: {'id': 6, 'course_id': 2, 'title': '高级索引与选择', 'duration': '3小时',
        'content': '''<h4>高级索引概述</h4>
<p>Pandas提供了多种强大的索引和选择数据的方法。理解这些方法的区别对于高效数据分析至关重要。</p>

<h5>1. loc 与 iloc 的区别</h5>
<pre class="bg-light p-3 rounded">import pandas as pd
import numpy as np

df = pd.DataFrame({
    "产品": ["A", "B", "C", "D", "E"],
    "销量": [100, 200, 150, 300, 250],
    "城市": ["北京", "上海", "广州", "深圳", "杭州"]
}, index=["r1", "r2", "r3", "r4", "r5"])

# loc: 基于标签的索引
print(df.loc["r1"])              # 选择单行
print(df.loc["r1":"r3"])         # 切片：包含r3
print(df.loc["r1", "产品"])      # 选择单个值

# iloc: 基于位置的整数索引
print(df.iloc[0])               # 选择第一行
print(df.iloc[0:3])             # 切片：不包含索引3
print(df.iloc[0, 0])            # 选择第一行第一列</pre>

<h5>2. 条件筛选</h5>
<pre class="bg-light p-3 rounded"># 单一条件
high_sales = df[df["销量"] > 200]

# 多个条件（注意括号）
filtered = df[(df["销量"] > 150) & (df["城市"] == "北京")]

# 使用 OR 条件
filtered = df[(df["销量"] > 200) | (df["城市"] == "上海")]

# 使用 isin()
cities = ["北京", "上海", "广州"]
filtered = df[df["城市"].isin(cities)]

# 使用 str.contains() 模糊匹配
df[df["产品"].str.contains("A|B")]  # 包含A或B的产品</pre>

<h5>3. query 方法</h5>
<pre class="bg-light p-3 rounded"># 使用 query 方法（更直观的语法）
result = df.query("销量 > 200")

# 多条件
result = df.query("销量 > 150 and 城市 == '北京'")

# 使用变量
threshold = 180
result = df.query("销量 > @threshold")

# 选择列
result = df.query("销量 > 150")[["产品", "销量"]]</pre>

<h5>4. at 与 iat（快速单个值访问）</h5>
<pre class="bg-light p-3 rounded"># at: 快速访问单个标签值
value = df.at["r1", "产品"]  # 比 loc 更快

# iat: 快速访问单个位置值  
value = df.iat[0, 0]        # 比 iloc 更快

print(f"产品r1: {value}")</pre>

<h5>5. 多级索引</h5>
<pre class="bg-light p-3 rounded"># 创建多级索引DataFrame
df_multi = pd.DataFrame({
    "销售额": [100, 200, 150, 300]
}, index=[["华北", "华北", "华南", "华南"],
          ["北京", "天津", "广州", "深圳"]])

# 选择外层索引
print(df_multi.loc["华北"])

# 选择内层索引
print(df_multi.loc[("华北", "北京")])</pre>''',
        'code_example': '''df = [
    {"索引": "r1", "产品": "A", "销量": 100, "城市": "北京"},
    {"索引": "r2", "产品": "B", "销量": 200, "城市": "上海"},
    {"索引": "r3", "产品": "C", "销量": 150, "城市": "广州"},
    {"索引": "r4", "产品": "D", "销量": 300, "城市": "深圳"},
    {"索引": "r5", "产品": "E", "销量": 250, "城市": "杭州"},
]

print("=== 按索引范围选择 ===")
for i, row in enumerate(df):
    if 0 <= i <= 2:  # 类似 iloc[0:3]
        print(row)

print("\\n=== 按标签选择 ===")
for row in df:
    if row["索引"] in ["r1", "r2", "r3"]:
        print(row)

print("\\n=== 条件筛选 (销量>150) ===")
filtered = [row for row in df if row["销量"] > 150]
for row in filtered:
    print(row)

print("\\n=== 多条件筛选 ===")
filtered = [row for row in df if row["销量"] > 150 and row["城市"] == "北京"]
for row in filtered:
    print(row)''',
        'tips': [
            'loc[] 基于标签索引（含结束边界），iloc[] 基于整数位置（不含结束边界）',
            '多条件筛选时，每个条件要用括号括起来，并用 & (AND) 或 | (OR) 连接',
            'query() 方法更直观，但不支持链式调用时使用变量',
            '使用 @ 符号在 query 中引用外部变量',
            'at/iat 比 loc/iloc 快，但只能访问单个值',
            '布尔索引 df[df[列]>值] 会返回满足条件的行'
        ],
        'quiz': [
            {'q': 'loc和iloc的区别是？', 'options': ['loc按标签，iloc按位置', 'loc按位置，iloc按标签', '功能相同', 'loc用于行，iloc用于列'], 'answer': 0},
            {'q': '选择第2到第5行（包含）使用？', 'options': ['df.iloc[1:5]', 'df.iloc[2:5]', 'df.iloc[2:6]', 'df.loc[2:5]'], 'answer': 0},
            {'q': '多个条件筛选使用哪个运算符？', 'options': ['&', 'and', '&&', '|'], 'answer': 0}
        ]},
    7: {'id': 7, 'course_id': 2, 'title': '数据透视表与交叉表', 'duration': '4小时',
        'content': '''<h4>数据透视表</h4>
<p>数据透视表是数据分析中最强大的工具之一，可以快速对数据进行多维度汇总分析。</p>

<h5>1. 基础透视表</h5>
<pre class="bg-light p-3 rounded">import pandas as pd

df = pd.DataFrame({
    "日期": ["2024-01", "2024-01", "2024-02", "2024-02", "2024-03"],
    "类别": ["电子产品", "服装", "电子产品", "服装", "电子产品"],
    "地区": ["北京", "上海", "北京", "广州", "上海"],
    "销售额": [1000, 500, 1200, 600, 1500],
    "利润": [200, 100, 250, 120, 300]
})

# 基础透视表
pivot = pd.pivot_table(df, values="销售额", index="类别", columns="地区")
print(pivot)</pre>

<h5>2. 聚合函数与多值</h5>
<pre class="bg-light p-3 rounded"># 多个聚合函数
pivot = pd.pivot_table(
    df, 
    values=["销售额", "利润"],
    index="类别",
    columns="地区",
    aggfunc={"销售额": "sum", "利润": "mean"}
)
print(pivot)

# 常用聚合函数: sum, mean, count, min, max, std</pre>

<h5>3. 高级选项</h5>
<pre class="bg-light p-3 rounded"># 添加汇总
pivot = pd.pivot_table(
    df, 
    values="销售额",
    index="类别",
    columns="地区",
    aggfunc="sum",
    fill_value=0,        # 填充缺失值
    margins=True,        # 添加汇总
    margins_name="总计"
)

# 按多列分组
pivot = pd.pivot_table(
    df,
    values="销售额",
    index=["类别", "地区"],  # 多级行索引
    aggfunc="sum"
)</pre>

<h4>交叉表 (Crosstab)</h4>

<h5>4. 使用 crosstab</h5>
<pre class="bg-light p-3 rounded"># 基础交叉表
crosstab = pd.crosstab(df["类别"], df["地区"])
print(crosstab)

# 添加聚合值
crosstab = pd.crosstab(
    df["类别"], 
    df["地区"],
    values=df["销售额"],
    aggfunc="sum"
).fillna(0)

# 多级索引
crosstab = pd.crosstab(
    [df["类别"], df["地区"]],  # 行分组
    df["日期"]                  # 列分组
)</pre>

<h5>5. 百分比交叉表</h5>
<pre class="bg-light p-3 rounded"># 计算百分比（按行）
crosstab_pct = pd.crosstab(df["类别"], df["地区"], normalize="index")

# 计算百分比（按列）
crosstab_pct = pd.crosstab(df["类别"], df["地区"], normalize="columns")

# 计算百分比（全局）
crosstab_pct = pd.crosstab(df["类别"], df["地区"], normalize="all")</pre>''',
        'code_example': '''sales = [
    {"日期": "1月", "类别": "电子产品", "地区": "北京", "销售额": 1000},
    {"日期": "1月", "类别": "服装", "地区": "上海", "销售额": 500},
    {"日期": "2月", "类别": "电子产品", "地区": "北京", "销售额": 1200},
    {"日期": "2月", "类别": "服装", "地区": "广州", "销售额": 600},
]

print("=== 按类别透视 ===")
from collections import defaultdict
cat_totals = defaultdict(int)
for s in sales:
    cat_totals[s["类别"]] += s["销售额"]
for cat, total in cat_totals.items():
    print(f"{cat}: ¥{total}")

print("\\n=== 交叉表 ===")
cross = defaultdict(lambda: defaultdict(int))
for s in sales:
    cross[s["类别"]][s["地区"]] += s["销售额"]
for cat in cross:
    print(f"{cat}: {dict(cross[cat])}")''',
        'tips': [
            'pivot_table() 比 groupby 更灵活，可创建二维表格',
            'fill_value=0 用0填充缺失值，避免显示NaN',
            'margins=True 添加行列合计，margins_name设置合计列名',
            'crosstab() 专门用于计算频次分布表',
            'normalize 参数可以计算行/列/全局百分比',
            'values 参数指定要聚合的数值列'
        ],
        'quiz': [
            {'q': 'pivot_table中设置汇总行使用哪个参数？', 'options': ['margins=True', 'summary=True', 'total=True', 'aggfunc="sum"'], 'answer': 0},
            {'q': 'crosstab主要用于什么？', 'options': ['计算列联表', '数据排序', '数据过滤', '数据合并'], 'answer': 0},
            {'q': 'pivot_table默认的聚合函数是？', 'options': ['mean', 'sum', 'count', 'max'], 'answer': 0}
        ]},
    8: {'id': 8, 'course_id': 2, 'title': '时间序列分析', 'duration': '6小时',
        'content': '''<h4>时间序列基础</h4>
<p>时间序列数据是按时间顺序排列的数据，在商业分析中非常常见，如每日销售、股票价格等。</p>

<h5>1. 日期时间转换</h5>
<pre class="bg-light p-3 rounded">import pandas as pd

# 创建时间序列数据
df = pd.DataFrame({
    "日期": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04"],
    "销售额": [100, 150, 120, 180]
})

# 转换为datetime类型
df["日期"] = pd.to_datetime(df["日期"])
print(df["日期"].dtype)

# 设置日期为索引
df = df.set_index("日期")

# 使用 date_range 创建日期范围
dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
print(dates[:10])</pre>

<h5>2. 日期范围频率</h5>
<pre class="bg-light p-3 rounded"># 常用频率
pd.date_range("2024-01-01", periods=10, freq="D")   # 日
pd.date_range("2024-01-01", periods=12, freq="ME")    # 月
pd.date_range("2024-01-01", periods=4, freq="Q")    # 季度
pd.date_range("2024-01-01", periods=52, freq="W")   # 周
pd.date_range("2024-01-01", periods=10, freq="H")   # 小时</pre>

<h5>3. 重采样</h5>
<pre class="bg-light p-3 rounded"># 重采样：将日数据转为周/月数据
df_weekly = df["销售额"].resample("W").sum()    # 周求和
df_monthly = df["销售额"].resample("ME").sum()   # 月求和
df_quarterly = df["销售额"].resample("Q").sum() # 季度求和

# 上采样：低频转高频（需要插值）
df_daily = df.resample("D").interpolate()

# 多种聚合
df_agg = df["销售额"].resample("ME").agg(["sum", "mean", "max"])</pre>

<h5>4. 移动窗口</h5>
<pre class="bg-light p-3 rounded"># 移动平均
df["MA7"] = df["销售额"].rolling(window=7).mean()
df["MA30"] = df["销售额"].rolling(window=30).mean()

# 移动总和
df["移动总和"] = df["销售额"].rolling(window=7).sum()

# 移动标准差（波动率）
df["波动率"] = df["销售额"].rolling(window=7).std()

# 指数移动平均
df["EMA"] = df["销售额"].ewm(span=7).mean()</pre>

<h5>5. 时间索引操作</h5>
<pre class="bg-light p-3 rounded"># 提取日期组件
print(df.index.year)   # 年份
print(df.index.month) # 月份
print(df.index.day)   # 日期
print(df.index.dayofweek)  # 星期几(0=周一)

# 按日期范围筛选
df["2024-01"]      # 选择2024年1月
df["2024-01-01":"2024-01-10"]  # 日期范围

# 字符串索引（简化语法）
df.loc["2024-01"]</pre>''',
        'code_example': '''from datetime import datetime, timedelta

start_date = datetime(2024, 1, 1)
dates = [start_date + timedelta(days=i) for i in range(10)]

sales = [
    {"日期": d, "销售额": 100 + (i * 10) % 50}
    for i, d in enumerate(dates)
]

print("=== 时间序列数据 ===")
for s in sales[:5]:
    print(f"{s['日期'].strftime('%Y-%m-%d')}: ¥{s['销售额']}")

print("\\n=== 移动平均 ===")
window = 3
for i in range(len(sales) - window + 1):
    avg = sum(s["销售额"] for s in sales[i:i+window]) / window
    print(f"日期{sales[i+window-1]['日期'].strftime('%m-%d')}: MA3={avg:.0f}")

print("\\n=== 月度汇总 ===")
from collections import defaultdict
monthly = defaultdict(int)
for s in sales:
    month = s["日期"].strftime("%Y-%m")
    monthly[month] += s["销售额"]
for month, total in monthly.items():
    print(f"{month}: ¥{total}")''',
        'tips': [
            'pd.to_datetime() 转换日期字符串为datetime类型',
            'set_index("日期列") 将日期列设为索引便于时间操作',
            'resample() 需要配合聚合函数使用，如.sum(), .mean()',
            'rolling(window=n) 计算n期移动窗口统计',
            'ewm(span=n) 计算指数加权移动平均',
            '频率代码: D=日, W=周, M=月, Q=季度, Y=年'
        ],
        'quiz': [
            {'q': '将字符串转换为日期使用？', 'options': ['pd.to_datetime()', 'pd.as_date()', 'df.to_date()', 'datetime.parse()'], 'answer': 0},
            {'q': '按周聚合使用哪个频率代码？', 'options': ['W', 'w', 'week', 'weekly'], 'answer': 0},
            {'q': 'rolling(7).mean()计算的是什么？', 'options': ['7期移动平均', '前7行求和', '第7行的值', '7倍均值'], 'answer': 0}
        ]},
    9: {'id': 9, 'course_id': 2, 'title': '数据合并与连接', 'duration': '6小时',
        'content': '''<h4>数据合并概述</h4>
<p>实际数据分析中，数据通常分布在多个文件或表中，需要将它们合并在一起进行分析。</p>

<h5>1. concat - 纵向合并</h5>
<pre class="bg-light p-3 rounded">import pandas as pd

df1 = pd.DataFrame({"姓名": ["张三", "李四"], "年龄": [25, 30]})
df2 = pd.DataFrame({"姓名": ["王五", "赵六"], "年龄": [28, 35]})

# 纵向合并
result = pd.concat([df1, df2], ignore_index=True)
print(result)

# 横向合并
df3 = pd.DataFrame({"城市": ["北京", "上海"], "薪资": [15000, 20000]})
result = pd.concat([df1, df3], axis=1)
print(result)</pre>

<h5>2. merge - SQL风格连接</h5>
<pre class="bg-light p-3 rounded">orders = pd.DataFrame({
    "订单号": [1, 2, 3],
    "客户ID": [101, 102, 103],
    "金额": [1000, 2000, 1500]
})

customers = pd.DataFrame({
    "客户ID": [101, 102, 103],
    "姓名": ["张三", "李四", "王五"],
    "城市": ["北京", "上海", "广州"]
})

# 内连接（INNER JOIN）
result = pd.merge(orders, customers, on="客户ID", how="inner")

# 左连接（LEFT JOIN）
result = pd.merge(orders, customers, on="客户ID", how="left")

# 右连接（RIGHT JOIN）
result = pd.merge(orders, customers, on="客户ID", how="right")

# 全外连接（OUTER JOIN）
result = pd.merge(orders, customers, on="客户ID", how="outer")</pre>

<h5>3. join - 索引连接</h5>
<pre class="bg-light p-3 rounded"># 使用索引进行连接
df1 = pd.DataFrame({"销售额": [100, 200]}, index=["a", "b"])
df2 = pd.DataFrame({"利润": [20, 40]}, index=["a", "b"])

# 默认左连接
result = df1.join(df2)

# 指定连接方式
result = df1.join(df2, how="inner")</pre>

<h5>4. 合并时的常见问题</h5>
<pre class="bg-light p-3 rounded"># 列名不同时的连接
pd.merge(df1, df2, left_on="客户ID", right_on="ID")

# 处理重复列名
result = pd.merge(df1, df2, on="客户ID", suffixes=("_订单", "_客户"))

# 只保留特定列
result = pd.merge(orders[["订单号", "客户ID"]], customers, on="客户ID")</pre>''',
        'code_example': '''customers = [
    {"客户ID": 101, "姓名": "张三", "城市": "北京"},
    {"客户ID": 102, "姓名": "李四", "城市": "上海"},
    {"客户ID": 103, "姓名": "王五", "城市": "广州"},
]

orders = [
    {"订单号": 1, "客户ID": 101, "金额": 1000},
    {"订单号": 2, "客户ID": 102, "金额": 2000},
    {"订单号": 3, "客户ID": 104, "金额": 1500},  # 不存在的客户
]

print("=== 内连接 ===")
for o in orders:
    for c in customers:
        if o["客户ID"] == c["客户ID"]:
            print(f"订单{o['订单号']}: {c['姓名']}({c['城市']}) ¥{o['金额']}")

print("\\n=== 左连接 ===")
for c in customers:
    found = False
    for o in orders:
        if o["客户ID"] == c["客户ID"]:
            found = True
            break
    if found:
        for o in orders:
            if o["客户ID"] == c["客户ID"]:
                print(f"{c['姓名']}: 有订单")
                break
    else:
        print(f"{c['姓名']}: 无订单")''',
        'tips': [
            'concat() 用于纵向合并（增加行），merge() 用于横向合并（增加列）',
            'merge() 的 how 参数: inner(默认), left, right, outer',
            '连接列名不同时用 left_on 和 right_on 指定',
            'suffixes 参数处理重复列名，如("_左", "_右")',
            'join() 基于索引连接，比 merge() 更简洁',
            '合并前检查连接键是否有重复值，避免产生笛卡尔积'
        ],
        'quiz': [
            {'q': 'concat用于什么操作？', 'options': ['纵向或横向合并', '按列连接', '数据透视', '数据过滤'], 'answer': 0},
            {'q': 'LEFT JOIN在merge中使用哪个how参数？', 'options': ['how="left"', 'how="left_join"', 'join_type="left"', 'left=True'], 'answer': 0},
            {'q': 'merge和join的主要区别是？', 'options': ['merge按列连接，join按索引连接', '功能相同', 'merge更快', 'join支持更多参数'], 'answer': 0}
        ]},
    10: {'id': 10, 'course_id': 2, 'title': '性能优化技巧', 'duration': '6小时',
        'content': '''<h4>性能优化概述</h4>
<p>处理大规模数据时，性能优化至关重要。以下是Pandas中常用的性能优化技巧。</p>

<h5>1. 向量化操作</h5>
<pre class="bg-light p-3 rounded">import pandas as pd
import numpy as np

# 避免使用 for 循环
# 错误示例：
for i in range(len(df)):
    df.loc[i, "新列"] = df.loc[i, "A"] + df.loc[i, "B"]

# 正确示例：向量化操作
df["新列"] = df["A"] + df["B"]

# 使用 apply 替代复杂循环
df["新列"] = df.apply(lambda row: row["A"] + row["B"], axis=1)</pre>

<h5>2. 数据类型优化</h5>
<pre class="bg-light p-3 rounded"># 转换类别类型节省内存
df["类别"] = df["类别"].astype("category")

# 减少数值类型精度
df["金额"] = df["金额"].astype("float32")  # 比float64省一半内存

# 使用类别类型处理重复字符串
print(df.memory_usage(deep=True))  # 查看内存使用</pre>

<h5>3. query 方法优化</h5>
<pre class="bg-light p-3 rounded"># 复杂条件筛选用 query 更高效
result = df.query("A > 100 and B < 50 and C == '北京'")

# 使用变量
threshold = 100
result = df.query("A > @threshold")

# 链式筛选
result = df.query("A > 100").query("B < 50")</pre>

<h5>4. 分块读取大文件</h5>
<pre class="bg-light p-3 rounded"># 分块读取
chunks = pd.read_csv("large_file.csv", chunksize=10000)

# 处理每个块
result = []
for chunk in chunks:
    processed = chunk[chunk["金额"] > 100]
    result.append(processed)

# 合并结果
final = pd.concat(result, ignore_index=True)</pre>

<h5>5. 高效聚合</h5>
<pre class="bg-light p-3 rounded"># groupby 优化
# 使用 named aggregation
result = df.groupby("类别").agg(
    总金额=("金额", "sum"),
    平均金额=("金额", "mean"),
    数量=("金额", "count")
)

# 使用 transform 替代 apply
df["类别均值"] = df.groupby("类别")["金额"].transform("mean")</pre>

<h5>6. 内存优化</h5>
<pre class="bg-light p-3 rounded"># 选择性读取列
df = pd.read_csv("file.csv", usecols=["A", "B", "C"])

# 删除不需要的列
df = df.drop(columns=["不需要的列"])

# 使用高效数据类型
df = pd.read_csv("file.csv", dtype={"整型列": "int32", "浮点列": "float32"})</pre>''',
        'code_example': '''import pandas as pd
import numpy as np

import random
categories = ["A", "B", "C", "D"]
data = [
    {"类别": random.choice(categories),
     "金额": random.randint(100, 10000),
     "数量": random.randint(1, 100)}
    for _ in range(100)
]

for d in data:
    d["总计"] = d["金额"] * d["数量"]

print(f"数据量: {len(data)}条")
print("前3条:", data[:3])

from collections import defaultdict
grouped = defaultdict(lambda: {"金额": 0, "数量": 0, "count": 0})
for d in data:
    cat = d["类别"]
    grouped[cat]["金额"] += d["金额"]
    grouped[cat]["数量_sum"] = grouped[cat].get("数量_sum", 0) + d["数量"]
    grouped[cat]["count"] += 1

print("\\n聚合结果:")
for cat, stats in grouped.items():
    print(f"{cat}: 总额={stats['金额']}, 均值={stats['数量_sum']//stats['count']}")''',
        'tips': [
            '始终优先使用向量化操作，避免Python循环',
            'category 类型可大幅减少字符串列的内存占用',
            'query() 方法比普通布尔索引更快',
            'chunksize 参数分块读取大文件，避免内存溢出',
            'transform() 比 apply() 更高效，适合分组计算',
            '定期使用 memory_usage() 检查内存使用情况'
        ],
        'quiz': [
            {'q': 'Pandas中最快的操作方式是？', 'options': ['向量化操作', 'for循环', 'apply函数', 'iterrows'], 'answer': 0},
            {'q': '将字符串列转为category类型的好处是？', 'options': ['节省内存', '加快计算', '两者都是', '没好处'], 'answer': 2},
            {'q': 'query()方法的优势是？', 'options': ['代码更简洁', '性能更好', '支持SQL语法', '以上都是'], 'answer': 3}
        ]},
    11: {'id': 11, 'course_id': 3, 'title': 'Matplotlib基础图表', 'duration': '4小时',
        'content': '''<h4>Matplotlib 简介</h4>
<p>Matplotlib 是 Python 最流行的数据可视化库，提供了丰富的图表类型和高度自定义能力。</p>

<h5>1. 基础绘图流程</h5>
<pre class="bg-light p-3 rounded">import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 创建图表
fig, ax = plt.subplots(figsize=(10, 6))

# 绑图数据
x = ["1月", "2月", "3月", "4月"]
y = [1200, 1500, 1100, 1800]

# 绑制折线图
ax.plot(x, y, marker="o", linewidth=2, color="#1f77b4")

# 添加标题和标签
ax.set_title("月度销售额趋势", fontsize=16)
ax.set_xlabel("月份", fontsize=12)
ax.set_ylabel("销售额（元）", fontsize=12)

# 添加网格
ax.grid(True, alpha=0.3)

# 显示图表
plt.tight_layout()
plt.show()</pre>

<h5>2. 常用图表类型</h5>
<pre class="bg-light p-3 rounded"># 柱状图
fig, ax = plt.subplots()
categories = ["电子产品", "服装", "食品", "家居"]
values = [4500, 3200, 2800, 3500]
colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12"]
ax.bar(categories, values, color=colors)

# 饼图
fig, ax = plt.subplots()
ax.pie(values, labels=categories, autopct="%1.1f%%", startangle=90)

# 散点图
fig, ax = plt.subplots()
x = np.random.randn(100)
y = np.random.randn(100)
ax.scatter(x, y, alpha=0.5, s=50, c="blue")

# 直方图
fig, ax = plt.subplots()
data = np.random.randn(1000)
ax.hist(data, bins=30, edgecolor="black")</pre>

<h5>3. 图表元素设置</h5>
<pre class="bg-light p-3 rounded"># 设置标题
ax.set_title("图表标题", fontsize=18, fontweight="bold")

# 设置轴标签
ax.set_xlabel("X轴", fontsize=14)
ax.set_ylabel("Y轴", fontsize=14)

# 设置刻度标签
ax.set_xticks([0, 1, 2, 3])
ax.set_xticklabels(["类别A", "类别B", "类别C", "类别D"])

# 添加图例
ax.legend(["数据系列1", "数据系列2"], loc="upper right")

# 添加数据标签
for i, v in enumerate(values):
    ax.text(i, v+50, str(v), ha="center")</pre>

<h5>4. 多子图布局</h5>
<pre class="bg-light p-3 rounded"># 创建2x2子图
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 子图1
axes[0, 0].plot(x, y, "r-")
axes[0, 0].set_title("子图1")

# 子图2
axes[0, 1].bar(categories, values)
axes[0, 1].set_title("子图2")

# 子图3
axes[1, 0].scatter(x, y)
axes[1, 0].set_title("子图3")

# 子图4
axes[1, 1].pie(values, labels=categories)
axes[1, 1].set_title("子图4")

plt.tight_layout()
plt.show()</pre>

<h5>5. 样式和主题</h5>
<pre class="bg-light p-3 rounded"># 使用内置样式
plt.style.use("seaborn-v0_8")

# 保存图表
plt.savefig("chart.png", dpi=300, bbox_inches="tight")

# 设置颜色循环
plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"])</pre>''',
        'code_example': '''categories = ["电子产品", "服装", "食品", "家居"]
values = [4500, 3200, 2800, 3500]

print("=== 柱状图数据 ===")
print("类别        销售额")
print("-" * 25)
for cat, val in zip(categories, values):
    bar = "█" * (val // 200)  # 模拟柱状
    print(f"{cat:8s}  {val:5d}  {bar}")

print("\\n=== 饼图数据 ===")
total = sum(values)
for cat, val in zip(categories, values):
    pct = val / total * 100
    print(f"{cat}: {pct:.1f}%")

print("\\n=== 折线图数据 ===")
months = ["1月", "2月", "3月", "4月"]
sales = [1200, 1500, 1800, 2200]
for m, s in zip(months, sales):
    line = "●" + "─" * (s // 100 - 1)
    print(f"{m}: {line} {s}")''',
        'tips': [
            'plt.subplots() 创建画布和坐标轴，返回(fig, ax)元组',
            '中文显示需要设置 font.sans-serif 和 axes.unicode_minus',
            'plt.tight_layout() 自动调整子图参数避免重叠',
            'plt.savefig() 保存图表，支持PNG、PDF、SVG等多种格式',
            'figsize 参数控制图表尺寸，(宽, 高) 单位为英寸',
            '使用 alpha 参数调整透明度和 alpha=0.3 让网格更柔和'
        ],
        'quiz': [
            {'q': '创建图形窗口使用哪个函数？', 'options': ['plt.figure()', 'plt.create()', 'plt.plot()', 'plt.window()'], 'answer': 0},
            {'q': '设置x轴标签使用？', 'options': ['plt.xlabel()', 'plt.set_x()', 'plt.label_x()', 'df.set_xlabel()'], 'answer': 0},
            {'q': '绘制柱状图使用哪个函数？', 'options': ['plt.bar()', 'plt.column()', 'plt.hist()', 'plt.bars()'], 'answer': 0}
        ]},
    12: {'id': 12, 'course_id': 3, 'title': 'Seaborn统计图表', 'duration': '5小时',
        'content': '''<h4>Seaborn 简介</h4>
<p>Seaborn 是基于 Matplotlib 的高级统计可视化库，提供了更美观的默认样式和专门用于统计数据可视化的函数。</p>

<h5>1. Seaborn 基础</h5>
<pre class="bg-light p-3 rounded">import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置样式
sns.set_style("whitegrid")  # white, dark, whitegrid, darkgrid, ticks
sns.set_palette("husl")      # 设置调色板

# 创建示例数据
df = pd.DataFrame({
    "月份": ["1月"]*4 + ["2月"]*4,
    "类别": ["电子产品", "服装", "食品", "家居"]*2,
    "销售额": [4500, 3200, 2800, 3500, 5000, 3600, 3000, 3800]
})</pre>

<h5>2. 关系图表</h5>
<pre class="bg-light p-3 rounded"># 折线图（带置信区间）
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df, x="月份", y="销售额", hue="类别", markers=True, ax=ax)

# 带误差线的折线图
flights = sns.load_dataset("flights")
sns.relplot(data=flights, x="year", y="passengers", 
            hue="month", kind="line", height=5)</pre>

<h5>3. 分布图表</h5>
<pre class="bg-light p-3 rounded"># 直方图 + 核密度估计
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(data=df, x="销售额", kde=True, bins=20, ax=ax)

# 箱线图
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=df, x="类别", y="销售额", ax=ax)

# 小提琴图（结合箱线图和密度图）
fig, ax = plt.subplots(figsize=(10, 6))
sns.violinplot(data=df, x="类别", y="销售额", ax=ax)

# 联合分布图
sns.jointplot(data=df, x="销售额", y="利润", kind="reg")</pre>

<h5>4. 分类图表</h5>
<pre class="bg-light p-3 rounded"># 柱状图
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df, x="类别", y="销售额", ax=ax)

# 点图（显示趋势）
sns.pointplot(data=df, x="类别", y="销售额")

# 计数图
sns.countplot(data=df, x="类别")

# 分类散点图
sns.stripplot(data=df, x="类别", y="销售额", jitter=True)</pre>

<h5>5. 热力图</h5>
<pre class="bg-light p-3 rounded"># 相关性热力图
corr = df[["销售额", "利润", "成本"]].corr()
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(corr, annot=True, cmap="coolwarm", center=0, ax=ax)

# 透视表热力图
pivot = df.pivot_table(values="销售额", index="类别", columns="月份")
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlOrRd")</pre>

<h5>6. 高级功能</h5>
<pre class="bg-light p-3 rounded"># FacetGrid 多子图
g = sns.FacetGrid(df, col="类别", height=4)
g.map(sns.histplot, "销售额")

# PairPlot 配对图
sns.pairplot(df[["销售额", "利润", "成本"]])

# 设置主题
sns.set_theme(style="darkgrid", font_scale=1.2)</pre>''',
        'code_example': '''categories = ["A", "B", "C", "D"]
groups = {
    "A": [100, 120, 130, 110, 140, 120, 115],
    "B": [80, 90, 85, 95, 88, 92, 87],
    "C": [150, 160, 145, 170, 155, 165, 158],
    "D": [60, 70, 65, 75, 68, 72, 69]
}

import statistics
print("=== 各类别统计 ===")
for cat, values in groups.items():
    sorted_v = sorted(values)
    n = len(sorted_v)
    print(f"{cat}:")
    print(f"  最小值: {min(values)}")
    print(f"  Q1: {sorted_v[n//4]}")
    print(f"  中位数: {statistics.median(values)}")
    print(f"  Q3: {sorted_v[3*n//4]}")
    print(f"  最大值: {max(values)}")

print("\\n=== 分布统计 ===")
for cat, values in groups.items():
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    print(f"{cat}: 均值={mean:.1f}, 标准差={std:.1f}")''',
        'tips': [
            'Seaborn 自动处理美观样式，比 Matplotlib 更简洁',
            'set_style() 设置主题，常用: whitegrid, darkgrid',
            'hue 参数用于分组着色，可以同时展示多个维度',
            'kind 参数指定图表类型，如 relplot 的 kind="line"',
            'jointplot 可以同时展示两个变量的分布和关系',
            'seaborn 绑入 pandas DataFrame，使用 data 参数指定数据源'
        ],
        'quiz': [
            {'q': 'Seaborn绘制直方图使用？', 'options': ['sns.histplot()', 'sns.hist()', 'sns.plot_hist()', 'sns.histogram()'], 'answer': 0},
            {'q': '箱线图用于展示什么？', 'options': ['数据分布和异常值', '数据相关性', '时间序列', '比例关系'], 'answer': 0},
            {'q': '热力图通常用于展示？', 'options': ['相关性矩阵', '时间序列', '分类数据', '散点分布'], 'answer': 0}
        ]},
    13: {'id': 13, 'course_id': 3, 'title': '图表美化与配色', 'duration': '4小时',
        'content': '''<h4>图表美化原则</h4>
<p>好的数据可视化不仅要准确传达信息，还要美观、易读。以下是图表美化的核心原则。</p>

<h5>1. 配色方案</h5>
<pre class="bg-light p-3 rounded">import matplotlib.pyplot as plt
import seaborn as sns

# 使用调色板
# 分类数据：husl, Set2, Paired
sns.set_palette("husl")

# 连续数据：rocket, mako, flare, crest
sns.color_palette("rocket", as_cmap=True)

# 自定义颜色
colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]
plt.bar(categories, values, color=colors)

# 使用 colormap
import numpy as np
cmap = plt.cm.Blues
normalize = plt.Normalize(vmin=min(values), vmax=max(values))
colors = [cmap(normalize(v)) for v in values]</pre>

<h5>2. 字体和标签</h5>
<pre class="bg-light p-3 rounded"># 设置标题字体
ax.set_title("销售额分析", fontsize=18, fontweight="bold", pad=20)

# 设置轴标签
ax.set_xlabel("月份", fontsize=12, color="gray")
ax.set_ylabel("金额（元）", fontsize=12)

# 刻度标签
plt.xticks(fontsize=10, rotation=45)
plt.yticks(fontsize=10)

# 图例
ax.legend(title="产品类别", fontsize=10, title_fontsize=12)</pre>

<h5>3. 网格和边框</h5>
<pre class="bg-light p-3 rounded"># 显示网格
ax.grid(True, linestyle="--", alpha=0.7)

# 只显示特定网格
ax.grid(True, axis="y", alpha=0.3)

# 移除边框
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# 设置边框颜色
ax.spines["bottom"].set_color("gray")
ax.spines["left"].set_color("gray")</pre>

<h5>4. 主题样式</h5>
<pre class="bg-light p-3 rounded"># Matplotlib 内置样式
plt.style.use("seaborn-v0_8")
plt.style.use("ggplot")
plt.style.use("Solarize_Light2")

# 查看所有可用样式
print(plt.style.available)

# 重置为默认
plt.rcdefaults()

# 自定义样式
plt.style.use({
    "axes.facecolor": "white",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.titlesize": 16,
    "axes.labelsize": 12
})</pre>

<h5>5. 图表注释</h5>
<pre class="bg-light p-3 rounded"># 添加箭头注释
ax.annotate("峰值", xy=(3, 5000), xytext=(5, 4500),
            arrowprops=dict(arrowstyle="->", color="red"),
            fontsize=12)

# 添加文本框
bbox_props = dict(boxstyle="round", facecolor="wheat", alpha=0.5)
ax.text(0.95, 0.95, "注释文本", transform=ax.transAxes,
        fontsize=12, verticalalignment="top", bbox=bbox_props)

# 添加水平/垂直线
ax.axhline(y=3000, color="red", linestyle="--", alpha=0.5)
ax.axvline(x=5, color="blue", linestyle=":", alpha=0.5)</pre>

<h5>6. 布局调整</h5>
<pre class="bg-light p-3 rounded"># 调整子图间距
plt.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.1, wspace=0.3, hspace=0.3)

# 自动调整布局
plt.tight_layout()

# 紧凑布局
plt.tight_layout(pad=1.5)

# 保存高清图
plt.savefig("chart.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("chart.pdf", bbox_inches="tight")</pre>''',
        'code_example': '''categories = ["A", "B", "C", "D", "E"]
values = [45, 32, 28, 35, 42]
colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6"]

print("=== 美化柱状图 ===")
print("类别   数值   颜色")
print("-" * 30)
for cat, val, color in zip(categories, values, colors):
    bar = "█" * (val // 3)
    print(f"{cat:5s}  {val:5d}  {color}  {bar}")

print("\\n=== 美化网格示例 ===")
print("┌" + "─" * 50 + "┐")
for i, val in enumerate(values):
    row = "│" + " " * 10 + f"{categories[i]}" + " " * (35 - len(categories[i])) + "│"
    print(row)
    bar_row = "│" + "█" * (val) + " " * (50 - val) + "│"
    print(bar_row)
print("└" + "─" * 50 + "┘")''',
        'tips': [
            '颜色数量不超过7种，避免视觉混乱',
            '连续数据用渐变色，分类型数据用对比色',
            '标题字体应大于轴标签，轴标签应大于刻度',
            '删除不必要的边框，使用浅色网格辅助阅读',
            '数据标签应在空间允许时显示，避免遮挡',
            '导出为 PDF 或 SVG 保留矢量格式，方便后期编辑'
        ],
        'quiz': [
            {'q': '设置Matplotlib风格使用？', 'options': ['plt.style.use()', 'plt.set_style()', 'plt.theme()', 'plt.apply_style()'], 'answer': 0},
            {'q': 'tight_layout()的作用是？', 'options': ['自动调整布局', '压缩图表', '展开图表', '添加边框'], 'answer': 0},
            {'q': '设置线条宽度使用哪个参数？', 'options': ['linewidth', 'width', 'lw', '两者都可以'], 'answer': 3}
        ]},
    14: {'id': 14, 'course_id': 3, 'title': '交互式可视化', 'duration': '5小时',
        'content': '''<h4>交互式可视化简介</h4>
<p>交互式可视化让用户能够与图表进行交互，提供更好的数据探索体验。Plotly 是最流行的交互式可视化库之一。</p>

<h5>1. Plotly Express 基础</h5>
<pre class="bg-light p-3 rounded">import plotly.express as px
import pandas as pd

# 创建数据
df = pd.DataFrame({
    "月份": ["1月", "2月", "3月", "4月", "5月"],
    "销售额": [1200, 1900, 1500, 2200, 2800],
    "类别": ["A", "A", "B", "B", "A"]
})

# 折线图
fig = px.line(df, x="月份", y="销售额", title="月度销售趋势")
fig.show()

# 带标记的折线图
fig = px.line(df, x="月份", y="销售额", markers=True)</pre>

<h5>2. 常用图表类型</h5>
<pre class="bg-light p-3 rounded"># 柱状图
fig = px.bar(df, x="月份", y="销售额", color="类别", barmode="group")

# 散点图
fig = px.scatter(df, x="销售额", y="利润", color="类别", 
                 size="数量", hover_name="产品")

# 饼图
fig = px.pie(df, values="销售额", names="类别", title="销售占比")

# 气泡图
fig = px.scatter(df, x="市场份额", y="增长率",
                 size="用户数", color="类别",
                 hover_name="公司")

# 旭日图
fig = px.sunburst(df, path=["洲", "国家", "城市"], values="人口")</pre>

<h5>3. 交互功能</h5>
<pre class="bg-light p-3 rounded"># 悬停显示详情
fig = px.scatter(df, x="销售额", y="利润", hover_data=["产品", "类别"])

# 悬停模板自定义
fig.update_traces(hovertemplate="<b>%{y}</b><extra>%{customdata[0]}</extra>")

# 添加注释
fig.add_annotation(x="1月", y=1500, text="春节促销", showarrow=True)

# 更新悬停模式
fig.update_layout(hovermode="x unified")</pre>

<h5>4. 动态图表</h5>
<pre class="bg-light p-3 rounded"># 创建带动画的数据
df_anim = pd.DataFrame({
    "年份": [2020, 2020, 2021, 2021, 2022, 2022],
    "季度": [1, 2, 1, 2, 1, 2],
    "类别": ["A", "B", "A", "B", "A", "B"],
    "销售额": [100, 120, 150, 180, 200, 250]
})

# 动画折线图
fig = px.line(df_anim, x="季度", y="销售额", 
              color="类别", animation_frame="年份")

# 动画柱状图
fig = px.bar(df_anim, x="类别", y="销售额", 
             color="类别", animation_frame="年份")

# 动画设置
fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 1000</pre>

<h5>5. 子图布局</h5>
<pre class="bg-light p-3 rounded">from plotly.subplots import make_subplots
import plotly.graph_objects as go

# 创建子图
fig = make_subplots(rows=1, cols=2, subplot_titles=("销售额", "利润"))

# 添加图表到子图
fig.add_trace(go.Bar(x=df["月份"], y=df["销售额"]), row=1, col=1)
fig.add_trace(go.Scatter(x=df["月份"], y=df["利润"], mode="lines+markers"), row=1, col=2)

fig.update_layout(title_text="销售与利润分析", height=400)
fig.show()</pre>

<h5>6. 导出和嵌入</h5>
<pre class="bg-light p-3 rounded"># 导出为 HTML（交互式）
fig.write_html("interactive_chart.html")

# 导出为静态图片
fig.write_image("chart.png", width=1200, height=600, scale=2)

# Plotly Dash 创建网页应用
app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Graph(id="sales-chart", figure=fig)
])</pre>''',
        'code_example': '''df = {
    "月份": ["1月", "2月", "3月", "4月", "5月"],
    "销售额": [1200, 1900, 1500, 2200, 2800],
    "类别": ["A", "A", "B", "B", "A"]
}

print("=== 月度销售柱状图 ===")
print("月份   销售额   类别")
print("-" * 30)
for m, s, c in zip(df["月份"], df["销售额"], df["类别"]):
    bar = "█" * (s // 100)
    print(f"{m:4s}  ¥{s:5d}  {c}  {bar}")

print("\\n=== 销售趋势 ===")
months = df["月份"]
sales = df["销售额"]
print("月份:", "  ".join(months))
print("销售额:", "  ".join(f"¥{s}" for s in sales))

print("\\n=== 分组统计 ===")
from collections import defaultdict
cat_totals = defaultdict(int)
for c, s in zip(df["类别"], df["销售额"]):
    cat_totals[c] += s
for cat, total in cat_totals.items():
    bar = "█" * (total // 100)
    print(f"类别{cat}: ¥{total:5d}  {bar}")''',
        'tips': [
            'Plotly 图表默认交互：悬停显示数据、缩放、拖拽平移',
            'px.bar() 创建柱状图，barmode="group"/"stack" 控制柱形排列',
            'animation_frame 参数创建动画效果',
            'write_html() 导出交互式 HTML，可在浏览器中打开',
            'make_subplots() 创建多子图布局',
            'update_layout() 自定义图表布局和样式'
        ],
        'quiz': [
            {'q': 'Plotly Express中创建折线图使用？', 'options': ['px.line()', 'px.plot()', 'px.lineplot()', 'px.create_line()'], 'answer': 0},
            {'q': 'show()方法的作用是？', 'options': ['在浏览器中显示', '保存为文件', '打印图表', '输出数据'], 'answer': 0},
            {'q': '设置点的颜色使用哪个参数？', 'options': ['color', 'color_by', 'c', 'group_by'], 'answer': 0}
        ]},
    15: {'id': 15, 'course_id': 4, 'title': 'SQL基础语法', 'duration': '3小时',
        'content': '''<h4>SQL简介</h4>
<p>SQL（Structured Query Language）是用于管理关系型数据库的标准编程语言。本章节学习SQL的基础语法。</p>

<h5>1. 基础查询</h5>
<pre class="bg-light p-3 rounded">-- 查询所有数据
SELECT * FROM sales;

-- 查询特定列
SELECT order_id, customer_name, amount FROM sales;

-- 使用别名
SELECT order_id AS "订单号", amount AS "金额" FROM sales;

-- 去重查询
SELECT DISTINCT category FROM sales;</pre>

<h5>2. 条件筛选</h5>
<pre class="bg-light p-3 rounded">-- 基础条件
SELECT * FROM sales WHERE amount > 1000;

-- 多条件 AND
SELECT * FROM sales WHERE amount > 1000 AND status = "已完成";

-- 多条件 OR
SELECT * FROM sales WHERE category = "电子产品" OR category = "服装";

-- BETWEEN 范围
SELECT * FROM sales WHERE amount BETWEEN 500 AND 2000;

-- IN 列表
SELECT * FROM sales WHERE category IN ("电子产品", "服装", "食品");

-- LIKE 模糊匹配
SELECT * FROM sales WHERE customer_name LIKE "张%";  -- 张开头的
SELECT * FROM sales WHERE email LIKE "%@gmail.com";   -- gmail邮箱</pre>

<h5>3. 排序和限制</h5>
<pre class="bg-light p-3 rounded">-- 升序排序（默认）
SELECT * FROM sales ORDER BY amount;

-- 降序排序
SELECT * FROM sales ORDER BY amount DESC;

-- 多列排序
SELECT * FROM sales ORDER BY category, amount DESC;

-- 限制结果数量
SELECT * FROM sales ORDER BY amount DESC LIMIT 10;</pre>

<h5>4. 聚合函数</h5>
<pre class="bg-light p-3 rounded">-- 计数
SELECT COUNT(*) FROM sales;
SELECT COUNT(DISTINCT customer_id) FROM sales;

-- 求和
SELECT SUM(amount) FROM sales;

-- 平均值
SELECT AVG(amount) FROM sales;

-- 最大/最小值
SELECT MAX(amount), MIN(amount) FROM sales;

-- 综合统计
SELECT 
    COUNT(*) AS total_orders,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount
FROM sales;</pre>

<h5>5. 分组查询</h5>
<pre class="bg-light p-3 rounded">-- 按类别分组统计
SELECT category, COUNT(*) AS order_count, SUM(amount) AS total
FROM sales
GROUP BY category;

-- HAVING 过滤分组
SELECT category, COUNT(*) AS cnt
FROM sales
GROUP BY category
HAVING cnt > 10;

-- WHERE vs HAVING
-- WHERE 过滤行，HAVING 过滤分组</pre>

<h5>6. 实战练习</h5>
<pre class="bg-light p-3 rounded">-- 查找2024年销售额最高的前5个客户
SELECT customer_name, SUM(amount) AS total_sales
FROM sales
WHERE YEAR(order_date) = 2024
GROUP BY customer_name
ORDER BY total_sales DESC
LIMIT 5;

-- 统计每个月的订单数量
SELECT MONTH(order_date) AS month, COUNT(*) AS orders
FROM sales
WHERE YEAR(order_date) = 2024
GROUP BY MONTH(order_date)
ORDER BY month;</pre>''',
        'code_example': '''sales = [
    {"订单号": 1, "客户": "张三", "金额": 5800, "类别": "电子产品"},
    {"订单号": 2, "客户": "李四", "金额": 3200, "类别": "服装"},
    {"订单号": 3, "客户": "王五", "金额": 7200, "类别": "电子产品"},
    {"订单号": 4, "客户": "赵六", "金额": 1500, "类别": "食品"},
    {"订单号": 5, "客户": "钱七", "金额": 4800, "类别": "电子产品"},
]

high_value = [s for s in sales if s["金额"] > 5000]
print("高价值订单:")
for s in high_value:
    print(f"  {s['客户']}: ¥{s['金额']}")

from collections import defaultdict
category_stats = defaultdict(lambda: {"count": 0, "total": 0})
for s in sales:
    cat = s["类别"]
    category_stats[cat]["count"] += 1
    category_stats[cat]["total"] += s["金额"]

print("\\n按类别统计:")
for cat, stats in category_stats.items():
    avg = stats["total"] / stats["count"]
    print(f"  {cat}: {stats['count']}单, 总计¥{stats['total']}, 均值¥{avg:.0f}")''',
        'tips': [
            'SELECT * 查询所有列，但生产环境应指定具体列名',
            'WHERE 条件在 GROUP BY 之前执行，HAVING 在分组之后执行',
            'LIKE 中 % 匹配任意字符，_ 匹配单个字符',
            'ORDER BY 多个列时，按从左到右优先级排序',
            'LIMIT 5 OFFSET 10 可跳过前10条，返回接下来的5条',
            'DISTINCT 应用于所有选择的列，而非仅第一列'
        ],
        'quiz': [
            {'q': '查询所有列使用？', 'options': ['SELECT *', 'SELECT ALL', 'SELECT columns', 'SELECT * FROM'], 'answer': 0},
            {'q': '按销售额降序排序使用？', 'options': ['ORDER BY 销售额 DESC', 'ORDER BY 销售额', 'SORT BY 销售额 DESC', 'ORDER DESC 销售额'], 'answer': 0},
            {'q': '筛选条件使用哪个关键字？', 'options': ['WHERE', 'IF', 'FILTER', 'CONDITION'], 'answer': 0}
        ]},
    16: {'id': 16, 'course_id': 4, 'title': '多表连接查询', 'duration': '4小时',
        'content': '''<h4>多表查询概述</h4>
<p>实际业务中，数据通常分布在多个表中。本章节学习如何连接和组合多表数据。</p>

<h5>1. 表连接基础</h5>
<pre class="bg-light p-3 rounded">-- 内连接（INNER JOIN）- 只保留匹配的行
SELECT o.order_id, o.amount, c.customer_name, c.city
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;

-- 左连接（LEFT JOIN）- 保留左表所有行
SELECT o.order_id, o.amount, c.customer_name
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id;

-- 右连接（RIGHT JOIN）- 保留右表所有行
SELECT o.order_id, o.amount, c.customer_name
FROM orders o
RIGHT JOIN customers c ON o.customer_id = c.customer_id;

-- 全外连接（FULL OUTER JOIN）- 保留所有行
SELECT o.order_id, c.customer_name
FROM orders o
FULL OUTER JOIN customers c ON o.customer_id = c.customer_id;</pre>

<h5>2. 多表连接</h5>
<pre class="bg-light p-3 rounded">-- 连接多个表
SELECT 
    o.order_id,
    c.customer_name,
    p.product_name,
    o.amount
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id
INNER JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= "2024-01-01";</pre>

<h5>3. 自连接</h5>
<pre class="bg-light p-3 rounded">-- 员工表的自连接（查找经理）
SELECT 
    e.employee_name AS employee,
    m.employee_name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.employee_id;</pre>

<h5>4. 子查询</h5>
<pre class="bg-light p-3 rounded">-- 标量子查询（返回单个值）
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 表子查询（返回表）
SELECT *
FROM orders
WHERE customer_id IN (
    SELECT customer_id 
    FROM customers 
    WHERE city = "北京"
);

-- 使用 EXISTS
SELECT customer_name
FROM customers c
WHERE EXISTS (
    SELECT 1 FROM orders o 
    WHERE o.customer_id = c.customer_id AND o.amount > 5000
);</pre>

<h5>5. 联合查询</h5>
<pre class="bg-light p-3 rounded">-- UNION 合并（自动去重）
SELECT customer_name, "订单" AS source FROM orders
UNION
SELECT supplier_name, "供应商" AS source FROM suppliers;

-- UNION ALL 不去重
SELECT category FROM products_2023
UNION ALL
SELECT category FROM products_2024;</pre>

<h5>6. 高级应用</h5>
<pre class="bg-light p-3 rounded">-- 计算每个客户的订单占比
SELECT 
    customer_name,
    amount,
    SUM(amount) OVER (PARTITION BY customer_id) AS customer_total,
    ROUND(amount * 100.0 / SUM(amount) OVER (PARTITION BY customer_id), 2) AS percentage
FROM orders o
INNER JOIN customers c ON o.customer_id = c.customer_id;</pre>''',
        'code_example': '''customers = [
    {"客户ID": 1, "姓名": "张三", "城市": "北京"},
    {"客户ID": 2, "姓名": "李四", "城市": "上海"},
    {"客户ID": 3, "姓名": "王五", "城市": "广州"},
]

orders = [
    {"订单号": 101, "客户ID": 1, "金额": 5800},
    {"订单号": 102, "客户ID": 2, "金额": 3200},
    {"订单号": 103, "客户ID": 1, "金额": 7200},
    {"订单号": 104, "客户ID": 4, "金额": 1500},  # 不存在的客户ID
]

print("=== 内连接（匹配的客户和订单）===")
for o in orders:
    for c in customers:
        if o["客户ID"] == c["客户ID"]:
            print(f"{c['姓名']}({c['城市']}): 订单{o['订单号']} ¥{o['金额']}")

print("\\n=== 左连接（包含所有客户）===")
for c in customers:
    found = False
    for o in orders:
        if o["客户ID"] == c["客户ID"]:
            print(f"{c['姓名']}: 有订单")
            found = True
    if not found:
        print(f"{c['姓名']}: 无订单")''',
        'tips': [
            'INNER JOIN 只保留两表都有的匹配行，LEFT JOIN 保留左表全部',
            '连接条件用 ON，不建议在 WHERE 中写连接条件',
            '子查询可以嵌套，但注意性能影响',
            'UNION 去重开销大，如不需要去重用 UNION ALL',
            '多表连接注意表的顺序和别名使用',
            '使用 EXPLAIN 查看查询执行计划优化性能'
        ],
        'quiz': [
            {'q': 'INNER JOIN返回什么数据？', 'options': ['两表匹配的行', '左表全部行', '右表全部行', '两表所有行'], 'answer': 0},
            {'q': 'LEFT JOIN的特点是？', 'options': ['保留左表全部行', '保留右表全部行', '只返回匹配行', '返回两表所有行'], 'answer': 0},
            {'q': 'ON关键字用于指定？', 'options': ['连接条件', '筛选条件', '排序条件', '分组条件'], 'answer': 0}
        ]},
    17: {'id': 17, 'course_id': 4, 'title': '聚合与分组', 'duration': '4小时',
        'content': '''<h4>聚合与分组概述</h4>
<p>SQL提供强大的聚合函数和分组功能，可以快速汇总和分析数据。</p>

<h5>1. 常用聚合函数</h5>
<pre class="bg-light p-3 rounded">-- COUNT - 计数
SELECT COUNT(*) FROM sales;                    -- 所有行
SELECT COUNT(DISTINCT customer_id) FROM sales; -- 去重计数

-- SUM - 求和
SELECT SUM(amount) FROM sales WHERE category = "电子产品";

-- AVG - 平均值
SELECT AVG(amount) FROM sales;

-- MAX/MIN - 最大最小值
SELECT MAX(amount), MIN(amount) FROM sales;

-- 组合使用
SELECT 
    COUNT(*) AS total_orders,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    MAX(amount) AS max_amount,
    MIN(amount) AS min_amount
FROM sales;</pre>

<h5>2. GROUP BY 分组</h5>
<pre class="bg-light p-3 rounded">-- 按单列分组
SELECT category, SUM(amount) AS total
FROM sales
GROUP BY category;

-- 按多列分组
SELECT category, region, SUM(amount) AS total
FROM sales
GROUP BY category, region;

-- 按表达式分组
SELECT 
    YEAR(order_date) AS year,
    MONTH(order_date) AS month,
    SUM(amount) AS total
FROM sales
GROUP BY YEAR(order_date), MONTH(order_date)
ORDER BY year, month;</pre>

<h5>3. HAVING 过滤分组</h5>
<pre class="bg-light p-3 rounded">-- WHERE vs HAVING
-- WHERE 过滤行（在分组前）
-- HAVING 过滤分组（在分组后）

-- 示例：找出销售额超过10000的类别
SELECT category, SUM(amount) AS total
FROM sales
GROUP BY category
HAVING SUM(amount) > 10000;

-- 复杂条件
SELECT category, COUNT(*) AS cnt
FROM sales
WHERE YEAR(order_date) = 2024
GROUP BY category
HAVING COUNT(*) > 10 AND SUM(amount) > 50000;</pre>

<h5>4. 高级聚合</h5>
<pre class="bg-light p-3 rounded">-- GROUP_CONCAT 连接字符串
SELECT 
    category,
    GROUP_CONCAT(DISTINCT product_name ORDER BY product_name) AS products
FROM sales
GROUP BY category;

-- 多列聚合
SELECT 
    category,
    SUM(amount) AS total_amount,
    AVG(amount) AS avg_amount,
    COUNT(*) AS order_count
FROM sales
GROUP BY category;

-- 条件聚合
SELECT 
    category,
    SUM(CASE WHEN status = "已完成" THEN amount ELSE 0 END) AS completed,
    SUM(CASE WHEN status = "进行中" THEN amount ELSE 0 END) AS processing
FROM sales
GROUP BY category;</pre>

<h5>5. WITH ROLLUP 添加汇总</h5>
<pre class="bg-light p-3 rounded">-- 添加小计和总计
SELECT 
    COALESCE(category, "总计") AS category,
    SUM(amount) AS total
FROM sales
GROUP BY category WITH ROLLUP;

-- 多级汇总
SELECT 
    COALESCE(category, "全部") AS category,
    COALESCE(region, "全部") AS region,
    SUM(amount) AS total
FROM sales
GROUP BY category, region WITH ROLLUP;</pre>

<h5>6. 实战案例</h5>
<pre class="bg-light p-3 rounded">-- 月度销售报表
SELECT 
    DATE_FORMAT(order_date, "%Y-%m") AS month,
    COUNT(*) AS orders,
    SUM(amount) AS revenue,
    AVG(amount) AS avg_order,
    SUM(profit) AS profit
FROM sales
WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY DATE_FORMAT(order_date, "%Y-%m")
ORDER BY month DESC;</pre>''',
        'code_example': '''from collections import defaultdict

sales = [
    {"类别": "电子产品", "月份": "1月", "金额": 5800},
    {"类别": "服装", "月份": "1月", "金额": 3200},
    {"类别": "电子产品", "月份": "2月", "金额": 7200},
    {"类别": "服装", "月份": "2月", "金额": 2800},
    {"类别": "食品", "月份": "1月", "金额": 1500},
]

print("=== 按类别统计 ===")
cat_stats = defaultdict(lambda: {"count": 0, "total": 0})
for s in sales:
    cat_stats[s["类别"]]["count"] += 1
    cat_stats[s["类别"]]["total"] += s["金额"]

for cat, stats in cat_stats.items():
    avg = stats["total"] / stats["count"]
    print(f"{cat}: {stats['count']}单, 总计¥{stats['total']}, 均值¥{avg:.0f}")

print("\\n=== 筛选销售额>5000的类别 ===")
for cat, stats in cat_stats.items():
    if stats["total"] > 5000:
        print(f"{cat}: ¥{stats['total']}")''',
        'tips': [
            'SELECT 中的列必须出现在 GROUP BY 中，或被聚合函数包裹',
            'WHERE 在分组前过滤，HAVING 在分组后过滤',
            'COUNT(*) 包含 NULL 行，COUNT(column) 忽略 NULL',
            'WITH ROLLUP 添加分类汇总和总计行',
            'COALESCE() 处理 ROLLUP 产生的 NULL',
            '条件聚合可用 CASE WHEN 实现'
        ],
        'quiz': [
            {'q': '计算总和使用哪个聚合函数？', 'options': ['SUM()', 'TOTAL()', 'ADD()', 'COUNT()'], 'answer': 0},
            {'q': 'HAVING关键字用于？', 'options': ['过滤聚合结果', '过滤行', '排序', '分组'], 'answer': 0},
            {'q': 'COUNT(*)和COUNT(列名)的区别是？', 'options': ['COUNT(*)包含NULL', 'COUNT(列名)包含NULL', '没区别', 'COUNT(*)更快'], 'answer': 0}
        ]},
    18: {'id': 18, 'course_id': 4, 'title': '子查询与窗口函数', 'duration': '4小时',
        'content': '''<h4>高级查询技术</h4>
<p>子查询和窗口函数是SQL的高级特性，可以解决复杂的查询问题。</p>

<h5>1. 子查询类型</h5>
<pre class="bg-light p-3 rounded">-- 标量子查询（返回单个值）
SELECT product_name, price
FROM products
WHERE price > (SELECT AVG(price) FROM products);

-- 列子查询（返回一列）
SELECT *
FROM orders
WHERE customer_id IN (
    SELECT customer_id FROM customers WHERE vip = 1
);

-- 表子查询（返回表）
SELECT *
FROM (
    SELECT category, SUM(amount) AS total
    FROM sales GROUP BY category
) AS category_summary
WHERE total > 100000;</pre>

<h5>2. 窗口函数基础</h5>
<pre class="bg-light p-3 rounded">-- 基础语法
SELECT 
    column_name,
    window_function() OVER (
        PARTITION BY column1
        ORDER BY column2
    ) AS result
FROM table_name;

-- 示例：累计销售额
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS cumulative
FROM sales;</pre>

<h5>3. 排名函数</h5>
<pre class="bg-light p-3 rounded">-- ROW_NUMBER - 连续排名（无并列）
SELECT 
    order_id, amount,
    ROW_NUMBER() OVER (ORDER BY amount DESC) AS rank
FROM orders;

-- RANK - 有间隙排名
SELECT 
    order_id, amount,
    RANK() OVER (ORDER BY amount DESC) AS rank
FROM orders;

-- DENSE_RANK - 密集排名（无间隙）
SELECT 
    order_id, amount,
    DENSE_RANK() OVER (ORDER BY amount DESC) AS rank
FROM orders;</pre>

<h5>4. 移动计算</h5>
<pre class="bg-light p-3 rounded">-- 累计求和
SELECT 
    order_date,
    amount,
    SUM(amount) OVER (ORDER BY order_date) AS cumulative_sum
FROM sales;

-- 移动平均
SELECT 
    order_date,
    amount,
    AVG(amount) OVER (
        ORDER BY order_date 
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS moving_avg_3d
FROM sales;

-- LAG 和 LEAD
SELECT 
    order_date,
    amount,
    LAG(amount, 1) OVER (ORDER BY order_date) AS prev_amount,
    LEAD(amount, 1) OVER (ORDER BY order_date) AS next_amount
FROM sales;</pre>

<h5>5. FIRST_VALUE 和 LAST_VALUE</h5>
<pre class="bg-light p-3 rounded">-- 获取分组内第一个/最后一个值
SELECT 
    order_date,
    amount,
    FIRST_VALUE(amount) OVER (
        PARTITION BY DATE_FORMAT(order_date, "%Y-%m")
        ORDER BY order_date
    ) AS first_amount_in_month,
    LAST_VALUE(amount) OVER (
        PARTITION BY DATE_FORMAT(order_date, "%Y-%m")
        ORDER BY order_date
        RANGE BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
    ) AS last_amount_in_month
FROM sales;</pre>

<h5>6. NTILE 分桶</h5>
<pre class="bg-light p-3 rounded">-- 将数据分成4组
SELECT 
    order_id,
    amount,
    NTILE(4) OVER (ORDER BY amount) AS quartile
FROM orders;

-- 按组内排名
SELECT 
    category,
    order_id,
    amount,
    ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rank_in_cat
FROM orders;</pre>''',
        'code_example': '''sales = [
    {"日期": "2024-01-01", "类别": "电子产品", "金额": 5800},
    {"日期": "2024-01-02", "类别": "服装", "金额": 3200},
    {"日期": "2024-01-03", "类别": "电子产品", "金额": 7200},
    {"日期": "2024-01-04", "类别": "食品", "金额": 1500},
]

sorted_by_amount = sorted(sales, key=lambda x: x["金额"], reverse=True)
print("=== 按金额排名 ===")
for i, s in enumerate(sorted_by_amount, 1):
    print(f"第{i}名: {s['类别']} ¥{s['金额']}")

print("\\n=== 累计销售额 ===")
sorted_by_date = sorted(sales, key=lambda x: x["日期"])
cumulative = 0
for s in sorted_by_date:
    cumulative += s["金额"]
    print(f"{s['日期']}: 当日¥{s['金额']}, 累计¥{cumulative}")

print("\\n=== 分组内排名 ===")
from collections import defaultdict
groups = defaultdict(list)
for s in sales:
    groups[s["类别"]].append(s)

for cat, items in groups.items():
    ranked = sorted(items, key=lambda x: x["金额"], reverse=True)
    print(f"{cat}:")
    for i, item in enumerate(ranked, 1):
        print(f"  第{i}名: ¥{item['金额']}")''',
        'tips': [
            '窗口函数不改变原表行数，这是与聚合函数的本质区别',
            'PARTITION BY 类似 GROUP BY，但不合并行',
            'ORDER BY 控制窗口内的排序，影响 LAG/LEAD 等函数',
            'ROWS BETWEEN 指定物理窗口，RANGE BETWEEN 指定逻辑窗口',
            '在 SELECT 中使用窗口函数，不影响 WHERE 的执行',
            '窗口函数可以链式使用'
        ],
        'quiz': [
            {'q': '窗口函数的OVER子句用于？', 'options': ['定义窗口范围', '排序', '分组', '筛选'], 'answer': 0},
            {'q': 'ROW_NUMBER()的作用是？', 'options': ['生成行号', '计算总和', '求平均值', '计数'], 'answer': 0},
            {'q': 'PARTITION BY的作用是？', 'options': ['分区', '排序', '过滤', '聚合'], 'answer': 0}
        ]},
    19: {'id': 19, 'course_id': 5, 'title': '描述统计与概率', 'duration': '5小时',
        'content': '''<h4>描述性统计基础</h4>
<p>描述性统计是对数据特征进行量化和总结的方法，是数据分析的第一步。</p>

<h5>1. 集中趋势</h5>
<pre class="bg-light p-3 rounded">import pandas as pd
import numpy as np

data = pd.Series([10, 15, 20, 25, 30, 35, 40, 45, 50, 100])

# 均值（Mean）- 算术平均
mean = data.mean()
print(f"均值: {mean}")

# 中位数（Median）- 排序后中间值
median = data.median()
print(f"中位数: {median}")

# 众数（Mode）- 出现最多的值
mode = data.mode()
print(f"众数: {mode.values}")

# 切尾均值（Trimmed Mean）
from scipy import stats
trimmed = stats.trim_mean(data, 0.1)  # 去掉10%的极端值
print(f"切尾均值: {trimmed}")</pre>

<h5>2. 离散程度</h5>
<pre class="bg-light p-3 rounded"># 方差（Variance）- 数据分散程度
variance = data.var()
print(f"方差: {variance}")

# 标准差（Standard Deviation）
std = data.std()
print(f"标准差: {std}")

# 变异系数（CV）
cv = (std / mean) * 100
print(f"变异系数: {cv:.2f}%")

# 极差（Range）
range_val = data.max() - data.min()
print(f"极差: {range_val}")

# 四分位距（IQR）
q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
iqr = q3 - q1
print(f"IQR: {iqr}")</pre>

<h5>3. 分布形态</h5>
<pre class="bg-light p-3 rounded"># 偏度（Skewness）- 分布对称性
skewness = data.skew()
print(f"偏度: {skewness}")
# > 0 右偏，< 0 左偏，= 0 对称

# 峰度（Kurtosis）
kurtosis = data.kurtosis()
print(f"峰度: {kurtosis}")
# > 0 尖峰，< 0 平坦，= 0 正态分布

# 正态性检验
from scipy import stats
stat, p_value = stats.shapiro(data)
print(f"Shapiro-Wilk检验: p={p_value:.4f}")</pre>

<h5>4. 位置度量</h5>
<pre class="bg-light p-3 rounded"># 分位数
print(f"最小值: {data.min()}")
print(f"25%分位: {data.quantile(0.25)}")
print(f"50%分位: {data.median()}")
print(f"75%分位: {data.quantile(0.75)}")
print(f"最大值: {data.max()}")

# 百分位数
print(f"90%分位: {data.quantile(0.90)}")
print(f"95%分位: {data.quantile(0.95)}")
print(f"99%分位: {data.quantile(0.99)}")</pre>

<h5>5. 描述统计汇总</h5>
<pre class="bg-light p-3 rounded"># 使用 describe()
print(data.describe())

# 自定义统计报告
def describe_stats(s):
    return pd.Series({
        "样本数": len(s),
        "均值": s.mean(),
        "标准差": s.std(),
        "最小值": s.min(),
        "25%分位": s.quantile(0.25),
        "中位数": s.median(),
        "75%分位": s.quantile(0.75),
        "最大值": s.max(),
        "偏度": s.skew(),
        "峰度": s.kurtosis()
    })

print(describe_stats(data))</pre>''',
        'code_example': '''import statistics

data = [10, 15, 20, 25, 30, 35, 40, 45, 50, 100]

print("=== 集中趋势 ===")
print(f"均值: {statistics.mean(data):.2f}")
print(f"中位数: {statistics.median(data):.2f}")
print(f"众数: {statistics.mode(data)}")

print("\\n=== 离散程度 ===")
print(f"方差: {statistics.variance(data):.2f}")
print(f"标准差: {statistics.stdev(data):.2f}")
sorted_data = sorted(data)
n = len(sorted_data)
q1 = sorted_data[n//4]
q3 = sorted_data[3*n//4]
print(f"IQR: {q3 - q1}")

print("\\n=== 位置度量 ===")
print(f"最小值: {min(data)}")
print(f"最大值: {max(data)}")
print(f"范围: {max(data) - min(data)}")

def percentile(data, p):
    sorted_d = sorted(data)
    k = (len(sorted_d) - 1) * p
    f = int(k)
    c = f + 1
    if c >= len(sorted_d):
        return sorted_d[f]
    return sorted_d[f] + (k - f) * (sorted_d[c] - sorted_d[f])

print(f"25%分位: {percentile(data, 0.25):.1f}")
print(f"50%分位: {percentile(data, 0.50):.1f}")
print(f"75%分位: {percentile(data, 0.75):.1f}")''',
        'tips': [
            '均值易受极端值影响，中位数对异常值更稳健',
            '标准差单位与原数据相同，方差单位是原数据的平方',
            '变异系数用于比较不同量纲数据的离散程度',
            '偏度 > 0 表示右偏，数据右侧有长尾',
            'IQR 用于检测异常值，异常值通常定义为 < Q1-1.5*IQR',
            'describe() 快速获取完整统计摘要'
        ],
        'quiz': [
            {'q': '描述统计中50%分位数对应什么？', 'options': ['中位数', '均值', '众数', '标准差'], 'answer': 0},
            {'q': '标准差衡量什么？', 'options': ['数据离散程度', '数据中心位置', '数据偏斜程度', '数据峰值'], 'answer': 0},
            {'q': '偏度大于0表示什么？', 'options': ['右偏分布', '左偏分布', '对称分布', '均匀分布'], 'answer': 0}
        ]},
    20: {'id': 20, 'course_id': 5, 'title': '假设检验', 'duration': '6小时',
        'content': '''<h4>假设检验基础</h4>
<p>假设检验是统计推断的核心方法，用于判断样本数据是否支持某个假设。</p>

<h5>1. 假设检验概念</h5>
<pre class="bg-light p-3 rounded"># 假设检验步骤
# 1. 建立原假设 H0 和备择假设 H1
# 2. 选择显著性水平 α（通常为0.05）
# 3. 计算检验统计量
# 4. 确定p值
# 5. 做出决策：p < α 则拒绝H0

# 决策规则
# p < 0.05: 拒绝原假设，差异显著
# p >= 0.05: 不能拒绝原假设，差异不显著</pre>

<h5>2. 单样本t检验</h5>
<pre class="bg-light p-3 rounded">from scipy import stats
import numpy as np

# 检验样本均值是否等于已知总体均值
sample = np.array([98, 102, 95, 105, 100, 99, 101, 97, 103, 100])
pop_mean = 100  # 总体均值假设

# 单样本t检验
t_stat, p_value = stats.ttest_1samp(sample, pop_mean)
print(f"t统计量: {t_stat:.4f}")
print(f"p值: {p_value:.4f}")

if p_value < 0.05:
    print("拒绝H0: 样本均值与总体均值存在显著差异")
else:
    print("不能拒绝H0")</pre>

<h5>3. 独立样本t检验</h5>
<pre class="bg-light p-3 rounded"># 比较两组独立样本的均值
group1 = np.array([85, 90, 88, 92, 87, 91, 89, 93, 86, 88])
group2 = np.array([78, 82, 75, 80, 77, 83, 76, 81, 79, 74])

# 独立样本t检验
t_stat, p_value = stats.ttest_ind(group1, group2)
print(f"t统计量: {t_stat:.4f}")
print(f"p值: {p_value:.4f}")

# 方差齐性检验
f_stat, p_f = stats.levene(group1, group2)
print(f"Levene检验 p值: {p_f:.4f}")

# 如果方差不齐，使用Welch's t检验
t_stat_welch, p_welch = stats.ttest_ind(group1, group2, equal_var=False)
print(f"Welch's t检验 p值: {p_welch:.4f}")</pre>

<h5>4. 配对样本t检验</h5>
<pre class="bg-light p-3 rounded"># 同一组样本在两个时间点的比较
before = np.array([120, 130, 125, 140, 135, 128, 132, 138, 125, 130])
after = np.array([115, 125, 120, 132, 128, 122, 126, 130, 118, 124])

# 配对样本t检验
t_stat, p_value = stats.ttest_rel(before, after)
print(f"t统计量: {t_stat:.4f}")
print(f"p值: {p_value:.4f}")

if p_value < 0.05:
    print("拒绝H0: 干预前后存在显著差异")
else:
    print("不能拒绝H0: 干预前后无显著差异")</pre>

<h5>5. ANOVA（方差分析）</h5>
<pre class="bg-light p-3 rounded"># 比较三组及以上样本均值
group_a = np.array([85, 90, 88, 92, 87])
group_b = np.array([78, 82, 75, 80, 77])
group_c = np.array([95, 98, 92, 96, 94])

# 单因素ANOVA
f_stat, p_value = stats.f_oneway(group_a, group_b, group_c)
print(f"F统计量: {f_stat:.4f}")
print(f"p值: {p_value:.4f}")

if p_value < 0.05:
    print("拒绝H0: 至少有两组均值存在显著差异")</pre>

<h5>6. 卡方检验</h5>
<pre class="bg-light p-3 rounded"># 检验分类变量之间的独立性
from scipy.stats import chi2_contingency

# 列联表
observed = np.array([
    [120, 80],  # 男性：购买/未购买
    [90, 110]   # 女性：购买/未购买
])

chi2, p_value, dof, expected = chi2_contingency(observed)
print(f"卡方统计量: {chi2:.4f}")
print(f"p值: {p_value:.4f}")
print(f"自由度: {dof}")

if p_value < 0.05:
    print("拒绝H0: 性别与购买行为存在显著关联")</pre>''',
        'code_example': '''import statistics
import math

group1 = [85, 90, 88, 92, 87, 91, 89, 93, 86, 88]
group2 = [78, 82, 75, 80, 77, 83, 76, 81, 79, 74]

mean1, mean2 = statistics.mean(group1), statistics.mean(group2)
std1, std2 = statistics.stdev(group1), statistics.stdev(group2)
n1, n2 = len(group1), len(group2)

print("=== 两组数据比较 ===")
print(f"A组: 均值={mean1:.2f}, 标准差={std1:.2f}, n={n1}")
print(f"B组: 均值={mean2:.2f}, 标准差={std2:.2f}, n={n2}")

diff = mean1 - mean2
pooled_std = math.sqrt((std1**2/n1 + std2**2/n2))
t_stat = diff / pooled_std

print(f"\\n均值差异: {diff:.2f}")
print(f"差异标准误: {pooled_std:.2f}")
print(f"t统计量: {t_stat:.4f}")
print(f"\\n结论: A组均值{'高于' if diff > 0 else '低于'}B组")''',
        'tips': [
            'p值 < 0.05 通常表示统计显著',
            '单样本t检验：样本均值 vs 总体均值',
            '独立样本t检验：两组独立样本均值比较',
            '配对样本t检验：同一组样本两次测量比较',
            'ANOVA：比较三组及以上样本均值',
            '卡方检验：分析分类变量之间的关系'
        ],
        'quiz': [
            {'q': 'p值小于0.05通常意味着什么？', 'options': ['拒绝原假设', '接受原假设', '样本量不足', '数据有问题'], 'answer': 0},
            {'q': '独立样本t检验用于比较？', 'options': ['两组独立样本均值', '两组相关样本均值', '多组均值', '方差'], 'answer': 0},
            {'q': '方差分析(ANOVA)用于？', 'options': ['比较三组及以上均值', '比较两组均值', '计算相关系数', '回归分析'], 'answer': 0}
        ]},
    21: {'id': 21, 'course_id': 5, 'title': '相关与回归分析', 'duration': '6小时',
        'content': '''<h4>相关与回归分析</h4>
<p>相关分析用于衡量变量之间的关系强度，回归分析用于建立预测模型。</p>

<h5>1. 相关系数</h5>
<pre class="bg-light p-3 rounded">import pandas as pd
import numpy as np

# 示例数据
df = pd.DataFrame({
    "广告投入": [10, 15, 20, 25, 30, 35, 40],
    "销售额": [100, 150, 180, 220, 260, 300, 350],
    "客户数": [20, 30, 35, 45, 55, 65, 70]
})

# Pearson相关系数
corr = df["广告投入"].corr(df["销售额"])
print(f"Pearson相关系数: {corr:.4f}")

# Spearman秩相关系数
spearman = df["广告投入"].corr(df["销售额"], method="spearman")
print(f"Spearman相关系数: {spearman:.4f}")

# 相关矩阵
corr_matrix = df.corr()
print(corr_matrix)</pre>

<h5>2. 相关性解读</h5>
<pre class="bg-light p-3 rounded"># 相关系数解读
# |r| < 0.3    弱相关
# 0.3 <= |r| < 0.7  中等相关
# |r| >= 0.7   强相关

def interpret_correlation(r):
    r = abs(r)
    if r < 0.3:
        return "弱相关"
    elif r < 0.7:
        return "中等相关"
    else:
        return "强相关"

print(interpret_correlation(0.85))  # 强相关</pre>

<h5>3. 简单线性回归</h5>
<pre class="bg-light p-3 rounded">from sklearn.linear_model import LinearRegression
import numpy as np

# 准备数据
X = df[["广告投入"]].values
y = df["销售额"].values

# 拟合模型
model = LinearRegression()
model.fit(X, y)

# 系数
print(f"截距: {model.intercept_:.2f}")
print(f"斜率: {model.coef_[0]:.2f}")
print(f"R²: {model.score(X, y):.4f}")

# 预测
new_ad = np.array([[50]])
predicted = model.predict(new_ad)
print(f"广告投入50时的预测销售额: {predicted[0]:.2f}")</pre>

<h5>4. 多元线性回归</h5>
<pre class="bg-light p-3 rounded">from sklearn.linear_model import LinearRegression

# 准备数据 - 多个特征
X = df[["广告投入", "客户数"]].values
y = df["销售额"].values

# 拟合模型
model = LinearRegression()
model.fit(X, y)

print(f"截距: {model.intercept_:.2f}")
print(f"广告投入系数: {model.coef_[0]:.2f}")
print(f"客户数系数: {model.coef_[1]:.2f}")
print(f"R²: {model.score(X, y):.4f}")</pre>

<h5>5. 回归诊断</h5>
<pre class="bg-light p-3 rounded">from scipy import stats

# 计算残差
y_pred = model.predict(X)
residuals = y - y_pred

# 残差分析
print(f"残差均值: {residuals.mean():.4f}")
print(f"残差标准差: {residuals.std():.4f}")

# 正态性检验
stat, p = stats.shapiro(residuals)
print(f"残差正态性检验 p值: {p:.4f}")

# 异常值检测
z_scores = np.abs(stats.zscore(residuals))
outliers = np.where(z_scores > 3)
print(f"异常值索引: {outliers}")</pre>

<h5>6. 回归结果可视化</h5>
<pre class="bg-light p-3 rounded">import matplotlib.pyplot as plt

# 预测值 vs 实际值
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 图1: 回归线
axes[0].scatter(df["广告投入"], df["销售额"], color="blue")
axes[0].plot(df["广告投入"], y_pred, color="red", linewidth=2)
axes[0].set_xlabel("广告投入")
axes[0].set_ylabel("销售额")
axes[0].set_title("简单线性回归")

# 图2: 残差图
axes[1].scatter(y_pred, residuals)
axes[1].axhline(y=0, color="red", linestyle="--")
axes[1].set_xlabel("预测值")
axes[1].set_ylabel("残差")
axes[1].set_title("残差图")

plt.tight_layout()
plt.show()</pre>''',
        'code_example': '''import statistics
import math

ad_spend = [10, 15, 20, 25, 30, 35, 40]  # 广告投入
sales = [100, 150, 180, 220, 260, 300, 350]  # 销售额

n = len(ad_spend)
mean_x, mean_y = statistics.mean(ad_spend), statistics.mean(sales)
cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(ad_spend, sales)) / n
std_x, std_y = statistics.stdev(ad_spend), statistics.stdev(sales)
corr = cov / (std_x * std_y)

print("=== 相关性分析 ===")
print(f"相关系数: {corr:.4f}")
print(f"解释: {'强正相关' if corr > 0.7 else '中等正相关' if corr > 0.3 else '弱相关'}")

x = ad_spend
y = sales
mean_x, mean_y = statistics.mean(x), statistics.mean(y)
slope = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / sum((xi - mean_x)**2 for xi in x)
intercept = mean_y - slope * mean_x

print(f"\\n=== 线性回归 ===")
print(f"斜率: {slope:.2f}")
print(f"截距: {intercept:.2f}")
print(f"回归方程: 销售额 = {intercept:.2f} + {slope:.2f} * 广告投入")

new_ad = 50
pred_sales = intercept + slope * new_ad
print(f"\\n广告投入{new_ad}时预测销售额: {pred_sales:.0f}")''',
        'tips': [
            'Pearson相关系数适用于线性关系，Spearman适用于单调关系',
            '相关性不等于因果性，高相关可能是第三方变量导致',
            'R² 表示模型解释的方差比例，越接近1越好',
            '回归诊断检查残差是否符合假设（正态性、独立性、同方差性）',
            'VIF（方差膨胀因子）用于检测多重共线性',
            '标准化回归系数可以比较不同特征的相对重要性'
        ],
        'quiz': [
            {'q': '皮尔逊相关系数的取值范围是？', 'options': ['[-1, 1]', '[0, 1]', '[-∞, +∞]', '[0, 100]'], 'answer': 0},
            {'q': '相关系数为0表示？', 'options': ['无线性关系', '完全负相关', '完全正相关', '不确定'], 'answer': 0},
            {'q': 'R²表示什么？', 'options': ['模型解释度', '相关系数', '回归系数', 'p值'], 'answer': 0}
        ]},
    22: {'id': 22, 'course_id': 5, 'title': 'A/B测试原理', 'duration': '5小时',
        'content': '''<h4>A/B测试基础</h4>
<p>A/B测试是一种对照实验方法，用于比较两种或多种方案的效果，是数据驱动决策的重要工具。</p>

<h5>1. A/B测试概念</h5>
<pre class="bg-light p-3 rounded"># A/B测试流程
# 1. 明确业务目标和关键指标（KPI）
# 2. 提出假设
# 3. 设计实验（样本量、流量分配）
# 4. 收集数据
# 5. 统计分析
# 6. 做出决策

# 常见指标
# - 转化率（点击、注册、购买）
# - 用户停留时间
# - 客单价
# - 用户满意度</pre>

<h5>2. 实验设计</h5>
<pre class="bg-light p-3 rounded">import numpy as np

# 计算样本量
def calculate_sample_size(base_rate, mde, alpha=0.05, power=0.8):
    """
    base_rate: 基准转化率
    mde: 最小可检测效应（相对提升）
    alpha: 显著性水平
    power: 统计功效
    """
    p1 = base_rate
    p2 = base_rate * (1 + mde)
    
    # 简化计算
    effect = (p2 - p1) ** 2
    n = 16 * p1 * (1 - p1) / effect
    
    return int(np.ceil(n))

# 示例：基准转化率5%，希望检测到10%相对提升
sample_size = calculate_sample_size(0.05, 0.10)
print(f"每组所需样本量: {sample_size}")
print(f"总样本量: {sample_size * 2}")</pre>

<h5>3. 转化率检验</h5>
<pre class="bg-light p-3 rounded">from scipy import stats

# A组和B组数据
# A组: 1000人访问，50人转化
# B组: 1000人访问，65人转化

n_a, conv_a = 1000, 50
n_b, conv_b = 1000, 65

p_a = conv_a / n_a
p_b = conv_b / n_b

# 比例z检验
from statsmodels.stats.proportion import proportions_ztest

count = np.array([conv_b, conv_a])
nobs = np.array([n_b, n_a])

z_stat, p_value = proportions_ztest(count, nobs, alternative="larger")
print(f"Z统计量: {z_stat:.4f}")
print(f"p值: {p_value:.4f}")

if p_value < 0.05:
    print("拒绝H0: B组显著优于A组")
else:
    print("不能拒绝H0")</pre>

<h5>4. 置信区间</h5>
<pre class="bg-light p-3 rounded"># 计算置信区间
def confidence_interval(p1, p2, n1, n2, confidence=0.95):
    """计算两组比例差异的置信区间"""
    from scipy.stats import norm
    
    z = norm.ppf((1 + confidence) / 2)
    p_diff = p2 - p1
    se = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    
    lower = p_diff - z * se
    upper = p_diff + z * se
    
    return lower, upper

lower, upper = confidence_interval(p_a, p_b, n_a, n_b)
print(f"95%置信区间: [{lower:.4f}, {upper:.4f}]")
print(f"相对提升: {(p_b/p_a - 1)*100:.2f}%")</pre>

<h5>5. 卡方检验</h5>
<pre class="bg-light p-3 rounded">from scipy.stats import chi2_contingency

# 构建列联表
observed = np.array([
    [conv_a, n_a - conv_a],    # A组: [转化, 未转化]
    [conv_b, n_b - conv_b]     # B组: [转化, 未转化]
])

chi2, p_value, dof, expected = chi2_contingency(observed)
print(f"卡方统计量: {chi2:.4f}")
print(f"p值: {p_value:.4f}")
print(f"自由度: {dof}")
print(f"期望频数:\\n{expected}")

if p_value < 0.05:
    print("\\n结论: 两组转化率存在显著差异")</pre>

<h5>6. 效果评估</h5>
<pre class="bg-light p-3 rounded"># 计算统计功效
def calculate_power(n, p1, p2, alpha=0.05):
    """计算统计功效"""
    from scipy.stats import norm
    
    p_avg = (p1 + p2) / 2
    se = np.sqrt(p_avg * (1 - p_avg) * (2/n))
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = (p2 - p1) / se - z_alpha
    
    power = norm.cdf(z_beta)
    return power

power = calculate_power(1000, p_a, p_b)
print(f"统计功效: {power:.4f}")</pre>''',
        'code_example': '''import math

n_a, conv_a = 1000, 50
n_b, conv_b = 1000, 65

p_a = conv_a / n_a  # 5%
p_b = conv_b / n_b  # 6.5%

print("=== A/B测试结果 ===")
print(f"A组: {n_a}访问, {conv_a}转化, 转化率={p_a*100:.1f}%")
print(f"B组: {n_b}访问, {conv_b}转化, 转化率={p_b*100:.1f}%")

lift = (p_b - p_a) / p_a
print(f"\\n相对提升: {lift*100:.1f}%")

p_diff = p_b - p_a
se = math.sqrt(p_a*(1-p_a)/n_a + p_b*(1-p_b)/n_b)
z = 1.96  # 95%置信度
lower = p_diff - z * se
upper = p_diff + z * se
print(f"95%置信区间: [{lower*100:.2f}%, {upper*100:.2f}%]")

if lower > 0:
    print("\\n结论: B组显著优于A组")
else:
    print("\\n结论: 两组无显著差异")''',
        'tips': [
            'A/B测试需要足够的样本量才能检测到统计显著差异',
            'p值 < 0.05 表示差异显著，可以拒绝原假设',
            '置信区间包含0表示无显著差异',
            '除了统计显著性，还要考虑实际业务意义',
            '多个指标时需要控制FWER（族错误率）',
            '测试时间应覆盖完整业务周期（如一周）'
        ],
        'quiz': [
            {'q': 'A/B测试的目的是什么？', 'options': ['比较不同方案效果', '预测未来趋势', '分析相关性', '聚类分析'], 'answer': 0},
            {'q': '卡方检验用于分析什么？', 'options': ['分类变量关系', '连续变量差异', '相关性', '回归系数'], 'answer': 0},
            {'q': '样本量越大，p值通常会？', 'options': ['越小', '越大', '不变', '不确定'], 'answer': 0}
        ]}
}

PROJECTS = [
    {
        'id': 1,
        'title': '电商销售数据清洗',
        'level': '初级',
        'level_color': 'success',
        'duration': '2小时',
        'dataset': 'sales_raw.csv',
        'background': '某电商平台积累了大量销售数据，但数据质量参差不齐，存在缺失值、重复值和异常值。',
        'goal': '1. 识别并处理缺失值\n2. 去除重复记录\n3. 识别并处理异常值（使用IQR方法）\n4. 导出清洗后的数据集',
        'tips': ['使用df.isnull().sum()快速查看各列缺失值数量', 'dropna()和fillna()是处理缺失值的常用方法', '使用duplicated()检查重复行', 'IQR方法：Q1 - 1.5*IQR 和 Q3 + 1.5*IQR', '处理完成后用describe()验证数据质量'],
        'pitfalls': ['直接删除所有含缺失值的行可能导致样本量大幅减少', '用均值填充缺失值时要注意数据分布', '重复值可能不是完全相同的行', '异常值不一定是错误数据', '忘记重置索引可能导致后续操作出错'],
                'starter_code': 'import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv("data/sales_raw.csv")\nprint("原始数据形状:", df.shape)\nprint("\\\n=== 缺失值检查 ===")\nprint(df.isnull().sum().to_string())\n',
                        'code': 'import pandas as pd\nfrom scipy import stats\nimport numpy as np\n\ndf = pd.read_csv("data/ab_test_data.csv")\nprint("=== A/B测试分析 ===")\nprint(f"总样本量: {len(df)}")\nprint(f"组别分布: {df[\'组别\'].value_counts().to_dict()}")\nprint(f"\\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\ngroup_ctrl = df[df["组别"] == "对照组"]\ngroup_exp = df[df["组别"] == "实验组"]\n\nprint(f"\\\n=== 对照组 ===")\nprint(f"样本量: {len(group_ctrl)}")\nprint(f"点击率: {group_ctrl[\'是否点击\'].mean():.2%}")\nprint(f"转化率: {group_ctrl[\'是否转化\'].mean():.2%}")\nprint(f"平均停留时长: {group_ctrl[\'停留时长(秒)\'].mean():.1f} 秒")\nprint(f"平均页面浏览数: {group_ctrl[\'页面浏览数\'].mean():.1f}")\n\nprint(f"\\\n=== 实验组 ===")\nprint(f"样本量: {len(group_exp)}")\nprint(f"点击率: {group_exp[\'是否点击\'].mean():.2%}")\nprint(f"转化率: {group_exp[\'是否转化\'].mean():.2%}")\nprint(f"平均停留时长: {group_exp[\'停留时长(秒)\'].mean():.1f} 秒")\nprint(f"平均页面浏览数: {group_exp[\'页面浏览数\'].mean():.1f}")\n\nprint(f"\\\n=== 核心指标对比 ===")\nconv_ctrl = group_ctrl["是否转化"].mean()\nconv_exp = group_exp["是否转化"].mean()\nclick_ctrl = group_ctrl["是否点击"].mean()\nclick_exp = group_exp["是否点击"].mean()\ntime_ctrl = group_ctrl["停留时长(秒)"].mean()\ntime_exp = group_exp["停留时长(秒)"].mean()\nprint(f"转化率: 对照组 {conv_ctrl:.2%} vs 实验组 {conv_exp:.2%} ({(conv_exp-conv_ctrl)/conv_ctrl*100:+.2f}%)")\nprint(f"点击率: 对照组 {click_ctrl:.2%} vs 实验组 {click_exp:.2%} ({(click_exp-click_ctrl)/click_ctrl*100:+.2f}%)")\nprint(f"停留时长: 对照组 {time_ctrl:.1f}s vs 实验组 {time_exp:.1f}s ({(time_exp-time_ctrl)/time_ctrl*100:+.2f}%)")\n\nprint(f"\\\n=== 转化率卡方检验 ===")\nobserved_conv = [\n    [group_ctrl["是否转化"].sum(), len(group_ctrl) - group_ctrl["是否转化"].sum()],\n    [group_exp["是否转化"].sum(), len(group_exp) - group_exp["是否转化"].sum()]\n]\nchi2, p_value, _, _ = stats.chi2_contingency(observed_conv)\nprint(f"卡方值: {chi2:.4f}")\nprint(f"p值: {p_value:.6f}")\nif p_value < 0.05:\n    print(f"结论: ✅ 差异显著 (p<0.05)，两组转化率存在统计学差异")\nelse:\n    print(f"结论: ⚠️ 差异不显著 (p>=0.05)")\n\nprint(f"\\\n=== 点击率卡方检验 ===")\nobserved_click = [\n    [group_ctrl["是否点击"].sum(), len(group_ctrl) - group_ctrl["是否点击"].sum()],\n    [group_exp["是否点击"].sum(), len(group_exp) - group_exp["是否点击"].sum()]\n]\nchi2_click, p_click, _, _ = stats.chi2_contingency(observed_click)\nprint(f"卡方值: {chi2_click:.4f}")\nprint(f"p值: {p_click:.6f}")\nif p_click < 0.05:\n    print(f"结论: ✅ 差异显著 (p<0.05)")\nelse:\n    print(f"结论: ⚠️ 差异不显著 (p>=0.05)")\n\nprint(f"\\\n=== 停留时长t检验 ===")\nt_stat, t_p = stats.ttest_ind(group_ctrl["停留时长(秒)"], group_exp["停留时长(秒)"], equal_var=False)\nprint(f"t值: {t_stat:.4f}")\nprint(f"p值: {t_p:.6f}")\nif t_p < 0.05:\n    print(f"结论: ✅ 差异显著 (p<0.05)")\nelse:\n    print(f"结论: ⚠️ 差异不显著 (p>=0.05)")\n\nprint(f"\\\n=== 最终业务建议 ===")\nconv_lift = (conv_exp - conv_ctrl) / conv_ctrl * 100\nprint(f"转化率变化: {conv_lift:+.2f}%")\nprint(f"显著性p值: {p_value:.6f}")\nif p_value < 0.05 and conv_exp > conv_ctrl:\n    print("🎯 建议: 实验组效果显著更优，可考虑全面推广")\nelif p_value < 0.05 and conv_ctrl > conv_exp:\n    print("🎯 建议: 对照组效果显著更优，应保持原方案")\nelse:\n    print("📊 建议: 效果差异不显著，需增加样本量或调整实验方案")'
    },
    {
        'id': 2,
        'title': '销售趋势分析',
        'level': '初级',
        'level_color': 'success',
        'duration': '2.5小时',
        'dataset': 'sales_trend.csv',
        'background': '电商平台需要了解销售趋势，以便制定营销策略和库存管理计划。',
        'goal': '1. 将日期列转换为datetime格式\n2. 按周/月聚合销售数据\n3. 绘制销售趋势折线图\n4. 识别季节性模式',
        'tips': ['使用pd.to_datetime()转换日期格式', '设置日期为索引便于时间序列操作', 'resample()方法用于时间序列重采样', 'rolling()计算移动平均平滑数据'],
        'pitfalls': ['忘记设置日期为索引会导致resample失败', '日期格式不统一会导致转换失败', '直接绘制原始数据可能噪音太大', '忽略周末/节假日可能导致误判趋势'],
                'starter_code': 'import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv("data/sales_trend.csv")\n',
                'code': 'import pandas as pd\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv("data/sales_trend.csv")\ndf["日期"] = pd.to_datetime(df["日期"])\ndf = df.set_index("日期")\n\nprint("=== 销售趋势分析 ===")\nprint(f"数据时间范围: {df.index.min().strftime(\'%Y-%m-%d\')} 至 {df.index.max().strftime(\'%Y-%m-%d\')}")\nprint(f"总记录数: {len(df):,} 条")\nprint(f"总销售额: {df[\'销售额\'].sum():,.2f} 元")\nprint(f"日均销售额: {df[\'销售额\'].mean():,.2f} 元")\n\nweekly_sales = df["销售额"].resample("W").sum()\nmonthly_sales = df["销售额"].resample("ME").sum()\n\nprint(f"\\n=== 月销售额汇总 ===")\nfor idx, val in monthly_sales.items():\n    print(f"{idx.strftime(\'%Y-%m\')}: {val:,.2f} 元")\n\nma7 = df["销售额"].rolling(7).mean()\nprint(f"\\n=== 7日移动平均（最后10个日期）===")\nprint(ma7.tail(10).to_string())\n\nprint(f"\\n=== 各类别销售额占比 ===")\ncat_sales = df.groupby("类别")["销售额"].sum().sort_values(ascending=False)\nfor cat, val in cat_sales.items():\n    pct = val / cat_sales.sum() * 100\n    print(f"{cat}: {val:,.2f} 元 ({pct:.1f}%)")\n\nprint(f"\\n=== 各渠道销售额占比 ===")\nchannel_sales = df.groupby("渠道")["销售额"].sum().sort_values(ascending=False)\nfor ch, val in channel_sales.items():\n    pct = val / channel_sales.sum() * 100\n    print(f"{ch}: {val:,.2f} 元 ({pct:.1f}%)")'
    },
    {
        'id': 3,
        'title': '用户消费分层(RFM)',
        'level': '中级',
        'level_color': 'warning',
        'duration': '3小时',
        'dataset': 'rfm_data.csv',
        'background': '电商平台需要对用户进行分层管理，以便实施差异化的营销策略。',
        'goal': '1. 计算RFM三个维度得分\n2. 对每个维度进行分箱评分\n3. 综合RFM得分进行用户分群\n4. 分析各群组特征',
        'tips': ['R=最近一次消费距离当前的天数', 'F=指定时间内的消费频次', 'M=指定时间内的消费金额', '使用qcut进行分箱'],
        'pitfalls': ['计算R值时要确定参考日期', '分箱数量要根据业务需求确定', 'RFM权重需要根据业务调整', '新用户可能没有消费记录'],
                'starter_code': 'import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv("data/rfm_data.csv")\nprint("数据概览:")\nprint(df.head())\n',
                'code': 'import pandas as pd\nimport numpy as np\n\ndf = pd.read_csv("data/rfm_data.csv")\nprint("=== RFM用户消费分层分析 ===")\nprint(f"客户总数: {len(df)}")\nprint(f"\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\nrfm = df.copy()\nrfm.columns = ["客户ID", "R", "F", "M", "注册时长", "会员等级"]\n\nrfm["R_score"] = pd.qcut(rfm["R"], 5, labels=[5, 4, 3, 2, 1]).astype(int)\nrfm["F_score"] = pd.qcut(rfm["F"], 5, labels=[1, 2, 3, 4, 5]).astype(int)\nrfm["M_score"] = pd.qcut(rfm["M"], 5, labels=[1, 2, 3, 4, 5]).astype(int)\n\nrfm["RFM_total"] = rfm[["R_score", "F_score", "M_score"]].sum(axis=1)\n\ndef segment(row):\n    if row["R_score"] >= 4 and row["F_score"] >= 4 and row["M_score"] >= 4:\n        return "重要价值客户"\n    elif row["R_score"] >= 4 and row["F_score"] <= 2 and row["M_score"] <= 2:\n        return "新客户"\n    elif row["R_score"] <= 2 and row["F_score"] >= 4 and row["M_score"] >= 4:\n        return "重要挽留客户"\n    elif row["R_score"] <= 2 and row["F_score"] <= 2 and row["M_score"] <= 2:\n        return "流失客户"\n    elif row["M_score"] >= 4:\n        return "高消费客户"\n    else:\n        return "一般客户"\n\nrfm["客户分层"] = rfm.apply(segment, axis=1)\n\nprint(f"\\n=== 各分层客户数 ===")\nseg_counts = rfm["客户分层"].value_counts()\nfor seg, cnt in seg_counts.items():\n    pct = cnt / len(rfm) * 100\n    print(f"{seg}: {cnt} 人 ({pct:.1f}%)")\n\nprint(f"\\n=== 各分层平均消费金额 ===")\nprint(rfm.groupby("客户分层")["M"].mean().sort_values(ascending=False).round(0).to_string())\n\nprint(f"\\n=== RFM得分分布 ===")\nscore_bins = pd.cut(rfm["RFM_total"], bins=[3, 6, 9, 12, 15], labels=["低价值", "中低", "中高", "高价值"])\nprint(score_bins.value_counts().sort_index().to_string())'
    },
    {
        'id': 4,
        'title': '商品关联规则挖掘',
        'level': '中级',
        'level_color': 'warning',
        'duration': '3.5小时',
        'dataset': 'transactions.csv',
        'background': '电商平台希望通过关联规则挖掘发现商品之间的关联关系，用于商品推荐和货架摆放优化。',
        'goal': '1. 准备交易数据格式\n2. 使用Apriori算法挖掘关联规则\n3. 分析规则的支持度、置信度和提升度\n4. 筛选有价值的规则',
        'tips': ['交易数据需要转换为事务格式', '支持度表示规则出现的频率', '置信度表示规则的可靠性', '提升度 > 1表示正相关'],
        'pitfalls': ['支持度阈值设置太高会找不到规则', '支持度阈值设置太低会产生大量规则', '只看置信度可能忽略实际价值', '数据稀疏时结果不可靠'],
                'starter_code': 'import pandas as pd\n\ndf = pd.read_csv("data/transactions.csv")\nprint(df.head())\n',
                'code': 'import pandas as pd\nfrom mlxtend.frequent_patterns import apriori, association_rules\nimport warnings\nwarnings.filterwarnings("ignore")\n\ndf = pd.read_csv("data/transactions.csv")\nprint("=== 商品关联规则挖掘 ===")\nprint(f"订单数: {len(df)}")\nprint(f"\\n=== 数据样例 ===")\nprint(df.head(5).to_string())\n\nrecords = []\nfor _, row in df.iterrows():\n    items = [str(row[c]) for c in df.columns if c != "订单号" and pd.notna(row[c])]\n    records.append(items)\n\nfrom mlxtend.preprocessing import TransactionEncoder\nte = TransactionEncoder()\nte_ary = te.fit(records).transform(records)\nbasket = pd.DataFrame(te_ary, columns=te.columns_)\n\nprint(f"\\n唯一商品数: {len(te.columns_)}")\nprint(f"商品列表: {list(te.columns_)[:10]}...")\n\nfrequent_itemsets = apriori(basket, min_support=0.03, use_colnames=True)\nprint(f"\\n=== 频繁项集 (共{len(frequent_itemsets)}个) ===")\nprint(frequent_itemsets.sort_values("support", ascending=False).head(10).to_string())\n\nif len(frequent_itemsets) > 1:\n    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0)\n    print(f"\\n=== 关联规则 (共{len(rules)}条) ===")\n    if len(rules) > 0:\n        rules_sorted = rules.sort_values("lift", ascending=False)\n        for _, r in rules_sorted.head(10).iterrows():\n            print(f"{set(r[\'antecedents\'])} -> {set(r[\'consequents\'])}: "\n                  f"支持度={r[\'support\']:.3f}, 置信度={r[\'confidence\']:.3f}, 提升度={r[\'lift\']:.2f}")\n    else:\n        print("未找到有效关联规则（尝试降低min_threshold）")\nelse:\n    print("频繁项集不足，无法生成关联规则")'
    },
    {
        'id': 5,
        'title': '客户流失预测',
        'level': '高级',
        'level_color': 'danger',
        'duration': '4小时',
        'dataset': 'churn_data.csv',
        'background': '客户流失是企业面临的重要问题。通过构建流失预测模型，可以识别潜在流失客户并采取挽留措施。',
        'goal': '1. 数据预处理和特征工程\n2. 划分训练集和测试集\n3. 构建逻辑回归模型\n4. 评估模型性能\n5. 分析特征重要性',
        'tips': ['流失标签需要明确定义', '类别变量需要编码', '数据不平衡时考虑过采样/欠采样', '评价指标选择AUC-ROC和Recall'],
        'pitfalls': ['样本不平衡会导致模型偏向多数类', '特征过多可能导致过拟合', '时间顺序很重要', '相关特征可能导致多重共线性'],
                'starter_code': 'import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LogisticRegression\n\ndf = pd.read_csv("data/churn_data.csv")\nprint(df.head())\n',
                'code': 'import pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.metrics import classification_report, roc_auc_score\nimport warnings\nwarnings.filterwarnings("ignore")\n\ndf = pd.read_csv("data/churn_data.csv")\nprint("=== 客户流失预测分析 ===")\nprint(f"客户总数: {len(df)}")\nprint(f"流失率: {df[\'是否流失\'].mean():.2%}")\nprint(f"\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\nX = df.drop(["客户ID", "是否流失"], axis=1)\ny = df["是否流失"]\n\nscaler = StandardScaler()\nX_scaled = scaler.fit_transform(X)\n\nX_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, stratify=y, random_state=42)\n\nprint(f"\\n训练集大小: {len(X_train)}, 测试集大小: {len(X_test)}")\nprint(f"训练集流失率: {y_train.mean():.2%}, 测试集流失率: {y_test.mean():.2%}")\n\nmodel = LogisticRegression(class_weight="balanced", max_iter=1000)\nmodel.fit(X_train, y_train)\n\ny_pred = model.predict(X_test)\ny_prob = model.predict_proba(X_test)[:, 1]\n\nprint(f"\\n=== 模型评估 ===")\nprint(f"准确率: {(y_pred == y_test).mean():.2%}")\nprint(f"AUC-ROC: {roc_auc_score(y_test, y_prob):.4f}")\n\nprint(f"\\n=== 特征重要性（影响流失的关键因素）===")\nfeature_imp = pd.DataFrame({"特征": X.columns, "系数": model.coef_[0]})\nfeature_imp["影响程度"] = feature_imp["系数"].abs()\nfeature_imp = feature_imp.sort_values("影响程度", ascending=False)\nfor _, row in feature_imp.iterrows():\n    direction = "增加流失风险" if row["系数"] > 0 else "降低流失风险"\n    print(f"{row[\'特征\']:20s}: 系数={row[\'系数\']:+.4f} ({direction})")\n\nprint(f"\\n=== 分类报告 ===")\nprint(classification_report(y_test, y_pred))'
    },
    {
        'id': 6,
        'title': '销售数据仪表板',
        'level': '高级',
        'level_color': 'danger',
        'duration': '4小时',
        'dataset': 'dashboard_data.csv',
        'background': '企业需要实时监控销售数据。你将创建一个交互式仪表板，展示关键销售指标和趋势。',
        'goal': '1. 使用Plotly创建交互式图表\n2. 设计仪表板布局\n3. 添加筛选器和交互功能\n4. 部署仪表板',
        'tips': ['Plotly Express语法简洁', 'Dash框架适合构建完整仪表板', '考虑使用回调函数实现交互', '图表颜色要协调一致'],
        'pitfalls': ['图表太多会让仪表板混乱', '颜色选择不当会影响可读性', '数据刷新频率需要合理设置', '移动端适配需要考虑'],
                'starter_code': 'import pandas as pd\nimport plotly.express as px\n\ndf = pd.read_csv("data/dashboard_data.csv")\nprint(df.head())\n',
                'code': 'import pandas as pd\nimport plotly.express as px\nimport warnings\nwarnings.filterwarnings("ignore")\n\ndf = pd.read_csv("data/dashboard_data.csv")\nprint("=== 销售数据仪表板分析 ===")\nprint(f"数据记录数: {len(df)}")\nprint(f"\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\ntotal_sales = df["销售额"].sum()\ntotal_orders = df["订单数"].sum()\ntotal_profit = df["利润"].sum()\navg_growth = df["增长率"].mean()\n\nprint(f"\\n=== 核心指标 ===")\nprint(f"总销售额: {total_sales:,.2f} 元")\nprint(f"总订单数: {total_orders:,} 单")\nprint(f"总利润: {total_profit:,.2f} 元")\nprint(f"平均增长率: {avg_growth:.2%}")\n\nprint(f"\\n=== 各区域销售表现 ===")\nregion_stats = df.groupby("区域").agg({\n    "销售额": "sum",\n    "订单数": "sum",\n    "利润": "sum",\n    "增长率": "mean"\n}).round(2).sort_values("销售额", ascending=False)\nprint(region_stats.to_string())\n\nprint(f"\\n=== 各产品销售表现 ===")\nproduct_stats = df.groupby("产品").agg({\n    "销售额": "sum",\n    "订单数": "sum"\n}).round(2).sort_values("销售额", ascending=False)\nprint(product_stats.to_string())\n\nprint(f"\\n=== 月度销售趋势（前6月）===")\nmonthly = df.groupby("月份").agg({"销售额": "sum", "订单数": "sum"}).reset_index()\nprint(monthly.head(6).to_string())\n\nprint(f"\\n=== 区域x产品销售矩阵 ===")\npivot = df.pivot_table(values="销售额", index="产品", columns="区域", aggfunc="sum", fill_value=0)\nprint(pivot.round(0).to_string())\n\nprint(f"\\n仪表板可展示的关键洞察:")\nprint(f"  - 最佳销售区域: {region_stats.index[0]} ({region_stats.iloc[0][\'销售额\']:,.0f}元)")\nprint(f"  - 最畅销产品: {product_stats.index[0]} ({product_stats.iloc[0][\'销售额\']:,.0f}元)")\nprint(f"  - 高增长区域: {region_stats.sort_values(\'增长率\', ascending=False).index[0]}")'
    },
    {
        'id': 7,
        'title': '时间序列预测(ARIMA)',
        'level': '高级',
        'level_color': 'danger',
        'duration': '4.5小时',
        'dataset': 'timeseries_sales.csv',
        'background': '企业需要预测未来销售趋势，以便进行库存管理和资源规划。',
        'goal': '1. 数据预处理和可视化\n2. 识别时间序列特征\n3. 选择ARIMA模型参数\n4. 训练模型并预测\n5. 评估预测效果',
        'tips': ['时间序列需要是平稳的', 'ACF/PACF图用于确定p和q参数', '差分可以使序列平稳', 'AIC/BIC用于模型选择'],
        'pitfalls': ['非平稳序列会导致预测结果不可靠', '参数选择不当会影响预测精度', '过度拟合会导致泛化能力差', '长期预测误差会累积'],
                'starter_code': 'import pandas as pd\nfrom statsmodels.tsa.arima.model import ARIMA\n\ndf = pd.read_csv("data/timeseries_sales.csv")\nprint(df.head())\n',
                'code': 'import pandas as pd\nfrom statsmodels.tsa.arima.model import ARIMA\nfrom sklearn.metrics import mean_absolute_error, mean_squared_error\nimport warnings\nwarnings.filterwarnings("ignore")\n\ndf = pd.read_csv("data/timeseries_sales.csv")\ndf["日期"] = pd.to_datetime(df["日期"])\ndf = df.set_index("日期").asfreq("D")\n\nprint("=== 时间序列预测分析 ===")\nprint(f"数据时间范围: {df.index.min().strftime(\'%Y-%m-%d\')} 至 {df.index.max().strftime(\'%Y-%m-%d\')}")\nprint(f"数据记录数: {len(df)} 天")\nprint(f"\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\nprint(f"\\n=== 销售描述统计 ===")\nprint(df["历史销售额"].describe().round(2).to_string())\n\nholiday_sales = df[df["节日标记"] == 1]["历史销售额"].mean()\nnormal_sales = df[df["节日标记"] == 0]["历史销售额"].mean()\npromo_sales = df[df["促销标记"] == 1]["历史销售额"].mean()\nno_promo_sales = df[df["促销标记"] == 0]["历史销售额"].mean()\n\nprint(f"\\n=== 特殊因素影响 ===")\nprint(f"节日日均销售额: {holiday_sales:.2f} 元 (非节日: {normal_sales:.2f} 元)")\nprint(f"促销期间销售额: {promo_sales:.2f} 元 (无促销: {no_promo_sales:.2f} 元)")\n\ntrain = df.iloc[:-30]\ntest = df.iloc[-30:]\n\nprint(f"\\n=== 模型训练与预测 ===")\nprint(f"训练集: {len(train)} 天, 测试集: {len(test)} 天")\n\nmodel = ARIMA(train["历史销售额"], order=(2, 1, 1))\nmodel_fit = model.fit()\nprint(f"\\n模型摘要: AIC={model_fit.aic:.2f}, BIC={model_fit.bic:.2f}")\n\ntest_pred = model_fit.predict(start=test.index[0], end=test.index[-1])\nmae = mean_absolute_error(test["历史销售额"], test_pred)\nrmse = mean_squared_error(test["历史销售额"], test_pred) ** 0.5\n\nprint(f"\\n=== 预测误差 ===")\nprint(f"MAE (平均绝对误差): {mae:.2f} 元")\nprint(f"RMSE (均方根误差): {rmse:.2f} 元")\n\nforecast = model_fit.forecast(steps=30)\nprint(f"\\n=== 未来30天销售额预测 ===")\nfor i, (date, val) in enumerate(forecast.items()):\n    if i < 15:\n        print(f"{date.strftime(\'%Y-%m-%d\')}: {val:.2f} 元")\nprint(f"... (省略后15天)")\nprint(f"\\n预测期平均销售额: {forecast.mean():.2f} 元")\nprint(f"预测期总销售额: {forecast.sum():,.2f} 元")'
    },
    {
        'id': 8,
        'title': 'A/B测试分析',
        'level': '中级',
        'level_color': 'warning',
        'duration': '3小时',
        'dataset': 'ab_test_data.csv',
        'background': '产品团队进行了A/B测试，需要分析两种方案的效果差异是否显著。',
        'goal': '1. 数据探索和描述统计\n2. 进行假设检验\n3. 计算效果量\n4. 给出业务建议',
        'tips': ['明确原假设和备择假设', '选择合适的统计检验方法', '计算统计功效和样本量', '考虑多重比较问题'],
        'pitfalls': ['样本量不足会导致检验功效低', '忽略数据收集过程中的偏差', '过度解读统计显著性', '混淆统计显著和实际显著'],
                'starter_code': 'import pandas as pd\nfrom scipy import stats\n\ndf = pd.read_csv("data/ab_test_data.csv")\nprint(df.head())\n',
                'code': 'import pandas as pd\nfrom scipy import stats\nimport numpy as np\n\ndf = pd.read_csv("data/ab_test_data.csv")\nprint("=== A/B测试分析 ===")\nprint(f"总样本量: {len(df)}")\nprint(f"组别分布: {df[\'组别\'].value_counts().to_dict()}")\nprint(f"\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\ngroup_a = df[df["组别"] == "A"]\ngroup_b = df[df["组别"] == "B"]\n\nprint(f"\\n=== 组A (对照组) ===")\nprint(f"样本量: {len(group_a)}")\nprint(f"点击率: {group_a[\'是否点击\'].mean():.2%}")\nprint(f"转化率: {group_a[\'是否转化\'].mean():.2%}")\nprint(f"平均停留时长: {group_a[\'停留时长(秒)\'].mean():.1f} 秒")\nprint(f"平均页面浏览数: {group_a[\'页面浏览数\'].mean():.1f}")\n\nprint(f"\\n=== 组B (实验组) ===")\nprint(f"样本量: {len(group_b)}")\nprint(f"点击率: {group_b[\'是否点击\'].mean():.2%}")\nprint(f"转化率: {group_b[\'是否转化\'].mean():.2%}")\nprint(f"平均停留时长: {group_b[\'停留时长(秒)\'].mean():.1f} 秒")\nprint(f"平均页面浏览数: {group_b[\'页面浏览数\'].mean():.1f}")\n\nprint(f"\\n=== 转化率卡方检验 ===")\nobserved_conv = [\n    [group_a["是否转化"].sum(), len(group_a) - group_a["是否转化"].sum()],\n    [group_b["是否转化"].sum(), len(group_b) - group_b["是否转化"].sum()]\n]\nchi2, p_value, _, _ = stats.chi2_contingency(observed_conv)\nprint(f"卡方值: {chi2:.4f}")\nprint(f"p值: {p_value:.6f}")\nif p_value < 0.05:\n    print(f"结论: 差异显著 (p<0.05)，两组转化率存在统计学差异")\nelse:\n    print(f"结论: 差异不显著 (p>=0.05)，两组转化率无统计学差异")\n\nprint(f"\\n=== 点击率卡方检验 ===")\nobserved_click = [\n    [group_a["是否点击"].sum(), len(group_a) - group_a["是否点击"].sum()],\n    [group_b["是否点击"].sum(), len(group_b) - group_b["是否点击"].sum()]\n]\nchi2_click, p_click, _, _ = stats.chi2_contingency(observed_click)\nprint(f"卡方值: {chi2_click:.4f}")\nprint(f"p值: {p_click:.6f}")\nif p_click < 0.05:\n    print(f"结论: 差异显著 (p<0.05)")\nelse:\n    print(f"结论: 差异不显著 (p>=0.05)")\n\nprint(f"\\n=== 停留时长t检验 ===")\nt_stat, t_p = stats.ttest_ind(group_a["停留时长(秒)"], group_b["停留时长(秒)"])\nprint(f"t值: {t_stat:.4f}")\nprint(f"p值: {t_p:.6f}")\nif t_p < 0.05:\n    print(f"结论: 差异显著 (p<0.05)")\nelse:\n    print(f"结论: 差异不显著 (p>=0.05)")\n\nprint(f"\\n=== 业务建议 ===")\nb_conv = group_b["是否转化"].mean()\na_conv = group_a["是否转化"].mean()\nimprovement = (b_conv - a_conv) / a_conv * 100\nprint(f"实验组比对照组转化率 {\'提升\' if improvement > 0 else \'下降\'} {abs(improvement):.2f}%")\nif p_value < 0.05 and b_conv > a_conv:\n    print("建议: 实验组效果显著更优，可以全面推广方案B")\nelif p_value < 0.05 and a_conv > b_conv:\n    print("建议: 对照组效果显著更优，应保持方案A")\nelse:\n    print("建议: 效果差异不显著，建议增加样本量或调整实验方案")'
    },
    {
        'id': 9,
        'title': '文本情感分析',
        'level': '高级',
        'level_color': 'danger',
        'duration': '4小时',
        'dataset': 'reviews.csv',
        'background': '电商平台积累了大量用户评论，需要通过情感分析了解用户反馈。',
        'goal': '1. 文本数据预处理\n2. 使用情感词典或模型进行情感分析\n3. 可视化分析结果\n4. 生成词云',
        'tips': ['使用jieba进行中文分词', '可以使用SnowNLP进行情感分析', '停用词过滤可以提高分析质量', '词云可以直观展示高频词汇'],
        'pitfalls': ['中文分词质量影响分析结果', '情感词典可能覆盖不全', '否定词处理需要特别注意', '上下文语境很重要'],
                'starter_code': 'import pandas as pd\n\ndf = pd.read_csv("data/reviews.csv")\nprint(df.head())\nprint(f"评论总数: {len(df)}")\n',
                'code': 'import pandas as pd\ntry:\n    from snownlp import SnowNLP\n    HAS_SNOWNLP = True\nexcept ImportError:\n    HAS_SNOWNLP = False\n\ndf = pd.read_csv("data/reviews.csv")\nprint("=== 文本情感分析 ===")\nprint(f"评论总数: {len(df)}")\nprint(f"\\n=== 数据概览 ===")\nprint(df[["评论ID", "商品", "评分"]].head(8).to_string())\n\nprint(f"\\n=== 评分分布 ===")\nrating_dist = df["评分"].value_counts().sort_index()\nfor rating, cnt in rating_dist.items():\n    pct = cnt / len(df) * 100\n    bars = "█" * int(pct)\n    print(f"{rating}星: {cnt:4d} ({pct:5.1f}%) {bars}")\n\navg_rating = df["评分"].mean()\nprint(f"\\n平均评分: {avg_rating:.2f} 星")\n\nprint(f"\\n=== 各商品评论数及平均评分 ===")\nproduct_stats = df.groupby("商品").agg(\n    评论数=("评分", "count"),\n    平均评分=("评分", "mean")\n).sort_values("评论数", ascending=False).round(2)\nprint(product_stats.to_string())\n\ncorr = df["评分"].corr(df["点赞数"])\nprint(f"\\n=== 评分与点赞数的相关系数: {corr:.4f}")\n\nif HAS_SNOWNLP:\n    print(f"\\n=== 情感分析 ===")\n    try:\n        df["情感得分"] = df["评论文本"].apply(lambda x: SnowNLP(str(x)).sentiments)\n        print(f"平均情感得分: {df[\'情感得分\'].mean():.4f}")\n        print(f"正面评论(得分>0.5): {(df[\'情感得分\'] > 0.5).sum()} ({(df[\'情感得分\'] > 0.5).mean():.1%})")\n        print(f"负面评论(得分<0.5): {(df[\'情感得分\'] < 0.5).sum()} ({(df[\'情感得分\'] < 0.5).mean():.1%})")\n        \n        print(f"\\n=== 高情感得分评论 (样本) ===")\n        for _, row in df.nlargest(5, "情感得分").iterrows():\n            print(f"  [{row[\'情感得分\']:.3f}] {str(row[\'评论文本\'])[:50]}")\n        \n        print(f"\\n=== 低情感得分评论 (样本) ===")\n        for _, row in df.nsmallest(5, "情感得分").iterrows():\n            print(f"  [{row[\'情感得分\']:.3f}] {str(row[\'评论文本\'])[:50]}")\n    except Exception as e:\n        print(f"情感分析处理失败: {e}")\nelse:\n    print(f"\\n(提示: 安装 snownlp 可进行更详细的中文情感分析)")\n\nprint(f"\\n=== 高频词汇统计 ===")\nfrom collections import Counter\nimport re\n\nall_text = " ".join(df["评论文本"].astype(str))\nwords = re.findall(r"[\\u4e00-\\u9fa5]{2,4}", all_text)\nword_counts = Counter(words)\n\nprint("Top 15 高频词:")\nfor word, cnt in word_counts.most_common(15):\n    print(f"  {word}: {cnt}次")'
    },
    {
        'id': 10,
        'title': 'KMeans聚类分析',
        'level': '高级',
        'level_color': 'danger',
        'duration': '4小时',
        'dataset': 'customer_clusters.csv',
        'background': '企业需要对客户进行分群，以便实施个性化营销策略。',
        'goal': '1. 数据预处理和标准化\n2. 使用肘部法则确定聚类数量\n3. 应用KMeans算法\n4. 分析各簇特征',
        'tips': ['KMeans对初始质心敏感', '特征需要标准化', '肘部法则是确定K值的常用方法', '轮廓系数可以评估聚类质量'],
        'pitfalls': ['K值选择主观', '异常值会严重影响聚类结果', '假设数据是凸形分布', '不适合处理高维数据'],
                'starter_code': 'import pandas as pd\nfrom sklearn.cluster import KMeans\nfrom sklearn.preprocessing import StandardScaler\n\ndf = pd.read_csv("data/customer_clusters.csv")\nprint(df.head())\n',
                'code': 'import pandas as pd\nfrom sklearn.cluster import KMeans\nfrom sklearn.preprocessing import StandardScaler\nfrom sklearn.metrics import silhouette_score\nimport matplotlib.pyplot as plt\nimport warnings\nwarnings.filterwarnings("ignore")\n\ndf = pd.read_csv("data/customer_clusters.csv")\nprint("=== KMeans客户聚类分析 ===")\nprint(f"客户总数: {len(df)}")\nprint(f"\\n=== 数据概览 ===")\nprint(df.head(8).to_string())\n\nfeatures = df[["年收入(万)", "消费评分(1-100)", "年龄"]]\nfeature_names = features.columns.tolist()\n\nprint(f"\\n=== 特征描述统计 ===")\nprint(features.describe().round(2).to_string())\n\nscaler = StandardScaler()\nscaled_features = scaler.fit_transform(features)\n\nprint(f"\\n=== 肘部法则 - 不同K值的inertia ===")\ninertia = []\nfor k in range(2, 10):\n    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)\n    kmeans.fit(scaled_features)\n    inertia.append(kmeans.inertia_)\n    print(f"K={k}: inertia={kmeans.inertia_:.2f}")\n\nprint(f"\\n=== K=4 聚类结果 ===")\nkmeans = KMeans(n_clusters=4, random_state=42, n_init=10)\ndf["cluster"] = kmeans.fit_predict(scaled_features)\ndf["cluster"] = df["cluster"] + 1  # 从1开始编号\n\nprint(f"\\n=== 各簇客户数 ===")\ncluster_counts = df["cluster"].value_counts().sort_index()\nfor cl, cnt in cluster_counts.items():\n    pct = cnt / len(df) * 100\n    print(f"簇{cl}: {cnt} 人 ({pct:.1f}%)")\n\nprint(f"\\n=== 各簇特征均值 ===")\ncluster_stats = df.groupby("cluster")[feature_names].mean().round(2)\nprint(cluster_stats.to_string())\n\nsil_score = silhouette_score(scaled_features, df["cluster"] - 1)\nprint(f"\\n=== 聚类质量评估 ===")\nprint(f"轮廓系数: {sil_score:.4f} (范围: -1到1，越接近1越好)")\n\nprint(f"\\n=== 各簇特征洞察 ===")\nfor cl in sorted(df["cluster"].unique()):\n    cluster_data = df[df["cluster"] == cl]\n    income_level = "高收入" if cluster_data["年收入(万)"].mean() > df["年收入(万)"].mean() else "低收入"\n    spending_level = "高消费意愿" if cluster_data["消费评分(1-100)"].mean() > df["消费评分(1-100)"].mean() else "低消费意愿"\n    age_level = "年长" if cluster_data["年龄"].mean() > df["年龄"].mean() else "年轻"\n    print(f"簇{cl} ({len(cluster_data)}人): {income_level}, {spending_level}, {age_level}群")\n\nif "性别" in df.columns:\n    print(f"\\n=== 各簇性别分布 ===")\n    gender_dist = df.groupby(["cluster", "性别"]).size().unstack(fill_value=0)\n    print(gender_dist.to_string())\n\nprint(f"\\n=== 业务建议 ===")\nprint("可根据各簇特征制定差异化营销策略:")\nprint("  - 高收入+高消费意愿: VIP客户，推送高端产品")\nprint("  - 高收入+低消费意愿: 需唤醒客户，推送促销活动")\nprint("  - 低收入+高消费意愿: 价格敏感客户，推送性价比产品")\nprint("  - 低收入+低消费意愿: 需培育客户，推送入门产品")'
    }
]

ASSESSMENT_QUESTIONS = [
    {"q": "Pandas中创建DataFrame的正确方式是？", "options": ["pd.DataFrame(data)", "pd.create(data)", "DataFrame(data)", "pd.make_dataframe(data)"], "answer": 0},
    {"q": "SQL中用于连接两个表的关键字是？", "options": ["JOIN", "CONNECT", "LINK", "COMBINE"], "answer": 0},
    {"q": "NumPy数组的形状由哪个属性获取？", "options": ["arr.shape", "arr.size", "arr.dim", "arr.ndim"], "answer": 0},
    {"q": "Matplotlib中绘制折线图使用哪个函数？", "options": ["plt.plot()", "plt.line()", "plt.draw()", "plt.create_line()"], "answer": 0},
    {"q": "p值小于0.05表示？", "options": ["拒绝原假设", "接受原假设", "数据无效", "样本量不足"], "answer": 0},
    {"q": "GROUP BY子句的作用是？", "options": ["分组聚合", "排序", "过滤", "连接"], "answer": 0},
    {"q": "df.dropna()的作用是？", "options": ["删除含缺失值的行", "填充缺失值", "替换NaN", "查找缺失值"], "answer": 0},
    {"q": "Seaborn中绘制热力图使用？", "options": ["sns.heatmap()", "sns.map()", "sns.plot_heat()", "sns.heat()"], "answer": 0},
    {"q": "相关系数r的取值范围是？", "options": ["[-1, 1]", "[0, 1]", "[-∞, +∞]", "[0, 100]"], "answer": 0},
    {"q": "LEFT JOIN会保留哪个表的所有行？", "options": ["左表", "右表", "两表都保留", "只保留匹配行"], "answer": 0},
    {"q": "Python中安装第三方库使用？", "options": ["pip install", "npm install", "apt install", "install"], "answer": 0},
    {"q": "ARIMA模型中d参数表示？", "options": ["差分阶数", "自回归阶数", "移动平均阶数", "滞后阶数"], "answer": 0},
    {"q": "df.groupby()后的常用聚合函数是？", "options": ["sum()", "group_sum()", "aggregate()", "calc()"], "answer": 0},
    {"q": "IQR方法用于检测什么？", "options": ["异常值", "缺失值", "重复值", "错误值"], "answer": 0},
    {"q": "A/B测试中常用的统计检验是？", "options": ["卡方检验", "t检验", "方差分析", "以上都是"], "answer": 3},
    {"q": "KMeans聚类的目标是最小化什么？", "options": ["惯性值", "距离和", "方差", "误差"], "answer": 0},
    {"q": "SQL中的HAVING子句用于？", "options": ["过滤聚合结果", "过滤行", "排序", "分组"], "answer": 0},
    {"q": "Pandas中设置日期为索引使用？", "options": ["df.set_index()", "df.index()", "df.make_index()", "df.set_date()"], "answer": 0},
    {"q": "RFM模型中的F代表？", "options": ["消费频次", "消费金额", "最近消费", "消费间隔"], "answer": 0},
    {"q": "机器学习中的过拟合意味着？", "options": ["模型在训练集表现好，测试集差", "模型太简单", "数据太少", "特征太多"], "answer": 0}
]

BADGES = {
    "first_login": {"name": "初来乍到", "desc": "首次登录平台", "icon": "🌱"},
    "first_project": {"name": "代码新秀", "desc": "完成第一个项目", "icon": "💻"},
    "five_projects": {"name": "数据分析师", "desc": "完成5个项目", "icon": "📊"},
    "ten_projects": {"name": "数据科学大师", "desc": "完成全部10个项目", "icon": "🏆"},
    "perfect_score": {"name": "完美学霸", "desc": "测评满分", "icon": "👑"},
    "seven_days": {"name": "坚持不懈", "desc": "连续学习7天", "icon": "🔥"}
}

@app.route('/')
def index():
    user_id = session.get('user_id')
    completed_chapters = []
    completed_projects = []
    if user_id:
        completed_chapters = [cp.chapter_id for cp in ChapterProgress.query.filter_by(user_id=user_id).all()]
        completed_projects = [pp.project_id for pp in ProjectProgress.query.filter_by(user_id=user_id).all()]
    return render_template('index.html', courses=COURSES, projects=PROJECTS[:3], 
                           completed_chapters=completed_chapters, completed_projects=completed_projects)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and user.check_password(request.form['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            user.last_login = datetime.now()
            db.session.commit()
            check_badge('first_login')
            return redirect(url_for('index'))
        flash('邮箱或密码错误')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash('邮箱已被注册')
            return redirect(url_for('register'))
        if User.query.filter_by(username=request.form['username']).first():
            flash('用户名已被使用')
            return redirect(url_for('register'))
        user = User(username=request.form['username'], email=request.form['email'])
        user.set_password(request.form['password'])
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['username'] = user.username
        check_badge('first_login')
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    if not course:
        return '课程不存在', 404
    user_id = session.get('user_id')
    completed_chapters = []
    if user_id:
        completed_chapters = [cp.chapter_id for cp in ChapterProgress.query.filter_by(user_id=user_id, course_id=course_id).all()]
    completed_count = len(completed_chapters)
    total_count = len(course['chapters'])
    percent = round(completed_count / total_count * 100) if total_count > 0 else 0
    return render_template('course_detail.html', course=course, 
                           completed_chapters=completed_chapters,
                           completed_count=completed_count,
                           total_count=total_count,
                           percent=percent)

@app.route('/course/<int:course_id>/chapter/<int:chapter_id>')
def chapter_page(course_id, chapter_id):
    course = next((c for c in COURSES if c['id'] == course_id), None)
    chapter = CHAPTERS.get(chapter_id)
    if not course or not chapter or chapter['course_id'] != course_id:
        return '章节不存在', 404
    user_id = session.get('user_id')
    is_complete = False
    if user_id:
        is_complete = ChapterProgress.query.filter_by(user_id=user_id, course_id=course_id, chapter_id=chapter_id).first() is not None
    return render_template('chapter_page.html', course=course, chapter=chapter, is_complete=is_complete)

@app.route('/projects')
def projects_list():
    user_id = session.get('user_id')
    completed_projects = []
    if user_id:
        completed_projects = [pp.project_id for pp in ProjectProgress.query.filter_by(user_id=user_id).all()]
    return render_template('projects_list.html', projects=PROJECTS, completed_projects=completed_projects)

@app.route('/project/<int:project_id>')
def project_page(project_id):
    project = next((p for p in PROJECTS if p['id'] == project_id), None)
    if not project:
        return '项目不存在', 404
    user_id = session.get('user_id')
    is_complete = False
    if user_id:
        is_complete = ProjectProgress.query.filter_by(user_id=user_id, project_id=project_id).first() is not None
    dataset_exists = os.path.exists(f"data/{project['dataset']}")
    return render_template('project.html', project=project, is_complete=is_complete, dataset_exists=dataset_exists)

@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    user = User.query.get(user_id)
    completed_chapters = ChapterProgress.query.filter_by(user_id=user_id).all()
    completed_projects = ProjectProgress.query.filter_by(user_id=user_id).all()
    badges = Badge.query.filter_by(user_id=user_id).all()
    badge_keys = [b.badge_key for b in badges]
    
    course_progress = []
    for course in COURSES:
        completed = len([cp for cp in completed_chapters if cp.course_id == course['id']])
        total = len(course['chapters'])
        course_progress.append({
            'title': course['title'],
            'completed': completed,
            'total': total,
            'percent': round(completed / total * 100) if total > 0 else 0
        })
    
    earned_badges = {key: BADGES[key] for key in badge_keys if key in BADGES}
    unlocked_badges = {key: BADGES[key] for key in BADGES if key not in badge_keys}
    
    return render_template('dashboard.html', user=user, 
                           completed_chapters_count=len(completed_chapters),
                           completed_projects_count=len(completed_projects),
                           course_progress=course_progress,
                           earned_badges=earned_badges,
                           unlocked_badges=unlocked_badges)

@app.route('/assessment')
def assessment():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('assessment.html', questions=ASSESSMENT_QUESTIONS)

@app.route('/assessment/submit', methods=['POST'])
def submit_assessment():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': '请先登录'}), 401
    
    data = request.get_json()
    answers = data.get('answers', {})
    score = 0
    for i, q in enumerate(ASSESSMENT_QUESTIONS):
        if str(i) in answers and int(answers[str(i)]) == q['answer']:
            score += 5
    
    result = AssessmentResult(user_id=user_id, score=score)
    db.session.add(result)
    db.session.commit()
    
    if score == 100:
        check_badge('perfect_score')
    
    return jsonify({'score': score, 'total': 20, 'pass': score >= 60})

@app.route('/assessment/result/<int:score>')
def assessment_result(score):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    return render_template('assessment_result.html', score=score)

@app.route('/api/run_code', methods=['POST'])
def api_run_code():
    data = request.get_json()
    code = data.get('code', '')

    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        import matplotlib
        matplotlib.use('Agg')
        exec_globals = {
            '__builtins__': __builtins__,
            '__name__': '__main__',
        }
        pre_imports = '''
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import plotly
import scipy
from datetime import datetime, timedelta
from collections import defaultdict, OrderedDict
import json
import os
import sys
import re
'''
        exec(pre_imports, exec_globals)
        import warnings
        warnings.filterwarnings('ignore')
        code = code.replace('freq="M"', 'freq="ME"').replace("freq='M'", "freq='ME'")
        code = code.replace('resample("M")', 'resample("ME")').replace("resample('M')", "resample('ME')")
        code = code.replace('resample("Y")', 'resample("YE")').replace("resample('Y')", "resample('YE')")
        code = code.replace('freq="Y"', 'freq="YE"').replace("freq='Y'", "freq='YE'")
        code = code.replace('freq="Q"', 'freq="QE"').replace("freq='Q'", "freq='QE'")
        code = code.replace('resample("Q")', 'resample("QE")').replace("resample('Q')", "resample('QE')")
        code = code.replace('resample("A")', 'resample("YE")').replace("resample('A')", "resample('YE')")
        exec(code, exec_globals)
        output = sys.stdout.getvalue()
        status = 'success'
    except Exception as e:
        output = sys.stdout.getvalue() + '\n[错误] ' + str(e)
        status = 'error'
    finally:
        sys.stdout = old_stdout

    return jsonify({'output': output, 'status': status})

@app.route('/api/chapter/complete', methods=['POST'])
def api_complete_chapter():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'ok': False, 'error': '请先登录'})
    
    data = request.get_json()
    course_id = data.get('course_id')
    chapter_id = data.get('chapter_id')
    
    progress = ChapterProgress.query.filter_by(user_id=user_id, course_id=course_id, chapter_id=chapter_id).first()
    if not progress:
        progress = ChapterProgress(user_id=user_id, course_id=course_id, chapter_id=chapter_id, completed_at=datetime.now())
        db.session.add(progress)
        db.session.commit()
    
    return jsonify({'ok': True})

@app.route('/api/project/complete', methods=['POST'])
def api_complete_project():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'ok': False, 'error': '请先登录'})
    
    data = request.get_json()
    project_id = data.get('project_id')
    
    progress = ProjectProgress.query.filter_by(user_id=user_id, project_id=project_id).first()
    if not progress:
        progress = ProjectProgress(user_id=user_id, project_id=project_id, completed_at=datetime.now())
        db.session.add(progress)
        db.session.commit()
    
    new_badges = []
    completed_count = ProjectProgress.query.filter_by(user_id=user_id).count()
    
    if completed_count == 1:
        if check_badge('first_project'):
            new_badges.append('first_project')
    elif completed_count == 5:
        if check_badge('five_projects'):
            new_badges.append('five_projects')
    elif completed_count == 10:
        if check_badge('ten_projects'):
            new_badges.append('ten_projects')
    
    return jsonify({'ok': True, 'new_badges': new_badges})

@app.route('/download_dataset/<filename>')
def download_dataset(filename):
    return send_from_directory('data', filename)

def check_badge(badge_key):
    user_id = session.get('user_id')
    if not user_id:
        return False
    if Badge.query.filter_by(user_id=user_id, badge_key=badge_key).first():
        return False
    badge = Badge(user_id=user_id, badge_key=badge_key)
    db.session.add(badge)
    db.session.commit()
    return True

if __name__ == '__main__':
    app.run(debug=True)
