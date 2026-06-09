# 📊 BizData · 商务数据分析在线教育平台

**一键可运行** 的商务数据分析在线学习平台，涵盖 5 门课程、10 个项目实战、综合测评、徽章成就系统。

## ✨ 功能概览

| 模块 | 说明 |
| --- | --- |
| 用户系统 | 注册 / 登录 / 个人中心 / 学习进度自动保存 |
| 课程体系 | 5 门课程（Python数据分析基础、Pandas高级、数据可视化、SQL商业分析、统计分析）|
| 章节系统 | 每门 3-5 章；独立 URL；完成状态持久化到数据库 |
| 项目实战 | 10 个真实场景；完整代码 + CSV 数据集 + 在线编辑器 + 完成标记 |
| 成就徽章 | 初来乍到 / 代码新秀 / 数据分析师 / 数据科学大师 / 完美学霸 / 坚持不懈 |
| 综合测评 | 20 题；自动评分；60 分及格；满分解锁“完美学霸” |
| 数据安全 | 代码运行沙箱化；数据库密码哈希（SHA-256） |

## 🚀 一键启动

```bash
# 1. 克隆/进入目录
cd /workspace

# 2. 安装依赖
pip install -r requirements.txt

# 3. 生成数据集（10 个项目的 CSV）
python generate_datasets.py

# 4. 启动平台
python app.py
```

然后访问 **http://localhost:5000**

## 📂 目录结构

```
/workspace
├── app.py                    # Flask 后端主程序
├── generate_datasets.py      # 自动生成 10 个项目数据集
├── requirements.txt
├── data/                     # 项目数据集（CSV）
├── platform.db               # SQLite 数据库（首次启动自动创建）
└── templates/
    ├── base.html             # 基础模板 + Bootstrap 5
    ├── index.html            # 首页
    ├── login.html / register.html
    ├── course_detail.html    # 课程详情 + 章节目录
    ├── chapter_page.html     # 章节详情 + 在线编辑器 + 测验
    ├── projects_list.html    # 项目列表
    ├── project.html          # 项目详情
    ├── assessment.html / assessment_result.html
    └── dashboard.html        # 个人中心 + 徽章展示
```

## 🔗 主要路由

```
/                          首页
/register /login /logout   认证
/course/<id>               课程详情（章节目录）
/course/<cid>/chapter/<chid>  章节详情（独立 URL）
/projects                  项目列表
/project/<pid>             项目详情（独立 URL）
/data/<filename>           下载项目数据集 CSV
/assessment                综合测评
/dashboard                 个人中心
/api/run_code              在线代码运行（POST）
/api/chapter/complete      标记章节完成（POST）
/api/project/complete      标记项目完成（POST）
```

## 🏅 徽章解锁指南

| 徽章 | 条件 |
| --- | --- |
| 🎉 初来乍到 | 首次登录 |
| 💻 代码新秀 | 完成 1 个项目 |
| 📊 数据分析师 | 完成 5 个项目 |
| 🏆 数据科学大师 | 完成 10 个项目 |
| 🎯 完美学霸 | 综合测评满分 |
| 🔥 坚持不懈 | 连续学习 7 天 |

## 📋 10 个项目清单

1. 🧹 电商销售数据清洗（缺失值、重复值、异常值）
2. 📈 销售趋势分析（时间序列 + 可视化）
3. 👥 用户消费分层（RFM 模型）
4. 🔗 商品关联规则挖掘（Apriori）
5. 🎯 客户流失预测（逻辑回归）
6. 📊 销售数据仪表板（Plotly/Dash 风格）
7. 🔮 时间序列预测（ARIMA）
8. 🧪 A/B 测试分析（卡方检验）
9. 📝 文本情感分析（NLP 简易实现）
10. 🧩 KMeans 聚类分析（用户分群）

## 🛠 技术栈

- **后端**: Python 3.11 + Flask 3.0 + Flask-SQLAlchemy
- **数据库**: SQLite（本地文件）
- **前端**: Bootstrap 5 + Bootstrap Icons
- **数据分析**: Pandas / NumPy / scikit-learn / statsmodels / SciPy / Matplotlib / Seaborn

## ⚠ 注意事项

- `api/run_code` 为教学演示用的服务端 Python 沙箱，生产环境请使用更严格的隔离方案（如 Docker、Pyodide）
- 项目数据集自动生成后保存在 `data/` 目录，每个项目详情页有「下载 CSV」入口

## 📝 License

教育用途，自由分发。
