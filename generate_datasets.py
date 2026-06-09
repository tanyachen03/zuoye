"""
数据集生成脚本 —— 一键生成 10 个商务数据分析项目的真实 CSV 数据。
运行: python generate_datasets.py
所有文件会写入 data/ 目录。
"""
import os
import csv
import random
from datetime import datetime, timedelta

random.seed(42)
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)


def write_csv(filename, header, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    print(f'已生成: {filename} ({len(rows)} 行)')


# ========== 1. 电商销售数据清洗 ==========
def gen_sales_cleaning():
    header = ['订单编号', '下单时间', '客户ID', '商品名称', '类别', '数量', '单价', '金额', '支付方式', '收货城市']
    categories = ['电子产品', '服装', '图书', '家居', '食品', '美妆']
    products = {
        '电子产品': ['iPhone 15', 'MacBook Air', 'AirPods Pro', 'iPad', '小米手环'],
        '服装': ['T恤', '牛仔裤', '羽绒服', '连衣裙', '运动鞋'],
        '图书': ['Python数据分析', '机器学习实战', '深度学习', '统计学', 'SQL必知必会'],
        '家居': ['台灯', '沙发', '床品四件套', '收纳箱', '加湿器'],
        '食品': ['坚果礼盒', '进口牛奶', '巧克力', '咖啡豆', '茶叶'],
        '美妆': ['口红', '面膜', '精华液', '香水', '洗面奶']
    }
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '南京', '西安', '重庆']
    payments = ['微信', '支付宝', '银行卡', '货到付款']
    rows = []
    base = datetime(2024, 1, 1)
    for i in range(1, 501):
        cat = random.choice(categories)
        prod = random.choice(products[cat])
        qty = random.randint(1, 5)
        price = round(random.uniform(20, 2000), 2)
        amount = round(qty * price, 2)
        date = (base + timedelta(days=random.randint(0, 179))).strftime('%Y-%m-%d')
        row = [
            f'ORD{i:06d}', date, f'C{random.randint(1000, 1200):04d}',
            prod, cat, qty, price, amount,
            random.choice(payments), random.choice(cities)
        ]
        # 人工注入脏数据（约 10%）
        if random.random() < 0.05:
            row[5] = ''  # 数量缺失
        if random.random() < 0.03:
            row[7] = ''  # 金额缺失
        if random.random() < 0.02:
            row = row * 1  # 复制一份模拟重复（下面额外加）
        rows.append(row)
    # 注入重复记录
    dup = random.sample(rows, 15)
    rows.extend(dup)
    # 注入异常值
    for _ in range(10):
        idx = random.randint(0, len(rows) - 1)
        rows[idx][5] = random.randint(100, 500)  # 异常大数量
        rows[idx][7] = round(rows[idx][5] * rows[idx][6], 2)
    write_csv('sales_raw.csv', header, rows)


# ========== 2. 销售趋势分析 ==========
def gen_sales_trend():
    header = ['日期', '销售额', '订单数', '客单价', '类别', '渠道']
    categories = ['电子产品', '服装', '图书', '家居', '食品', '美妆']
    channels = ['线上', '线下', '小程序', 'APP']
    rows = []
    base = datetime(2024, 1, 1)
    for d in range(365):
        date = (base + timedelta(days=d)).strftime('%Y-%m-%d')
        for cat in categories:
            for ch in channels:
                trend = 1 + d * 0.0015  # 轻微增长
                seasonal = 1 + 0.3 * ((d % 90) / 90)  # 季节性
                sales = round(random.uniform(3000, 15000) * trend * seasonal, 2)
                orders = random.randint(20, 150)
                aov = round(sales / orders, 2)
                rows.append([date, sales, orders, aov, cat, ch])
    write_csv('sales_trend.csv', header, rows)


# ========== 3. RFM 用户消费分层 ==========
def gen_rfm():
    header = ['客户ID', '最近一次消费(天前)', '消费频次', '消费总金额', '注册时长(月)', '会员等级']
    levels = ['普通', '银卡', '金卡', '钻石']
    rows = []
    for i in range(1, 1001):
        recency = random.randint(1, 365)
        frequency = random.randint(1, 80)
        monetary = round(random.uniform(50, 20000), 2)
        tenure = random.randint(1, 48)
        level = random.choices(levels, weights=[50, 25, 15, 10])[0]
        rows.append([f'C{i:04d}', recency, frequency, monetary, tenure, level])
    write_csv('rfm_data.csv', header, rows)


# ========== 4. 商品关联规则 ==========
def gen_association():
    header = ['订单号', '商品1', '商品2', '商品3', '商品4', '商品5']
    all_products = ['牛奶', '面包', '鸡蛋', '啤酒', '尿布', '薯片', '可乐', '饼干', '水果', '蔬菜', '肉类', '咖啡', '茶叶', '巧克力', '坚果']
    rows = []
    for i in range(1, 1501):
        n = random.randint(2, 5)
        items = random.sample(all_products, n)
        # 注入经典模式：牛奶+面包、啤酒+尿布 的概率较高
        if random.random() < 0.15:
            items = ['牛奶', '面包'] + [x for x in items if x not in ['牛奶', '面包']]
            items = items[:5]
        if random.random() < 0.1:
            items = ['啤酒', '尿布'] + [x for x in items if x not in ['啤酒', '尿布']]
            items = items[:5]
        while len(items) < 5:
            items.append('')
        rows.append([f'TXN{i:05d}'] + items)
    write_csv('transactions.csv', header, rows)


# ========== 5. 客户流失预测 ==========
def gen_churn():
    header = ['客户ID', '注册时长(月)', '使用频率', '消费金额', '最后一次使用(天前)', '客服投诉次数', '是否流失']
    rows = []
    for i in range(1, 2001):
        tenure = random.randint(1, 60)
        freq = random.randint(1, 30)
        spend = round(random.uniform(50, 10000), 2)
        last = random.randint(1, 365)
        tickets = random.randint(0, 10)
        # 简单流失规则：久未使用 + 低频率 -> 流失
        churn_score = (last > 90) + (freq < 5) + (tickets > 5)
        churn = 1 if churn_score >= 2 or random.random() < 0.05 else 0
        rows.append([f'C{i:04d}', tenure, freq, spend, last, tickets, churn])
    write_csv('churn_data.csv', header, rows)


# ========== 6. 销售仪表板 ==========
def gen_dashboard_data():
    header = ['月份', '区域', '产品', '销售额', '订单数', '利润', '增长率']
    regions = ['华北', '华东', '华南', '华中', '西南', '西北', '东北']
    products = ['A系列', 'B系列', 'C系列', 'D系列']
    rows = []
    for m in range(1, 13):
        for r in regions:
            for p in products:
                sales = round(random.uniform(50000, 500000), 2)
                orders = random.randint(100, 2000)
                profit = round(sales * random.uniform(0.1, 0.3), 2)
                growth = round(random.uniform(-0.2, 0.4), 4)
                rows.append([f'2024-{m:02d}', r, p, sales, orders, profit, growth])
    write_csv('dashboard_data.csv', header, rows)


# ========== 7. 时间序列预测 ==========
def gen_timeseries():
    header = ['日期', '历史销售额', '节日标记', '促销标记']
    rows = []
    base = datetime(2023, 1, 1)
    value = 5000
    for d in range(730):
        date = (base + timedelta(days=d)).strftime('%Y-%m-%d')
        trend = d * 3
        seasonal = 2000 * (1 + 0.5 * (d % 30) / 30)
        noise = random.uniform(-500, 500)
        value = max(1000, 5000 + trend + seasonal + noise)
        holiday = 1 if random.random() < 0.03 else 0
        promo = 1 if random.random() < 0.05 else 0
        if holiday:
            value *= 1.5
        if promo:
            value *= 1.3
        rows.append([date, round(value, 2), holiday, promo])
    write_csv('timeseries_sales.csv', header, rows)


# ========== 8. A/B 测试 ==========
def gen_ab_test():
    header = ['用户ID', '组别', '是否点击', '是否转化', '停留时长(秒)', '页面浏览数', '实验日期']
    rows = []
    base = datetime(2024, 3, 1)
    for i in range(1, 5001):
        group = random.choice(['对照组', '实验组'])
        date = (base + timedelta(days=random.randint(0, 13))).strftime('%Y-%m-%d')
        if group == '实验组':
            click = 1 if random.random() < 0.35 else 0
            convert = 1 if (click and random.random() < 0.28) else 0
        else:
            click = 1 if random.random() < 0.28 else 0
            convert = 1 if (click and random.random() < 0.20) else 0
        duration = round(random.uniform(10, 600), 2)
        pages = random.randint(1, 10)
        rows.append([f'U{i:05d}', group, click, convert, duration, pages, date])
    write_csv('ab_test_data.csv', header, rows)


# ========== 9. 文本情感分析 ==========
def gen_text_sentiment():
    header = ['评论ID', '商品', '评论文本', '评分', '点赞数', '评论日期']
    positive_texts = [
        '非常好用，物流很快，客服态度也很好！',
        '质量超出预期，会再次购买。',
        '包装精美，产品和描述一致，推荐！',
        '性价比很高，满意的一次购物。',
        '使用体验很棒，朋友都说好看。',
        '功能齐全，做工精细，好评！'
    ]
    neutral_texts = [
        '还行吧，一般般。',
        '产品正常，没有惊喜。',
        '价格还算合理。',
        '跟描述差不多，可以接受。'
    ]
    negative_texts = [
        '质量不好，跟图片不一样，不推荐。',
        '物流太慢了，客服也不回复。',
        '用了几天就出问题，失望。',
        '不值这个价格，不建议购买。',
        '包装有破损，体验差。'
    ]
    products = ['智能手机', '笔记本电脑', '耳机', '手表', '家电']
    rows = []
    base = datetime(2024, 1, 1)
    for i in range(1, 801):
        r = random.random()
        if r < 0.6:
            text = random.choice(positive_texts)
            rating = random.randint(4, 5)
        elif r < 0.8:
            text = random.choice(neutral_texts)
            rating = 3
        else:
            text = random.choice(negative_texts)
            rating = random.randint(1, 2)
        date = (base + timedelta(days=random.randint(0, 179))).strftime('%Y-%m-%d')
        likes = random.randint(0, 500)
        rows.append([f'R{i:04d}', random.choice(products), text, rating, likes, date])
    write_csv('reviews.csv', header, rows)


# ========== 10. KMeans 聚类 ==========
def gen_kmeans():
    header = ['客户ID', '年收入(万)', '消费评分(1-100)', '年龄', '性别', '城市等级']
    cities = ['一线城市', '二线城市', '三线城市', '四线及以下']
    clusters_centers = [(15, 30), (30, 50), (50, 80), (80, 95), (20, 15)]
    rows = []
    for i in range(1, 301):
        cx, cy = random.choice(clusters_centers)
        income = round(cx + random.uniform(-8, 8), 1)
        income = max(5, income)
        score = int(max(1, min(100, cy + random.randint(-15, 15))))
        age = random.randint(18, 70)
        gender = random.choice(['男', '女'])
        city = random.choice(cities)
        rows.append([f'K{i:04d}', income, score, age, gender, city])
    write_csv('customer_clusters.csv', header, rows)


if __name__ == '__main__':
    print('=' * 60)
    print('开始生成项目数据集...')
    print('=' * 60)
    gen_sales_cleaning()
    gen_sales_trend()
    gen_rfm()
    gen_association()
    gen_churn()
    gen_dashboard_data()
    gen_timeseries()
    gen_ab_test()
    gen_text_sentiment()
    gen_kmeans()
    print('=' * 60)
    print(f'全部数据集已生成到: {DATA_DIR}')
    print('=' * 60)
