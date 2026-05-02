#!/usr/bin/env python3
import os
import re

PROJECTS_DIR = "/workspace/data-analytics-platform/projects"

# 所有项目的配置
PROJECTS_CONFIG = {
    "project4.html": {
        "title": "项目4：RFM客户价值分析 - 数析学院",
        "project_name": "项目4：RFM客户价值分析",
        "difficulty": "中级",
        "time": "45分钟",
        "tech": "Python + Pandas",
        "data_info": "客户交易记录",
        "tips_title": "RFM分析技巧",
        "tips": [
            ("recency", "最近一次购买时间"),
            ("frequency", "购买频率"),
            ("monetary", "消费金额"),
            ("pd.qcut()", "分位数分组"),
        ],
        "goals": [
            "理解RFM模型原理",
            "学会客户分群方法",
            "掌握客户价值评估",
        ],
        "description": "某零售企业需要通过RFM模型对客户进行价值分群，找出高价值客户群体。",
        "task_title": "请完成以下分析任务：",
        "tasks": [
            "计算每个客户的R、F、M值",
            "对客户进行RFM评分",
        ],
        "default_code": '''import pandas as pd
from datetime import datetime

# 客户交易数据
data = [
    {"客户ID": "C001", "交易日期": "2024-01-15", "交易金额": 580},
    {"客户ID": "C001", "交易日期": "2024-02-20", "交易金额": 320},
    {"客户ID": "C001", "交易日期": "2024-03-10", "交易金额": 450},
    {"客户ID": "C002", "交易日期": "2023-12-05", "交易金额": 1200},
    {"客户ID": "C003", "交易日期": "2024-03-01", "交易金额": 280},
    {"客户ID": "C003", "交易日期": "2024-03-15", "交易金额": 350},
    {"客户ID": "C004", "交易日期": "2023-10-20", "交易金额": 890},
    {"客户ID": "C005", "交易日期": "2024-02-28", "交易金额": 1500},
    {"客户ID": "C005", "交易日期": "2024-03-05", "交易金额": 680},
    {"客户ID": "C005", "交易日期": "2024-03-12", "交易金额": 420},
]

df = pd.DataFrame(data)
df['交易日期'] = pd.to_datetime(df['交易日期'])
print("【原始数据】")
print(df.to_string(index=False))

# TODO: 完成RFM分析
# 1. 计算每个客户的R（最近购买天数）、F（购买次数）、M（总金额）
# 2. 对客户进行评分

print("\\n【RFM分析结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd
from datetime import datetime

data = [
    {"客户ID": "C001", "交易日期": "2024-01-15", "交易金额": 580},
    {"客户ID": "C001", "交易日期": "2024-02-20", "交易金额": 320},
    {"客户ID": "C001", "交易日期": "2024-03-10", "交易金额": 450},
    {"客户ID": "C002", "交易日期": "2023-12-05", "交易金额": 1200},
    {"客户ID": "C003", "交易日期": "2024-03-01", "交易金额": 280},
    {"客户ID": "C003", "交易日期": "2024-03-15", "交易金额": 350},
    {"客户ID": "C004", "交易日期": "2023-10-20", "交易金额": 890},
    {"客户ID": "C005", "交易日期": "2024-02-28", "交易金额": 1500},
    {"客户ID": "C005", "交易日期": "2024-03-05", "交易金额": 680},
    {"客户ID": "C005", "交易日期": "2024-03-12", "交易金额": 420},
]

df = pd.DataFrame(data)
df['交易日期'] = pd.to_datetime(df['交易日期'])

# 设定分析日期
analysis_date = pd.to_datetime('2024-03-20')

# 计算RFM值
rfm = df.groupby('客户ID').agg({
    '交易日期': lambda x: (analysis_date - x.max()).days,  # Recency
    '客户ID': 'count',  # Frequency
    '交易金额': 'sum'  # Monetary
}).rename(columns={
    '交易日期': 'R',
    '客户ID': 'F',
    '交易金额': 'M'
})

# RFM评分（使用分位数）
rfm['R_Score'] = pd.qcut(rfm['R'], q=3, labels=[3, 2, 1])  # R越小越好
rfm['F_Score'] = pd.qcut(rfm['F'], q=3, labels=[1, 2, 3], duplicates='drop')  # F越大越好
rfm['M_Score'] = pd.qcut(rfm['M'], q=3, labels=[1, 2, 3])  # M越大越好

print("【RFM分析结果】")
print(rfm.to_string())'''
    },
    "project5.html": {
        "title": "项目5：商品关联规则分析 - 数析学院",
        "project_name": "项目5：商品关联规则分析",
        "difficulty": "中级",
        "time": "50分钟",
        "tech": "Python + Pandas",
        "data_info": "购物篮数据",
        "tips_title": "关联分析技巧",
        "tips": [
            ("support", "支持度"),
            ("confidence", "置信度"),
            ("lift", "提升度"),
            ("apriori", "Apriori算法"),
        ],
        "goals": [
            "理解关联规则原理",
            "学会购物篮分析",
            "掌握商品推荐策略",
        ],
        "description": "某超市需要分析商品之间的关联关系，发现经常一起购买的商品组合，优化商品陈列和促销策略。",
        "task_title": "请完成以下分析任务：",
        "tasks": [
            "统计商品组合出现频率",
            "找出高频商品组合",
        ],
        "default_code": '''import pandas as pd
from itertools import combinations
from collections import Counter

# 购物篮数据
transactions = [
    ["牛奶", "面包", "黄油"],
    ["牛奶", "面包"],
    ["面包", "黄油", "果酱"],
    ["牛奶", "面包", "鸡蛋"],
    ["牛奶", "鸡蛋"],
    ["面包", "黄油"],
    ["牛奶", "面包", "黄油", "鸡蛋"],
    ["牛奶", "果酱"],
    ["面包", "果酱"],
    ["牛奶", "面包", "黄油"],
]

print("【购物篮数据】")
for i, t in enumerate(transactions, 1):
    print(f"交易{i}: {t}")

# TODO: 完成关联分析
# 1. 统计商品组合出现频率
# 2. 计算支持度

print("\\n【分析结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd
from itertools import combinations
from collections import Counter

transactions = [
    ["牛奶", "面包", "黄油"],
    ["牛奶", "面包"],
    ["面包", "黄油", "果酱"],
    ["牛奶", "面包", "鸡蛋"],
    ["牛奶", "鸡蛋"],
    ["面包", "黄油"],
    ["牛奶", "面包", "黄油", "鸡蛋"],
    ["牛奶", "果酱"],
    ["面包", "果酱"],
    ["牛奶", "面包", "黄油"],
]

# 统计单个商品频率
item_counts = Counter()
for trans in transactions:
    for item in trans:
        item_counts[item] += 1

print("【单个商品频率】")
for item, count in item_counts.most_common():
    support = count / len(transactions) * 100
    print(f"{item}: {count}次, 支持度: {support:.1f}%")

# 统计商品对频率
pair_counts = Counter()
for trans in transactions:
    for pair in combinations(sorted(trans), 2):
        pair_counts[pair] += 1

print("\\n【商品组合频率（Top 5）】")
for pair, count in pair_counts.most_common(5):
    support = count / len(transactions) * 100
    print(f"{pair}: {count}次, 支持度: {support:.1f}%")'''
    },
    "project6.html": {
        "title": "项目6：A/B测试效果分析 - 数析学院",
        "project_name": "项目6：A/B测试效果分析",
        "difficulty": "中级",
        "time": "40分钟",
        "tech": "Python + Pandas",
        "data_info": "A/B测试数据",
        "tips_title": "A/B测试技巧",
        "tips": [
            ("转化率", "conversion rate"),
            ("显著性检验", "significance test"),
            ("置信区间", "confidence interval"),
            ("p-value", "显著性水平"),
        ],
        "goals": [
            "理解A/B测试原理",
            "学会转化率分析",
            "掌握统计显著性判断",
        ],
        "description": "某电商平台进行了按钮颜色的A/B测试，需要分析哪种颜色的转化率更高，并判断差异是否显著。",
        "task_title": "请完成以下分析任务：",
        "tasks": [
            "计算各组的转化率",
            "分析转化率差异",
        ],
        "default_code": '''import pandas as pd

# A/B测试数据
data = [
    {"用户ID": "U001", "组别": "A", "是否转化": 1},
    {"用户ID": "U002", "组别": "A", "是否转化": 0},
    {"用户ID": "U003", "组别": "A", "是否转化": 1},
    {"用户ID": "U004", "组别": "A", "是否转化": 0},
    {"用户ID": "U005", "组别": "A", "是否转化": 0},
    {"用户ID": "U006", "组别": "B", "是否转化": 1},
    {"用户ID": "U007", "组别": "B", "是否转化": 1},
    {"用户ID": "U008", "组别": "B", "是否转化": 1},
    {"用户ID": "U009", "组别": "B", "是否转化": 0},
    {"用户ID": "U010", "组别": "B", "是否转化": 1},
]

df = pd.DataFrame(data)
print("【A/B测试数据】")
print(df.to_string(index=False))

# TODO: 完成A/B测试分析
# 1. 计算各组的转化率
# 2. 比较两组差异

print("\\n【分析结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd

data = [
    {"用户ID": "U001", "组别": "A", "是否转化": 1},
    {"用户ID": "U002", "组别": "A", "是否转化": 0},
    {"用户ID": "U003", "组别": "A", "是否转化": 1},
    {"用户ID": "U004", "组别": "A", "是否转化": 0},
    {"用户ID": "U005", "组别": "A", "是否转化": 0},
    {"用户ID": "U006", "组别": "B", "是否转化": 1},
    {"用户ID": "U007", "组别": "B", "是否转化": 1},
    {"用户ID": "U008", "组别": "B", "是否转化": 1},
    {"用户ID": "U009", "组别": "B", "是否转化": 0},
    {"用户ID": "U010", "组别": "B", "是否转化": 1},
]

df = pd.DataFrame(data)

# 计算各组统计指标
results = df.groupby('组别').agg({
    '用户ID': 'count',
    '是否转化': 'sum'
}).rename(columns={'用户ID': '样本量', '是否转化': '转化数'})

results['转化率'] = results['转化数'] / results['样本量'] * 100

print("【A/B测试结果】")
print(results)

# 计算转化率差异
conv_a = results.loc['A', '转化率']
conv_b = results.loc['B', '转化率']
diff = conv_b - conv_a

print(f"\\n【结论】")
print(f"A组转化率: {conv_a:.1f}%")
print(f"B组转化率: {conv_b:.1f}%")
print(f"B组比A组高: {diff:.1f}个百分点")
if conv_b > conv_a:
    print("建议: B组表现更好，建议采用B方案")'''
    },
    "project7.html": {
        "title": "项目7：时间序列趋势分析 - 数析学院",
        "project_name": "项目7：时间序列趋势分析",
        "difficulty": "中级",
        "time": "45分钟",
        "tech": "Python + Pandas",
        "data_info": "月度销售数据",
        "tips_title": "时间序列技巧",
        "tips": [
            ("rolling()", "移动平均"),
            ("diff()", "差分计算"),
            ("pct_change()", "环比增长"),
            ("resample()", "重采样"),
        ],
        "goals": [
            "掌握时间序列处理",
            "学会趋势分析方法",
            "掌握移动平均计算",
        ],
        "description": "某企业需要分析销售数据的时间趋势，识别增长或下降趋势，为业务决策提供支持。",
        "task_title": "请完成以下分析任务：",
        "tasks": [
            "计算月度销售额趋势",
            "计算移动平均值",
        ],
        "default_code": '''import pandas as pd

# 月度销售数据
data = [
    {"月份": "2023-01", "销售额": 120000},
    {"月份": "2023-02", "销售额": 135000},
    {"月份": "2023-03", "销售额": 128000},
    {"月份": "2023-04", "销售额": 145000},
    {"月份": "2023-05", "销售额": 152000},
    {"月份": "2023-06", "销售额": 148000},
    {"月份": "2023-07", "销售额": 165000},
    {"月份": "2023-08", "销售额": 172000},
    {"月份": "2023-09", "销售额": 168000},
    {"月份": "2023-10", "销售额": 185000},
    {"月份": "2023-11", "销售额": 195000},
    {"月份": "2023-12", "销售额": 210000},
]

df = pd.DataFrame(data)
df['月份'] = pd.to_datetime(df['月份'])
print("【月度销售数据】")
print(df.to_string(index=False))

# TODO: 完成时间序列分析
# 1. 计算环比增长率
# 2. 计算3个月移动平均

print("\\n【分析结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd

data = [
    {"月份": "2023-01", "销售额": 120000},
    {"月份": "2023-02", "销售额": 135000},
    {"月份": "2023-03", "销售额": 128000},
    {"月份": "2023-04", "销售额": 145000},
    {"月份": "2023-05", "销售额": 152000},
    {"月份": "2023-06", "销售额": 148000},
    {"月份": "2023-07", "销售额": 165000},
    {"月份": "2023-08", "销售额": 172000},
    {"月份": "2023-09", "销售额": 168000},
    {"月份": "2023-10", "销售额": 185000},
    {"月份": "2023-11", "销售额": 195000},
    {"月份": "2023-12", "销售额": 210000},
]

df = pd.DataFrame(data)
df['月份'] = pd.to_datetime(df['月份'])

# 计算环比增长率
df['环比增长'] = df['销售额'].pct_change() * 100

# 计算3个月移动平均
df['移动平均(3月)'] = df['销售额'].rolling(window=3).mean()

# 计算同比增长（假设有去年同期数据）
df['趋势'] = df['环比增长'].apply(lambda x: '↑' if x > 0 else '↓' if x < 0 else '-')

print("【时间序列分析结果】")
print(df.to_string(index=False))

print(f"\\n【趋势总结】")
print(f"平均月销售额: {df['销售额'].mean():,.0f}元")
print(f"年度增长: {(df['销售额'].iloc[-1] - df['销售额'].iloc[0]) / df['销售额'].iloc[0] * 100:.1f}%")'''
    },
    "project8.html": {
        "title": "项目8：用户留存率分析 - 数析学院",
        "project_name": "项目8：用户留存率分析",
        "difficulty": "中级",
        "time": "45分钟",
        "tech": "Python + Pandas",
        "data_info": "用户登录日志",
        "tips_title": "留存分析技巧",
        "tips": [
            ("留存率", "retention rate"),
            ("cohort", "用户群组"),
            ("pivot_table", "透视表"),
            ("nunique()", "唯一计数"),
        ],
        "goals": [
            "理解留存率概念",
            "学会群组分析方法",
            "掌握留存率计算",
        ],
        "description": "某APP需要分析用户留存情况，了解用户在不同时间段的留存率变化，评估产品粘性。",
        "task_title": "请完成以下分析任务：",
        "tasks": [
            "计算各日留存用户数",
            "计算留存率",
        ],
        "default_code": '''import pandas as pd

# 用户登录数据
data = [
    {"用户ID": "U001", "注册日期": "2024-01-01", "登录日期": "2024-01-01"},
    {"用户ID": "U001", "注册日期": "2024-01-01", "登录日期": "2024-01-02"},
    {"用户ID": "U001", "注册日期": "2024-01-01", "登录日期": "2024-01-03"},
    {"用户ID": "U002", "注册日期": "2024-01-01", "登录日期": "2024-01-01"},
    {"用户ID": "U002", "注册日期": "2024-01-01", "登录日期": "2024-01-02"},
    {"用户ID": "U003", "注册日期": "2024-01-01", "登录日期": "2024-01-01"},
    {"用户ID": "U004", "注册日期": "2024-01-02", "登录日期": "2024-01-02"},
    {"用户ID": "U004", "注册日期": "2024-01-02", "登录日期": "2024-01-03"},
    {"用户ID": "U005", "注册日期": "2024-01-02", "登录日期": "2024-01-02"},
]

df = pd.DataFrame(data)
df['注册日期'] = pd.to_datetime(df['注册日期'])
df['登录日期'] = pd.to_datetime(df['登录日期'])
print("【用户登录数据】")
print(df.to_string(index=False))

# TODO: 完成留存分析
# 1. 计算每个用户的留存天数
# 2. 计算各日留存率

print("\\n【留存分析结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd

data = [
    {"用户ID": "U001", "注册日期": "2024-01-01", "登录日期": "2024-01-01"},
    {"用户ID": "U001", "注册日期": "2024-01-01", "登录日期": "2024-01-02"},
    {"用户ID": "U001", "注册日期": "2024-01-01", "登录日期": "2024-01-03"},
    {"用户ID": "U002", "注册日期": "2024-01-01", "登录日期": "2024-01-01"},
    {"用户ID": "U002", "注册日期": "2024-01-01", "登录日期": "2024-01-02"},
    {"用户ID": "U003", "注册日期": "2024-01-01", "登录日期": "2024-01-01"},
    {"用户ID": "U004", "注册日期": "2024-01-02", "登录日期": "2024-01-02"},
    {"用户ID": "U004", "注册日期": "2024-01-02", "登录日期": "2024-01-03"},
    {"用户ID": "U005", "注册日期": "2024-01-02", "登录日期": "2024-01-02"},
]

df = pd.DataFrame(data)
df['注册日期'] = pd.to_datetime(df['注册日期'])
df['登录日期'] = pd.to_datetime(df['登录日期'])

# 计算留存天数
df['留存天数'] = (df['登录日期'] - df['注册日期']).dt.days

# 计算各注册日期的新用户数
new_users = df.groupby('注册日期')['用户ID'].nunique().reset_index()
new_users.columns = ['注册日期', '新用户数']

# 计算留存用户数
retention = df.groupby(['注册日期', '留存天数'])['用户ID'].nunique().reset_index()
retention.columns = ['注册日期', '留存天数', '留存用户数']

# 合并计算留存率
retention = retention.merge(new_users, on='注册日期')
retention['留存率'] = retention['留存用户数'] / retention['新用户数'] * 100

print("【留存率分析结果】")
print(retention.to_string(index=False))'''
    },
    "project9.html": {
        "title": "项目9：数据可视化实战 - 数析学院",
        "project_name": "项目9：数据可视化实战",
        "difficulty": "初级",
        "time": "35分钟",
        "tech": "Python + Pandas",
        "data_info": "销售数据",
        "tips_title": "可视化技巧",
        "tips": [
            ("plot()", "基础绑图"),
            ("plot.bar()", "柱状图"),
            ("plot.pie()", "饼图"),
            ("plot.line()", "折线图"),
        ],
        "goals": [
            "掌握数据可视化方法",
            "学会选择合适的图表",
            "掌握图表美化技巧",
        ],
        "description": "某公司需要将销售数据以图表形式展示，便于管理层快速了解业务状况。",
        "task_title": "请完成以下可视化任务：",
        "tasks": [
            "计算各类目销售额",
            "输出图表数据",
        ],
        "default_code": '''import pandas as pd

# 销售数据
data = [
    {"类目": "电子产品", "销售额": 150000},
    {"类目": "服装", "销售额": 120000},
    {"类目": "食品", "销售额": 80000},
    {"类目": "家居", "销售额": 95000},
    {"类目": "美妆", "销售额": 65000},
]

df = pd.DataFrame(data)
print("【销售数据】")
print(df.to_string(index=False))

# TODO: 完成数据可视化准备
# 1. 按销售额排序
# 2. 计算各品类占比

print("\\n【可视化数据】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd

data = [
    {"类目": "电子产品", "销售额": 150000},
    {"类目": "服装", "销售额": 120000},
    {"类目": "食品", "销售额": 80000},
    {"类目": "家居", "销售额": 95000},
    {"类目": "美妆", "销售额": 65000},
]

df = pd.DataFrame(data)

# 按销售额降序排序
df_sorted = df.sort_values('销售额', ascending=False)

# 计算占比
total = df_sorted['销售额'].sum()
df_sorted['占比'] = df_sorted['销售额'] / total * 100

# 计算累计占比
df_sorted['累计占比'] = df_sorted['占比'].cumsum()

print("【可视化数据】")
print(df_sorted.to_string(index=False))

print(f"\\n【数据摘要】")
print(f"总销售额: {total:,}元")
print(f"最高品类: {df_sorted.iloc[0]['类目']} ({df_sorted.iloc[0]['销售额']:,}元)")
print(f"最低品类: {df_sorted.iloc[-1]['类目']} ({df_sorted.iloc[-1]['销售额']:,}元)")'''
    },
    "project10.html": {
        "title": "项目10：销售趋势预测 - 数析学院",
        "project_name": "项目10：销售趋势预测",
        "difficulty": "高级",
        "time": "60分钟",
        "tech": "Python + Pandas",
        "data_info": "历史销售数据",
        "tips_title": "预测分析技巧",
        "tips": [
            ("移动平均", "moving average"),
            ("趋势预测", "trend forecast"),
            ("rolling()", "滚动计算"),
            ("mean()", "平均值"),
        ],
        "goals": [
            "理解预测分析原理",
            "学会移动平均预测",
            "掌握趋势分析方法",
        ],
        "description": "某企业需要基于历史销售数据，使用移动平均法预测未来销售趋势。",
        "task_title": "请完成以下预测任务：",
        "tasks": [
            "计算移动平均值",
            "预测下月销售额",
        ],
        "default_code": '''import pandas as pd

# 历史销售数据
data = [
    {"月份": "2023-07", "销售额": 180000},
    {"月份": "2023-08", "销售额": 195000},
    {"月份": "2023-09", "销售额": 185000},
    {"月份": "2023-10", "销售额": 210000},
    {"月份": "2023-11", "销售额": 225000},
    {"月份": "2023-12", "销售额": 240000},
    {"月份": "2024-01", "销售额": 215000},
    {"月份": "2024-02", "销售额": 230000},
    {"月份": "2024-03", "销售额": 245000},
]

df = pd.DataFrame(data)
df['月份'] = pd.to_datetime(df['月份'])
print("【历史销售数据】")
print(df.to_string(index=False))

# TODO: 完成销售预测
# 1. 计算3个月移动平均
# 2. 预测下月销售额

print("\\n【预测结果】")
# 在这里编写代码...
''',
        "answer_code": '''import pandas as pd

data = [
    {"月份": "2023-07", "销售额": 180000},
    {"月份": "2023-08", "销售额": 195000},
    {"月份": "2023-09", "销售额": 185000},
    {"月份": "2023-10", "销售额": 210000},
    {"月份": "2023-11", "销售额": 225000},
    {"月份": "2023-12", "销售额": 240000},
    {"月份": "2024-01", "销售额": 215000},
    {"月份": "2024-02", "销售额": 230000},
    {"月份": "2024-03", "销售额": 245000},
]

df = pd.DataFrame(data)
df['月份'] = pd.to_datetime(df['月份'])

# 计算3个月移动平均
df['MA_3'] = df['销售额'].rolling(window=3).mean()

# 计算预测值（使用最近3个月的平均值）
last_3_avg = df['销售额'].tail(3).mean()

print("【销售趋势分析】")
print(df.to_string(index=False))

print(f"\\n【预测结果】")
print(f"最近3个月平均销售额: {last_3_avg:,.0f}元")
print(f"预测下月销售额: {last_3_avg:,.0f}元")

# 计算增长趋势
growth_rate = (df['销售额'].iloc[-1] - df['销售额'].iloc[0]) / len(df) / df['销售额'].iloc[0] * 100
print(f"月均增长率: {growth_rate:.2f}%")'''
    },
}

def generate_project_html(config):
    difficulty_class = "beginner" if config["difficulty"] == "初级" else "intermediate" if config["difficulty"] == "中级" else "advanced"
    
    tips_html = "\n".join([f'                    <div class="tip-item">\n                        <strong>{t[0]}</strong> - {t[1]}\n                    </div>' for t in config["tips"]])
    goals_html = "\n".join([f'                    <div class="tip-item">{g}</div>' for g in config["goals"]])
    tasks_html = "\n".join([f'                                <li style="padding:0.5rem 0;padding-left:1.5rem;position:relative;">\n                                    <span style="position:absolute;left:0;color:#3fb950;">✓</span>\n                                    {t}\n                                </li>' for t in config["tasks"]])
    
    default_code_escaped = config["default_code"].replace("\\", "\\\\").replace("`", "\\`")
    answer_code_escaped = config["answer_code"].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config["title"]}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="stylesheet" href="../styles.css">
    
    <!-- CodeMirror -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/theme/monokai.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/python/python.min.js"></script>
    
    <!-- Pyodide -->
    <script src="https://cdn.jsdelivr.net/pyodide/v0.24.1/full/pyodide.js"></script>
    
    <style>
        .project-page {{
            padding-top: 70px;
            min-height: 100vh;
            background: #f8fafc;
        }}

        .project-header {{
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 50%, #06b6d4 100%);
            color: white;
            padding: 2rem;
        }}

        .project-header-content {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .project-container {{
            max-width: 95%;
            margin: 1.5rem auto;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 1.5rem;
        }}

        .project-sidebar {{
            position: sticky;
            top: 90px;
        }}

        .tips-card {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.25rem;
            margin-bottom: 1rem;
        }}

        .tips-card h3 {{
            font-size: 1rem;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 0.75rem;
        }}

        .tip-item {{
            padding: 0.5rem 0;
            border-bottom: 1px solid #f1f5f9;
            color: #64748b;
            font-size: 0.85rem;
        }}

        .project-main {{
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }}

        .project-section {{
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 1.5rem;
        }}

        .section-content {{
            color: #475569;
            line-height: 1.6;
            font-size: 0.95rem;
        }}

        .task-description {{
            background: #eff6ff;
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid #3b82f6;
        }}

        .description-toggle {{
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
        }}

        .description-toggle i {{
            transition: transform 0.2s;
        }}

        .description-toggle.collapsed i {{
            transform: rotate(-90deg);
        }}

        .description-content {{
            overflow: hidden;
            transition: max-height 0.3s;
        }}

        .description-content.collapsed {{
            max-height: 0 !important;
        }}

        .description-inner {{
            padding-top: 1rem;
        }}
        
        .editor-container {{
            background: white;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            overflow: hidden;
            border: 1px solid #e2e8f0;
        }}
        
        .editor-toolbar {{
            background: #f8fafc;
            padding: 12px 16px;
            border-bottom: 1px solid #e2e8f0;
            display: flex;
            gap: 10px;
        }}
        
        .editor-toolbar button {{
            padding: 8px 16px;
            border: none;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        
        .btn-run {{
            background: #22c55e;
            color: white;
        }}
        
        .btn-run:hover {{
            background: #16a34a;
        }}
        
        .btn-reset {{
            background: #f1f5f9;
            color: #475569;
            border: 1px solid #e2e8f0;
        }}
        
        .btn-reset:hover {{
            background: #e2e8f0;
        }}
        
        .btn-answer {{
            background: #f59e0b;
            color: white;
        }}
        
        .btn-answer:hover {{
            background: #d97706;
        }}
        
        .btn-fullscreen {{
            background: #64748b;
            color: white;
        }}
        
        .btn-fullscreen:hover {{
            background: #475569;
        }}
        
        .editor-main {{
            border-bottom: 1px solid #e2e8f0;
        }}
        
        .CodeMirror {{
            height: 500px !important;
            font-size: 15px;
        }}
        
        .output-area {{
            background: #0f172a;
            padding: 16px;
        }}
        
        .output-area pre {{
            margin: 0;
            color: #e2e8f0;
            font-family: 'Fira Code', 'Consolas', monospace;
            font-size: 14px;
            line-height: 1.6;
            white-space: pre-wrap;
        }}
        
        .status {{
            padding: 8px 16px;
            background: #fffbeb;
            border-left: 3px solid #f59e0b;
            margin-bottom: 10px;
            border-radius: 0 6px 6px 0;
            color: #92400e;
        }}

        .difficulty-badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
        }}

        .difficulty-badge.beginner {{
            background-color: rgba(16, 185, 129, 0.15);
            color: #10b981;
        }}
        
        .difficulty-badge.intermediate {{
            background-color: rgba(245, 158, 11, 0.15);
            color: #f59e0b;
        }}
        
        .difficulty-badge.advanced {{
            background-color: rgba(239, 68, 68, 0.15);
            color: #ef4444;
        }}

        @media (max-width: 1200px) {{
            .project-container {{
                grid-template-columns: 1fr;
            }}

            .project-sidebar {{
                position: static;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 1rem;
            }}
        }}
    </style>
</head>
<body>
    <header class="navbar">
        <div class="navbar-container">
            <div class="navbar-logo" onclick="location.href='../index.html'">
                <i class="fas fa-chart-bar"></i>
                <span>数析学院</span>
            </div>
            <nav class="navbar-menu">
                <a href="../index.html" class="nav-link">首页</a>
                <a href="#courses" class="nav-link">课程中心</a>
                <a href="../projects.html" class="nav-link active">实战项目</a>
                <a href="../achievements.html" class="nav-link">成就殿堂</a>
            </nav>
            <button class="hamburger-menu" id="hamburger-menu">
                <i class="fas fa-bars"></i>
            </button>
            <div class="navbar-auth">
                <button id="login-btn" class="auth-btn login-btn">
                    <i class="fas fa-sign-in-alt"></i> 登录
                </button>
                <button id="register-btn" class="auth-btn register-btn">
                    <i class="fas fa-user-plus"></i> 注册
                </button>
            </div>
        </div>
    </header>

    <div class="project-page">
        <div class="project-header">
            <div class="project-header-content">
                <a href="../projects.html" class="project-back-link" style="color:white;text-decoration:none;display:inline-flex;align-items:center;gap:0.5rem;">
                    <i class="fas fa-arrow-left"></i> 返回实战项目
                </a>
                <div class="project-title-row" style="display:flex;align-items:center;gap:1rem;margin-top:0.5rem;">
                    <h1 style="font-size:1.75rem;font-weight:700;">{config["project_name"]}</h1>
                    <span class="difficulty-badge {difficulty_class}">{config["difficulty"]}</span>
                </div>
                <div style="display:flex;gap:1.5rem;margin-top:0.75rem;font-size:0.9rem;">
                    <span><i class="fas fa-clock"></i> 预计时长：{config["time"]}</span>
                    <span><i class="fas fa-code"></i> 技术栈：{config["tech"]}</span>
                    <span><i class="fas fa-database"></i> 数据量：{config["data_info"]}</span>
                </div>
            </div>
        </div>

        <div class="project-container">
            <div class="project-sidebar">
                <div class="tips-card">
                    <h3><i class="fas fa-lightbulb"></i> {config["tips_title"]}</h3>
{tips_html}
                </div>
                <div class="tips-card">
                    <h3><i class="fas fa-check-circle"></i> 学习目标</h3>
{goals_html}
                </div>
            </div>

            <div class="project-main">
                <div class="project-section">
                    <div class="description-toggle" onclick="toggleDescription()">
                        <span><i class="fas fa-book"></i> 题目描述 & 学习内容</span>
                        <i class="fas fa-chevron-down"></i>
                    </div>
                    <div class="description-content" id="description-content">
                        <div class="description-inner">
                            <div class="section-content">
                                <p>{config["description"]}</p>
                            </div>

                            <div class="task-description" style="margin-top:1rem;">
                                <h3>{config["task_title"]}</h3>
                                <ul style="list-style:none;padding:0;">
{tasks_html}
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="status" id="status">
                    <i class="fas fa-spinner fa-spin"></i> 环境加载中，请稍候...
                </div>

                <div class="editor-container">
                    <div class="editor-toolbar">
                        <button class="btn-run" onclick="runCode()">
                            <i class="fas fa-play"></i> 运行代码
                        </button>
                        <button class="btn-reset" onclick="resetCode()">
                            <i class="fas fa-undo"></i> 重置
                        </button>
                        <button class="btn-answer" onclick="toggleAnswer()">
                            <i class="fas fa-lightbulb"></i> 参考答案
                        </button>
                        <button class="btn-fullscreen" onclick="toggleFullscreen()">
                            <i class="fas fa-expand"></i> 全屏
                        </button>
                    </div>

                    <div class="editor-main">
                        <div id="code-editor"></div>
                    </div>

                    <div class="output-area">
                        <pre id="output">// 运行结果将显示在这里</pre>
                    </div>
                </div>

                <div id="answer-section" style="display:none; margin-top:20px; padding:16px; background:#f0fdf4; border-radius:8px; border:1px solid #86efac;">
                    <h3 style="margin:0 0 10px 0; color:#166534;"><i class="fas fa-check-circle"></i> 参考答案代码</h3>
                    <pre style="background:#e0f2fe; padding:12px; border-radius:6px; margin:0;">{answer_code_escaped}</pre>
                </div>

            </div>
        </div>
    </div>

    <script src="../script.js"></script>
    <script>
        let editor;
        let pyodide;
        let isRunning = false;

        const defaultCode = `{default_code_escaped}`;

        function initEditor() {{
            editor = CodeMirror(document.getElementById('code-editor'), {{
                mode: 'python',
                theme: 'monokai',
                lineNumbers: true,
                tabSize: 4,
                indentUnit: 4,
                indentWithTabs: false,
                value: defaultCode
            }});
        }}

        async function initPyodide() {{
            try {{
                pyodide = await loadPyodide();
                document.getElementById('status').innerHTML =
                    '<i class="fas fa-check-circle"></i> 环境加载完成！可以开始编写代码了。';
                document.getElementById('status').style.background = '#f0fdf4';
                document.getElementById('status').style.borderLeftColor = '#22c55e';
                document.getElementById('status').style.color = '#166534';
            }} catch (err) {{
                document.getElementById('status').innerHTML =
                    '<i class="fas fa-exclamation-triangle"></i> 环境加载失败: ' + err;
                document.getElementById('status').style.background = '#fef2f2';
                document.getElementById('status').style.borderLeftColor = '#ef4444';
                document.getElementById('status').style.color = '#991b1b';
            }}
        }}

        async function runCode() {{
            if (!pyodide) {{
                document.getElementById('output').textContent = '环境还在加载中，请稍候...';
                return;
            }}

            if (isRunning) {{
                return;
            }}

            isRunning = true;
            const code = editor.getValue();
            const outputElement = document.getElementById('output');

            outputElement.textContent = '⏳ 正在运行...';

            try {{
                let output = '';
                pyodide.runPython(`
import sys
from io import StringIO
sys.stdout = StringIO()
`);

                await pyodide.runPythonAsync(code);

                output = pyodide.runPython(`
result = sys.stdout.getvalue()
sys.stdout = sys.__stdout__
result
`);

                if (output.trim() === '') {{
                    output = '✅ 代码运行成功！没有输出内容。';
                }}

                outputElement.textContent = output;
            }} catch (err) {{
                outputElement.textContent = '❌ 运行错误:\\n' + err;
            }} finally {{
                isRunning = false;
            }}
        }}

        function resetCode() {{
            editor.setValue(defaultCode);
            document.getElementById('output').textContent = '// 运行结果将显示在这里';
        }}

        function toggleAnswer() {{
            const answerSection = document.getElementById('answer-section');
            if (answerSection.style.display === 'none') {{
                answerSection.style.display = 'block';
            }} else {{
                answerSection.style.display = 'none';
            }}
        }}

        function toggleFullscreen() {{
            const container = document.querySelector('.editor-container');
            if (!document.fullscreenElement) {{
                container.requestFullscreen().catch(err => {{
                    console.log('全屏失败:', err);
                }});
            }} else {{
                document.exitFullscreen();
            }}
        }}

        function toggleDescription() {{
            const content = document.getElementById('description-content');
            const toggle = document.querySelector('.description-toggle');
            content.classList.toggle('collapsed');
            toggle.classList.toggle('collapsed');
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            initEditor();
            initPyodide();

            const descriptionContent = document.getElementById('description-content');
            if (descriptionContent) {{
                descriptionContent.style.maxHeight = descriptionContent.scrollHeight + 'px';
            }}
        }});
    </script>
</body>
</html>'''
    return html

def main():
    for filename, config in PROJECTS_CONFIG.items():
        print(f"正在生成 {filename}...")
        html = generate_project_html(config)
        filepath = os.path.join(PROJECTS_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"✓ {filename} 生成完成")
    
    print("\n所有项目文件已更新！")

if __name__ == "__main__":
    main()
