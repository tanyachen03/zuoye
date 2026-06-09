const COURSES_DATA = [
    {
        id: "python-basics",
        title: "Python基础入门",
        icon: "🐍",
        description: "从零开始掌握Python编程基础",
        difficulty: "入门",
        lessons: [
            {
                id: "1.1",
                title: "Python安装与环境配置",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "本节课将带你完成Python的安装和环境配置。Python可以在官网下载安装包，也可以使用Anaconda科学计算发行版。我们会介绍如何配置pip包管理器和IDE开发环境。",
                    codeExamples: [
                        {
                            title: "Python安装检查",
                            code: "# Windows系统\npython --version\npip --version\n\n# Linux/Mac系统\npython3 --version\npip3 --version"
                        },
                        {
                            title: "第一个Python程序",
                            code: "# 保存为 hello.py\nprint(\"Hello, World!\")\n\n# 运行\npython hello.py"
                        }
                    ],
                    tips: ["建议使用Anaconda，它预装了数据分析常用的库。", "建议使用VSCode或PyCharm作为开发工具。"],
                    commonErrors: ["安装时记得勾选Add Python to PATH。", "Windows系统可能需要重启电脑使环境变量生效。"]
                }
            },
            {
                id: "1.2",
                title: "变量与数据类型",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "变量是编程中最基本的概念之一。在Python中，我们使用变量来存储数据值。Python中的基本数据类型包括：整数（int）、浮点数（float）、字符串（str）、布尔值（bool）。",
                    codeExamples: [
                        {
                            title: "变量赋值基础",
                            code: "name = \"小明\"\nage = 25\nheight = 1.75\nis_student = True\nprint(\"姓名:\", name)\nprint(\"年龄:\", age)\nprint(\"类型:\", type(age))"
                        },
                        {
                            title: "类型转换",
                            code: "num_str = \"42\"\nnum_int = int(num_str)\nprint(\"字符串转整数:\", num_int + 10)\nage = 25\nage_str = str(age)\nprint(\"整数转字符串:\", \"年龄是 \" + age_str)"
                        }
                    ],
                    tips: ["Python是动态类型语言，变量类型会在赋值时自动确定。", "使用有意义的变量名可以让代码更易读。"],
                    commonErrors: ["变量名以数字开头会导致SyntaxError。", "字符串引号不匹配会导致SyntaxError。"]
                }
            },
            {
                id: "1.3",
                title: "条件判断if-else",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "条件判断是程序控制流的基础。Python使用if、elif、else关键字来实现条件判断。注意Python使用缩进而不是大括号来定义代码块。",
                    codeExamples: [
                        {
                            title: "基础if语句",
                            code: "age = 18\nif age >= 18:\n    print(\"已成年\")\nelif age >= 12:\n    print(\"青少年\")\nelse:\n    print(\"儿童\")"
                        },
                        {
                            title: "复合条件判断",
                            code: "score = 85\nhas_passed = score >= 60\nis_excellent = score >= 90\n\nif has_passed and is_excellent:\n    print(\"优秀\")\nelif has_passed:\n    print(\"及格\")\nelse:\n    print(\"不及格\")"
                        }
                    ],
                    tips: ["使用and、or、not可以进行复合条件判断。", "三元表达式可以让代码更简洁：result = '及格' if score >= 60 else '不及格'。"],
                    commonErrors: ["if语句后必须加冒号:。", "忘记缩进会导致IndentationError。"]
                }
            },
            {
                id: "1.4",
                title: "循环语句for/while",
                duration: "25分钟",
                type: "图文",
                content: {
                    text: "循环语句允许我们重复执行代码块。Python中有两种循环：for循环用于遍历序列，while循环在条件为真时重复执行。break和continue用于控制循环流程。",
                    codeExamples: [
                        {
                            title: "for循环遍历",
                            code: "# 遍历列表\nfruits = [\"苹果\", \"香蕉\", \"橙子\"]\nfor fruit in fruits:\n    print(fruit)\n\n# 使用range函数\nfor i in range(5):\n    print(f\"第{i}次循环\")"
                        },
                        {
                            title: "while循环",
                            code: "count = 0\nwhile count < 5:\n    print(count)\n    count += 1\n\n# 循环控制\nfor i in range(10):\n    if i == 5:\n        break  # 提前退出\n    if i % 2 == 0:\n        continue  # 跳过偶数\n    print(i)"
                        }
                    ],
                    tips: ["range(5)生成0-4，range(1,5)生成1-4。", "列表推导式是处理列表的简洁方式。"],
                    commonErrors: ["while循环要确保有退出条件，否则会无限循环。", "for循环中的变量在循环结束后仍然存在。"]
                }
            },
            {
                id: "1.5",
                title: "列表与元组",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "列表和元组是Python中最常用的数据结构。列表用方括号[]创建，是可变的；元组用圆括号()创建，是不可变的，适合存储不变的数据。",
                    codeExamples: [
                        {
                            title: "列表操作",
                            code: "fruits = [\"苹果\", \"香蕉\", \"橙子\"]\nprint(\"水果:\", fruits)\nprint(\"第一个:\", fruits[0])\nfruits[0] = \"草莓\"\nfruits.append(\"西瓜\")\nprint(\"修改后:\", fruits)\nprint(\"长度:\", len(fruits))"
                        },
                        {
                            title: "列表切片与元组",
                            code: "# 列表切片\nnumbers = [0, 1, 2, 3, 4, 5]\nprint(\"前三个:\", numbers[:3])\nprint(\"后两个:\", numbers[-2:])\nprint(\"间隔:\", numbers[::2])\n\n# 元组（不可变）\npoint = (10, 20)\nx, y = point\nprint(f\"坐标: ({x}, {y})\")"
                        }
                    ],
                    tips: ["列表切片语法：[start:end:step]。", "元组可用于字典的键，因为不可变。"],
                    commonErrors: ["列表切片超出范围不会报错，会返回空列表。", "元组是不可变的，不能修改元素。"]
                }
            },
            {
                id: "1.6",
                title: "字典与集合",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "字典用花括号{}存储键值对，通过键快速查找值，查找效率高。集合也是用花括号{}，但无序且不重复，适合去重和集合运算。",
                    codeExamples: [
                        {
                            title: "字典操作",
                            code: "student = {\n    \"name\": \"小明\",\n    \"age\": 18,\n    \"score\": 95\n}\nprint(\"姓名:\", student[\"name\"])\nstudent[\"age\"] = 19\nstudent[\"city\"] = \"北京\"\nprint(\"所有键:\", student.keys())\nprint(\"所有值:\", student.values())"
                        },
                        {
                            title: "集合操作",
                            code: "set1 = {1, 2, 3, 4}\nset2 = {3, 4, 5, 6}\n\nprint(\"交集:\", set1 & set2)\nprint(\"并集:\", set1 | set2)\nprint(\"差集:\", set1 - set2)\nprint(\"对称差:\", set1 ^ set2)\n\n# 去重\nnumbers = [1, 2, 2, 3, 3, 3]\nunique = list(set(numbers))\nprint(\"去重:\", unique)"
                        }
                    ],
                    tips: ["字典的键必须是可哈希的（不可变类型）。", "使用set()可以将列表快速去重。"],
                    commonErrors: ["字典的键不能重复，后者会覆盖前者。", "集合不支持索引访问。"]
                }
            },
            {
                id: "1.7",
                title: "函数定义与调用",
                duration: "25分钟",
                type: "图文",
                content: {
                    text: "函数是组织代码的基本单元，可以提高代码的复用性。Python使用def关键字定义函数，支持默认参数、可变参数、关键字参数等高级特性。",
                    codeExamples: [
                        {
                            title: "基础函数定义",
                            code: "def greet(name):\n    \"\"\"问候函数\"\"\"\n    return f\"你好，{name}！\"\n\nprint(greet(\"小明\"))\n\ndef add(a, b=10):\n    \"\"\"带默认参数的函数\"\"\"\n    return a + b\n\nprint(add(5))\nprint(add(5, 3))"
                        },
                        {
                            title: "可变参数函数",
                            code: "def sum_all(*args):\n    \"\"\"可变参数函数\"\"\"\n    total = 0\n    for num in args:\n        total += num\n    return total\n\nprint(sum_all(1, 2, 3, 4, 5))\n\ndef print_info(**kwargs):\n    \"\"\"关键字参数函数\"\"\"\n    for key, value in kwargs.items():\n        print(f\"{key}: {value}\")\n\nprint_info(name=\"小明\", age=18)"
                        }
                    ],
                    tips: ["使用文档字符串（三引号）来描述函数功能。", "函数可以返回多个值，实际上返回的是元组。"],
                    commonErrors: ["函数定义后必须调用才能执行。", "默认参数必须是不可变类型。"]
                }
            },
            {
                id: "1.8",
                title: "模块与包导入",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "模块是包含Python代码的文件，包是包含多个模块的目录。使用import语句可以导入模块或模块中的特定函数/类。Python标准库和第三方库提供了丰富的功能。",
                    codeExamples: [
                        {
                            title: "导入模块",
                            code: "import math\nprint(math.pi)\nprint(math.sqrt(16))\n\nimport random\nprint(random.randint(1, 10))\nprint(random.choice([\"苹果\", \"香蕉\", \"橙子\"]))"
                        },
                        {
                            title: "导入特定函数",
                            code: "from datetime import datetime\nnow = datetime.now()\nprint(now.strftime(\"%Y-%m-%d %H:%M:%S\"))\n\nfrom statistics import mean, median\nscores = [90, 85, 92, 88, 95]\nprint(\"平均分:\", mean(scores))\nprint(\"中位数:\", median(scores))"
                        }
                    ],
                    tips: ["使用as给模块或函数起别名可以简化代码。", "第三方库使用pip install安装。"],
                    commonErrors: ["导入的模块名拼写错误会导致ImportError。", "避免使用from module import *，可能导致命名冲突。"]
                }
            }
        ]
    },
    {
        id: "pandas-intro",
        title: "Pandas入门",
        icon: "📊",
        description: "掌握数据分析核心库Pandas",
        difficulty: "入门",
        lessons: [
            {
                id: "2.1",
                title: "Pandas安装与Series",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "Pandas是Python数据分析的核心库。Series是Pandas的基本数据结构，类似于一维数组，由索引和值组成。本节学习Series的创建和基本操作。",
                    codeExamples: [
                        {
                            title: "安装Pandas",
                            code: "pip install pandas\n\n# 验证安装\nimport pandas as pd\nprint(pd.__version__)"
                        },
                        {
                            title: "创建Series",
                            code: "import pandas as pd\n\n# 从列表创建\ns = pd.Series([1, 3, 5, 7, 9])\nprint(s)\n\n# 指定索引\ns = pd.Series([90, 85, 92], index=['语文', '数学', '英语'])\nprint(s)\nprint(\"数学成绩:\", s['数学'])"
                        }
                    ],
                    tips: ["Series类似于带索引的列。", "可以使用.values获取底层NumPy数组。"],
                    commonErrors: ["Series索引必须是可哈希的。", "Series和列表的索引不同，Series支持自定义索引。"]
                }
            },
            {
                id: "2.2",
                title: "DataFrame创建与查看",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "DataFrame是Pandas最常用的数据结构，类似于二维表格，由行索引和列名组成。本节学习如何创建DataFrame以及查看数据的基本方法。",
                    codeExamples: [
                        {
                            title: "创建DataFrame",
                            code: "import pandas as pd\n\n# 从字典创建\ndata = {\n    '姓名': ['小明', '小红', '小刚'],\n    '年龄': [18, 17, 19],\n    '分数': [92, 88, 95]\n}\ndf = pd.DataFrame(data)\nprint(df)\n\n# 从列表的字典创建\ndata = [\n    {'姓名': '小明', '年龄': 18},\n    {'姓名': '小红', '年龄': 17}\n]\ndf = pd.DataFrame(data)"
                        },
                        {
                            title: "查看数据",
                            code: "import pandas as pd\ndf = pd.read_csv('data.csv')\n\n# 查看前几行\nprint(df.head())\nprint(df.head(10))\n\n# 查看后几行\nprint(df.tail())\n\n# 查看基本信息\nprint(df.info())\nprint(df.describe())\nprint(df.shape)\nprint(df.columns)"
                        }
                    ],
                    tips: ["head()默认显示前5行，tail()显示后5行。", "describe()只显示数值列的统计信息。"],
                    commonErrors: ["读取CSV时要确保文件路径正确。", "列名区分大小写。"]
                }
            },
            {
                id: "2.3",
                title: "数据读取与写入",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "Pandas支持多种数据格式的读取和写入，包括CSV、Excel、JSON、SQL等。本节学习常用的数据读写方法。",
                    codeExamples: [
                        {
                            title: "读取数据",
                            code: "import pandas as pd\n\n# 读取CSV\ndf = pd.read_csv('data.csv')\ndf = pd.read_csv('data.csv', encoding='utf-8')\ndf = pd.read_csv('data.csv', sep='\\t')  # Tab分隔\n\n# 读取Excel\ndf = pd.read_excel('data.xlsx', sheet_name='Sheet1')\n\n# 读取JSON\ndf = pd.read_json('data.json')"
                        },
                        {
                            title: "写入数据",
                            code: "import pandas as pd\n\ndf = pd.DataFrame({\n    '姓名': ['小明', '小红'],\n    '分数': [92, 88]\n})\n\n# 写入CSV\ndf.to_csv('output.csv', index=False)\n\n# 写入Excel\ndf.to_excel('output.xlsx', index=False)\n\n# 写入JSON\ndf.to_json('output.json', force_ascii=False)"
                        }
                    ],
                    tips: ["read_csv的index_col参数可以指定索引列。", "写入CSV时设置index=False不保存行索引。"],
                    commonErrors: ["中文文件要注意编码格式。", "读取时列名要与实际文件一致。"]
                }
            },
            {
                id: "2.4",
                title: "数据筛选与过滤",
                duration: "25分钟",
                type: "图文",
                content: {
                    text: "数据筛选是数据分析的基础操作。Pandas提供了强大的数据选择功能，包括按标签选择、按位置选择、按条件过滤等。",
                    codeExamples: [
                        {
                            title: "选择列和行",
                            code: "import pandas as pd\ndf = pd.DataFrame({\n    '姓名': ['小明', '小红', '小刚'],\n    '年龄': [18, 17, 19],\n    '分数': [92, 88, 95]\n})\n\n# 选择单列\nnames = df['姓名']\n\n# 选择多列\nsubset = df[['姓名', '分数']]\n\n# 选择行\nprint(df.loc[0])  # 按索引\nprint(df.iloc[0:2])  # 按位置"
                        },
                        {
                            title: "条件过滤",
                            code: "import pandas as pd\ndf = pd.DataFrame({\n    '姓名': ['小明', '小红', '小刚'],\n    '分数': [92, 88, 95]\n})\n\n# 单条件\nhigh_scores = df[df['分数'] >= 90]\n\n# 多条件\nselected = df[(df['分数'] >= 90) & (df['分数'] < 95)]\n\n# 使用query\nresult = df.query('分数 >= 90 and 分数 < 95')\n\n# 字符串过滤\ndf[df['姓名'].str.contains('小')]"
                        }
                    ],
                    tips: ["条件表达式要加括号，避免运算符优先级问题。", "使用query()方法可以让条件表达式更易读。"],
                    commonErrors: ["&和|是按位运算符，不是逻辑运算符。", "使用AND和OR会报错。"]
                }
            },
            {
                id: "2.5",
                title: "缺失值处理",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "缺失值是真实数据中常见的问题。Pandas使用NaN表示缺失值，提供了isnull()、fillna()、dropna()等方法处理缺失值。",
                    codeExamples: [
                        {
                            title: "检测缺失值",
                            code: "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'A': [1, 2, np.nan, 4],\n    'B': [5, np.nan, 7, 8],\n    'C': [9, 10, 11, 12]\n})\n\n# 检测缺失值\nprint(df.isnull())\nprint(df.isnull().sum())  # 每列缺失值数量\nprint(df.isnull().sum().sum())  # 总缺失值数量"
                        },
                        {
                            title: "处理缺失值",
                            code: "# 删除缺失值\ndf_clean = df.dropna()\ndf_clean = df.dropna(axis=1)  # 删除有缺失值的列\ndf_clean = df.dropna(how='all')  # 只删除全为NaN的行\n\n# 填充缺失值\ndf_filled = df.fillna(0)  # 用0填充\ndf_filled = df.fillna(df.mean())  # 用均值填充\ndf_filled = df.fillna(method='ffill')  # 前向填充\ndf_filled = df.fillna(method='bfill')  # 后向填充"
                        }
                    ],
                    tips: ["fillna()可以使用字典为不同列填充不同的值。", "插值方法可以用interpolate()进行线性插值。"],
                    commonErrors: ["直接删除缺失值可能丢失重要信息。", "用均值填充会受异常值影响。"]
                }
            },
            {
                id: "2.6",
                title: "分组聚合groupby",
                duration: "25分钟",
                type: "图文",
                content: {
                    text: "groupby是Pandas强大的数据分析工具，用于将数据按一个或多个列分组，然后对每个组进行聚合计算，如求和、计数、平均值等。",
                    codeExamples: [
                        {
                            title: "基础分组聚合",
                            code: "import pandas as pd\n\ndf = pd.DataFrame({\n    '班级': ['一班', '一班', '二班', '二班'],\n    '姓名': ['小明', '小红', '小刚', '小丽'],\n    '分数': [92, 88, 95, 90]\n})\n\n# 按班级分组求平均分\nclass_avg = df.groupby('班级')['分数'].mean()\nprint(class_avg)\n\n# 按班级分组并统计\nstats = df.groupby('班级').agg({\n    '分数': ['mean', 'sum', 'count']\n})"
                        },
                        {
                            title: "多级分组",
                            code: "import pandas as pd\n\ndf = pd.DataFrame({\n    '班级': ['一班', '一班', '二班', '二班'],\n    '性别': ['男', '女', '男', '女'],\n    '分数': [92, 88, 95, 90]\n})\n\n# 多级分组\nresult = df.groupby(['班级', '性别'])['分数'].mean()\nprint(result)\n\n# 透视表\npivot = pd.pivot_table(df, \n    values='分数', \n    index='班级', \n    columns='性别', \n    aggfunc='mean'\n)"
                        }
                    ],
                    tips: ["agg()可以同时使用多个聚合函数。", "transform()返回与原数据同样大小的结果。"],
                    commonErrors: ["分组键必须是列名或列名列表。", "分组后忘记选择要聚合的列。"]
                }
            }
        ]
    },
    {
        id: "data-cleaning",
        title: "数据清洗",
        icon: "🧹",
        description: "学习数据预处理与清洗技术",
        difficulty: "入门",
        lessons: [
            {
                id: "3.1",
                title: "缺失值识别与统计",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "数据清洗是数据分析的第一步。缺失值是最常见的数据问题之一。本节学习如何识别和统计缺失值。",
                    codeExamples: [
                        {
                            title: "缺失值检测",
                            code: "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'A': [1, 2, np.nan, 4, np.nan],\n    'B': [5, np.nan, 7, np.nan, 10],\n    'C': [9, 10, 11, 12, 13]\n})\n\n# 每列缺失值数量\nprint(df.isnull().sum())\n\n# 缺失值比例\nprint(df.isnull().sum() / len(df) * 100)\n\n# 可视化缺失值\nprint(df.isnull().sum(axis=1))  # 每行缺失值数量"
                        },
                        {
                            title: "缺失值模式分析",
                            code: "# 判断缺失是否随机\nprint(df.notnull().sum())\n\n# 查看缺失模式\nprint(df[df.isnull().any(axis=1)])  # 包含缺失值的行\n\n# 相关性分析缺失\nprint(df.isnull().corr())"
                        }
                    ],
                    tips: ["缺失比例超过30%的列可能要考虑删除。", "分析缺失模式可以帮助选择合适的填充方法。"],
                    commonErrors: ["NaN和0是不同的，0是有效值。", "字符串'NA'不会自动识别为NaN。"]
                }
            },
            {
                id: "3.2",
                title: "fillna填充方法",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "fillna()方法提供了多种填充缺失值的策略，包括固定值、前向填充、后向填充、统计值填充等。选择合适的方法取决于数据特征。",
                    codeExamples: [
                        {
                            title: "固定值填充",
                            code: "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'A': [1, 2, np.nan, 4, 5],\n    'B': [5, np.nan, 7, 8, 10]\n})\n\n# 用固定值填充\ndf_filled = df.fillna(0)\n\n# 用指定值填充不同列\ndf_filled = df.fillna({'A': 0, 'B': -1})\n\n# 用均值填充\ndf_filled = df.fillna(df.mean())\n\n# 用中位数填充\ndf_filled = df.fillna(df.median())"
                        },
                        {
                            title: "插值填充",
                            code: "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'A': [1, 2, np.nan, 4, 5, 6, np.nan, 8]\n})\n\n# 线性插值\ndf_interpolated = df.interpolate()\n\n# 前向填充（用前面的值填充）\ndf_ffill = df.fillna(method='ffill')\n\n# 后向填充（用后面的值填充）\ndf_bfill = df.fillna(method='bfill')\n\n# 限制填充数量\ndf_limited = df.interpolate(limit=1)"
                        }
                    ],
                    tips: ["线性插值假设数据是线性变化的。", "前向填充适用于时间序列数据。"],
                    commonErrors: ["fillna()默认返回新DataFrame，不修改原数据。", "使用前向填充时，开头的NaN无法填充。"]
                }
            },
            {
                id: "3.3",
                title: "dropna删除缺失值",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "当缺失值无法有效填充或缺失比例过高时，删除是备选方案。dropna()提供了灵活的删除策略，可以按行或按列删除。",
                    codeExamples: [
                        {
                            title: "按行删除",
                            code: "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    'A': [1, 2, np.nan, 4],\n    'B': [5, 6, 7, 8],\n    'C': [9, np.nan, 11, 12]\n})\n\n# 删除包含缺失值的行\ndf_clean = df.dropna()\n\n# 只删除某列有缺失值的行\ndf_clean = df.dropna(subset=['A'])\n\n# 只删除所有列都是缺失值的行\ndf_clean = df.dropna(how='all')\n\n# 删除缺失值超过指定数量的行\ndf_clean = df.dropna(thresh=2)  # 至少2个非空值"
                        },
                        {
                            title: "按列删除",
                            code: "# 删除包含缺失值的列\ndf_clean = df.dropna(axis=1)\n\n# 只删除某列有缺失值的列\ndf_clean = df.dropna(axis=1, subset=['A'])\n\n# 删除缺失值比例超过阈值的列\nthreshold = 0.5\ncols_to_drop = df.columns[df.isnull().sum() / len(df) > threshold]\ndf_clean = df.drop(columns=cols_to_drop)"
                        }
                    ],
                    tips: ["删除前要考虑数据量是否足够。", "优先删除缺失比例高的列。"],
                    commonErrors: ["dropna()默认按行删除。", "删除操作是不可逆的，要谨慎。"]
                }
            },
            {
                id: "3.4",
                title: "重复值检测与删除",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "重复数据会导致分析结果偏差。Pandas提供了检测和删除重复值的方法，可以基于全部列或特定列进行去重。",
                    codeExamples: [
                        {
                            title: "检测重复值",
                            code: "import pandas as pd\n\ndf = pd.DataFrame({\n    '姓名': ['小明', '小红', '小明', '小刚'],\n    '年龄': [18, 17, 18, 19],\n    '城市': ['北京', '上海', '北京', '广州']\n})\n\n# 检测完全重复的行\nprint(df.duplicated())\n\n# 统计重复行数\nprint(df.duplicated().sum())\n\n# 显示所有重复的行\nprint(df[df.duplicated(keep=False)])"
                        },
                        {
                            title: "删除重复值",
                            code: "# 删除重复行（保留第一行）\ndf_clean = df.drop_duplicates()\n\n# 删除重复行（保留最后一行）\ndf_clean = df.drop_duplicates(keep='last')\n\n# 基于特定列删除重复\ndf_clean = df.drop_duplicates(subset=['姓名'])\n\n# 基于多列删除重复\ndf_clean = df.drop_duplicates(subset=['姓名', '年龄'])\n\n# 删除后查看\nprint(df_clean)"
                        }
                    ],
                    tips: ["keep=False会标记所有重复行。", "先排序再删除可以控制保留哪一行。"],
                    commonErrors: ["默认保留第一条重复记录。", "删除重复会改变DataFrame的索引。"]
                }
            },
            {
                id: "3.5",
                title: "异常值识别",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "异常值是偏离正常范围的数据点，可能是测量错误或真实异常值。常用方法包括IQR（四分位距）和Z-score（标准分数）来识别异常值。",
                    codeExamples: [
                        {
                            title: "基于IQR识别",
                            code: "import pandas as pd\nimport numpy as np\n\ndf = pd.DataFrame({\n    '分数': [85, 90, 88, 92, 95, 100, 150, 88, 91]\n})\n\n# 计算IQR\nQ1 = df['分数'].quantile(0.25)\nQ3 = df['分数'].quantile(0.75)\nIQR = Q3 - Q1\n\n# 定义异常值边界\nlower = Q1 - 1.5 * IQR\nupper = Q3 + 1.5 * IQR\n\n# 识别异常值\noutliers = df[(df['分数'] < lower) | (df['分数'] > upper)]\nprint(f\"异常值: {outliers['分数'].values}\")\nprint(f\"正常范围: [{lower}, {upper}]\")"
                        },
                        {
                            title: "基于Z-score识别",
                            code: "import pandas as pd\nimport numpy as np\nfrom scipy import stats\n\ndf = pd.DataFrame({\n    '分数': [85, 90, 88, 92, 95, 100, 150, 88, 91]\n})\n\n# 计算Z-score\nz_scores = np.abs(stats.zscore(df['分数']))\n\n# 识别异常值（阈值通常为3）\noutliers = df[z_scores > 3]\nprint(f\"异常值: {outliers['分数'].values}\")\n\n# 基于Z-score过滤\ndf_clean = df[z_scores <= 3]"
                        }
                    ],
                    tips: ["IQR方法适合非正态分布数据。", "Z-score假设数据近似正态分布。"],
                    commonErrors: ["异常值不一定是错误的。", "不同业务场景选择不同的阈值。"]
                }
            },
            {
                id: "3.6",
                title: "数据类型转换",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "正确的数据类型是数据分析的基础。常见类型包括整数、浮点数、字符串、日期时间、分类数据等。本节学习数据类型转换方法。",
                    codeExamples: [
                        {
                            title: "查看和转换数据类型",
                            code: "import pandas as pd\n\ndf = pd.DataFrame({\n    '整数列': ['1', '2', '3'],\n    '浮点列': ['1.5', '2.5', '3.5'],\n    '日期列': ['2024-01-01', '2024-01-02', '2024-01-03']\n})\n\n# 查看数据类型\nprint(df.dtypes)\n\n# 转换为整数\ndf['整数列'] = df['整数列'].astype(int)\n\n# 转换为浮点数\ndf['浮点列'] = df['浮点列'].astype(float)\n\n# 转换为日期\ndf['日期列'] = pd.to_datetime(df['日期列'])"
                        },
                        {
                            title: "分类数据和字符串",
                            code: "import pandas as pd\n\ndf = pd.DataFrame({\n    '城市': ['北京', '上海', '北京', '广州'],\n    '温度': ['25度', '28度', '26度', '27度']\n})\n\n# 转换为分类数据（节省内存）\ndf['城市'] = df['城市'].astype('category')\n\n# 清理字符串并提取数字\ndf['温度数值'] = df['温度'].str.replace('度', '').astype(int)\n\n# 处理货币格式\ndf['价格'] = ['$100', '$200', '$300']\ndf['价格数值'] = df['价格'].str.replace('$', '').astype(float)"
                        }
                    ],
                    tips: ["分类数据类型可以节省内存。", "处理前先备份原始数据。"],
                    commonErrors: ["astype()转换失败会抛出异常。", "日期格式不统一时要用pd.to_datetime()的format参数。"]
                }
            },
            {
                id: "3.7",
                title: "数据标准化与归一化",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "标准化和归一化是特征工程的重要步骤。标准化将数据转换为均值为0、标准差为1的分布；归一化将数据缩放到指定范围（通常是0-1）。",
                    codeExamples: [
                        {
                            title: "Min-Max归一化",
                            code: "import pandas as pd\nfrom sklearn.preprocessing import MinMaxScaler\n\ndf = pd.DataFrame({\n    '分数': [60, 75, 80, 95, 70]\n})\n\n# Min-Max归一化到0-1\nscaler = MinMaxScaler()\ndf['分数_归一化'] = scaler.fit_transform(df[['分数']])\n\n# 手动实现\nmin_val = df['分数'].min()\nmax_val = df['分数'].max()\ndf['分数_归一化'] = (df['分数'] - min_val) / (max_val - min_val)"
                        },
                        {
                            title: "Z-score标准化",
                            code: "import pandas as pd\nfrom sklearn.preprocessing import StandardScaler\n\ndf = pd.DataFrame({\n    '分数': [60, 75, 80, 95, 70]\n})\n\n# Z-score标准化\nscaler = StandardScaler()\ndf['分数_标准化'] = scaler.fit_transform(df[['分数']])\n\n# 手动实现\nmean_val = df['分数'].mean()\nstd_val = df['分数'].std()\ndf['分数_标准化'] = (df['分数'] - mean_val) / std_val"
                        }
                    ],
                    tips: ["归一化适用于有明确边界的场景。", "标准化适用于没有边界但要求正态分布的场景。"],
                    commonErrors: ["训练集和测试集要使用相同的scaler。", "树模型通常不需要标准化。"]
                }
            }
        ]
    },
    {
        id: "data-visualization",
        title: "数据可视化",
        icon: "📈",
        description: "掌握数据可视化技术",
        difficulty: "入门",
        lessons: [
            {
                id: "4.1",
                title: "matplotlib基础绘图",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "matplotlib是Python最基础的绘图库，几乎能绘制所有类型的图表。本节学习matplotlib的基本概念和简单绘图方法。",
                    codeExamples: [
                        {
                            title: "matplotlib基本使用",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 基本绘图\nplt.plot([1, 2, 3, 4], [1, 4, 9, 16])\nplt.show()\n\n# 使用numpy生成数据\nx = np.linspace(0, 2*np.pi, 100)\ny = np.sin(x)\nplt.plot(x, y)\nplt.title('正弦函数')\nplt.xlabel('x轴')\nplt.ylabel('y轴')\nplt.grid(True)\nplt.show()"
                        },
                        {
                            title: "面向对象绘图",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 创建画布和坐标轴\nfig, ax = plt.subplots(figsize=(8, 6))\n\n# 绑定数据\nx = np.linspace(0, 10, 100)\ny = np.cos(x)\n\n# 绘图\nax.plot(x, y, 'b-', linewidth=2, label='cos(x)')\nax.set_title('余弦函数', fontsize=16)\nax.set_xlabel('X', fontsize=12)\nax.set_ylabel('Y', fontsize=12)\nax.legend()\nax.grid(True, alpha=0.3)\n\nplt.tight_layout()\nplt.show()"
                        }
                    ],
                    tips: ["使用中文时先设置中文字体。", "figsize参数可以控制图像大小。"],
                    commonErrors: ["忘记调用plt.show()看不到图。", "多个subplot要调用plt.tight_layout()。"]
                }
            },
            {
                id: "4.2",
                title: "折线图与散点图",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "折线图展示数据随时间或有序类别的变化趋势；散点图展示两个变量之间的关系。本节学习这两种最常用的图表类型。",
                    codeExamples: [
                        {
                            title: "折线图",
                            code: "import matplotlib.pyplot as plt\nimport pandas as pd\n\n# 基本折线图\nmonths = ['1月', '2月', '3月', '4月', '5月']\nsales = [120, 150, 180, 160, 200]\n\nplt.figure(figsize=(10, 6))\nplt.plot(months, sales, marker='o', linewidth=2, markersize=8)\nplt.title('月度销售额', fontsize=16)\nplt.xlabel('月份')\nplt.ylabel('销售额(万元)')\nplt.grid(True, linestyle='--')\nplt.show()\n\n# 多条折线\nplt.plot(months, sales, label='2024年')\nplt.plot(months, [100, 130, 150, 140, 170], label='2023年')\nplt.legend()"
                        },
                        {
                            title: "散点图",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 基本散点图\nx = np.random.randn(100)\ny = x + np.random.randn(100) * 0.5\n\nplt.figure(figsize=(8, 6))\nplt.scatter(x, y, alpha=0.6, s=50, c='blue')\nplt.title('散点图示例')\nplt.xlabel('X')\nplt.ylabel('Y')\nplt.grid(True, alpha=0.3)\nplt.show()\n\n# 多类别散点图\ncolors = ['red', 'blue', 'green']\nfor i, color in enumerate(colors):\n    x = np.random.randn(30)\n    y = np.random.randn(30)\n    plt.scatter(x, y, c=color, label=f'类别{i+1}')"
                        }
                    ],
                    tips: ["alpha参数控制透明度，适合重叠数据点。", "s参数控制点的大小。"],
                    commonErrors: ["数据点过多时散点图会很杂乱。", "散点图不适合展示时间序列数据。"]
                }
            },
            {
                id: "4.3",
                title: "柱状图与直方图",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "柱状图用于比较不同类别的数值大小；直方图展示数据的分布情况。两者看起来相似但用途不同。",
                    codeExamples: [
                        {
                            title: "柱状图",
                            code: "import matplotlib.pyplot as plt\n\n# 基本柱状图\nfruits = ['苹果', '香蕉', '橙子', '葡萄']\ncounts = [30, 25, 20, 35]\n\nplt.figure(figsize=(10, 6))\nplt.bar(fruits, counts, color=['red', 'yellow', 'orange', 'purple'])\nplt.title('水果销量', fontsize=16)\nplt.xlabel('水果')\nplt.ylabel('销量')\nplt.show()\n\n# 水平柱状图\nplt.barh(fruits, counts)\n\n# 分组柱状图\nx = np.arange(4)\nwidth = 0.35\nplt.bar(x - width/2, counts, width, label='2024')\nplt.bar(x + width/2, [25, 20, 18, 30], width, label='2023')\nplt.xticks(x, fruits)\nplt.legend()"
                        },
                        {
                            title: "直方图",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 生成正态分布数据\ndata = np.random.randn(1000)\n\nplt.figure(figsize=(10, 6))\nplt.hist(data, bins=30, color='skyblue', edgecolor='white')\nplt.title('数据分布直方图')\nplt.xlabel('值')\nplt.ylabel('频数')\nplt.grid(True, alpha=0.3)\nplt.show()\n\n# 设置区间边界\nbins = [0, 10, 20, 30, 40, 50, 100]\nplt.hist(data, bins=bins)"
                        }
                    ],
                    tips: ["柱状图的条形之间通常有间隙。", "直方图的bins参数控制分组数量。"],
                    commonErrors: ["柱状图和直方图容易混淆。", "bins太多或太少都不好。"]
                }
            },
            {
                id: "4.4",
                title: "饼图与箱线图",
                duration: "20分钟",
                type: "图文",
                content: {
                    text: "饼图展示各部分占总体的比例关系；箱线图展示数据的分布特征，包括中位数、四分位数和异常值。",
                    codeExamples: [
                        {
                            title: "饼图",
                            code: "import matplotlib.pyplot as plt\n\n# 基本饼图\nsizes = [25, 35, 20, 20]\nlabels = ['苹果', '香蕉', '橙子', '葡萄']\ncolors = ['red', 'yellow', 'orange', 'purple']\n\nplt.figure(figsize=(8, 8))\nplt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)\nplt.title('水果占比', fontsize=16)\nplt.axis('equal')  # 使饼图保持圆形\nplt.show()\n\n# 突出显示某一块\nplt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',\n        explode=[0, 0.1, 0, 0])  # 突出第二块"
                        },
                        {
                            title: "箱线图",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 生成数据\ndata = [np.random.normal(0, std, 100) for std in range(1, 4)]\n\nplt.figure(figsize=(10, 6))\nplt.boxplot(data, labels=['A', 'B', 'C'])\nplt.title('箱线图示例')\nplt.xlabel('类别')\nplt.ylabel('值')\nplt.grid(True, alpha=0.3)\nplt.show()\n\n# 水平箱线图\nplt.boxplot(data, labels=['A', 'B', 'C'], vert=False)\n\n# 带异常值的箱线图\nplt.boxplot(data, labels=['A', 'B', 'C'], showfliers=True)"
                        }
                    ],
                    tips: ["饼图适合展示比例关系，不适合类别太多的情况。", "箱线图可以直观看出数据的离散程度。"],
                    commonErrors: ["饼图类别太多时不清晰。", "箱线图的异常值检测使用IQR方法。"]
                }
            },
            {
                id: "4.5",
                title: "子图与布局",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "subplots允许在一个图形中创建多个子图，合理布局可以更有效地展示和比较数据。",
                    codeExamples: [
                        {
                            title: "基本子图布局",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 创建2x2子图\nfig, axes = plt.subplots(2, 2, figsize=(12, 10))\n\n# 在每个子图上绘图\nx = np.linspace(0, 10, 100)\n\naxes[0, 0].plot(x, np.sin(x))\naxes[0, 0].set_title('正弦')\n\naxes[0, 1].plot(x, np.cos(x))\naxes[0, 1].set_title('余弦')\n\naxes[1, 0].plot(x, x)\naxes[1, 0].set_title('线性')\n\naxes[1, 1].plot(x, x**2)\naxes[1, 1].set_title('平方')\n\nplt.tight_layout()\nplt.show()"
                        },
                        {
                            title: "网格布局",
                            code: "import matplotlib.pyplot as plt\n\nfig = plt.figure(figsize=(12, 8))\n\n# 不规则网格\nax1 = plt.subplot(2, 2, 1)\nax2 = plt.subplot(2, 2, 2)\nax3 = plt.subplot(2, 1, 2)  # 占据下方整行\n\nax1.plot([1, 2, 3], [1, 2, 3])\nax2.plot([1, 2, 3], [3, 2, 1])\nax3.bar(['A', 'B', 'C'], [3, 5, 2])\n\nplt.tight_layout()\nplt.show()\n\n# 使用GridSpec精确控制\nfrom matplotlib.gridspec import GridSpec\nfig = plt.figure()\ngs = GridSpec(3, 3, figure=fig)"
                        }
                    ],
                    tips: ["tight_layout()自动调整子图参数。", "共享坐标轴可以让比较更容易。"],
                    commonErrors: ["子图太多时每个图会太小。", "忘记tight_layout()可能导致重叠。"]
                }
            },
            {
                id: "4.6",
                title: "图表美化与保存",
                duration: "15分钟",
                type: "图文",
                content: {
                    text: "良好的图表应该清晰、美观、易读。本节学习如何美化图表样式、设置颜色方案，以及保存高质量图像。",
                    codeExamples: [
                        {
                            title: "样式设置",
                            code: "import matplotlib.pyplot as plt\nimport numpy as np\n\n# 使用内置样式\nplt.style.use('seaborn')\n\n# 自定义颜色\nplt.rcParams['axes.facecolor'] = 'white'\nplt.rcParams['figure.facecolor'] = 'white'\n\nx = np.linspace(0, 10, 100)\nplt.plot(x, np.sin(x), color='red', linewidth=2, linestyle='--')\nplt.plot(x, np.cos(x), color='blue', linewidth=2)\n\n# 设置标题和标签的字体\nplt.title('示例图', fontsize=16, fontweight='bold')\nplt.xlabel('X轴', fontsize=12)\nplt.ylabel('Y轴', fontsize=12)\n\n# 添加图例\nplt.legend(['sin(x)', 'cos(x)'], loc='upper right')\n\nplt.grid(True, alpha=0.3)\nplt.show()"
                        },
                        {
                            title: "保存图像",
                            code: "import matplotlib.pyplot as plt\n\nfig, ax = plt.subplots(figsize=(10, 6))\nax.plot([1, 2, 3], [1, 4, 9])\nax.set_title('保存示例')\n\n# 保存为不同格式\nfig.savefig('plot.png', dpi=300, bbox_inches='tight')\nfig.savefig('plot.pdf', bbox_inches='tight')\nfig.savefig('plot.svg', bbox_inches='tight')\n\n# 保存时不显示\nplt.savefig('plot.png', dpi=300, bbox_inches='tight')\n\n# 设置透明背景\nplt.savefig('plot_transparent.png', transparent=True)"
                        }
                    ],
                    tips: ["保存时设置dpi=300可以获得高清图像。", "bbox_inches='tight'自动调整边界。"],
                    commonErrors: ["保存前不要关闭图形。", "PDF和SVG是矢量格式，放大不失真。"]
                }
            }
        ]
    }
];
