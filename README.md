# 商务数据分析在线教育平台

一款完整的、可运行的、动态的商务数据分析在线教育平台。

## 技术栈

- **后端框架**: Flask 3.x
- **数据库**: SQLite + SQLAlchemy
- **前端**: Bootstrap 5 + Jinja2模板引擎
- **数据分析**: Pandas, NumPy, Matplotlib, scikit-learn

## 功能特性

### 用户系统
- 用户注册与登录
- 个人中心展示学习进度
- 学习进度自动保存

### 课程体系（5门课程，22个章节）
1. Python数据分析基础
2. Pandas数据处理
3. 数据可视化实战
4. 统计分析方法
5. 机器学习入门

### 实操项目（10个）
- 电商销售数据分析
- 客户流失预测
- 财务报表分析
- 市场调研数据分析
- 用户行为分析
- 销售预测建模
- 库存优化分析
- 客户分群分析
- A/B测试分析
- 营销效果评估

### 成就系统（6个徽章）
- 🌟 初学者 - 首次登录
- 📚 勤奋学员 - 完成第1门课程
- 🏆 全能选手 - 完成所有课程
- 💼 实战专家 - 完成所有项目
- 🎯 精准射手 - 首次测评及格
- 💯 完美学霸 - 测评满分

### 综合测评
- 20道选择题，涵盖所有课程内容
- 自动评分，60分及格
- 满分颁发"完美学霸"徽章

## 快速开始

### 安装依赖

```bash
pip install flask flask-sqlalchemy pandas numpy matplotlib scikit-learn scipy
```

### 启动服务

```bash
python app.py
```

### 访问地址

打开浏览器访问：http://localhost:5000

## 项目结构

```
/workspace/
├── app.py                 # 核心Flask应用
├── requirements.txt       # 依赖列表
├── README.md             # 项目说明
├── data/                 # 数据集目录
│   └── (自动生成的数据集文件)
├── instance/             # SQLite数据库目录
│   └── site.db          # 数据库文件
└── templates/            # HTML模板
    ├── base.html        # 基础模板
    ├── index.html       # 首页
    ├── login.html       # 登录页
    ├── register.html    # 注册页
    ├── dashboard.html   # 个人中心
    ├── course_detail.html # 课程详情
    ├── chapter_page.html  # 章节详情
    ├── projects_list.html # 项目列表
    ├── project.html       # 项目详情
    ├── assessment.html    # 综合测评
    └── assessment_result.html # 测评结果
```

## 使用说明

1. 首次访问首页后，点击"登录/注册"按钮创建账号
2. 浏览课程列表，选择感兴趣的课程开始学习
3. 每个章节包含理论内容、代码示例和随堂练习
4. 使用在线代码编辑器运行和测试代码
5. 完成章节后点击"标记完成"保存进度
6. 在项目页面完成实操项目并获取徽章
7. 完成所有学习后参加综合测评
