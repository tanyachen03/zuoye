/**
 * Cloudflare Workers API - 商务数据分析教育平台
 * 
 * 主要功能：
 * - 用户认证（注册/登录）
 * - 课程和章节数据
 * - 学习进度追踪
 * - 成就徽章系统
 * - 综合测评
 * 
 * 限制：
 * - 无法在线执行 Python 代码
 * - 使用 Cloudflare D1 作为数据库
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;
    
    // CORS 头
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    // 处理 OPTIONS 请求
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    try {
      // 路由处理
      if (path === '/api/courses' || path.startsWith('/api/courses/')) {
        return handleCourses(request, env, path, corsHeaders);
      }
      
      if (path === '/api/projects') {
        return handleProjects(request, env, corsHeaders);
      }
      
      if (path === '/api/register') {
        return handleRegister(request, env, corsHeaders);
      }
      
      if (path === '/api/login') {
        return handleLogin(request, env, corsHeaders);
      }
      
      if (path === '/api/progress') {
        return handleProgress(request, env, corsHeaders);
      }
      
      if (path === '/api/assessment') {
        return handleAssessment(request, env, corsHeaders);
      }
      
      if (path === '/api/badges') {
        return handleBadges(request, env, corsHeaders);
      }

      // 默认返回 404
      return new Response(JSON.stringify({ error: 'Not Found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });

    } catch (error) {
      console.error('Error:', error);
      return new Response(JSON.stringify({ error: error.message }), {
        status: 500,
        headers: { 'Content-Type': 'application/json', ...corsHeaders }
      });
    }
  }
};

// ============================================
// 课程数据
// ============================================

const COURSES = [
  {
    id: 'python-basics',
    title: 'Python 数据分析基础',
    description: '从零开始学习 Python 基础语法和数据处理库 Pandas，为数据分析打下坚实基础。',
    level: '入门',
    duration: '8小时',
    color: 'primary',
    chapters: [
      {
        id: 'python-intro',
        title: 'Python 环境搭建与基础语法',
        duration: '1.5小时',
        theory: `## Python 简介

Python 是一种高级编程语言，以其简洁易读的语法和强大的功能而闻名。在数据分析领域，Python 是最流行的工具之一。

### 为什么选择 Python？

1. **简洁易学**：语法接近英语，学习曲线平缓
2. **生态丰富**：拥有大量的数据分析库（如 pandas, numpy, matplotlib）
3. **应用广泛**：从数据分析到机器学习，从 Web 开发到自动化

### Python 环境搭建

推荐使用 Anaconda 发行版，它包含了 Python 解释器和常用的科学计算库。

\`\`\`bash
# 下载 Anaconda
wget https://repo.anaconda.com/archive/Anaconda3-2023.03-Linux-x86_64.sh
bash Anaconda3-2023.03-Linux-x86_64.sh

# 验证安装
python --version
conda --version
\`\`\`

### 基本语法

\`\`\`python
# 变量赋值
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

# 循环遍历
for fruit in fruits:
    print(f"- {fruit}")
\`\`\``,
        exercises: [
          {
            question: 'Python 中变量的命名规则是什么？',
            options: ['可以数字开头', '可以包含下划线', '大小写敏感', '所有都可以'],
            answer: 1
          },
          {
            question: '下列哪个是合法的 Python 变量名？',
            options: ['2name', 'my-name', 'my_name', 'class'],
            answer: 2
          }
        ]
      },
      {
        id: 'pandas-basics',
        title: 'Pandas 数据处理入门',
        duration: '2小时',
        theory: `## Pandas 简介

Pandas 是 Python 中最强大的数据处理和分析库，提供了快速、灵活和表达力强的数据结构。

### 核心数据结构

1. **Series**：一维标签数组
2. **DataFrame**：二维表格数据

### 基本操作

\`\`\`python
import pandas as pd

# 创建 DataFrame
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
print(df['姓名'])                    # 选择单列
print(df[['姓名', '年龄']])           # 选择多列
print(df[df['年龄'] > 25])           # 条件筛选

# 数据清洗
df.dropna()                          # 删除缺失值
df.fillna(0)                         # 填充缺失值
df.drop_duplicates()                 # 删除重复行
\`\`\``,
        exercises: [
          {
            question: 'Pandas 中用于存储表格数据的核心数据结构是？',
            options: ['Series', 'DataFrame', 'Array', 'Matrix'],
            answer: 1
          }
        ]
      },
      {
        id: 'data-cleaning',
        title: '数据清洗与预处理',
        duration: '2.5小时',
        theory: `## 数据清洗的重要性

真实世界的数据往往充满噪声和缺失值，数据清洗是数据分析中最重要的步骤之一。

### 常见数据问题

1. **缺失值**：数据丢失或未记录
2. **重复数据**：相同记录重复出现
3. **格式错误**：数据类型不一致
4. **异常值**：明显偏离正常范围的值

### 实战技巧

\`\`\`python
import pandas as pd
import numpy as np

# 处理缺失值
df['年龄'].fillna(df['年龄'].mean(), inplace=True)  # 用均值填充
df.dropna(subset=['关键列'], inplace=True)          # 删除含缺失值的行

# 处理重复
df.drop_duplicates(inplace=True)

# 数据类型转换
df['日期'] = pd.to_datetime(df['日期'])
df['金额'] = pd.to_numeric(df['金额'], errors='coerce')

# 异常值检测
Q1 = df['金额'].quantile(0.25)
Q3 = df['金额'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
df = df[(df['金额'] >= lower_bound) & (df['金额'] <= upper_bound)]
\`\`\``,
        exercises: [
          {
            question: '处理缺失值时，用均值填充适用于什么类型的数据？',
            options: ['分类数据', '数值数据', '文本数据', '日期数据'],
            answer: 1
          }
        ]
      }
    ]
  },
  {
    id: 'data-visualization',
    title: '数据可视化与图表制作',
    description: '学习使用 Matplotlib 和 Seaborn 创建专业的数据可视化图表，让数据讲故事。',
    level: '入门',
    duration: '6小时',
    color: 'success',
    chapters: [
      {
        id: 'matplotlib-intro',
        title: 'Matplotlib 基础图表',
        duration: '2小时',
        theory: `## 数据可视化概述

数据可视化是将数据转换为图形表示的过程，帮助我们发现数据中的模式、趋势和异常。

### Matplotlib 简介

Matplotlib 是 Python 最流行的可视化库，可以创建各种静态、动态、交互式图表。

### 基础图表类型

\`\`\`python
import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 折线图
x = [1, 2, 3, 4, 5]
y = [2, 4, 6, 8, 10]
plt.figure(figsize=(10, 6))
plt.plot(x, y, marker='o', linewidth=2)
plt.title('销售趋势图')
plt.xlabel('月份')
plt.ylabel('销售额(万元)')
plt.grid(True)
plt.show()

# 柱状图
categories = ['产品A', '产品B', '产品C', '产品D']
values = [45, 67, 32, 89]
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['#3498db', '#2ecc71', '#e74c3c', '#f39c12'])
plt.title('产品销量对比')
plt.xlabel('产品')
plt.ylabel('销量')
plt.show()

# 饼图
sizes = [25, 35, 20, 20]
labels = ['北京', '上海', '广州', '深圳']
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.title('市场份额分布')
plt.show()
\`\`\``,
        exercises: [
          {
            question: 'Matplotlib 中用于创建柱状图的函数是？',
            options: ['plt.plot()', 'plt.bar()', 'plt.pie()', 'plt.scatter()'],
            answer: 1
          }
        ]
      }
    ]
  }
];

// ============================================
// 项目数据
// ============================================

const PROJECTS = [
  {
    id: 'sales-analysis',
    title: '电商销售数据分析',
    level: '初级',
    duration: '3小时',
    background: '某电商平台近一年的销售数据，包含订单信息、商品信息和客户信息。',
    goals: '分析销售趋势、识别爆款产品、发现客户购买行为模式。',
    dataset: 'sales_data.csv',
    tips: [
      '注意处理缺失值和异常订单',
      '按月聚合分析趋势更清晰',
      '使用分组聚合发现产品规律'
    ]
  },
  {
    id: 'customer-churn',
    title: '客户流失预测分析',
    level: '中级',
    duration: '4小时',
    background: '电信运营商客户数据，包含客户基本信息、使用行为和流失标签。',
    goals: '识别流失客户特征，建立预警机制。',
    dataset: 'customer_data.csv',
    tips: [
      '分析流失与哪些因素相关',
      '注意数据不平衡问题',
      '可视化客户画像'
    ]
  },
  {
    id: 'dashboard',
    title: '经营仪表板开发',
    level: '高级',
    duration: '5小时',
    background: '连锁零售企业多维度经营数据。',
    goals: '使用可视化工具创建实时更新的经营仪表板。',
    dataset: 'retail_data.csv',
    tips: [
      '设计清晰的数据层级',
      '选择合适的图表类型',
      '考虑数据刷新频率'
    ]
  }
];

// ============================================
// 处理函数
// ============================================

async function handleCourses(request, env, path, headers) {
  if (request.method === 'GET') {
    // 获取课程列表或单个课程
    const courseId = path.split('/')[3];
    
    if (courseId) {
      const course = COURSES.find(c => c.id === courseId);
      if (course) {
        return new Response(JSON.stringify(course), {
          headers: { 'Content-Type': 'application/json', ...headers }
        });
      }
      return new Response(JSON.stringify({ error: 'Course not found' }), {
        status: 404,
        headers: { 'Content-Type': 'application/json', ...headers }
      });
    }
    
    return new Response(JSON.stringify(COURSES), {
      headers: { 'Content-Type': 'application/json', ...headers }
    });
  }
}

async function handleProjects(request, env, headers) {
  if (request.method === 'GET') {
    return new Response(JSON.stringify(PROJECTS), {
      headers: { 'Content-Type': 'application/json', ...headers }
    });
  }
}

async function handleRegister(request, env, headers) {
  if (request.method === 'POST') {
    const { username, email, password } = await request.json();
    
    if (!username || !email || !password) {
      return new Response(JSON.stringify({ error: '缺少必填字段' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json', ...headers }
      });
    }
    
    // 检查用户是否存在
    const existing = await env.DB.prepare(
      'SELECT id FROM users WHERE email = ? OR username = ?'
    ).bind(email, username).first();
    
    if (existing) {
      return new Response(JSON.stringify({ error: '用户已存在' }), {
        status: 409,
        headers: { 'Content-Type': 'application/json', ...headers }
      });
    }
    
    // 创建用户（简单哈希，实际应使用更安全的方式）
    const hashedPassword = await hashPassword(password);
    const now = new Date().toISOString();
    
    const result = await env.DB.prepare(
      'INSERT INTO users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)'
    ).bind(username, email, hashedPassword, now).run();
    
    const token = generateToken(username);
    
    return new Response(JSON.stringify({
      success: true,
      token,
      user: { id: result.meta.last_row_id, username, email }
    }), {
      headers: { 'Content-Type': 'application/json', ...headers }
    });
  }
}

async function handleLogin(request, env, headers) {
  if (request.method === 'POST') {
    const { email, password } = await request.json();
    
    const user = await env.DB.prepare(
      'SELECT * FROM users WHERE email = ?'
    ).bind(email).first();
    
    if (!user) {
      return new Response(JSON.stringify({ error: '用户不存在' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json', ...headers }
      });
    }
    
    const isValid = await verifyPassword(password, user.password_hash);
    
    if (!isValid) {
      return new Response(JSON.stringify({ error: '密码错误' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json', ...headers }
      });
    }
    
    const token = generateToken(user.username);
    
    return new Response(JSON.stringify({
      success: true,
      token,
      user: { id: user.id, username: user.username, email: user.email }
    }), {
      headers: { 'Content-Type': 'application/json', ...headers }
    });
  }
}

async function handleProgress(request, env, headers) {
  // 获取/更新学习进度
  return new Response(JSON.stringify({ message: 'Progress API' }), {
    headers: { 'Content-Type': 'application/json', ...headers }
  });
}

async function handleAssessment(request, env, headers) {
  // 综合测评
  return new Response(JSON.stringify({ message: 'Assessment API' }), {
    headers: { 'Content-Type': 'application/json', ...headers }
  });
}

async function handleBadges(request, env, headers) {
  // 成就徽章
  return new Response(JSON.stringify({ message: 'Badges API' }), {
    headers: { 'Content-Type': 'application/json', ...headers }
  });
}

// ============================================
// 辅助函数
// ============================================

async function hashPassword(password) {
  const encoder = new TextEncoder();
  const data = encoder.encode(password + 'salt_12345');
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

async function verifyPassword(password, hash) {
  const passwordHash = await hashPassword(password);
  return passwordHash === hash;
}

function generateToken(username) {
  const payload = {
    username,
    exp: Date.now() + 7 * 24 * 60 * 60 * 1000 // 7天过期
  };
  return btoa(JSON.stringify(payload));
}
