#!/usr/bin/env python3
import json

# 读取课程数据
with open('courses_data.json', 'r', encoding='utf-8') as f:
    courses_data = json.load(f)

# 生成JSON
courses_json = json.dumps(courses_data, ensure_ascii=False)

# 其他数据
projects_data = [
    {"id":"data-cleaning","title":"数据清洗实战","icon":"🧹","difficulty":"入门","duration":"30分钟","dataset":"retail_orders.csv","description":"学习如何清洗真实零售订单数据"},
    {"id":"group-aggregate","title":"分组聚合分析","icon":"📊","difficulty":"入门","duration":"30分钟","dataset":"retail_orders.csv","description":"使用分组聚合分析销售数据"},
    {"id":"market-basket","title":"购物篮分析","icon":"🛒","difficulty":"进阶","duration":"45分钟","dataset":"market_basket.csv","description":"发现商品之间的关联规则"},
    {"id":"customer-clustering","title":"客户聚类分析","icon":"👥","difficulty":"进阶","duration":"45分钟","dataset":"customer_features.csv","description":"使用K-Means进行客户分群"},
    {"id":"data-visualization","title":"数据可视化","icon":"📈","difficulty":"进阶","duration":"45分钟","dataset":"retail_orders.csv","description":"创建专业的数据可视化图表"},
    {"id":"ab-testing","title":"A/B测试分析","icon":"🧪","difficulty":"进阶","duration":"45分钟","dataset":"ab_test.csv","description":"统计方法验证实验效果"},
    {"id":"time-series","title":"时间序列分析","icon":"⏰","difficulty":"进阶","duration":"45分钟","dataset":"time_series_sales.csv","description":"预测未来趋势"},
    {"id":"feature-engineering","title":"特征工程","icon":"🔧","difficulty":"高级","duration":"60分钟","dataset":"customer_features.csv","description":"创建有意义的特征"},
    {"id":"anomaly-detection","title":"异常值检测","icon":"🔍","difficulty":"高级","duration":"45分钟","dataset":"customer_features.csv","description":"发现数据中的异常"},
    {"id":"data-merge","title":"多数据集合并","icon":"🔗","difficulty":"进阶","duration":"45分钟","dataset":"retail_orders.csv","description":"整合多个数据源"}
]
projects_json = json.dumps(projects_data, ensure_ascii=False)

datasets = {
    "retail_orders.csv": """订单ID,客户ID,姓名,产品,数量,单价,订单日期
10001,C001,张伟,手机,2,5999,2024-01-15
10002,C002,李娜,电脑,1,8999,2024-01-15
10003,C003,王芳,耳机,3,299,2024-01-16
10004,C001,张伟,手机壳,5,39,2024-01-16
10005,C004,刘强,键盘,2,399,2024-01-17
10006,C005,陈静,鼠标,4,159,2024-01-17
10007,C002,李娜,显示器,1,2599,2024-01-18
10008,C006,赵敏,笔记本,3,89,2024-01-18
10009,C007,孙磊,平板电脑,1,3299,2024-01-19
10010,C003,王芳,路由器,2,299,2024-01-19""",
    "market_basket.csv": """item1,item2,item3,item4,item5
牛奶,面包,,,
面包,奶油,,,
牛奶,面包,奶油,,
面包,奶油,,,
牛奶,尿布,面包,啤酒,
牛奶,尿布,啤酒,,""",
    "customer_features.csv": """客户ID,年龄,年收入,购买次数,平均订单金额,活跃天数
C001,25,50000,15,300,120
C002,32,75000,22,450,180
C003,28,60000,18,320,150
C004,45,120000,35,800,200
C005,35,85000,28,520,165""",
    "ab_test.csv": """user_id,group,conversion,page_views,time_on_page
U001,control,1,5,120
U002,control,0,3,80
U003,control,1,4,95
U004,control,0,2,60
U005,control,1,5,110
U006,treatment,1,6,150
U007,treatment,1,7,180
U008,treatment,0,3,85
U009,treatment,1,5,125
U010,treatment,1,6,140""",
    "time_series_sales.csv": """date,sales
2024-01-01,1500
2024-01-02,1600
2024-01-03,1550
2024-01-04,1700
2024-01-05,1800
2024-01-06,1750
2024-01-07,1650
2024-01-08,1500
2024-01-09,1580
2024-01-10,1620"""
}
datasets_json = json.dumps(datasets, ensure_ascii=False)

achievements_data = [
    {"id":"first-course","title":"初学者","icon":"🎓","description":"完成第1门课程"},
    {"id":"five-courses","title":"五门课程","icon":"📚","description":"完成5门课程"},
    {"id":"all-courses","title":"全能分析师","icon":"🏆","description":"完成所有课程"},
    {"id":"first-project","title":"实战新手","icon":"🛠️","description":"完成第1个项目"},
    {"id":"five-projects","title":"项目达人","icon":"💼","description":"完成5个项目"},
    {"id":"all-projects","title":"项目大师","icon":"👑","description":"完成所有项目"},
    {"id":"streak-3","title":"三天学习","icon":"🔥","description":"连续学习3天"},
    {"id":"streak-7","title":"一周坚持","icon":"⭐","description":"连续学习7天"},
    {"id":"streak-30","title":"一个月坚持","icon":"🌟","description":"连续学习30天"},
    {"id":"run-50","title":"代码新手","icon":"💻","description":"累计运行代码50次"},
    {"id":"run-100","title":"代码达人","icon":"⚡","description":"累计运行代码100次"},
    {"id":"run-500","title":"代码大师","icon":"🚀","description":"累计运行代码500次"}
]
achievements_json = json.dumps(achievements_data, ensure_ascii=False)

# 读取HTML模板文件
with open('template.html', 'r', encoding='utf-8') as f:
    html_template = f.read()

# 替换占位符
html = html_template.replace('{courses_json}', courses_json)
html = html.replace('{projects_json}', projects_json)
html = html.replace('{datasets_json}', datasets_json)
html = html.replace('{achievements_json}', achievements_json)

# 写入HTML文件
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print(f"✓ HTML文件已生成")
print(f"✓ 文件大小: {len(html)} 字符")
print(f"✓ 课程: {len(courses_data)} 门")
print(f"✓ 项目: {len(projects_data)} 个")
print(f"✓ 数据集: {len(datasets)} 个")
print(f"✓ 成就: {len(achievements_data)} 个")
