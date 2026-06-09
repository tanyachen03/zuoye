export const COURSES = {
  1: {
    id: 1,
    title: 'Python编程基础',
    description: '从零开始学习Python，掌握编程入门必备技能',
    icon: '💻',
    chapters: [1, 2, 3],
    duration: '8小时',
    level: '入门'
  },
  2: {
    id: 2,
    title: 'NumPy数据分析',
    description: '掌握Python科学计算核心库，处理海量数值数据',
    icon: '📊',
    chapters: [4, 5, 6],
    duration: '10小时',
    level: '初级'
  },
  3: {
    id: 3,
    title: 'Pandas数据处理',
    description: '精通数据清洗、转换和分析的利器',
    icon: '📈',
    chapters: [7, 8, 9],
    duration: '12小时',
    level: '初级'
  },
  4: {
    id: 4,
    title: '数据可视化',
    description: '用Matplotlib和Seaborn创建专业图表',
    icon: '🎨',
    chapters: [10, 11, 12],
    duration: '8小时',
    level: '初级'
  },
  5: {
    id: 5,
    title: '统计分析基础',
    description: '掌握描述性统计和推论统计方法',
    icon: '📐',
    chapters: [13, 14, 15],
    duration: '10小时',
    level: '中级'
  },
  6: {
    id: 6,
    title: '机器学习入门',
    description: '学习监督学习和无监督学习算法',
    icon: '🤖',
    chapters: [16, 17, 18],
    duration: '15小时',
    level: '中级'
  },
  7: {
    id: 7,
    title: '商业数据分析',
    description: '将数据分析技能应用于商业决策',
    icon: '💼',
    chapters: [19, 20, 21],
    duration: '12小时',
    level: '中级'
  },
  8: {
    id: 8,
    title: '实战项目演练',
    description: '综合运用所学知识完成真实商业项目',
    icon: '🚀',
    chapters: [22, 23, 24],
    duration: '20小时',
    level: '高级'
  }
};

export const CHAPTERS = {
  1: {
    id: 1,
    course_id: 1,
    title: 'Python环境搭建',
    theory: `<h3>Python简介</h3><p>Python是一种高级通用编程语言，以其简洁的语法和强大的功能著称。它广泛应用于数据分析、人工智能、Web开发等领域。</p><h3>安装Python</h3><p>可以从<a href="https://www.python.org/downloads/" target="_blank">Python官网</a>下载最新版本，或使用Anaconda发行版。</p><div class="key-point"><strong>关键点：</strong>建议安装Python 3.8及以上版本，Python 2已停止维护。</div><h3>开发环境选择</h3><ul><li>PyCharm - 专业Python IDE</li><li>VS Code - 轻量级代码编辑器</li><li>Jupyter Notebook - 交互式数据分析</li></ul><div class="tip-box"><strong>小贴士：</strong>安装完成后可以在终端输入 <code>python --version</code> 验证安装是否成功。</div>`,
    code_example: 'print("Hello, World!")',
    starter_code: '# 在此编写你的代码\n',
    exercises: [
      { question: 'Python的官方网站地址是什么？', answer: 'https://www.python.org' },
      { question: 'pip install 命令的作用是什么？', answer: '安装Python包' },
      { question: 'Anaconda主要面向哪些用户群体？', answer: '数据科学和机器学习从业者' }
    ]
  },
  2: {
    id: 2,
    course_id: 1,
    title: '基础语法与数据类型',
    theory: `<h3>变量与数据类型</h3><p>Python中的变量不需要声明类型，直接赋值即可。主要数据类型包括：</p><ul><li><strong>int</strong> - 整数</li><li><strong>float</strong> - 浮点数</li><li><strong>str</strong> - 字符串</li><li><strong>bool</strong> - 布尔值</li></ul><h3>字符串操作</h3><p>Python提供丰富的字符串处理方法：</p><pre><code>s = "Hello, Python"
print(s.upper())      # 转大写
print(s.lower())      # 转小写
print(s.replace("Python", "World"))  # 替换</code></pre><div class="warn-box"><strong>注意：</strong>字符串是不可变类型，所有字符串方法都返回新字符串。</div><h3>基本运算符</h3><table><tr><th>运算符</th><th>说明</th></tr><tr><td>+</td><td>加法/字符串拼接</td></tr><tr><td>-</td><td>减法</td></tr><tr><td>*</td><td>乘法/字符串重复</td></tr><tr><td>/</td><td>除法</td></tr></table>`,
    code_example: 'name = "Alice"\nage = 25\nprint(f"My name is {name}, I am {age} years old.")',
    starter_code: '# 练习：创建变量并输出\n',
    exercises: [
      { question: 'Python中如何定义一个字符串变量？', answer: '使用单引号或双引号' },
      { question: 'print()函数的作用是什么？', answer: '输出内容到控制台' },
      { question: 'f-string是什么？', answer: '格式化字符串的一种方式' }
    ]
  },
  3: {
    id: 3,
    course_id: 1,
    title: '控制流程与函数',
    theory: `<h3>条件判断</h3><p>使用if-elif-else语句进行条件判断：</p><pre><code>score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"</code></pre><h3>循环结构</h3><ul><li><strong>for循环</strong>：遍历可迭代对象</li><li><strong>while循环</strong>：条件满足时重复执行</li></ul><h3>函数定义</h3><p>使用def关键字定义函数：</p><pre><code>def greet(name):
    """打招呼函数"""
    return f"Hello, {name}!"

result = greet("Bob")
print(result)</code></pre><div class="key-point"><strong>关键点：</strong>函数应该遵循单一职责原则，一个函数只做一件事。</div>`,
    code_example: 'def calculate_area(radius):\n    return 3.14159 * radius ** 2',
    starter_code: '# 练习：定义一个计算矩形面积的函数\n',
    exercises: [
      { question: 'for循环和while循环的区别是什么？', answer: 'for遍历序列，while根据条件重复' },
      { question: 'def关键字的作用是什么？', answer: '定义函数' },
      { question: '函数的return语句有什么作用？', answer: '返回函数执行结果' }
    ]
  },
  4: {
    id: 4,
    course_id: 2,
    title: 'NumPy数组基础',
    theory: `<h3>什么是NumPy</h3><p>NumPy是Python科学计算的核心库，提供高性能的多维数组对象和数学函数。</p><div class="key-point"><strong>关键点：</strong>NumPy数组比Python列表快数十倍，是数据分析的基础。</div><h3>创建数组</h3><pre><code>import numpy as np

# 创建一维数组
arr1 = np.array([1, 2, 3, 4, 5])

# 创建二维数组
arr2 = np.array([[1, 2, 3], [4, 5, 6]])

# 创建特殊数组
zeros = np.zeros((3, 4))  # 全零数组
ones = np.ones((2, 3))    # 全一数组
identity = np.eye(3)      # 单位矩阵</code></pre><h3>数组属性</h3><ul><li><code>shape</code> - 数组形状</li><li><code>dtype</code> - 数据类型</li><li><code>size</code> - 元素总数</li><li><code>ndim</code> - 维度数</li></ul>`,
    code_example: 'import numpy as np\narr = np.arange(12)\nprint(arr.reshape(3, 4))',
    starter_code: '# 练习：创建NumPy数组\nimport numpy as np\n',
    exercises: [
      { question: 'np.zeros()函数的作用是什么？', answer: '创建全零数组' },
      { question: '数组的shape属性表示什么？', answer: '数组的维度信息' },
      { question: 'np.arange(12)会生成多少个元素？', answer: '12个' }
    ]
  },
  5: {
    id: 5,
    course_id: 2,
    title: '数组操作与运算',
    theory: `<h3>数组索引与切片</h3><pre><code>import numpy as np

arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# 获取单个元素
print(arr[0, 1])   # 第一行第二列

# 切片操作
print(arr[:, 1])   # 所有行的第二列
print(arr[1:3, :]) # 第二到第三行</code></pre><h3>向量化运算</h3><p>NumPy支持向量化运算，无需显式循环：</p><pre><code>a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)  # [5 7 9]
print(a * b)  # [4 10 18]
print(a ** 2) # [1 4 9]</code></pre><div class="tip-box"><strong>小贴士：</strong>向量化运算比Python循环快得多，应尽量使用。</div>`,
    code_example: 'a = np.array([1, 2, 3])\nb = np.array([4, 5, 6])\nprint(a @ b)  # 点积',
    starter_code: '# 练习：数组运算\nimport numpy as np\n',
    exercises: [
      { question: 'arr[:, 1]表示什么含义？', answer: '所有行的第二列元素' },
      { question: 'NumPy的向量化运算有什么优势？', answer: '速度快，代码简洁' },
      { question: 'a @ b 表示什么运算？', answer: '矩阵乘法或点积' }
    ]
  },
  6: {
    id: 6,
    course_id: 2,
    title: '常用NumPy函数',
    theory: `<h3>数学函数</h3><pre><code>import numpy as np

arr = np.array([1, 2, 3, 4, 5])

print(np.sum(arr))      # 求和
print(np.mean(arr))     # 平均值
print(np.max(arr))      # 最大值
print(np.min(arr))      # 最小值
print(np.std(arr))      # 标准差</code></pre><h3>矩阵操作</h3><pre><code>matrix = np.array([[1, 2], [3, 4]])

# 转置
print(matrix.T)

# 矩阵乘法
a = np.array([[1, 0], [0, 1]])
b = np.array([[4, 1], [2, 2]])
print(a @ b)</code></pre><div class="warn-box"><strong>注意：</strong>矩阵乘法需要满足维度兼容条件。</div><h3>布尔索引</h3><pre><code>arr = np.array([10, 20, 30, 40, 50])
mask = arr > 25
print(arr[mask])  # [30 40 50]</code></pre>`,
    code_example: 'arr = np.random.randn(100)\nprint(f"均值: {np.mean(arr):.2f}")\nprint(f"标准差: {np.std(arr):.2f}")',
    starter_code: '# 练习：使用NumPy函数\nimport numpy as np\n',
    exercises: [
      { question: 'np.mean()和np.sum()的区别是什么？', answer: 'mean计算平均值，sum计算总和' },
      { question: '矩阵的T属性表示什么？', answer: '矩阵的转置' },
      { question: '布尔索引的作用是什么？', answer: '根据条件筛选元素' }
    ]
  },
  7: {
    id: 7,
    course_id: 3,
    title: 'Pandas数据结构',
    theory: `<h3>Series与DataFrame</h3><p>Pandas主要有两种数据结构：</p><ul><li><strong>Series</strong>：一维带标签数组</li><li><strong>DataFrame</strong>：二维表格数据结构</li></ul><pre><code>import pandas as pd

# 创建Series
s = pd.Series([1, 3, 5, np.nan, 6, 8])

# 创建DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['Beijing', 'Shanghai', 'Guangzhou']
})</code></pre><h3>查看数据</h3><pre><code># 查看前几行
print(df.head())

# 查看基本信息
print(df.info())

# 统计摘要
print(df.describe())</code></pre><div class="key-point"><strong>关键点：</strong>DataFrame是Pandas中最重要的数据结构，类似Excel表格。</div>`,
    code_example: 'import pandas as pd\ndf = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})\nprint(df)',
    starter_code: '# 练习：创建DataFrame\nimport pandas as pd\n',
    exercises: [
      { question: 'Series和DataFrame的区别是什么？', answer: 'Series是一维，DataFrame是二维' },
      { question: 'df.head()的作用是什么？', answer: '查看数据前几行' },
      { question: 'df.info()会显示什么信息？', answer: '数据类型、非空值数量等' }
    ]
  },
  8: {
    id: 8,
    course_id: 3,
    title: '数据读取与清洗',
    theory: `<h3>读取外部数据</h3><pre><code># 读取CSV文件
df = pd.read_csv('data.csv')

# 读取Excel文件
df = pd.read_excel('data.xlsx')

# 读取JSON文件  
df = pd.read_json('data.json')</code></pre><h3>数据清洗</h3><pre><code># 检查缺失值
print(df.isnull().sum())

# 处理缺失值
df.fillna(0, inplace=True)  # 填充0
df.dropna(inplace=True)     # 删除含缺失值的行

# 重复值处理
df.drop_duplicates(inplace=True)</code></pre><div class="tip-box"><strong>小贴士：</strong>数据清洗通常占数据分析工作的80%以上时间。</div><h3>数据类型转换</h3><pre><code># 转换为数值类型
df['price'] = pd.to_numeric(df['price'], errors='coerce')

# 转换为日期类型
df['date'] = pd.to_datetime(df['date'])</code></pre>`,
    code_example: 'df = pd.read_csv("data/sales.csv")\nprint(df.dropna().head())',
    starter_code: '# 练习：读取并清洗数据\nimport pandas as pd\n',
    exercises: [
      { question: 'read_csv()函数的作用是什么？', answer: '读取CSV文件' },
      { question: 'fillna()和dropna()的区别是什么？', answer: 'fillna填充缺失值，dropna删除缺失值' },
      { question: 'to_datetime()的作用是什么？', answer: '将字符串转换为日期类型' }
    ]
  },
  9: {
    id: 9,
    course_id: 3,
    title: '数据筛选与聚合',
    theory: `<h3>数据筛选</h3><pre><code># 按条件筛选
filtered = df[df['Age'] > 30]

# 使用loc和iloc
df.loc[0:2, ['Name', 'Age']]  # 按标签
df.iloc[0:2, 0:2]             # 按位置</code></pre><h3>数据聚合</h3><pre><code># 分组聚合
grouped = df.groupby('City')['Age'].mean()

# 多个聚合函数
agg_result = df.groupby('City').agg({
    'Age': ['mean', 'max'],
    'Salary': 'sum'
})</code></pre><h3>数据透视表</h3><pre><code>pivot = df.pivot_table(
    index='City',
    columns='Gender',
    values='Salary',
    aggfunc='mean'
)</code></pre><div class="warn-box"><strong>注意：</strong>loc使用标签索引，iloc使用位置索引。</div>`,
    code_example: 'grouped = df.groupby("category")["sales"].sum()\nprint(grouped)',
    starter_code: '# 练习：数据筛选与聚合\nimport pandas as pd\n',
    exercises: [
      { question: 'loc和iloc的区别是什么？', answer: 'loc按标签，iloc按位置' },
      { question: 'groupby()的作用是什么？', answer: '按指定列分组' },
      { question: 'pivot_table()用于什么场景？', answer: '创建数据透视表' }
    ]
  },
  10: {
    id: 10,
    course_id: 4,
    title: 'Matplotlib基础',
    theory: `<h3>Matplotlib简介</h3><p>Matplotlib是Python最常用的数据可视化库，可以创建各种类型的图表。</p><pre><code>import matplotlib.pyplot as plt

# 简单折线图
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]

plt.plot(x, y)
plt.title("Simple Line Plot")
plt.xlabel("X Axis")
plt.ylabel("Y Axis")
plt.show()</code></pre><h3>常用图表类型</h3><ul><li><strong>折线图</strong>：展示趋势</li><li><strong>柱状图</strong>：比较数值</li><li><strong>散点图</strong>：展示相关性</li><li><strong>直方图</strong>：展示分布</li></ul><div class="key-point"><strong>关键点：</strong>良好的可视化能够帮助快速理解数据特征。</div>`,
    code_example: 'import matplotlib.pyplot as plt\nplt.bar(["A", "B", "C"], [10, 20, 15])\nplt.show()',
    starter_code: '# 练习：创建图表\nimport matplotlib.pyplot as plt\n',
    exercises: [
      { question: 'plt.plot()用于创建什么类型的图表？', answer: '折线图' },
      { question: 'plt.bar()用于创建什么类型的图表？', answer: '柱状图' },
      { question: 'plt.show()的作用是什么？', answer: '显示图表' }
    ]
  },
  11: {
    id: 11,
    course_id: 4,
    title: 'Seaborn高级图表',
    theory: `<h3>Seaborn简介</h3><p>Seaborn是基于Matplotlib的高级可视化库，提供更美观的图表样式。</p><pre><code>import seaborn as sns
import matplotlib.pyplot as plt

# 加载内置数据集
tips = sns.load_dataset("tips")

# 创建分布图
sns.histplot(data=tips, x="total_bill", kde=True)
plt.show()</code></pre><h3>常用Seaborn图表</h3><ul><li><strong>distplot</strong>：分布直方图</li><li><strong>scatterplot</strong>：散点图</li><li><strong>boxplot</strong>：箱线图</li><li><strong>heatmap</strong>：热力图</li></ul><div class="tip-box"><strong>小贴士：</strong>Seaborn默认样式比Matplotlib更美观。</div><h3>热力图示例</h3><pre><code>corr = df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.show()</code></pre>`,
    code_example: 'import seaborn as sns\ntips = sns.load_dataset("tips")\nsns.scatterplot(data=tips, x="total_bill", y="tip")\nplt.show()',
    starter_code: '# 练习：使用Seaborn\nimport seaborn as sns\n',
    exercises: [
      { question: 'Seaborn是基于哪个库开发的？', answer: 'Matplotlib' },
      { question: 'heatmap常用于展示什么？', answer: '相关性矩阵' },
      { question: 'load_dataset()可以加载什么？', answer: '内置数据集' }
    ]
  },
  12: {
    id: 12,
    course_id: 4,
    title: '交互式可视化',
    theory: `<h3>Plotly简介</h3><p>Plotly提供交互式可视化功能，可以创建可交互的图表。</p><pre><code>import plotly.express as px

df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species")
fig.show()</code></pre><h3>交互式图表特点</h3><ul><li>支持缩放和拖拽</li><li>悬停显示数据详情</li><li>支持多种导出格式</li><li>可嵌入网页</li></ul><div class="key-point"><strong>关键点：</strong>交互式图表非常适合网页展示和探索性数据分析。</div><h3>交互式柱状图</h3><pre><code>fig = px.bar(df, x="category", y="value", color="category")
fig.update_layout(title="Interactive Bar Chart")
fig.show()</code></pre>`,
    code_example: 'import plotly.express as px\nfig = px.line(x=[1,2,3], y=[4,5,6], title="Interactive Line")\nfig.show()',
    starter_code: '# 练习：创建交互式图表\nimport plotly.express as px\n',
    exercises: [
      { question: 'Plotly的主要特点是什么？', answer: '交互式可视化' },
      { question: 'fig.show()在Plotly中有什么作用？', answer: '显示交互式图表' },
      { question: 'plotly.express提供了什么？', answer: '高级API，简化图表创建' }
    ]
  },
  13: {
    id: 13,
    course_id: 5,
    title: '描述性统计',
    theory: `<h3>集中趋势度量</h3><ul><li><strong>均值</strong>：所有数据的平均值</li><li><strong>中位数</strong>：数据排序后的中间值</li><li><strong>众数</strong>：出现次数最多的值</li></ul><pre><code>import pandas as pd

data = pd.Series([1, 2, 3, 4, 5, 5, 6])
print(f"均值: {data.mean()}")
print(f"中位数: {data.median()}")
print(f"众数: {data.mode()[0]}")</code></pre><h3>离散程度度量</h3><ul><li><strong>极差</strong>：最大值减最小值</li><li><strong>方差</strong>：数据与均值的平均平方差</li><li><strong>标准差</strong>：方差的平方根</li></ul><div class="warn-box"><strong>注意：</strong>均值受极端值影响较大，中位数更稳健。</div>`,
    code_example: 'data = pd.Series([23, 45, 67, 89, 12, 34])\nprint(f"标准差: {data.std():.2f}")\nprint(f"极差: {data.max() - data.min()}")',
    starter_code: '# 练习：计算描述性统计\nimport pandas as pd\n',
    exercises: [
      { question: '均值和中位数的区别是什么？', answer: '均值易受极端值影响，中位数更稳健' },
      { question: '标准差表示什么？', answer: '数据的离散程度' },
      { question: '众数的定义是什么？', answer: '出现次数最多的值' }
    ]
  },
  14: {
    id: 14,
    course_id: 5,
    title: '概率分布',
    theory: `<h3>常见概率分布</h3><ul><li><strong>正态分布</strong>：钟形曲线，自然界常见</li><li><strong>二项分布</strong>：独立重复试验</li><li><strong>泊松分布</strong>：事件发生次数</li></ul><pre><code>import numpy as np
import matplotlib.pyplot as plt

# 生成正态分布数据
data = np.random.normal(0, 1, 1000)

# 绘制直方图
plt.hist(data, bins=30, density=True)
plt.title("Normal Distribution")
plt.show()</code></pre><h3>中心极限定理</h3><p>大量独立随机变量的和近似服从正态分布，与原始分布无关。</p><div class="key-point"><strong>关键点：</strong>中心极限定理是统计学的基石。</div>`,
    code_example: 'data = np.random.binomial(n=10, p=0.5, size=1000)\nplt.hist(data, bins=11)\nplt.show()',
    starter_code: '# 练习：生成概率分布数据\nimport numpy as np\n',
    exercises: [
      { question: '正态分布的特点是什么？', answer: '钟形曲线，对称分布' },
      { question: 'np.random.normal()的参数是什么？', answer: '均值、标准差、样本数' },
      { question: '中心极限定理的意义是什么？', answer: '大量独立变量和近似正态分布' }
    ]
  },
  15: {
    id: 15,
    course_id: 5,
    title: '假设检验',
    theory: `<h3>假设检验基本概念</h3><ul><li><strong>原假设(H0)</strong>：默认成立的假设</li><li><strong>备择假设(H1)</strong>：与原假设对立</li><li><strong>p值</strong>：在原假设成立时观察到当前数据的概率</li></ul><pre><code>from scipy import stats

# 单样本t检验
data = [1.1, 1.2, 1.3, 1.4, 1.5]
t_stat, p_value = stats.ttest_1samp(data, popmean=1.0)
print(f"p值: {p_value}")

if p_value < 0.05:
    print("拒绝原假设")
else:
    print("不能拒绝原假设")</code></pre><h3>常用检验方法</h3><ul><li><strong>t检验</strong>：比较均值</li><li><strong>卡方检验</strong>：检验独立性</li><li><strong>方差分析</strong>：比较多组均值</li></ul><div class="tip-box"><strong>小贴士：</strong>p值小于0.05通常认为统计显著。</div>`,
    code_example: 'from scipy import stats\na = [1, 2, 3, 4, 5]\nb = [2, 3, 4, 5, 6]\nt_stat, p_value = stats.ttest_ind(a, b)\nprint(f"p值: {p_value}")',
    starter_code: '# 练习：进行假设检验\nfrom scipy import stats\n',
    exercises: [
      { question: 'p值的含义是什么？', answer: '原假设成立时观察到当前数据的概率' },
      { question: 't检验用于什么场景？', answer: '比较均值' },
      { question: 'p < 0.05意味着什么？', answer: '拒绝原假设，结果统计显著' }
    ]
  },
  16: {
    id: 16,
    course_id: 6,
    title: '监督学习基础',
    theory: `<h3>监督学习概念</h3><p>监督学习是从标注数据中学习映射关系的机器学习方法。</p><ul><li><strong>分类</strong>：预测离散标签</li><li><strong>回归</strong>：预测连续数值</li></ul><pre><code>from sklearn.linear_model import LinearRegression

# 准备数据
X = [[1], [2], [3], [4], [5]]
y = [2, 4, 6, 8, 10]

# 创建模型
model = LinearRegression()

# 训练模型
model.fit(X, y)

# 预测
print(model.predict([[6]]))  # [12]</code></pre><div class="key-point"><strong>关键点：</strong>监督学习需要标注好的训练数据。</div><h3>模型评估</h3><ul><li><strong>准确率</strong>：分类正确的比例</li><li><strong>MSE</strong>：均方误差</li><li><strong>R²</strong>：回归拟合优度</li></ul>`,
    code_example: 'from sklearn.tree import DecisionTreeClassifier\nmodel = DecisionTreeClassifier()\nmodel.fit(X_train, y_train)\ny_pred = model.predict(X_test)',
    starter_code: '# 练习：训练简单模型\nfrom sklearn.linear_model import LinearRegression\n',
    exercises: [
      { question: '分类和回归的区别是什么？', answer: '分类预测离散标签，回归预测连续值' },
      { question: 'fit()方法的作用是什么？', answer: '训练模型' },
      { question: 'predict()方法的作用是什么？', answer: '进行预测' }
    ]
  },
  17: {
    id: 17,
    course_id: 6,
    title: '常用分类算法',
    theory: `<h3>逻辑回归</h3><p>逻辑回归用于二分类问题，输出概率值。</p><pre><code>from sklearn.linear_model import LogisticRegression

model = LogisticRegression()
model.fit(X_train, y_train)
prob = model.predict_proba(X_test)</code></pre><h3>决策树</h3><p>决策树通过递归划分特征空间进行预测。</p><pre><code>from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=3)
model.fit(X_train, y_train)</code></pre><h3>随机森林</h3><p>随机森林是多个决策树的集成，通常表现更好。</p><pre><code>from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)</code></pre><div class="tip-box"><strong>小贴士：</strong>随机森林通常比单棵决策树效果更好。</div>`,
    code_example: 'from sklearn.ensemble import RandomForestClassifier\nmodel = RandomForestClassifier(n_estimators=100)\nmodel.fit(X_train, y_train)',
    starter_code: '# 练习：使用分类算法\nfrom sklearn.ensemble import RandomForestClassifier\n',
    exercises: [
      { question: '逻辑回归用于什么场景？', answer: '二分类问题' },
      { question: '随机森林是什么？', answer: '多个决策树的集成' },
      { question: 'n_estimators参数表示什么？', answer: '决策树的数量' }
    ]
  },
  18: {
    id: 18,
    course_id: 6,
    title: '无监督学习',
    theory: `<h3>聚类分析</h3><p>聚类是将数据分组的无监督学习方法。</p><pre><code>from sklearn.cluster import KMeans

# 创建模型
kmeans = KMeans(n_clusters=3)

# 训练并预测
labels = kmeans.fit_predict(X)

# 获取聚类中心
centers = kmeans.cluster_centers_</code></pre><h3>降维方法</h3><p>主成分分析(PCA)用于数据降维：</p><pre><code>from sklearn.decomposition import PCA

# 将数据降至2维
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)</code></pre><div class="key-point"><strong>关键点：</strong>无监督学习不需要标注数据。</div><h3>评估指标</h3><ul><li><strong>轮廓系数</strong>：评估聚类质量</li><li><strong>惯性</strong>：KMeans的目标函数值</li></ul>`,
    code_example: 'from sklearn.cluster import KMeans\nkmeans = KMeans(n_clusters=3)\nlabels = kmeans.fit_predict(X)',
    starter_code: '# 练习：聚类分析\nfrom sklearn.cluster import KMeans\n',
    exercises: [
      { question: '聚类分析属于哪种学习类型？', answer: '无监督学习' },
      { question: 'KMeans需要指定什么参数？', answer: '聚类数量k' },
      { question: 'PCA的作用是什么？', answer: '数据降维' }
    ]
  },
  19: {
    id: 19,
    course_id: 7,
    title: '业务指标分析',
    theory: `<h3>关键业务指标</h3><ul><li><strong>销售额</strong>：总收入</li><li><strong>转化率</strong>：访问到购买的比例</li><li><strong>复购率</strong>：重复购买用户比例</li><li><strong>客单价</strong>：平均订单金额</li></ul><pre><code># 计算转化率
conversion_rate = (orders_count / visits_count) * 100

# 计算客单价
avg_order_value = total_revenue / orders_count

# 计算复购率
repeat_rate = (repeat_users / total_users) * 100</code></pre><h3>指标监控</h3><p>建立业务指标仪表盘，实时监控业务健康状况。</p><div class="tip-box"><strong>小贴士：</strong>选择核心KPI时要遵循SMART原则。</div>`,
    code_example: 'conversion_rate = (150 / 2000) * 100\nprint(f"转化率: {conversion_rate:.2f}%")',
    starter_code: '# 练习：计算业务指标\n',
    exercises: [
      { question: '转化率的计算公式是什么？', answer: '转化数/访问数 × 100%' },
      { question: '客单价表示什么？', answer: '平均订单金额' },
      { question: '复购率的意义是什么？', answer: '用户忠诚度的体现' }
    ]
  },
  20: {
    id: 20,
    course_id: 7,
    title: '用户行为分析',
    theory: `<h3>用户行为指标</h3><ul><li><strong>活跃用户</strong>：特定时间段内有行为的用户</li><li><strong>留存率</strong>：用户在后续时间点的留存比例</li><li><strong>用户旅程</strong>：用户从注册到转化的路径</li></ul><pre><code># 计算次日留存率
day1_retention = (day1_active / day0_new) * 100

# 计算7日留存率
day7_retention = (day7_active / day0_new) * 100</code></pre><h3>RFM模型</h3><p>RFM是客户价值分析的经典模型：</p><ul><li><strong>R</strong>：最近一次购买时间</li><li><strong>F</strong>：购买频率</li><li><strong>M</strong>：购买金额</li></ul><div class="key-point"><strong>关键点：</strong>留存率是衡量产品粘性的核心指标。</div>`,
    code_example: 'day1_retention = (350 / 1000) * 100\nprint(f"次日留存: {day1_retention:.1f}%")',
    starter_code: '# 练习：用户行为分析\n',
    exercises: [
      { question: '留存率的定义是什么？', answer: '用户在后续时间点的留存比例' },
      { question: 'RFM模型包含哪三个维度？', answer: '最近购买时间、购买频率、购买金额' },
      { question: '活跃用户的定义是什么？', answer: '特定时间段内有行为的用户' }
    ]
  },
  21: {
    id: 21,
    course_id: 7,
    title: 'A/B测试',
    theory: `<h3>A/B测试原理</h3><p>A/B测试是一种对照实验方法，用于比较两个版本的效果。</p><pre><code># 假设检验示例
from scipy import stats

# 版本A和版本B的转化率
a_conversion = [1, 0, 1, 0, 1, ...]
b_conversion = [1, 1, 0, 1, 1, ...]

# 进行卡方检验
contingency = [[sum(a_conversion), len(a_conversion)-sum(a_conversion)],
               [sum(b_conversion), len(b_conversion)-sum(b_conversion)]]

chi2, p_value, _, _ = stats.chi2_contingency(contingency)</code></pre><h3>A/B测试流程</h3><ol><li>确定假设和指标</li><li>计算样本量</li><li>分组实验</li><li>收集数据</li><li>统计分析</li><li>决策</li></ol><div class="warn-box"><strong>注意：</strong>确保两组用户具有可比性。</div>`,
    code_example: 'from scipy import stats\nchi2, p_value, _, _ = stats.chi2_contingency([[50, 150], [70, 130]])\nprint(f"p值: {p_value}")',
    starter_code: '# 练习：A/B测试分析\nfrom scipy import stats\n',
    exercises: [
      { question: 'A/B测试的目的是什么？', answer: '比较两个版本的效果' },
      { question: '卡方检验用于什么场景？', answer: '检验分类变量的独立性' },
      { question: 'A/B测试需要注意什么？', answer: '确保两组用户具有可比性' }
    ]
  },
  22: {
    id: 22,
    course_id: 8,
    title: '销售数据分析',
    theory: `<h3>销售数据预处理</h3><pre><code>import pandas as pd

# 读取销售数据
df = pd.read_csv('sales_data.csv')

# 数据清洗
df['date'] = pd.to_datetime(df['date'])
df = df.dropna(subset=['amount'])

# 添加时间特征
df['month'] = df['date'].dt.month
df['weekday'] = df['date'].dt.weekday</code></pre><h3>销售趋势分析</h3><pre><code># 按月统计销售额
monthly_sales = df.groupby('month')['amount'].sum()

# 可视化趋势
import matplotlib.pyplot as plt
monthly_sales.plot(kind='line')
plt.title("Monthly Sales Trend")
plt.show()</code></pre><h3>销售预测</h3><p>使用时间序列模型进行销售预测。</p><div class="tip-box"><strong>小贴士：</strong>时间序列分析需要考虑季节性因素。</div>`,
    code_example: 'monthly_sales = df.groupby(df["date"].dt.month)["amount"].sum()\nmonthly_sales.plot()',
    starter_code: '# 练习：销售数据分析\nimport pandas as pd\n',
    exercises: [
      { question: '时间序列分析需要考虑什么因素？', answer: '季节性、趋势、周期性' },
      { question: 'dt.month的作用是什么？', answer: '提取日期的月份' },
      { question: '销售趋势分析的目的是什么？', answer: '了解销售变化规律' }
    ]
  },
  23: {
    id: 23,
    course_id: 8,
    title: '客户分群分析',
    theory: `<h3>客户分群方法</h3><p>使用聚类分析对客户进行分群：</p><pre><code>import pandas as pd
from sklearn.cluster import KMeans

# 准备RFM数据
rfm_data = df.groupby('customer_id').agg({
    'date': lambda x: (max(df['date']) - x.max()).days,  # Recency
    'order_id': 'count',  # Frequency
    'amount': 'sum'       # Monetary
})

# 数据标准化
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm_data)

# 聚类
kmeans = KMeans(n_clusters=4, random_state=42)
rfm_data['cluster'] = kmeans.fit_predict(rfm_scaled)</code></pre><h3>客户群体特征分析</h3><p>分析每个客户群体的特征，制定差异化策略。</p><div class="key-point"><strong>关键点：</strong>客户分群有助于精准营销。</div>`,
    code_example: 'rfm_data = df.groupby("customer_id").agg({\n    "date": lambda x: (max_date - x.max()).days,\n    "order_id": "count",\n    "amount": "sum"\n})',
    starter_code: '# 练习：客户分群分析\nimport pandas as pd\nfrom sklearn.cluster import KMeans\n',
    exercises: [
      { question: 'RFM模型的三个维度是什么？', answer: 'Recency、Frequency、Monetary' },
      { question: '为什么需要数据标准化？', answer: '消除量纲差异，使各特征权重相等' },
      { question: '客户分群的目的是什么？', answer: '精准营销，差异化策略' }
    ]
  },
  24: {
    id: 24,
    course_id: 8,
    title: '综合项目实战',
    theory: `<h3>项目流程</h3><ol><li><strong>需求理解</strong>：明确业务问题</li><li><strong>数据收集</strong>：获取相关数据</li><li><strong>数据清洗</strong>：处理缺失值和异常值</li><li><strong>分析建模</strong>：应用分析方法</li><li><strong>结果呈现</strong>：可视化和报告</li></ol><h3>实战项目示例</h3><p>电商用户购买行为分析：</p><pre><code># 完整分析流程
1. 数据导入与探索
2. 用户行为漏斗分析
3. 转化率计算
4. 用户分群
5. 营销建议</code></pre><h3>报告撰写</h3><p>数据分析报告应包括：</p><ul><li>问题定义</li><li>数据来源</li><li>分析方法</li><li>关键发现</li><li>建议措施</li></ul><div class="tip-box"><strong>小贴士：</strong>优秀的报告应该清晰、简洁、有行动建议。</div>`,
    code_example: '# 综合项目实战\nprint("完成商务数据分析综合项目")',
    starter_code: '# 综合项目实战\n# 整合所学知识完成完整分析\n',
    exercises: [
      { question: '数据分析项目的基本流程是什么？', answer: '需求理解→数据收集→数据清洗→分析建模→结果呈现' },
      { question: '数据分析报告应包含哪些部分？', answer: '问题定义、数据来源、分析方法、关键发现、建议措施' },
      { question: '为什么结果呈现很重要？', answer: '让非技术人员理解分析结果' }
    ]
  }
};

export const PROJECTS = [
  {
    id: 1,
    title: '销售数据分析报告',
    description: '分析电商平台销售数据，识别销售趋势和关键指标',
    difficulty: '初级',
    duration: '3小时',
    skills: ['Pandas', 'Matplotlib', '数据可视化']
  },
  {
    id: 2,
    title: '用户行为漏斗分析',
    description: '分析用户从访问到购买的转化漏斗，找出优化点',
    difficulty: '初级',
    duration: '4小时',
    skills: ['Pandas', '漏斗图', '转化率分析']
  },
  {
    id: 3,
    title: '客户分群与精准营销',
    description: '使用RFM模型对客户进行分群，制定营销策略',
    difficulty: '中级',
    duration: '5小时',
    skills: ['Pandas', 'KMeans', 'RFM分析']
  },
  {
    id: 4,
    title: 'A/B测试效果评估',
    description: '设计并分析A/B测试结果，评估新功能效果',
    difficulty: '中级',
    duration: '4小时',
    skills: ['统计检验', '假设检验', '数据分析']
  },
  {
    id: 5,
    title: '销售预测模型',
    description: '使用时间序列分析预测未来销售额',
    difficulty: '中级',
    duration: '6小时',
    skills: ['时间序列', 'ARIMA', '预测']
  },
  {
    id: 6,
    title: '客户流失预测',
    description: '构建机器学习模型预测客户流失风险',
    difficulty: '高级',
    duration: '6小时',
    skills: ['机器学习', '分类算法', '特征工程']
  },
  {
    id: 7,
    title: '商品推荐系统',
    description: '基于协同过滤构建商品推荐系统',
    difficulty: '高级',
    duration: '8小时',
    skills: ['协同过滤', '相似度计算', '推荐算法']
  },
  {
    id: 8,
    title: '用户满意度分析',
    description: '分析用户评论数据，挖掘用户满意度影响因素',
    difficulty: '中级',
    duration: '5小时',
    skills: ['文本分析', '情感分析', '词云']
  },
  {
    id: 9,
    title: '供应链数据分析',
    description: '分析供应链数据，优化库存管理',
    difficulty: '中级',
    duration: '5小时',
    skills: ['库存分析', '需求预测', '优化']
  },
  {
    id: 10,
    title: '综合数据分析项目',
    description: '整合所有知识，完成一个完整的商业数据分析项目',
    difficulty: '高级',
    duration: '10小时',
    skills: ['综合分析', '报告撰写', '可视化']
  }
];
