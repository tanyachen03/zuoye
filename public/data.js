// 课程数据
const coursesData = {
    'python-basics': {
        id: 'python-basics',
        title: '🐍 Python 数据分析基础',
        description: '从零开始学习 Python 基础语法和数据处理库 Pandas',
        level: '入门',
        duration: '8小时',
        color: '#667eea',
        gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        chapters: [
            {
                id: 'intro',
                title: 'Python 环境搭建与基础语法',
                duration: '2小时',
                theory: `## Python 简介\n\nPython是一种高级编程语言，以其简洁易读的语法和强大的功能而闻名。在数据分析领域，Python是最流行的工具之一。\n\n### 为什么选择Python？\n\n1. **简洁易学**：语法接近英语，学习曲线平缓\n2. **生态丰富**：拥有大量的数据分析库（如pandas, numpy, matplotlib）\n3. **应用广泛**：从数据分析到机器学习，从Web开发到自动化\n\n### Python环境搭建\n\n推荐使用Anaconda发行版，它包含了Python解释器和常用的科学计算库。\n\n### 基本语法示例\n\n- 变量赋值：直接使用变量名\n- 数据类型：数字、字符串、列表、字典\n- 条件语句：if/elif/else\n- 循环语句：for/while`,
                tips: [
                    '在Python中，缩进是语法的一部分，请保持4个空格的缩进风格',
                    '建议使用Anaconda来管理你的Python环境和包',
                    '多写多练是学习Python最好的方法'
                ],
                code: `# 变量赋值
name = "张三"
age = 25
is_student = True

# 打印输出
print(f"姓名: {name}, 年龄: {age}")

# 列表操作
fruits = ["苹果", "香蕉", "橙子"]
fruits.append("葡萄")
print(f"水果列表: {fruits}")

# 条件判断
if age >= 18:
    print("已成年")
else:
    print("未成年")

# 循环
for fruit in fruits:
    print(f"- {fruit}")`,
                exercises: [
                    { question: 'Python中用于定义列表的符号是？', options: ['{}', '[]', '()', '<>'], answer: 1, explanation: '在Python中，列表使用方括号[]定义，{}用于字典，()用于元组，<>不是Python的容器定义符号。' },
                    { question: '以下哪个是正确的Python变量命名？', options: ['2name', 'my-name', 'my_name', 'class'], answer: 2, explanation: 'Python变量命名规则：不能以数字开头，不能包含连字符，可以使用下划线，class是保留关键字不能作为变量名。' },
                    { question: 'Python中print函数的作用是？', options: ['计算', '输入', '输出', '保存'], answer: 2, explanation: 'print()函数用于将内容输出到控制台，是Python中最常用的输出方法。' },
                    { question: '以下哪个不是Python的基本数据类型？', options: ['int', 'float', 'string', 'array'], answer: 3, explanation: 'Python的基本数据类型包括int(整数)、float(浮点数)、str(字符串)等，array不是Python内置类型，需要导入array模块。' },
                    { question: 'for循环可以遍历哪种数据类型？', options: ['只有列表', '只有字符串', '只有字典', '可迭代对象'], answer: 3, explanation: 'for循环可以遍历任何可迭代对象，包括列表、字符串、字典、元组、集合等。' }
                ]
            },
            {
                id: 'pandas',
                title: 'Pandas 数据处理入门',
                duration: '3小时',
                theory: `## Pandas 简介\n\nPandas是Python中最强大的数据处理和分析库，提供了快速、灵活和表达力强的数据结构。\n\n### 核心数据结构\n\n1. **Series**：一维标签数组\n2. **DataFrame**：二维表格数据\n\n### 基本操作\n\n- 读取数据：read_csv, read_excel, read_sql\n- 数据探索：head(), info(), describe()\n- 数据选择：列选择、行选择、条件筛选\n- 数据清洗：dropna(), fillna(), drop_duplicates()\n\n### DataFrame 是什么？\n\nDataFrame是Pandas的核心数据结构，可以想象成一个Excel表格，包含行索引和列名。`,
                tips: [
                    '学会使用head()和tail()快速查看数据的前几行和后几行',
                    'info()方法能显示数据的基本信息，包括每列的数据类型和非空值数量',
                    'describe()提供数值列的统计摘要，非常实用'
                ],
                code: `import pandas as pd

# 创建DataFrame
data = {
    '姓名': ['张三', '李四', '王五'],
    '年龄': [25, 30, 35],
    '城市': ['北京', '上海', '深圳']
}
df = pd.DataFrame(data)
print(df)

# 查看数据
print(df.head())      # 前5行
print(df.info())      # 数据信息
print(df.describe())   # 统计描述

# 数据选择
print(df['姓名'])        # 选择单列
print(df[['姓名', '年龄']]) # 选择多列
print(df[df['年龄'] > 25]) # 条件筛选`,
                exercises: [
                    { question: 'Pandas中用于存储二维表格数据的数据结构是？', options: ['Series', 'DataFrame', 'Array', 'Matrix'], answer: 1, explanation: 'DataFrame是Pandas的核心数据结构，用于存储二维表格数据，类似于Excel表格。' },
                    { question: '查看DataFrame前5行数据应该使用哪个方法？', options: ['view()', 'head()', 'top()', 'first()'], answer: 1, explanation: 'head()方法默认显示前5行数据，可以传入参数指定行数，如head(10)显示前10行。' },
                    { question: '要获取DataFrame的基本信息（列名、数据类型、非空值数量）应该使用？', options: ['describe()', 'info()', 'summary()', 'stats()'], answer: 1, explanation: 'info()方法显示数据的基本信息，describe()显示统计摘要。' },
                    { question: '如何从DataFrame中选择单列数据？', options: ['df.col', 'df["col"]', 'df.col()', '以上都可以'], answer: 3, explanation: 'Pandas支持多种方式选择列：df["列名"]和df.列名都可以，推荐使用df["列名"]的方式。' },
                    { question: 'dropna()方法的作用是？', options: ['删除列', '删除包含缺失值的行', '填充缺失值', '删除重复值'], answer: 1, explanation: 'dropna()用于删除包含缺失值(NaN)的行，fillna()用于填充缺失值，drop_duplicates()用于删除重复值。' }
                ]
            },
            {
                id: 'analysis',
                title: '数据聚合与分析实战',
                duration: '3小时',
                theory: `## 数据聚合\n\n数据聚合是将数据按特定维度进行分组并计算统计量的过程。\n\n### 常用聚合方法\n\n1. **groupby**：按列分组\n2. **agg**：对分组应用多种统计方法\n3. **transform**：对分组内数据进行变换\n\n### 常见统计量\n\n- count：计数\n- sum：求和\n- mean：均值\n- median：中位数\n- min/max：最小/最大值\n- std：标准差`,
                tips: [
                    'groupby是Pandas中最强大的功能之一，熟练掌握非常重要',
                    '结合agg()可以一次性计算多个统计量，非常高效',
                    '学会使用value_counts()快速了解列的取值分布'
                ],
                code: `import pandas as pd

# 创建示例销售数据
sales_data = {
    '产品': ['A', 'B', 'A', 'B', 'A', 'B'],
    '地区': ['华北', '华东', '华南', '华北', '华东', '华南'],
    '销量': [120, 85, 200, 65, 180, 95],
    '单价': [100, 150, 100, 150, 100, 150]
}
df = pd.DataFrame(sales_data)
df['销售额'] = df['销量'] * df['单价']

# 按产品分组计算统计量
product_stats = df.groupby('产品').agg({
    '销量': ['count', 'sum', 'mean'],
    '销售额': ['sum', 'mean']
})
print("产品统计:")
print(product_stats)

# 按地区分组计算总销售额
region_sales = df.groupby('地区')['销售额'].sum().sort_values(ascending=False)
print("\\n地区销售排名:")
print(region_sales)`,
                exercises: [
                    { question: '按列进行分组的Pandas方法是？', options: ['sort()', 'groupby()', 'filter()', 'split()'], answer: 1, explanation: 'groupby()方法用于按指定列对数据进行分组，是Pandas中最强大的功能之一。' },
                    { question: 'agg()方法的作用是？', options: ['排序', '聚合计算', '筛选', '合并'], answer: 1, explanation: 'agg()方法用于对分组数据应用聚合函数，可以一次性计算多个统计量。' },
                    { question: '计算销售额列的总和应该使用？', options: ['df.sum()', 'df["销售额"].sum()', 'df.sum("销售额")', 'df.total()'], answer: 1, explanation: '正确的用法是df["列名"].sum()来计算某一列的总和。' },
                    { question: 'value_counts()方法的作用是？', options: ['计算总和', '统计频次', '排序', '去重'], answer: 1, explanation: 'value_counts()用于统计某列中各值出现的频次，是数据分析中常用的方法。' },
                    { question: 'sort_values()方法默认按什么顺序排序？', options: ['降序', '升序', '随机', '按索引'], answer: 1, explanation: 'sort_values()默认按升序(ascending=True)排序，可以设置ascending=False改为降序。' }
                ]
            }
        ]
    },
    'data-visualization': {
        id: 'data-visualization',
        title: '📊 数据可视化与图表制作',
        description: '学习使用 Matplotlib 和 Seaborn 创建专业图表',
        level: '入门',
        duration: '6小时',
        color: '#11998e',
        gradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        chapters: [
            {
                id: 'matplotlib',
                title: 'Matplotlib 基础图表',
                duration: '2小时',
                theory: `## 数据可视化概述\n\n数据可视化是将数据转换为图形表示的过程，帮助我们发现数据中的模式、趋势和异常。\n\n### Matplotlib 简介\n\nMatplotlib是Python最流行的可视化库，可以创建各种静态、动态、交互式图表。\n\n### 基础图表类型\n\n- 折线图：显示趋势变化\n- 柱状图：对比不同类别\n- 饼图：显示占比\n- 散点图：显示相关性\n- 直方图：显示分布`,
                tips: [
                    '好的图表应该简洁明了，突出重点信息',
                    '中文字体需要特别设置，否则会显示乱码',
                    '图表要添加标题和坐标轴标签，让读者一眼理解'
                ],
                code: `import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

# 折线图
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linewidth=2, color='#3498db')
plt.title('销售趋势图')
plt.xlabel('月份')
plt.ylabel('销售额(万元)')
plt.grid(True, alpha=0.3)
plt.show()

# 柱状图
categories = ['产品A', '产品B', '产品C']
values = [45, 67, 89]
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['#3498db', '#2ecc71', '#e74c3c'])
plt.title('产品销量对比')
plt.show()`,
                exercises: [
                    { question: 'Matplotlib中创建柱状图的函数是？', options: ['plt.plot()', 'plt.bar()', 'plt.pie()', 'plt.scatter()'], answer: 1 }
                ]
            },
            {
                id: 'seaborn',
                title: 'Seaborn 高级可视化',
                duration: '2小时',
                theory: `## Seaborn 简介\n\nSeaborn是基于Matplotlib的高级可视化库，提供更美观的默认样式和统计图表。\n\n### Seaborn 特色\n\n1. 更美观的默认样式\n2. 内置统计图表\n3. 简单的API\n4. 支持DataFrame直接操作\n\n### 常用图表\n\n- 热力图：显示矩阵数据\n- 箱线图：显示分布和异常值\n- 分布图：显示变量分布\n- 相关性矩阵图：探索变量间关系`,
                tips: [
                    'Seaborn需要搭配Matplotlib一起使用，两者可以无缝结合',
                    '用heatmap展示相关性矩阵非常直观',
                    '箱线图(boxplot)非常适合发现异常值'
                ],
                code: `import seaborn as sns
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

# 创建示例数据
import pandas as pd
data = {
    '销售额': [100, 200, 150, 300, 250],
    '客户数': [50, 80, 65, 120, 100],
    '满意度': [4.2, 4.5, 4.0, 4.8, 4.6]
}
df = pd.DataFrame(data)

# 绘制相关性热力图
corr_matrix = df.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('相关性矩阵')
plt.show()

# 箱线图 - 展示分布
plt.figure(figsize=(10, 6))
sns.boxplot(data=df)
plt.title('各变量分布情况')
plt.show()`,
                exercises: [
                    { question: '用于展示变量之间相关性的最佳图表类型是？', options: ['折线图', '饼图', '热力图', '柱状图'], answer: 2, explanation: '热力图通过颜色深浅来表示数据之间的相关性，是展示变量相关性的最佳选择。' },
                    { question: '展示时间序列趋势应该使用哪种图表？', options: ['饼图', '折线图', '散点图', '直方图'], answer: 1, explanation: '折线图最适合展示随时间变化的数据趋势。' },
                    { question: '对比不同类别的数值大小应该使用？', options: ['折线图', '柱状图', '饼图', '箱线图'], answer: 1, explanation: '柱状图是对比不同类别数值大小的最佳选择。' },
                    { question: '展示数据分布情况应该使用？', options: ['柱状图', '折线图', '直方图', '饼图'], answer: 2, explanation: '直方图用于展示数据的分布情况，显示不同区间的数据频次。' },
                    { question: '设置中文字体应该修改哪个参数？', options: ['font.size', 'font.sans-serif', 'font.family', 'text.font'], answer: 1, explanation: '通过plt.rcParams[\'font.sans-serif\']设置中文字体，如SimHei或Noto Sans CJK SC。' }
                ]
            },
            {
                id: 'best-practices',
                title: '图表设计原则与最佳实践',
                duration: '2小时',
                theory: `## 好图表的原则\n\n1. 简洁清晰：去掉多余装饰\n2. 突出重点：让读者一眼看到关键信息\n3. 色彩协调：使用适当的配色方案\n4. 信息完整：包含必要的标题、标签、图例\n\n### 常见错误\n\n1. 饼图太多类别：超过5个类别就改用柱状图\n2. 3D效果：会误导读者判断，建议慎用\n3. 坐标轴不从0开始：容易误导读者\n4. 颜色过于花哨：保持简洁专业`,
                tips: [
                    '少即是多：图表越简洁越容易理解',
                    '始终添加标题、坐标轴标签和单位',
                    '选择合适的图表类型比复杂的样式更重要'
                ],
                code: `# 最佳实践示例
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei', 'Noto Sans CJK SC']
plt.rcParams['axes.unicode_minus'] = False

# 好的柱状图：简洁明了
categories = ['A', 'B', 'C', 'D']
values = [45, 67, 32, 89]

plt.figure(figsize=(12, 7))
bars = plt.bar(categories, values, 
               color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'],
               edgecolor='white', linewidth=2)

# 添加数值标签
for bar, val in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, val + 1,
             str(val), ha='center', fontsize=12, fontweight='bold')

plt.title('产品销量对比', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('产品类型', fontsize=12)
plt.ylabel('销量', fontsize=12)
plt.xticks(fontsize=11)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.show()`,
                exercises: [
                    { question: '设计图表时最重要的原则是？', options: ['使用炫酷效果', '简洁清晰突出重点', '多用色彩', '信息越详细越好'], answer: 1, explanation: '好图表的核心原则是简洁清晰，让读者能够快速理解关键信息。' },
                    { question: '饼图适合展示多少个类别？', options: ['越多越好', '不超过5个', '10个以上', '随便多少'], answer: 1, explanation: '饼图适合展示少量类别（建议不超过5个），类别太多会难以区分。' },
                    { question: '以下哪种做法容易误导读者？', options: ['坐标轴从0开始', '使用3D效果', '添加数据标签', '保持简洁'], answer: 1, explanation: '3D效果会扭曲视觉比例，容易误导读者对数据大小的判断。' },
                    { question: '图表应该包含哪些元素？', options: ['标题', '坐标轴标签', '图例', '以上都是'], answer: 3, explanation: '一个完整的图表应该包含标题、坐标轴标签和图例，帮助读者理解图表内容。' },
                    { question: '颜色使用原则是？', options: ['越多越好看', '保持简洁专业', '使用高饱和度颜色', '随机搭配'], answer: 1, explanation: '图表颜色应该保持简洁专业，避免过于花哨的配色。' }
                ]
            }
        ]
    },
    'sql-analysis': {
        id: 'sql-analysis',
        title: '🗄️ SQL 数据查询与分析',
        description: '掌握 SQL 查询技巧，从数据库高效提取业务数据',
        level: '入门',
        duration: '5小时',
        color: '#2193b0',
        gradient: 'linear-gradient(135deg, #2193b0 0%, #6dd5ed 100%)',
        chapters: [
            {
                id: 'sql-basics',
                title: 'SQL 基础查询',
                duration: '2小时',
                theory: `## SQL 简介\n\nSQL（结构化查询语言）是用于管理和查询关系型数据库的标准语言。\n\n### 基本语句\n\n1. **SELECT**：选择数据\n2. **FROM**：指定表\n3. **WHERE**：筛选条件\n4. **ORDER BY**：排序\n5. **LIMIT**：限制返回行数\n\n### 常见查询模式\n\n- 选择所有列：SELECT * FROM table\n- 选择特定列：SELECT col1, col2 FROM table\n- 条件筛选：WHERE condition\n- 模糊匹配：LIKE '%text%'`,
                tips: [
                    'SELECT * 在生产环境要慎用，尽量明确列名',
                    'WHERE子句在大数据表中可以通过索引优化查询速度',
                    'ORDER BY 可以指定 ASC(升序) 或 DESC(降序)'
                ],
                code: `-- 基本查询
SELECT * FROM customers;  -- 选择所有列
SELECT name, email FROM customers;  -- 选择特定列

-- 条件筛选
SELECT * FROM orders
WHERE amount > 1000;  -- 金额大于1000

-- 多条件查询
SELECT * FROM orders
WHERE amount > 1000
  AND status = 'completed'
  AND order_date >= '2024-01-01';

-- 模糊匹配
SELECT * FROM products
WHERE name LIKE '%手机%';  -- 名称包含"手机"

-- 排序
SELECT * FROM orders
ORDER BY amount DESC  -- 按金额降序
LIMIT 10;  -- 取前10条`,
                exercises: [
                    { question: 'SQL中用于筛选条件的关键字是？', options: ['FILTER', 'WHERE', 'IF', 'CONDITION'], answer: 1, explanation: 'WHERE子句用于筛选满足条件的记录，是SQL查询中最常用的关键字之一。' },
                    { question: 'SELECT * FROM table的作用是？', options: ['选择特定列', '选择所有列', '删除数据', '更新数据'], answer: 1, explanation: '*表示选择所有列，SELECT * FROM table会返回表中的所有数据。' },
                    { question: 'ORDER BY默认按什么顺序排序？', options: ['降序', '升序', '随机', '按ID'], answer: 1, explanation: 'ORDER BY默认按升序(ASC)排序，可以使用DESC关键字改为降序。' },
                    { question: 'LIMIT关键字的作用是？', options: ['删除数据', '限制返回行数', '修改数据', '插入数据'], answer: 1, explanation: 'LIMIT用于限制查询结果返回的行数，常用于分页或获取前N条数据。' },
                    { question: 'LIKE操作符用于？', options: ['精确匹配', '模糊匹配', '数值比较', '逻辑运算'], answer: 1, explanation: 'LIKE用于模糊匹配，可以使用%表示任意字符，_表示单个字符。' }
                ]
            },
            {
                id: 'sql-aggregation',
                title: 'SQL 聚合与分组',
                duration: '1.5小时',
                theory: `## 聚合函数\n\n聚合函数用于对一组值进行计算，返回单个值。\n\n### 常用聚合函数\n\n- COUNT()：计数\n- SUM()：求和\n- AVG()：平均值\n- MIN()/MAX()：最小/最大值\n\n### GROUP BY\n\n将数据按一个或多个列分组，对每个组应用聚合函数。\n\n### HAVING\n\n对分组后的结果进行筛选（WHERE筛选原始数据，HAVING筛选分组结果）。`,
                tips: [
                    'COUNT(*) 会包括NULL值，COUNT(列名) 会排除NULL',
                    'WHERE在GROUP BY之前执行，HAVING在GROUP BY之后执行',
                    'GROUP BY的列必须出现在SELECT中（聚合函数除外）'
                ],
                code: `-- 聚合函数
SELECT COUNT(*) as total_orders,  -- 总订单数
       SUM(amount) as total_amount,  -- 总金额
       AVG(amount) as avg_amount,   -- 平均金额
       MIN(amount) as min_amount,   -- 最小金额
       MAX(amount) as max_amount    -- 最大金额
FROM orders;

-- 按客户分组：找出TOP 10客户
SELECT customer_id,
       COUNT(*) as order_count,
       SUM(amount) as total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

-- 按月分组：月度销售趋势
SELECT strftime('%Y-%m', order_date) as month,
       SUM(amount) as monthly_sales
FROM orders
GROUP BY month
ORDER BY month DESC;`,
                exercises: [
                    { question: '对分组后的数据进行筛选应该使用？', options: ['WHERE', 'HAVING', 'FILTER', 'IF'], answer: 1, explanation: 'HAVING用于筛选分组后的结果，而WHERE在分组前筛选原始数据。' },
                    { question: 'COUNT(*)和COUNT(列名)的区别是？', options: ['没有区别', 'COUNT(*)包含NULL', 'COUNT(列名)包含NULL', 'COUNT(*)更快'], answer: 1, explanation: 'COUNT(*)会统计所有行包括NULL值，COUNT(列名)只统计非NULL值。' },
                    { question: '计算平均值应该使用哪个聚合函数？', options: ['SUM()', 'AVG()', 'MEAN()', 'MEDIAN()'], answer: 1, explanation: 'AVG()用于计算平均值，SUM()求和，MEDIAN()不是标准SQL聚合函数。' },
                    { question: 'GROUP BY子句的作用是？', options: ['排序', '分组', '筛选', '连接'], answer: 1, explanation: 'GROUP BY用于按指定列对数据进行分组，通常与聚合函数一起使用。' },
                    { question: '计算总和应该使用？', options: ['COUNT()', 'AVG()', 'SUM()', 'TOTAL()'], answer: 2, explanation: 'SUM()用于计算数值列的总和。' }
                ]
            },
            {
                id: 'sql-joins',
                title: 'SQL 多表连接',
                duration: '1.5小时',
                theory: `## 表连接\n\n关系型数据库通常由多张表组成，通过JOIN可以在查询中组合多张表的数据。\n\n### 连接类型\n\n1. **INNER JOIN**：只返回匹配的行\n2. **LEFT JOIN**：返回左表所有行+右表匹配行\n3. **RIGHT JOIN**：返回右表所有行+左表匹配行\n4. **FULL JOIN**：返回两表所有行\n\n### 连接条件\n\n通常使用主键和外键的关系来连接表。`,
                tips: [
                    'INNER JOIN是最常用的连接类型',
                    'LEFT JOIN适合保留主表所有信息的场景',
                    '给表起别名(AS)可以让查询更简洁',
                    '多表连接时，确保ON子句条件正确，避免笛卡尔积'
                ],
                code: `-- INNER JOIN: 只返回匹配行
SELECT o.order_id, o.amount, c.name
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id;

-- LEFT JOIN: 保留左表所有行
SELECT p.product_id, p.name, SUM(o.amount) as total_sales
FROM products p
LEFT JOIN orders o ON p.id = o.product_id
GROUP BY p.id, p.name
ORDER BY total_sales DESC NULLS LAST;

-- 多表连接：同时连接3张表
SELECT c.name as customer_name,
       p.name as product_name,
       o.amount,
       o.order_date
FROM orders o
INNER JOIN customers c ON o.customer_id = c.id
INNER JOIN products p ON o.product_id = p.id
WHERE o.order_date >= '2024-01-01'
ORDER BY o.amount DESC;`,
                exercises: [
                    { question: '只返回两表匹配行的连接类型是？', options: ['LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'FULL JOIN'], answer: 2, explanation: 'INNER JOIN只返回两表中匹配的行，不匹配的行会被过滤掉。' },
                    { question: '保留左表所有行的连接类型是？', options: ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN'], answer: 1, explanation: 'LEFT JOIN会返回左表的所有行，右表中不匹配的行显示为NULL。' },
                    { question: '连接条件应该写在哪个子句中？', options: ['WHERE', 'ON', 'HAVING', 'FROM'], answer: 1, explanation: 'JOIN的连接条件应该写在ON子句中，WHERE用于筛选结果。' },
                    { question: '给表起别名使用哪个关键字？', options: ['AS', 'ALIAS', 'RENAME', 'USE'], answer: 0, explanation: '可以使用AS关键字给表起别名，也可以直接写别名（如FROM orders o）。' },
                    { question: '哪种连接会返回两表所有行？', options: ['INNER JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'FULL JOIN'], answer: 3, explanation: 'FULL JOIN会返回两表的所有行，不匹配的部分显示为NULL。' }
                ]
            }
        ]
    },
    'statistical-analysis': {
        id: 'statistical-analysis',
        title: '📈 统计分析基础',
        description: '学习描述性统计、假设检验和回归分析等统计方法',
        level: '进阶',
        duration: '10小时',
        color: '#f2994a',
        gradient: 'linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)',
        chapters: [
            {
                id: 'descriptive',
                title: '描述性统计',
                duration: '3小时',
                theory: `## 描述性统计\n\n描述性统计用于总结和描述数据的主要特征。\n\n### 集中趋势\n\n1. **均值(Mean)**：平均值\n2. **中位数(Median)**：中间值，不受极端值影响\n3. **众数(Mode)**：出现最频繁的值\n\n### 离散程度\n\n1. **极差(Range)**：最大值-最小值\n2. **方差(Variance)**：数据的离散程度\n3. **标准差(Standard Deviation)**：方差的平方根，最常用\n\n### 分布形态\n\n- 偏度(Skewness)：分布的对称性\n- 峰度(Kurtosis)：分布的尖锐程度`,
                tips: [
                    '均值对异常值敏感，这时候中位数更可靠',
                    '标准差越大，说明数据越分散',
                    '在报告中，最好同时报告均值和标准差'
                ],
                code: `import pandas as pd
import numpy as np

# 示例数据
data = [23, 25, 27, 28, 30, 35, 40, 45, 50, 55, 100]

# 描述性统计
print(f"均值: {np.mean(data):.2f}")
print(f"中位数: {np.median(data):.2f}")
print(f"标准差: {np.std(data):.2f}")
print(f"方差: {np.var(data):.2f}")
print(f"最小值: {np.min(data)}")
print(f"最大值: {np.max(data)}")

# 使用Pandas的describe
df = pd.DataFrame(data, columns=['values'])
print("\\nPandas描述统计:")
print(df.describe())

# 检测异常值: 使用IQR方法
Q1 = np.percentile(data, 25)
Q3 = np.percentile(data, 75)
IQR = Q3 - Q1
print(f"\\nIQR: {IQR}")
print(f"异常值边界: [{Q1 - 1.5*IQR:.2f}, {Q3 + 1.5*IQR:.2f}]")`,
                exercises: [
                    { question: '不受极端值影响的集中趋势指标是？', options: ['均值', '中位数', '众数', '极差'], answer: 1, explanation: '中位数是中间位置的值，不受极端值影响，适合描述偏态分布的数据。' },
                    { question: '衡量数据离散程度的指标是？', options: ['均值', '中位数', '标准差', '众数'], answer: 2, explanation: '标准差衡量数据与均值的平均距离，是最常用的离散程度指标。' },
                    { question: '描述数据分布形态的指标是？', options: ['均值', '偏度', '总和', '计数'], answer: 1, explanation: '偏度描述分布的对称性，峰度描述分布的尖锐程度。' },
                    { question: 'IQR方法用于？', options: ['计算均值', '检测异常值', '计算标准差', '数据排序'], answer: 1, explanation: 'IQR（四分位距）方法是常用的异常值检测方法，超过Q1-1.5*IQR或Q3+1.5*IQR的值被认为是异常值。' },
                    { question: 'Pandas中哪个方法可以快速获取描述性统计？', options: ['stats()', 'describe()', 'summary()', 'info()'], answer: 1, explanation: 'describe()方法可以快速获取数据的基本统计信息，包括均值、标准差、最小值、最大值等。' }
                ]
            },
            {
                id: 'hypothesis',
                title: '假设检验',
                duration: '3.5小时',
                theory: `## 假设检验\n\n假设检验是一种统计方法，用于判断关于总体的某个假设是否合理。\n\n### 基本概念\n\n1. **原假设(H0)**：通常是要否定的假设\n2. **备择假设(H1)**：通常是要支持的假设\n3. **p值**：结果偶然发生的概率\n4. **显著性水平(α)**：通常设为0.05\n\n### 常用检验\n\n- **t检验**：比较两组均值\n- **卡方检验**：比较分类变量\n- **ANOVA**：比较多组均值\n\n### 判断规则\n\n- p < 0.05：拒绝原假设，结果显著\n- p >= 0.05：不拒绝原假设，结果不显著`,
                tips: [
                    'p值小不代表效应大，只是说明结果更可信',
                    '0.05是常用的阈值，但不是绝对标准',
                    '相关不等于因果，假设检验只能判断显著性'
                ],
                code: `import numpy as np
from scipy import stats

# 示例：比较两个班级的成绩
class_a = [85, 88, 90, 92, 95, 80, 78, 90, 88, 85]
class_b = [75, 78, 80, 82, 85, 70, 72, 78, 80, 75]

# 独立样本t检验
t_stat, p_value = stats.ttest_ind(class_a, class_b)

print(f"班级A均值: {np.mean(class_a):.1f}")
print(f"班级B均值: {np.mean(class_b):.1f}")
print(f"t统计量: {t_stat:.4f}")
print(f"p值: {p_value:.4f}")

if p_value < 0.05:
    print("结论: 两个班级成绩存在显著差异 (p < 0.05)")
else:
    print("结论: 两个班级成绩无显著差异 (p >= 0.05)")`,
                exercises: [
                    { question: '通常认为统计显著的p值阈值是？', options: ['p < 0.01', 'p < 0.05', 'p < 0.10', 'p < 0.50'], answer: 1, explanation: '0.05是最常用的显著性水平，p < 0.05表示结果不太可能是偶然发生的。' },
                    { question: '原假设通常是？', options: ['要支持的假设', '要否定的假设', '研究假设', '备择假设'], answer: 1, explanation: '原假设(H0)通常是我们想要否定的假设，备择假设(H1)是我们想要支持的研究假设。' },
                    { question: '比较两组均值应该使用哪种检验？', options: ['卡方检验', 't检验', 'ANOVA', '回归分析'], answer: 1, explanation: 't检验用于比较两组数据的均值是否存在显著差异。' },
                    { question: '比较多组均值应该使用？', options: ['t检验', '卡方检验', 'ANOVA', '相关分析'], answer: 2, explanation: 'ANOVA（方差分析）用于比较三组或更多组的均值差异。' },
                    { question: 'p值表示？', options: ['效应大小', '结果偶然发生的概率', '样本量', '统计功效'], answer: 1, explanation: 'p值表示在原假设为真的情况下，观察到当前结果或更极端结果的概率。' }
                ]
            },
            {
                id: 'regression',
                title: '回归分析',
                duration: '3.5小时',
                theory: `## 回归分析\n\n回归分析用于研究变量之间的关系。\n\n### 简单线性回归\n\n预测一个因变量和一个自变量之间的线性关系。\n\n公式：Y = a + bX + ε\n\n### 多元线性回归\n\n包含多个自变量。\n\n公式：Y = a + b1*X1 + b2*X2 + ... + ε\n\n### 评估指标\n\n1. **R-squared**：模型解释的变异比例\n2. **p值**：系数的显著性\n3. **残差分析**：检查模型假设`,
                tips: [
                    '线性回归要求变量之间存在线性关系',
                    'R-squared越高不代表模型越好，可能过拟合',
                    '检查残差是否随机分布是模型诊断的重要步骤'
                ],
                code: `import numpy as np
import pandas as pd

# 模拟数据：销售预算 vs 销售额
sales_budget = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
sales_revenue = [15, 35, 40, 55, 70, 90, 100, 120, 140, 160]

# 创建DataFrame
df = pd.DataFrame({'budget': sales_budget, 'revenue': sales_revenue})

# 计算相关系数
correlation = df['budget'].corr(df['revenue'])
print(f"相关系数: {correlation:.4f}")

# 使用numpy进行简单线性回归
slope, intercept = np.polyfit(sales_budget, sales_revenue, 1)
print(f"回归方程: revenue = {intercept:.1f} + {slope:.2f} * budget")

# 预测
new_budget = [75, 85, 95]
for b in new_budget:
    prediction = intercept + slope * b
    print(f"预算: {b}万, 预测销售额: {prediction:.1f}万")`,
                exercises: [
                    { question: '评估回归模型拟合优度的常用指标是？', options: ['p值', 't统计量', 'R-squared', '标准差'], answer: 2, explanation: 'R-squared表示模型解释的变异比例，范围0-1，值越高表示拟合越好。' },
                    { question: '简单线性回归的公式是？', options: ['Y = aX', 'Y = a + bX', 'Y = a + bX + cX2', 'Y = abX'], answer: 1, explanation: '简单线性回归公式为Y = a + bX，其中a是截距，b是斜率。' },
                    { question: '相关系数的取值范围是？', options: ['0到1', '-1到1', '-100到100', '0到100'], answer: 1, explanation: '相关系数r的取值范围是[-1, 1]，表示变量之间线性关系的强度和方向。' },
                    { question: '正相关意味着？', options: ['X增大Y减小', 'X增大Y增大', 'X和Y没有关系', 'X和Y完全相同'], answer: 1, explanation: '正相关(r > 0)表示当X增大时，Y也倾向于增大。' },
                    { question: '残差分析的目的是？', options: ['计算均值', '检查模型假设', '计算标准差', '选择变量'], answer: 1, explanation: '残差分析用于检查回归模型的假设是否成立，如残差是否独立、正态分布等。' }
                ]
            }
        ]
    },
    'business-intelligence': {
        id: 'business-intelligence',
        title: '💼 商业智能与分析',
        description: '综合运用各种分析工具和方法，解决真实商业问题',
        level: '进阶',
        duration: '12小时',
        color: '#ee0979',
        gradient: 'linear-gradient(135deg, #ee0979 0%, #ff6a00 100%)',
        chapters: [
            {
                id: 'bi-intro',
                title: '商业智能概述',
                duration: '3小时',
                theory: `## 商业智能(BI)\n\n商业智能是一套技术和方法，用于收集、存储、分析业务数据以辅助决策。\n\n### BI 流程\n\n1. **数据收集**：从各业务系统采集数据\n2. **数据仓库**：集中存储，统一口径\n3. **数据分析**：运用各种分析方法\n4. **数据可视化**：制作报表和仪表板\n5. **决策支持**：为业务提供洞察\n\n### 常见分析场景\n\n- 销售分析：趋势、排名、区域对比\n- 客户分析：客户画像、流失预警\n- 产品分析：产品组合、定价策略\n- 运营分析：效率优化、成本控制`,
                tips: [
                    'BI的价值不在于工具，在于能否回答业务问题',
                    '建立统一的数据口径非常重要',
                    '好的BI项目，业务人员和数据人员必须紧密配合'
                ],
                code: `# 销售数据完整分析示例
import pandas as pd
import numpy as np

# 模拟销售数据
sales_data = {
    '日期': pd.date_range('2024-01-01', periods=100),
    '产品': np.random.choice(['A', 'B', 'C', 'D'], 100),
    '区域': np.random.choice(['华北', '华东', '华南', '西部'], 100),
    '销量': np.random.randint(10, 200, 100),
    '单价': np.random.randint(100, 1000, 100)
}
df = pd.DataFrame(sales_data)
df['销售额'] = df['销量'] * df['单价']

# 分析1: 月度销售趋势
df['月份'] = df['日期'].dt.month
monthly = df.groupby('月份')['销售额'].sum()
print("月度销售额:")
print(monthly)
print()

# 分析2: 产品销售排名
product_rank = df.groupby('产品')['销售额'].sum().sort_values(ascending=False)
print("产品销售排名:")
print(product_rank)
print()

# 分析3: 区域对比
region_analysis = df.groupby('区域').agg({
    '销售额': 'sum',
    '销量': 'sum'
}).sort_values('销售额', ascending=False)
print("区域销售分析:")
print(region_analysis)`,
                exercises: [
                    { question: '商业智能分析的最终目标是？', options: ['制作精美的图表', '支持业务决策', '使用最新技术', '展示数据分析能力'], answer: 1, explanation: '商业智能的最终目标是为业务决策提供数据支持，帮助企业做出更明智的决策。' },
                    { question: 'BI流程的第一步是？', options: ['数据分析', '数据收集', '数据可视化', '决策支持'], answer: 1, explanation: 'BI流程始于数据收集，从各业务系统采集数据是分析的基础。' },
                    { question: '数据仓库的作用是？', options: ['存储文件', '集中存储统一口径的数据', '运行应用程序', '展示报表'], answer: 1, explanation: '数据仓库用于集中存储企业各业务系统的数据，并建立统一的数据口径。' },
                    { question: '销售分析不包括以下哪项？', options: ['趋势分析', '客户画像', '区域对比', '产品排名'], answer: 1, explanation: '客户画像属于客户分析范畴，不是销售分析的直接内容。' },
                    { question: 'BI项目成功的关键是？', options: ['使用昂贵的工具', '业务人员和数据人员紧密配合', '制作漂亮的图表', '收集所有数据'], answer: 1, explanation: 'BI项目成功的关键是业务人员和数据人员的紧密配合，确保分析结果能够真正解决业务问题。' }
                ]
            },
            {
                id: 'dashboard',
                title: '数据仪表板设计',
                duration: '4小时',
                theory: `## 数据仪表板\n\n仪表板是关键指标的可视化展示，帮助管理者快速了解业务状况。\n\n### 仪表板设计原则\n\n1. **简洁明了**：一屏展示关键信息\n2. **突出重点**：核心指标放在显眼位置\n3. **可交互**：提供筛选和下钻功能\n4. **实时更新**：数据尽量保持最新\n\n### 常见组件\n\n- **核心指标卡片**：KPI数值展示\n- **趋势图**：折线图展示时间序列\n- **分布图**：条形图/饼图展示占比\n- **数据表**：详细数据展示\n- **过滤器**：时间、区域等筛选条件`,
                tips: [
                    '仪表板不是数据仓库，不能什么都展示',
                    '最关键的指标要放在左上角最显眼位置',
                    '颜色要克制，不要变成彩虹',
                    '理解用户角色：CEO和销售经理关注的指标完全不同'
                ],
                code: `# 数据仪表板数据准备示例
import pandas as pd
import numpy as np

# 模拟KPI数据
data = {
    '指标': ['总销售额', '订单数', '客户数', '平均客单价', '转化率', '复购率'],
    '当前值': [1250000, 3450, 1250, 362, 0.125, 0.45],
    '目标值': [1500000, 4000, 1500, 375, 0.15, 0.50],
    '同比': [0.15, 0.12, 0.08, 0.03, -0.02, 0.05],
    '单位': ['元', '单', '人', '元', '%', '%']
}
kpi_df = pd.DataFrame(data)

print("="*60)
print("📊 销售仪表板 - KPI概览")
print("="*60)

for _, row in kpi_df.iterrows():
    metric = row['指标']
    current = row['当前值']
    target = row['目标值']
    yoy = row['同比']
    unit = row['单位']
    
    rate = current / target
    status = "✅" if rate >= 0.9 else "⚠️" if rate >= 0.7 else "❌"
    
    if unit == '元':
        current_str = f"{current/10000:.1f}万"
        target_str = f"{target/10000:.1f}万"
    else:
        current_str = f"{current:.0f}"
        target_str = f"{target:.0f}"
    
    yoy_str = f"+{yoy*100:.1f}%" if yoy >= 0 else f"{yoy*100:.1f}%"
    
    print(f"{status} {metric}: {current_str} / 目标{target_str} (达成率{rate*100:.0f}%, 同比{yoy_str})")`,
                exercises: [
                    { question: '设计仪表板最重要的原则是？', options: ['使用最新技术', '简洁明了突出关键信息', '色彩丰富美观', '展示尽可能多的数据'], answer: 1, explanation: '仪表板的核心原则是简洁明了，让用户能够快速获取关键信息，而不是展示所有数据。' },
                    { question: '核心指标应该放在仪表板的哪个位置？', options: ['右下角', '左上角', '中间', '随便放'], answer: 1, explanation: '最关键的指标应该放在左上角最显眼的位置，符合人们的阅读习惯。' },
                    { question: '仪表板的颜色使用原则是？', options: ['越多越好看', '保持克制', '使用彩虹配色', '使用高饱和度颜色'], answer: 1, explanation: '仪表板颜色应该保持克制，避免过于花哨，确保信息清晰可读。' },
                    { question: '不同角色的用户关注的指标？', options: ['完全相同', '完全不同', '部分相同', '随机'], answer: 1, explanation: '不同角色的用户关注的指标差异很大，CEO关注整体业务指标，销售经理关注销售业绩。' },
                    { question: '仪表板应该具备什么功能？', options: ['只能看不能交互', '提供筛选和下钻功能', '只能显示图表', '只能显示文字'], answer: 1, explanation: '好的仪表板应该具备交互功能，允许用户筛选数据和下钻查看详情。' }
                ]
            },
            {
                id: 'rfm',
                title: 'RFM分析与客户分群',
                duration: '5小时',
                theory: `## RFM分析\n\nRFM是客户价值分析的经典方法：\n- **Recency**：最近一次消费时间\n- **Frequency**：消费频率\n- **Monetary**：消费金额\n\n### 客户分层\n\n根据RFM得分，可以将客户分为不同层级：\n- 高价值客户：最近消费、频繁消费、高消费\n- 潜力客户：有消费潜力但需要激活\n- 流失客户：长时间未消费\n\n### 应用场景\n\n- 个性化营销：针对不同层级客户制定不同策略\n- 客户挽留：识别即将流失的客户\n- 资源分配：优先服务高价值客户`,
                tips: [
                    'RFM分析特别适合有会员体系的电商业务',
                    '分析结果需要结合业务理解来解读',
                    '定期更新RFM得分，跟踪客户变化'
                ],
                code: `# RFM分析示例
import pandas as pd
import numpy as np

# 模拟客户订单数据
np.random.seed(42)
n_customers = 100
customer_ids = np.repeat(np.arange(n_customers), np.random.randint(1, 10, n_customers))
n_orders = len(customer_ids)

orders_df = pd.DataFrame({
    'customer_id': customer_ids,
    'order_date': np.random.choice(pd.date_range('2024-01-01', '2024-12-31'), n_orders),
    'amount': np.random.randint(50, 2000, n_orders)
})

# 计算RFM
current_date = pd.Timestamp('2024-12-31')
rfm = orders_df.groupby('customer_id').agg({
    'order_date': lambda x: (current_date - x.max()).days,
    'amount': ['count', 'sum']
}).round(0)
rfm.columns = ['R', 'F', 'M']

# 打分
rfm['R_score'] = pd.cut(rfm['R'], bins=5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_score'] = pd.cut(rfm['F'], bins=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_score'] = pd.cut(rfm['M'], bins=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['RFM_total'] = rfm[['R_score', 'F_score', 'M_score']].sum(axis=1)

# 客户分层
rfm['level'] = pd.cut(rfm['RFM_total'], bins=3, labels=['低价值', '中价值', '高价值'])

print("客户价值分布:")
print(rfm['level'].value_counts().sort_index())
print("\\nTOP 5高价值客户:")
print(rfm.nlargest(5, 'RFM_total'))`,
                exercises: [
                    { question: 'RFM分析中的R代表什么？', options: ['Revenue(收入)', 'Recency(最近)', 'Retention(留存)', 'Return(回报)'], answer: 1, explanation: 'R代表Recency（最近一次消费时间），时间越近得分越高。' },
                    { question: 'RFM分析中的F代表什么？', options: ['Frequency(频率)', 'Finance(财务)', 'Future(未来)', 'Feature(特征)'], answer: 0, explanation: 'F代表Frequency（消费频率），消费次数越多得分越高。' },
                    { question: 'RFM分析中的M代表什么？', options: ['Market(市场)', 'Margin(利润)', 'Monetary(金额)', 'Marketing(营销)'], answer: 2, explanation: 'M代表Monetary（消费金额），消费金额越高得分越高。' },
                    { question: '高价值客户的特征是？', options: ['消费时间久、频率低、金额少', '最近消费、频繁消费、高消费', '从未消费', '偶尔消费'], answer: 1, explanation: '高价值客户是指最近有消费、消费频率高、消费金额大的客户。' },
                    { question: 'RFM分析适合哪种业务？', options: ['制造业', '电商零售', '医疗行业', '教育行业'], answer: 1, explanation: 'RFM分析特别适合有会员体系和交易记录的电商零售业务。' }
                ]
            }
        ]
    }
};

// 项目数据
const projectsData = {
    'sales-analysis': {
        id: 'sales-analysis',
        title: '📈 电商销售数据分析',
        description: '分析销售趋势、识别爆款产品、发现客户购买行为模式',
        level: '初级',
        duration: '3小时',
        gradient: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)',
        dataset: 'sales_data',
        background: '某电商平台近一年的销售数据，包含订单信息、商品信息和客户信息。作为数据分析师，你需要帮助业务团队了解销售情况，发现业务机会。',
        goals: [
            '分析月度销售趋势，识别旺季和淡季',
            '找出销售额最高的Top 10产品',
            '分析不同地区的销售分布',
            '发现客户购买行为模式'
        ],
        tips: [
            '注意处理缺失值和异常订单，确保数据质量',
            '按月聚合分析趋势更清晰，可以使用 resample 方法',
            '使用分组聚合发现产品规律，groupby 是强大的工具'
        ],
        code: `import pandas as pd
import numpy as np

# 读取数据（在编辑器中运行时数据已加载到df变量）
# df = pd.read_csv('sales_data.csv')

print("=== 数据预览 ===")
print(df.head())

print("\\n=== 数据信息 ===")
print(f"共 {len(df)} 行，{len(df.columns)} 列")
print(f"列名: {', '.join(df.columns)}")

# 数据清洗
df = df.dropna()

# 计算销售额
df['销售额'] = df['数量'] * df['单价']

# 月度销售趋势
df['日期'] = pd.to_datetime(df['日期'])
monthly_sales = df.groupby(df['日期'].dt.month)['销售额'].sum()
print("\\n=== 月度销售额 ===")
print(monthly_sales)

# Top 10产品
top_products = df.groupby('产品')['销售额'].sum().sort_values(ascending=False).head(10)
print("\\n=== Top 10产品 ===")
print(top_products)

# 地区销售分布
region_sales = df.groupby('地区')['销售额'].sum().sort_values(ascending=False)
print("\\n=== 地区销售分布 ===")
print(region_sales)`,
        errors: [
            'KeyError: "订单金额" - 实际列名为"金额"',
            'ValueError: 日期格式不正确 - 需要转换为datetime',
            'TypeError: 字符串不能直接求和 - 需要转换为数值类型'
        ]
    },
    'customer-churn': {
        id: 'customer-churn',
        title: '👥 客户流失预测分析',
        description: '识别流失客户特征，建立预警机制',
        level: '中级',
        duration: '4小时',
        gradient: 'linear-gradient(135deg, #f2994a 0%, #f2c94c 100%)',
        dataset: 'customer_data',
        background: '某订阅制服务平台需要了解客户流失情况，通过数据分析识别高风险客户，并制定挽留策略。',
        goals: [
            '分析客户流失率和流失趋势',
            '识别流失客户的关键特征',
            '构建客户流失预警模型',
            '提出客户挽留建议'
        ],
        tips: [
            '流失率 = 流失客户数 / 总客户数',
            '可以使用逻辑回归或决策树进行预测',
            '特征工程是预测模型成败的关键'
        ],
        code: `import pandas as pd
import numpy as np

# 读取数据
# df = pd.read_csv('customer_data.csv')

print("=== 数据预览 ===")
print(df.head())

print("\\n=== 流失率 ===")
churn_counts = df['流失标记'].value_counts(normalize=True)
print(f"未流失客户: {churn_counts[0]:.1%}")
print(f"流失客户: {churn_counts[1]:.1%}")

# 特征分析
print("\\n=== 按流失状态分组 ===")
print(df.groupby('流失标记')[['年龄', '消费金额', '订单数']].mean())

# 计算客单价
df['客单价'] = df['消费金额'] / df['订单数']

# 流失与未流失客户对比
churned = df[df['流失标记'] == 1]
non_churned = df[df['流失标记'] == 0]

print("\\n=== 流失客户 vs 未流失客户 ===")
print(f"流失客户平均消费: {churned['消费金额'].mean():.0f}元")
print(f"未流失客户平均消费: {non_churned['消费金额'].mean():.0f}元")
print(f"流失客户平均订单数: {churned['订单数'].mean():.1f}单")
print(f"未流失客户平均订单数: {non_churned['订单数'].mean():.1f}单")

# 各地区流失率
print("\\n=== 各地区流失率 ===")
print(df.groupby('地区')['流失标记'].mean().sort_values(ascending=False))`,
        errors: [
            'KeyError: "is_churn" - 实际列名为"流失标记"',
            'ZeroDivisionError: 订单数为0时计算客单价出错',
            'ValueError: 日期格式不正确'
        ]
    },
    'inventory-analysis': {
        id: 'inventory-analysis',
        title: '📦 库存管理分析',
        description: '分析库存水平和销售预测，优化库存管理',
        level: '初级',
        duration: '2小时',
        gradient: 'linear-gradient(135deg, #3498db 0%, #9b59b6 100%)',
        dataset: 'inventory_data',
        background: '某电商平台需要优化库存管理，通过数据分析库存水平和销售预测，降低库存成本。',
        goals: [
            '分析库存水平趋势',
            '评估库存周转情况',
            '分析促销活动对销量的影响',
            '提出库存优化建议'
        ],
        tips: [
            '库存天数 = 当前库存 / 日均销量',
            '安全库存 = 日均销量 × 补货周期',
            '促销期间销量通常会显著增加'
        ],
        code: `import pandas as pd
import numpy as np

# 读取数据
# df = pd.read_csv('inventory_data.csv')

print("=== 数据预览 ===")
print(df.head())

print("\\n=== 产品库存概览 ===")
product_inventory = df.groupby('产品').agg({
    '库存水平': ['mean', 'min', 'max'],
    '销量': ['sum', 'mean']
})
print(product_inventory)

# 库存天数分析
df['日期'] = pd.to_datetime(df['日期'])
daily_sales = df.groupby(['产品', df['日期'].dt.date])['销量'].sum().reset_index()
daily_sales['avg_daily'] = daily_sales.groupby('产品')['销量'].transform('mean')

print("\\n=== 各产品日均销量 ===")
print(daily_sales.groupby('产品')['avg_daily'].first())

# 促销活动效果分析
promo_effect = df.groupby('促销活动')['销量'].agg(['mean', 'sum', 'count'])
print("\\n=== 促销活动效果 ===")
print(promo_effect)

# 库存预警
current_inventory = df.groupby('产品')['库存水平'].last()
avg_sales = df.groupby('产品')['销量'].mean()
inventory_days = current_inventory / avg_sales
print("\\n=== 当前库存可售天数 ===")
print(inventory_days.round(1))`,
        errors: [
            'KeyError: "stock_level" - 实际列名为"库存水平"',
            'TypeError: 日期列需要转换为datetime格式',
            'ValueError: 库存水平不能为负数'
        ]
    },
    'fraud-detection': {
        id: 'fraud-detection',
        title: '🔍 异常交易检测',
        description: '使用统计方法识别异常交易和欺诈行为',
        level: '中级',
        duration: '4小时',
        gradient: 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)',
        dataset: 'sales_data',
        background: '某支付平台需要检测异常交易，防止欺诈行为。你需要使用统计方法来识别可疑交易。',
        goals: [
            '分析交易金额分布，识别异常值',
            '使用IQR方法检测异常交易',
            '建立交易风险评分系统',
            '分析欺诈交易的时间模式'
        ],
        tips: [
            '异常值不一定是欺诈，需要结合业务判断',
            'IQR方法简单有效，是常用的异常检测方法',
            '时间维度的分析可以发现周期性的欺诈模式'
        ],
        code: `import pandas as pd
import numpy as np

# 模拟交易数据
np.random.seed(42)
n_transactions = 1000
amounts = np.random.normal(200, 100, n_transactions)
amounts = np.append(amounts, [5000, 6000, 7000, 8000, 9000])

df = pd.DataFrame({
    'transaction_id': range(len(amounts)),
    'amount': amounts.round(2),
    'hour': np.random.randint(0, 24, len(amounts)),
    'is_fraud': [0]*n_transactions + [1]*5
})

print("=== 交易数据概览 ===")
print(df['amount'].describe())

# 使用IQR方法检测异常值
Q1 = df['amount'].quantile(0.25)
Q3 = df['amount'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print(f"\\nIQR异常检测边界:")
print(f"下限: {lower_bound:.2f}元")
print(f"上限: {upper_bound:.2f}元")

# 标记异常交易
df['is_anomaly'] = (df['amount'] < lower_bound) | (df['amount'] > upper_bound)
anomalies = df[df['is_anomaly'] == True]

print(f"\\n异常交易数: {len(anomalies)} ({len(anomalies)/len(df)*100:.1f}%)")
print(f"异常交易金额范围: {anomalies['amount'].min():.0f} - {anomalies['amount'].max():.0f}元")

# 欺诈交易时间分析
print("\\n=== 欺诈交易时间分布 ===")
print(df[df['is_fraud'] == 1]['hour'].value_counts().sort_index())`,
        errors: [
            'RuntimeWarning: 标准差太大可能影响检测效果',
            'ValueError: 分位数计算出错 - 数据量太少',
            'TypeError: 需要确保金额列为数值类型'
        ]
    },
    'market-basket': {
        id: 'market-basket',
        title: '🛒 购物篮分析',
        description: '发现商品关联规则，优化商品陈列和推荐',
        level: '初级',
        duration: '2小时',
        gradient: 'linear-gradient(135deg, #27ae60 0%, #2ecc71 100%)',
        dataset: 'sales_data',
        background: '某零售超市希望了解顾客购买商品的关联规律，用于优化商品陈列、设计捆绑销售和推荐系统。',
        goals: [
            '找出最常被一起购买的商品组合',
            '计算商品之间的关联度',
            '使用Apriori算法发现关联规则',
            '提出商品陈列和促销建议'
        ],
        tips: [
            '关联规则的三个指标：支持度、置信度、提升度',
            '商品组合数量可能很大，需要设置合理的阈值',
            '结果需要结合业务常识进行筛选'
        ],
        code: `import pandas as pd
from itertools import combinations
from collections import Counter

# 模拟购物篮数据
np.random.seed(42)
products = ['牛奶', '面包', '鸡蛋', '水果', '蔬菜', '零食', '饮料', '肉类']
n_orders = 100

order_data = []
for order_id in range(n_orders):
    n_items = np.random.randint(2, 5)
    items = np.random.choice(products, n_items, replace=False)
    for item in items:
        order_data.append({'order_id': order_id, 'product': item})

df = pd.DataFrame(order_data)

print("=== 订单商品统计 ===")
items_per_order = df.groupby('order_id')['product'].count()
print(f"平均每单商品数: {items_per_order.mean():.1f}")
print(f"商品购买次数:")
print(df['product'].value_counts())

# 创建购物篮
baskets = df.groupby('order_id')['product'].apply(list).reset_index()

# 统计商品组合
pair_counts = Counter()
for items in baskets['product']:
    if len(items) >= 2:
        for pair in combinations(sorted(items), 2):
            pair_counts[pair] += 1

print("\\n=== Top 10商品组合 ===")
for (item1, item2), count in pair_counts.most_common(10):
    support = count / len(baskets)
    print(f"{item1} + {item2}: {count}次 (支持度: {support:.1%})")`,
        errors: [
            'MemoryError: 商品组合过多可能导致内存不足',
            'ValueError: 需要确保订单ID列正确',
            'KeyError: 商品名列名不正确'
        ]
    },
    'user-segmentation': {
        id: 'user-segmentation',
        title: '👤 用户画像与分群',
        description: '构建用户标签体系，实现精细化运营',
        level: '中级',
        duration: '4小时',
        gradient: 'linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%)',
        dataset: 'customer_data',
        background: '某互联网平台希望基于用户行为数据建立用户画像系统，用于精细化运营、精准营销和产品优化。',
        goals: [
            '分析用户基本属性分布',
            '构建用户行为标签体系',
            '进行用户分群和RFM分析',
            '设计用户分层运营策略'
        ],
        tips: [
            'RFM是经典的客户价值分析模型',
            '用户标签需要结合业务场景设计',
            '用户画像不是一成不变的，需要定期更新'
        ],
        code: `import pandas as pd
import numpy as np

# 模拟用户行为数据
np.random.seed(42)
n_users = 200

user_data = {
    'user_id': range(n_users),
    'age': np.random.randint(18, 60, n_users),
    'gender': np.random.choice(['男', '女'], n_users),
    'avg_spend': np.random.randint(50, 1000, n_users),
    'order_count': np.random.randint(1, 50, n_users),
    'last_active_days': np.random.randint(0, 90, n_users),
    'avg_session_time': np.random.randint(5, 120, n_users)
}

df = pd.DataFrame(user_data)

print("=== 用户数据概览 ===")
print(df.describe())

print("\\n=== 性别分布 ===")
print(df['gender'].value_counts())

print("\\n=== 年龄分布 ===")
age_bins = [18, 25, 35, 45, 60]
df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=['18-25', '26-35', '36-45', '46-60'])
print(df['age_group'].value_counts().sort_index())

# RFM简化版
df['R_score'] = pd.cut(df['last_active_days'], bins=5, labels=[5,4,3,2,1]).astype(int)
df['F_score'] = pd.cut(df['order_count'], bins=5, labels=[1,2,3,4,5]).astype(int)
df['M_score'] = pd.cut(df['avg_spend'], bins=5, labels=[1,2,3,4,5]).astype(int)
df['RFM_total'] = df[['R_score', 'F_score', 'M_score']].sum(axis=1)

df['level'] = pd.cut(df['RFM_total'], bins=3, labels=['低价值', '中价值', '高价值'])

print("\\n=== 用户价值分层 ===")
print(df['level'].value_counts())`,
        errors: [
            'ValueError: 分箱边界设置不合理',
            'TypeError: 需要确保数值列为数值类型',
            'KeyError: 列名拼写错误'
        ]
    },
    'price-optimization': {
        id: 'price-optimization',
        title: '💰 价格优化分析',
        description: '分析价格弹性，优化定价策略',
        level: '高级',
        duration: '5小时',
        gradient: 'linear-gradient(135deg, #f39c12 0%, #e67e22 100%)',
        dataset: 'sales_data',
        background: '某电商平台需要优化产品定价策略，通过分析历史价格和销量数据，找到最优价格点。',
        goals: [
            '分析价格与销量的关系',
            '计算价格弹性系数',
            '寻找最优价格点',
            '制定差异化定价策略'
        ],
        tips: [
            '价格弹性 = 销量变化率 / 价格变化率',
            '弹性大于1表示需求富有弹性',
            '需要考虑竞争对手价格'
        ],
        code: `import pandas as pd
import numpy as np

# 模拟价格销量数据
np.random.seed(42)
prices = np.linspace(50, 200, 30)
base_demand = 1000 - 5 * prices + np.random.normal(0, 50, 30)

df = pd.DataFrame({
    'price': prices.round(0),
    'sales': base_demand.round(0).astype(int),
    'cost': 40
})

df['revenue'] = df['price'] * df['sales']
df['profit'] = (df['price'] - df['cost']) * df['sales']

print("=== 价格销量数据 ===")
print(df.head())

# 计算价格弹性
df['price_change'] = df['price'].pct_change()
df['sales_change'] = df['sales'].pct_change()
df['elasticity'] = df['sales_change'] / df['price_change']

print("\\n=== 价格弹性分析 ===")
print(f"平均价格弹性: {df['elasticity'].mean():.2f}")
print(f"价格弹性范围: {df['elasticity'].min():.2f} 到 {df['elasticity'].max():.2f}")

# 寻找最大利润点
max_profit_idx = df['profit'].idxmax()
optimal_price = df.loc[max_profit_idx, 'price']
max_profit = df.loc[max_profit_idx, 'profit']

print(f"\\n=== 最优价格点 ===")
print(f"最优价格: {optimal_price:.0f}元")
print(f"最大利润: {max_profit:.0f}元")
print(f"对应销量: {df.loc[max_profit_idx, 'sales']:.0f}件")

# 利润随价格变化趋势
print("\\n=== 利润随价格变化 ===")
selected_prices = [80, 100, 120, 140, 160]
for p in selected_prices:
    profit = df[df['price'] == p]['profit'].values[0]
    print(f"价格 {p}元: 利润 {profit:.0f}元")`,
        errors: [
            'ZeroDivisionError: 价格变化为0时无法计算弹性',
            'ValueError: 需要确保销量为正数',
            'TypeError: 数据类型不正确'
        ]
    },
    'demand-forecast': {
        id: 'demand-forecast',
        title: '📈 需求预测分析',
        description: '使用时间序列分析预测未来需求',
        level: '高级',
        duration: '5小时',
        gradient: 'linear-gradient(135deg, #1abc9c 0%, #16a085 100%)',
        dataset: 'sales_data',
        background: '某零售企业需要预测未来销量，以便优化库存和采购计划。',
        goals: [
            '分析历史销售趋势',
            '识别季节性模式',
            '构建预测模型',
            '评估预测准确性'
        ],
        tips: [
            '时间序列分析需要足够的历史数据',
            '注意识别趋势和季节性',
            '使用多种方法交叉验证'
        ],
        code: `import pandas as pd
import numpy as np

# 模拟时间序列数据
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=365)
base_sales = 1000 + 5 * np.arange(365)  # 趋势
seasonal = 200 * np.sin(2 * np.pi * np.arange(365) / 30)  # 月度周期
noise = np.random.normal(0, 50, 365)

df = pd.DataFrame({
    'date': dates,
    'sales': (base_sales + seasonal + noise).round(0).astype(int)
})

print("=== 销售趋势数据 ===")
print(df.head())

# 分析月度趋势
df['month'] = df['date'].dt.month
monthly_avg = df.groupby('month')['sales'].mean()

print("\\n=== 月度平均销量 ===")
print(monthly_avg.round(0))

# 计算7天移动平均
df['ma7'] = df['sales'].rolling(7).mean()

# 简单预测：使用最近7天平均
last_7_avg = df['sales'].tail(7).mean()
print(f"\\n=== 简单预测 ===")
print(f"最近7天平均销量: {last_7_avg:.0f}")
print(f"下一天预测销量: {last_7_avg:.0f}")

# 趋势预测
x = np.arange(len(df))
slope, intercept = np.polyfit(x, df['sales'], 1)
trend_pred = intercept + slope * (len(df) + 7)
print(f"\\n=== 趋势预测 ===")
print(f"趋势方程: sales = {intercept:.0f} + {slope:.2f} * day")
print(f"7天后预测: {trend_pred:.0f}")`,
        errors: [
            'ValueError: 需要确保日期列为datetime格式',
            'RuntimeWarning: 数据中存在缺失值',
            'TypeError: 销量需要为数值类型'
        ]
    },
    'supply-chain': {
        id: 'supply-chain',
        title: '🔗 供应链分析',
        description: '优化供应链流程，降低成本',
        level: '中级',
        duration: '4小时',
        gradient: 'linear-gradient(135deg, #34495e 0%, #2c3e50 100%)',
        dataset: 'inventory_data',
        background: '某制造企业需要分析供应链数据，识别瓶颈环节，优化物流和库存管理。',
        goals: [
            '分析供应链各环节效率',
            '识别瓶颈环节',
            '优化库存策略',
            '降低物流成本'
        ],
        tips: [
            '供应链效率 = 产出 / 投入',
            '识别关键路径上的瓶颈',
            '考虑上下游协同'
        ],
        code: `import pandas as pd
import numpy as np

# 模拟供应链数据
suppliers = ['供应商A', '供应商B', '供应商C', '供应商D']
products = ['产品1', '产品2', '产品3']

supply_data = []
for supplier in suppliers:
    for product in products:
        for month in range(1, 13):
            supply_data.append({
                'supplier': supplier,
                'product': product,
                'month': month,
                'lead_time': np.random.randint(3, 15),
                'defect_rate': np.random.uniform(0.01, 0.1),
                'delivery_rate': np.random.uniform(0.9, 1.0),
                'cost': np.random.randint(100, 500)
            })

df = pd.DataFrame(supply_data)

print("=== 供应商表现概览 ===")
supplier_stats = df.groupby('supplier').agg({
    'lead_time': ['mean', 'std'],
    'defect_rate': 'mean',
    'delivery_rate': 'mean',
    'cost': 'mean'
})
print(supplier_stats.round(2))

print("\\n=== 各产品平均交付周期 ===")
product_lead = df.groupby('product')['lead_time'].mean().sort_values()
print(product_lead.round(1))

# 供应商评分
df['score'] = (1 - df['defect_rate']) * df['delivery_rate'] / df['lead_time'] * 100
top_supplier = df.groupby('supplier')['score'].mean().sort_values(ascending=False)

print("\\n=== 供应商综合评分 ===")
print(top_supplier.round(1))

# 月度表现趋势
monthly_performance = df.groupby('month')['delivery_rate'].mean()
print("\\n=== 月度交付率趋势 ===")
print(monthly_performance.round(2))`,
        errors: [
            'KeyError: 列名拼写错误',
            'ValueError: 需要确保数值列正确',
            'TypeError: 百分比需要转换为小数'
        ]
    },
    'marketing-analysis': {
        id: 'marketing-analysis',
        title: '📣 营销效果分析',
        description: '评估营销活动效果，优化营销预算分配',
        level: '中级',
        duration: '4小时',
        gradient: 'linear-gradient(135deg, #e91e63 0%, #c2185b 100%)',
        dataset: 'sales_data',
        background: '某企业需要评估不同营销渠道的效果，优化营销预算分配，提高ROI。',
        goals: [
            '分析各渠道营销效果',
            '计算ROI',
            '优化预算分配',
            '提出营销建议'
        ],
        tips: [
            'ROI = (收入 - 成本) / 成本 × 100%',
            '考虑长期效应和短期效应',
            'A/B测试是评估效果的好方法'
        ],
        code: `import pandas as pd
import numpy as np

# 模拟营销数据
channels = ['搜索广告', '社交媒体', '邮件营销', '线下活动', '联盟营销']
campaign_data = []

for channel in channels:
    for month in range(1, 7):
        spend = np.random.randint(5000, 50000)
        impressions = np.random.randint(10000, 500000)
        clicks = np.random.randint(500, 10000)
        conversions = np.random.randint(50, 500)
        revenue = conversions * np.random.randint(100, 500)
        
        campaign_data.append({
            'channel': channel,
            'month': month,
            'spend': spend,
            'impressions': impressions,
            'clicks': clicks,
            'conversions': conversions,
            'revenue': revenue
        })

df = pd.DataFrame(campaign_data)

print("=== 营销渠道数据 ===")
print(df.head())

# 计算关键指标
df['ctr'] = df['clicks'] / df['impressions']
df['cpc'] = df['spend'] / df['clicks']
df['cpa'] = df['spend'] / df['conversions']
df['roi'] = (df['revenue'] - df['spend']) / df['spend'] * 100

# 渠道效果对比
channel_stats = df.groupby('channel').agg({
    'spend': 'sum',
    'revenue': 'sum',
    'conversions': 'sum',
    'ctr': 'mean',
    'cpa': 'mean',
    'roi': 'mean'
}).round(2)

print("\\n=== 各渠道效果对比 ===")
print(channel_stats)

# 按ROI排序
print("\\n=== 渠道ROI排名 ===")
roi_rank = channel_stats['roi'].sort_values(ascending=False)
print(roi_rank)`,
        errors: [
            'ZeroDivisionError: 点击数为0时无法计算CPC',
            'ValueError: 需要确保数值列为数值类型',
            'KeyError: 列名拼写错误'
        ]
    }
};

// 徽章数据
const badgesData = {
    'first_code': { id: 'first_code', name: '🚀 代码初体验', desc: '第一次运行代码', icon: 'code' },
    'course_complete': { id: 'course_complete', name: '📚 课程完成', desc: '完成任意一门课程', icon: 'book' },
    'project_complete': { id: 'project_complete', name: '🎯 项目实战', desc: '完成任意一个项目', icon: 'target' },
    'assessment_pass': { id: 'assessment_pass', name: '🏆 通过测评', desc: '通过综合测评', icon: 'trophy' },
    'streak_7': { id: 'streak_7', name: '🔥 连续7天学习', desc: '连续学习7天', icon: 'flame' },
    'master_analyst': { id: 'master_analyst', name: '👑 分析大师', desc: '完成所有课程和项目', icon: 'crown' }
};

// 数据集数据
const datasetsData = {
    'sales_data': {
        id: 'sales_data',
        name: '销售数据分析',
        desc: '50条电商销售记录',
        file: 'datasets/sales_data.csv',
        columns: ['订单ID', '日期', '产品', '类别', '地区', '数量', '单价', '金额', '客户ID'],
        preview: [
            ['ORD001', '2024-01-05', '手机', '电子产品', '华北', 120, 3999, 479880, 'C001'],
            ['ORD002', '2024-01-06', '笔记本电脑', '电子产品', '华东', 85, 5999, 509915, 'C002'],
            ['ORD003', '2024-01-07', 'T恤', '服装', '华南', 200, 99, 19800, 'C003']
        ]
    },
    'customer_data': {
        id: 'customer_data',
        name: '客户行为数据',
        desc: '30位客户的行为数据',
        file: 'datasets/customer_data.csv',
        columns: ['客户ID', '注册日期', '地区', '年龄', '性别', '消费金额', '订单数', '上次购买', '流失标记'],
        preview: [
            ['C001', '2024-01-15', '华北', 28, '男', 12500, 12, '2024-12-20', 0],
            ['C002', '2024-02-20', '华东', 35, '女', 28000, 25, '2024-12-18', 0],
            ['C003', '2024-03-10', '华南', 42, '男', 8500, 8, '2024-11-05', 1]
        ]
    },
    'inventory_data': {
        id: 'inventory_data',
        name: '库存管理数据',
        desc: '4款产品10天库存数据',
        file: 'datasets/inventory_data.csv',
        columns: ['日期', '产品', '库存水平', '销售预测', '促销活动', '价格', '销量', '库存天数'],
        preview: [
            ['2024-01-01', '产品A', 500, 120, 0, 100, 115, 4.3],
            ['2024-01-02', '产品A', 385, 130, 1, 95, 180, 2.1],
            ['2024-01-03', '产品B', 800, 200, 0, 150, 190, 4.2]
        ]
    }
};