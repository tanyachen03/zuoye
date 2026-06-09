const PROJECTS_DATA = [
    {
        id: "data-cleaning",
        title: "数据清洗实战",
        icon: "🧹",
        difficulty: "入门",
        duration: "30分钟",
        dataset: "retail_orders.csv",
        description: "学习如何清洗真实零售订单数据",
        content: {
            objectives: [
                "识别并处理缺失值",
                "检测并处理重复数据",
                "修正格式不一致的数据",
                "处理异常值"
            ],
            datasetInfo: "retail_orders.csv 包含1000条零售订单记录，包含订单ID、客户ID、产品、数量、单价、订单日期等字段。数据中包含缺失值、重复行、日期格式不一致等问题。",
            steps: [
                {
                    title: "加载数据并初步检查",
                    description: "使用Pandas读取CSV文件，查看数据的基本信息和数据类型"
                },
                {
                    title: "处理缺失值",
                    description: "识别各列的缺失值情况，根据业务逻辑选择合适的填充或删除策略"
                },
                {
                    title: "处理重复数据",
                    description: "检测并删除完全重复的订单记录"
                },
                {
                    title: "数据格式统一",
                    description: "统一日期格式，确保数据类型正确"
                },
                {
                    title: "处理异常值",
                    description: "检测数量和单价中的异常值并进行处理"
                }
            ],
            codeExamples: [
                {
                    title: "数据加载和初步检查",
                    code: "import pandas as pd\n\ndf = pd.read_csv('retail_orders.csv')\nprint(df.head())\nprint('\\n数据信息:')\nprint(df.info())\nprint('\\n缺失值统计:')\nprint(df.isnull().sum())"
                }
            ],
            tips: [
                "使用info()可以快速了解数据类型和缺失值",
                "处理缺失值前先了解缺失原因",
                "备份原始数据再进行清洗"
            ],
            commonErrors: [
                "直接删除缺失值而没有分析原因",
                "忽略数据类型不一致的问题",
                "修改数据后忘记保存"
            ],
            challenges: [
                "尝试使用不同策略处理缺失值，对比结果差异",
                "分析重复订单产生的原因"
            ]
        },
        starterCode: "import pandas as pd\n\n# 读取数据\ndf = pd.read_csv('retail_orders.csv')\n\n# 查看数据基本信息\nprint('数据形状:', df.shape)\nprint('\\n前5行数据:')\nprint(df.head())\n\nprint('\\n数据类型:')\nprint(df.dtypes)\n\nprint('\\n缺失值统计:')\nprint(df.isnull().sum())"
    },
    {
        id: "group-aggregate",
        title: "分组聚合分析",
        icon: "📊",
        difficulty: "入门",
        duration: "30分钟",
        dataset: "retail_orders.csv",
        description: "使用分组聚合分析销售数据",
        content: {
            objectives: [
                "掌握groupby分组方法",
                "使用聚合函数进行统计分析",
                "多维度数据分析",
                "数据透视表使用"
            ],
            datasetInfo: "使用retail_orders.csv数据分析各维度下的销售情况，包括按月、按产品、按客户等维度的统计。",
            steps: [
                {
                    title: "按月统计销售额",
                    description: "将订单按月份分组，计算月度销售额"
                },
                {
                    title: "按产品类别统计",
                    description: "统计各产品类别的销售数量和金额"
                },
                {
                    title: "TOP N分析",
                    description: "找出销售额最高的产品和客户"
                },
                {
                    title: "数据透视表",
                    description: "使用pivot_table进行多维度分析"
                }
            ],
            codeExamples: [
                {
                    title: "基本分组统计",
                    code: "df['订单月份'] = pd.to_datetime(df['订单日期']).dt.to_period('M')\nmonthly_sales = df.groupby('订单月份')['销售额'].sum()\nprint('月度销售额:')\nprint(monthly_sales)"
                }
            ],
            tips: [
                "groupby后可以使用多个聚合函数",
                "as_index=False可以使分组列不成为索引"
            ],
            commonErrors: [
                "忘记对日期进行转换",
                "聚合时数据类型不匹配"
            ],
            challenges: [
                "计算同比和环比增长率",
                "按地区和产品进行交叉分析"
            ]
        },
        starterCode: "import pandas as pd\n\ndf = pd.read_csv('retail_orders.csv')\ndf['订单日期'] = pd.to_datetime(df['订单日期'])\n\n# 计算每笔订单的销售额\ndf['销售额'] = df['数量'] * df['单价']\n\n# 按月统计\ndf['月份'] = df['订单日期'].dt.to_period('M')\nmonthly = df.groupby('月份')['销售额'].sum()\nprint('月度销售额:')\nprint(monthly)\n\n# 按产品统计\nproduct_stats = df.groupby('产品').agg({\n    '数量': 'sum',\n    '销售额': 'sum'\n}).sort_values('销售额', ascending=False)\nprint('\\n产品销售排行:')\nprint(product_stats.head(10))"
    },
    {
        id: "market-basket",
        title: "购物篮分析",
        icon: "🛒",
        difficulty: "进阶",
        duration: "45分钟",
        dataset: "market_basket.csv",
        description: "关联规则挖掘发现商品组合",
        content: {
            objectives: [
                "理解关联规则概念",
                "计算支持度、置信度、提升度",
                "发现有价值的商品组合",
                "应用Apriori算法"
            ],
            datasetInfo: "market_basket.csv 包含客户的购物篮数据，每行代表一个客户的购买商品列表。用于发现哪些商品经常一起购买。",
            steps: [
                {
                    title: "数据预处理",
                    description: "将购物数据转换为事务格式"
                },
                {
                    title: "计算频繁项集",
                    description: "找出支持度高于阈值的商品组合"
                },
                {
                    title: "生成关联规则",
                    description: "计算置信度和提升度"
                },
                {
                    title: "规则分析与可视化",
                    description: "解读有意义的关联规则"
                }
            ],
            codeExamples: [
                {
                    title: "购物篮数据转换",
                    code: "from collections import Counter\nfrom itertools import combinations\n\n# 统计单个商品出现次数\nitems = []\nfor basket in df['商品列表']:\n    items.extend(basket.split(','))\nitem_counts = Counter(items)\nprint('最畅销商品:', item_counts.most_common(5))"
                }
            ],
            tips: [
                "支持度阈值不宜过低",
                "提升度大于1才有意义"
            ],
            commonErrors: [
                "混淆支持度和置信度",
                "忽视提升度的作用"
            ],
            challenges: [
                "实现简化的Apriori算法",
                "分析不同时间段的购物篮差异"
            ]
        },
        starterCode: "import pandas as pd\nfrom collections import Counter\n\ndf = pd.read_csv('market_basket.csv')\nprint('数据预览:')\nprint(df.head())\n\n# 统计商品出现频率\nall_items = []\nfor items in df['商品']:\n    all_items.extend(items.split(','))\nitem_counts = Counter(all_items)\nprint('\\n商品出现频率TOP10:')\nfor item, count in item_counts.most_common(10):\n    print(f'{item}: {count}')\n\n# 统计商品组合\npairs = Counter()\nfor items in df['商品']:\n    item_list = sorted(items.split(','))\n    for pair in combinations(item_list, 2):\n        pairs[pair] += 1\nprint('\\n最常一起购买的商品组合:')\nfor pair, count in pairs.most_common(5):\n    print(f'{pair[0]} + {pair[1]}: {count}')"
    },
    {
        id: "customer-cluster",
        title: "客户聚类分析",
        icon: "👥",
        difficulty: "进阶",
        duration: "45分钟",
        dataset: "customer_features.csv",
        description: "使用K-means对客户进行分群",
        content: {
            objectives: [
                "特征工程准备",
                "数据标准化",
                "K-means聚类实现",
                "客户分群画像分析"
            ],
            datasetInfo: "customer_features.csv 包含客户的多维度特征，包括年龄、收入、消费频率、平均消费金额等。",
            steps: [
                {
                    title: "特征选择与预处理",
                    description: "选择用于聚类的特征，处理缺失值和异常值"
                },
                {
                    title: "数据标准化",
                    description: "对不同量纲的特征进行标准化"
                },
                {
                    title: "确定最优聚类数",
                    description: "使用肘部法则确定K值"
                },
                {
                    title: "客户分群与画像",
                    description: "分析各客户群的特征"
                }
            ],
            codeExamples: [
                {
                    title: "K-means聚类",
                    code: "from sklearn.cluster import KMeans\nfrom sklearn.preprocessing import StandardScaler\n\nfeatures = df[['年龄', '月收入', '购买次数', '平均消费']]\nscaler = StandardScaler()\nfeatures_scaled = scaler.fit_transform(features)\n\nkmeans = KMeans(n_clusters=4, random_state=42)\ndf['客户群'] = kmeans.fit_predict(features_scaled)\nprint(df['客户群'].value_counts())"
                }
            ],
            tips: [
                "聚类前必须进行标准化",
                "使用肘部法则选择最优K"
            ],
            commonErrors: [
                "忽视特征量纲差异",
                "K值选择不当"
            ],
            challenges: [
                "尝试不同的聚类算法比较",
                "对各客户群制定营销策略"
            ]
        },
        starterCode: "import pandas as pd\nimport numpy as np\nfrom sklearn.cluster import KMeans\nfrom sklearn.preprocessing import StandardScaler\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('customer_features.csv')\nprint('客户特征数据:')\nprint(df.head())\n\n# 选择聚类特征\nfeatures = df[['年龄', '月收入', '购买次数', '平均消费额']]\n\n# 标准化\nscaler = StandardScaler()\nfeatures_scaled = scaler.fit_transform(features)\n\n# 肘部法则确定K值\ninertias = []\nfor k in range(1, 11):\n    kmeans = KMeans(n_clusters=k, random_state=42)\n    kmeans.fit(features_scaled)\n    inertias.append(kmeans.inertia_)\n\nprint('\\n各K值惯性:')\nfor k, inertia in enumerate(inertias, 1):\n    print(f'K={k}: {inertia:.2f}')\n\n# 使用K=4进行聚类\nkmeans = KMeans(n_clusters=4, random_state=42)\ndf['客户群'] = kmeans.fit_predict(features_scaled)\nprint('\\n客户群分布:')\nprint(df['客户群'].value_counts().sort_index())"
    },
    {
        id: "data-viz",
        title: "数据可视化",
        icon: "📈",
        difficulty: "进阶",
        duration: "45分钟",
        dataset: "retail_orders.csv",
        description: "创建专业的销售数据可视化图表",
        content: {
            objectives: [
                "选择合适的图表类型",
                "创建多维度可视化",
                "制作数据看板",
                "图表优化与美化"
            ],
            datasetInfo: "使用retail_orders.csv创建销售数据分析的可视化报表。",
            steps: [
                {
                    title: "趋势可视化",
                    description: "创建销售额趋势图"
                },
                {
                    title: "对比可视化",
                    description: "产品对比、地区对比图表"
                },
                {
                    title: "分布可视化",
                    description: "使用直方图和箱线图展示分布"
                },
                {
                    title: "组合图表",
                    description: "创建包含多个子图的综合报表"
                }
            ],
            codeExamples: [
                {
                    title: "销售趋势图",
                    code: "import matplotlib.pyplot as plt\nimport pandas as pd\n\ndf['订单日期'] = pd.to_datetime(df['订单日期'])\ndf['销售额'] = df['数量'] * df['单价']\ndf['月份'] = df['订单日期'].dt.to_period('M')\n\nmonthly = df.groupby('月份')['销售额'].sum()\nplt.figure(figsize=(12, 6))\nplt.plot(monthly.index.astype(str), monthly.values, marker='o')\nplt.title('月度销售额趋势')\nplt.xlabel('月份')\nplt.ylabel('销售额')\nplt.xticks(rotation=45)\nplt.grid(True)\nplt.tight_layout()\nplt.show()"
                }
            ],
            tips: [
                "图表要简洁，标题和标签清晰",
                "选择合适的颜色方案"
            ],
            commonErrors: [
                "图表过于复杂难懂",
                "坐标轴刻度误导"
            ],
            challenges: [
                "创建一个完整的数据看板",
                "使用交互式图表"
            ]
        },
        starterCode: "import pandas as pd\nimport matplotlib.pyplot as plt\nimport numpy as np\n\nplt.rcParams['font.size'] = 10\n\ndf = pd.read_csv('retail_orders.csv')\ndf['订单日期'] = pd.to_datetime(df['订单日期'])\ndf['销售额'] = df['数量'] * df['单价']\ndf['月份'] = df['订单日期'].dt.to_period('M')\ndf['星期'] = df['订单日期'].dt.day_name()\n\n# 创建组合图表\nfig, axes = plt.subplots(2, 2, figsize=(14, 10))\n\n# 1. 月度销售额趋势\nmonthly = df.groupby('月份')['销售额'].sum()\naxes[0, 0].plot(range(len(monthly)), monthly.values, marker='o')\naxes[0, 0].set_title('月度销售额趋势')\naxes[0, 0].set_xticks(range(len(monthly)))\naxes[0, 0].set_xticklabels([str(m) for m in monthly.index], rotation=45)\n\n# 2. 产品类别销售对比\nproduct_sales = df.groupby('产品')['销售额'].sum().sort_values(ascending=True)\naxes[0, 1].barh(product_sales.index, product_sales.values)\naxes[0, 1].set_title('各产品销售额')\n\n# 3. 每周各天销售额分布\nday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']\ndaily = df.groupby('星期')['销售额'].mean().reindex(day_order)\naxes[1, 0].bar(range(7), daily.values)\naxes[1, 0].set_title('各天平均销售额')\naxes[1, 0].set_xticks(range(7))\naxes[1, 0].set_xticklabels(['一', '二', '三', '四', '五', '六', '日'])\n\n# 4. 销售额分布直方图\naxes[1, 1].hist(df['销售额'], bins=30, edgecolor='black')\naxes[1, 1].set_title('销售额分布')\naxes[1, 1].set_xlabel('销售额')\naxes[1, 1].set_ylabel('频次')\n\nplt.tight_layout()\nplt.show()"
    },
    {
        id: "ab-test",
        title: "A/B测试分析",
        icon: "🧪",
        difficulty: "进阶",
        duration: "45分钟",
        dataset: "ab_test.csv",
        description: "分析A/B测试结果判断方案效果",
        content: {
            objectives: [
                "理解A/B测试原理",
                "计算统计显著性",
                "进行假设检验",
                "给出业务建议"
            ],
            datasetInfo: "ab_test.csv 包含A/B测试的实验数据，包括用户ID、分组(A/B)、是否转化、转化金额等字段。",
            steps: [
                {
                    title: "数据探索",
                    description: "查看各组的样本量和基础指标"
                },
                {
                    title: "转化率分析",
                    description: "计算并比较各组的转化率"
                },
                {
                    title: "统计检验",
                    description: "使用卡方检验判断差异显著性"
                },
                {
                    title: "结果解读",
                    description: "给出是否采用新方案的结论"
                }
            ],
            codeExamples: [
                {
                    title: "转化率分析",
                    code: "from scipy import stats\n\ngroup_a = df[df['分组'] == 'A']\ngroup_b = df[df['分组'] == 'B']\n\nrate_a = group_a['转化'].mean()\nrate_b = group_b['转化'].mean()\n\nprint(f'A组转化率: {rate_a:.4f}')\nprint(f'B组转化率: {rate_b:.4f}')\nprint(f'相对提升: {(rate_b - rate_a) / rate_a * 100:.2f}%')\n\n# 卡方检验\ncontingency = pd.crosstab(df['分组'], df['转化'])\nchi2, p, dof, expected = stats.chi2_contingency(contingency)\nprint(f'\\n卡方值: {chi2:.4f}')\nprint(f'P值: {p:.4f}')"
                }
            ],
            tips: [
                "样本量要足够大才有统计意义",
                "P值小于0.05通常被认为显著"
            ],
            commonErrors: [
                "只看绝对差异不检验显著性",
                "忽视样本量差异"
            ],
            challenges: [
                "进行功效分析确定最小样本量",
                "分析不同用户分层的测试结果"
            ]
        },
        starterCode: "import pandas as pd\nimport numpy as np\nfrom scipy import stats\n\ndf = pd.read_csv('ab_test.csv')\nprint('A/B测试数据概览:')\nprint(df.head())\nprint(f'\\n总样本量: {len(df)}')\n\n# 分组统计\ngroup_stats = df.groupby('分组').agg({\n    '用户ID': 'count',\n    '转化': ['sum', 'mean'],\n    '转化金额': 'mean'\n}).round(4)\ngroup_stats.columns = ['样本量', '转化数', '转化率', '平均转化金额']\nprint('\\n分组统计:')\nprint(group_stats)\n\n# 转化率差异\nrate_a = df[df['分组'] == 'A']['转化'].mean()\nrate_b = df[df['分组'] == 'B']['转化'].mean()\nprint(f'\\nA组转化率: {rate_a:.4f}')\nprint(f'B组转化率: {rate_b:.4f}')\nprint(f'差异: {rate_b - rate_a:.4f}')\nprint(f'相对提升: {(rate_b - rate_a) / rate_a * 100:.2f}%')\n\n# 卡方检验\ncontingency = pd.crosstab(df['分组'], df['转化'])\nchi2, p_value, dof, expected = stats.chi2_contingency(contingency)\nprint(f'\\n卡方检验:')\nprint(f'卡方值: {chi2:.4f}')\nprint(f'P值: {p_value:.6f}')\n\nif p_value < 0.05:\n    print('\\n结论: 差异具有统计显著性')\nelse:\n    print('\\n结论: 差异不具有统计显著性')"
    },
    {
        id: "time-series",
        title: "时间序列分析",
        icon: "📅",
        difficulty: "进阶",
        duration: "45分钟",
        dataset: "time_series_sales.csv",
        description: "时间序列预测销售趋势",
        content: {
            objectives: [
                "时间序列数据处理",
                "趋势和季节性分解",
                "移动平均预测",
                "指数平滑法应用"
            ],
            datasetInfo: "time_series_sales.csv 包含每日销售数据，包含日期、销售额字段，数据跨度一年。",
            steps: [
                {
                    title: "数据准备",
                    description: "将数据转换为时间序列格式"
                },
                {
                    title: "可视化探索",
                    description: "观察趋势和季节性模式"
                },
                {
                    title: "趋势分析",
                    description: "使用移动平均分析趋势"
                },
                {
                    title: "简单预测",
                    description: "使用指数平滑进行预测"
                }
            ],
            codeExamples: [
                {
                    title: "趋势分解",
                    code: "from statsmodels.tsa.seasonal import seasonal_decompose\n\nts = df.set_index('日期')['销售额']\ndecomposition = seasonal_decompose(ts, model='additive', period=30)\n\nprint('趋势成分均值:', decomposition.trend.dropna().mean())\nprint('季节性成分振幅:', decomposition.seasonal.max() - decomposition.seasonal.min())"
                }
            ],
            tips: [
                "确保日期是连续的时间序列",
                "period参数设置要合理"
            ],
            commonErrors: [
                "数据有缺失日期",
                "period设置不当"
            ],
            challenges: [
                "尝试不同的季节性分解模型",
                "进行多步预测"
            ]
        },
        starterCode: "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\n\ndf = pd.read_csv('time_series_sales.csv')\ndf['日期'] = pd.to_datetime(df['日期'])\ndf = df.sort_values('日期')\ndf = df.set_index('日期')\n\nprint('时间序列数据:')\nprint(df.head())\nprint(f'\\n数据范围: {df.index.min()} 至 {df.index.max()}')\n\n# 基本统计\nprint('\\n销售统计:')\nprint(df['销售额'].describe())\n\n# 移动平均\ndf['MA7'] = df['销售额'].rolling(7).mean()\ndf['MA30'] = df['销售额'].rolling(30).mean()\n\nprint('\\n最近7天数据:')\nprint(df[['销售额', 'MA7', 'MA30']].tail(7))\n\n# 月度汇总\nmonthly = df['销售额'].resample('M').sum()\nprint('\\n月度销售汇总:')\nprint(monthly)"
    },
    {
        id: "feature-engineering",
        title: "特征工程",
        icon: "🔧",
        difficulty: "高级",
        duration: "60分钟",
        dataset: "customer_features.csv",
        description: "构建高质量的机器学习特征",
        content: {
            objectives: [
                "理解特征工程的重要性",
                "进行特征转换和处理",
                "创建新特征",
                "特征选择和降维"
            ],
            datasetInfo: "customer_features.csv 包含客户特征数据，进行特征工程后用于后续的机器学习建模。",
            steps: [
                {
                    title: "数据探索",
                    description: "了解各特征的分布和相关性"
                },
                {
                    title: "缺失值和异常值处理",
                    description: "处理数据质量问题"
                },
                {
                    title: "特征转换",
                    description: "标准化、编码、变换"
                },
                {
                    title: "新特征创建",
                    description: "基于业务逻辑创建特征"
                },
                {
                    title: "特征选择",
                    description: "选择重要特征"
                }
            ],
            codeExamples: [
                {
                    title: "特征编码和标准化",
                    code: "from sklearn.preprocessing import StandardScaler, LabelEncoder\n\n# 类别编码\nle = LabelEncoder()\ndf['城市编码'] = le.fit_transform(df['城市'])\n\n# 数值标准化\nscaler = StandardScaler()\ndf[['收入标准化', '年龄标准化']] = scaler.fit_transform(\n    df[['月收入', '年龄']]\n)"
                }
            ],
            tips: [
                "类别变量需要进行编码",
                "树模型不需要标准化"
            ],
            commonErrors: [
                "对树模型进行不必要的标准化",
                "忽视特征的相关性"
            ],
            challenges: [
                "创建业务相关的新特征",
                "使用PCA进行降维"
            ]
        },
        starterCode: "import pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import StandardScaler, LabelEncoder\n\ndf = pd.read_csv('customer_features.csv')\nprint('原始数据:')\nprint(df.head())\nprint(f'\\n数据类型:\\n{df.dtypes}')\n\n# 缺失值处理\nprint('\\n缺失值:')\nprint(df.isnull().sum())\ndf['月收入'].fillna(df['月收入'].median(), inplace=True)\n\n# 异常值处理\nQ1 = df['年龄'].quantile(0.25)\nQ3 = df['年龄'].quantile(0.75)\nIQR = Q3 - Q1\ndf = df[(df['年龄'] >= Q1 - 1.5*IQR) & (df['年龄'] <= Q3 + 1.5*IQR)]\n\n# 类别编码\nle = LabelEncoder()\ndf['城市编码'] = le.fit_transform(df['城市'].astype(str))\nprint('\\n编码映射:')\nfor i, label in enumerate(le.classes_):\n    print(f'{label}: {i}')\n\n# 创建新特征\ndf['消费强度'] = df['平均消费额'] * df['购买次数']\ndf['收入年龄比'] = df['月收入'] / df['年龄']\n\n# 标准化\nscaler = StandardScaler()\ndf[['收入标准化', '年龄标准化', '消费标准化']] = scaler.fit_transform(\n    df[['月收入', '年龄', '平均消费额']]\n)\n\nprint('\\n处理后数据:')\nprint(df.head())"
    },
    {
        id: "anomaly-detection",
        title: "异常值检测",
        icon: "⚠️",
        difficulty: "高级",
        duration: "45分钟",
        dataset: "customer_features.csv",
        description: "识别数据中的异常和欺诈",
        content: {
            objectives: [
                "掌握异常检测方法",
                "使用统计方法检测异常",
                "使用机器学习方法",
                "分析异常原因"
            ],
            datasetInfo: "customer_features.csv 包含客户特征数据，使用多种方法检测异常客户。",
            steps: [
                {
                    title: "基于统计的检测",
                    description: "使用Z-score和IQR方法"
                },
                {
                    title: "基于距离的检测",
                    description: "使用K近邻和LOF方法"
                },
                {
                    title: "基于模型的检测",
                    description: "使用Isolation Forest"
                },
                {
                    title: "异常分析",
                    description: "分析异常客户特征"
                }
            ],
            codeExamples: [
                {
                    title: "Isolation Forest",
                    code: "from sklearn.ensemble import IsolationForest\n\nfeatures = df[['年龄', '月收入', '购买次数']]\niso_forest = IsolationForest(contamination=0.05, random_state=42)\ndf['异常'] = iso_forest.fit_predict(features)\nprint('异常客户数:', (df['异常'] == -1).sum())"
                }
            ],
            tips: [
                "contamination参数设置要合理",
                "结合多种方法结果"
            ],
            commonErrors: [
                "只依赖单一方法",
                "忽视异常的业务含义"
            ],
            challenges: [
                "实现半监督的异常检测",
                "对新数据实时检测"
            ]
        },
        starterCode: "import pandas as pd\nimport numpy as np\nfrom sklearn.ensemble import IsolationForest\nfrom sklearn.preprocessing import StandardScaler\n\ndf = pd.read_csv('customer_features.csv')\nprint('客户数据:')\nprint(df.head())\n\n# 选择用于异常检测的特征\nfeatures = df[['年龄', '月收入', '购买次数', '平均消费额']].copy()\n\n# 1. Z-score方法\nprint('\\n=== Z-score异常检测 ===')\nz_scores = np.abs((features - features.mean()) / features.std())\nanomalies_zscore = (z_scores > 3).any(axis=1)\nprint(f'Z-score检测到的异常数: {anomalies_zscore.sum()}')\n\n# 2. IQR方法\nprint('\\n=== IQR异常检测 ===')\nQ1 = features.quantile(0.25)\nQ3 = features.quantile(0.75)\nIQR = Q3 - Q1\nanomalies_iqr = ((features < (Q1 - 1.5 * IQR)) | (features > (Q3 + 1.5 * IQR))).any(axis=1)\nprint(f'IQR检测到的异常数: {anomalies_iqr.sum()}')\n\n# 3. Isolation Forest\nprint('\\n=== Isolation Forest ===')\nscaler = StandardScaler()\nfeatures_scaled = scaler.fit_transform(features)\niso_forest = IsolationForest(contamination=0.05, random_state=42)\ndf['异常分数'] = iso_forest.fit_predict(features_scaled)\ndf['异常'] = df['异常分数'] == -1\nprint(f'Isolation Forest检测到的异常数: {df[\"异常\"].sum()}')\n\n# 显示异常客户\nprint('\\n=== 异常客户 ===')\nprint(df[df['异常']][['姓名', '年龄', '月收入', '购买次数']])"
    },
    {
        id: "multi-merge",
        title: "多数据集合并",
        icon: "🔗",
        difficulty: "进阶",
        duration: "45分钟",
        dataset: "retail_orders.csv",
        description: "合并多个数据源进行综合分析",
        content: {
            objectives: [
                "掌握多种合并方法",
                "处理合并中的冲突",
                "多表关联查询",
                "综合数据分析"
            ],
            datasetInfo: "演示如何合并多个相关数据集进行综合分析。",
            steps: [
                {
                    title: "数据加载",
                    description: "加载多个数据源"
                },
                {
                    title: "数据匹配合并",
                    description: "使用merge进行关联"
                },
                {
                    title: "追加合并",
                    description: "使用concat追加数据"
                },
                {
                    title: "综合分析",
                    description: "基于合并后的数据进行分析"
                }
            ],
            codeExamples: [
                {
                    title: "多表合并",
                    code: "# 假设有orders和customers两个表\nmerged = orders.merge(customers, on='客户ID', how='left')\nresult = merged.groupby('城市').agg({\n    '订单数': 'count',\n    '总金额': 'sum'\n})"
                }
            ],
            tips: [
                "确认合并键的正确性",
                "选择合适的连接类型"
            ],
            commonErrors: [
                "合并键不唯一导致笛卡尔积",
                "选择错误的连接类型"
            ],
            challenges: [
                "处理多对多关系",
                "合并后数据的去重和清洗"
            ]
        },
        starterCode: "import pandas as pd\n\n# 读取主订单数据\norders = pd.read_csv('retail_orders.csv')\norders['销售额'] = orders['数量'] * orders['单价']\n\nprint('=== 订单数据 ===')\nprint(orders.head())\nprint(f'订单数: {len(orders)}')\n\n# 创建客户信息表\ncustomers = orders.groupby('客户ID').agg({\n    '姓名': 'first',\n    '订单日期': 'count',\n    '销售额': 'sum'\n}).reset_index()\ncustomers.columns = ['客户ID', '客户名称', '订单数', '累计消费']\n\nprint('\\n=== 客户汇总 ===')\nprint(customers.head())\n\n# 创建产品汇总表\nproducts = orders.groupby('产品').agg({\n    '数量': 'sum',\n    '销售额': 'sum'\n}).reset_index()\nproducts.columns = ['产品名称', '总销量', '总销售额']\n\nprint('\\n=== 产品汇总 ===')\nprint(products.head())\n\n# 综合分析：按产品统计客户数\nproduct_customers = orders.groupby('产品')['客户ID'].nunique().reset_index()\nproduct_customers.columns = ['产品名称', '客户数']\nproducts = products.merge(product_customers, on='产品名称')\nproducts['客单价'] = products['总销售额'] / products['客户数']\n\nprint('\\n=== 产品分析汇总 ===')\nprint(products.sort_values('总销售额', ascending=False))"
    }
];

if (typeof module !== 'undefined' && module.exports) {
    module.exports = PROJECTS_DATA;
}
